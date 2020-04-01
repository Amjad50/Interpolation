import sys

# BLACK, BLUE, RED, GREEN, YELLOW, LIGHTBLUE, MAGENTA, WHITE = (0, 21, 9, 10, 11, 14, 13, 15)

import re

colors = {
	'BLACK': 0,
	'RED': 9,
	'BLUE': 21,
	'GREEN': 10,
	'YELLOW': 11,
	'MAGENTA': 13,
	'LIGHTBLUE': 14,
	'WHITE': 15,
}

BOLD = '\x1b[1m'

RESET = '\x1b[0m'

def foreground(color):
	return f'\x1b[38;5;{color}m'

def background(color):
	return f'\x1b[48;5;{color}m'


def __replace_handler(c):
	c = c.group(0)
	start = c[0]
	if start in ('#', '@'):
		c = c[1:-1]
		if c in colors:
			return foreground(colors[c]) if start == '#' else background(colors[c])
		else:
			return RESET
	if c[0] == '$':
		return BOLD

	return RESET

def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)

    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty

def __format(s, is_color = True):
	handler = __replace_handler if is_color and supports_color() else ''

	return re.sub(r'((?<!\\)[@#][A-Z]+[@#])|\$|\%', handler, s)

"""
@COLOR@		background
#COLOR#		foreground
$			bold
%			reset

example:
@YELLOW@#RED#[$#BLUE#*%@YELLOW@#RED#]% added (1, 2)
"""
def color_print(*args, **kwargs):
	is_color = (not 'color' in kwargs or kwargs['color'])
	if 'color' in kwargs:
		del kwargs['color']

	print(*[__format(i, is_color) for i in args], **kwargs)
