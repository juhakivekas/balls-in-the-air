from pattern import Pattern

#----test some known valid cases

p = Pattern([4,4,1])
if(p.is_valid() == False):
	print "test_fail, pattern [4,4,1] should be a valid siteswap"
if(p.particles != 3):
	print "test_fail, pattern [4,4,1] should have 3 balls"

p = Pattern([1,-1,0])
if(p.is_valid() == False):
	print "test_fail, pattern [1,-1,0] should be a valid siteswap"
if(p.particles != 0):
	print "test_fail, pattern [1,-1,0] should have 0 balls"
	
p = Pattern([2,3,3,-2,2,-2,1,1])
if(p.is_valid() == False):
	print "test_fail, pattern [2,3,3,-2,2,-2,1,1] should be a valid siteswap"
if(p.particles != 1):
	print "test_fail, pattern [2,3,3,-2,2,-2,1,1] should have 1 ball"

#----test some known invalid cases
#we try to construct the objects, and in case it fails and throws an error
# then we know everything went as expeced
construct_fail = False
try:
	p = Pattern([2,1,0])
except ValueError as e:
	construct_fail = True

if(construct_fail == False):
	print "test_fail, pattern [2,1,0] should is invalid and should not be possibel to construct"

construct_fail = False
try:
	p = Pattern([4,2,3,-1,-2])
except ValueError as e:
	construct_fail = True

if(construct_fail == False):
	print "test_fail, pattern [4,2,3,-1,-2] should is invalid and should not be possible to construct"

print "Pattern: all tests ran"
