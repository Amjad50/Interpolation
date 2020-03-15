from graph import Plotter
import numpy as np


# For testing only
x = np.arange(0, 20, 0.01)
y = np.sin(x)
yy = np.cos(x)

p = Plotter()

p.add(x, y)
input()
p.add(x, yy)
