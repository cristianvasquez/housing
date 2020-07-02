from simulator.setup import MONTHS_A_PERSON_LIVES, MONTHS_PER_YEAR

import numpy as np

AVERAGE_HOUSE_COST = MONTHS_PER_YEAR * 40 * 15  # 7200


def new_random_house(name=''):
    sigma = 200
    # The price of the house is taken from a normal distribution, sigma as standard deviation
    house_price = np.random.normal(AVERAGE_HOUSE_COST, sigma)
    number_of_shares = MONTHS_A_PERSON_LIVES
    share_price = house_price / number_of_shares

    return House(number_of_shares=number_of_shares, share_price=share_price, name=name), house_price


class House:
    def __init__(self, number_of_shares=0, share_price=10, share_owners=None, name=''):
        '''
        A house has a price that we initially divided into a fixed amount of shares.
        The number of shares corresponds to the number of months an average person can live,
        the idea is that the ownership of the owner can decay in one generation

        :param number_of_shares:
        :param share_price:
        :param share_owners:
        :param name:
        '''
        if share_owners is None:
            share_owners = {}
        self.founder_shares = number_of_shares
        self.share_owners = share_owners
        self.share_price = share_price
        self.name = name

        self.inflation = 0

    @property
    def total_shares(self):
        total = 0
        for k, v in self.share_owners.items():
            total += v

        return total + self.founder_shares

    def assign_share(self, person_id):

        # Ownership of the founder decays by one share each month
        if self.founder_shares > 0:
            self.founder_shares -= 1
        else:
            '''
            When the founder shares decay to 0
            some sort inflationary effect begins, 
            the number of shares become more than the initial amount
            '''
            self.inflation += 1  # Just for stats purposes

        # Increment the shares of a person_id by one
        if person_id in self.share_owners:
            self.share_owners[person_id] += 1
        else:
            self.share_owners[person_id] = 1

    def inherit_to_sibling(self, deceased_id, heir_id):
        '''
        Inheritance is the practice of passing on private property,
        titles, debts, rights, and obligations upon the death of an individual.
        '''
        assert (deceased_id in self.share_owners)
        amount = self.share_owners[deceased_id]
        del self.share_owners[deceased_id]

        if heir_id in self.share_owners:
            self.share_owners[heir_id] += amount
        else:
            self.share_owners[heir_id] = amount

        return amount

    def inherit_to_founder(self, deceased_id):
        assert (deceased_id in self.share_owners)
        amount = self.share_owners[deceased_id]
        del self.share_owners[deceased_id]

        self.founder_shares += amount
        return amount
