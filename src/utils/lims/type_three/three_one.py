from src.utils.Random import Random
import os

async def generate_inf_power_zero_limit(rand):
    A = rand.randint(-20, 20)
    while A == 0:  
        A = rand.randint(-20, 20)
    
    m = rand.randint(-10, 10)
    
    n = rand.randint(1, 5)  
    
    b = rand.randint(-20, 20)
    while b == 0: 
        b = rand.randint(-20, 20)
    
    if A == 1:
        base_str = f"x^{{{m}}}"
    elif A == -1:
        base_str = f"-x^{{{m}}}"
    else:
        base_str = f"{A}x^{{{m}}}"
    
    if m == 0:
        if A == 1:
            base_str = "1"
        elif A == -1:
            base_str = "-1"
        else:
            base_str = str(A)
    
    exponent_str = f"\\frac{{{b}}}{{{f'x^{{{n}}}' if n != 1 else 'x'}}}"
    
    limit_str = f"\\lim_{{x \\to \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def generate_lim_3_1(rand, n):
    primers = []
    for _ in range(n):
        primer = await generate_inf_power_zero_limit(rand)
        primers.append(primer)
    return primers
