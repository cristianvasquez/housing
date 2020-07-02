import random
from enum import Enum

from simulator.shareholder import new_random_person
from simulator.setup import MAX_PEOPLE, MONTHS_PER_YEAR
from simulator.stats import Stats


class Ruleset(Enum):
    by_shares = 0
    normal_rent = 1


class Community:
    def __init__(self, house_tenant=None, people=None, houses=None, founder=None,
                 allow_inheritance=False,
                 ruleset=True):
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
        self.founder = founder
        self.inheritance = allow_inheritance
        self.ruleset = ruleset
        self.people_max_id = len(people)
        self.house_max_id = len(houses)

        self.current_tick = 0

        self.stats = Stats()

    def next_timestep(self):
        '''
        The game 'time-ticks' correspond to one month.
        '''
        year = int(self.current_tick / MONTHS_PER_YEAR)

        if self.current_tick % MONTHS_PER_YEAR == 0:
            self.record_people_stats(year)
            self.record_general_stats(year)
            self.record_example_house_stats(year)

        self.current_tick += 1

    @property
    def available_houses(self):
        '''
        Returns all unocuppied houses
        '''
        result = set(self.houses.keys())
        for k, v in self.house_tenants.items():
            result.remove(k)
        return result

    def random_available_house(self, budget):
        '''
        Returns a random unoccupied house
        :param budget:
        :return:
        '''
        houses = list(range(len(self.houses)))
        random.shuffle(houses)
        for i in houses:
            if self.houses[i].share_price < budget and i not in self.house_tenants:
                return i, self.houses[i].share_price
        return None, None

    @property
    def homeless_people(self):
        '''
        returns the current homeless people
        Homeless people = All people that are not tenants
        '''
        result = set(self.people.keys())
        for k, v in self.house_tenants.items():
            result.remove(v)
        return result

    def occupy_house(self, person_id, new_house_id):
        '''
        Sets the person_id as the tenant of house_id
        :param person_id:
        :param new_house_id:
        :return:
        '''
        self._return_house(person_id)
        # The person is assigned to the new house
        self.house_tenants[new_house_id] = person_id

    def _return_house(self, person_id):
        '''
        Unsets the person_id as tenant of any house
        :param person_id:
        :return:
        '''
        for k, v in self.house_tenants.items():
            if v == person_id:
                del self.house_tenants[k]
                return

    def do_life_and_death_step(self):
        '''
        Applies rules of life in the simulator
        :return:
        '''

        self.founder.age += 1 / MONTHS_PER_YEAR

        for k, person in self.people.copy().items():

            if len(self.people) < MAX_PEOPLE:
                if person.produces_a_child_this_month():
                    self.add_new_born(parent=k)

            if person.dies_this_month():
                self._person_dies(k)

            else:
                # Everyone ages
                person.age += 1 / MONTHS_PER_YEAR

    def do_income_and_taxes_step(self):
        '''
        Apply income, taxes and consumption
        :return:
        '''
        for k, shareholder in self.people.items():
            shareholder.work()

    def so_shares_step(self):
        # If persons are tenants, they need to acquire a share to continue living in the house for one month.
        # otherwise they go homeless
        for house_id, person_id in self.house_tenants.copy().items():

            monthly_payment = self.houses[house_id].share_price

            if self.people[person_id].money < monthly_payment:
                # print(self)
                person = self.people[person_id]
                print(
                    f'[{person.name} is_retired:{person.is_retired} money:${person.money:.2f}, cannot pay ${monthly_payment:.2f} and becomes homeless')
                self._return_house(house_id)

            else:
                # Person pays the price for the share
                # print(f'{self.people[person_id].name} pays {money_to_pay} for a share')
                self.people[person_id].money -= monthly_payment

                # All previous shareholders receive their share
                total_shares = self.houses[house_id].total_shares
                for owner_id, shares in self.houses[house_id].share_owners.items():
                    share_benefit = (shares / total_shares) * monthly_payment
                    # print(f'{self.people[owner_id].name} receives {share_benefit} for {shares}/{total_shares}')
                    self.people[owner_id].money += share_benefit
                    self.people[owner_id].period_share_income += share_benefit  # Only for stats

                # Brother state receives his share
                self.founder.money += (self.houses[house_id].founder_shares / total_shares) * monthly_payment
                # print(
                #     f'{self.brother_state.name} receives {(self.houses[house_id].founder_shares / total_shares) * money_to_pay}')

                if self.ruleset == Ruleset.by_shares:
                    self.houses[house_id].assign_share(person_id)
                elif self.ruleset == Ruleset.normal_rent:
                    # There is no share assignation
                    pass
                else:
                    raise RuntimeError(f'Rule {self.ruleset} not implemented')

    def _get_random_sibling(self, person_id):
        for k, person in self.people.items():
            if person.parent == person_id:
                return k
        return None

    def _person_dies(self, deceased_id):

        # Remove the shares
        for k, house in self.houses.items():
            if deceased_id in house.share_owners:
                child_id = self._get_random_sibling(deceased_id)
                if self.inheritance and child_id is not None:

                    # Child inherits the shares
                    share_amount = house.inherit_to_sibling(deceased_id, child_id)
                    self.people[child_id].shares_inherited += share_amount  # Only for stats

                    # Child also inherits money
                    money_amount = self.people[deceased_id].money
                    self.people[deceased_id].money = 0
                    self.people[child_id].money += money_amount
                    self.people[child_id].money_inherited += money_amount  # Only for stats

                else:
                    # Brother state inherits the shares
                    amount = house.inherit_to_founder(deceased_id)
                    self.founder.shares_inherited += amount  # Only for stats

        self._return_house(deceased_id)
        del self.people[deceased_id]
        self.dead_people.add(deceased_id)

    def add_new_born(self, parent=None):
        self.people[self.people_max_id] = new_random_person(name=f'person {self.people_max_id}', parent=parent)
        self.people_max_id += 1

    def add_new_house(self, new_house):
        self.houses[self.house_max_id] = new_house
        self.house_max_id += 1

    def record_people_stats(self, year):
        '''
        Records statistics about all people in the simulator
        :param year:
        :return:
        '''

        for k, person in self.people.items():
            total_shares = 0
            for _, house in self.houses.items():
                if k in house.share_owners:
                    total_shares += house.share_owners[k]

            monthly_payment = 0
            current_house = None
            for house_id, person_id in self.house_tenants.items():
                if person_id == k:
                    current_house = self.houses[house_id]
                    monthly_payment = current_house.share_price

            self.stats.add_people_stats_record({
                'year': year,
                'id': person.name,
                'money': person.money,
                'shares': total_shares,
                'age': person.age,
                'parent': 'None' if person.parent is None else person.parent,
                'inherited': person.shares_inherited > 0,
                'current_house': current_house.name if current_house is not None else None,
                'monthly_payment': monthly_payment,
                'share_income': person.period_share_income,
                'work_income': person.period_work_income,
                'income': person.period_share_income + person.period_work_income - monthly_payment
            })
            person.period_share_income = 0  # Reset the share income for this period
            person.period_work_income = 0  # Reset the work income for this period

        # I had to add this dummy person to make the animation facet's work.
        if self.inheritance:
            self.stats.add_people_stats_record({
                'year': year,
                'id': 'dummy',
                'money': 0,
                'shares': 0,
                'age': 0,
                'parent': None,
                'share_income': 0,
                'work_income': 0,
                'income': 0,
                'inherited': True,
                'current_house': None
            })
            self.stats.add_people_stats_record({
                'year': year,
                'id': 'dummy',
                'money': 0,
                'shares': 0,
                'age': 0,
                'parent': None,
                'share_income': 0,
                'work_income': 0,
                'income': 0,
                'inherited': False,
                'current_house': None
            })

    def record_general_stats(self, year):
        '''
        Records the history of general statistics
        :param year:
        :return:
        '''

        self.stats.add_general_stats_record({
            'year': year,
            'amount': len(self.people.keys()),

            'type': 'People alive',
            'scale': 'human'
        })

        self.stats.add_general_stats_record({
            'year': year,
            'amount': len(self.homeless_people),
            'type': 'Homeless people',
            'scale': 'human'
        })

        self.stats.add_general_stats_record({
            'year': year,
            'amount': len(self.houses),
            'type': 'houses',
            'scale': 'human'
        })

        self.stats.add_general_stats_record({
            'year': year,
            'amount': self.founder.money,
            'type': 'Founder money',
            'scale': 'money'
        })

        self.stats.add_general_stats_record({
            'year': year,
            'amount': self.founder.spent_building_houses,
            'type': 'Spent building houses',
            'scale': 'money'
        })

    def record_example_house_stats(self, year):
        '''
        Records the history of the shares for one example house
        :param year:
        :return:
        '''
        _house = self.houses[0]
        self.stats.add_example_house_stats_record({
            'year': year,
            'shares': _house.founder_shares,
            'name': self.founder.name,

        })
        for person_id, shares in _house.share_owners.items():
            self.stats.add_example_house_stats_record({
                'year': year,
                'shares': shares,
                'name': self.people[person_id].name,

            })

    def __repr__(self):

        houses = ''
        for i, house in self.houses.items():

            tenant = ''
            if i in self.house_tenants:
                tenant_name = self.people[self.house_tenants[i]].name
                tenant = f', current tenant:[{tenant_name}]'

            houses += f'\n[{house.name}]: share price:${house.share_price:.2f}, share owners:{house.share_owners}, founder has {house.founder_shares}/{house.total_shares} shares, inflation:{house.inflation:.2f}{tenant}'
        people = ''
        for i, person in self.people.items():

            house = ', is homeless'
            for _house_id, _person_id in self.house_tenants.items():
                if _person_id == i:
                    house = f', lives in [{self.houses[_house_id].name}]'
            inheritance_info = f' shares_inherited:{person.shares_inherited},' if self.inheritance else ''

            people += f'\n[{person.name} (parent:{person.parent})]: money:${person.money:.2f}, age:{person.age:.2f},{inheritance_info} changed {person.changed_house} times{house}'

        return \
            f'''
-----------------------------
Year {self.current_tick / MONTHS_PER_YEAR:.0f}, month {self.current_tick % MONTHS_PER_YEAR + 1}
-----------------------------
{self.founder.name}, money:${self.founder.money:.2f} age:{self.founder.age:.0f}
Tenants: {self.house_tenants}
Homeless people: {self.homeless_people}
-----------------------------
Current houses: 
{houses}
-----------------------------
Current people: 
{people}
-----------------------------
Deceased:
{self.dead_people}
        '''
