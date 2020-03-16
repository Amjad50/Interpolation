from fractions import Fraction

class Interpolator:
	def __init__(self):
		self.x_data = []
		self.y_data = []
		self.c_data = []
		self.min = 0
		self.max = 0

	def add(self, x, y):
		x, y = map(Fraction, (x, y))
		try:
			# TODO: x_differences is computed internally in compute(), change that for more efficiency
			old_computed, x_differences = self.__compute(x)
			self.c_data.append((y - old_computed) / x_differences)
		except:
			raise ArithmeticError(f"this value of x ({x}) already exists")
		self.x_data.append(x)
		self.y_data.append(y)

		if x > self.max:
			self.max = x
		if x < self.min:
			self.min = x

	def __compute(self, x):
		res = self.c_data[0] if len(self.c_data) > 0 else 0

		total_sub_x = 1

		for i in range(1, len(self.c_data)):
			total_sub_x *= (x - self.x_data[i - 1])

			res += self.c_data[i] * total_sub_x

		if len(self.x_data) > 0:
			total_sub_x *= (x - self.x_data[-1])

		return res, total_sub_x

	def compute(self, x):
		return self.__compute(x)[0]

	def __str__(self):
		res = []

		for i in range(len(self.c_data)):
			sub_res = str(self.c_data[i])

			for j in range(i):
				sub_res += f'(x - {self.x_data[j]})'

			res.append(sub_res)

		final =  ' + '.join(res)
		return final.replace(' + -', ' - ').replace(' - -', ' + ')

