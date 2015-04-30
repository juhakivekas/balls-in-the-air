from simulation import *
from pattern import *
from state import *

#----CURRENT WORKING CONDITION
#create a cyclic pattern
p = Pattern([4,2,3]); 
sim = Simulation(p);
sim.run()

#----goal for week2
"""
#start from the three ball ground state
s = State([0,1,2])
#create a random pattern starting from the state 's'
r = RandomPattern(s)
sim = Simulation(r);
"""

#---goal for week2/3?
"""
#start from the three ball ground state
s = State([0,1,2])
#create a random pattern starting from the state 's'
r = RandomPattern(s)
#create a buffer for the random pattern
b = Buffer(r)
sim = Simulation(r);
"""
