from src.utils.Random import Random
import os

async def monomial(rand, max_deg, min_deg=0, factor=None):
    degree = rand.randint(min_deg, max_deg)
    if factor is None:
        factor = rand.randint(1, 20)
    if max_deg == min_deg == 0.5:
        if factor != 1:
            return f"{factor}\\sqrt{{x}}", 0.5, factor
        else:
            return f"\\sqrt{{x}}", 0.5, factor
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

async def polynomial(rand, max_deg, max_deg_factor, count):
    string = ""
    max_degree = 0
    for i in range(count):
        if i == 0:
            s, max_degree, max_deg_factor = await monomial(rand, max_deg, max_deg, max_deg_factor)
            string = s
        else:
            s, max_deg, _ = await monomial(rand, max_deg, count-i-1)
            op = rand.random_choice(["+", "-"])
            string += op+s
        max_deg -= 1
    return string, max_degree, max_deg_factor

async def polynomials_part(rand, deg, count):
    root_deg = rand.randint(2, 5)
    max_deg_factor = rand.randint(1, 5) ** root_deg
    string, max_deg, max_deg_factor = await polynomial(rand, deg*root_deg, max_deg_factor, count)
    if root_deg != 2:
        string = f"\\sqrt[{root_deg}]{{{string}}}"
    else:
        string = f"\\sqrt{{{string}}}"
    return string, max_deg/root_deg, max_deg_factor**(1/root_deg)

async def polynomials(rand, max_deg, count):
    string = ""
    general_degree = 0
    general_factor = 1
    for i in range(count):
        if i == 0:
            degree = rand.randint(1, max_deg-count+1)
            string, general_degree, general_factor = await polynomials_part(rand, degree, rand.randint(2, 3))
            max_deg -= degree
        elif i == count-1:
            degree = max_deg
            s, d, f = await polynomials_part(rand, degree, rand.randint(2, 3))
            string += s
            general_degree += d
            general_factor *= f
        else:
            degree = rand.randint(1, max_deg-count+i+1)
            s, d, f = await polynomials_part(rand, degree, rand.randint(2, 3))
            max_deg -= degree
            string += s
            general_degree += d
            general_factor *= f
    return string, general_degree, general_factor

async def generate_lim(rand):
    if rand.chance(70):
        denominator_degree = divisor_degree = rand.randint(3, 7)
    else:
        denominator_degree = rand.randint(3, 7)
        divisor_degree = rand.randint(3, 7)
    devisor, devisor_max_degree, devisor_max_factor = await polynomials(rand, divisor_degree, rand.randint(2, 3))
    denominator, denominator_max_degree, denominator_max_factor = await polynomials(rand, denominator_degree, rand.randint(2, 3))
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
            solution = f"\\frac{{{int(devisor_max_factor)}}}{{{int(denominator_max_factor)}}}"
        else:
            solution = f"{int(devisor_max_factor // denominator_max_factor)}"
    return problem, solution

async def generate_lim_4_5(rand, n):
    primers = []
    for _ in range(n):
        primer, solution = await generate_lim(rand)
        primers.append(primer)
    return primers