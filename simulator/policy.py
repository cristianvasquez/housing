import random

from simulator.house import new_random_house


def apply_custom_policy(state, setup, verbose=True):
    '''
    This corresponds to choices that people and founder can take
    '''

    for current_house, tenant in state.house_tenants.items():
        if (random.random() < setup['probability_of_changing_house']):
            # print(f'tenant {tenant} tries to find another house')
            prospect_house, price = state.random_available_house(state.people[tenant].money)
            if prospect_house is not None:
                # print(f'{tenant} moves to house {prospect_house} for ${price}')
                state.occupy_house(tenant, prospect_house)
                state.people[tenant].changed_house += 1
            # else:
            #     print(f'tenant {tenant} did not find another house')

    # All homeless people try to rent a house with a probability 0.9
    for person_id in state.homeless_people.copy():
        if (random.random() < 0.9):
            available_money = state.people[person_id].money
            # print(f'homeless {person_id} tries to find a house with ${available_money}')
            prospect_house, price = state.random_available_house(available_money)
            if prospect_house is not None:
                # print(f'homeless {person_id} rents house {prospect_house} for ${price}')
                state.occupy_house(person_id, prospect_house)
            else:
                if verbose:
                    print(
                        f'homeless {person_id} did not find a house, available_money:{available_money} available_houses:{state.available_houses}')

    #  if there are few houses available, brother state tries to build new ones
    if len(state.available_houses) < setup['minimum_free_houses_policy']:
        house, price = new_random_house(setup, f'new house {state.house_max_id}')

        state.founder.money -= price
        state.founder.period_spent_building_houses += price
        state.add_new_house(house)

    return state
