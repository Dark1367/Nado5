from src.utils.Random import Random
import os
rnd = Random(str(os.urandom(8)))

async def generate_limit():
    a1 = rnd.randint(1, 5)
    d1 = rnd.randint(1, 4)
    a2 = rnd.randint(3, 8)
    d2 = rnd.randint(1, 3)
    
    c1 = a1 - d1
    if c1 == 0:
        last1 = f"{d1}n"
    elif c1 > 0:
        last1 = f"{d1}n + {c1}"
    else:
        last1 = f"{d1}n - {abs(c1)}"
    
    c2 = a2 - d2
    if c2 == 0:
        last2 = f"{d2}n"
    elif c2 > 0:
        last2 = f"{d2}n + {c2}"
    else:
        last2 = f"{d2}n - {abs(c2)}"

    num_terms = []
    for k in range(1, 5):
        val = a1 + d1 * (k - 1)
        num_terms.append(val)
    num_str = " + ".join(map(str, num_terms))
    num_str += f" + \\cdots + ({last1})"
    
    den_terms = []
    for k in range(1, 5):
        val = a2 + d2 * (k - 1)
        den_terms.append(val)
    den_str = " + ".join(map(str, den_terms))
    den_str += f" + \\cdots + ({last2})"
    
    primer = f"\\lim_{{n \\to \\infty}} \\frac{{{num_str}}}{{{den_str}}}"
    return primer

async def generate_lim_7_2(n):
    primer = []
    for _ in range(n):
        primer.append(await generate_limit())
    return primer
