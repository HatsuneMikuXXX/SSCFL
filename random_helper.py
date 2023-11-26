import math
import random

def flip():
    return random.random() < 0.5

def biased_flip(p):
    return random.random() < p

def uniform(lb, ub, return_integer = False):
    p = random.random()
    if return_integer:
        x = math.floor(p*lb + (1 - p)*(ub + 1))
        if x == ub + 1:
            return ub
        return x
    return p*lb + (1 - p)*ub

def sample(Elements, Probabilities, eliminate_almost_never_probabilities = False):
    n = len(Probabilities)
    assert len(Elements) == n

    elements_copy = Elements.copy()
    probabilities_copy = Probabilities.copy()
    # Remove almost-never probabilities
    if eliminate_almost_never_probabilities:
        toRemove = []
        adjustment = 0
        for i in range(n):
            if probabilities_copy[i] == 0:
                toRemove.add(i - adjustment)
                adjustment += 1
        for r in toRemove:
            del probabilities_copy[r]
            del elements_copy[r]
    # Gather Sample        
    normed_P = [p/sum(probabilities_copy) for p in probabilities_copy]
    random_real = random.random()
    cumulative_sum = 0
    for i in range(n):
        if cumulative_sum <= random_real and random_real < cumulative_sum + normed_P[i]:
            return elements_copy[i]
        cumulative_sum += normed_P[i] 
    assert False

    
    