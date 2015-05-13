from pattern import *
from random_pattern import *
class Buffer:
	"""This class buffers the throws."""
	#generator: Pattern or RandomPattern
	def __init__(self, generator):
		self.throw_generator = generator
		self.throws = []
		#creates the empty buffer from Rattern or RandomPattern
		if (isinstance(generator, Pattern)):
			for i in xrange(0, -min(generator.siteswap)+1):
				self.throws.append([])
		if (isinstance(generator, RandomPattern)):
			for i in xrange(0, -(generator.min_height)+1):
				self.throws.append([])
		#fills the buffer with throws
		for i in xrange(0, len(self.throws)):
			throw = self.throw_generator.next_throw()
			#determines if the throw is normal (>0) or virtual(<0)
			if (throw > 0):
				self.throws[i].append(throw)
			if (throw < 0):
				self.throws[i + throw].append(throw)

	def next_throw(self):
		#returns the first throw from the buffer
		#puts new throw into the "queue"
		throw = self.throws.pop(0)
		self.throws.append([])
		next = self.throw_generator.next_throw()
		#determines if the throw is normal (>0) or virtual(<0)
		if (next > 0):
			self.throws[-1].append(next)
		if (next < 0):
			self.throws[-1 + next].append(next)
		return throw
		
	def nth_throw(self, n):
		return (self.throws[n])
