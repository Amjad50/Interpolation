from lib.interpolate import Interpolator
from random import randint
from fractions import Fraction
from time import time

def run(N):
	start = time()

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

	print(f"\n\nThe final interpolated function is \n\nP{len(a.x_data) - 1}(x) = {a}")

	end = time()
	
	print()
	print(f"took {end-start:0.5f} seconds")


while True:
	try:
		N = int(input("Enter a number of points, -1 to quit >> "))
	except:
		print("wrong format")
		continue
	
	if N == -1:
		break
	
	run(N)

