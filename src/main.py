from datetime import datetime, timedelta, timezone

import base64
import json
import jwt
from fastapi import HTTPException, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import select, Session

from src.api.templates import router as template_router
from src.api.users import router as user_router
from src.api import SessionDep
from src.database import PrivateUser, Generation, TableGeneration, TableTemplate, get_session
from src.utils import users as uu
from src.utils import templates as ut
from src.models import GenerateRequest, AccountRequest, GeneratePDFRequest, TemplateCreate
from src.utils.generate_lim import generate_lims
from src.utils.generations import create_genertion, list_generations
from src.utils.templates import get_user_templates
from src.utils.create_file import create_pdf

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(template_router)
app.include_router(user_router)

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"


async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user_from_request(request: Request, session: SessionDep):
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            return uu.get_by_email(email, session)
        except jwt.PyJWTError:
            return None
    return None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, session: SessionDep):
    current_user = get_current_user_from_request(request, session)

    if not current_user:
        return RedirectResponse(url="/login", status_code=302)

    return RedirectResponse(url="/main", status_code=302)


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, session: SessionDep, login: str = Form(...), password: str = Form(...)):
    current_user = uu.get_by_email(login, session)
    if current_user is None:
        return templates.TemplateResponse("Login.html", {"request": request, "error": "Неправильно введён логин"})
    if current_user.password_hash != uu.make_hash(PrivateUser(email=login, password=password)):
        return templates.TemplateResponse("Login.html", {"request": request, "error": "Неправильно введён пароль"})
    token = await create_access_token(data={"sub": login})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie("access_token", token, httponly=True)
    return response


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    session: SessionDep,
    login: str = Form(...),
    password: str = Form(...),
    password_conf: str = Form(...),
):
    if not uu.get_by_email(login, session) is None:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Такой логин уже существует"})
    if len(login) < 4:
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": "Логин должен содержать хотя-бы 4 символа"}
        )
    if len(password) < 5:
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": "Пароль должен содержать хотя-бы 5 символов"}
        )
    if password != password_conf:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Пароли не соответствуют"})
    user = PrivateUser(email=login, password=password)
    uu.create_user(user, session)
    token = await create_access_token(data={"sub": login})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie("access_token", token, httponly=True)
    return response


@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response


@app.get("/account", response_class=HTMLResponse)
async def account(request: Request, session: SessionDep):
    current_user = await get_current_user_from_request(request, session)

    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    tmpls = await ut.get_user_templates(current_user.id, session)
    return templates.TemplateResponse("account.html", {"request": request, "user": current_user, "templates": tmpls})


@app.post("/account")
async def account(request: Request, session: SessionDep, data: AccountRequest):
    current_user = await get_current_user_from_request(request, session)

    if data.btn == "show":
        generations = await list_generations(current_user.id, session)
        json_data = json.dumps(str(generations[data.index].id))
        encoded = base64.urlsafe_b64encode(json_data.encode()).decode()
        url = f"/primer_list?problems={encoded}"
        return RedirectResponse(url=url, status_code=302)

    if data.btn == "dell_gen":
        generations = await list_generations(current_user.id, session)
        generation_to_delete = generations[data.index]
        session.delete(generation_to_delete)
        session.commit()
        return RedirectResponse(url="/account", status_code=302)

    if data.btn == "dell_templ":
        templates = await get_user_templates(current_user.id, session)
        templates_to_delete = templates[data.index]
        session.delete(templates_to_delete)
        session.commit()
        return RedirectResponse(url="/account", status_code=302)


@app.get("/main", response_class=HTMLResponse)
async def main(request: Request, session: SessionDep):
    current_user = get_current_user_from_request(request, session)

    if not current_user:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("main.html", {"request": request, "user": current_user})


@app.get("/generate", response_class=HTMLResponse)
async  def generate(request: Request, session: SessionDep):
    current_user = await get_current_user_from_request(request, session)

    if not current_user:
        return RedirectResponse(url="/login", status_code=302)

    tmpls = await ut.get_user_templates(0, session) + await ut.get_user_templates(current_user.id, session)

    return templates.TemplateResponse("generate.html", {"request": request, "user": current_user, "templates": tmpls})


@app.get("/primer_list", response_class=HTMLResponse)
async def primer_list(request: Request, session: SessionDep):
    current_user = get_current_user_from_request(request, session)

    if not current_user:
        return RedirectResponse(url="/login", status_code=302)

    encoded = request.query_params.get("problems", "")
    decoded = base64.urlsafe_b64decode(encoded).decode()
    id = int(json.loads(decoded))

    statement = select(TableGeneration).where(TableGeneration.id == id)
    ses = next(get_session())
    results = ses.exec(statement)
    table_gen = results.first()
    problems = await generate_lims(table_gen.counters, str(table_gen.seed))

    ses.close()
    return templates.TemplateResponse("primer_list.html", {"request": request, "user": current_user, "problems": problems})


@app.post("/generate")
async def generate(request: Request, session: SessionDep, data: GenerateRequest):
    current_user = await get_current_user_from_request(request, session)

    if not current_user:
        return RedirectResponse(url="/login", status_code=302)

    user_generations_count = session.query(TableGeneration).filter(TableGeneration.user_id == current_user.id).count()
    
    if user_generations_count >= 5:
        return templates.TemplateResponse("Generate.html", {"request": request, "error": True})

    gen = Generation()
    gen.templates = [x for x in range(len(data.values))]
    gen.counters = data.values
    table_gen = await create_genertion(current_user.id, gen, session)

    json_data = json.dumps(str(table_gen.id))
    encoded = base64.urlsafe_b64encode(json_data.encode()).decode()

    url = f"/primer_list?problems={encoded}"
    return RedirectResponse(url=url, status_code=302)

@app.get("/get_user_info")
async def get_user_info(request: Request, session: SessionDep):
    current_user = await get_current_user_from_request(request, session)

    generations = await list_generations(current_user.id, session)

    gen_tab = ["", "", "", "", ""]
    for i in range(min(len(gen_tab), len(generations))):
        date = datetime.fromtimestamp(generations[i].creating_time)
        gen_tab[i] = f"Генерация от {date.day}.{date.month}"

    templates = await get_user_templates(current_user.id, session)

    temp_tab = ["", "", "", "", ""]
    for i in range(min(len(temp_tab), len(templates))):
        temp_tab[i] = templates[i].title

    data = {
        "gen": gen_tab,
        "temp": temp_tab
    }
    return data

@app.post("/generate_pdf")
async def generate_pdf(request: Request, session: SessionDep, data: GeneratePDFRequest):
    file_path = "primer_list.pdf"
    await create_pdf(data.problems)
    return FileResponse(
        file_path,
        filename="file.pdf"
    )
    
@app.post("/create_templ")
async def add_template(request: Request, session: SessionDep, template_data: TemplateCreate):
    current_user = await get_current_user_from_request(request, session)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    user_templates_count = session.query(TableTemplate).filter(TableTemplate.user_id == current_user.id).count()
    
    if user_templates_count >= 5:
        tmpls = ut.get_user_templates(current_user.id, session)
        return templates.TemplateResponse("Account.html", {"request": request, "error": True, "user": current_user, "templates": tmpls})

    template = TableTemplate(user_id=current_user.id, title=template_data.title, repr=template_data.repr)
    session.add(template)
    session.commit()
    session.refresh(template)
    return RedirectResponse(url="/account", status_code=302)