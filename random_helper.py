import math
import random

def flip():
    return random.random() < 0.5

def biased_flip(p):
    return random.random() < p

# Returns a random element from Elements using Probabilities as distribution. If the optional parameter is true then elements with probability 0 cannot be chosen, ever.
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
                toRemove.append(i - adjustment)
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

def get_uniform_distribution(n):
    return [1/n for _ in range(n)]

# Returns a random number in [lb, ub] uniformly. If integer is true then it is drawn uniformly from the integers between lb and ub (inclusive)
def uniform(lb, ub, return_integer = False):
    p = random.random()
    if return_integer:
        x = math.floor(p*lb + (1 - p)*(ub + 1))
        if x == ub + 1:
            return ub
        return x
    return p*lb + (1 - p)*ub

# Return a random number from a triangular distribution. MINMAX method from https://www.sciencedirect.com/science/article/pii/S0895717708002665
def triangular(lb, ub, peak):
    assert peak >= lb and peak <= ub
    u = uniform(lb, ub)
    v = uniform(lb, ub)
    # Compute relative position of peak
    c = (peak - lb)/(ub - lb)
    return (1 - c) * min(u, v) + c * max(u, v)

    
    