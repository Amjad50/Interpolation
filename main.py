from lib.interpolate import Interpolator

a = Interpolator()

points = [(1, 3), (1/2, -10), (3, 2), (5, 3/2), (7, 1)]

print(f"number of points = {len(points)}")

print("building the interpolation...\n")
for point in points:
	a.add(point[0], point[1])

print(f"The final interpolated function is \n\nf(x) = {a}")


