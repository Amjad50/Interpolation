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
			self.c_data.append((y - self.compute(x)) / self.x_differences(x))
		except:
			raise ArithmeticError(f"this value of x ({x}) already exists")
		self.x_data.append(x)
		self.y_data.append(y)

		if x > self.max:
			self.max = x
		if x < self.min:
			self.min = x

	def x_differences(self, x):
		res = 1
		
		for i in self.x_data:
			res *= (x - i)

		return res

	def compute(self, x):
		res = self.c_data[0] if len(self.c_data) > 0 else 0

		total_sub_x = 1

		for i in range(1, len(self.c_data)):
			total_sub_x *= (x - self.x_data[i - 1])
		
			res += self.c_data[i] * total_sub_x

		return res
	
	def __str__(self):
		res = []
		
		for i in range(len(self.c_data)):
			sub_res = str(self.c_data[i])

			for j in range(i):
				sub_res += f'(x - {self.x_data[j]})'	
		
			res.append(sub_res)

		final =  ' + '.join(res)
		return final.replace(' + -', ' - ').replace(' - -', ' + ')

