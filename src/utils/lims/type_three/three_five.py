from src.utils.Random import Random
import os

async def generate_trig_power_limit(rand):
    A = rand.randint(-20, 20)
    while A == 0:  
        A = rand.randint(-20, 20)
    
    m = rand.randint(-10, 10)
    

    p = rand.randint(1, 5)
    
    b = rand.randint(-10, 10)
    while b == 0:
        b = rand.randint(-10, 10)
    
    c = rand.randint(-10, 10)
    while c == 0:
        c = rand.randint(-10, 10)
    

    trig_funcs = ["\\sin", "\\cos", "\\text{tg}", "\\text{ctg}"]
    trig_func = rand.choice(trig_funcs)
    

    k = rand.randint(1, 5)
    if k == 1:
        k = ""
    
    if rand.chance(30):  
        arg_type = rand.randint(1, 3)
        if arg_type == 1:
            arg = f"{k}x"
        elif arg_type == 2:
            d = rand.randint(1, 5)
            arg = f"{k}x+{d}"
        else:
            arg = f"{k}x-{rand.randint(1, 5)}"
    else:
        arg = f"{k}x"
    
    if A == 1:
        if m == 0:
            base_str = "1"
        elif m == 1:
            base_str = "x"
        else:
            base_str = f"x^{{{m}}}"
    elif A == -1:
        if m == 0:
            base_str = "-1"
        elif m == 1:
            base_str = "-x"
        else:
            base_str = f"-x^{{{m}}}"
    else:
        if m == 0:
            base_str = str(A)
        elif m == 1:
            base_str = f"{A}x"
        else:
            base_str = f"{A}x^{{{m}}}"
    
    if abs(c) == 1:
        if c == 1:
            trig_part = f"{trig_func}{{{arg}}}"
        else: 
            trig_part = f"-{trig_func}{{{arg}}}"
    else:
        trig_part = f"{c}\\cdot{trig_func}{{{arg}}}"
    
    if b > 0:
        if c > 0:
            numerator = f"{b}+{trig_part}"
        else:  
            numerator = f"{b}{trig_part}"  
    else:  
        if c > 0:
            numerator = f"{b}+{trig_part}"
        else:  
            numerator = f"{b}{trig_part}"
    

    numerator = numerator.replace("+-", "-").replace("-+", "-").replace("++", "+")
    

    if p == 1:
        denominator = "x"
    else:
        denominator = f"x^{{{p}}}"
    

    exponent_str = f"\\frac{{{numerator}}}{{{denominator}}}"
    

    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def generate_trig_power_limit_variations(rand):
    variation = rand.randint(1, 3)
    
 
    A = rand.randint(-15, 15)
    while A == 0:
        A = rand.randint(-15, 15)
    
    m = rand.randint(-8, 8)
    p = rand.randint(1, 5)
    b = rand.randint(-8, 8)
    while b == 0:
        b = rand.randint(-8, 8)
    
    c = rand.randint(-8, 8)
    while c == 0:
        c = rand.randint(-8, 8)
    
    if A == 1:
        if m == 0:
            base_str = "1"
        elif m == 1:
            base_str = "x"
        else:
            base_str = f"x^{{{m}}}"
    elif A == -1:
        if m == 0:
            base_str = "-1"
        elif m == 1:
            base_str = "-x"
        else:
            base_str = f"-x^{{{m}}}"
    else:
        if m == 0:
            base_str = str(A)
        elif m == 1:
            base_str = f"{A}x"
        else:
            base_str = f"{A}x^{{{m}}}"
    
    if variation == 1:

        trig_funcs = ["\\sin", "\\cos", "\\text{tg}", "\\text{ctg}"]
        trig_func = rand.choice(trig_funcs)
        
    
        k = rand.randint(1, 5)
        if rand.chance(40):
            d = rand.randint(1, 5)
            if rand.chance(50):
                arg = f"{k}x+{d}"
            else:
                arg = f"{k}x-{d}"
        else:
            arg = f"{k}x"
    
    elif variation == 2:
        trig_funcs = ["\\sin", "\\cos", "\\text{tg}", "\\text{ctg}"]
        trig1 = rand.choice(trig_funcs)
        trig2 = rand.choice(trig_funcs)
        
  
        k1 = rand.randint(1, 4)
        k2 = rand.randint(1, 4)
        
      
        d = rand.randint(-6, 6)
        while d == 0:
            d = rand.randint(-6, 6)
        
     
        if abs(c) == 1:
            if c == 1:
                trig_part1 = f"{trig1}{{{k1}x}}"
            else:
                trig_part1 = f"-{trig1}{{{k1}x}}"
        else:
            trig_part1 = f"{c}\\cdot{trig1}{{{k1}x}}"
        
        if abs(d) == 1:
            if d == 1:
                trig_part2 = f"+{trig2}{{{k2}x}}"
            elif d == -1:
                trig_part2 = f"-{trig2}{{{k2}x}}"
            else:
                trig_part2 = f"+{d}\\cdot{trig2}{{{k2}x}}"
        else:
            if d > 0:
                trig_part2 = f"+{d}\\cdot{trig2}{{{k2}x}}"
            else:
                trig_part2 = f"{d}\\cdot{trig2}{{{k2}x}}" 
        
        numerator = f"{b}+{trig_part1}{trig_part2}"
    
    else: 
        inv_trig_funcs = ["\\text{arcsin}", "\\text{arccos}", "\\text{arctan}", "\\text{arccot}"]
        trig_func = rand.choice(inv_trig_funcs)
        
 
        k = rand.randint(1, 5)
        if rand.chance(50):
            arg = f"\\frac{{1}}{{{k}x}}"
        else:
            arg = f"\\frac{{{k}}}{{x}}"
    

    if variation != 2:
        if abs(c) == 1:
            if c == 1:
                trig_part = f"{trig_func}{{{arg}}}"
            else:
                trig_part = f"-{trig_func}{{{arg}}}"
        else:
            trig_part = f"{c}\\cdot{trig_func}{{{arg}}}"
        
        if b > 0:
            numerator = f"{b}+{trig_part}"
        else:
            numerator = f"{b}{trig_part}" if trig_part.startswith("-") else f"{b}+{trig_part}"
    
 
    numerator = numerator.replace("+-", "-").replace("-+", "-").replace("++", "+")
    
 
    if p == 1:
        denominator = "x"
    else:
        denominator = f"x^{{{p}}}"
    

    exponent_str = f"\\frac{{{numerator}}}{{{denominator}}}"
    

    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def generate_trig_power_limit_with_exponential(rand):
    base_type = rand.randint(1, 2)

    p = rand.randint(1, 5)
    b = rand.randint(-8, 8)
    while b == 0:
        b = rand.randint(-8, 8)
    
    c = rand.randint(-8, 8)
    while c == 0:
        c = rand.randint(-8, 8)
   
    trig_funcs = ["\\sin", "\\cos", "\\text{tg}", "\\text{ctg}"]
    trig_func = rand.choice(trig_funcs)
    k = rand.randint(1, 5)
    

    if rand.chance(40):
        d = rand.randint(1, 5)
        arg = f"{k}x+{d}"
    else:
        arg = f"{k}x"
    
    if base_type == 1:
    
        A = rand.randint(-8, 8)
        while A == 0:
            A = rand.randint(-8, 8)
        
        if A == 1:
            base_str = "e^{x}"
        elif A == -1:
            base_str = "e^{-x}"
        else:
            base_str = f"e^{{{A}x}}"
    
    else:  
        A_coef = rand.randint(-6, 6)
        while A_coef == 0:
            A_coef = rand.randint(-6, 6)
        
        B = rand.randint(-6, 6)
        while B == 0:
            B = rand.randint(-6, 6)
        
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
    

    if abs(c) == 1:
        if c == 1:
            trig_part = f"{trig_func}{{{arg}}}"
        else:
            trig_part = f"-{trig_func}{{{arg}}}"
    else:
        trig_part = f"{c}\\cdot{trig_func}{{{arg}}}"
    
    if b > 0:
        numerator = f"{b}+{trig_part}"
    else:
        numerator = f"{b}{trig_part}" if trig_part.startswith("-") else f"{b}+{trig_part}"
    
    numerator = numerator.replace("+-", "-").replace("-+", "-")
    
    if p == 1:
        denominator = "x"
    else:
        denominator = f"x^{{{p}}}"
    
    exponent_str = f"\\frac{{{numerator}}}{{{denominator}}}"
    
    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def generate_lim_3_5(rand, n, variations=True):
    primers = []
    
    for _ in range(n):
        if variations:
            choice = rand.randint(1, 3)
            if choice == 1:
                primer = await generate_trig_power_limit(rand)
            elif choice == 2:
                primer = await generate_trig_power_limit_variations(rand)
            else:
                primer = await generate_trig_power_limit_with_exponential(rand)
        else:
            primer = await generate_trig_power_limit(rand)
        
        primers.append(primer)
    
    return primers
