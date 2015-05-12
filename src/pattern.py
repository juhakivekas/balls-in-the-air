# balls_in_the_air
# Juha Kivekas
# 27.4.2015

class Pattern:
	"""This is a class for handling periodic siteswaps. (virtual, periodic)"""

	def __init__(self, throws=[]):
		"""initialize an object given the siteswap as a list"""
		#TODO check that the elements are integers
		self.siteswap = list(throws)
		if (self.is_valid() == False):
			raise ValueError('The given siteswap is not valid')
		self.particles = self.particle_count()
		self.time = 0

	def is_valid(self):
		"""checks whether the siteswap is a valid one"""
		siteswap_copy = list(self.siteswap)
		length = len(siteswap_copy)
		
		#create the set {(a_i + i) mod n : i in {0,1,...,n}}
		for i in range(0, length):
			siteswap_copy[i] += i;
			siteswap_copy[i] %= length;
	
		#check that the created set is the set{0,1,...,n}
		siteswap_copy.sort()
		for i in range(0, length):
			if siteswap_copy[i] != i:
				#some number is double, so this is not a valid siteswap
				return False

		#everything seems to be ok!
		return True

	def particle_count(self):
		"""calculates the number of particles in a siteswap, given a valid siteswap""" 
		#given a valis siteswap, this is the number of NET balls
		return sum(self.siteswap) / len(self.siteswap)

	def next_throw(self):
		"""returns the next throw in this siteswap"""
		ret = self.siteswap[self.time]
		self.time += 1;
		self.time %= len(self.siteswap)
		return ret
