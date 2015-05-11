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
	"""

	def __init__(self, numballs, min_h, max_h):
		#allow virtual throws for states if min_height is negative
		virtual = (min_h <0)
		#the ground state of an n ball pattern is [0,1,...,n-1]
		self.state = State(range(0, numballs), virtual)
		self.min_height = min_h
		self.max_height = max_h
		print min_h
		print max_h
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

	def next_throw(self):
		"""returns a random (allowed) throw and manages the state accordingly"""
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

		#pick an integer that is an index for the valid throws list
		#XXX this is where the distribution can be made non-uniform!
		print allowed
		index = random.randint(0,len(allowed)-1)

		next_throw = allowed[index]
		#manage the state accoring to the new throw
		self.state.throw(next_throw);
		return next_throw;
