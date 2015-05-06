from pattern import *
from random_pattern import *
class Buffer:
	"""This class buffers the throws."""
	#h: max height
	#flags: ["r" if random or else "p" if pattern] and ["n" if only normal balls or else "a" if antiballs too]
	#p: Pattern or RandomPattern
	def __init__(self, h, flags, p):
		self.ballBuffer = []
		self.antiBuffer = []
		self.h = h
		self.random = false
		self.anti = false
		self.throw_generator = p
		if(flags[0] == 'r'):
			self.random = true
		if(flags[1] == 'a'):
			self.anti = true
		i = 0
		while(i < h):
			self.fetch_throw()
			i += 1

	def fetch_throw(self):
		throw = throw_generator.next_throw()
		if(throw >= 0):
			self.ballBuffer.append(throw)
			self.antiBuffer.append(0)
		else:
			self.ballBuffer.append(0)
			self.antiBuffer.append(throw)

	def next_throw(self):
		throw = (self.ballBuffer[0], self.antiBuffer[0])
		del self.ballBuffer[0]
		del self.antiBuffer[0]
		self.fetch_throw()
		return throw

	def nth_throw(self, n):
		return (self.ballBuffer[n], self.antiBuffer[n])
