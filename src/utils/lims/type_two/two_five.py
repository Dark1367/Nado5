from src.utils.Random import Random
import os

async def generate_coefficient(rand):
    coeff = rand.randint(-10, 10)
    while coeff == 0:
        coeff = rand.randint(-10, 10)
    
    if coeff > 0 and rand.random() < 0.3:
        return str(coeff)
    elif coeff > 0:
        return f"+{coeff}"
    else:
        return str(coeff)

async def generate_simple_base(rand):
    A = await generate_coefficient(rand)
    

    m_type = rand.choice([1, 2, 3, 4])
    
    if m_type == 1: 
        m = rand.choice([1, 2, 3])
        if m == 1:
            return f"{A}x", m
        else:
            return f"{A}x^{{{m}}}", m
    
    elif m_type == 2:  
        m = rand.choice([0.5, 1.5, 2.5])
        if m == 0.5:
            return f"{A}\\sqrt{{x}}", m
        else:
            num = int(m * 2)
            return f"{A}x^{{\\frac{{{num}}}{{2}}}}", m
    
    elif m_type == 3: 
        m = rand.choice([-1, -2, -3])
        return f"{A}x^{{{m}}}", m
    
    else: 
        return str(A), 0

async def generate_composite_exponent(rand):
    b = await generate_coefficient(rand)
    c = await generate_coefficient(rand)
    
    case_type = rand.choice([1, 2, 3, 4, 5])
    
    if case_type == 1: 
        n = rand.choice([1, 2, 3])
        p = rand.choice([1, 2, 3])
        while p == n:
            p = rand.choice([1, 2, 3])
    
    elif case_type == 2:
        n = rand.choice([1, 2, 3])
        p = rand.choice([0.5, 1.5, 2.5])
    
    elif case_type == 3:  
        n = rand.choice([1, 2, 3])
        p = rand.choice([-1, -2, -3])
    
    elif case_type == 4:  
        n = rand.choice([-1, -2, -3])
        p = rand.choice([-1, -2, -3])
        while p == n:
            p = rand.choice([-1, -2, -3])
    
    else: 
        n = 0
        p = rand.choice([1, 2, 0.5, -1])
    
    if n > p:
        n, p = p, n
        b, c = c, b 
    
    if n == 0:
        term1 = b
    elif n == 1:
        term1 = f"{b}x"
    elif n == 0.5:
        term1 = f"{b}\\sqrt{{x}}"
    elif isinstance(n, float) and n != int(n):
        num = int(n * 2)
        term1 = f"{b}x^{{\\frac{{{num}}}{{2}}}}"
    else:
        term1 = f"{b}x^{{{int(n)}}}"
    
    if p == 0:
        term2 = c
    elif p == 1:
        term2 = f"{c}x"
    elif p == 0.5:
        term2 = f"{c}\\sqrt{{x}}"
    elif isinstance(p, float) and p != int(p):
        num = int(p * 2)
        term2 = f"{c}x^{{\\frac{{{num}}}{{2}}}}"
    else:
        term2 = f"{c}x^{{{int(p)}}}"
    
    if term2.startswith('-'):
        exponent_str = f"{term1}{term2}"
    else:
        exponent_str = f"{term1}+{term2}"
    
    return exponent_str

async def generate_simple_power_limit(rand):
    base_expr, m = await generate_simple_base(rand)
    
    exponent_expr = await generate_composite_exponent(rand)
    
    limit_type = rand.choice([1, 2, 3, 4])
    
    if limit_type == 1:
        primer = f"\\lim_{{x \\to 0}} \\left({base_expr}\\right)^{{{exponent_expr}}}"
    elif limit_type == 2:
        side = rand.choice(["+", "-"])
        primer = f"\\lim_{{x \\to 0^{side}}} \\left({base_expr}\\right)^{{{exponent_expr}}}"
    elif limit_type == 3:
        primer = f"\\lim_{{x \\to 0}} \\left[{base_expr}\\right]^{{{exponent_expr}}}"
    else:
        primer = f"\\lim_{{x \\to 0}} \\left({base_expr}\\right)^{{\\left({exponent_expr}\\right)}}"
    
    return primer

async def generate_lim_2_5(rand, n):
    primers = []
    
    for i in range(n):
        primer = await generate_simple_power_limit(rand)
        primers.append("2.5"+primer)
    
    return primers

