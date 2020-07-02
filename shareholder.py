import random

from house import new_random_house
from setup import probability_of_birth_per_month, probability_of_death_per_month, MONTHS_A_PERSON_LIVES

CHANGE_HOUSE_PROBABILITY = 10 / MONTHS_A_PERSON_LIVES


def new_random_person(name='', parent=None):
    age = random.randint(14, 20)
    money = random.randint(10, 100)
    return Shareholder(age=age, money=money, name=name, parent=parent)


class Shareholder():
    def __init__(self, age=14, money=0, name='', parent=None):
        self.money = money
        self.age = age
        self.name = name
        self.parent = parent

        self.spent_building_houses = 0  # Only for stats
        self.shares_inherited = 0  # Only for stats
        self.money_inherited = 0  # Only for stats
        self.period_share_income = 0  # Only for stats
        self.changed_house = 0  # Only for stats

    def work(self):
        # People perceives money only if they are less than 60 y/o
        if self.age < 60:
            income = random.randint(20, 25)
        else:
            income = 0
        self.money += income

    def produces_a_child_this_month(self):
        b_prob = probability_of_birth_per_month()
        return random.random() < b_prob

    def dies_this_month(self):
        d_prob = probability_of_death_per_month(self.age)
        return random.random() < d_prob


def apply_custom_policy(state, change_house_prob=CHANGE_HOUSE_PROBABILITY):
    '''
    This corresponds to choices that people and founder can take
    '''

    # All tenants try to get another house with a probability 0.1
    for current_house, tenant in state.house_tenants.items():
        if (random.random() < change_house_prob):
            # print(f'tenant {tenant} tries to find another house')
            prospect_house, price = state.random_available_house(state.people[tenant].money)
            if prospect_house is not None:
                # print(f'{tenant} moves to house {prospect_house} for ${price}')
                state.occupy_house(tenant, prospect_house)
                state.people[tenant].changed_house += 1
            # else:
            #     print(f'tenant {tenant} did not find another house')

    # All homeless people try to rent a house with a probability 0.9
    for person_id in state.homeless_people.copy():
        if (random.random() < 0.9):
            available_money = state.people[person_id].money
            # print(f'homeless {person_id} tries to find a house with ${available_money}')
            prospect_house, price = state.random_available_house(available_money)
            if prospect_house is not None:
                # print(f'homeless {person_id} rents house {prospect_house} for ${price}')
                state.occupy_house(person_id, prospect_house)
            # else:
            #     print(f'homeless {person_id} did not find a house')

    #  if there are more people than houses, brother state tries to build a house
    if len(state.people) + 1 > len(state.houses):
        house, price = new_random_house(f'new house {state.house_max_id}')
        if state.founder.money > price:
            state.founder.money -= price
            state.founder.spent_building_houses += price
            state.add_new_house(house)
            # print(f'{state.founder.name} built a house')

    return state
