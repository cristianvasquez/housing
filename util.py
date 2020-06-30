import math
import random as np


def probability_of_death(age):
    # A = 7.5763e-9
    A = 8.5e-8
    k = 0.148
    return A * math.exp(k * age)

def test_prob():
    for j in range(100):
        for i in range(1000):
            if np.random() < probability_of_death(i):
                print(f'Died at age: {i}')
                break

