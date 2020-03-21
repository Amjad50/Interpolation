from interpolate import Interpolator
from fractions import Fraction


class InterpolatorCommandHandler:
	# run_command values
	BREAK = 129

	def __init__(self):
		self.commands_map = {
			'help': (self.cmd_help, "Print the help messages and shows the commands that can be used."),
			'add': (self.cmd_add_point, "Adds x, y value to the interpolation"),
			'add_points': (self.cmd_add_points, "(add_points [x0] [y0]...[xn] [yn]) Adds many points in one go"),
			'print': (self.cmd_print, "Print the interpolation function"),
			'compute': (self.cmd_compute, "Input value x into the function and get the result"),
			'ans': (self.cmd_print_ans, "Print the value of `ans` which is the last computed value"),
			'approx': (self.cmd_approx_ans, "Print the value of `ans` in decimal form (float)"),
			'clear': (self.cmd_clear, "Clears the current interpolation"),
			'exit': (self.cmd_exit, "Exit from this program"),
		}

		self.__max_length_cmd = max(map(len, self.commands_map))

		self.interpolator = Interpolator()

	def cmd_help(self, *args):
		# this format_string is to set an indentation for the commands and their help message, 
		# which depend on __max_length_cmd.
		format_string = '{:' + str(self.__max_length_cmd) + '}\t{}'
		print('\n'.join([format_string.format(k, v[1]) for k, v in self.commands_map.items()]))

	def cmd_add_point(self, *args):
		try:
			x, y = map(lambda x: Fraction(x.strip()), args[:2])
			self.interpolator.add(x, y)
			print(f'[*] added ({x}, {y})')
		except ArithmeticError:
			print(f'[ERROR] the value of x = {x} already exists')
		except:
			print('[ERROR] the input for add_point is not correct')

	def cmd_add_points(self, *args):
		l = len(args)
		if l % 2 != 0:
			l -= 1
			print(f'[WARN] ignoring value x = {args[-1]} as there is no y value to it')

		for i in range(l // 2):
			self.cmd_add_point(args[i * 2], args[(i * 2) + 1])

	def cmd_exit(self, *args):
		return self.BREAK
	
	def cmd_print(self, *args):
		size = self.interpolator.size()

		if size:
			print(f'P{self.interpolator.size() - 1}(x) = {self.interpolator}')
		else:
			print('[WARN] No data points, nothing to print...')

	def cmd_compute(self, *args):
		if args:
			if size := self.interpolator.size():
				try:
					x = Fraction(args[0])
					result = self.interpolator.compute(x)
					self.ans = result
					print(f'ans = P{size}({x}) = {result}')
				except:
					print(f'[ERROR] Error in evaluating value x = {args[0]}')
			else:
				print('[ERROR] there is no data points to build the interpolation function')
		else:
			print('[ERROR] no value x specified')

	def cmd_print_ans(self, *args):
		print(f'ans = {self.ans}')

	def cmd_approx_ans(self, *args):
		if 'ans' in dir(self):
			print(f'ans = {float(self.ans):.5f}')
		else:
			print('[ERROR] There is no value for `ans` yet, you can get a value for `ans` by compute')

	def cmd_clear(self, *args):
		self.interpolator = Interpolator()
		if 'ans' in dir(self):
			del self.ans

	def cmd_exit(self, *args):
		return self.BREAK

	def run_command(self, commandline):
		command, *args = commandline.split()
		command = command.strip()
		if command in self.commands_map:
			return self.commands_map[command][0](*args)
		else:
			print(f'[ERROR] command "{command}" could not be found')

def welcome_message():
	print(
r"""
Welcome to The
 ______          __                                  ___             __
/\__  _\        /\ \__                              /\_ \           /\ \__
\/_/\ \/     ___\ \ ,_\    __   _ __   _____     ___\//\ \      __  \ \ ,_\   ___   _ __
   \ \ \   /' _ `\ \ \/  /'__`\/\`'__\/\ '__`\  / __`\\ \ \   /'__`\ \ \ \/  / __`\/\`'__\
    \_\ \__/\ \/\ \ \ \_/\  __/\ \ \/ \ \ \L\ \/\ \L\ \\_\ \_/\ \L\.\_\ \ \_/\ \L\ \ \ \/
    /\_____\ \_\ \_\ \__\ \____\\ \_\  \ \ ,__/\ \____//\____\ \__/.\_\\ \__\ \____/\ \_\
    \/_____/\/_/\/_/\/__/\/____/ \/_/   \ \ \/  \/___/ \/____/\/__/\/_/ \/__/\/___/  \/_/
                                         \ \_\
                                          \/_/
type "help" to access the available commands you can use, enjoy.
""")


def main():
	cmd = InterpolatorCommandHandler()
	welcome_message()

	while True:
		command = input('>>> ').strip()

		if not command:
			continue

		if cmd.run_command(command) == cmd.BREAK:
			break
		print()


if __name__ == '__main__':
	main()
