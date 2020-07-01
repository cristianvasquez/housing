from setup import MONTHS_A_PERSON_LIVES
import random as np


def new_house(name=''):
    # The price of the share is proportional to the perceived value of the house
    share_price = np.randint(10, 15)
    # Brother state is the founder and owns the initial shares of a house.
    # The number of shares correspond to one generation so they can decay in a fair way
    return House(founder_shares=MONTHS_A_PERSON_LIVES, share_price=share_price, name=name)


class House:
    def __init__(self, founder_shares=0, share_price=10, shares=None, name=''):
        if shares is None:
            shares = {}
        self.founder_shares = founder_shares
        self.shares = shares
        self.share_price = share_price
        self.name = name
        self.inflation = 0

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
        else:
            '''
            When the founder shares decay to 0, and there is inheritance, 
            then an inflationary effect begins, the shares can increase more than the initial
            '''
            self.inflation += 1

        # Increment shares for person_id by one
        if person_id in self.shares:
            self.shares[person_id] += 1
        else:
            self.shares[person_id] = 1

    def inherit_shares(self, deceased_id, child_id):
        assert (deceased_id in self.shares)
        amount = self.shares[deceased_id]
        del self.shares[deceased_id]

        if child_id in self.shares:
            self.shares[child_id] += amount
        else:
            self.shares[child_id] = amount

        return amount

    def founder_inherit_shares(self, deceased_id):
        assert (deceased_id in self.shares)
        amount = self.shares[deceased_id]
        del self.shares[deceased_id]

        self.founder_shares += amount
        return amount
