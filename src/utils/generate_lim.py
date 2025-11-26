from hashlib import sha256
import os

class Random:
    last_hash = 0

    def __init__(self, seed:str):
        self.last_hash = int(sha256(seed.encode()).hexdigest(), 16)

    def seed(self, seed:str):
        self.last_hash = int(sha256(seed.encode()).hexdigest(), 16)

    def shufle(self):
        self.last_hash = int(sha256(str(self.last_hash).encode()).hexdigest(), 16)

    def random(self):
        self.shufle()
        return self.last_hash

    def randint(self, a:int, b:int):
        self.shufle()
        return self.last_hash % (b-a+1) + a

    def random_choice(self, mas):
        self.shufle()
        return mas[self.last_hash % len(mas)]

    def chance(self, percent:int):
        self.shufle()
        return self.last_hash % 101 <= percent
r = Random(str(os.urandom(8)))


async def generate_easy_predel(count):
    examples = []
    L, R = '{', '}'
    def F(maxx):
        B = []
        while len(B) < r.randint(1, 2):
            Nado = r.randint(2, maxx - 1)
            if Nado not in B:
                B.append(Nado)
            B.sort(reverse = True)
        res = ''.join([f'{r.random_choice(['-', '+'])} {r.randint(2, 10)} x^{x}' if r.chance(70) else f'{r.random_choice(['-', '+'])} \sqrt{L}{r.randint(2, 10)} x^{x}{R}' for x in B])
        return res

    for _ in range(count):
        localstep = r.randint(4, 9)
        predel = "\lim_{x\\to\infty}"
        chislitel = f"{r.random_choice(['-', ''])} {r.randint(2, 10)} x^{localstep} {F(localstep)} {r.random_choice(['-', '+'])} {r.random_choice([r.randint(1, 20), r.randint(1, 20), '\cos x', '\sin x'])}"
        znamenatel = f"{r.random_choice(['-', ''])} {r.randint(2, 10)} x^{localstep} {F(localstep)} {r.random_choice(['-', '+'])} {r.random_choice([r.randint(1, 20), r.randint(1, 20), '\cos x', '\sin x'])}"
        examples.append(predel + "\\frac" + L + chislitel + R + L + znamenatel + R)

    return examples