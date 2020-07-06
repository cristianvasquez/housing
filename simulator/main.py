from simulator.house import new_random_house
from simulator.policy import apply_custom_policy
from simulator.simulation import Community
from simulator.setup import DEFAULT_SETUP
from simulator.shareholder import Shareholder

def run_for_one_month(state, setup, verbose):
    state.do_life_and_death_step()
    state = apply_custom_policy(state,setup,verbose=verbose)
    state.do_income_and_taxes_step()
    state.so_shares_step()
    state.next_timestep()
    return state


def run(
        setup=DEFAULT_SETUP,
        verbose=True,
        ):
    founder = Shareholder(age=0, money=0, name='Founder')
    state = Community(founder=founder, setup=setup)

    initial_number_of_people = setup['initial_number_of_people']
    initial_number_of_houses = setup['initial_number_of_houses']
    ruleset = setup['ruleset']

    for i in range(initial_number_of_people):
        # newborns initially have no house (homeless status)
        state.add_new_born()

    for i in range(initial_number_of_houses):
        house, price = new_random_house(setup,f'initial house {state.house_max_id}')
        # houses are initially owned by the founder
        state.add_new_house(house)

        # The initial debt of the founder
        founder.money = -price
        founder.period_spent_building_houses += price

    if verbose:
        print(
            f'Simulation starts with {initial_number_of_houses} initial houses and {initial_number_of_people} people, ruleset:{ruleset}')

    for i in range(setup['number_of_months_to_run']):
        state = run_for_one_month(state,setup,verbose)

    if verbose:
        print(state)

    return state.stats


if __name__ == '__main__':
    run()
