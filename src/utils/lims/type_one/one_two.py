from src.utils.Random import Random
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
            s = f"{mult}x{f"^{{{deg}}}" if deg != 1 else ""}"
        else:
            deg = n
            while True:
                mult = rand.randint(-10, 10)
                if not force_nonzero or mult != 0:
                    break
            s = f"{mult}\\sqrt{{x{f"^{{{int(deg * 2)}}}" if deg * 2 != 1 else ""}}}"
        return s, deg, str(mult)

    if type == 1:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0:
                break
        deg = rand.randint(-3, 3)
        s = f"{mult}x{f"^{{{deg}}}" if deg != 1 else ""}"

    if type == 2:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0:
                break
        deg = rand.randint(-6, 6)/2
        if deg%1==0:
            deg = int(deg)
        s = f"{mult}\\sqrt{{x{f"^{{{int(deg*2)}}}" if deg*2 != 1 else ""}}}"

    if type == 3:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0:
                break
        deg = 0
        s = str(mult)

    if type == 4:
        funcs = ["sin", "cos", "tg", "ctg"]
        deg = 0
        mult = funcs[rand.randint(0, 3)]+"(x)"
        s = mult
        return s, deg, mult

    return s, deg, str(mult)

async def mnogochlen(rand, max_n=None, guaranteed_degree=None, allow_trig=False):
    if max_n is None:
        max_n = rand.randint(1, 4)
    
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
        s, deg, mult = await chlen(rand, None, allow_trig=allow_trig, force_nonzero=False)
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

async def generate_exponent(rand, allow_trig=False):
    choice = rand.choice(["linear", "constant", "reciprocal", "with_trig"])
    
    if choice == "constant":
        num = rand.randint(-5, 5)
        while num == 0:
            num = rand.randint(-5, 5)
        return str(num)
    
    elif choice == "reciprocal":
        D = rand.randint(1, 5)
        return f"\\frac{{{D}}}{{x}}"
    
    elif choice == "with_trig" and allow_trig:
        D = rand.randint(-5, 5)
        while D == 0:
            D = rand.randint(-5, 5)
        funcs = ["sin(x)", "cos(x)", "tg(x)", "ctg(x)"]
        trig = rand.choice(funcs)
        if rand.chance(50):
            return f"{D}x+{trig}"
        else:
            return trig
    
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

async def generate_limit_point(rand):
    choices = [
        ("\\infty", "inf"),
        ("0", "zero"),
        (str(rand.randint(1, 5)), "finite"),
    ]
    return rand.choice(choices)

async def generate_general_limit(rand):
    a, a_type = await generate_limit_point(rand)
    
    use_trig_in_PQ = rand.chance(30)
    use_trig_in_exp = rand.chance(20)  
    
    P_str, deg_P_str, coef_P = await mnogochlen(rand, allow_trig=use_trig_in_PQ)
    Q_str, deg_Q_str, coef_Q = await mnogochlen(rand, allow_trig=use_trig_in_PQ)
    
    R_str = await generate_exponent(rand, allow_trig=use_trig_in_exp)
    
    if rand.chance(40): 
        pass
    else:
        unc_type = rand.choice(["1^inf", "0^0", "inf^0", "0^inf", "inf^inf"])
        
        if unc_type == "1^inf" and a_type == "inf":
            deg = rand.randint(1, 4)
            P_str, _, _ = await mnogochlen(rand, guaranteed_degree=deg, allow_trig=False)
            Q_str, _, _ = await mnogochlen(rand, guaranteed_degree=deg, allow_trig=False)
            R_str = f"{rand.randint(2, 10)}x"
        
        elif unc_type == "0^0" and a_type == "finite":
            a_num = int(a) if a.isdigit() else 0
            if a_num != 0:
                P_str = f"(x-{a_num})" + ("*" + P_str if rand.chance(50) else "")
            R_str = f"x-{a_num}"
        
        elif unc_type == "inf^0" and a_type == "inf":
            deg_P = rand.randint(3, 5)
            deg_Q = rand.randint(1, 2)
            P_str, _, _ = await mnogochlen(rand, guaranteed_degree=deg_P, allow_trig=False)
            Q_str, _, _ = await mnogochlen(rand, guaranteed_degree=deg_Q, allow_trig=False)
            R_str = f"\\frac{{1}}{{x}}"
    
    if a == "\\infty":
        limit_expr = f"\\lim_{{x \\to \\infty}}"
    else:
        limit_expr = f"\\lim_{{x \\to {a}}}"
    
    primer = f"{limit_expr}\\left(\\frac{{{P_str}}}{{{Q_str}}}\\right)^{{{{{R_str}}}}}"
    return primer

async def gen_one_two_lim(rand, n):
    primers = []
    for _ in range(n):
        primer = await generate_general_limit(rand)
        primers.append(primer)
    return primers

