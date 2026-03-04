from src.utils.Random import Random
import os

async def factorial(rand, max_constant=5, min_constant=-5):
    constant = rand.randint(min_constant, max_constant)
    if constant == 0:
        string = "(x)!"
    elif constant < 0:
        string = f"(x{constant})!"
    else:
        string = f"(x+{constant})!"
    return string, constant

async def polynomial(rand, count, max_constant=5, min_constant=-5):
    max_const = min_constant-1
    max_const_sign = "-"
    string = ""
    for i in range(count):
        sign = rand.random_choice(["+", "-"])
        s, constant = await factorial(rand, max_constant, min_constant)
        if i == 0 and sign == "+":
            string += s
        else:
            string += sign + s
        if constant > max_const:
            max_const = constant
            max_const_sign = sign
    return string, max_const, max_const_sign

async def generate_lim(rand):
    devisor, devisor_max_constant, devisor_max_const_sign = await polynomial(rand, rand.randint(1, 3))
    denominator, denominator_max_constant, denominator_max_const_sign = await polynomial(rand, rand.randint(1, 3))
    problem = f"\\lim_{{x \\to \\infty}}\\frac{{{devisor}}}{{{denominator}}}"
    if devisor_max_constant > denominator_max_constant:
        if devisor_max_const_sign == denominator_max_const_sign:
            sign = "+"
        else:
            sign = "-"
        solution = sign+"\\infty"
    elif devisor_max_constant < denominator_max_constant:
        solution = "0"
    else:
        if devisor_max_const_sign == denominator_max_const_sign:
            solution = "1"
        else:
            solution = "-1"
    return problem, solution

async def generate_lim_5_1(rand, n):
    primers = []
    for _ in range(n):
        primer, solution = await generate_lim(rand)
        primers.append(primer)
    return primers