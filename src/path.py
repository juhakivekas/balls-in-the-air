# balls_in_the_air
# Tatu Leinonen
# 23.4.2015
# A helper module for parametrized ball trajectories, etc. for use in the juggling simulation.

class Path:
	"""A base class for parametrized paths, with t in the interval from 0 to 1. Currently, only calling the contained function is supported, but cases could be made for e.g. composing paths as well."""
	def __init__(self):
		self.fct = lambda t: t
	def at(self, t):
		"""Return the position on the path at time t. The parameter should be between 0 and 1 (inclusive), but the function may work with other values as well. It is not guaranteed, though, and there should be no need for those."""
		return self.fct(t)

class LinPath(Path):
	"""A linear path between two points."""
	def __init__(self, start, end):
		# Error checking needed
		Path.__init__(self)
		self.fct = lambda t: (start[0] + (end[0] - start[0])*t, start[1] + (end[1] - start[1])*t)

class QuadGPath(Path):
	"""A quadratic path between two points, obeying the specified gravity given in dSpeed/frame. The lifetime of a particle is needed to normalize the timing."""
	def __init__(self, start, end, gravity, lifetime):
		# Error checking needed
		Path.__init__(self)
		# Find a v_y (vertical velocity component) such that at t = 1:
		# y_0 + v_y*(t*lifetime) + g*(t*lifetime)^2 = y_1
		# i.e. v_y = (y_1 - y_0)/(lifetime) - g*lifetime
		# Note that frames are our only reliable way to normalize time and the path is computed accordingly.
		# Gravity should be speed increase in pixels/frame.
		v = float(end[1] - start[1])/lifetime - gravity*lifetime
		self.fct = lambda t: (start[0] + (end[0] - start[0])*t, start[1] + v*t*lifetime + gravity*(t*lifetime)**2)
