import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sps

START_BASE = 2
END_BASE = 125


# ============ CALCULATION ============
def digits_to_decimal(base, digits):
    base_list = np.ones(len(digits)) * base
    base_powers = np.power(base_list, np.arange(len(digits) - 1, -1, -1))
    return np.dot(digits, base_powers)


def quotient(base):
    den = digits_to_decimal(base, np.arange(1, base))
    num = digits_to_decimal(base, np.arange(base - 1, 0, -1))
    return num / den


# ============ PLOTTING ============
x = list(range(START_BASE, END_BASE + 1))
y = [quotient(i) for i in x]

plt.figure(figsize=(6.4, 4.8))
plt.plot(x, y)
plt.xlabel('Base')
plt.ylabel('Quotient')
plt.savefig('plot.png')

# ============ LINEAR REGRESSION ===========
regression = sps.linregress(x, y)
print(regression)
print(f'r-squared: {regression[2] ** 2}')
