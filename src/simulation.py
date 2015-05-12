# balls_in_the_air
# Tatu Leinonen
# 22.4.2015

# Temporary constants. May (should) be changed later to accomodate for command line inputs.
FPS = 60
BEATLENGTH = 40
RESOLUTION = (640, 480)
GRAVITY = 0.03
BOTTOM = (320, 360)
BOT1 = (280, 360)
BOT2 = (360, 360)
TOP = (320, 60)


import pygame.draw
import pygame.event
import pygame.time
import pygame.display
import sys
import signal

from path import *
from buffer import *

def exit_handler(signal, frame):
    sys.exit(0)

class DummyBuffer:
	"""I'm a dumb buffer class that says you should always throw 3's."""
	def __init__(self):
		pass
	def next_throw(self):
		return (3)

class Simulation:
	"""A simulation object, encapsulating the entirety of the graphical part of the program as well as following the instructions of a buffer object."""
	def __init__(self, buffer=None):
		self.fpsClock = pygame.time.Clock()
		self.t = 0

		if (buffer == None):
			self.buffer = DummyBuffer()
		else:
			self.buffer = buffer
		self.parts = []

		pygame.display.init()
		self.disp = pygame.display.set_mode(RESOLUTION)
        signal.signal(signal.SIGINT, exit_handler)

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

		# Things that occur once every beat
		if (self.t % BEATLENGTH == 0):
			next = self.buffer.next_throw()
			# The following line no longer works. Have to figure out something.
			# print self.buffer.throw_generator.state

			# Split particles into the ones in the air and the ones just caught
			hand = [p for p in self.parts if p.t >= p.maxt]
			self.parts = [p for p in self.parts if p.t < p.maxt]

			for n in next:
				if (n > 0):
					# If we have nothing in hand, create a new particle. This is necessary in the beginning, but should no longer occur once the buffer has been established
					if (len(hand) == 0):
						self.parts.append(Particle(n*BEATLENGTH, QuadGPath(BOT1, BOT2, GRAVITY, n*BEATLENGTH)))
					# Otherwise throw an existing particle. A new path is created to accommodate for hand alternation.
					else:
						part = hand.pop()
						path = QuadGPath(part.path.at(1), part.path.at(0), GRAVITY, n*BEATLENGTH)
						self.parts.append(Particle(n*BEATLENGTH, path))

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
		# These two variables determine the particle's position on a parametrized path.
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
