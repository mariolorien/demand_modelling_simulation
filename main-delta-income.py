"""
Income-change main script.

Scenario:
    - Build an Economy with N households
    - Apply a change in INCOME (same factor for all households)
    - Summarise new demand
    - Plot demand and budget share by income group
"""

from Economy import Economy, economy_calculations, build_summary_and_plot_data
from plots import (
    plot_demand_by_income_group_income_change,
    plot_budget_share_by_income_group_income_change,
)
import matplotlib.pyplot as plt


def main():
    household_number = 200
    econ = Economy(household_number=household_number)
    econ.create_economy()

    #  Define the income scenario
    # Interpreted as a MULTIPLICATIVE FACTOR on income, e.g. 1.10 = +10%.
    income_factor = 1.5


    #  Run calculations (INCOME CHANGE scenario)
    economy_calculations(econ, new_income=income_factor)

    # Build table + plot data by income group
    # For the income-change case, the price does NOT change, so we use
    # the baseline food price when computing the new budget share.
    baseline_price = econ.households[0].food_price
    table_summary, plot_data = build_summary_and_plot_data(
        econ,
        new_food_price=baseline_price,
    )

    # Print the table summary to the terminal
    print("\n=== INCOME CHANGE SCENARIO ===")
    print(f"Income factor: ×{income_factor:.2f}")
    print("\nTable summary (NEW demand, market level):")
    for key, value in table_summary.items():
        print(f"  {key}: {value:.3f}")

    # Generate the plots (income-change versions)
    #    a) Quantity demanded by income group
    plot_demand_by_income_group_income_change(plot_data, income_factor=income_factor)

    #    b) Budget share by income group
    plot_budget_share_by_income_group_income_change(
        plot_data,
        income_factor=income_factor,
    )
    plt.show()


if __name__ == "__main__":
    main()
