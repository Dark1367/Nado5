from src.utils.Random import Random
import os

async def fmt_exp(exp):
    if exp == 0:
        return "n"
    elif exp > 0:
        return f"n+{exp}"
    else:
        return f"n{exp}"
        
async def fmt_exp_base(base, exp):
    if exp == 0:
        return "1"
    elif exp == 1:
        return str(base)
    else:
        return f"{base}^{exp}"

async def generate_limit(rand):
    bases = [2, 3, 4, 5, 6, 7, 8, 9]
    b1 = bases[rand.randint(0, len(bases)-1)]
    b2 = bases[rand.randint(0, len(bases)-1)]
    while b2 == b1:
        b2 = bases[rand.randint(0, len(bases)-1)]

    c1 = rand.randint(-5, 5)
    while c1 == 0:
        c1 = rand.randint(-5, 5)
    
    c2 = rand.randint(-5, 5)
    while c2 == 0:
        c2 = rand.randint(-5, 5)
    
    c3 = rand.randint(-5, 5)
    while c3 == 0:
        c3 = rand.randint(-5, 5)

    c4 = rand.randint(-5, 5)
    while c4 == 0:
        c4 = rand.randint(-5, 5)
    
    s1 = rand.randint(-3, 3)
    s2 = rand.randint(-3, 3)
    s3 = rand.randint(-3, 3)
    s4 = rand.randint(-3, 3)
    num_terms = []
    
    exp1 = await fmt_exp(s1)
    if c1 == 1:
        num_terms.append(f"{await fmt_exp_base(b1, exp1)}")
    elif c1 == -1:
        num_terms.append(f"-{await fmt_exp_base(b1, exp1)}")
    else:
        num_terms.append(f"{c1} \\cdot {await fmt_exp_base(b1, exp1)}")
    
    exp2 = await fmt_exp(s2)
    if c2 > 0:
        if c2 == 1:
            num_terms.append(f"+ {await fmt_exp_base(b2, exp2)}")
        else:
            num_terms.append(f"+ {c2} \\cdot {await fmt_exp_base(b2, exp2)}")
    else:
        if c2 == -1:
            num_terms.append(f"- {await fmt_exp_base(b2, exp2)}")
        else:
            num_terms.append(f"- {abs(c2)} \\cdot {await fmt_exp_base(b2, exp2)}")

    den_terms = []
    
    if rand.randint(0, 1) == 0:
        base3 = b1
    else:
        base3 = b2
    
    exp3 = await fmt_exp(s3)
    if c3 > 0:
        if c3 == 1:
            den_terms.append(f"{await fmt_exp_base(base3, exp3)}")
        else:
            den_terms.append(f"{c3} \\cdot {await fmt_exp_base(base3, exp3)}")
    else:
        if c3 == -1:
            den_terms.append(f"-{await fmt_exp_base(base3, exp3)}")
        else:
            den_terms.append(f"- {abs(c3)} \\cdot {await fmt_exp_base(base3, exp3)}")
    
    exp4 = await fmt_exp(s4)
    if c4 > 0:
        if c4 == 1:
            den_terms.append(f"+ {await fmt_exp_base(b2, exp4)}")
        else:
            den_terms.append(f"+ {c4} \\cdot {await fmt_exp_base(b2, exp4)}")
    else:
        if c4 == -1:
            den_terms.append(f"- {await fmt_exp_base(b2, exp4)}")
        else:
            den_terms.append(f"- {abs(c4)} \\cdot {await fmt_exp_base(b2, exp4)}")
    
    numerator = "".join(num_terms)
    denominator = "".join(den_terms)
    
    if numerator.startswith('+'):
        numerator = numerator[1:]
    if denominator.startswith('+'):
        denominator = denominator[1:]
    
    primer = f"\\lim_{{n \\to \\infty}} \\frac{{{numerator}}}{{{denominator}}}"
    return primer

async def generate_lim_6_1(rand, n):
    primer = []
    for _ in range(n):
        primer.append("6.1"+await generate_limit(rand))
    return primer
