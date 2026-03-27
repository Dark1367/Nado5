from src.utils.Random import Random
import os

async def fmt_exp(exp):
    if exp == 0:
        return "n"
    elif exp > 0:
        return f"n+{exp}"
    else:
        return f"n{exp}"

async def fmt_term(coef, base, exp):
    exp_str = await fmt_exp(exp)
    
    if coef == 1:
        return f"{base}^{{{exp_str}}}"
    elif coef == -1:
        return f"-{base}^{{{exp_str}}}"
    else:
        return f"{coef} \\cdot {base}^{{{exp_str}}}"

async def generate_limit(rand):
    bases = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    base_num = bases[rand.randint(0, len(bases)-1)]
    
    coef_num = rand.randint(1, 8)
    exp_num = rand.randint(-4, 4)
    
    const_num = rand.randint(1, 12)
    
    inner = await fmt_term(coef_num, base_num, exp_num)
    
    if const_num > 0:
        inner += f" + {const_num}"
    else:
        inner += f" - {abs(const_num)}"
    numerator = f"\\sqrt{{{inner}}}"
    
    base_den1 = bases[rand.randint(0, len(bases)-1)]
    coef_den1 = rand.randint(-8, 8)
    while coef_den1 == 0:
        coef_den1 = rand.randint(-8, 8)
    exp_den1 = rand.randint(-4, 4)
    
    base_den2 = bases[rand.randint(0, len(bases)-1)]
    coef_den2 = rand.randint(-8, 8)
    while coef_den2 == 0:
        coef_den2 = rand.randint(-8, 8)
    exp_den2 = rand.randint(-4, 4)
    
    denom1 = await fmt_term(coef_den1, base_den1, exp_den1)
    denom2 = await fmt_term(coef_den2, base_den2, exp_den2)
    
    if denom2.startswith('-'):
        denominator = denom1 + denom2
    else:
        denominator = denom1 + " + " + denom2
    
    denominator = denominator
    if denominator.startswith('+'):
        denominator = denominator[1:]
    
    primer = f"\\lim_{{n \\to \\infty}} \\frac{{{numerator}}}{{{denominator}}}"
    return primer

async def generate_lim_6_3(rand, n):
    primer = []
    for _ in range(n):
        primer.append("6.3"+await generate_limit(rand))
    return primer
