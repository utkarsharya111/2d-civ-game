"""
econ_model.py

Houses the information-theoretic economics logic:
- Probability distribution p(ω)
- Shannon Entropy
- Knowledge Stock K(t)
- TFP A(t)
- Etc.
"""

import math

# Number of possible methods
NUM_METHODS = 5

# The maximum entropy for a uniform distribution among NUM_METHODS
H_MAX = math.log(NUM_METHODS)

# Exponential TFP scale factor (alpha)
ALPHA = 1.0

# Exponential time price factor (unused if not needed, but let's keep it)
DELTA = 0.7

# Research rate: how quickly p(ω) shifts toward best method
RESEARCH_RATE = 0.05

# For production function, we define some constants
BETA = 0.5
K_PHYSICAL = 10.0
L_FIXED = 10.0

# Hidden best method index (the real best among the 5)
BEST_METHOD_INDEX = 0

def shannon_entropy(prob_dist):
    """
    Compute Shannon entropy H(p) = -sum p(ω) ln p(ω).
    """
    entropy = 0.0
    for p in prob_dist:
        if p > 0:
            entropy -= p * math.log(p)
    return entropy

def knowledge_stock(prob_dist):
    """
    K(t) = H_max - H(p).
    """
    return H_MAX - shannon_entropy(prob_dist)

def tfp(prob_dist):
    """
    A(t) = exp(ALPHA * K(t)).
    """
    K = knowledge_stock(prob_dist)
    return math.exp(ALPHA * K)

def produce(prob_dist):
    """
    Production function Y(t) = A(t) * K_physical^BETA * L_fixed^(1-BETA).
    Returns the production quantity.
    """
    A_val = tfp(prob_dist)
    Y = A_val * (K_PHYSICAL**BETA) * (L_FIXED**(1 - BETA))
    return Y

def research(prob_dist):
    """
    Nudges the probability distribution toward the best method (BEST_METHOD_INDEX).
    p(best) *= (1 + RESEARCH_RATE), then renormalize.
    Returns a new distribution.
    """
    updated = prob_dist[:]
    updated[BEST_METHOD_INDEX] = updated[BEST_METHOD_INDEX] * (1.0 + RESEARCH_RATE)
    # Re-normalize
    s = sum(updated)
    updated = [p / s for p in updated]
    return updated

def initialize_prob_dist():
    """
    Returns a uniform distribution among NUM_METHODS.
    """
    return [1.0/NUM_METHODS for _ in range(NUM_METHODS)]
