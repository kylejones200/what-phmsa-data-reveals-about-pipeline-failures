import numpy as np

def issues_per_mile(issues, miles):
    issues = np.asarray(issues, dtype=float)
    miles = np.asarray(miles, dtype=float)
    out = np.zeros_like(issues)
    mask = np.abs(miles) >= 1e-12
    out[mask] = issues[mask] / miles[mask]
    return out
