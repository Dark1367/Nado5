from src.utils.Random import Random
import os

async def chlen(rand, n=None, force_nonzero=False):
    if n is None:
        type = rand.randint(1, 3)
    elif n == 0:
        type = 3
    else:
        type = rand.randint(1, 2)
        if type == 1:
            deg = n
            while True:
                mult = rand.randint(-10, 10)
                if not force_nonzero or mult != 0:
                    break
            if mult == 1:
                smult = ""
            elif mult == -1:
                smult = "-"
            else:
                smult = mult
            s = f"{smult}x{f"^{{{deg}}}" if deg != 1 else ""}"
        else:
            deg = n
            while True:
                mult = rand.randint(-10, 10)
                if not force_nonzero or mult != 0:
                    break
            if mult == 1:
                smult = ""
            elif mult == -1:
                smult = "-"
            else:
                smult = mult
            s = f"{smult}\\sqrt{{x{f"^{{{int(deg * 2)}}}" if deg * 2 != 1 else ""}}}"
        return s, deg, str(mult)

    if type == 1:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0:
                break
        deg = rand.randint(-3, 3)
        if mult == 1:
            smult = ""
        elif mult == -1:
            smult = "-"
        else:
            smult = mult
        s = f"{smult}x{f"^{{{deg}}}" if deg != 1 else ""}"

    if type == 2:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0:
                break
        deg = rand.randint(-6, 6)/2
        if deg%1==0:
            deg = int(deg)
        if mult == 1:
            smult = ""
        elif mult == -1:
            smult = "-"
        else:
            smult = mult
        s = f"{smult}\\sqrt{{x{f"^{{{int(deg*2)}}}" if deg*2 != 1 else ""}}}"

    if type == 3:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0:
                break
        deg = 0
        s = str(mult)

    return s, deg, str(mult)

async def mnogochlen(rand, max_n=None, guaranteed_degree=None):
    if max_n is None:
        max_n = rand.randint(3, 6)
    
    n = rand.randint(2, 4)
    parts = []
    nums = {}

    if guaranteed_degree is not None:
        s, deg, mult = await chlen(rand, guaranteed_degree, force_nonzero=True)
    else:
        s, deg, mult = await chlen(rand, max_n, force_nonzero=True)
    
    deg = str(deg)
    parts.append(s)
    nums[deg] = mult

    for i in range(n):
        s, deg, mult = await chlen(rand, None, force_nonzero=False)
        deg = str(deg)
        parts.append(s)
        if deg in nums:
            nums[deg] = nums[deg] + "+" + mult
        else:
            nums[deg] = mult

    mnogoch = parts[0]
    for i in range(1, len(parts)):
        if parts[i][0] != "-":
            mnogoch += "+"
        mnogoch += parts[i]


    mnogoch = mnogoch.replace("+-", "-")
    mnogoch = mnogoch.replace("1x", "x")
    mnogoch = mnogoch.replace("-1x", "-x")
    
    return mnogoch

async def generate_polynomial_power_sum_limit(rand):

    poly_degree = rand.randint(2, 5)
    P_x = await mnogochlen(rand, guaranteed_degree=poly_degree)
    
 
    if rand.chance(70):
        extra_degree = poly_degree + rand.randint(1, 3)
        extra_coef = rand.randint(2, 10)
        extra_term = f"{extra_coef}x^{{{extra_degree}}}"
        
        if P_x[0] != "-":
            P_x = extra_term + "+" + P_x
        else:
            P_x = extra_term + P_x
    

    p = rand.randint(1, 5)
    q = rand.randint(1, 5)
    

    while q == p:
        q = rand.randint(1, 5)
    
 
    b = rand.randint(-10, 10)
    while b == 0:
        b = rand.randint(-10, 10)
    
    c = rand.randint(-10, 10)
    while c == 0:
        c = rand.randint(-10, 10)
    

    if p == 1:
        first_term = f"\\frac{{{b}}}{{x}}"
    else:
        first_term = f"\\frac{{{b}}}{{x^{{{p}}}}}"
   
    if q == 1:
        second_term = f"\\frac{{{c}}}{{x}}"
    else:
        second_term = f"\\frac{{{c}}}{{x^{{{q}}}}}"
    

    if c > 0:
        exponent_str = first_term + "+" + second_term
    else:
     
        exponent_str = first_term + second_term
    

    if abs(b) == 1:
        if p == 1:
            if b == 1:
                first_term = "\\frac{1}{x}"
            else:
                first_term = "-\\frac{1}{x}"
        else:
            if b == 1:
                first_term = f"\\frac{{1}}{{x^{{{p}}}}}"
            else:
                first_term = f"-\\frac{{1}}{{x^{{{p}}}}}"
    

    if abs(c) == 1:
        if q == 1:
            if c == 1:
                second_term = "+\\frac{1}{x}"
            elif c == -1:
                second_term = "-\\frac{1}{x}"
            else:
                second_term = f"+{c}\\frac{{1}}{{x}}"
        else:
            if c == 1:
                second_term = f"+\\frac{{1}}{{x^{{{q}}}}}"
            elif c == -1:
                second_term = f"-\\frac{{1}}{{x^{{{q}}}}}"
    
 
    if c > 0:
        exponent_str = first_term + "+" + second_term
    else:
        exponent_str = first_term + second_term
    
 
    if exponent_str.startswith("+"):
        exponent_str = exponent_str[1:]
    

    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({P_x}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def generate_polynomial_power_sum_limit_variations(rand):

    variation = rand.randint(1, 3)
    

    poly_degree = rand.randint(2, 4)
    P_x = await mnogochlen(rand, guaranteed_degree=poly_degree)
    

    p = rand.randint(1, 4)
    q = rand.randint(1, 4)
    while q == p:
        q = rand.randint(1, 4)
    
    b = rand.randint(-8, 8)
    while b == 0:
        b = rand.randint(-8, 8)
    
    c = rand.randint(-8, 8)
    while c == 0:
        c = rand.randint(-8, 8)
    
    if variation == 1:
     
        pass
    
    elif variation == 2:
  
        c = abs(c)
    
    else:  
        a = rand.randint(-3, 3)
        while a == 0:
            a = rand.randint(-3, 3)
        
    
        if p == 1:
            first_frac = f"\\frac{{{b}}}{{x}}"
        else:
            first_frac = f"\\frac{{{b}}}{{x^{{{p}}}}}"
        
        if q == 1:
            second_frac = f"\\frac{{{c}}}{{x}}"
        else:
            second_frac = f"\\frac{{{c}}}{{x^{{{q}}}}}"
        
      
        if c > 0:
            exponent_str = f"{a}+{first_frac}+{second_frac}"
        else:
            exponent_str = f"{a}+{first_frac}{second_frac}"
        

        exponent_str = exponent_str.replace("+-", "-").replace("++", "+")
        
        limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({P_x}\\right)}}^{{{exponent_str}}}"
        return limit_str
    
 
    if p == 1:
        first_term = f"\\frac{{{b}}}{{x}}"
    else:
        first_term = f"\\frac{{{b}}}{{x^{{{p}}}}}"

    if variation == 2:
       
        if q == 1:
            second_term = f"-\\frac{{{c}}}{{x}}"
        else:
            second_term = f"-\\frac{{{c}}}{{x^{{{q}}}}}"
        exponent_str = first_term + second_term
    else:
     
        if q == 1:
            second_term = f"\\frac{{{c}}}{{x}}"
        else:
            second_term = f"\\frac{{{c}}}{{x^{{{q}}}}}"
        
        if c > 0:
            exponent_str = first_term + "+" + second_term
        else:
            exponent_str = first_term + second_term

    exponent_str = exponent_str.replace("+-", "-")
    
    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({P_x}\\right)}}^{{{exponent_str}}}"
    return limit_str

async def generate_polynomial_power_sum_limit_with_diff_polys(rand):
    poly_type = rand.randint(1, 3)
    
  
    p = rand.randint(1, 5)
    q = rand.randint(1, 5)
    while q == p:
        q = rand.randint(1, 5)
    
    b = rand.randint(-10, 10)
    while b == 0:
        b = rand.randint(-10, 10)
    
    c = rand.randint(-10, 10)
    while c == 0:
        c = rand.randint(-10, 10)
    
    if poly_type == 1:
     
        poly_degree = rand.randint(2, 4)
        P_x = await mnogochlen(rand, guaranteed_degree=poly_degree)
    
    elif poly_type == 2:
     
        base_degree = rand.randint(2, 3)
        P_x = await mnogochlen(rand, guaranteed_degree=base_degree)
        
     
        high_degree = base_degree + rand.randint(3, 6)
        high_coef = rand.randint(2, 10)
        high_term = f"{high_coef}x^{{{high_degree}}}"
        
        if P_x[0] != "-":
            P_x = high_term + "+" + P_x
        else:
            P_x = high_term + P_x
    
    else: 
        poly_degree = rand.randint(2, 3)
        P_x = await mnogochlen(rand, guaranteed_degree=poly_degree)
        
     
        root_deg = rand.randint(1, 3) / 2
        root_coef = rand.randint(2, 8)
        
        if root_deg == 0.5:
            root_term = f"{root_coef}\\sqrt{{x}}"
        elif root_deg == 1:
            root_term = f"{root_coef}\\sqrt{{x^{2}}}"
        elif root_deg == 1.5:
            root_term = f"{root_coef}\\sqrt{{x^{3}}}"
        else:
            root_term = f"{root_coef}\\sqrt{{x^{{{int(root_deg*2)}}}}}"
        
        if P_x[0] != "-":
            P_x = root_term + "+" + P_x
        else:
            P_x = root_term + P_x
    
    if p == 1:
        first_term = f"\\frac{{{b}}}{{x}}"
    else:
        first_term = f"\\frac{{{b}}}{{x^{{{p}}}}}"
    
    if q == 1:
        second_term = f"\\frac{{{c}}}{{x}}"
    else:
        second_term = f"\\frac{{{c}}}{{x^{{{q}}}}}"
    
    if c > 0:
        exponent_str = first_term + "+" + second_term
    else:
        exponent_str = first_term + second_term

    exponent_str = exponent_str.replace("+-", "-")
    
    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({P_x}\\right)}}^{{{exponent_str}}}"
    return limit_str

async def generate_lim_3_4(rand, n, variations=True):
    primers = []
    
    for _ in range(n):
        if variations:
            choice = rand.randint(1, 3)
            if choice == 1:
                primer = await generate_polynomial_power_sum_limit(rand)
            elif choice == 2:
                primer = await generate_polynomial_power_sum_limit_variations(rand)
            else:
                primer = await generate_polynomial_power_sum_limit_with_diff_polys(rand)
        else:
            primer = await generate_polynomial_power_sum_limit(rand)
        
        primers.append("3.4"+primer)
    
    return primers
