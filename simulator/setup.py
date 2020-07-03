import math
from enum import Enum, unique


@unique
class Ruleset(Enum):
    by_shares = 1
    normal_rent = 2


YEARS_A_PERSON_LIVES = 100  # Max number of years a person lives
MONTHS_A_PERSON_LIVES = YEARS_A_PERSON_LIVES * 12  # Max number of months a person will ever live
MONTHS_PER_YEAR = 12

DEFAULT_SETUP = {
    'max_people': 30,
    'min_people': 2,

    'probability_of_changing_house': 10 / MONTHS_A_PERSON_LIVES,
    'minimum_free_houses_policy': 2,
    'number_of_months_to_run': MONTHS_A_PERSON_LIVES * 3,
    'initial_number_of_people': 5,
    'initial_number_of_houses': 20,
    'allow_inheritance': False,
    'ruleset': Ruleset.by_shares,
    'average_house_cost': MONTHS_PER_YEAR * 40 * 15,  # 7200
    'sigma_house_cost':200,
    'number_of_shares_per_house': MONTHS_A_PERSON_LIVES
}


def probability_of_death_per_month(age):
    A = 8.5e-8
    k = 0.148
    return A * math.exp(k * age)


def probability_of_birth_per_month():
    return 2 / MONTHS_A_PERSON_LIVES
