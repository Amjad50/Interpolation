import numpy as np

from lib.graph import Plotter
from lib.interpolate import Interpolator

a = Interpolator()

points = [(1, 3), (1 / 2, -10), (3, 2), (5, 3 / 2), (7, 1)]

print(f"number of points = {len(points)}")

print("building the interpolation...\n")
for point in points:
    a.add(point[0], point[1])

print(f"\n\nThe final interpolated function is \n\nf(x) = {a}")

p = Plotter()

x = np.arange(a.min - 0.1, a.max + 0.1, 0.1)
y = []

print("building the visualization graph...\n")
for i in range(len(x)):
    y.append(a.compute(x[i]))
    done = i / len(x)
    still = 1 - done
    size = 20
    print(f'\r{"=" * int(done * size) + "-" * int(still * size)}', flush=True, end=f'{i}/{len(x)}')

# plt.ylim(float(np.min(a.y_data)) - 10, float(np.max(a.y_data)) + 10)
p.add_line(x, y)
p.add_points(a.x_data, a.y_data)

print('\n\n')
