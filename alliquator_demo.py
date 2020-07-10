# imports
import alliquator as aq

# press return
def press_return():
	"""Enter any input to advance."""
	
	# raw input
	k = raw_input('(press return)')
	print(' ')
	
	return None

def rse():
	"""raise System Exit."""
	
	raise SystemExit
	
	return None

# import
print('>>> import alliquator as aq\n')
press_return()

# verticle projectile motion
print('Consider the equation for vertical projectile motion, where h is the height, v is the initial velocity, t is the time, and g is the gravitational acceleration rate:\n')
print('   h = vt - 1/2gt^2\n')
press_return()
print('Use a string to initialize an Equation instance:\n')
press_return()
h = aq.Eq('h = v t - 1/2 g t2')
print(">>> h = aq.Eq('h = v t - 1/2 g t2')\n")
press_return()

# view the equation
print('View the equation:\n')
print('>>> h.view()\n')
press_return()
print('or, as a shortcut:\n')
print('>>> +h\n')
press_return()
h.view()
press_return()

# solve
print('Solve it for t to find the times at which the height is 0, assuming an initial velocity of 10 m/s and gravitational acceleration rate of 9.8 m/s^2:\n')
print(">>> p = h.solve('t',h=0,v=10,g=9.8)\n")
press_return()
p = h.solve('t',h=0,v=10,g=9.8)
print('The results are stored as a Page instance.\n')
press_return()
print('View the page:\n')
print(">>> +p")
press_return()
+p
press_return()

# Draw
print('Draw the solutions for height with respect to time from 0 to 2.1 seconds for the same parameters:\n')
print(">>> d = h.draw('h','t',0,2.1,v=10,g=9.8)\n")
press_return()
d = h.draw('h','t',0,2.1,v=10,g=9.8)
press_return()

# Projectile equations
print('Consider the equations for projectile motion in 2-dimensions, where d is the horizontal distance, h is the height, vi is the initial velocity, t is time, g is gravitational acceleration, and o is the launch angle:\n')
print('    d = vi t cos(o)')
print('    h = vi t sin(o) - 1/2 g t^2\n')
press_return()
print(">>> d = aq.Eq('d = vi t coso')")
print(">>> h = aq.Eq('h = vi t sino - 1/2 g t2')\n")
d = aq.Eq('d = vi t coso')
h = aq.Eq('h = vi t sino - 1/2 g t2')
press_return()

# derivatives
print('Take the derivatives with respect to time, where d and h are functions of time, and dt and ht represent d(d)/dt and d(h)/dt:\n')
press_return()
print(">>> dt = d.derive('t','d')")
print(">>> ht = h.derive('t','h')\n")
dt = d.derive('t','d')
ht = h.derive('t','h')
press_return()

# view shortcut
print('View the equations:\n')
press_return()
print(">>> +dt\n")
+dt
press_return()
print(">>> +ht\n")
+ht
press_return()

# Kinetic energy
print('Consider the equation for kinetic energy:\n')
print('    K = 1/2 m v^2\n')
press_return()
print(">>> k = aq.Eq('K = 1/2 m v2')\n")
k = aq.Eq('K = 1/2 m v2')
press_return()

# Substitution
print('The total velocity is related to the component velocities in the following way:\n')
print("    v^2 = vx^2 + vy^2\n")
press_return()
print('Substitute vx^2 + vy^2 for v^2:\n')
press_return()
print(">>> k = k.substitute('vx2 + vy2','v2')\n")
press_return()
print('or, as a shortcut:\n')
print(">>> k <<= ('vx2 + vy2','v2')\n")
k = k.substitute('vx2 + vy2','v2')
press_return()
print('view it.\n')
print(">>> +k\n")
+k
press_return()

# System
print('Put these equations into a System:\n')
press_return()
print(">>> s = aq.Sy(d,h,dt,ht,k)\n")
s = aq.Sy(d,h,dt,ht,k)
press_return()
print('View it:\n')
print(">>> +s\n")
press_return()
+s
press_return()

# substitute shortcuts
print('Substitute vx for d(d)/dt and vy for d(h)/dt:\n')
print(">>> s <<= ('vx','dt')")
print(">>> s <<= ('vy','ht')\n")
s <<= ('vx','dt')
s <<= ('vy','ht')
press_return()
print('View it:\n')
print(">>> +s\n")
press_return()
+s
press_return()

# elimination
print('Eliminate vx from the system using equation 2 and eliminate vy from the system using equation 3:\n')
print(">>> e = s.eliminate('vx',2)")
print(">>> e = e.eliminate('vy',3)\n")
e = s.eliminate('vx',2)
e = e.eliminate('vy',3)
press_return()
print(">>> +e\n")
press_return()
+e
press_return()
print('Eliminate t from the system using equation 0 and h using equation 1:\n')
print(">>> e = e.eliminate('t',0)")
print(">>> e = e.eliminate('h',1)")
print(">>> +e\n")
e = e.eliminate('t',0)
e = e.eliminate('h',1)
press_return()
+e
press_return()

# pick
print('Pick the last equation:\n')
press_return()
print(">>> p = e.pick(4)")
print(">>> +p\n")
press_return()
p = e.pick(4)
+p
press_return()

# draw
print('Draw a graph of kinetic energy with respect to distance from 0 to 10 m, assuming initial velocity of 10 m/s, a mass of 1 kg, and a launch angle of 1 radian:\n')
press_return()
print(">>> d = p.draw('K','d',0,10,vi=10,m=1,g=9.8,sino=aq.sin(1),coso=aq.cos(1))\n")
press_return()
d = p.draw('K','d',0,10,vi=10,m=1,g=9.8,sino=aq.sin(1),coso=aq.cos(1))
press_return()

# sculpt
print('Sculpt a 3D plot of kinetic energy with respect to launch angle from 0 to 1 radians and distance from 0 to 10 m:\n')
press_return()
print(">>> u = p.sculpt('K','o','d',0,0,1,10,vi=10,m=1,g=9.8,sino=lambda o: aq.sin(o),coso=lambda o: aq.cos(o))\n")
press_return()
u = p.sculpt('K','o','d',0,0,1,10,vi=10,m=1,g=9.8,sino=lambda o: aq.sin(o),coso=lambda o: aq.cos(o))
press_return()

# annilation
print('Alternatively, eliminate all the variables at once and create a Chain of resulting expressions:\n')
print(">>> a = s.annihilate(['vx','vy','t','h'],[2,3,0,1])")
print(">>> +a\n")
a = s.annihilate(['vx','vy','t','h'],[2,3,0,1])
press_return()
+a
press_return()

# draw
print('Draw graphs of kinetic energy and all other eliminated variables with respect to distance from 0 to 10 m, assuming initial velocity of 10 m/s, a mass of 1 kg, and a launch angle of 1 radian:\n')
press_return()
print(">>> c = a.draw('K','d',0,10,vi=10,m=1,g=9.8,sino=aq.sin(1),coso=aq.cos(1))\n")
press_return()
c = a.draw('K','d',0,10,vi=10,m=1,g=9.8,sino=aq.sin(1),coso=aq.cos(1))
press_return()

# sculpt
print('Sculpt a 3D plot of kinetic energy  and all other eliminated variables with respect to launch angle from 0 to 1 radians and distance from 0 to 10 m:\n')
press_return()
print(">>> u = a.sculpt('K','o','d',0,0,1,10,vi=10,m=1,g=9.8,sino=lambda o: aq.sin(o),coso=lambda o: aq.cos(o))\n")
press_return()
u = a.sculpt('K','o','d',0,0,1,10,vi=10,m=1,g=9.8,sino=lambda o: aq.sin(o),coso=lambda o: aq.cos(o))
press_return()

# end
print('Thank you for viewing this quick demo.  The Equation, System, and Chain classes have been introduced here.  They are built upon more elementary classes Term, Line, Expression, and Group.\n')
press_return()
print ('Also, the Page class has been introduced.  It is built upon the Result class.  Graphs are stored in a hierarchy of Pages in Books, Books on Shelves, and Shelves in Cases, all of which support further manipulation or storage as text flles for later retrieval.\n')
press_return()
print('There are many other useful methods.  Please refer to the class directories and help pages.\n')
press_return()
print('Thanks again!')
print('After a while, Calcudile...')







