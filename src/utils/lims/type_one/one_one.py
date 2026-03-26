from src.utils.Random import Random
import os

def to_num(s):
    try:
        return float(s)
    except:
        return 0

async def try_calc(a, b, op):
    if op == "+":
        try:
            c = int(a) + int(b)
            return str(c)
        except:
            return f"{a}{'+' if str(b)[0]!='-' else ''}{b}"
    if op == "/":
        try:
            c = int(a) / int(b)
            if c % 1 == 0:
                return str(int(c))
            else:
                return f"\\frac{{{a}}}{{{b}}}"
        except:
            return f"\\frac{{{a}}}{{{b}}}"

async def chlen(rand, n=None, allow_trig=False, force_nonzero=False):
    if n is None:
        type = rand.randint(1, 4 if allow_trig else 3)
    elif n == 0:
        type = rand.randint(3, 4 if allow_trig else 3)
    else:
        type = rand.randint(1, 2)
    
    if type == 1:
        deg = n if n is not None else rand.randint(-3, 3)
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0: break
        s = f"{mult}x{f'^{{{deg}}}' if deg != 1 else ''}" if deg != 0 else str(mult)
        return s, deg, str(mult)

    if type == 2:
        deg = n if n is not None else rand.randint(-6, 6)/2
        if deg % 1 == 0: deg = int(deg)
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0: break
        s = f"{mult}\\sqrt{{x{f'^{{{int(deg*2)}}}' if deg*2 != 1 else ''}}}"
        return s, deg, str(mult)

    if type == 3:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0: break
        return str(mult), 0, str(mult)

    if type == 4:
        funcs = ["sin", "cos", "tg", "ctg"]
        f = funcs[rand.randint(0, 3)] + "(x)"
        return f, 0, f

async def mnogochlen(rand, max_n=None, guaranteed_degree=None, allow_trig=False):
    if max_n is None: max_n = rand.randint(4, 6)
    n = rand.randint(1, 3)
    parts = []
    nums = dict()

    s, deg, mult = await chlen(rand, guaranteed_degree if guaranteed_degree is not None else max_n, allow_trig=False, force_nonzero=True)
    deg_str = str(deg)
    parts.append(s)
    nums[deg_str] = mult

    for i in range(n):
        s, deg, mult = await chlen(rand, None, allow_trig=allow_trig, force_nonzero=False)
        deg_str = str(deg)
        parts.append(s)
        if deg_str in nums:
            nums[deg_str] = nums[deg_str] + "+" + mult
        else:
            nums[deg_str] = mult

    mnogoch = parts[0]
    for i in range(1, len(parts)):
        if parts[i][0] != "-": mnogoch += "+"
        mnogoch += parts[i]

    m_deg = max(nums.keys(), key=lambda x: float(x))
    m_mult = "0"
    for x in str(nums[m_deg]).split("+"):
        m_mult = await try_calc(m_mult, x, "+")

    return mnogoch, m_deg, m_mult

async def generate_lim(rand):
    diff_choice = rand.choice([1, 1, 1, 2, 0])
    if diff_choice == 0:
        deg_den = rand.randint(2, 6)
        deg_num = deg_den - 1
    elif diff_choice == 1:
        deg_den = rand.randint(2, 6)
        deg_num = deg_den - 1
    else:
        deg_den = rand.randint(3, 6)
        deg_num = deg_den - 2
    
    chisl, act_deg_num_s, coef_num_s = await mnogochlen(rand, max_n=deg_num, guaranteed_degree=deg_num)
    znam, act_deg_den_s, coef_znam_s = await mnogochlen(rand, max_n=deg_den, guaranteed_degree=deg_den)
    
    act_deg_num = float(act_deg_num_s)
    act_deg_den = float(act_deg_den_s)
    coef_num = to_num(coef_num_s)
    coef_znam = to_num(coef_znam_s)

    if act_deg_num >= act_deg_den:
        extra_deg = act_deg_num + 1
        extra_coef = rand.randint(1, 5)
        extra_part = f"{extra_coef}x^{{{int(extra_deg)}}}" if extra_deg != 1 else f"{extra_coef}x"
        znam = extra_part + ("+" if znam[0] != "-" else "") + znam
        act_deg_den = extra_deg
        coef_znam = float(extra_coef)

    D = rand.randint(-10, 10)
    while D == 0: D = rand.randint(-10, 10)
    E = rand.randint(-10, 10)
    stepen_str = f"{D}x{f'+{E}' if E > 0 else (E if E < 0 else '')}"
    
    sign_str = rand.choice(["+", "-"])
    sign_val = 1 if sign_str == "+" else -1
    
    primer = f"\\lim_{{x \\to \\infty}}(1{sign_str}\\frac{{{chisl}}}{{{znam}}})^{{{stepen_str}}}"
    
    if act_deg_den == act_deg_num + 1:
        chisl_exp_prod = sign_val * coef_num * D
        A = await try_calc(str(int(chisl_exp_prod) if chisl_exp_prod%1==0 else chisl_exp_prod), str(int(coef_znam)), "/")
        solution = f"e^{{{A}}}"
    elif act_deg_den > act_deg_num + 1:
        solution = "1"
    else:
        solution = "e^{\\infty}" 

    return primer, solution

async def generate_lim_1_1(rand, n):
    primers = []
    for _ in range(n):
        primer, solution = await generate_lim(rand)
        primers.append(primer)
    return primers