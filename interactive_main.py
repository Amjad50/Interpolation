from lib.interpolate import Interpolator
from fractions import Fraction
from time import process_time_ns as time
from lib.colors import color_format, color_print, supports_color
from re import sub as re_sub
from subprocess import call as call_system_cmd
try:
	import readline
except ImportError:
	color_print("#YELLOW#[WARN]% This system does not support auto completion and history functionality, as it does not have readline library.")

class InterpolatorCommandHandler:
	# some constant value to know if the main should stop its loop
	BREAK = 129

	def __init__(self):
		self.commands_map = {
			'help': (self.cmd_help, "Print the help messages and shows the commands that can be used"),
			'add': (self.cmd_add_point, "Adds x, y value to the interpolation"),
			'addall': (self.cmd_add_all, "(addall [x0] [y0]...[xn] [yn]) Adds many points in one go"),
			'addfile': (self.cmd_add_file, "(addfile <filename>) Adds many points in one go from the file"),
			'savefile': (self.cmd_save_file, "(savefile <filename>) saves the current points stored in the interpolator to a file"),
			'points': (self.cmd_print_points, "print the data points used in the current interpolation"),
			'print': (self.cmd_print, "Print the interpolation function"),
			'compute': (self.cmd_compute, "Input value x into the function and get the result"),
			'ans': (self.cmd_print_ans, "Print the value of `ans` which is the last computed value"),
			'approx': (self.cmd_approx_ans, "Print the value of `ans` in decimal form (float) or compute a new value if specified as argument"),
			'config': (self.cmd_set_config, "Sets the value of one of the configuration, (key=value), to see the current config type `set` without parameters"),
			'clear': (self.cmd_clear, "Clears the current interpolation"),
			'exit': (self.cmd_exit, "Exit from this program"),
		}

		self.__max_length_cmd = max(map(len, self.commands_map))

		__set_boolean_helper = lambda x: False if x.lower() == 'false' or (len(x) and x.lower()[0] == 'f') else bool(x)

		def __set_show_colors(x):
			if supports_color():
				return __set_boolean_helper(x)
			else:
				print("[WARN] This terminal does not support coloring, disabling...")
				return False

		def __set_prompt(x):
			if len(x) >= 2 and (x[0] in '\'"' and x[-1] == x[0]):
				x = x[1:-1]
			return x + '%' # reset the colors if the user didn't do it

		self.config = {
			# not the best way to know if the value is false or not, but mah.
			'show-time': [__set_boolean_helper, False],
			'show-colors': [__set_show_colors, __set_show_colors('True')],
			'prompt': [__set_prompt, '>>>'],
		}

		self.interpolator = Interpolator()

	def get_matched_commands(self, text):
		return [c for c in self.commands_map.keys() if c.startswith(text)]

	def command_completer(self, text, state):
		"""
		This is used by the readline library to implement auto-completion
		"""
		start = readline.get_begidx()
		# if this is in the start, it means it is a command, otherwise the user
		# should supply the input arguments to the command
		if start == 0:
			possible_cmds = self.get_matched_commands(text)
			possible_cmds.append(None)
			return possible_cmds[state]
		elif readline.get_line_buffer().startswith('config') and start == len('config '):
			possible_configs = [c for c in self.config if c.startswith(text)]
			possible_configs.append(None)
			return possible_configs[state]

		return None

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

	def cmd_add_all(self, *args):
		l = len(args)
		if l % 2 != 0:
			l -= 1
			self.__print(f'#YELLOW#[WARN]% ignoring value #GREEN#x = {args[-1]}% as there is no #GREEN#y% value to it')

		for i in range(l // 2):
			self.cmd_add_point(args[i * 2], args[(i * 2) + 1])

	def cmd_add_file(self, *args):
		if len(args) < 1:
			self.__print("#RED#[ERROR]% please provide #MAGENTA#file% to be read from.")
		else:
			filename = args[0]
			try:
				with open(filename, 'r') as f:
					for line in f:
						stripped_line = line.strip()
						if stripped_line:
							line_splitted = stripped_line.split()
							if len(line_splitted) < 2:
								self.__print(f'#YELLOW#[WARN]% ignoring value #GREEN#x = {line_splitted[0]}% as there is no #GREEN#y% value to it')
							else:
								self.cmd_add_point(*line_splitted[:2])
			except PermissionError:
				self.__print(f"#RED#[ERROR]% The file #GREEN#{filename}% could not be read due to insufficient permissions that the current user have.")
			except FileNotFoundError:
				self.__print(f"#RED#[ERROR]% The file #GREEN#{filename}% does not exist.")
			except:
				self.__print(f"#RED#$[PANIC]% unknown error occurred in #MAGENTA#addfile% command, please fix.")

	def cmd_save_file(self, *args):
		if len(args) < 1:
			self.__print("#RED#[ERROR]% please provide #MAGENTA#file% to be saved to.")
		else:
			if self.interpolator.size():
				filename = args[0]
				try:
					with open(filename, 'w') as f:
						for point in zip(self.interpolator.x_data, self.interpolator.y_data):
							print(f'{point[0]} {point[1]}', file=f)

					self.__print(f'$#LIGHTBLUE#[*]% points saved to #MAGENTA#{filename}% successfully')

				except PermissionError:
					self.__print(f"#RED#[ERROR]% The file #GREEN#{filename}% could not be written to due to insufficient permissions that the current user have.")
				except:
					self.__print(f"#RED#$[PANIC]% unknown error occurred in #MAGENTA#addfile% command, please fix.")
			else:
				self.__print('#YELLOW#[WARN]% No data points, nothing to print...')

	def cmd_print_points(self, *args):
		if self.interpolator.size():
			for point in zip(self.interpolator.x_data, self.interpolator.y_data):
				self.__print(f'#LIGHTBLUE#(#GREEN#{point[0]}#LIGHTBLUE#, #GREEN#{point[1]}%#LIGHTBLUE#)%')
		else:
			self.__print('#YELLOW#[WARN]% No data points, nothing to print...')

	@staticmethod
	def _color_interpolation_string_handler(s):
		s = s.group(0)

		color = ''

		if s == ')' or s =='(':
			color = 'LIGHTBLUE'
		elif s == '/' or s == '+' or s == '-':
			color = 'MAGENTA'
		else:
			color = 'GREEN'

		return f'#{color}#{s}%'

	def cmd_print(self, *args):
		size = self.interpolator.size()

		if size:
			interpolation_string = re_sub(r'[0-9]+|[\-\+\/\(\)x]',
				InterpolatorCommandHandler._color_interpolation_string_handler, str(self.interpolator))

			self.__print(f'#LIGHTBLUE#P#GREEN#{self.interpolator.size() - 1}#LIGHTBLUE#(x) =% {interpolation_string}')
		else:
			self.__print('#YELLOW#[WARN]% No data points, nothing to print...')

	def __inner_compute(self, x):
		size = self.interpolator.size()
		if size:
			try:
				x = Fraction(x)
				result = self.interpolator.compute(x)
				self.ans = result
				return x, result
			except:
				self.__print(f'#RED#[ERROR]% Error in evaluating value #GREEN#x = {args[0]}%')
				return None, None
		else:
			self.__print('#RED#[ERROR]% there is no data points to build the interpolation function')
			return None, None

	def cmd_compute(self, *args):
		size = self.interpolator.size()
		if args:
			x, result = self.__inner_compute(args[0])
			if x and result:
				self.__print(f'#MAGENTA#ans =% #LIGHTBLUE#P{size - 1}(#GREEN#{x}%#LIGHTBLUE#) =% {result}')
		else:
			self.__print('#RED#[ERROR]% no value #GREEN#x% specified')

	def cmd_print_ans(self, *args):
		if 'ans' in dir(self):
			self.__print(f'#MAGENTA#ans =% {self.ans}')
		else:
			self.__print('#RED#[ERROR]% There is no value for #MAGENTA#ans% yet, you can get a value for #MAGENTA#ans% by #GREEN#compute%')

	def cmd_approx_ans(self, *args):
		size = self.interpolator.size()
		if args:
			x, result = self.__inner_compute(args[0])
			if x and result:
				self.__print(f'#MAGENTA#ans =% #LIGHTBLUE#P{size - 1}(#GREEN#{x}%#LIGHTBLUE#) =% {float(result):.5f}')
		else:
			if 'ans' in dir(self):
				self.__print(f'#MAGENTA#ans =% {float(self.ans):.5f}')
			else:
				self.__print('#RED#[ERROR]% There is no value for #MAGENTA#ans% yet, you can get a value for #MAGENTA#ans% by #GREEN#compute%')

	def cmd_set_config(self, *args):
		if len(args):
			try:
				kv = (''.join(args)).split('=')
				if len(kv) == 1:
					k = kv[0]
					v = None
				else:
					k, v = kv

				if k in self.config:
					if v != None:
						self.config[k][1] = self.config[k][0](v)
						self.__print(f'$#LIGHTBLUE#[*]% config #GREEN#{k}% updated to #MAGENTA#{self.config[k][1]}%')
					else:
						self.__print(f'#GREEN#{k} = #MAGENTA#{self.config[k][1]}%')
				else:
					self.__print(f'#RED#[ERROR]% key #GREEN#{k}% was not found in the configuration')
			except:
				self.__print('#RED#[ERROR]% wrong format for setting config values')
		else:
			self.__print('\n'.join([f'#GREEN#{k} = #MAGENTA#{repr(v[1])}%' for k, v in self.config.items()]))

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

		possible_commands = self.get_matched_commands(command)

		if len(possible_commands) == 1 or command in self.commands_map:
			command = possible_commands[0]

			start_t = -1
			if self.config['show-time'][1]:
				start_t = time()

			ret_val = self.commands_map[command][0](*args)

			# very weird to print the time it takes to exit haha
			if start_t != -1 and command != 'exit':
				end_t = time()
				self.__print(f'\n#LIGHTBLUE#[-] took $#GREEN#{(end_t - start_t) / 1000000:.5f}% #LIGHTBLUE#milliseconds%')

			return ret_val
		elif len(possible_commands) == 0:
			self.__print(f'#RED#[ERROR]% command #MAGENTA#{command}% could not be found')
		else:
			possible_commands_string = '\n\t'.join(possible_commands)
			self.__print(f'#YELLOW#[WARN]% do you mean\n\n\t{possible_commands_string}')

	def get_prompt(self):
		return self.config['prompt'][1] + ' '

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

	if readline:
		readline.parse_and_bind('tab: complete')
		readline.set_completer(cmd.command_completer)
		readline.set_completer_delims(' \t\n')

	while True:
		try:
			command = input(color_format(cmd.get_prompt())).strip()

			if not command:
				continue

			command = command.lstrip()

			if command[0] == '!':
				call_system_cmd(command[1:], shell=True)
				continue

			if cmd.run_command(command) == cmd.BREAK:
				break
			print()
		except EOFError:
			print()
			while True:
				response = input("Do you want to exit ([y]/n)? ").strip()
				if not response:
					exit(0)
				else:
					c = response[0].lower()
					if c == 'y':
						exit(0)
					elif c != 'n':
						continue
				break
		except KeyboardInterrupt:
			print()

if __name__ == '__main__':
	main()
