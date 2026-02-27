from src.utils.Random import Random
import os

rand = Random(str(os.urandom(8)))

async def generate_coefficient():
    coeff = rand.randint(-10, 10)
    while coeff == 0:
        coeff = rand.randint(-10, 10)
    
    if coeff > 0 and rand.random() < 0.3:
        return str(coeff)
    elif coeff > 0:
        return f"+{coeff}"
    else:
        return str(coeff)

async def generate_polynomial_term(degree, force_coeff=False):
    coeff = await generate_coefficient()
    
    if degree == 0:
        return coeff
    elif degree == 1:
        return f"{coeff}x"
    else:
        if isinstance(degree, float) and degree != int(degree):
            if degree == 0.5:
                return f"{coeff}\\sqrt{{x}}"
            else:
                num = int(degree * 2)
                den = 2
                return f"{coeff}x^{{\\frac{{{num}}}{{{den}}}}}"
        else:
            return f"{coeff}x^{{{int(degree)}}}"

async def generate_polynomial(min_degree=0.5, max_terms=3):
    m_type = rand.choice([1, 2, 3])
    
    if m_type == 1: 
        m = rand.choice([1, 2, 3])
    elif m_type == 2:  
        m = rand.choice([0.5, 1.5, 2.5])
    else: 
        m = rand.choice([0, -1, -2])
    
    A = await generate_coefficient()
    if m == 0:
        main_term = A
    elif m == 1:
        main_term = f"{A}x"
    elif m == 0.5:
        main_term = f"{A}\\sqrt{{x}}"
    elif isinstance(m, float) and m != int(m):
        num = int(m * 2)
        main_term = f"{A}x^{{\\frac{{{num}}}{{2}}}}"
    else:
        main_term = f"{A}x^{{{int(m)}}}"
    
    terms = [main_term]
    num_extra = rand.randint(0, max_terms - 1)
    
    for _ in range(num_extra):
        extra_deg = m + rand.choice([1, 2, 3, 0.5, 1.5])
        term = await generate_polynomial_term(extra_deg)
        terms.append(term)
    
    polynomial = terms[0]
    for term in terms[1:]:
        if not term.startswith('-') and not term.startswith('+'):
            polynomial += "+"
        polynomial += term
    
    return polynomial, m, A

async def generate_root():
    n_type = rand.choice([1, 2, 3])
    
    if n_type == 1: 
        return "\\sqrt{", "}", 2
    elif n_type == 2: 
        return "\\sqrt[3]{", "}", 3
    else:  
        n = rand.choice([4, 5, 6])
        return f"\\sqrt[{n}]{{", "}", n

async def generate_exponent():
    b = await generate_coefficient()
    
    p_type = rand.choice([1, 2, 3, 4])
    
    if p_type == 1:  
        p = rand.choice([1, 2, 3])
        if p == 1:
            return f"{b}x"
        else:
            return f"{b}x^{{{p}}}"
    
    elif p_type == 2:  
        p_form = rand.choice(["sqrt", "frac"])
        if p_form == "sqrt":
            return f"{b}\\sqrt{{x}}"
        else:
            return f"{b}x^{{\\frac{{1}}{{2}}}}"
    
    elif p_type == 3: 
        p = rand.choice([-1, -2, -3])
        return f"{b}x^{{{p}}}"
    
    else: 
        return str(b)

async def generate_root_limit():
    root_start, root_end, n = await generate_root()
    
    polynomial, m, A = await generate_polynomial()
    
    exponent = await generate_exponent()
    
    base_str = f"{root_start}{polynomial}{root_end}"
    
    limit_form = rand.choice([1, 2, 3])
    
    if limit_form == 1:
        primer = f"\\lim_{{x \\to 0^+}} \\left({base_str}\\right)^{{{exponent}}}"
    elif limit_form == 2:
        primer = f"\\lim_{{x \\to 0^+}} \\left[{base_str}\\right]^{{{exponent}}}"
    else:
        primer = f"\\lim_{{x \\to 0^+}} \\left({base_str}\\right)^{{\\left({exponent}\\right)}}"
    
    return primer

async def gen_two_three_lim(n):
    primers = []
    
    for i in range(n):
        primer = await generate_root_limit()
        primers.append(primer)
    
    return primers
