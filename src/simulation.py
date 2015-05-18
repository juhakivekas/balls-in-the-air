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
from math import sin, cos, pi

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
		self.HANDS = ((self.LEFT, self.BOT), (self.RIGHT, self.BOT))

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
			beatparity = (self.t/self.BEATLENGTH) % 2
			next = self.buffer.next_throw()
			# Remove the landed particles
			self.parts = [p for p in self.parts if p.t < p.maxt]
			
			print self.buffer.throw_generator
			
			# Iterate through the sequence of given throws. On even beats throw from left hand, on odd beats throw from right one. On even throws throw to the same hand, on odd throws throw to the other one.
			for n in next:
				if (n != 0):
					self.parts.append(Particle(abs(n)*self.BEATLENGTH, QuadGPath(self.HANDS[beatparity % 2], self.HANDS[(n + beatparity) % 2], self.GRAVITY, abs(n)*self.BEATLENGTH), n/abs(n)))

		# Update the particles
		for p in self.parts:
			p.update()

		self.draw()
		self.t = (self.t + 1) % (2*self.BEATLENGTH)
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
		
		rot = self.path.at(float(self.t)/self.maxt)[0]/(2*5*pi)
		pts = map(lambda x: (circ.get_width()/2 + 10*cos(rot + 2*pi*x/24), circ.get_height()/2 + 10*sin(rot + 2*pi*x/24)), range(0, 24))
		
		if (self.charge > 0):
			col1 = (0, 0, 255)
			col2 = (0, 0, 160)
			
		if (self.charge < 0):
			col1 = (255, 0, 0)
			col2 = (160, 0, 0)

		pygame.draw.polygon(circ, col1, [(circ.get_width()/2, circ.get_height()/2)] + pts[0:7])
		pygame.draw.polygon(circ, col2, [(circ.get_width()/2, circ.get_height()/2)] + pts[6:13])
		pygame.draw.polygon(circ, col1, [(circ.get_width()/2, circ.get_height()/2)] + pts[12:19])
		pygame.draw.polygon(circ, col2, [(circ.get_width()/2, circ.get_height()/2)] + pts[18:25] + [pts[0]])

		# pygame.draw.circle(circ, col1, (circ.get_width()/2, circ.get_height()/2), 10)
		
		coords = self.path.at(float(self.t)/self.maxt)
		coords = (coords[0] - circ.get_width()/2, coords[1] - circ.get_height()/2)
		surf.blit(circ, coords, special_flags=pygame.BLEND_ADD)
