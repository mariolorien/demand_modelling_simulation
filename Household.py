import numpy as np


class Household: 
    def __init__(
        self,
        income=1,
        food_budget_share=0.3,
        food_baseline_buy=1,
        income_elasticity_food=0.8,
        price_elasticity_food=-0.6,
        food_price=1.0,
    ):
        self.income = income
        self.food_budget_share = food_budget_share
        self.food_baseline_buy = food_baseline_buy
        self.income_elasticity_food = income_elasticity_food 
        self.price_elasticity_food = price_elasticity_food
        self.food_price = food_price

        # Compute baseline quantity at initialisation
        self.food_baseline_buy = self.calculate_food_baseline_buy()

    def calculate_food_baseline_buy(self): 
        """
        Baseline quantity of food.

        Baseline food spending = income * food_budget_share.
        Quantity = spending / food_price.

        Because we are currently setting food_price = 1, dividing by self.food_price
        does not change the value numerically: spending and quantity coincide.
        This division is included to make the formula explicit for later, when
        you may want to use a price different from 1.
        """
        food_spending = self.income * self.food_budget_share
        food_baseline_buy = food_spending / self.food_price
        self.food_baseline_buy = food_baseline_buy
        return food_baseline_buy
        
    def calculate_new_food_demand_income_change(self, new_income):
        """
        Scenario: only income changes, price stays at the baseline value.

        Uses: Δln q = income_elasticity_food * Δln income
              q_new = q_baseline * exp(Δln q)
        """
        ln_change_income = np.log(new_income)  # natural log (ln)
        delta_ln_q = self.income_elasticity_food * ln_change_income
        new_absolute_food_demand = self.food_baseline_buy * np.exp(delta_ln_q)
        return new_absolute_food_demand

    def calculate_new_food_demand_price_change(self, new_food_price):
        """
        Scenario: only price changes, income stays at the baseline value.

        Uses: Δln q = price_elasticity_food * Δln price
              q_new = q_baseline * exp(Δln q)
        """
        ln_change_price = np.log(new_food_price) - np.log(self.food_price)
        delta_ln_q = self.price_elasticity_food * ln_change_price
        new_absolute_food_demand = self.food_baseline_buy * np.exp(delta_ln_q)
        return new_absolute_food_demand
