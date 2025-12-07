"""
plots.py

Plotting utilities for the demand modelling simulation.

Assumes that for BOTH price and income scenarios you pass in a
`plot_data` dict with the following keys:

    - "groups": list of group labels (e.g. ["Q1", "Q2", "Q3", "Q4"])
    - "baseline_demand": list of baseline average demands per group
    - "new_demand": list of new average demands per group
    - "baseline_budget_share": list of baseline food budget shares per group
    - "new_budget_share": list of new food budget shares per group

Price-change and income-change functions differ only in labels/titles.
"""

import numpy as np
import matplotlib.pyplot as plt


# ===================== PRICE CHANGE PLOTS =====================

def plot_demand_by_income_group(plot_data, new_price):
    """
    Plot baseline vs new food demand by income group (Q1-Q4),
    for a PRICE CHANGE scenario.

    Parameters
    ----------
    plot_data : dict
        Must contain keys:
          - "groups"
          - "baseline_demand"
          - "new_demand"
    new_price : float
        New price level (e.g. 1.10 for a 10% increase).
    """
    groups = plot_data["groups"]
    baseline = plot_data["baseline_demand"]
    new = plot_data["new_demand"]

    x = np.arange(len(groups))
    width = 0.35

    plt.figure()
    plt.bar(x - width / 2, baseline, width, label="Baseline demand")
    plt.bar(x + width / 2, new, width,
            label=f"New demand (price = {new_price:.2f})")

    plt.xticks(x, groups)
    plt.xlabel("Income group")
    plt.ylabel("Average food quantity")
    plt.title("Food demand by income group: baseline vs new (price change)")
    plt.legend()
    plt.tight_layout()


def plot_budget_share_by_income_group(plot_data, new_price):
    """
    Plot baseline vs new food budget share by income group (Q1-Q4),
    for a PRICE CHANGE scenario.

    Parameters
    ----------
    plot_data : dict
        Must contain keys:
          - "groups"
          - "baseline_budget_share"
          - "new_budget_share"
    new_price : float
        New price level (e.g. 1.10 for a 10% increase).
    """
    groups = plot_data["groups"]
    baseline = plot_data["baseline_budget_share"]
    new = plot_data["new_budget_share"]

    x = np.arange(len(groups))
    width = 0.35

    plt.figure()
    plt.bar(x - width / 2, baseline, width, label="Baseline budget share")
    plt.bar(x + width / 2, new, width,
            label=f"New budget share (price = {new_price:.2f})")

    plt.xticks(x, groups)
    plt.xlabel("Income group")
    plt.ylabel("Average food budget share")
    plt.title("Food budget share by income group: baseline vs new (price change)")
    plt.legend()
    plt.tight_layout()


# ===================== INCOME CHANGE PLOTS =====================

def plot_demand_by_income_group_income_change(plot_data, income_factor):
    """
    Plot baseline vs new food demand by income group (Q1-Q4),
    for an INCOME CHANGE scenario.

    Parameters
    ----------
    plot_data : dict
        Must contain keys:
          - "groups"
          - "baseline_demand"
          - "new_demand"
    income_factor : float
        Multiplicative income factor (e.g. 1.10 for +10% income).
    """
    groups = plot_data["groups"]
    baseline = plot_data["baseline_demand"]
    new = plot_data["new_demand"]

    x = np.arange(len(groups))
    width = 0.35

    plt.figure()
    plt.bar(x - width / 2, baseline, width, label="Baseline demand")
    plt.bar(x + width / 2, new, width,
            label=f"New demand (income × {income_factor:.2f})")

    plt.xticks(x, groups)
    plt.xlabel("Income group")
    plt.ylabel("Average food quantity")
    plt.title("Food demand by income group: baseline vs new (income change)")
    plt.legend()
    plt.tight_layout()


def plot_budget_share_by_income_group_income_change(plot_data, income_factor):
    """
    Plot baseline vs new food budget share by income group (Q1-Q4),
    for an INCOME CHANGE scenario.

    Parameters
    ----------
    plot_data : dict
        Must contain keys:
          - "groups"
          - "baseline_budget_share"
          - "new_budget_share"
    income_factor : float
        Multiplicative income factor (e.g. 1.10 for +10% income).
    """
    groups = plot_data["groups"]
    baseline = plot_data["baseline_budget_share"]
    new = plot_data["new_budget_share"]

    x = np.arange(len(groups))
    width = 0.35

    plt.figure()
    plt.bar(x - width / 2, baseline, width, label="Baseline budget share")
    plt.bar(x + width / 2, new, width,
            label=f"New budget share (income × {income_factor:.2f})")

    plt.xticks(x, groups)
    plt.xlabel("Income group")
    plt.ylabel("Average food budget share")
    plt.title("Food budget share by income group: baseline vs new (income change)")
    plt.legend()
    plt.tight_layout()
