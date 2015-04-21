from state import State

#these tests are just me trying out the program intuitively, not real unit tests

s = State([0,1]);
s.debug()
s.throw(3)
s.debug()
s.throw(1)
s.debug()

s = State([0]);
s.debug()
s.throw(2)
s.debug()
s.throw(2)
s.debug()
s.throw(-1)
s.debug()
