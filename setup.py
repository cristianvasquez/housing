import math
import random as np

YEARS_A_PERSON_LIVES = 100  # Max number of years a person lives
MONTHS_A_PERSON_LIVES = YEARS_A_PERSON_LIVES * 12  # Max number of months a person will ever live
MONTHS_PER_YEAR = 12
MAX_PEOPLE = 30


def probability_of_death_per_month(age):
    A = 8.5e-8
    k = 0.148
    return A * math.exp(k * age)


def probability_of_birth_per_month():
    return 2 / MONTHS_A_PERSON_LIVES


def test_probability_of_death():
    for j in range(100):
        for i in range(1000):
            if np.random() < probability_of_death_per_month(i):
                print(f'Died at age: {i}')
                break
