# balls_in_the_air
# Juha Kivekas
# 4.5.2015

from random_pattern import RandomPattern
from state import State

r = RandomPattern(State([0,1,2]))
if r.particle_count() != 3:
	print "test fail"
