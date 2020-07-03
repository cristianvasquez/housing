import random

from simulator.setup import probability_of_birth_per_month, probability_of_death_per_month


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
        self.period_work_income = 0  # Only for stats
        self.changed_house = 0  # Only for stats

    @property
    def is_retired(self):
        return self.age > 60

    def work(self):

        if not self.is_retired:
            # Person works
            income = random.randint(8, 12)
        else:
            # Person is retired
            income = random.randint(3, 6)
        self.period_work_income = income
        self.money += income

    def produces_a_child_this_month(self):
        b_prob = probability_of_birth_per_month()
        return random.random() < b_prob

    def dies_this_month(self):
        d_prob = probability_of_death_per_month(self.age)
        return random.random() < d_prob
