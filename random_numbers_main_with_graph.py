from fractions import Fraction
from random import randint

import numpy as np

from lib.graph import Plotter, plt
from lib.interpolate import Interpolator

p = Plotter()


def run(N):
    a = Interpolator()

    x_d = list({Fraction(randint(-200, 200), randint(1, 20)) for _ in range(N)})

    print(f"number of points = {len(x_d)}")

    y_d = [Fraction(randint(-2000, 2000), randint(1, 20)) for _ in range(len(x_d))]

    print("building the interpolation...\n")
    for i in range(len(x_d)):
        a.add(x_d[i], y_d[i])
        done = i / len(x_d)
        still = 1 - done
        size = 20
        print(f'\r{"=" * int(done * size) + "-" * int(still * size)}', flush=True, end=f'{i}/{len(x_d)}')

    print(f"\n\nThe final interpolated function is \n\nf(x) = {a}")

    x = np.arange(a.min - 0.1, a.max + 0.1, 0.1)
    y = []

    print("building the visualization graph...\n")
    for i in range(len(x)):
        y.append(a.compute(x[i]))
        done = i / len(x)
        still = 1 - done
        size = 20
        print(f'\r{"=" * int(done * size) + "-" * int(still * size)}', flush=True, end=f'{i}/{len(x)}')

    p.clear()
    plt.ylim(float(np.min(a.y_data)) - 10, float(np.max(a.y_data)) + 10)
    p.add_line(x, y)
    p.add_points(a.x_data, a.y_data)

    print('\n\n')


while True:
    try:
        N = int(input("Enter a number of points, -1 to quit >> "))
    except:
        print("wrong format")
        continue

    if N == -1:
        break
    run(N)

p.show()
