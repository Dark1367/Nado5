from fastapi import APIRouter, HTTPException

from src.api import SessionDep
from src.database import TableTemplate, Template
import src.utils.templates as ut

router = APIRouter(prefix="/api")


@router.get("/templates")
async def list_templates(session: SessionDep) -> list[TableTemplate]:
    return await ut.list_templates(session)


@router.post("/templates")
async def post_template(template: Template, session: SessionDep):
    table_template = await ut.create_template(template, session)
    return {"success": True, "template_id": table_template.id}


@router.get("/templates/{id}")
async def get_template(id: int, session: SessionDep) -> Template:
    template = await ut.get_template(id, session)
    if not template:
        raise HTTPException(status_code=404)
    return template

@router.delete("/templates/{id}")
async def delete_template(id: int, session: SessionDep):
    success = await ut.delete_template(id, session)
    if not success:
        raise HTTPException(status_code=404)
    return {"success": True}