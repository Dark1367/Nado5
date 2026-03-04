from src.utils.Random import Random
import os

async def generate_exp_power_zero_limit(rand):
    A = rand.randint(-10, 10)
    while A == 0:
        A = rand.randint(-10, 10)
    
    p = rand.randint(1, 5)  
    
    b = rand.randint(-10, 10)
    while b == 0:  
        b = rand.randint(-10, 10)
    
    if A == 1:
        base_str = "e^{x}"
    elif A == -1:
        base_str = "e^{-x}"
    else:
        base_str = f"e^{{{A}x}}"
    
    if p == 1:
        denominator = "x"
    else:
        denominator = f"x^{{{p}}}"
    
    if b == 1:
        exponent_str = f"\\frac{{1}}{{{denominator}}}"
    elif b == -1:
        exponent_str = f"-\\frac{{1}}{{{denominator}}}"
    else:
        exponent_str = f"\\frac{{{b}}}{{{denominator}}}"
    
    limit_str = f"\\lim_{{x \\to \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def generate_exp_power_zero_limit_variations(rand):
    variation = rand.randint(1, 3)
    
    p = rand.randint(1, 5)
    b = rand.randint(-10, 10)
    while b == 0:
        b = rand.randint(-10, 10)
    
    if variation == 1:
        A = rand.randint(-10, 10)
        while A == 0:
            A = rand.randint(-10, 10)
        
        if A == 1:
            base_str = "e^{x}"
        elif A == -1:
            base_str = "e^{-x}"
        else:
            base_str = f"e^{{{A}x}}"
    
    elif variation == 2:
        A = rand.randint(-5, 5)
        while A == 0:
            A = rand.randint(-5, 5)
        
        B = rand.randint(-5, 5)
        if B == 0:
            if A == 1:
                base_str = "e^{x}"
            elif A == -1:
                base_str = "e^{-x}"
            else:
                base_str = f"e^{{{A}x}}"
        elif B > 0:
            if A == 1:
                base_str = f"e^{{x+{B}}}"
            elif A == -1:
                base_str = f"e^{{-x+{B}}}"
            else:
                base_str = f"e^{{{A}x+{B}}}"
        else:
            if A == 1:
                base_str = f"e^{{x{B}}}"  
            elif A == -1:
                base_str = f"e^{{-x{B}}}"  
            else:
                base_str = f"e^{{{A}x{B}}}"  
    
    else:  
        A_coef = rand.randint(-5, 5)
        while A_coef == 0:
            A_coef = rand.randint(-5, 5)
        
        B = rand.randint(-5, 5)
        while B == 0:
            B = rand.randint(-5, 5)
        
        if A_coef == 1:
            if B == 1:
                base_str = "e^{x}"
            elif B == -1:
                base_str = "e^{-x}"
            else:
                base_str = f"e^{{{B}x}}"
        elif A_coef == -1:
            if B == 1:
                base_str = "-e^{x}"
            elif B == -1:
                base_str = "-e^{-x}"
            else:
                base_str = f"-e^{{{B}x}}"
        else:
            if B == 1:
                base_str = f"{A_coef}e^{{x}}"
            elif B == -1:
                base_str = f"{A_coef}e^{{-x}}"
            else:
                base_str = f"{A_coef}e^{{{B}x}}"
    

    if p == 1:
        denominator = "x"
    else:
        denominator = f"x^{{{p}}}"
    
    if b == 1:
        exponent_str = f"\\frac{{1}}{{{denominator}}}"
    elif b == -1:
        exponent_str = f"-\\frac{{1}}{{{denominator}}}"
    else:
        exponent_str = f"\\frac{{{b}}}{{{denominator}}}"

    limit_str = f"\\lim_{{x \\to \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def generate_exp_power_zero_limit_with_trig(rand):
    trig_type = rand.randint(1, 2)
    p = rand.randint(1, 5)
    b = rand.randint(-10, 10)
    while b == 0:
        b = rand.randint(-10, 10)
    

    trig_funcs = ["\\sin x", "\\cos x", "\\tan x", "\\cot x"]
    trig_func = rand.choice(trig_funcs)
    

    if rand.chance(50):
        k = rand.randint(2, 5)
        if trig_func == "\\sin x":
            trig_func = f"\\sin({k}x)"
        elif trig_func == "\\cos x":
            trig_func = f"\\cos({k}x)"
        elif trig_func == "\\tan x":
            trig_func = f"\\tan({k}x)"
        elif trig_func == "\\cot x":
            trig_func = f"\\cot({k}x)"
    
    if trig_type == 1:
        A = rand.randint(-5, 5)
        while A == 0:
            A = rand.randint(-5, 5)
        
        if A == 1:
            base_str = f"e^{{{trig_func}}}"
        elif A == -1:
            base_str = f"e^{{-{trig_func}}}"
        else:
            base_str = f"e^{{{A}\\cdot{trig_func}}}"
    
    else:  
        A = rand.randint(-5, 5)
        while A == 0:
            A = rand.randint(-5, 5)
        
        if A == 1:
            base_str = "e^{x}"
        elif A == -1:
            base_str = "e^{-x}"
        else:
            base_str = f"e^{{{A}x}}"
        
        if b == 1:
            numerator = trig_func
        elif b == -1:
            numerator = f"-{trig_func}"
        else:
            numerator = f"{b}\\cdot{trig_func}"
        
        if p == 1:
            denominator = "x"
        else:
            denominator = f"x^{{{p}}}"
        
        exponent_str = f"\\frac{{{numerator}}}{{{denominator}}}"
        
        limit_str = f"\\lim_{{x \\to \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
        return limit_str
    
    if p == 1:
        denominator = "x"
    else:
        denominator = f"x^{{{p}}}"
    
    if b == 1:
        exponent_str = f"\\frac{{1}}{{{denominator}}}"
    elif b == -1:
        exponent_str = f"-\\frac{{1}}{{{denominator}}}"
    else:
        exponent_str = f"\\frac{{{b}}}{{{denominator}}}"
    
    limit_str = f"\\lim_{{x \\to \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    return limit_str

async def gen_three_two_lim(rand, n, variations=True, trig=True):
    primers = []
    
    for _ in range(n):
        if trig and rand.chance(30):  
            primer = await generate_exp_power_zero_limit_with_trig(rand)
        elif variations and rand.chance(50): 
            primer = await generate_exp_power_zero_limit_variations(rand)
        else: 
            primer = await generate_exp_power_zero_limit(rand)
        
        primers.append(primer)
    
    return primers
