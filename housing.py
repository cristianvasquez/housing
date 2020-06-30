import math
import random as np

from util import probability_of_death

MAX_PERSON_AGE = 100  # Max number of years a person lives
BROTHER_ESTATE_INITIAL_SHARE = MAX_PERSON_AGE * 12  # Max number of months a person will ever live

INITIAL_NUMBER_OF_PEOPLE = 5
INITIAL_NUMBER_OF_HOUSES = 7

'''
Game 'time-ticks' correspond to one month.
'''

class Community:
    def __init__(self, house_tenant: dict = {}, shareholders: dict = {}, houses: dict = {}, brother_state=None):
        self.house_tenants = house_tenant
        self.shareholders = shareholders
        self.houses = houses
        self.max_id = len(shareholders)
        self.brother_state = brother_state

    def get_best_available_house(self, available_money):
        for k, house in sorted(self.houses.items(), key=lambda item: item[1].share_price, reverse=True):
            if k not in self.house_tenants and self.houses[k].share_price < available_money:
                return k, self.houses[k].share_price
        return None, None

    @property
    def homeless_people(self):
        '''
        Homeless people = All people that are not tenants
        '''
        result = set(self.shareholders.keys())
        for k, v in self.house_tenants.items():
            result.remove(v)
        return result

    def current_house(self, person_id):
        for k, v in self.house_tenants.items():
            if v == person_id:
                return k
        return None

    def assign_house(self, person_id, new_house_id):
        current_house_id = self.current_house(person_id)
        if current_house_id is not None:
            # the current house has no tenant
            del self.house_tenants[current_house_id]
        self.house_tenants[new_house_id] = person_id

    def income_and_taxes(self):
        # All people receives a basic income
        for k, v in self.shareholders.items():
            money = np.randint(20, 25)
            print(f'{k} received {money} as basic income')
            v.money += money

    def return_house_to_community(self, house_id):
        del self.house_tenants[house_id]

    def acquire_shares(self):
        # If persons are tenants, they need to acquire a share to continue living in the house for one month.
        # otherwise they go homeless
        for house_id, person_id in self.house_tenants.items():

            money_to_pay = self.houses[house_id].share_price

            if self.shareholders[person_id].money < money_to_pay:
                print(f'person {person_id} cannot pay a share and becomes homeless')
                self.return_house_to_community(house_id)
                raise RuntimeError(f'person {person_id} went broke, investigate this')
            else:
                # Person pays the price for the share
                print(f'{person_id} pays {money_to_pay} for a share')
                self.shareholders[person_id].money -= money_to_pay

                # All previous shareholders receive their share
                total_shares = self.houses[house_id].total_shares
                for owner_id, shares in self.houses[house_id].shares.items():
                    share_benefit = (shares / total_shares) * money_to_pay
                    print(f'{owner_id} receives {share_benefit} for {shares}/{total_shares}')
                    self.shareholders[owner_id].money += share_benefit
                # Including brother state
                self.brother_state.money += (self.houses[house_id].founder_shares / total_shares) * money_to_pay

                self.houses[house_id].assign_share(person_id)

    def _person_dies(self, person_id):

        # Remove the shares
        for k, house in self.houses.items():
            if person_id in house.shares:
                # Brother state inherits the shares
                house.founder_shares += house.shares[person_id]
                del house.shares[person_id]

        # Person died, if is a tenant, the house goes back to the community
        house_id = self.current_house(person_id)
        if house_id is not None:
            self.return_house_to_community(house_id)

        del self.shareholders[person_id]

    def add_new_born(self):
        self.shareholders[self.max_id] = new_person(name=f'person {self.max_id}')
        self.max_id += 1

    def life_and_death(self):

        self.brother_state.age += 1 / 12

        for k, person in self.shareholders.copy().items():

            d_prob = probability_of_death(person.age)
            if np.random() < d_prob:
                print(f'{type(person).__name__} dies at {person.age}<---------------')
                self._person_dies(k)
                # To keep things simple, a person will be born each time one dies
                self.add_new_born()
            else:
                # Everyone ages
                person.age += 1 / 12


class House:
    def __init__(self, founder_shares=0, share_price=10, shares=None):
        if shares is None:
            shares = {}
        self.founder_shares = founder_shares
        self.shares = shares
        self.share_price = share_price

    @property
    def total_shares(self):
        total = 0
        for k, v in self.shares.items():
            total += v
        return total + self.founder_shares

    def assign_share(self, person_id):
        # Ownership of the founder decays by one share each month
        if self.founder_shares > 0:
            self.founder_shares -= 1

        # Increment shares for person_id by one
        if person_id in self.shares:
            self.shares[person_id] += 1
        else:
            self.shares[person_id] = 1


class Shareholder():
    def __init__(self, age=14, money=0, name=''):
        self.money = money
        self.age = age
        self.name = name


def new_person(name=''):
    age = np.randint(14, 80)
    money = np.randint(10, 100)
    return Shareholder(age=age, money=money, name=name)


def init():
    houses = {}
    for i in range(INITIAL_NUMBER_OF_HOUSES):
        # The price of the share is proportional to the perceived value of the house
        share_price = np.randint(10, 15)
        # Brother state is the founder and owns the initial shares of a house.
        # The number of shares correspond to one generation so they can decay in a fair way
        houses[i] = House(founder_shares=BROTHER_ESTATE_INITIAL_SHARE, share_price=share_price)

    brother_state = Shareholder(age=0, money=0, name='Brother Estate')
    state = Community(houses=houses, brother_state=brother_state)

    for i in range(INITIAL_NUMBER_OF_PEOPLE):
        # People initially have no house (homeless status)
        state.add_new_born()

    return state


def make_decisions(state):
    # All tenants try to get a better house with a probability 0.1
    for (current_house, tenant) in state.house_tenants.items():
        if (np.random() < 0.1):
            print(f'tenant {tenant} tries to find a better house')
            prospect_house, price = state.get_best_available_house(state.shareholders[tenant].money)
            # If there is a house available with higher price (quality)
            if prospect_house is not None and price > state.houses[current_house].share_price:
                print(f'tenant {tenant} moves to house {prospect_house} for ${price}')
                state.assign_house(tenant, prospect_house)
            else:
                print(f'tenant {tenant} did not find a better house')
            pass

    # All homeless people try to rent a house with a probability 0.9
    for person_id in state.homeless_people.copy():
        if (np.random() < 0.9):
            available_money = state.shareholders[person_id].money
            print(f'homeless {person_id} tries to find a house with ${available_money}')
            prospect_house, price = state.get_best_available_house(available_money)
            if prospect_house is not None:
                print(f'homeless {person_id} rents house {prospect_house} for ${price}')
                state.assign_house(person_id, prospect_house)
            else:
                print(f'homeless {person_id} did not find a house')

    return state


def pprint(state):
    print('* Market')
    print('Tenants', state.house_tenants)
    print('Homeless people', state.homeless_people)
    print('* Houses')
    for i, house in state.houses.items():
        print(
            f'{type(house).__name__} {i}, share_price:${house.share_price}, shares:{house.shares}, founder_shares:{house.founder_shares}')
    print('* Shareholders')
    for i, shareholder in state.shareholders.items():
        print(f'{shareholder.name}, money:${shareholder.money}, age:{shareholder.age}')
    print('* Brother state')
    print(f'{state.brother_state.name}, money:${state.brother_state.money}, age:{state.brother_state.age}')


def month(state):
    state.life_and_death()
    state = make_decisions(state)
    state.income_and_taxes()
    state.acquire_shares()
    return state


state = init()
pprint(state)
for i in range(BROTHER_ESTATE_INITIAL_SHARE):
    state = month(state)
    # print(state.people[0].money)
pprint(state)
