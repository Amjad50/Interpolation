import matplotlib.pyplot as plt

# TODO: make this standalone, or that a program can have more than one Plotter
class Plotter:
	def __init__(self, setup_callback=None):
		# start interactive mode
		plt.ion()	
		plt.cla()

		if callable(setup_callback):
			setup_callback(plt)
		
	def clear(self):
		plt.cla()
	
	def add(self, x_data, y_data):
		plt.plot(x_data, y_data)
		plt.pause(0.001)
