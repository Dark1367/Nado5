from src.utils.Random import Random
import os

async def generate_log_limit(rand):
    S = rand.randint(1, 10)  
    
    A = rand.randint(-5, 5)
    while A == 0:
        A = rand.randint(-5, 5)
    
    C = rand.randint(-5, 5)
    while C == 0:
        C = rand.randint(-5, 5)
    

    B = S - A
    D = S - C

    s_A = A
    s_B = B
    s_C = C
    s_D = D

    if s_A == 1:
        s_A = ""
    elif s_A == -1:
        s_A = "-"

    if s_C == 1:
        s_C = ""
    elif s_C == -1:
        s_C = "-"

    if B == 0:
        arg1 = f"{s_A}x"
    elif B > 0:
        arg1 = f"{s_A}x+{s_B}"
    else:
        arg1 = f"{s_A}x{s_B}"

    if D == 0:
        arg2 = f"{s_C}x"
    elif D > 0:
        arg2 = f"{s_C}x+{s_D}"
    else:
        arg2 = f"{s_C}x{s_D}"
    
    primer = f"\\lim_{{x \\to 1}}\\left(\\frac{{\\ln\\left({arg1}\\right)}}{{\\ln\\left({arg2}\\right)}}\\right)^{{\\frac{{1}}{{x-1}}}}"
    return primer, A, B, C, D

async def generate_lim_1_5(rand, n):
    primers = []
    for _ in range(n):
        primer, A, B, C, D = await generate_log_limit(rand)
        primers.append(primer)
    return primers
