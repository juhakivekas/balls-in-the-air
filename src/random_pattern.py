# balls_in_the_air
# Juha Kivekas
# 4.5.2015

#for making copies of objects in order to minimize side-effects
import copy
from state import State

class RandomPattern:
	"An object for handling random siteswaps. (virtual, non-periodic)"

	def __init__(self, org_state=State([])):
		#copy the argument state
		self.state = copy.copy(org_state);

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
		#TODO check for valid throws, and choose one at random
		#it's funny how the most important feature in not yet implemented :D
		return 0
