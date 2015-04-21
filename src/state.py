# balls_in_the_air
# Juha Kivekäs
# 21.4.2015

class State:
	"""A class that keeps track of the juggling pattern state"""

	def __init__(self, start=[]):
		"""initialize a state from a list"""
		#positive integers and zero indicate landing times/slots for particles
		#negative integers indicate an unlanded slot in the past
		self.land = start;

	def throw(self, t):
		"""Do a throw of height 't' on the state"""
		if self.land.count(0) != 0:
			#if there is a ball to throw NOW, remove it.
			self.land.remove(0)
		else:
			#if there is no ball to throw NOW, cerate an antiparticle from the PRESENT.
			self.land.append(0)
		
		if t>0:
			if self.land.count(t) != 0:
				#if there's a ball landing on time 't' already,
				#then we will have a collision of particles.
				print "Throwing ball to existing time slot!"
	
			#throw a ball
			self.land.append(t);
		if t<0:
			if self.land.count(t) == 0:
				#if a ball has landed on time 't',
				#then we will have a collision of antiparticles in the past.
				print "Throwing ball to existing time slot!"
			self.land.remove(t)

		#keep the list sorted for clarity
		self.land.sort();
		#progress in time by subtracting one from each state element
		self.land[:] = [a-1 for a in self.land]

	def debug(self):
		"""print the state as a string"""
		print self.land
