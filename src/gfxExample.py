# balls_in_the_air
# Tatu Leinonen
# 22.4.2015

# NOTE: Install PyGame from http://pygame.org/ and make sure it imports correctly.

# fetch some needed modules
import pygame.draw
import pygame.event
import pygame.time
import pygame.display
from math import sin, cos, pi

# initialize our program to run at 60fps and in a small window
fps = pygame.time.Clock()
pygame.display.init()
disp = pygame.display.set_mode((320,240))


t = 0
# a quick and dirty main loop
while(True):
	# check whether user wants to quit
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
	
	# this represents simulating things
	# for now, it's just an increasing timer
	t += 1
	
	# after that, draw everything
	disp.fill((0, 0, 0))
	pygame.draw.circle(disp, (255,255,255), (160 + int(20*cos(2*pi*t/60)), 120 - int(20*sin(2*pi*t/60))), 10)
	pygame.display.flip()
	# finally, make sure our timing's correct
	fps.tick(60)
