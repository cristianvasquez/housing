from housing import Community
from setup import MONTHS_A_PERSON_LIVES
from shareholder import shareholder_policy, Shareholder


def month(community):
    community.step_life_and_death()
    community = shareholder_policy(community)
    community.step_income_and_taxes()
    community.step_acquire_shares()
    community.increase_tick()
    return community


def run(number_of_months=MONTHS_A_PERSON_LIVES * 2, initial_number_of_people=5, initial_number_of_houses=6,
        inheritance=False):
    brother_state = Shareholder(age=0, money=0, name='Brother State')
    community = Community(brother_state=brother_state, inheritance=inheritance)

    # newborns initially have no house (homeless status)
    for i in range(initial_number_of_people):
        community.add_new_born()

    for i in range(initial_number_of_houses):
        community.add_new_house()

    for i in range(number_of_months):
        community = month(community)

    print(community)
    return community.stats
