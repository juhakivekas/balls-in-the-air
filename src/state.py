# balls_in_the_air
# Juha Kivekas
# 21.4.2015

class State:
	"""A class that keeps track of the juggling pattern state. Specifically virtual siteswaps."""

	def __init__(self, start=[]):
		"""Initialize a virtual siteswap state from a list"""
		#positive integers and zero indicate occupied landing times/slots for particles
		#negative integers indicate unoccupied landing times/slots in the past
		self.land = start;

	def is_valid_throw(self, t):
		"""Checks wether the throw t can be thrown without particle collisions"""
		if t>=0 and self.land.count(t) != 0:
			return False
		if t<0 and self.land.count(t) == 0:
			return False
		return True

	def throw(self, t):
		"""Do a throw of height 't' on the state"""		
		if t>=0:
			if self.land.count(t) != 0:
				#if there's a ball landing on time 't' already,
				#then we will have a collision of particles.
				print "Throwing ball to existing time slot!"
			#throw a ball
			self.land.append(t);

		elif t<0:
			if self.land.count(t) == 0:
				#if a ball has landed on time 't',
				#then we will have a collision of antiparticles in the past.
				print "Throwing ball to existing time slot!"
			#throw a ball
			self.land.remove(t)

		#keep the list sorted for clarity
		self.land.sort();

		if self.land.count(0) != 0:
			#if there was a ball to throw NOW, remove it.
			self.land.remove(0)
		else:
			#if there was no ball to throw NOW, cerate an antiparticle from the PRESENT.
			self.land.append(0)

		#progress in time by subtracting one from each state element
		self.land[:] = [a-1 for a in self.land]

	def debug(self):
		"""print the state as a string"""
		print self.land
