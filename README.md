# Demand Modelling Simulation

This project implements a simple demand model for **food consumption** across
heterogeneous households. It focuses on how **changes in price** and
**changes in income** affect:

- Food quantity demanded by income group
- Share of income spent on food (food budget share)

The simulation is intentionally minimal and runs **from the terminal**, producing
both **text summaries** and **Matplotlib plots**.

---

## 1. Conceptual scope

- There are `N` households (e.g. 200) with different incomes.
- Households are grouped into **income quartiles**:
  - Q1: lowest 25% (poorest)
  - Q2: second quartile
  - Q3: third quartile
  - Q4: top 25% (richest)
- Each household has:
  - A baseline income
  - A baseline food budget share
  - Income and price elasticities of demand for food
- Baseline food demand is computed from:
  - Income
  - Food budget share
  - Baseline food price

Two separate experiments are run, each with its own main script:

1. **Price change** (`main-delta-price.py`)
   - Change the food price, holding income constant.
   - Study how food demand and food budget shares adjust by income group.

2. **Income change** (`main-delta-income.py`)
   - Multiply all household incomes by a factor (e.g. income × 1.5).
   - Price remains at the baseline level.
   - Study how food demand and food budget shares adjust by income group.
   - This experiment illustrates **Engel’s law**: as income rises, the share of
     income spent on food tends to fall, especially for richer households.

---

## 2. Project structure

The key files are:

- `Household.py`  
  Defines the `Household` class, including:
  - Baseline income and food budget share
  - Baseline and current food demand
  - Functions for updating demand under price and income changes

- `Economy.py`  
  Defines the `Economy` class and helper functions:
  - Creates the population of households
  - Assigns households to income quartiles
  - Runs the calculations for:
    - Baseline demand
    - Demand under price change
    - Demand under income change
  - Aggregates results and prepares data for plotting

- `plots.py`  
  Contains functions to generate the Matplotlib bar charts for:
  - Food demand by income group (baseline vs new)
  - Food budget share by income group (baseline vs new)
  under both price and income change scenarios.

- `main-delta-price.py`  
  Terminal script that:
  - Builds the economy
  - Applies a **price change** to food
  - Prints summary statistics to the terminal
  - Generates and shows the plots for the price-change scenario

- `main-delta-income.py`  
  Terminal script that:
  - Builds the economy
  - Applies an **income change** (multiplicative factor) to all households
  - Prints summary statistics to the terminal
  - Generates and shows the plots for the income-change scenario

- `sigma_calibration.py`  
  (If used) Contains helper functions to calibrate parameters, elasticities or
  other model constants.

- `environment.yml`  
  Conda environment specification for reproducing the Python environment.

---

## 3. Setting up the environment

You’ll need Conda (Anaconda or Miniconda) installed.

From the project folder (where `environment.yml` lives):

```bash
conda env create -f environment.yml
conda activate demand-modelling

'''

