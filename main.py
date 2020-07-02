from house import new_random_house
from simulation import Community
from setup import MONTHS_A_PERSON_LIVES
from shareholder import apply_custom_policy, Shareholder


def run_one_month(state):
    state.do_life_and_death_step()
    state = apply_custom_policy(state)
    state.do_income_and_taxes_step()
    state.do_acquire_shares_step()
    state.next_timestep()
    return state


def run(number_of_months=MONTHS_A_PERSON_LIVES * 3,
        initial_number_of_people=5,
        initial_number_of_houses=6,
        allow_inheritance=False):

    founder = Shareholder(age=0, money=0, name='Founder')
    state = Community(founder=founder, allow_inheritance=allow_inheritance)

    for i in range(initial_number_of_people):
        # newborns initially have no house (homeless status)
        state.add_new_born()

    total_price = 0
    for i in range(initial_number_of_houses):
        house, price = new_random_house(f'initial house {state.house_max_id}')
        # houses are initially owned by the founder
        state.add_new_house(house)
        total_price += price

    print(
        f'Simulation starts with {initial_number_of_houses} initial houses and {initial_number_of_people} people, total price:${total_price}')

    for i in range(number_of_months):
        state = run_one_month(state)

    print(state)
    return state.stats


if __name__ == '__main__':
    run()
