from pattern import *
from random_pattern import *
class Buffer:
	"""This class buffers the throws."""
	#h: max height
	#flags: ["r" if random or else "p" if pattern] and ["n" if only normal balls or else "a" if antiballs too]
	#generator: Pattern or RandomPattern
	def __init__(self, generator):
		self.throw_generator = generator
		self.throws = []
		
		#self.random = False
		#self.anti = False
		# if(flags[0] == 'r'):
			# self.random = True
		# if(flags[1] == 'a'):
			# self.anti = True

		if (isinstance(generator, Pattern)):
			for i in xrange(0, -min(generator.siteswap)+1):
				self.throws.append([])
		if (isinstance(generator, RandomPattern)):
			for i in xrange(0, -(generator.min_height)+1):
				self.throws.append([])
		
		for i in xrange(0, len(self.throws)):
			throw = self.throw_generator.next_throw()
			if (throw > 0):
				self.throws[i].append(throw)
			if (throw < 0):
				self.throws[i + throw].append(throw)
			


	# def fetch_throw(self):
		# throw = self.throw_generator.next_throw()
		# self.throws.append([])
		# if(throw > 0):
			# self.throws[-1].append
		# if(throw < 0):
			# print -1+throw
			# self.throws[-1+throw].append

	def next_throw(self):
		throw = self.throws.pop(0)
		self.throws.append([])
		next = self.throw_generator.next_throw()
		if (next > 0):
			self.throws[-1].append(next)
		if (next < 0):
			self.throws[-1 + next].append(next)
		return throw
		
	def nth_throw(self, n):
		return (self.ballBuffer[n], self.antiBuffer[n])
