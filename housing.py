import random as np

from house import new_house
from shareholder import new_person
from setup import MAX_PEOPLE, MONTHS_PER_YEAR


class Stats:
    def __init__(self):
        self.people_stats = {}
        self.people_stats_row = 0

        self.general_stats = {}
        self.general_stats_row = 0

        self.example_house_stats = {}
        self.example_house_stats_row = 0

    def add_people_stats_record(self, record):
        self.people_stats[self.people_stats_row] = record
        self.people_stats_row += 1

    def add_general_stats_record(self, record):
        self.general_stats[self.general_stats_row] = record
        self.general_stats_row += 1

    def add_example_house_stats_record(self, record):
        self.example_house_stats[self.example_house_stats_row] = record
        self.example_house_stats_row += 1


class Community:
    def __init__(self, house_tenant=None, people=None, houses=None, brother_state=None, inheritance=False):
        if houses is None:
            houses = {}
        if people is None:
            people = {}
        if house_tenant is None:
            house_tenant = {}
        self.dead_people = set()
        self.house_tenants = house_tenant
        self.people = people
        self.houses = houses
        self.brother_state = brother_state
        self.inheritance = inheritance
        self.people_max_id = len(people)
        self.house_max_id = len(houses)

        self.current_tick = 0

        self.stats = Stats()

    def increase_tick(self):
        '''
        Game 'time-ticks' correspond to one month.
        '''
        if self.current_tick % MONTHS_PER_YEAR == 0:
            year = int(self.current_tick / MONTHS_PER_YEAR)
            self.add_people_stats(year)
            self.add_general_stats(year)

        self.current_tick += 1

    def add_people_stats(self, year):

        for k, person in self.people.items():
            total_shares = 0
            for _, house in self.houses.items():
                if k in house.shares:
                    total_shares += house.shares[k]
            self.stats.add_people_stats_record({
                'year': year,
                'id': person.name,
                'money': person.money,
                'shares': total_shares,
                'age': person.age,
                'parent': person.parent,
                'share_income': person.period_share_income,
                'inherited': person.shares_inherited > 0,
                'current_house': None
            })
            person.period_share_income = 0  # Reset the share income for this period

        # I added this dummy person to make the animation facet's work.
        if self.inheritance:
            self.stats.add_people_stats_record({
                'year': year,
                'id': 'dummy',
                'money': 0,
                'shares': 0,
                'age': 0,
                'parent': None,
                'share_income': 0,
                'inherited': True,
                'current_house': None
            })

    def add_general_stats(self, year):
        self.stats.add_general_stats_record({
            'year': year,
            'homeless_people': len(self.homeless_people),
            'houses': len(self.houses),
            'alive': len(self.people),
            'dead': len(self.dead_people),
            'state_money': self.brother_state.money,
            'spent_building_houses': self.brother_state.spent_building_houses,
        })

    def add_example_house_stats(self, year):
        pass
        # self.stats.add_example_house_record({
        #     'homeless_people': len(self.homeless_people),
        #     'houses': len(self.houses),
        #     'alive': len(self.people),
        #     'dead': len(self.dead_people),
        #     'state_money': len(self.brother_state.money),
        #     'spent_building_houses': len(self.brother_state.spent_building_houses),
        # })

    def random_available_house(self, budget):
        houses = list(range(len(self.houses)))
        np.shuffle(houses)
        for i in houses:
            if self.houses[i].share_price < budget and i not in self.house_tenants:
                return i, self.houses[i].share_price
        return None, None

    @property
    def homeless_people(self):
        '''
        Homeless people = All people that are not tenants
        '''
        result = set(self.people.keys())
        for k, v in self.house_tenants.items():
            result.remove(v)
        return result

    def occupy_house(self, person_id, new_house_id):
        self._return_house(person_id)
        # The person is assigned to the new house
        self.house_tenants[new_house_id] = person_id

    def _return_house(self, person_id):
        for k, v in self.house_tenants.items():
            if v == person_id:
                del self.house_tenants[k]
                return

    def step_life_and_death(self):

        self.brother_state.age += 1 / MONTHS_PER_YEAR

        for k, person in self.people.copy().items():

            if len(self.people) < MAX_PEOPLE:
                if person.produces_child():
                    self.add_new_born(parent=k)

            if person.dies():
                self._person_dies(k)

            else:
                # Everyone ages
                person.age += 1 / MONTHS_PER_YEAR

    def step_income_and_taxes(self):
        for k, shareholder in self.people.items():
            shareholder.work()

    def step_acquire_shares(self):
        # If persons are tenants, they need to acquire a share to continue living in the house for one month.
        # otherwise they go homeless
        for house_id, person_id in self.house_tenants.items():

            money_to_pay = self.houses[house_id].share_price

            if self.people[person_id].money < money_to_pay:
                print(f'person {person_id} cannot pay a share and becomes homeless')
                self._return_house(house_id)

            else:
                # Person pays the price for the share
                # print(f'{self.people[person_id].name} pays {money_to_pay} for a share')
                self.people[person_id].money -= money_to_pay

                # All previous shareholders receive their share
                total_shares = self.houses[house_id].total_shares
                for owner_id, shares in self.houses[house_id].shares.items():
                    share_benefit = (shares / total_shares) * money_to_pay
                    # print(f'{self.people[owner_id].name} receives {share_benefit} for {shares}/{total_shares}')
                    self.people[owner_id].money += share_benefit
                    self.people[owner_id].period_share_income += share_benefit  # Only for stats

                # Brother state receives his share
                self.brother_state.money += (self.houses[house_id].founder_shares / total_shares) * money_to_pay
                # print(
                #     f'{self.brother_state.name} receives {(self.houses[house_id].founder_shares / total_shares) * money_to_pay}')

                self.houses[house_id].assign_share(person_id)

    def _get_random_child(self, person_id):
        for k, person in self.people.items():
            if person.parent == person_id:
                return k
        return None

    def _person_dies(self, deceased_id):

        # Remove the shares
        for k, house in self.houses.items():
            if deceased_id in house.shares:
                child_id = self._get_random_child(deceased_id)
                if self.inheritance and child_id is not None:

                    # Child inherits the shares
                    share_amount = house.inherit_shares(deceased_id, child_id)
                    self.people[child_id].shares_inherited += share_amount  # Only for stats

                    # Child also inherits money
                    money_amount = self.people[deceased_id].money
                    self.people[deceased_id].money = 0
                    self.people[child_id].money += money_amount
                    self.people[child_id].money_inherited += money_amount  # Only for stats

                else:
                    # Brother state inherits the shares
                    amount = house.founder_inherit_shares(deceased_id)
                    self.brother_state.shares_inherited += amount  # Only for stats

        self._return_house(deceased_id)
        del self.people[deceased_id]
        self.dead_people.add(deceased_id)

    def add_new_born(self, parent=None):
        self.people[self.people_max_id] = new_person(name=f'person {self.people_max_id}', parent=parent)
        self.people_max_id += 1

    def add_new_house(self):
        self.houses[self.house_max_id] = new_house(name=f'house {self.house_max_id}')
        self.house_max_id += 1

    def __repr__(self):

        houses = ''
        for i, house in self.houses.items():
            houses += f'\n{house.name}, share_price:${house.share_price}, shares:{house.shares}, founder_shares:{house.founder_shares}, total_shares={house.total_shares}, inflation={house.inflation}'
        people = ''
        for i, person in self.people.items():
            people += f'\n{person.name} (parent:{person.parent}), money:${person.money}, age:{person.age}, shares_inherited:{person.shares_inherited}'

        return \
            f'''
-----------------------------
Tenants: {self.house_tenants}
Homeless people: {self.homeless_people}
Brother state: money:${self.brother_state.money} age:{self.brother_state.age}
-----------------------------
Houses: 
{houses}
-----------------------------
People: 
{people}
-----------------------------
Dead People:
{self.dead_people}
        '''
