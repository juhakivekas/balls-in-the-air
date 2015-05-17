from simulation import *
from pattern import *
from random_pattern import *
from state import *

import argparse

"""

--b is the number of balls
--r for random pattern
--dist \"g\" means that geometric distribution is going to be used, other
values are ignored and default value for the distribution is used
--min minimum throw height (if it is < 0 then virtual throws are allowed)
--max maxmimum throw height
--p user specified pattern

examples:

python2 main.py --p 1 2 3 4 5
starts simulation with user specified pattern

python2 main.py --r --max 8 --min -2 --b 3 --dist "g"
starts random pattern simulation with 3 balls, maximum throw height of 8,
minimum throw height of -2 and using geometric distribution

"""


parser = argparse.ArgumentParser(description="Juggling simulator")
parser.add_argument('--b', action="store", dest="num_balls", type=int)
parser.add_argument('--r', action="store_true", dest="enable_random")
parser.add_argument('--dist', action="store", dest="distribution")
parser.add_argument('--min', action="store", dest="min_throw", type=int)
parser.add_argument('--max', action="store", dest="max_throw", type=int)
parser.add_argument('--p', action="store", nargs="+", dest="pattern", type=int)
parser.set_defaults(enable_random=False)
args = parser.parse_args()

print(args.enable_random)

if args.enable_random:
    dist = "u"
    if args.distribution == "g":
        dist = "g"
    elif args.distribution != "None":
        print("Invalid distribution type!")
        print("Using default value (uniform) for the distribution!")

    random_pattern = RandomPattern(args.num_balls, args.min_throw, args.max_throw, dist_type=dist)
    buffer = Buffer(random_pattern)
    simulation = Simulation(buffer)
    simulation.run()
else:
    s = Pattern(args.pattern)
    buffer = Buffer(s)
    simulation = Simulation(buffer)
    simulation.run()
