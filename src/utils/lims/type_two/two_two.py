from src.utils.Random import Random
import os

async def generate_coefficient(rand):
    coeff = rand.randint(-10, 10)
    while coeff == 0:
        coeff = rand.randint(-10, 10)
    
    if coeff > 0 and rand.random() < 0.3:  # Иногда убираем + для положительных
        return str(coeff)
    elif coeff > 0:
        return f"+{coeff}"
    else:
        return str(coeff)

async def generate_base_exponential(rand):
    A = await generate_coefficient(rand)
    
    variant = rand.choice([1, 2, 3])
    
    if variant == 1:
        return f"e^{{{A}x}}"
    elif variant == 2:
        if A[0] == '+':
            return f"e^{{-{A[1:]}x}}"
        else:
            return f"e^{{{A[1:] if A[0] == '-' else f'-{A}'}x}}"
    else:
        k = rand.randint(-5, 5)
        if k == 0:
            return f"e^{{{A}x}}"
        elif k > 0:
            return f"e^{{{k}{A}x}}"
        else:
            return f"e^{{{A}x{k}}}"

async def generate_exponent_fraction(rand):
    b = await generate_coefficient(rand)
    
    p_type = rand.choice([1, 2, 3, 4])
    
    if p_type == 1: 
        p = rand.choice([1, 2, 3])
        return f"\\frac{{{b}}}{{x^{{{p}}}}}"
    
    elif p_type == 2: 
        p_num = rand.choice([1, 2])
        p_den = rand.choice([2, 3, 4])
        if p_num == 1 and p_den == 2:
            return f"\\frac{{{b}}}{{\\sqrt{{x}}}}"
        else:
            return f"\\frac{{{b}}}{{x^{{\\frac{{{p_num}}}{{{p_den}}}}}}}"
    
    elif p_type == 3: 
        k = rand.randint(0, 5)
        p = rand.choice([1, 2])
        if k == 0:
            return f"\\frac{{{b}}}{{x^{{{p}}}}}"
        elif k > 0:
            return f"\\frac{{{b}}}{{x^{{{p}}} + {k}}}"
        else:
            return f"\\frac{{{b}}}{{x^{{{p}}} {k}}}"
    
    else:  
        return f"\\frac{{{b}}}{{x}}"

async def generate_infinity_limit(rand):
    base_str = await generate_base_exponential(rand)
    
    exp_str = await generate_exponent_fraction(rand)
    
    limit_form = rand.choice([1, 2, 3])
    
    if limit_form == 1:
        primer = f"\\lim_{{x \\to \\infty}} \\left({base_str}\\right)^{{{exp_str}}}"
    elif limit_form == 2:
        primer = f"\\lim_{{x \\to +\\infty}} \\left[{base_str}\\right]^{{{exp_str}}}"
    else:
        primer = f"\\lim_{{x \\to \\infty}} \\left({base_str}\\right)^{{\\left({exp_str}\\right)}}"
    
    return primer

async def generate_lim_2_2(rand, n):
    primers = []
    
    for i in range(n):
        primer = await generate_infinity_limit(rand)
        primers.append("2.2"+primer)
    
    return primers