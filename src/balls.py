import sys
from pattern import *
from random_pattern import *
from buffer import *
from state import *
 
#commandline arguments should give at least least height
#the order for arguments is maximum height, flags, pattern
#if pattern is not given, but flags tell that there should be, it will throw constant pattern
#if only height given, it will throw random with normal balls
#pattern given in format: 3/-2/1
#if pattern is given with random flag, it will use the pattern as starting state
#TODO init simulation

def main(argv):
	number_of_arguments = len(sys.argv)
	if(number_of_arguments == 1):
		print "Error in giving arguments."
		print "You need to give at least maximum height."
	elif(number_of_arguments == 2):
		h = int(sys.argv[1])
		i = 0
		stat = []
		while(i<h):
			stat.append(i)
			i += 1
		pat = RandomPattern(State(stat))
		buf = Buffer(h, "rn", pat)
	elif(number_of_arguments == 3):
		h = int(sys.argv[1])
		flags = sys.argv[2]
		if(flags[0] == 'r'):
			if(flags[0] == 'a'):
				i = 0
				stat = []
				while(i<h):
					stat.append(i)
					i += 1
				pat = RandomPattern(State(stat))
				buf = Buffer(h, "ra", pat)
			elif(flags[0] == 'n'):
				i = 0
				stat = []
				while(i<h):
					stat.append(i)
					i += 1
				pat = RandomPattern(State(stat))
				buf = Buffer(h, "rn", pat)
			else:
				print "Error in giving arguments."
				print "You have given invalid flags."
		elif(flags[0] == 'p'):
			if(flags[0] == 'a'):
				i = 0
				stat = []
				while(i<h):
					stat.append(h)
					i += 1
				pat = Pattern(stat)
				buf = Buffer(h, "pa", pat)
			elif(flags[0] == 'n'):
				i = 0
				stat = []
				while(i<h):
					stat.append(h)
					i += 1
				pat = Pattern(stat)
				buf = Buffer(h, "pa", pat)
			else:
				print "Error in giving arguments."
				print "You have given invalid second flag."
		else:
			print "Error in giving arguments."
			print "You have given invalid first flag."
	elif(number_of_arguments == 4):
		h = int(sys.argv[1])
		flags = sys.argv[2]
		pattern = map(int,sys.argv[3].split('/'))
		if(flags[0] == 'r'):
			if(flags[0] == 'a'):
				if(not any(n < 0 for n in pattern)):
					pat = RandomPattern(State(pattern))
					buf = Buffer(h, "ra", pat)
				else:
					print "Invalid state given. Has minuses in it"
			elif(flags[0] == 'n'):
				if(not any(n < 0 for n in pattern)):
					pat = RandomPattern(State(pattern))
					buf = Buffer(h, "rn", pat)
				else:
					print "Invalid state given. Has minuses in it"
			else:
				print "Error in giving arguments."
				print "You have given invalid flags."
		elif(flags[0] == 'p'):
			if(flags[0] == 'a'):
				pat = Pattern(pattern)
				buf = Buffer(h, "pa", pat)
			elif(flags[0] == 'n'):
				pat = Pattern(pattern)
				buf = Buffer(h, "pn", pat)
			else:
				print "Error in giving arguments."
				print "You have given invalid flags."
	else:
		print "Error in giving arguments."
		print "You have given too many arguments."


if __name__ == "__main__":
   main(sys.argv[1:])
