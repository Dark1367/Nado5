from src.utils.Random import Random
import os

async def monomial(rand, max_deg, min_deg=0):
    degree = rand.randint(min_deg, max_deg)
    factor = rand.randint(1, 20)
    if degree == 0:
        string = str(factor)
    else:
        string = ""
        if factor != 1:
            string += str(factor)
        string += "x"
        if degree!=1:
            string += f"^{{{str(degree)}}}"
    return string, degree, factor

async def cos_or_sin(rand):
    monomial_s, _, _ = await monomial(rand, 6)
    func = "\\sin"
    if rand.chance(50):
        func = "\\cos"
    string = f"{func}({monomial_s})"
    return string

async def polynomial(rand, max_deg, count):
    string = ""
    max_degree = 0
    max_deg_factor = 0
    for i in range(count-1):
        if i == 0:
            s, max_degree, max_deg_factor = await monomial(rand, max_deg, max_deg)
            if rand.chance(50):
                s="-"+s
                max_deg_factor = -max_deg_factor
            string = s
        else:
            s, max_deg, _ = await monomial(rand, max_deg, count-i-2)
            op = rand.random_choice(["+", "-"])
            string += op+s
        max_deg -= 1
    op = rand.random_choice(["+", "-"])
    string += op + await cos_or_sin(rand)
    return string, max_degree, max_deg_factor

async def generate_lim(rand):
    if rand.chance(70):
        denominator_degree = divisor_degree = rand.randint(5, 8)
    else:
        denominator_degree = rand.randint(5, 8)
        divisor_degree = rand.randint(5, 8)
    devisor, devisor_max_degree, devisor_max_factor = await polynomial(rand, divisor_degree, rand.randint(2, 4))
    denominator, denominator_max_degree, denominator_max_factor = await polynomial(rand, denominator_degree, rand.randint(2, 4))
    problem = f"\\lim_{{x \\to \\infty}}\\frac{{{devisor}}}{{{denominator}}}"
    if devisor_max_degree > denominator_max_degree:
        sign = "+"
        if (devisor_max_factor>0) != (denominator_max_factor>0):
            sign = "-"
        solution = f"{sign}\\infty"
    elif devisor_max_degree < denominator_max_degree:
        solution = "0"
    else:
        if devisor_max_factor / denominator_max_factor % 1 != 0:
            solution = f"\\frac{{{devisor_max_factor}}}{{{denominator_max_factor}}}"
        else:
            solution = f"{devisor_max_factor // denominator_max_factor}"
    return problem, solution

async def generate_lim_4_2(rand, n):
    primers = []
    for _ in range(n):
        primer, solution = await generate_lim(rand)
        primers.append(primer)
    return primers