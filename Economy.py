import numpy as np
from Household import Household  # adjust path if needed


class Economy:
    def __init__(self, household_number):
        self.household_number = household_number
        self.households = []
        self.aggregate_food_baseline = 0.0
        self.aggregate_food_demand_income_change = 0.0
        self.aggregate_food_demand_price_change = 0.0
        self.income = None 
        self.current_income = self.income

    def create_economy(self):
        """
        Create 'household_number' Household objects.

        Incomes are drawn from a lognormal distribution calibrated
        to roughly match Gini ≈ 1/3 and P90/P10 ≈ 4 via sigma ≈ 0.55.
        Quartiles of the income distribution are then used to assign
        different food budget shares following Engel's law
        (poorer households -> higher food share).
        """

        # Generate all incomes first
        sigma = 0.55
        # Choose mu so that mean income is about 30,000
        target_mean_income = 30000
        mu = np.log(target_mean_income) - 0.5 * sigma**2

        incomes = np.random.lognormal(mean=mu, sigma=sigma, size=self.household_number)

        # Compute quartile cutoffs (Q1, median, Q3)
        q25, q50, q75 = np.percentile(incomes, [25, 50, 75])

        households = []

        # Create households with income-dependent food budget shares
        for i in range(self.household_number):
            income = incomes[i]

            # Assign food_budget_share based on income quartile (Engel's law)
            if income <= q25:
                # Lowest income group: highest food share
                food_budget_share = np.random.uniform(0.25, 0.35)
                income_group = "Q1"
            elif income <= q50:
                food_budget_share = np.random.uniform(0.20, 0.30)
                income_group = "Q2"
            elif income <= q75:
                food_budget_share = np.random.uniform(0.15, 0.25)
                income_group = "Q3"
            else:
                # Highest income group: lowest food share
                food_budget_share = np.random.uniform(0.10, 0.20)
                income_group = "Q4"

            h = Household(
                income=income,
                food_budget_share=food_budget_share,
                income_elasticity_food=0.8,
                price_elasticity_food=-0.6,
                food_price=1.0,
            )

            # Store the income group label for plotting/aggregation later
            h.income_group = income_group

            households.append(h)

        self.households = households

           
def economy_calculations(economy, new_income=None, new_food_price=None):
    """
    Aggregate baseline and new food demand across all households.
    - economy.households: list of Household objects
    - new_income: if not None, used for income-change scenario
    - new_food_price: if not None, used for price-change scenario
    """

    # initialise aggregates
    economy.aggregate_food_baseline = 0.0
    economy.aggregate_food_demand_income_change = 0.0
    economy.aggregate_food_demand_price_change = 0.0

    for h in economy.households:
        # baseline demand
        h.calculate_food_baseline_buy()
        economy.aggregate_food_baseline += h.food_baseline_buy

        # if an income scenario is provided
        if new_income is not None:  # here new_income is the income_factor
            for h in economy.households:
                h.current_income = h.income * new_income      # NEW LINE
                q_income = h.calculate_new_food_demand_income_change(new_income)
                h.current_food_demand = q_income

        # if a price scenario is provided
        if new_food_price is not None:
            q_price = h.calculate_new_food_demand_price_change(new_food_price)
            h.current_food_demand = q_price  # store for later use
            economy.aggregate_food_demand_price_change += q_price

    # return all three aggregates at the end, AFTER the loop
    return (
        economy.aggregate_food_baseline,
        economy.aggregate_food_demand_income_change,
        economy.aggregate_food_demand_price_change,
    )


def mean_income(economy):
    total_income = sum(h.income for h in economy.households)
    mean_income_value = total_income / len(economy.households)
    return mean_income_value


def median_income(economy):
    incomes = [h.income for h in economy.households]
    median_income_value = np.median(incomes)
    return median_income_value


def demand_summary(economy):
    """
    Build summary statistics (mean, median, std, total) of NEW food demand
    using h.current_food_demand for each household.
    """
    q_new = [h.current_food_demand for h in economy.households]

    mean_q = np.mean(q_new)
    median_q = np.median(q_new)
    std_q = np.std(q_new)
    total_q = np.sum(q_new)

    return mean_q, median_q, std_q, total_q


def build_summary_and_plot_data(economy, new_food_price):
    """
    Build:
      1) Summary stats for NEW demand (for the table)
      2) Data by income group (Q1–Q4) for the two plots:
         - baseline vs new demand
         - baseline vs new budget share

    Assumes:
      - economy_calculations(economy, ..., new_food_price=...) has already been called
      - each household h has:
          h.food_baseline_buy
          h.current_food_demand
          h.food_budget_share
          h.income_group
    """

    # ---------- 1. Table summary for NEW demand ----------
    q_new = [h.current_food_demand for h in economy.households]

    mean_q = np.mean(q_new)
    median_q = np.median(q_new)
    std_q = np.std(q_new)
    total_q = np.sum(q_new)

    table_summary = {
        "mean_demand": float(mean_q),
        "median_demand": float(median_q),
        "std_demand": float(std_q),
        "total_demand": float(total_q),
    }

    # ---------- 2. Data by income group for plots ----------
    groups = ["Q1", "Q2", "Q3", "Q4"]

    # Prepare containers
    plot_data = {
        "groups": groups,
        "baseline_demand": [],
        "new_demand": [],
        "baseline_budget_share": [],
        "new_budget_share": [],
    }

    for g in groups:
        # select households in this income group
        group_hh = [h for h in economy.households if h.income_group == g]

        if not group_hh:
            # in case a group is empty (shouldn't happen often)
            plot_data["baseline_demand"].append(0.0)
            plot_data["new_demand"].append(0.0)
            plot_data["baseline_budget_share"].append(0.0)
            plot_data["new_budget_share"].append(0.0)
            continue

        # baseline and new demand
        q_baseline = [h.food_baseline_buy for h in group_hh]
        q_new_g = [h.current_food_demand for h in group_hh]

        # baseline budget share is just the original food_budget_share
        w_baseline = [h.food_budget_share for h in group_hh]

        # new budget share: (new price * new quantity) / income
        w_new = [
             (new_food_price * h.current_food_demand) / h.current_income
             for h in group_hh
        ]


        plot_data["baseline_demand"].append(float(np.mean(q_baseline)))
        plot_data["new_demand"].append(float(np.mean(q_new_g)))
        plot_data["baseline_budget_share"].append(float(np.mean(w_baseline)))
        plot_data["new_budget_share"].append(float(np.mean(w_new)))

    return table_summary, plot_data
