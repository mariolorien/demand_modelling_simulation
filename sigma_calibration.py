"""
sigma_calibration.py

Helpers to calibrate the sigma parameter of a lognormal income distribution
from a target Gini coefficient and a target P90/P10 ratio.

For a lognormal with log-income variance sigma^2:

- Gini(sigma) = 2 * Phi(sigma / sqrt(2)) - 1 = erf(sigma / 2)
- P90/P10(sigma) = exp(2 * z_0.9 * sigma), where z_0.9 ≈ 1.28155
"""

import math


# ---------- Gini-related functions ----------

def gini_from_sigma(sigma: float) -> float:
    """
    Gini coefficient for a lognormal with log-std = sigma.

    Uses the closed form:
        Gini = 2 * Phi(sigma / sqrt(2)) - 1
             = erf(sigma / 2)
    where Phi is the standard normal CDF and erf is the error function.
    """
    return math.erf(sigma / 2.0)


def sigma_from_gini(target_gini: float,
                    tol: float = 1e-6,
                    max_iter: int = 100) -> float:
    """
    Solve for sigma given a target Gini using simple bisection.

    Gini(sigma) is increasing in sigma, and for reasonable sigma
    values (0, 3) we cover most realistic inequality ranges.
    """
    if not (0.0 < target_gini < 1.0):
        raise ValueError("target_gini must be between 0 and 1.")

    lo, hi = 1e-8, 3.0  # search bracket for sigma

    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        g = gini_from_sigma(mid)

        if abs(g - target_gini) < tol:
            return mid

        if g < target_gini:
            lo = mid   # need larger sigma
        else:
            hi = mid   # need smaller sigma

    # return best guess if we did not hit tolerance exactly
    return mid


# ---------- P90/P10-related functions ----------

# 90th percentile of standard normal N(0, 1)
Z90 = 1.2815515655446004


def p90_p10_from_sigma(sigma: float) -> float:
    """
    P90/P10 ratio for a lognormal with log-std = sigma.

    For ln(X) ~ N(mu, sigma^2), we have:
        Pp = exp(mu + sigma * z_p)

    => P90/P10 = exp(sigma * (z_0.9 - z_0.1))
               = exp(2 * sigma * z_0.9), since z_0.1 = -z_0.9.
    """
    return math.exp(2.0 * Z90 * sigma)


def sigma_from_p90_p10(target_ratio: float) -> float:
    """
    Closed-form sigma from a target P90/P10 ratio for a lognormal.

        P90/P10 = exp(2 * sigma * z_0.9)
        => sigma = ln(target_ratio) / (2 * z_0.9)
    """
    if target_ratio <= 1.0:
        raise ValueError("target_ratio must be > 1.")
    return math.log(target_ratio) / (2.0 * Z90)


# ---------- Example usage when run as a script ----------

if __name__ == "__main__":
    # Your typical targets
    target_gini = 1.0 / 3.0   # ≈ 0.333
    target_ratio = 4.0        # P90/P10 ≈ 4

    sigma_gini = sigma_from_gini(target_gini)
    sigma_ratio = sigma_from_p90_p10(target_ratio)

    print(f"Target Gini:     {target_gini:.3f} -> sigma ≈ {sigma_gini:.4f}")
    print(f"Target P90/P10:  {target_ratio:.3f} -> sigma ≈ {sigma_ratio:.4f}")

    # A simple compromise value (e.g. average the two)
    sigma_avg = 0.5 * (sigma_gini + sigma_ratio)
    print(f"Average of both sigmas ≈ {sigma_avg:.4f}")

    # Optional: show what Gini and P90/P10 that average sigma implies
    g_from_avg = gini_from_sigma(sigma_avg)
    r_from_avg = p90_p10_from_sigma(sigma_avg)
    print(f"Gini at sigma_avg:    {g_from_avg:.3f}")
    print(f"P90/P10 at sigma_avg: {r_from_avg:.3f}")
