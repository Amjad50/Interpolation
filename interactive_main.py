from interpolate import Interpolator
from fractions import Fraction
from time import process_time_ns as time
from colors import color_print


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
			'config': (self.cmd_set_config, "Sets the value of one of the configuration, (key=value), to see the current config type `set` without parameters"),
			'clear': (self.cmd_clear, "Clears the current interpolation"),
			'exit': (self.cmd_exit, "Exit from this program"),
		}

		self.__max_length_cmd = max(map(len, self.commands_map))

		__set_boolean_helper = lambda x: False if x.lower() == 'false' or (len(x) and x.lower()[0] == 'f') else bool(x)

		self.config = {
			# not the best way to know if the value is false or not, but mah.
			'show-time': [__set_boolean_helper, False],
			'show-colors': [__set_boolean_helper, True],
		}

		self.interpolator = Interpolator()

	def cmd_help(self, *args):
		# this format_string is to set an indentation for the commands and their help message,
		# which depend on __max_length_cmd.
		format_string = '#MAGENTA#{:' + str(self.__max_length_cmd) + '}\t%#GREEN#{}%'
		self.__print('\n'.join([format_string.format(k, v[1]) for k, v in self.commands_map.items()]))

	def cmd_add_point(self, *args):
		try:
			x, y = map(lambda x: Fraction(x.strip()), args[:2])
			self.interpolator.add(x, y)
			self.__print(f'$#LIGHTBLUE#[*]% added #GREEN#({x}, {y})%')
		except ArithmeticError:
			self.__print(f'#RED#[ERROR]% the value of #GREEN#x = {x}% already exists')
		except:
			self.__print('#RED#[ERROR]% the input for #GREEN#add% is not correct')

	def cmd_add_points(self, *args):
		l = len(args)
		if l % 2 != 0:
			l -= 1
			self.__print(f'#YELLOW#[WARN]% ignoring value #GREEN#x = {args[-1]}% as there is no #GREEN#y% value to it')

		for i in range(l // 2):
			self.cmd_add_point(args[i * 2], args[(i * 2) + 1])

	def cmd_exit(self, *args):
		return self.BREAK

	def cmd_print(self, *args):
		size = self.interpolator.size()

		if size:
			self.__print(f'#LIGHTBLUE#P#GREEN#{self.interpolator.size() - 1}#LIGHTBLUE#(x) =% {self.interpolator}')
		else:
			self.__print('#YELLOW#[WARN]% No data points, nothing to print...')

	def cmd_compute(self, *args):
		if args:
			if size := self.interpolator.size():
				try:
					x = Fraction(args[0])
					result = self.interpolator.compute(x)
					self.ans = result
					self.__print(f'#MAGENTA#ans =% #LIGHTBLUE#P{size - 1}(#GREEN#{x}%#LIGHTBLUE#) =% {result}')
				except:
					self.__print(f'#RED#[ERROR]% Error in evaluating value #GREEN#x = {args[0]}%')
			else:
				self.__print('#RED#[ERROR]% there is no data points to build the interpolation function')
		else:
			self.__print('#RED#[ERROR]% no value #GREEN#x% specified')

	def cmd_print_ans(self, *args):
		if 'ans' in dir(self):
			self.__print(f'#MAGENTA#ans =% {self.ans}')
		else:
			self.__print('#RED#[ERROR]% There is no value for #MAGENTA#ans% yet, you can get a value for #MAGENTA#ans% by #GREEN#compute%')

	def cmd_approx_ans(self, *args):
		if 'ans' in dir(self):
			self.__print(f'#MAGENTA#ans =% {float(self.ans):.5f}')
		else:
			self.__print('#RED#[ERROR]% There is no value for #MAGENTA#ans% yet, you can get a value for #MAGENTA#ans% by #GREEN#compute%')

	def cmd_set_config(self, *args):
		if len(args):
			try:
				k, v = (''.join(args)).split('=')

				if k in self.config:
					self.config[k][1] = self.config[k][0](v)
					self.__print(f'$#LIGHTBLUE#[*]% config #GREEN#{k}% updated to #MAGENTA#{self.config[k][1]}%')
				else:
					self.__print(f'#RED#[ERROR]% key #GREEN#{k}% was not found in the configuration')
			except:
				self.__print('#RED#[ERROR]% wrong format for setting config values')
		else:
			self.__print('\n'.join([f'#GREEN#{k} = #MAGENTA#{v[1]}%' for k, v in self.config.items()]))



	def cmd_clear(self, *args):
		self.__print('$#LIGHTBLUE#[*] clearing...%')
		self.interpolator = Interpolator()
		if 'ans' in dir(self):
			del self.ans

	def cmd_exit(self, *args):
		return self.BREAK

	def run_command(self, commandline):
		command, *args = commandline.split()
		command = command.strip()
		if command in self.commands_map:
			start_t = -1
			if self.config['show-time'][1]:
				start_t = time()

			ret_val = self.commands_map[command][0](*args)

			# very weird to print the time it takes to exit haha
			if start_t != -1 and command != 'exit':
				end_t = time()
				self.__print(f'\n#LIGHTBLUE#[-] took $#GREEN#{(end_t - start_t) / 1000000:.5f}% #LIGHTBLUE#milliseconds%')

			return ret_val
		else:
			self.__print(f'#RED#[ERROR]% command #MAGENTA#{command}% could not be found')

	def __print(self, *args):
		color_print(*args, color=self.config['show-colors'][1])

def welcome_message():
	color_print(
r"""
#GREEN#Welcome to The%#LIGHTBLUE#
 ______          __                                  ___             __
/\__  _\        /\ \__                              /\_ \           /\ \__
\/_/\ \/     ___\ \ ,_\    __   _ __   _____     ___\//\ \      __  \ \ ,_\   ___   _ __
   \ \ \   /' _ `\ \ \/  /'__`\/\`'__\/\ '__`\  / __`\\ \ \   /'__`\ \ \ \/  / __`\/\`'__\
    \_\ \__/\ \/\ \ \ \_/\  __/\ \ \/ \ \ \L\ \/\ \L\ \\_\ \_/\ \L\.\_\ \ \_/\ \L\ \ \ \/
    /\_____\ \_\ \_\ \__\ \____\\ \_\  \ \ ,__/\ \____//\____\ \__/.\_\\ \__\ \____/\ \_\
    \/_____/\/_/\/_/\/__/\/____/ \/_/   \ \ \/  \/___/ \/____/\/__/\/_/ \/__/\/___/  \/_/
                                         \ \_\
                                          \/_/
#GREEN#type #MAGENTA#help#GREEN# to access the available commands you can use, enjoy.%
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
