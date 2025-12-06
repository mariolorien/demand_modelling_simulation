"""
Just to test, to be deleted
"""

from Economy import Economy, economy_calculations, demand_summary, build_summary_and_plot_data
import numpy as np


econ = Economy(household_number=200)
econ.create_economy()
new_price = 1.1  # 10% price increase

# Run the scenario: update demands given the new price
economy_calculations(econ, new_food_price=new_price)

# Compute table stats for the NEW demand (market level)
mean_q, median_q, std_q, total_q = demand_summary(econ)

print("Mean demand:", mean_q)
print("Median demand:", median_q)
print("Std of demand:", std_q)
print("Total demand:", total_q)

"""
# Inspect some households
for i, h in enumerate(econ.households[:5], start=1):  # just first 5 to avoid spam
    print(
        f"Household {i} has an income of {h.income:.2f}, "
        f"a food budget share of {h.food_budget_share:.2f}, "
        f"and belongs to the income group {h.income_group}"
    )
"""

# Build data for table + plots by income group
table_summary, plot_data = build_summary_and_plot_data(econ, new_food_price=new_price)

print("\nTable summary dict:")
print(table_summary)

print("\nPlot data dict:")
print(plot_data)
