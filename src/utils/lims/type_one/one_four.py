from src.utils.Random import Random
import os

rand = Random(str(os.urandom(8)))

async def generate_exp_limit():
    A = rand.randint(-5, 5)
    while A == 0:
        A = rand.randint(-5, 5)
    
    B = rand.randint(-5, 5)
    while B == 0:
        B = rand.randint(-5, 5)
    
    m = rand.randint(1, 6)
    
    C = rand.randint(-8, 8)
    while C == 0:
        C = rand.randint(-8, 8)
    
    D = rand.randint(-6, 6)
    while D == 0:
        D = rand.randint(-6, 6)
    
    exp1 = f"e^{{{A}x}}"
    exp2 = f"e^{{{B}x}}"
    
    denominator = str(m)
    
    if D == 1:
        exponent = f"\\frac{{{C}}}{{x}}"
    elif D == -1:
        exponent = f"\\frac{{{-C}}}{{x}}"
    else:
        exponent = f"\\frac{{{C}}}{{{D}x}}"
    
    primer = f"\\lim_{{x \\to 0}}\\left(\\frac{{{exp1}+{exp2}}}{{{denominator}}}\\right)^{{{exponent}}}"
    return primer

async def gen_one_four_lim(n):
    primers = []
    for _ in range(n):
        primer = await generate_exp_limit()
        primers.append(primer)
    return primers

