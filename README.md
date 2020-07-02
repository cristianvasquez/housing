# Housing by shares

We need a house to live in. To do so, the most common options are:

1. To rent a house
2. To buy a house

This simulation explores "Housing by shares," a hybrid mechanism that lives somewhere in between option 1 and 2

# The problem

Everyone wants to own a house, but not everyone can buy a home.

The ability to own a house is determined by an individual's access (or lack of access) to financing, and lower-income individuals have less access. 
Banks are more likely to offer to finance to those who already own capital or, thanks to higher incomes, have greater repayment capacities.

People with lower-income must take on significant and unsustainable debt burdens, which reduced wealth among the bottom income groups, increased poverty, and further exasperated inequalities.

Also, Inheritance plays a significant effect on social stratification, affecting the distribution of wealth. Heritage is transmitted across generations, determining people's chances in society.  Those who receive an inheritance are more likely to own a home than those who do not.

How can we smooth these existing disparities, which also have intergenerational consequences?

## The mechanism

A person pays a fee to live in a house just like in renting, but with the possibility of owning a fraction of the house, materialized in shares. The paid price goes proportionally to all the share-holders that previously lived in the house.

The idea is that a person collects several shares during her lifetime, that will represent an income in the future, especially when the person is retired.

## Setup

A community needs a founder, for example, the government. 

Houses enter the community, bought in traditional markets by the founder.  Each time a house enters, it's initial value is divided into a fixed amount of shares that are transferred to the founder, meaning that in the beginning, he is the only shareholder.

If a person wants to live for one month in one of those houses, she has to pay a fee corresponding to the price of a share. The paid amount goes proportionally to all share-holders, then one share is created to be owned by the person, and one share of the founder is destroyed.

## Simulation

I don't have a finished idea of how this would work, so I programmed a simple simulation that uses the following initial values:

The number of initial shares created corresponds to the number of months an average person can live. 

The price of each share is simply the house's initial price divided by the number of initial shares

Since this is only a preliminary exploration, I try to keep it simple. 
The simulation does not apply taxes.
Shares are not bought or sold on the open market

When a person dies, his shares are transferred back to the founder or to a random sibling if the inheritance option is enabled.

To run the application:

```
python application.py
```

## Other remedies  (from Wikipedia)

Proposals to remedy the adverse effects of housing inequality include:

Subsidized housing, also known as affordable housing. Subsidized housing includes:
* Co-operative housing
* Non-profit housing
* Direct housing
* Public housing
* Rent supplements
* Scattered-site housing - A housing system where rent is based on household income
* Fair-lending enforcement - Lenders are expected to not discriminate against borrowers because of family status, race, originality, gender, and color


