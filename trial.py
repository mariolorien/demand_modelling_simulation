"""
Just to test, to be deleted
"""

from Economy import Economy, economy_calculations, demand_summary
import numpy as np

econ = Economy(household_number=200)
econ.create_economy()

# run a scenario: e.g. price increase to 1.1
economy_calculations(econ, new_food_price=1.1)

# compute table stats for the NEW demand
mean_q, median_q, std_q, total_q = demand_summary(econ)

print("Mean demand:", mean_q)
print("Median demand:", median_q)
print("Std of demand:", std_q)
print("Total demand:", total_q)



for h in econ.households:
    print(f"{h} has an income of {h.income:.2f}, a food buget of {h.food_budget_share:.2f}, and belongs to the income group {h.income_group}")
