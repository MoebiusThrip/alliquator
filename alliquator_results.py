# alliquator_results.py
# manipulation of calculation results
 
# import math
import math
atan = math.atan2
cos = math.cos
sin = math.sin
sqrt = math.sqrt
 
# import plotting
import matplotlib.pyplot as plt
 
# import time
import time as time

# timing decorator
def time_process(f,n=1000,r=10,u=False):
	"""Time a process.
	
	Arguments:
		f: function object
		n=1000: integer, number of repeats to average over
		r=10: integer, number of rounds to perform
		u=True: boolean, measure in microseconds?
		
	Returns:
		function object
	"""
	
	# fewer iterations for longer process
	if not u:
		n = 10
	
	def timer(*a,**k):
		
		# perform r rounds, collect data
		d = []
		for i in range(r):
		
			# start time
			s = time.time()
			
			# perform function n times
			for j in range(n):
				x = f(*a,**k)
			
			# end time
			e = time.time()
		
			# calculate
			t = float(e - s) / float(n)
			d.append(t)
		
		# print min and max in microseconds
		if u:
			d = [i * 1000000 for i in d]
			print('min: %f usec' % (min(d)))
			print('max: %f usec\n' % (max(d)))
			
		# or milliseconds
		else:
			d = [i * 1000 for i in d]
			print('min: %f msec' % (min(d)))
			print('max: %f msec' % (max(d)))
		
		# spacer
		print(' ')
		
		return x
		
	return timer
 
# Result class
class Result (complex):
	"""A Result instance is a complex number calculated by evaluating an algebraic Term.  
	
	Result class inherits from complex.
	
	class Attributes:
		permutations: list of permutations
		tolerance: floating point error tolerance
	"""
	
	permutations = [[],[(0,)]]
	permutations.append([(0,1),(1,0)])
	permutations.append([(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)])
	tolerance = 1e-16
	
	def __init__(self,r,i=0):
		"""Define a Result instance as a complex number.
		
		Arguments:
			r: number, real part
			i=0: number, imaginary part
			
		Returns:
			Result instance
			
		Attributes:
			real: float, real part
			imag: float, imaginary part
		"""
		
		# no additional attributes assigned
		pass
		
		
	# instance methods
	def __add__(self,r):
		"""Use the + shortcut for addition.
		
		Arguments:
			r: Result instance
			
		Returns:
			Result instance
		"""
		
		# add
		a = self.add(r)
		
		return a
	
	def __div__(self,r):
		"""Use the / shortcut for division.
		
		Arguments:
			r: Result instance
			
		Returns:
			Result instance.
		"""
		
		# divide
		d = self.divide(r)
		
		return d
	
	def __invert__(self):
		"""Use the ~ operator for the multiplicative inverse
		
		Arguments:
			None
			
		Returns:
			Result instance
		"""
		
		# divide into one
		v = Re(1).divide(self)
		
		return v
	
	def __mul__(self,r):
		"""	Use the * shortcut for multiplication.
		
		Arguments:
			r: Result instance
			
		Returns:
			Result instance.
		"""
		
		# multiply
		m = self.multiply(r)
		
		return m
	
	def __neg__(self):
		"""Use the - shortcut for the additive inverse.
		
		Arguments:
			None
			
		Returns:
			Result instance
		"""
		
		# take negative
		n = self.scale(-1)
		
		return n

	def __pos__(self):
		"""Use the + operator as a shortcut to view the Result instance.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# view the term
		self.view()
		
		return None
	
	def __pow__(self,n):
		"""Use the ** shortcut for taking a power.
		
		Arguments:
			n: integer
			
		Returns:
			Result instance
		"""
		
		# take power
		p = self.power(n)
		
		return p
	
	def __sub__(self,r):
		"""Use the - shortcut for subtraction.
		
		Arguments:
			r: Result instance
			
		Returns:
			Result instance
		"""
		
		# add negative
		s = self.subtract(r)
		
		return s
	
	def add(self,r):
		"""Add to the Result instance.
		
		Arguments:
			r: Result instance, or other number type
			
		Returns:
			Result instance
		
		Notes:
			(a + bi) + (c + di) = (a + c) + (b + d)i.
		"""
		
		# self attributes
		a = self.real
		b = self.imag
		
		# convert argument
		r = Re(r)
		c = r.real
		d = r.imag
		
		# add
		f = a + c
		g = b + d
		
		return Re(f,g)
		
	def angle(self):
		"""Calculate the polar angle of the Result instance.
		
		Arguments:
			None
			
		Returns:
			float, angle measured in radians
			
		Notes:
			Angle spans 0 to pi for positve imaginary components and -pi to 0 for negative imaginary components.
		"""
		
		# calculate angle
		r = self.real
		g = self.imag
		a = atan(g,r)
		
		return a
		
	def conjugate(self):
		"""Form the complex conjugate of the Result instance.
		
		Arguments:
			None
			
		Returns:
			Result instance
		"""
		
		# complex conjugate
		r = self.real
		m = -self.imag
		
		return Re(r,m)
		
	def copy(self):
		"""Copy the Result instance.
		
		Arguments:
			None
			
		Returns:
			Result instance.
		"""
		
		# references
		r = self.real
		i = self.imag
		
		return Re(r,i)

	def divide(self,r):
		"""Divide the Result instance by another number.
		
		Arguments:
			r: Result instance, or other number type
			
		Returns:
			Result instance
			
		Notes:
			(a + bi) / (c + di) = ((ac + bd) + (bc - ad)i) / (c^2 + d^2).
			
			c or d must be nonzero.
		"""
		
		# attributes
		a = self.real
		b = self.imag
		
		# convert argument
		r = Re(r)
		c = r.real
		d = r.imag
		
		# new complex quantities
		m = c**2 + d**2
		f = a * c + b * d
		g = b * c - a * d
		
		# m must be nonzero
		try:
			p = f / m
			q = g / m
			
		# otherwise return a copy
		except ZeroDivisionError:
			print('Cannot divide by zero, division aborted.\n')
			
			return self.copy()
		
		return Re(p,q)
		
	def draw(self):
		"""Draw the Result instance as a vector in the complex plane.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# make vectors
		x = [0,self.real]
		y = [0,self.imag]
		
		# plot
		plt.plot(x,y,'r-')
		plt.margins(0.1,0.1)
		plt.show()
		plt.close()
		
		return None
		
	def modulus(self):
		"""Calculate the modulus of the Result instance.
		
		Arguments:
			None
			
		Returns:
			float, the modulus
		"""
		
		# calculate modulus
		r = self.real
		g = self.imag
		m = sqrt(r**2 + g**2)
		
		return m
		
	def multiply(self,r):
		"""Multiply the Result instance by another number.
		
		Arguments:
			r: Result instance, or other number type
			
		Returns:
			Result instance
			
		Notes:
			(a + bi) * (c + di) = (ac - bd) + (ad + bc)i.
		"""
		
		# attributes
		a = self.real
		b = self.imag
		
		# convert argument
		r = Re(r)
		c = r.real
		d = r.imag
		
		# multiply
		# (a + bi) * (c + di) = 
		# (ac - bd) + (ad + bc)i
		f = (a * c) - (b * d)
		g = (a * d) + (b * c)
		
		return Re(f,g)
		
	def normalize(self):
		"""Normalize the Result instance.
		
		Arguments:
			None
			
		Returns:
			Result instance
		"""
		
		# normalize
		r = self.real
		g = self.imag
		m = sqrt(r**2 + g**2)
		n = self.divide(Re(m))
		
		return n
		
	def power(self,p):
		"""Take the Result instance to a power.
		
		Arguments:
			p: integer, the exponent
			
		Returns:
			Result instance
			
		Notes:
			Performs p rounds of multiplication.  If p is negative, takes the positive power and divides into one.
		"""
		
		# convert power to int
		p = int(p)
		
		# begin with one
		s = self
		m = Re(1)
		
		# multiply
		for i in range(abs(p)):
			m = m.multiply(s)
			
		# if p is negative, divide into one
		if p < 0:
			m = Re(1).divide(m)
		
		return m
		
	def root(self,t): 
		"""Take a root of the Result instance.
		
		Arguments:
			t: integer, degree of root
			
		Returns:
			Result instance
			
		Notes:
			Polar form is used.  The angle is divided by t and the modulus is taken to the (1/t) power.  Other possible roots are not calculated.
		"""
		
		# convert to float
		t = float(t)
		
		# form angle and modulus
		r = self.real
		g = self.imag
		m = self.modulus()
		
		# divide angle
		try:
			a = self.angle() / t
			
		# unless t is zero
		except ZeroDivisionError:
			print('Cannot take zeroth root, root aborted.\n')
			
			return self.copy()
		
		# take root of modulus
		m = m ** (1.0 / t)
		
		# recalculate
		r = m * cos(a)
		g = m * sin(a)
		
		return Re(r,g)
		
	def scale(self,n,d=None):
		"""Scale by a constant.
		
		Arguments:
			n: real number, numerator of scale factor
			d: real number, denominator of scale factor
			
		Returns:
			Result instance
		"""
		
		# make copy
		s = self.copy()
		
		# calculate scale factor
		k = float(n)
		if d:
			k /= float(d)
			
		# adjust attributes
		a = s.real * k
		b = s.imag * k
		
		return Re(a,b)
		
	def subtract(self,r):
		"""Subtract from the Result instance.
		
		Arguments:
			r: Result instance, or other number type
			
		Returns:
			Result instance
			
		Notes:
			Multiplies by -1 and adds.
		"""
		
		# multiply by -1 and add
		r = Re(r)
		r = r.scale(-1)
		a = self.add(r)
		
		return a
		
	def view(self,a=0):
		"""View the Result instance.
		
		Arguments:
			a=0: integer, indentation spaces
			
		Returns:
			None
		"""

		# references
		r = self.real
		m = self.imag
		
		# tab
		t = ' ' * a
		
		# offset positives
		s = t + ' %f' % (r)
		if r < 0:
			s = s[1:]
			
		# add imaginary
		if m < 0:
			s += t + ' %fi' % (m)
		elif m > 0:
			s += t + ' +%fi' % (m)
		
		# print
		print(s)
		
		return None
		
		
# Abbreviation
Re = Result
		


