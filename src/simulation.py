# balls_in_the_air
# Tatu Leinonen
# 22.4.2015

# Temporary constants. May (should) be changed later to accomodate for command line inputs.



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
		
		self.FPS = 60
		self.BEATLENGTH = 40
		self.RESOLUTION = (640, 480)
		self.TOP = self.RESOLUTION[1]/8
		self.BOT = 7*self.RESOLUTION[1]/8
		self.GRAVITY = 4.0*(self.BOT - self.TOP)/((self.buffer.height*self.BEATLENGTH)**2) # Gravity scaled such that max throws reach the top height
		self.LEFT = self.RESOLUTION[0]/4
		self.RIGHT = 3*self.RESOLUTION[0]/4
		self.LHAND = (self.LEFT, self.BOT)
		self.RHAND = (self.RIGHT, self.BOT)

		pygame.display.init()
		self.disp = pygame.display.set_mode(self.RESOLUTION)
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
		if (self.t % self.BEATLENGTH == 0):
			next = self.buffer.next_throw()
			# The following line no longer works. Need to figure out something else if random throws have to be debugged.
			# print self.buffer.throw_generator.state

			# Split particles into the ones in the air and the ones just caught
			hand = [p for p in self.parts if p.t >= p.maxt]
			self.parts = [p for p in self.parts if p.t < p.maxt]

			pos = [p for p in hand if p.charge > 0]
			neg = [p for p in hand if p.charge < 0]
			
			for n in next:
				if (n > 0):
					# If we have nothing in hand, create a new particle. This is necessary in the beginning, but should no longer occur once the buffer has been established
					if (len(pos) == 0):
						self.parts.append(Particle(n*self.BEATLENGTH, QuadGPath(self.LHAND, self.RHAND, self.GRAVITY, n*self.BEATLENGTH), 1))
					# Otherwise throw an existing particle. A new path is created to accommodate for hand alternation.
					else:
						part = pos.pop()
						path = QuadGPath(part.path.at(1), part.path.at(0), self.GRAVITY, n*self.BEATLENGTH)
						self.parts.append(Particle(n*self.BEATLENGTH, path, 1))
				# Repeat for negative particles!
				if (n < 0):
					if (len(neg) == 0):
						self.parts.append(Particle(-n*self.BEATLENGTH, QuadGPath(self.LHAND, self.RHAND, self.GRAVITY, -n*self.BEATLENGTH), -1))
					else:
						part = neg.pop()
						path = QuadGPath(part.path.at(1), part.path.at(0), self.GRAVITY, -n*self.BEATLENGTH)
						self.parts.append(Particle(-n*self.BEATLENGTH, path, -1))

		# Update the particles
		for p in self.parts:
			p.update()

		self.draw()
		self.t = (self.t + 1) % self.BEATLENGTH
		self.fpsClock.tick(self.FPS)
		return True

	def draw(self):
		"""Draw everything to self.disp, i.e. the surface returned by setting up the display module."""
		self.disp.fill((0, 0, 0))
		for p in self.parts:
			p.draw(self.disp)
		#self.disp.blit(surf, (0,0))
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
		circ = pygame.Surface((24, 24))
		circ.fill((0, 0, 0))
		if self.charge == 1:
			pygame.draw.circle(circ, (0, 0, 255), (circ.get_width()/2, circ.get_height()/2), 10)
		if self.charge == -1:
			pygame.draw.circle(circ, (255, 0, 0), (circ.get_width()/2, circ.get_height()/2), 10)
		coords = self.path.at(float(self.t)/self.maxt)
		coords = (coords[0] - circ.get_width()/2, coords[1] - circ.get_height()/2)
		surf.blit(circ, coords, special_flags=pygame.BLEND_ADD)