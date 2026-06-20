import random
import time

class SeededRandom:
    def __init__(self, seed=None):
        if seed is None:
            seed = int(time.time() * 1000)
        self.seed_value = seed
        self.rng = random.Random(seed)

    def random(self):
        """Returns a random float in [0.0, 1.0)"""
        return self.rng.random()

    def randint(self, a, b):
        """Return a random integer N such that a <= N <= b."""
        return self.rng.randint(a, b)
