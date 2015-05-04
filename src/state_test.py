from state import State

#check that valid cases work right

#the siteswap [4,4,1] is valid
s = State([0,1,2]);
tmp = list(s.slot)
s.throw(4)
s.throw(4)
s.throw(1)
#for periodic siteswaps the final and initial state has to be the same
if(tmp != s.slot):
	print "State: test failed, [4,4,1] is periodic but seems not to be."

#[1,-1,0] is a valid siteswap
s = State([])
tmp = list(s.slot)
s.throw(1)
s.throw(-1)
s.throw(0)
if(tmp != s.slot):
	print "State: test failed, [1-1,0] is periodic but seems not to be."

print "State: all test ran"
