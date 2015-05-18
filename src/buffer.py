from pattern import *
from random_pattern import *
class Buffer:
	"""This class buffers the throws."""
	#generator: Pattern or RandomPattern
	def __init__(self, generator):
		self.throw_generator = generator
		self.throws = []
		self.height = 1
		
		# Determines the required buffer size depending on whether Pattern or RandomPattern is used
		if (isinstance(generator, Pattern)):
			for i in xrange(0, max(0, -min(generator.siteswap))+1):
				self.throws.append([])
				self.height = max(max(generator.siteswap), -min(generator.siteswap))
		if (isinstance(generator, RandomPattern)):
			for i in xrange(0, max(0, -(generator.min_height))+1):
				self.throws.append([])
				self.height = max(generator.max_height, -(generator.min_height))
				
		# Initialize the buffer with the first throws
		for i in xrange(0, len(self.throws)):
			throw = self.throw_generator.next_throw()
			if (throw > 0):
				self.throws[i].append(throw)
			# Negative indices refer to the n:th last entry in a list (e.g. -1 is the last)
			# When i+throw is negative, it refers to a virtual particle being thrown *BEFORE* the pattern starts properly so those have to be excluded.
			if (throw < 0 and i+throw >= 0):
				self.throws[i + throw].append(throw)

	def next_throw(self):
		# Take the first throw in the buffer, later return it
		throw = self.throws.pop(0)
		
		# Repopulate the queue according to the throw generator
		self.throws.append([])
		next = self.throw_generator.next_throw()
		if (next > 0):
			self.throws[-1].append(next)
		if (next < 0):
			self.throws[next-1].append(next)
		return throw
		
	def nth_throw(self, n):
		return (self.throws[n])
