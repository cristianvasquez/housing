import random as np

from setup import MONTHS_PER_YEAR, probability_of_birth_per_month, probability_of_death_per_month

CHANGE_HOUSE_PROB = 1 / MONTHS_PER_YEAR * 5
HOUSE_COST = MONTHS_PER_YEAR * 20 * 15


def new_person(name='', parent=None):
    age = np.randint(14, 20)
    money = np.randint(10, 100)
    return Shareholder(age=age, money=money, name=name, parent=parent)


class Shareholder():
    def __init__(self, age=14, money=0, name='', parent=None):
        self.money = money
        self.age = age
        self.name = name
        self.parent = parent
        self.spent_building_houses = 0

        self.shares_inherited = 0  # Only for stats
        self.money_inherited = 0  # Only for stats
        self.period_share_income = 0  # Only for stats

    def work(self):
        # People only perceives money if they are less than 60 y/o
        if self.age < 60:
            income = np.randint(20, 25)
        else:
            income = 0
        self.money += income

    def produces_child(self):
        b_prob = probability_of_birth_per_month()
        return np.random() < b_prob
        # if np.random() < b_prob:
        #     print(f'{self.name} gives birth')
        #     return True
        # return False

    def dies(self):
        d_prob = probability_of_death_per_month(self.age)
        return np.random() < d_prob
        # if np.random() < d_prob:
        #     print(f'{self.name} dies at {self.age}')
        #     return True
        # return False


def shareholder_policy(community, change_house_prob=CHANGE_HOUSE_PROB):
    # All tenants try to get another house with a probability 0.1
    for (current_house, tenant) in community.house_tenants.items():
        if (np.random() < change_house_prob):
            # print(f'tenant {tenant} tries to find another house')
            prospect_house, price = community.random_available_house(community.people[tenant].money)
            if prospect_house is not None:
                # print(f'{tenant} moves to house {prospect_house} for ${price}')
                community.occupy_house(tenant, prospect_house)
            # else:
            #     print(f'tenant {tenant} did not find another house')

    # All homeless people try to rent a house with a probability 0.9
    for person_id in community.homeless_people.copy():
        if (np.random() < 0.9):
            available_money = community.people[person_id].money
            # print(f'homeless {person_id} tries to find a house with ${available_money}')
            prospect_house, price = community.random_available_house(available_money)
            if prospect_house is not None:
                # print(f'homeless {person_id} rents house {prospect_house} for ${price}')
                community.occupy_house(person_id, prospect_house)
            # else:
            #     print(f'homeless {person_id} did not find a house')

    #  if there are more people than houses, brother state tries to build a house
    if len(community.people) + 1 > len(community.houses) and community.brother_state.money > HOUSE_COST:
        community.brother_state.money -= HOUSE_COST
        community.brother_state.spent_building_houses += HOUSE_COST
        community.add_new_house()
        # print(f'brother state built a house')

    return community
