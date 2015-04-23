Your mission is to write Python code for a rudimentary juggling simulator that implements random patterns (random walks on state graphs) and virtual patterns (matter / antimatter as in the blog video), and shows some particles moving on the screen.

A minimal spec: The user gives the number of particles and maximum throw height, and the simulator
 - starts from the ground state
 - chooses the next throw uniformly randomly
 - advances to the next state
and so on, while showing the graphics. It stops when the user tells it to stop.

Some extensions:
- non-uniform randomness
- keep track of the visiting frequencies of the states
- allow max throw to be infinite
- allow the number of particles to change during the process.

The aim is to write clear code that is easy to extend (on the course next year, say) and that I can understand. Keep it simple. For example, first do the graphics part with one hand and with linear gravity.
