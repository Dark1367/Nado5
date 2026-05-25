from src.utils.Random import Random
import random
import os


async def try_calc(a, b, op):
    if op == "+":
        try:
            c = int(a) + int(b)
            return str(c)
        except:
            return f"{a}{"+" if b[0]!="-" else ""}{b}"
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
            deg = n
            while True:
                mult = rand.randint(-10, 10)
                if not force_nonzero or mult != 0:
                    break
            s_mult = mult
            if s_mult == 1:
                s_mult = ""
            if s_mult == -1:
                s_mult = "-"
            s = f"{s_mult}x{f"^{{{deg}}}" if deg != 1 else ""}"
        else:
            deg = n
            while True:
                mult = rand.randint(-10, 10)
                if not force_nonzero or mult != 0:
                    break
            s_mult = mult
            if s_mult == 1:
                s_mult = ""
            if s_mult == -1:
                s_mult = "-"
            s = f"{s_mult}\\sqrt{{x{f"^{{{int(deg * 2)}}}" if deg * 2 != 1 else ""}}}"
        return s, deg, str(mult)

    if type == 1:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0:
                break
        deg = rand.randint(-3, 3)
        if deg != 0:
            s_mult = mult
            if s_mult == 1:
                s_mult = ""
            if s_mult == -1:
                s_mult = "-"
            s = f"{s_mult}x{f"^{{{deg}}}" if deg != 1 else ""}"
        else:
            s = f"{mult}"

    if type == 2:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0:
                break
        deg = rand.randint(-6, 6)/2
        if deg%1==0:
            deg = int(deg)
        s_mult = mult
        if s_mult == 1:
            s_mult = ""
        if s_mult == -1:
            s_mult = "-"
        s = f"{s_mult}\\sqrt{{x{f"^{{{int(deg*2)}}}" if deg*2 != 1 else ""}}}"

    if type == 3:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0:
                break
        deg = 0
        s = str(mult)

    if type == 4:
        funcs = ["\sin", "\cos", "\\text{tg}", "\\text{ctg}"]
        deg = 0
        mult = funcs[rand.randint(0, 3)]+"(x)"
        s = mult
        return s, deg, mult

    return s, deg, str(mult)

async def mnogochlen(rand, max_n=None, guaranteed_degree=None, allow_trig=False):
    if max_n is None:
        max_n = rand.randint(4, 6)
    
    n = rand.randint(1, 3)
    parts = []
    nums = dict()

    if guaranteed_degree is not None:
        s, deg, mult = await chlen(rand, guaranteed_degree, allow_trig=False, force_nonzero=True)
    else:
        s, deg, mult = await chlen(rand, max_n, allow_trig=False, force_nonzero=True)
    
    deg = str(deg)
    parts.append(s)
    nums[deg] = mult

    for i in range(n):
        s, deg, mult = await chlen(rand, None, allow_trig=allow_trig, force_nonzero=True)
        deg = str(deg)
        parts.append(s)
        if deg in nums:
            nums[deg] = nums[deg] + "+" + mult
        else:
            nums[deg] = mult

    mnogoch = parts[0]
    for i in range(1, len(parts)):
        if parts[i][0] != "-":
            mnogoch += "+"
        mnogoch += parts[i]

    m_deg = max(nums.keys())
    m_mult = "0"
    mult_str = str(nums[m_deg])
    for x in mult_str.split("+"):
        m_mult = await try_calc(m_mult, x, "+")

    return mnogoch, m_deg, m_mult

async def generate_linear_exponent(rand, allow_trig=False):
    if allow_trig and rand.chance(20):
        D = rand.randint(-10, 10)
        while D == 0:
            D = rand.randint(-10, 10)
        E = rand.randint(-10, 10)
        trig_funcs = ["\sin(x)", "\cos(x)", "\\text{tg}(x)", "\\text{ctg}(x)"]
        trig = random.choice(trig_funcs)
        
        if E == 0:
            return f"{D}x+{trig}"
        elif E > 0:
            return f"{D}x+{E}+{trig}"
        else:
            return f"{D}x{E}+{trig}"
    else:
        D = rand.randint(-10, 10)
        while D == 0:
            D = rand.randint(-10, 10)
        
        E = rand.randint(-10, 10)
        
        if E == 0:
            return f"{D}x"
        elif E > 0:
            return f"{D}x+{E}"
        else:
            return f"{D}x{E}"

async def generate_root_limit(rand):
    n = rand.randint(2, 5)
    

    deg_den = rand.randint(2, 6)
    deg_num = rand.randint(0, deg_den - 1)
    

    allow_trig_in_frac = rand.chance(30)
    

    chislitel_str, actual_deg_num_str, coef_num = await mnogochlen(
        rand,
        max_n=deg_num, 
        guaranteed_degree=deg_num, 
        allow_trig=allow_trig_in_frac
    )
    znamenatel_str, actual_deg_den_str, coef_den = await mnogochlen(
        rand,
        max_n=deg_den, 
        guaranteed_degree=deg_den, 
        allow_trig=allow_trig_in_frac
    )
    

    try:
        actual_deg_num = float(actual_deg_num_str) if '/' in actual_deg_num_str else int(float(actual_deg_num_str))
    except:
        actual_deg_num = deg_num
    
    try:
        actual_deg_den = float(actual_deg_den_str) if '/' in actual_deg_den_str else int(float(actual_deg_den_str))
    except:
        actual_deg_den = deg_den
    

    if actual_deg_num >= actual_deg_den:
        extra_deg = actual_deg_num + 1
        extra_coef = rand.randint(1, 5)
        extra_part = f"{extra_coef}x^{{{extra_deg}}}" if extra_deg != 1 else f"{extra_coef}x"
        if not znamenatel_str.startswith("-"):
            znamenatel_str = extra_part + "+" + znamenatel_str
        else:
            znamenatel_str = extra_part + znamenatel_str
    

    allow_trig_in_exp = rand.chance(20)
    stepen_str = await generate_linear_exponent(rand, allow_trig=allow_trig_in_exp)
    

    sign = random.choice(["+", "-"])
    

    if n == 2:
        root_symbol = "\\sqrt"
        inside = f"{{1{sign}\\frac{{{chislitel_str}}}{{{znamenatel_str}}}}}"
    else:
        root_symbol = f"\\sqrt[{n}]"
        inside = f"{{1{sign}\\frac{{{chislitel_str}}}{{{znamenatel_str}}}}}"
    
    primer = f"\\lim_{{x \\to \\infty}}\\left({root_symbol}{inside}\\right)^{{{stepen_str}}}"
    return primer

async def generate_lim_1_3(rand, n):
    primers = []
    for _ in range(n):
        primer = await generate_root_limit(rand)
        primers.append(primer)
    return primers
