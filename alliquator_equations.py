# alliquator_equations.py
# classes to manipulate algebraic expressions

# import results
import alliquator_results as aq_re
Re = aq_re.Result

# import pages
import alliquator_pages as aq_pa
Pa = aq_pa.Page

# import books
import alliquator_books as aq_bo
Bo = aq_bo.Book

# import shelves
import alliquator_shelves as aq_sh
Sh = aq_sh.Shelf

# import terms
import alliquator_terms as aq_te
Te = aq_te.Term

# import lines
import alliquator_lines as aq_li
Li = aq_li.Line

# import expressions
import alliquator_expressions as aq_ex
Ex = aq_ex.Expression


# Equation subclass of Expression
class Equation(Ex):
	"""An Equation is an Expression equaling zero.
	
	Equation inherits from Expression class.
	"""
	
	def __init__(self,l,r=None):
		"""Define an Equation from expressions on the left and right sides.
		
		Arguments:
			l: Expression instance, lefthand side
			r=None: Expression instance, righthand side
			
		Attributes:
			name: string, name of equation
			
		Notes:
			If a righthand side of the equation is entered, it will be subtracted from the lefthand side to make the lefthand side equal to zero.
			
		Examples:
			The equation (3x^2 + 2x) = (5x - 2) can be entered with a single string:
				
				Eq('3x2 + 2x = 5x - 2')
				
			two strings:
				
				Eq('3x2 + 2x','5x - 2')
				
			or two Expression instances:
				
				Eq(Ex('3x2 + 2x'),Ex('5x - 2'))
		"""
		
		# attempt to split string by =
		try:
			s = l.split('=')
			l = s[0]
			
			# right side
			try:
				r = s[1]
			except:
				pass
				
		# otherwise keep as is
		except:
			pass
		
		# convert to Expression
		l = Ex(l)
		
		# subtract right side from left
		if r:
			l = l.subtract(r)
			
		# transfer attributes
		self.append(l.top())
		self.append(l.bottom())
		self.name = l.name


	# static methods
	@staticmethod
	def _arrange(s):
		"""Arrange list of solutions in order of highest real part, or highest imaginary part for equal real parts.
		
		Arguments:
			s: list of numbers
			
		Returns:
			list of numbers
		"""
		
		# sort according to real part
		s.sort(key = lambda x: x.real)
		
		# segregate into partial lists of roughly equal real parts
		l = []
		f = s[0]
		p = [f]
		for i in s[1:]:
			
			# difference between reals
			d = abs(i.real - f.real)
			
			# if real parts are roughly equal, place in partial together
			if d < Re.tolerance:
				p.append(i)
				
			# otherwise start new partial 
			else:
				f = i
				l.append(p)
				p = [i]
				
		# add final partial
		l.append(p)
		
		# sort sublists by imaginary part
		for i in l:
			i.sort(key = lambda x: x.imag)
			
		# recombine lists
		l = [i for j in l for i in j]
		
		# reverse for largest first
		l.reverse()
		
		return l
	
	@staticmethod
	def _cubic(a,b,c,d):
		"""Solve a cubic equation of the form ax^3 + bx^2 + cx + d = 0
			
		Arguments:
			a: Result instance
			b: Result instance
			c: Result instance
			d: Result instance
			
		Returns:
			Page instance
		"""
		
		# intermediates
		# f = (2b^3 - 9abc + 27da^2) / 2
		f = Li('b3 -9/2a b c + 27/2 d a2')
		f = f.evaluate(a=a,b=b,c=c,d=d)
		
		# g = (b^2 - 3ac)
		g = Li('b2 -3a c')
		g = g.evaluate(a=a,b=b,c=c)
		
		# h = sqrt(f^2 - g^3)
		h = Li('f2 - g3')
		h = h.evaluate(f=f,g=g)
		h = h.root(2)
		
		# k = f +/- h
		o = [1,-1]
		k = [h.scale(i).add(f) for i in o]
		
		# take cube roots, l = rt3(k)
		l = [i.root(3) for i in k]
		
		# three cubic roots of unity
		# u = 1, (-1 +/- sqrt(3)) / 2
		u = [Re(1.0)]
		z = Re(3)
		z = z.root(2).real
		u.append(Re(-1.0 / 2.0, z / 2.0))
		u.append(Re(-1.0 / 2.0, -z / 2.0))
		
		# cycle through cube roots of unity
		m = [l[0].multiply(i) for i in u]
		n = [l[1].multiply(i) for i in u]
		
		# roots line up in opposite directions, so reverse n.
		n.reverse()
		
		# m * n = g for the correct combos
		# test first three values against m[0] and pick the one closest to g
		w = [i.multiply(m[0]) for i in n]
		s = [g.subtract(i) for i in w]
		s = [i.modulus() for i in s]
		j = s.index(min(s))
		
		# double n to wrap sequence around, and pick three members beginning at j
		n = n * 2
		p = n[j:j + 3]
			
		# add pairs together
		q = [i.add(j) for i,j in zip(m,p)]
		
		# finish roots
		# r = -1 / 3a
		# x = r * (q + b)
		r = Re(-1.0 / 3.0).divide(a)
		x = [i.add(b).multiply(r) for i in q]
		
		# arrange roots
		x = Eq._arrange(x)
		
		return x
	
	@staticmethod
	def _linear(a,b):
		"""Solve a linear equation of the form ax + b = 0.
		
		Arguments:
			a: Result instance
			b: Result instance
			
		Returns:
			Page instance
		"""
		
		# solution: x = -B / A
		s = b.scale(-1).divide(a)
		
		return Pa([s])
	
	@staticmethod
	def _quadratic(a,b,c):
		"""Solve a quadratic equation of the form ax^2 + bx + c = 0.
		
		Arguments:
			a: Result instance
			b: Result instance
			c: Result instance
			
		Returns:
			Page instance.
		"""
		
		# intermediates
		# f = -b / 2
		# g = f^2 -ac
		# h = sqrt(g)
		f = Li('-1/2b')
		f = f.evaluate(b=b)
		g = Li('f2 - a c')
		g = g.evaluate(a=a,c=c,f=f)
		h = g.root(2)
		
		# solutions
		# x = (f +/- h) / a
		o = [1,-1]
		x = [h.scale(i).add(f) for i in o]
		x = [i.divide(a) for i in x]
		
		# arrange roots
		x = Eq._arrange(x)
			
		return x
		
		
	# instance methods
	def assimilate(self,*g,**f):
		"""Perform ihtegration along two axes.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, variable to solve for
				1) string, name of variable to graph
				2) if string indicates a second variable. 
				2...) complex numbers or lists of numbers, by default (-2,-2) and (2,2).  Integers thereafter designate numbers of steps for the x and y axes, by default 16.
				3) boolean, show graph?, defaults to True
				4) boolean, crisp solutions?, defaults to False
				
			**f: unpacked dictionary mapping variables to functions or constants
			
		Returns:
			Shelf instance
			
		Notes:
			If three variables are given before **kwargs, the equation will be solved for the first and plotted against the real coordinates of the second and third variables.
			
			If two variables are given, the equation will be solved for the first variable and plotted against the complex plane of the second variable.
			
			If only one variable is given, the equation will be plotted against the complex plane of this variable without solving.
			
			Function objects are limited to being functions of the first variable.
		"""
	
		# get lists of solutions using sculpt
		s = self.sculpt(*g,**f)
		
		# assimilate
		t = s.assimilate()
			
		return t
	
	def crisp(self,*a,**d):
		"""Crisp the solutions by correcting for numerical instability using newton's method.
		
		Arguments:
			*a: unpacked tuple of *args:
				0) string, variable name solved for
				1) list of Results, uncrisped solutions
			**d: unpacked dictionary mapping variables to values
			
		Returns:
			list of Result instances, crisped solutions
		"""
		
		# unpack *args
		x = a[0]
		s = a[1]
		
		# get expression and derivative
		e = self.detach()
		v = e.derive(x)
		
		# for each solution
		for n,i in enumerate(s):
			
			# loop until tolerance is reached
			f = 1.0
			g = []
			while abs(f) > Re.tolerance:
				
				# evaluate the function and its derivative at the solution
				d[x] = i
				f = e.evaluate(**d)[0]
				p = v.evaluate(**d)[0]
				
				# recalculate 
				a = f.divide(p)
				i = i.subtract(a)
				
				# if algorithm is stuck
				if (f,i) in g:
					g.sort(key=lambda x: abs(x[0]))
					i = g[0][1]
					break
					
				# record pair
				g.append((f,i))
				
			# reinsert
			s[n] = i
				
		return s
		
	def detach(self):
		"""Detach the right side zero of an equation to make an Expression instance.
		
		Arguments:
			None
			
		Returns:
			an Expression instance."""
	
		# make copy
		s = self.copy()
		
		# attributes
		t = s.top()
		b = s.bottom()
		n = s.name
			
		return Ex(t,b,n)
	
	def draw(self,*g,**f):
		"""Draw a plot of the expression after solving.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, name of variable to solve for
				1) string, name of independent variable to plot against
				2) number, left limit, defaults to -2.  
				3) number, right limit, defaults to 2.  
				4) number, steps, defaults to 64.
				5) boolean, view graph?, defaults to True.
				6) boolean, crisp solutions?, defaults to False
				
			**f: unpacked dictionary variables mapped to numbers or function objects
			
		Returns:
			Book instance
			
		Examples:
			For the equation (3xc^2 + 5xc + 2) = 0, setting v = 'c' will first solve the equation in terms of.  In this example, the equation is quadratic in c, so two solutions will be calculated at each point, and both will be plotted.  The return value will be a list of two lists of ComplexNumber instances because there are two possible solutions calculated at each point.
			
		Notes:
			All numerical solutions are in the form of complex numbers, so the real and imaginary parts of the solutions are plotted separately in related colors.
			
			Endpoints themselves of the drawing range are not actually calculated.  The range is broken into steps and the midpoint of each step is calculated.
		"""
		
		# distil booleans from *args
		o = g
		g,w = Ex._distil(g)
		
		# left limit
		try:
			a = complex(g[1])
			x = g[0]
			v = None
			z = 0
			
		# if it is a string, there are two strings
		except ValueError:
			z = 1
			x = g[1]
			v = g[0]
			
			# get left limit
			try:
				a = complex(g[1 + z])
			except:
				a = -2.0
					
		# otherwise there is only one
		except:
			z = 0
			x = g[0]
			v = None
			a = -2.0
			
		# right limit
		try:
			b = complex(g[2 + z])
		except:
			b = 2.0
			
		# steps
		try:
			n = int(g[3 + z])
		except:
			n = 64
		
		# if no v is provided, perform regular draw with original *args
		if not v:
			u = self.detach()
			r = u.draw(*o,**f)
			
			return r
		
		# get points
		p = Ex._points(a,b,n)
			
		# get results
		if True in w:
			r = self.sample(v,x,p,True,**f)
		else:
			r = self.sample(v,x,p,**f)
			
		# show graph if appropriate
		if False not in w:
			r.draw()
		
		return r
	
	def integrate(self,*g,**f):
		"""Integrate the expression after solving.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, name of variable to solve for
				1) string, name of independent variable to plot against
				2) number, left limit, defaults to -2.  
				3) number, right limit, defaults to 2.  
				4) number, steps, defaults to 64.
				5) boolean, view graph?, defaults to True.
				6) boolean, crisp solutions?, defaults to False
				
			**f: unpacked dictionary variables mapped to numbers or function objects
			
		Returns:
			Page instance
			
		Notes:
			If the expression is quadratic or cubic in the solving variable, there will be multiple integration results, one for each sequence of solutions.
		"""
		
		# get lists of solutions using draw
		s = self.draw(*g,**f)
		
		# integrate
		t = s.integrate()
			
		return t
	
	def isolate(self,x):
		"""Isolate a variable.

		Arguments:
			x: string, variable name
			
		Returns:
			Expression instance.
			
		Examples:
			Consider the equation (3x^2a + 9x) = 0.  The equation can be rearranged to isolate one side.  In this case, a = (-9x) / (3x^2).  
			
			Consider the equation (4ax^2y + 5xy^2 - 2ax) / (x + 3) = 0.  Isolation of a leads to a = (-5xy^2) / (4x^2y -2x)
			
		Notes:
			Only terms with x^0 or x^1 are allowed.  Isolating variables at higher powers is beyond the abilities of this function.
			
			Divisors are ignored, as they can be multiplied through without effecting the zero on the other side.
		"""
		
		# partition into constant and linear terms
		p = self.section(x)
		
		# get powers of coefficients
		l = len(x)
		n = [int(i.name[l:]) for i in p]
		if set(n) != {0,1}:
			print('Isolation requires powers of %s at 0 and 1 only.  Isolation aborted\n' % (x))
			
			return self.copy()
			
		# if (Ax + B)/D = 0
		# x = -B D / A D = -B / A
		# denominators cancel
		t = p[0].top().scale(-1)
		b = p[1].top()
		
		# variable name is the name
		m = '%s' % (x)
		
		return Ex(t,b,m)

	def jot(self):
		"""Jot down the equation as a single string.
		
		Arguments:
			None
			
		Returns:
			string
		"""
		
		# jot expression
		s = self.detach().jot()
		
		# combine with =
		s += ' = 0'
		
		return s

	def sample(self,*a,**f):
		"""Evaluate equation at every point given after solving.
		
		Arguments:
			*a: unpacked tuple:
				0) string, variable to first solve for
				1) string, variable to sample at
				2) list of numbers, sampling points
				3) string, possible second variable
				4) number, value of second variable
				5) boolean, crisp solutions using newton's method? defaults to False
			
			**f: unpacked dictionary of function objects or numbers mapped to variable names to evaluate based on x
			
		Returns:
			Book instance
			
		Examples:
			If the equation is (3a^2x + 2ay - 1) = 0, solving first for 'a' will result in a quadratic, and hence two solutions per value of x.  A list of two lists of complex numbers will be returned.  An attempt is made to make the lists continuous by grouping together points with lowest overall curvature.
		"""
		
		# distil booleans
		a,b = Ex._distil(a)
		
		# unpack *args
		# assume all five parameters
		try:
			v = a[0]
			x = a[1]
			p = a[2]
			y = a[3]
			q = a[4]
			
		# or four without solving variable
		except:
			try:
				v = None
				x = a[0]
				p = a[1]
				y = a[2]
				q = a[3]
				
			# or three without second sampling variable
			except:
				try:
					v = a[0]
					x = a[1]
					p = a[2]
					y = None
					q = None
					
				# otherwise no solving variable either
				except:
					v = None
					x = a[0]
					p = a[1]
					y = None
					q = None
		
		# if no v given, perform regular sample
		if not v:
			r = self.detach().sample(*a,**f)
			
			return r
			
		# evaluate results
		r = []
		for i in p:
			
			# reckon dictionary
			d = Ex._reckon(f,x,i,y,q)
			
			# solve for variable v
			if True in b:
				s = self.solve(v,True,**d)
			else:
				s = self.solve(v,**d)
			r.append(s)
				
		# make book
		l = Bo(r,x)
				
		return l

	def sculpt(self,*g,**f):
		"""Sculpt a 3d plot.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, variable to solve for
				1) string, name of variable to graph
				2) if string indicates a second variable. 
				2...) complex numbers or lists of numbers, by default (-2,-2) and (2,2).  Integers thereafter designate numbers of steps for the x and y axes, by default 16.
				3) boolean, show graph?, defaults to True
				4) boolean, crisp solutions?, defaults to False
				
			**f: unpacked dictionary mapping variables to functions or constants
			
		Returns:
			Shelf instance
			
		Notes:
			If three variables are given before **kwargs, the equation will be solved for the first and plotted against the real coordinates of the second and third variables.
			
			If two variables are given, the equation will be solved for the first variable and plotted against the complex plane of the second variable.
			
			If only one variable is given, the equation will be plotted against the complex plane of this variable without solving.
			
			Function objects are limited to being functions of the first variable.
		"""
		
		# distil booleans
		o = g
		g,e = Ex._distil(g)
		
		# parse *args into strings and numbers
		s,n = Ex._segregate(g)
		
		# set all three variables
		try:
			z = s[0]
			x = s[1]
			y = s[2]
			
		# or skip second graphing variable
		except:
			try:
				z = s[0]
				x = s[1]
				y = None
				
			# or skip solving variable as well
			except:
				z = None
				x = s[0]
				y = None
		
		# if no solving variable, sculpt as regular expression with original *args
		if not z:
			h = self.detach()
			h = h.sculpt(*o,**f)
			
			return h
			
		# set lower left corner
		try:
			a = Re(n[0],n[1])
		except:
			a = Re(-2,-2)
			
		# set upper right corner
		try:
			b = Re(n[2],n[3])
		except:
			b = Re(2,2)
			
		# set x-axis resolution
		try:
			p = int(n[4])
		except:
			p = 16
			
		# set y-axis resolution
		try:
			q = int(n[5])
		except:
			q = 16
			
		# calculate first axis points
		u = Ex._points(a.real,b.real,p)
			
		# calculate second axis points
		v = Ex._points(a.imag,b.imag,q)
		
		# loop through second axis rows
		h = []
		for i in v:
			
			# progress tracker
			print('.', end='')
			
			# two real variables?
			if y:
				f[y] = i
				w = u
				
			# one complex variable?
			else:
				w = [Re(j,i) for j in u]
				
			# assemble *args
			if y:
				r = (z,x,w,y,i)
			else:
				r = (z,x,w)
				
			# crisp solutions?
			if True in e:
				r += True,
			
			# evaluate
			s = self.sample(*r,**f)
			
			# place into list of books
			h.append(s)
			
		# end tracker
		print('\n')
			
		# make Shelf
		if y:
			h = Sh(h,y)
		else:
			h = Sh(h,x)
			
		# sculpt
		if False not in e:
			h.sculpt()
		
		return h

	def simplify(self):
		"""Simplify an equation by removing the denominator and factoring.
		
		Arguments:
			None
			
		Returns:
			Equation instance
		"""
		
		# factor top
		t,g = self.top().factor()
		
		# bottom becomes one
		b = Li(1)
		
		# keep name
		n = self.name
		
		# make equation
		q = Eq(Ex(t,b,n))
					
		return q
					
	def solve(self,*g,**d):
		"""Solve a polynomial equation.
		
		Arguments:
			*g: unpacked tuple:
				1) string, name of variable to solve for
				2) boolean, True to use newton's method to tighten the solutions
			**d: unpacked dictionary mapping all variables to values
			
		Returns:
			Page instance
			
		Notes:
			If the highest degree of x is greater than 3, this function lacks to ability to solve it.
		"""
		
		# distil booleans
		g,b = Ex._distil(g)
		
		# get variable
		x = g[0]
		
		# partition
		p = self.section(x)
		
		# sort expressions into dictionary by exponent
		s = {}
		l = len(x)
		for i in p:
			n = i.name
			n = int(n[l:])
			s[n] = i
			
		# verify keys are 0-3
		t = [i in (0,1,2,3) for i in s]
		if False in t:
			print('Equation has powers of %s that are beyond the capabilities of this function.  Solve aborted.\n' % (x))
			
			return Pa([Re(0)])
			
		# fill in empty expression if missing
		m = max(s)
		for i in range(m + 1):
			if i not in s:
				s[i] = Ex([])
				
		# order by power and evaluate
		k = s.keys()
		k.sort()
		k.reverse()
		c = [s[i].evaluate(**d) for i in k]
		c = [i[0] for i in c]
		
		# only constant term?
		if len(c) < 2:
			print('%s is not in the equation.  Solve aborted\n.' % (x))
			
			return Pa([Re(0)])
		
		# solving subroutine
		if len(c) == 2:
			r = Eq._linear(*c)
		if len(c) == 3:
			r = Eq._quadratic(*c)
		if len(c) == 4:
			r = Eq._cubic(*c)
			
		# crisp solutions
		if True in b:
			r = self.crisp(x,r,**d)
		
		return Pa(r,x,self.jot(),d)

	def view(self):
		"""View the equation.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# print name
		if self.name:
			print(self.name + ':')
			
		# print top terms
		t = self.top()
		for i in t:
			i.view()
		if len(t) == 0:
			print('(0)')
			
		# check for trivial bottom
		b = self.bottom()
		o = Li(1)
		if not b.compare(o):
			print('/')
			
			# check for zero
			if len(b) == 0:
				print('(0)')
			else:
				for i in b:
					i.view()
			
		# equals zero
		print('= 0')
		print(' ')
			
		return None


# Abbreviation
Eq = Equation





