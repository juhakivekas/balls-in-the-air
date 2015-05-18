# balls_in_the_air
# Juha Kivekas
# 4.5.2015

#for making copies of objects in order to minimize side-effects
import copy
import random
from state import *

class RandomPattern:
	"""
	An object for handling random siteswaps. (virtual, non-periodic)
	aguments:
		number of (net) particles in pattern
		minimum throw height
		maximum throw height
		boolean for allowing virtual throws
		string for type of distribution (takes the first letter, so "unif", "uniform"... are valid inputs):
			"u" for uniform (default for compability)
			"g" for geometric
	"""

	def __init__(self, numballs, min_h, max_h, dist_type="u"):
		#allow virtual throws for states if min_height is negative
		virtual = (min_h <0)
		#the ground state of an n ball pattern is [0,1,...,n-1]
		self.state = State(range(0, numballs), virtual)
		self.min_height = min_h
		self.max_height = max_h
		#taking just the first letter allows different input values
		self.distribution_type = dist_type[0]
		# print min_h
		# print max_h
		if(max_h-min_h < numballs):
			raise ValueError('The difference in throw heights has to be larger than the number of balls ');

	def particle_count(self):
		"""calculates the number of net balls in the pattern"""
		slots = copy.copy(self.state.slot)
		while min(slots)<0:
			#every negative free slot will have to be filled with a positive one
			#therefore we can remove one positive and one negative slot at once
			#to remove one particle and anti-particle
			
			#cutting the list ends will do this since the list is ordered
			slots = slots[1:-1]
		return len(slots)

	def unif_next_throw(self):
		"""returns a random (allowed) throw from uniform distribution and manages the state accordingly"""
		#we can't let the lowest valued slot move too far to the past.
		#If we get a free slot in (min_height-1) we can never fill the slot
		#since it will move further away when time progresses.
		print self.state
		if self.state.is_valid_throw(self.min_height):
			next_throw =  self.min_height
			self.state.throw(next_throw);
			return next_throw;

		#the list of allowed throws
		allowed = []
		#check throws in the chosen range for validity
		for i in range(self.min_height, self.max_height+1):
			if self.state.is_valid_throw(i):
				allowed.append(i)

		if not allowed:
			#if the allowed list is empty, there is a problem.
			raise ValueError('The random pattern state got jammed!')

		#pick an integer that is an index for the valid throws list
		#XXX this is where the distribution can be made non-uniform!
		#print allowed
		index = random.randint(0,len(allowed)-1)
		
		next_throw = allowed[index]
		#manage the state accoring to the new throw
		self.state.throw(next_throw);
		#returns throw
		return next_throw;

	def geom_next_throw(self):
		"""returns a random (allowed) throw from geometric distribution and manages the state accordingly"""
		#we can't let the lowest valued slot move too far to the past.
		#If we get a free slot in (min_height-1) we can never fill the slot
		#since it will move further away when timwe progresses.
		if self.state.is_valid_throw(self.min_height):
			next_throw =  self.min_height
			self.state.throw(next_throw);
			return next_throw;

		#the list of allowed throws
		allowed = []
		#check throws in the chosen range for validity
		for i in range(self.min_height, self.max_height+1):
			if self.state.is_valid_throw(i):
				allowed.append(i)

		if not allowed:
			#if the allowed list is empty, there is a problem.
			raise ValueError('The random pattern state got jammed!')
		print allowed
		#dist will be created as normal geometric distribution
		dist = range(1, len(allowed) + 1)
		dist = map(lambda x: 0.5**x, dist)
		#sum of dist is then scaled to be 1 as for any probability vector
		dist = map(lambda x: x/sum(dist), dist)
		#rand is within 0 to 1
		rand = random.random()
		index = 0
		#from rand we look for the corresponding index
		#and condition is because machine epsilon
		while(rand > 0.0 and index < len(allowed)):
			rand -= dist[index]
			index += 1
		index -= 1
		next_throw = allowed[index]
		#manage the state accoring to the new throw
		self.state.throw(next_throw);
		#returns throw
		return next_throw;

	def next_throw(self):
		#fetches the next throw by type of random process
		#returns throw
		if(self.distribution_type == "u"):
			return self.unif_next_throw()
		else:
			return self.geom_next_throw()

	def __str__(self):
		"""prints the current state as a string"""
		string = ""
		#add the negative slots as -'s 
		for i in range(self.min_height,0):
			if self.state.slot.count(i) != 0:
				string += "-"
			else:
				string += "X"
		
		#add the zero-time marker
		string += "|"

		#add the positive slots as X's
		for i in range(0,self.max_height):
			if self.state.slot.count(i) != 0:
				string += "X"
			else:
				string += "-"

		return string
	
