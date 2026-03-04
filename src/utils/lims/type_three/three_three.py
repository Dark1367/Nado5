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
            s = f"{mult}x{f"^{{{deg}}}" if deg != 1 else ""}"
        else:
            deg = n
            while True:
                mult = rand.randint(-10, 10)
                if not force_nonzero or mult != 0:
                    break
            s = f"{mult}\\sqrt{{x{f"^{{{int(deg * 2)}}}" if deg * 2 != 1 else ""}}}"
        return s, deg, str(mult)

    if type == 1:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0:
                break
        deg = rand.randint(-3, 3)
        s = f"{mult}x{f"^{{{deg}}}" if deg != 1 else ""}"

    if type == 2:
        while True:
            mult = rand.randint(-10, 10)
            if not force_nonzero or mult != 0:
                break
        deg = rand.randint(-6, 6)/2
        if deg%1==0:
            deg = int(deg)
        s = f"{mult}\\sqrt{{x{f"^{{{int(deg*2)}}}" if deg*2 != 1 else ""}}}"

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
        max_n = rand.randint(4, 6)
    
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

async def generate_root_power_zero_limit(rand):

    r = rand.randint(2, 5)
    

    n = rand.randint(1, 5)
    

    b = rand.randint(-10, 10)
    while b == 0: 
        b = rand.randint(-10, 10)

    if rand.chance(70):
  
        poly_degree = rand.randint(2, 5)
        P_x = await mnogochlen(rand, guaranteed_degree=poly_degree)
        
      
        if rand.chance(50):
        
            extra_degree = poly_degree + rand.randint(1, 3)
            extra_coef = rand.randint(2, 10)
            extra_term = f"{extra_coef}x^{{{extra_degree}}}"
            
            if P_x[0] != "-":
                P_x = extra_term + "+" + P_x
            else:
                P_x = extra_term + P_x
    
  
    else:
     
        P_x = await mnogochlen(rand)
    
  
    P_x = P_x.replace("++", "+").replace("+-", "-")
    if P_x.startswith("+"):
        P_x = P_x[1:]
    
   
    if r == 2:
        base_str = f"\\sqrt{{{P_x}}}"
    elif r == 3:
        base_str = f"\\sqrt[3]{{{P_x}}}"
    else:
        base_str = f"\\sqrt[{r}]{{{P_x}}}"
    
   
    if n == 1:
        denominator = "x"
    else:
        denominator = f"x^{{{n}}}"
    
   
    if b == 1:
        exponent_str = f"\\frac{{1}}{{{denominator}}}"
    elif b == -1:
        exponent_str = f"-\\frac{{1}}{{{denominator}}}"
    else:
        exponent_str = f"\\frac{{{b}}}{{{denominator}}}"
    

    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def generate_root_power_zero_limit_variations(rand):
    variation = rand.randint(1, 3)
    
    r = rand.randint(2, 5)
    n = rand.randint(1, 5)
    b = rand.randint(-10, 10)
    while b == 0:
        b = rand.randint(-10, 10)
    
    if variation == 1:
        return await generate_root_power_zero_limit(rand)
    
    elif variation == 2:
        m = rand.randint(2, 6) 
        a = rand.randint(2, 10)  
        
   
        lower_poly = await mnogochlen(rand, max_n=m-1)
        
     
        if a == 1:
            P_x = f"x^{{{m}}}+{lower_poly}"
        else:
            P_x = f"{a}x^{{{m}}}+{lower_poly}"
        
     
        P_x = P_x.replace("++", "+").replace("+-", "-")
        if P_x.startswith("+"):
            P_x = P_x[1:]
    
    else: 
        num_degree = rand.randint(2, 4)
        den_degree = rand.randint(2, 4)
        
        P_num = await mnogochlen(rand, guaranteed_degree=num_degree)
        P_den = await mnogochlen(rand, guaranteed_degree=den_degree)
        
        P_x = f"\\frac{{{P_num}}}{{{P_den}}}"
    
    if r == 2:
        base_str = f"\\sqrt{{{P_x}}}"
    elif r == 3:
        base_str = f"\\sqrt[3]{{{P_x}}}"
    else:
        base_str = f"\\sqrt[{r}]{{{P_x}}}"
    
    if n == 1:
        denominator = "x"
    else:
        denominator = f"x^{{{n}}}"
    
    if b == 1:
        exponent_str = f"\\frac{{1}}{{{denominator}}}"
    elif b == -1:
        exponent_str = f"-\\frac{{1}}{{{denominator}}}"
    else:
        exponent_str = f"\\frac{{{b}}}{{{denominator}}}"
    
    limit_str = f"\\lim_{{x \\rightarrow \\infty}}{{\\left({base_str}\\right)}}^{{{exponent_str}}}"
    
    return limit_str

async def gen_three_three_lim(rand, n, variations=True):
    primers = []
    
    for _ in range(n):
        if variations and rand.chance(50): 
            primer = await generate_root_power_zero_limit_variations(rand)
        else:  
            primer = await generate_root_power_zero_limit(rand)
        
        primers.append(primer)
    
    return primers
