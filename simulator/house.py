import numpy as np


def new_random_house(setup, name=''):
    # The price of the house is taken from a normal distribution, sigma as standard deviation
    house_cost = np.random.normal(setup['average_house_cost'], setup['sigma_house_cost'])
    number_of_shares = setup['number_of_shares_per_house']

    house_to_rent_ratio = setup['house_to_rent_ratio']
    rent_price = house_cost * house_to_rent_ratio
    shares_per_month = setup['shares_per_month_earnings']

    return House(number_of_shares=number_of_shares, rent_price=rent_price, shares_per_month=shares_per_month,
                 name=name), house_cost


class House:
    def __init__(self, number_of_shares=0, rent_price=10, shares_per_month=1, name=''):
        '''
        A house has a price that we initially divided into a fixed amount of shares.
        The number of shares corresponds to the number of months an average person can live,
        the idea is that the ownership of the owner can decay in one generation
        '''
        self.share_owners = {}
        self.founder_shares = number_of_shares
        self.rent_price = rent_price
        self.name = name
        self.inflation = 0
        self.shares_per_month = shares_per_month

    @property
    def total_shares(self):
        total = 0
        for k, v in self.share_owners.items():
            total += v

        return total + self.founder_shares

    def assign_share(self, person_id):

        # Ownership of the founder decays by one share each month
        if self.founder_shares > 0:
            self.founder_shares -= self.shares_per_month
        else:
            '''
            When the founder shares decay to 0
            some sort inflationary effect begins, 
            the number of shares become more than the initial amount
            '''
            self.inflation += self.shares_per_month  # Just for stats purposes

        # Increment the shares of a person_id by one
        if person_id in self.share_owners:
            self.share_owners[person_id] += self.shares_per_month
        else:
            self.share_owners[person_id] = self.shares_per_month

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
