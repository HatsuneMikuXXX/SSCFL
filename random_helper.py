import math
import random

def flip():
    return random.random() < 0.5

def biased_flip(p):
    return random.random() < p

def uniform(a, b, integer = False):
    p = random.random()
    if integer:
        x = math.floor(p*a + (1 - p)*(b + 1))
        if x == b + 1:
            x = b
        return x
    return p*a + (1 - p)*b