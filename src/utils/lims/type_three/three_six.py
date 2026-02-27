from src.utils.Random import Random
import os

rand = Random(str(os.urandom(8)))

async def generate_log_power_limit():
    A = rand.randint(-20, 20)
    while A == 0 or A == 1: 
        A = rand.randint(-20, 20)
    

    p = rand.randint(1, 5)  
    

    b = rand.randint(-10, 10)
    while b == 0:  
        b = rand.randint(-10, 10)
    

    if A == 1:
        arg = "x"
    elif A == -1:
        arg = "-x"
    else:
        arg = f"{A}x"
    

    base_str = f"\\ln\\left({arg}\\right)"

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

    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def generate_log_power_limit_variations():
    variation = rand.randint(1, 3)
    
  
    p = rand.randint(1, 5)
    b = rand.randint(-10, 10)
    while b == 0:
        b = rand.randint(-10, 10)
    
    if variation == 1:
        A = rand.randint(-10, 10)
        while A == 0:
            A = rand.randint(-10, 10)
        
        m = rand.randint(1, 5)
        
        if A == 1:
            if m == 1:
                arg = "x"
            else:
                arg = f"x^{{{m}}}"
        elif A == -1:
            if m == 1:
                arg = "-x"
            else:
                arg = f"-x^{{{m}}}"
        else:
            if m == 1:
                arg = f"{A}x"
            else:
                arg = f"{A}x^{{{m}}}"
    
    elif variation == 2:
       
        A = rand.randint(-8, 8)
        while A == 0:
            A = rand.randint(-8, 8)
        
        B = rand.randint(-8, 8)
        if B == 0:
            if A == 1:
                arg = "x"
            elif A == -1:
                arg = "-x"
            else:
                arg = f"{A}x"
        elif B > 0:
            if A == 1:
                arg = f"x+{B}"
            elif A == -1:
                arg = f"-x+{B}"
            else:
                arg = f"{A}x+{B}"
        else:  
            if A == 1:
                arg = f"x{B}"  
            elif A == -1:
                arg = f"-x{B}"  
            else:
                arg = f"{A}x{B}" 
    
    else:  
        r = rand.randint(2, 5)
        A = rand.randint(-8, 8)
        while A == 0:
            A = rand.randint(-8, 8)
        
        if r == 2:
            if A == 1:
                arg = "\\sqrt{x}"
            elif A == -1:
                arg = "\\sqrt{-x}"
            else:
                arg = f"\\sqrt{{{A}x}}"
        else:
            if A == 1:
                arg = f"\\sqrt[{r}]{{x}}"
            elif A == -1:
                arg = f"\\sqrt[{r}]{{-x}}"
            else:
                arg = f"\\sqrt[{r}]{{{A}x}}"
    
    
    base_str = f"\\ln\\left({arg}\\right)"
    
   
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
    
  
    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def generate_log_power_limit_with_composition():
    variation = rand.randint(1, 3)
  
    p = rand.randint(1, 5)
    b = rand.randint(-8, 8)
    while b == 0:
        b = rand.randint(-8, 8)
    
    if variation == 1:
     
        A = rand.randint(2, 10)
        
        if A == 1:
            inner_arg = "x"
        else:
            inner_arg = f"{A}x"
        
        inner_log = f"\\ln\\left({inner_arg}\\right)"
        base_str = f"\\ln\\left({inner_log}\\right)"
    
    elif variation == 2:
  
        A_coef = rand.randint(-6, 6)
        while A_coef == 0:
            A_coef = rand.randint(-6, 6)
        
        B = rand.randint(2, 8)
        
        if A_coef == 1:
            if B == 1:
                base_str = "\\ln(x)"
            else:
                base_str = f"\\ln({B}x)"
        elif A_coef == -1:
            if B == 1:
                base_str = "-\\ln(x)"
            else:
                base_str = f"-\\ln({B}x)"
        else:
            if B == 1:
                base_str = f"{A_coef}\\ln(x)"
            else:
                base_str = f"{A_coef}\\ln({B}x)"
    
    else: 
        A = rand.randint(2, 8)
        C = rand.randint(-5, 5)
        while C == 0:
            C = rand.randint(-5, 5)
        
        if A == 1:
            log_part = "\\ln(x)"
        else:
            log_part = f"\\ln({A}x)"
        
        if C > 0:
            base_str = f"{log_part}+{C}"
        else:
            base_str = f"{log_part}{C}"  
    
    
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
    
   
    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def generate_log_power_limit_with_trig():
    variation = rand.randint(1, 2)
    
   
    p = rand.randint(1, 5)
    b = rand.randint(-8, 8)
    while b == 0:
        b = rand.randint(-8, 8)
    
   
    trig_funcs = ["\\sin", "\\cos", "\\tan", "\\cot"]
    trig_func = rand.choice(trig_funcs)
    
  
    k = rand.randint(1, 4)
    arg = f"{k}x"
    
    if variation == 1:
        A = rand.randint(2, 6)
        
        if A == 1:
            trig_arg = f"{trig_func}({arg})"
        else:
            trig_arg = f"{A}{trig_func}({arg})"
        
        base_str = f"\\ln\\left({trig_arg}\\right)"
    
    else: 
        log_part = "\\ln(x)"
        trig_part = f"{trig_func}({arg})"
        
        base_str = f"{log_part}+{trig_part}"
    
   
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
    
   
    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def gen_three_six_lim(n, variations=True):
    primers = []
    
    for _ in range(n):
        if variations:
            choice = rand.randint(1, 4)
            if choice == 1:
                primer = await generate_log_power_limit()
            elif choice == 2:
                primer = await generate_log_power_limit_variations()
            elif choice == 3:
                primer = await generate_log_power_limit_with_composition()
            else:
                primer = await generate_log_power_limit_with_trig()
        else:
            primer = await generate_log_power_limit()
        
        primers.append(primer)
    
    return primers

