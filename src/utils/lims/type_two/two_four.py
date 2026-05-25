from src.utils.Random import Random
import os

async def generate_coefficient(rand):
    coeff = rand.randint(-10, 10)
    while coeff == 0:
        coeff = rand.randint(-10, 10)

    if coeff == 1:
        coeff = ""
    elif coeff == -1:
        coeff = "-"

    return str(coeff)

async def generate_term_with_degree(rand, degree):
    coeff = await generate_coefficient(rand)
    
    if degree == 0:
        return coeff
    elif degree == 1:
        return f"{coeff}x"
    elif isinstance(degree, float) and degree != int(degree):
        if degree == 0.5:
            return f"{coeff}\\sqrt{{x}}"
        else:
            num = int(degree * 2)
            return f"{coeff}x^{{\\frac{{{num}}}{{2}}}}"
    else:
        return f"{coeff}x^{{{int(degree)}}}"

async def generate_polynomial_base(rand):
    degree_type = rand.choice([1, 2, 3, 4])
    
    if degree_type == 1:  
        m = rand.choice([0, 1, 2])
        n = m + rand.choice([1, 2])
    
    elif degree_type == 2: 
        m = rand.choice([0.5, 1.5, 2.5])
        n = rand.choice([1, 2, 3])
        if rand.random() < 0.5:
            m, n = n, m 
    
    elif degree_type == 3: 
        m = rand.choice([-1, -2])
        n = rand.choice([0, 1, 2])
    
    else:  
        m = rand.choice([0, 1, 2, 0.5])
        n = m
    
    term1 = await generate_term_with_degree(rand, m)
    term2 = await generate_term_with_degree(rand, n)

    min_deg = min(m, n) if isinstance(m, (int, float)) and isinstance(n, (int, float)) else 0
    
    base_expression = term1
    if not term2.startswith('-') and not term2.startswith('+'):
        base_expression += "+"
    base_expression += term2
    
    num_extra = rand.randint(0, 2)
    for _ in range(num_extra):
        extra_deg = min_deg + rand.choice([2, 3, 4, 0.5, 1.5])
        extra_term = await generate_term_with_degree(rand, extra_deg)
        if not extra_term.startswith('-') and not extra_term.startswith('+'):
            base_expression += "+"
        base_expression += extra_term
    
    return base_expression

async def generate_exponent(rand):
    b = await generate_coefficient(rand)
    
    p_type = rand.choice([1, 2, 3, 4, 5])
    
    if p_type == 1: 
        p = rand.choice([1, 2, 3])
        if p == 1:
            return f"{b}x"
        else:
            return f"{b}x^{{{p}}}"
    
    elif p_type == 2: 
        p_form = rand.choice(["sqrt", "frac", "cbrt"])
        if p_form == "sqrt":
            return f"{b}\\sqrt{{x}}"
        elif p_form == "cbrt":
            return f"{b}\\sqrt[3]{{x}}"
        else:
            return f"{b}x^{{\\frac{{1}}{{2}}}}"
    
    elif p_type == 3:  
        p = rand.choice([-1, -2, -3])
        return f"{b}x^{{{p}}}"
    
    elif p_type == 4: 
        p = rand.choice([0.5, 1.5, 2.5])
        return f"{b}x^{{{p}}}"
    
    else:  
        return str(b)

async def generate_polynomial_power_limit(rand):
    base_expr = await generate_polynomial_base(rand)
    
    exponent = await generate_exponent(rand)
    
    limit_type = rand.choice([1, 2, 3])
    
    if limit_type == 1:
        primer = f"\\lim_{{x \\to 0}} \\left({base_expr}\\right)^{{{exponent}}}"
    elif limit_type == 2:
        side = rand.choice(["+", "-"])
        primer = f"\\lim_{{x \\to 0}} \\left({base_expr}\\right)^{{{exponent}}}"
    else:
        primer = f"\\lim_{{x \\to 0}} \\left[{base_expr}\\right]^{{{exponent}}}"
    
    return primer

async def generate_lim_2_4(rand, n):
    primers = []
    
    for i in range(n):
        primer = await generate_polynomial_power_limit(rand)
        primers.append(primer)
    
    return primers
