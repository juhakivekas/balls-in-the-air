# balls_in_the_air
# Tatu Leinonen
# 22.4.2015

# Temporary constants. May (should) be changed later to accomodate for command line inputs.
FPS = 60
BEATLENGTH = 40
RESOLUTION = (320, 240)
BOTTOM = (160, 180)
BOT1 = (140, 180)
BOT2 = (180, 180)
TOP = (160, 60)


import pygame.draw
import pygame.event
import pygame.time
import pygame.display

from path import *
from pattern import *

class DummyPattern:
	"""I'm a dumb pattern class that says you should always throw 3's."""
	def __init__(self):
		pass
	def next_throw(self):
		return 3

class Simulation:
	"""A simulation object, encapsulating the entirety of the graphical part of the program as well as following the instructions of a pattern object."""
	def __init__(self, pattern=None):
		self.fpsClock = pygame.time.Clock()
		self.t = 0

		if (pattern == None):
			self.pattern = DummyPattern()
		else:
			self.pattern = pattern
		self.parts = []

		pygame.display.init()
		self.disp = pygame.display.set_mode(RESOLUTION)
	
	def run(self):
		"""Run the simulation until 'update' tells us to stop. Currently, the only halting condition is the user pressing ESC."""
		run = True
		while(run):
			run = self.update()
		
	def update(self):
		"""Advance the simulation for a single frame. Compute the particles' new locations and draw them."""
		# The user can press ESC at any time to stop the simulation
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return False
		
		# pump() should be called once a frame to empty the event queue
		pygame.event.pump()

		# Particle creation
		if (self.t % BEATLENGTH == 0):
			next = self.pattern.next_throw()
			if (next > 0):
				self.parts.append(Particle(next*BEATLENGTH, QuadGPath(BOT1, BOT2, 0.04, next*BEATLENGTH)))
			# Particle removal
			self.parts = [p for p in self.parts if p.t < p.maxt]
			# NOTE: If needed, this part may be modified so that particles persist, i.e. particles don't get removed + added but are given a new trajectory instead.
			
		# Update the particles we have left
		for p in self.parts:
			p.update()
		
		self.draw()
		self.t = (self.t + 1) % BEATLENGTH
		self.fpsClock.tick(FPS)
		return True
		
	def draw(self):
		"""Draw everything to self.disp, i.e. the surface returned by setting up the display module."""
		self.disp.fill((0, 0, 0))
		for p in self.parts:
			p.draw(self.disp)
		pygame.display.flip()

class Particle:
	"""A particle that is thrown and follows a trajectory (a path). The current and total lifetimes are needed to find its current position on the path, and at the end it is removed. "Charge" represents whether it is an (anti)particle, though it's entirely possible this variable isn't needed."""
	def __init__(self, lifetime, path, charge=1):
		# These two variables that determine the particle's position on a parametrized path.
		self.t = 0
		self.maxt = lifetime
		
		self.path = path
		self.charge = charge
		
	def update(self):
		"""Advance a single frame."""
		self.t += 1
		
	def draw(self, surf):
		"""Draw some graphical representation of the particle in its current position, on the specified surface."""
		pygame.draw.circle(surf, (255,255,255), map(int, self.path.at(float(self.t)/self.maxt)), 10)