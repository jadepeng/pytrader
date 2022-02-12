import numpy as np


def get_ols(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    r2 = 1 - (sum((y - (slope * x + intercept)) ** 2) / ((len(y) - 1) * np.var(y, ddof=1)))
    return slope, r2

x = np.array([12, 10, 9, 9.2])
y = np.array([12.5,10.5,9.2,9.5])

x2 = np.array([7,7.2])
y2 = np.array([7.2,7.5])

print(get_ols(x, y))

print(get_ols(x2, y2))
