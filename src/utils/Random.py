from hashlib import sha256

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

    def choice(self, mas):
        return self.random_choice(mas)