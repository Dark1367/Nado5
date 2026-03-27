from src.utils.Random import Random
import os

async def generate_base_part(rand):
    base_type = rand.randint(1, 4)  
    
    if base_type == 1:  
        A = rand.randint(-10, 10)
        while A == 0:
            A = rand.randint(-10, 10)
        
        m = rand.randint(-3, 3)
        if m == 0:
            base_str = str(A)
        elif m == 1:
            base_str = f"{A}x"
        else:
            base_str = f"{A}x^{{{m}}}"
        return base_str
    
    elif base_type == 2:  
        A = rand.randint(-10, 10)
        while A == 0:
            A = rand.randint(-10, 10)
        
        if rand.chance(70):
            base_str = f"{A}\\sqrt{{x}}"
        else:
            k = rand.randint(2, 4)
            base_str = f"{A}\\sqrt[{k}]{{x}}"
        return base_str
    
    elif base_type == 3:
        A = rand.randint(-10, 10)
        while A == 0:
            A = rand.randint(-10, 10)
        return str(A)
    
    else:  
        funcs = ["sin", "cos", "tg", "ctg"]
        func = rand.choice(funcs)
        return f"{func}(x)"

async def generate_exponent_part(rand):
    b = rand.randint(-10, 10)
    while b == 0:
        b = rand.randint(-10, 10)
    
    n_type = rand.choice([0, 1, 2, 3])
    
    if n_type == 0: 
        n = rand.choice([1, 2, 3])
        if n == 1:
            exp_str = f"{b}x"
        else:
            exp_str = f"{b}x^{{{n}}}"
    
    elif n_type == 1:  
        n_form = rand.choice(["sqrt", "frac"])
        if n_form == "sqrt":
            exp_str = f"{b}\\sqrt{{x}}"
        else:
            exp_str = f"{b}x^{{\\frac{{1}}{{2}}}}"
    
    elif n_type == 2: 
        n = rand.choice([-1, -2, -3])
        exp_str = f"{b}x^{{{n}}}"
    
    else:  
        exp_str = str(b)
    
    return exp_str

async def generate_zero_plus_limit(rand):
    base_str = await generate_base_part(rand)
    
    exp_str = await generate_exponent_part(rand)
    
    primer = f"\\lim_{{x \\to 0^+}} \\left({base_str}\\right)^{{{exp_str}}}"
    
    return primer

async def generate_lim_2_1(rand, n):
    primers = []
    
    for i in range(n):
        primer = await generate_zero_plus_limit(rand)
        primers.append("2.1"+primer)
    
    return primers

