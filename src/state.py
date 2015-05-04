# balls_in_the_air
# Juha Kivekas
# 21.4.2015

class State:
	"""A class that keeps track of the juggling pattern state. Specifically virtual siteswap states."""

	def __init__(self, start=[]):
		"""Initialize a virtual siteswap state from a list"""
		#XXX is timeslot a good word for a "cross" in the state?
		#positive integers and zero indicate occupied sloting times/slots for particles
		#negative integers indicate unoccupied sloting times/slots in the past
		self.slot = list(start)

	def __str__(self):
		"""print the state as a string"""
		return self.slot.__str__()

	def is_valid_throw(self, t):
		"""Checks wether the throw t can be thrown without particle collisions"""
		if t>=0 and self.slot.count(t) != 0:
			return False
		if t<0 and self.slot.count(t) == 0:
			return False
		return True

	def throw(self, t):
		"""Do a throw of height 't' on the state"""		
		if t>=0:
			if self.slot.count(t) != 0:
				#if there's a ball landing on time 't' already,
				#then we will have a collision of particles.
				raise ValueError('Throwing ball to occupied time slot!')
			#throw a ball
			self.slot.append(t)

		elif t<0:
			if self.slot.count(t) == 0:
				#if a ball has landed on time 't',
				#then we will have a collision of antiparticles in the past.
				raise ValueError('Throwing ball to occupied time slot!')
			#throw a ball
			self.slot.remove(t)

		#keep the list sorted for clarity
		self.slot.sort()

		if self.slot.count(0) != 0:
			#if there was a ball to throw NOW, remove it.
			self.slot.remove(0)
		else:
			#if there was no ball to throw NOW, cerate an antiparticle from the PRESENT.
			self.slot.append(0)

		#progress in time by subtracting one from each state element
		#shorter syntax -> self.slot[:] = [a-1 for a in self.slot]
		for i in range(0, len(self.slot)):
			self.slot[i] -= 1
			

