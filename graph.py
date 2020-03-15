import matplotlib.pyplot as plt
import matplotlib

# TODO: make this standalone, or that a program can have more than one Plotter
class Plotter:
	def __init__(self, setup_callback=None):
		matplotlib.use('GTK3Agg')
		# start interactive mode
		# FIXME: allow interactivity with pause
		plt.ion()	
		plt.cla()

		if callable(setup_callback):
			setup_callback(plt)
		
	def clear(self):
		plt.cla()

	def show(self):
		plt.show()
	
	def add_line(self, x_data, y_data):
		plt.plot(x_data, y_data)
		plt.pause(0.001)
	
	def add_points(self, x_data, y_data):
		plt.plot(x_data, y_data, 'o')
		plt.pause(0.001)
