from src.utils.Random import Random
import os
rand = Random(str(os.urandom(8)))

async def monomial(max_deg, min_deg=0):
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

async def polynomial(max_deg, count):
    string = ""
    max_degree = 0
    max_deg_factor = 0
    for i in range(count):
        if i == 0:
            s, max_degree, max_deg_factor = await monomial(max_deg, max_deg)
            if rand.chance(50):
                s="-"+s
                max_deg_factor = -max_deg_factor
            string = s
        else:
            s, max_deg, _ = await monomial(max_deg, count-i-1)
            op = rand.random_choice(["+", "-"])
            string += op+s
        max_deg -= 1
    return string, max_degree, max_deg_factor

async def get_factors(n):
    factors = set()
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)
    return sorted(list(factors))

async def polynomials_part(deg, count):
    deg_factors = await get_factors(deg)
    part_degree = 1
    if deg > 1 and rand.chance(30) and len(deg_factors)!=0:
        part_degree = rand.random_choice(list(deg_factors))
        deg = int(deg / part_degree)

    string, max_degree, max_deg_factor = await polynomial(deg, min(count, deg+1))
    string = f"({string})"
    if part_degree != 1:
        string += f"^{{{part_degree}}}"
    return string, max_degree * part_degree, max_deg_factor ** part_degree

async def polynomials(max_deg, count):
    string = ""
    general_degree = 0
    general_factor = 1
    for i in range(count):
        if i == 0:
            degree = rand.randint(1, max_deg-count+1)
            string, general_degree, general_factor = await polynomials_part(degree, rand.randint(2, 3))
            max_deg -= degree
        elif i == count-1:
            degree = max_deg
            s, d, f = await polynomials_part(degree, rand.randint(2, 3))
            string += s
            general_degree += d
            general_factor *= f
        else:
            degree = rand.randint(1, max_deg-count+i+1)
            s, d, f = await polynomials_part(degree, rand.randint(2, 3))
            max_deg -= degree
            string += s
            general_degree += d
            general_factor *= f
    return string, general_degree, general_factor

async def generate_lim():
    if rand.chance(70):
        denominator_degree = divisor_degree = rand.randint(3, 5)
    else:
        denominator_degree = rand.randint(3, 5)
        divisor_degree = rand.randint(3, 5)
    devisor, devisor_max_degree, devisor_max_factor = await polynomials(divisor_degree, rand.randint(2, 3))
    denominator, denominator_max_degree, denominator_max_factor = await polynomials(denominator_degree, rand.randint(2, 3))
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

async def generate_lim_4_3(n):
    primers = []
    for _ in range(n):
        primer, solution = await generate_lim()
        primers.append(primer)
    return primers