# balls_in_the_air
# Juha Kivekas
# 21.4.2015

class State:
	"""A class that keeps track of the juggling pattern state. Specifically virtual siteswap states."""

	def __init__(self, start=[], virtual=False):
		"""Initialize a virtual siteswap state from a list"""
		#positive integers and zero indicate occupied sloting times/slots for particles
		#negative integers indicate unoccupied sloting times/slots in the past
		self.slot = list(start)

		#this is a boolean allowing virtual throws
		self.virtual = virtual

	def __str__(self):
		"""print the state as a string"""
		return self.slot.__str__()
	
#	def __str__(self):
#		"""print the state as a string"""
#		string = ""
#		#add the negative slots as -'s 
#		for i in range(-5,0):
#			if self.slot.count(i) != 0:
#				string += "-"
#			else:
#				string += "X"
#		
#		#add the zero-time marker
#		string += "|"
#
#		#add the positive slots as X's
#		for i in range(0,6):
#			if self.slot.count(i) != 0:
#				string += "X"
#			else:
#				string += "-"
#		
#		return string
			

	def is_valid_throw(self, t):
		"""Checks whether the throw t can be thrown without particle collisions"""
		#if we don't allow virtual throws, ONLY zeros can be thrown when
		#the state doesn't contain a particle in the zero slot
		if not self.virtual and self.slot.count(0) == 0:
			if t==0:
				return True
			else:
				return False

		#we can throw to any unoccupied slot.
		#positive slots are unoccupied if they ARE NOT in the 'slot' list
		if t>=0 and self.slot.count(t) != 0:
			return False
		#negative slots are unoccupied if they ARE in the 'slot' list
		if t<0 and self.slot.count(t) == 0:
			return False
		return True

	def throw(self, t):
		"""Do a throw of height 't' on the state"""
		#validity of the throw is not checked, but exceptions are thrown
		#when erraneous things happen.
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
