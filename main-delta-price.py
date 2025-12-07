"""
Price-change main script.

Scenario:
    - Build an Economy with N households
    - Apply a change in food PRICE
    - Summarise new demand
    - Plot demand and budget share by income group
"""

from Economy import Economy, economy_calculations, build_summary_and_plot_data
from plots import (
    plot_demand_by_income_group,
    plot_budget_share_by_income_group,
)
import matplotlib.pyplot as plt


def main():
    # Create the economy
    household_number = 200
    econ = Economy(household_number=household_number)
    econ.create_economy()

    # Define the price scenario
    # Example: 10% price increase from baseline price = 1.0 to 1.10
    new_price = 1.10

    # Run calculations (PRICE CHANGE scenario)
    economy_calculations(econ, new_food_price=new_price)

    # table + plot data by income group
    table_summary, plot_data = build_summary_and_plot_data(
        econ,
        new_food_price=new_price,
    )

    #  table summary to the terminal
    print("\n=== PRICE CHANGE SCENARIO ===")
    print(f"New price: {new_price:.2f}")
    print("\nTable summary (NEW demand, market level):")
    for key, value in table_summary.items():
        print(f"  {key}: {value:.3f}")

    #Generate the plots
    #    a) Quantity demanded by income group
    plot_demand_by_income_group(plot_data, new_price=new_price)

    #    b) Budget share by income group
    plot_budget_share_by_income_group(plot_data, new_price=new_price)

    plt.show()


if __name__ == "__main__":
    main()
