import math


def compute_interest(principal, rate, time, n=None):
    if n:
        return principal * (1 + rate / n) ** (n * time)
    else:
        return principal * math.e ** (rate * time)


for time in range(1, 10):
    for n in {1, 12, 365, None}:
        print(
            f"time={time}, n={n}, \ninterest={compute_interest(350, 0.0215, time, n)}"
        )
