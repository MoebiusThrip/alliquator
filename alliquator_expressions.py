# alliquator_expressions.py
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


# class to manipulate algebraic expressions
class Expression (list):
	"""An Expression is one Line of Terms divided by another.
	
	Expression class inherits from list.
	"""
	
	def __init__(self,t=None,b=None,n=None):
		"""Define an algebraic expression.
		
		Arguments:
			t: Expression instance, Line instance, string, pair of integers, or integer
			b: Line instance, string, pair of integers, or integer
			n: string, name of expression
			
		Attributes:
			name: string, name of expression
			
		Notes:
			A string for the expression may contain a '/' to separate the top and bottom lines.  It must have a space on each side to differentiate from a fraction.
			
		Examples:
			For instance, the expression (3x^2 - 5) / (5x^3 + 2y) can be entered as:
				
				Ex('3x2 -5', '5x3 +2y')
				
			or:
				 
				Ex('3x2 -5 / 5x3 + 2y')
				
			The expression (1/2x^2 + 2) / (3/4y^3 - 2/3x) can be entered as:
				
				Ex('1/2x2 + 2 / 3/4y3 - 2/3x')
				
			but not
			
				Ex('1 / 2x2 + 2 / 3 / 4y3 - 2 / 3x')
		"""
		
		# default top to 0
		if t is None:
			t = 0
			
		# default bottom to 1
		if b is None:
			b = 1
			
		# check for name
		try:
			n = t.name
		except:
			pass
			
		# split by '/' and translate
		try:
			p = t.split(' / ')
			t = p[0]
			t = Li(t)
			if len(p) > 1:
				b = p[1]
			b = Li(b)
			
		# or translate directly
		except:
			try:
				t = Li(t)
				b = Li(b)
		
			# otherwise assume list of lists
			except:
				b = Li(t[1])
				t = Li(t[0])
			
		# put into self
		self.append(t)
		self.append(b)
		
		# attributes
		self.name = n


	# static methods
	@staticmethod
	def _build(f,p,a,d):
		"""Build a dictionary of partial derivative substitutions.
		
		Arguments:
			f: string, function whose partials are to be expanded
			p: list of strings, partials to calculate
			a: list of strings, additional derivable functions
			d: dictionary mapping variables to substitutions
			
			Returns:
				a dictionary mapping partial derivatives to substituting expressions
			"""
		
		# remove stem for list of subscripts
		n = len(f)
		u = [i[n:] for i in p]
		
		# highest order is largest length of subscript
		o = [len(i) for i in u]
		
		# return empty dictionary if no partials
		try:
			o = max(o)
		except ValueError:
			
			return {}
		
		# find coordinates by picking unique letters from subscripts
		c = [j for i in u for j in i]
		c = set(c)
		
		# pair functions with coordinates
		z = Ex._couple(c,a)
		
		# extend dictionary to include all coordinates
		d = Ex._mimic(d,c,z)
		
		# begin substitution dictionary
		b = {f:d[f]}
		
		# begin derivatives list with stem
		l = [f]
		
		# for every degree
		for g in range(o):
			
			# begin new derivatives list
			w = []
			
			# for every derivative already generated
			for i in l:
				
				# for every coordinate, take the derivative
				for j in c:
					
					# form function list
					y = [k for k in z.keys()]
					y = [k for k in y if j in z[k]]
					e = b[i].derive(j,*y)
					
					# substitute from dictionary
					for k in d:
						e = e.substitute(d[k],k)
						
					# add to new derivative list
					w.append(i + j)
					
					# add to substitution dictionary
					b[i + j] = e
					
			# swap new list for old
			l = w
			
		return b
	
	@staticmethod
	def _couple(c,a):
		"""Couple functions with associated coordinates.
		
		Arguments:
			c: list of strings, coordinates
			a: tuple of strings, function names and potentially function coordinates
			
		Returns:
			dictionary, maps functions to coordinates
		"""
		
		# string containing all coordinates
		o = ''
		for i in c:
			o += i
			
		# search additional function strings for coordinate strings and pair them with their functions
		f = []
		g = []
		q = False
		for i in a:
			
			# if last string was a function
			if q:
				
				# search this string for coordinate characters
				t = [j in c for j in i]
				
				# if non-coordinate character is found, pair last function with all coordinates and add new function
				if False in t:
					g.append(o)
					f.append(i)
					
				# otherwise add to coordinates list
				else:
					g.append(i)
					q = False
					
			# otherwise add string to function list
			else:
				f.append(i)
				q = True
				
		# add all coordinates to last function if not given, gets dropped at zip if not needed
		g.append(o)
				
		# form dictionary from pairs
		z = zip(f,g)
		d = {i:j for i,j in z}
		
		return d
	
	@staticmethod
	def _distil(g):
		"""Distil booleans from a list of arguments.
		
		Arguments:
			g: tuple of arguments
			
		Returns:
			tuple:
				tuple of *args without booleans
				list of booleans
		"""
		
		# true of false
		t = True
		f = False
		tf = lambda x: x is t or x is f
		
		# take out of *args
		g = list(g)
		u = [i for i in g if tf(i)]
		g = [i for i in g if not tf(i)]
		g = tuple(g)
		
		return g,u
	
	@staticmethod
	def _mimic(d,c,z):
		"""Mimic derivatives explicitly given for other coordinates.
		
		Arguments:
			d: dictionary mapping partial derivative strings to Expressions
			c: list of strings, the coordinate variables
			z: dictionary, function strings mapped to coordinate strings
		
		Returns:
			tuple:
				dictionary mapping variables to Expression instances,
				dictionary mapping additional functions to coordinates
		"""
			
		# for all coordinates, sort their dictionary entries
		l = []
		for i in c:
			e = [k for k in d if k.endswith(i)]
			l.append(e)
			
		# find stems
		s = [j[:-1] for i in l for j in i]
		s = set(s)
		
		# for each stem
		for i in s:
			
			# check for entry in coordinate dictionary
			if i not in z:
				
				# add all coordinates
				a = ''
				for j in c:
					a += j
				z[i] = a
			
			# find entries that are present in dictionary and those that are not
			p = []
			n = []
			for j in c:
				if i + j in d:
					p.append(j)
				else:
					n.append(j)
					
			# for entries not in dictionary
			for j in n:
				
				# add zero to substitution dictionary if not in associated coordinates
				if j not in z[i]:
					d[i + j] = Ex(0)
					
				# otherwise mimic 
				else:
				
					# pick one that has an entry
					x = p[0]
				
					# replace coordinate in expression
					b = d[i + x]
					b = b.plug(j,x)
				
					# replace any additional functions
					for k in z.keys():
						b = b.plug(k + j,k + x)
					
					# add to dictionary
					d[i + j] = b
			
		return d

	@staticmethod
	def _points(a,b,n):
		"""Make a collection of points from beginning and ending distances, and number of points.
		
		Arguments:
			a: number, beginning of range
			b: number, end of range
			n: integer, number of points
			
		Returns:
			list of numbers, the points
		"""
		
		# check n
		n = int(n)
		
		# make template
		t = [i * 2 + 1 for i in range(n)]
		
		# calculate distance
		a = Re(a)
		b = Re(b)
		d = b.subtract(a)
		
		# scale template for points
		p = [d.scale(i,2 * n) for i in t]
		p = [a.add(i) for i in p]
			
		return p
				
	@staticmethod
	def _reckon(f,x,p,y=None,q=None):
		"""Convert function objects to values.
		
		Arguments:
			f: dictionary, maps variable names to numbers or function objects
			x: string, first independent variable name
			p: number, value for x
			y=None: string, second independent variable name
			q=None: number, value for y
			
		Returns:
			dictionary, maps variables to values.
		"""
		
		# begin dictionary
		d = {x:p}
		if y:
			d[y] = q
			
		# convert functions to numbers
		for k,i in f.items():
			
			# check for number
			try:
				d[k] = Re(i)
				
			# or evaluate function with both variables
			except:
				try:
					d[k] = i(p,q)
					
				# or use only real components
				except:
					try:
						d[k] = i(p.real,q.real)
						
					# or try one variable
					except:
						try:
							d[k] = i(p)
							
						# or the real component
						except:
							try:
								d[k] = i(p.real)
								
							# or assume Expression instance
							except:
								try:
									i = Ex(i)
									e = i.evaluate(**d)
									d[k] = e[0]
									
								# otherwise abort
								except:
									print('Invalid function or value.  Evaluation aborted.\n')
									raise ValueError('Invalid function or value.  Evaluation aborted.\n')
									
		return d

	@staticmethod
	def _segregate(a):
		"""Segregate a list of *args into strings and numbers.
		
		Arguments:
			a: tuple of strings, numbers, and pairs of numbers
			
		Returns:
			tuple:
				list of strings,
				list of numbers
		"""

		# parse *args into strings and numbers
		s = []
		n = []
		for i in a:
			
			# add to strings if all letters
			try:
				if i.isalpha():
					s.append(i)
				
			# otherwise search for numbers
			except:
				try:
					n.append(float(i))
					
				# or pairs of numbers
				except:
					try:
						n.append(i[0])
						n.append(i[1])
						
					# or complex numbers
					except:
						try:
							n.append(i.real)
							n.append(i.imag)
							
						# otherwise skip
						except:
							pass
							
		return s,n

	# instance methods
	def __add__(self,e):
		"""Use the + shortcut for addition.
		
		Arguments:
			e: Expression instance, Line instance, Term instance, pair of integers, or integer
			
		Returns:
			Expression instance
		"""
		
		# add
		a = self.add(e)
		
		return a
	
	def __div__(self,r):
		"""Use the / shortcut for division.
		
		Arguments:
			e: Expression instance, Line instance, Term instance, pair of integers, or integer
			
		Returns:
			Expression instance.
		"""
	
		# divide
		d = self.divide(e)
		
		return d
	
	def __eq__(self,e):
		"""Use the == shortcut for comparison.
		
		Arguments:
			e: Expression instance or string
			
		Returns:
			boolean, expressions equal?.
		"""
	
		# compare
		q = self.compare(e)
			
		return q
	
	def __iadd__(self,e):
		"""Use the += shortcut for addition and reassignment to the same pointer.
		
		Arguments:
			e: Expression instance, Line instance, Term instance, string, pair of integers, or integer
			
		Returns:
			Expression instance
		"""
		
		return self.add(e)
		
	def __idiv__(self,e):
		"""Use the /= shortcut for division with reassignment of pointer.
		
		Arguments:
			e: Expression instance, Line instance, Term instance, pair of integers, or integer
			
		Returns:
			Expression instance.
		"""
	
		# divide
		d = self.divide(e)
		
		return d
		
	def __ilshift__(self,g):
		"""Use the <<= shortcut to substitute an expression and reassign the pointer.
		
		Arguments:
			g: tuple:
				0) pair of Line instances, or string
				1) string, name of variable with optional exponent
				
		Returns:
			Expression instance
		"""
		
		return self.substitute(*g)
		
	def __imul__(self,e):
		"""Use the *= shortcut for multiplication and reassignment to the same pointer.
		
		Arguments:
			e: Expression instance, Line instance, Term instance, string, pair of integers, or integer
			
		Returns:
			Expression instance
		"""
		
		return self.multiply(e)
	
	def __invert__(self):
		"""Use the ~ prefix as a shortcut to simplify.
		
		Arguments:
			None
			
		Returns:
			Expression instance
		"""
		
		# invert
		v = self.simplify()
		
		return v
	
	def __ipow__(self,n):
		"""Use the **= shortcut for exponentiation and reassignment to the same pointer.
		
		Arguments:
			n: integer, the exponent
			
		Returns:
			Expression instance
		"""
		
		return self.power(n)
		
	def __irshift__(self,g):
		"""Use the >>= shortcut to substitute an expression and reassign the pointer.
		
		Arguments:
			g: tuple:
				0) pair of Line instances, or string
				1) string, name of variable with optional exponent
				
		Returns:
			Expression instance
		"""
		
		return self.substitute(*g)
		
	def __isub__(self,e):
		"""Use the -= shortcut for subtraction and reassignment to the same pointer.
		
		Arguments:
			e: Expression instance, Line instance, Term instance, string, pair of integers, or integer
			
		Returns:
		Expression instance
		"""
		
		return self.subtract(e)
	
	def __lshift__(self,g):
		"""Use the << shortcut to substitute an expression.
		
		Arguments:
			g: tuple:
				0) pair of Line instances, or string
				1) string, name of variable with optional exponent
				
		Returns:
			Expression instance
		"""
		
		return self.substitute(*g)
	
	def __mul__(self,e):
		"""Use the * shortcut for multiplication.
		
		Arguments:
			e: Expression instance, Line instance, Term instance, tuple of integers, or integer
			
		Returns:
			Expression instance.
		"""
		
		# multiply
		m = self.multiply(e)
		
		return m
	
	def __neg__(self):
		"""Use the - shortcut for the additive inverse.
		
		Arguments:
			None
			
		Returns:
			Expression instance
		"""
		
		# take negative
		n = self.scale(-1)
		
		return n

	def __pos__(self):
		"""Use the + operator as a shortcut to view the line.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# view the line
		self.view()
		
		return None
	
	def __pow__(self,n):
		"""Use the ** shortcut for taking a power.
		
		Arguments:
			n: integer
			
		Returns:
			Expression instance
		"""
		
		# take power
		p = self.power(n)
		
		return p
	
	def __rshift__(self,g):
		"""Use the >> shortcut to substitute an expression.
		
		Arguments:
			g: tuple:
				0) pair of Line instances, or string
				1) string, name of variable with optional exponent
				
		Returns:
			Expression instance
		"""
		
		return self.substitute(*g)

	def __sub__(self,e):
		"""Use the - shortcut to subtract expressions.
		
		Arguments:
			e: Expression instance, Line instance, Term instance, string, pair of integers. or integer
			
		Returns:
			Expression instance
		"""
		
		# add negative
		s = self.subtract(e)
		
		return s
	
	def add(self,e):
		"""Add another Expression.
		
		Arguments:
			e: Expression instance, string, Line instance, Term instance, pair of integers, or integer
			
		Returns:
			Expression instance
		"""
		
		# A / B + C / D =
		# (A D + B C) / B D
		a = self.top()
		b = self.bottom()
		
		# convert to expression
		e = Ex(e)
		c = e.top()
		d = e.bottom()
		
		# if denominators are equal, add tops
		if b.compare(d):
			t = a.add(c)
			m = b.copy()
			
		# otherwise cross multiply
		else:
			f = a.multiply(d)
			g = b.multiply(c)
			t = f.add(g)
			m = b.multiply(d)
			
		# set bottom to one if top is zero
		z = Li(0)
		if t.compare(z):
			m = Li(1)
		
		# keep name of first
		n = self.name
		
		# append name of second
		if n and e.name:
			n = n + ' + ' + e.name
		
		# maintain subclass
		r = Ex(t,m,n)
		r.__class__ = self.__class__
		
		return r

	def apply(self,*a,**d):
		"""Apply specific function definitions to generic functions and their derivatives.
		
		Arguments:
			*a: unpacked tuple: 
				0) string, the variable to be replaced
				1) expresion or string denoting the replacement function
				2...) additional strings, names of any additional differentiable functions or coordinates to which the function applies
				
			**d: unpacked dictionary mapping functions or derivatives encountered to their expressions or strings representing their expressions
			
		Returns:
			Expression instance
			
		Notes:
			If the replacement expression is not given as a string, a string for the replacement expression must be in tuple a or it will not be differentiated.
			
		Examples:
			Consider the expression (F + Fx + Fxx + Fxy + Fxxy).  Consider replacing 'F' with e^u, where u is also some function of x and y.  One derivative rule is sufficient, i.e., d(e^u)/x = ux e^u.  
		
			This can be called with: 
				
				self.apply('F','eu','u',eux='ux eu').
			
			Even though derivation with respect to y is not given, it will be inferred from the parallel rule for x.  If this inference is not desired, differentiation by y may be suppressed by restricting e^u to be a function of x only:
				
				self.apply('F','eu','x','u',eux='ux eu').
				
			Suppose F = 'sinu'.  The derivative is ux cosu.  But for further differentiation, the derivative of cosu is also needed.  The derivative of cosu is -ux sinu.  Now the cycle is closed.  Call with:
			self.apply('F','sinu','cosu','u',sinux='ux cosu', cosux = '-ux sinu'). 
		"""
		
		# get arguments
		f = a[0]
		r = a[1]
		
		# add replacement to dictionary 
		d[f] = r
		
		# also add to beginning of function list if string
		try:
			if r.isalnum():
				a = list(a[1:])
		except AttributeError:
			a = list(a[2:])
		
		# convert dictionary strings to expressions
		for k,i in d.items():
			d[k] = Ex(i)
		
		# make list of partials
		v = self.scan(p=False)
		p = [i for i in v if i.startswith(f)]
		
		# build substitutions
		b = Ex._build(f,p,a,d)

		# substitute
		s = self
		for k in b:
			s = s.substitute(b[k],k)
			
		# maintain subclass
		s.__class__ = self.__class__
			
		return s

	def assimilate(self,*g,**f):
		"""Integrate a 3d plot along two dimensions.
		
		Arguments:
			*g: *args, unpacked tuple of: 
				0) string, name of variable
				1) if string, indicates a second variable. 
				1...) complex numbers or lists of numbers, by default (-2,-2) and (2,2).  Integers thereafter designate numbers of steps for the x and y axes, by default 64.
				2) boolean, plot graph? By default this is True.
				
			**f: **kwargs, unpacked dictionary mapping variables to functions or constants
			
		Returns:
			Page instance
		"""

		# get lists of solutions using sculpt
		s = self.sculpt(*g,**f)
		
		# assimilate
		t = s.assimilate()
			
		return t

	def bottom(self):
		"""Get the bottom Line of Terms.
		
		Arguments:
			None
			
		Returns:
			Line instance
		"""
		
		# bottom is second member
		b = self[1].copy()
		
		return b

	def compare(self,e):
		"""Test for equality between two expressions.
		
		Arguments:
			e: Expression instance or string
			
		Returns:
			boolean, expressions equal?
			
		Notes:
			Comparison is performed on a term by term basis, so two expressions that have terms in different orders will evaluate as false.
		"""
		
		# convert to Expression
		e = Ex(e)
		
		# check for top equality
		t = self.top()
		u = e.top()
		q = t.compare(u)
				
		# check for bottom equality
		if q:
			b = self.bottom()
			c = e.bottom()
			q = b.compare(c)
		
		return q
		
	def copy(self):
		"""Copy the expression.
		
		Arguments:
			None
			
		Returns:
			Expression instance
		"""
		
		# get attributes
		t = self.top()
		b = self.bottom()
		n = self.name
			
		# maintain subclass
		c = Ex(t,b,n)
		c.__class__ = self.__class__
			
		return c
		
	def derive(self,x,*f):
		"""Take the derivative.
		
		Arguments:
			x: string, variable name
			*f: unpacked tuple of strings, functions of variable x
			
		Returns:
			Expression instance
			
		Notes:
			When designating functions in list f, only the stem needs to be listed.  For instance, if f = ['F'], then F and all partials, i.e., 'Fx', 'Fy', 'Fxxy', will also be considered functions of x.  
			
			If f = ['c'], for instance, then any variable beginning with 'c' will be treated as a function of x, even if it is unrelated, such as 'cosu'.  However, if f = ['cosu'], then 'c' will not be treated as a function because it does not contain the entire stem.
			
		Examples:
			For expression (3x^2 + 2x + 1), the derivative is simply (6x + 2) via the power rule.
			
			For expression (3x^2 + 2x + F), where F is some function of x listed in f, the derivative is (6x + 2 + Fx), where Fx represents the partial derivative of F with respect to x, dF/dx.
			
			For expression (3x^2 + 2x F), the derivative is (6x + 2F + 2x Fx), by the product rule.
			
			For expression (3Fx + 2Fy), where partials are already present, the derivative is (3Fxx + 2Fyx), indicating second partial derivatives.
			
			For expression (3x^2 + 2) / (x - 1), where there is a divisor, the quotient rule applies: d/dx (F/G) = (FxG - FGx) / G^2 = ((6x)(x - 1) - (3x^2 + 2)(1)) / (x - 1)^2 = (3x^2 - 6x - 2) / (x^2 - 2x +1).
		"""
		
		# take derivative of top
		t = self.top()
		p = t.derive(x,*f)
		q = Li(1)
		
		# if bottom, apply quotient rule:
		# d/dx (t/b) = (tx b - t bx) / b^2
		o = Li(1)
		b = self.bottom()
		if not b.compare(o):
			d = b.derive(x,*f)
			u = b.multiply(p)
			v = t.multiply(d)
			p = u.subtract(v)
			q = b.multiply(b)
			
		# add prefix to name
		n = self.name
		if n:
			n = 'd/d%s %s' % (x,n)
			
		# result type mimics self
		r = Ex(p,q,n)
		r.__class__ = self.__class__
			
		return r
	
	def divide(self,e):
		"""Divide one expression by another.
		
		Arguments:
			e: Expression instance, Line instance, Term instance, pair of integers, or integer.
		
		Returns:
			Expression instance
		"""

		# convert to expression
		e = Ex(e)

		# invert, multiply, and revert
		v = self.invert()
		m = v.multiply(e)
		q = m.invert()
		
		# keep type
		q.__class__ = self.__class__
		
		# get divisor name
		try:
			a = e.name
		except:
			a = None
			
		# adjust name
		n = self.name
		if n and a:
			n = n + ' / ' + a
		q.name = n
		
		return q
				
	def draw(self,*g,**f):
		"""Draw a plot of the expression.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, name of independent variable
				1) number, left limit, defaults to -2.  
				2) number, right limit, defaults to 2.  
				3) number, steps, defaults to 64.
				4) boolean, view graph?, defaults to True.
				
			**f: unpacked dictionary mapping variables to numbers or function objects
			
		Returns:
			Book instance
		"""
		
		# distil booleans from *args
		g,u = Ex._distil(g)
				
		# independent variable
		x = g[0]
		
		# left limit
		try:
			a = complex(g[1])
		except:
			a = -2.0
			
		# right limit
		try:
			b = complex(g[2])
		except:
			b = 2.0
			
		# steps
		try:
			n = int(g[3])
		except:
			n = 64
		
		# get points
		p = Ex._points(a,b,n)
			
		# get results
		s = self.sample(x,p,**f)
			
		# show graph by default
		if False not in u:
			s.draw()
			
		return s
				
	def evaluate(self,**d):
		"""Evaluate the expression to a complex number.
		
		Arguments:
			**d: unpacked dictionary, maps variable names to numerical values.
			
		Returns:
			Result instance
		
		Notes:
			Any number type may be used in the dictionary.  They all get converted to complex numbers.
			
			If any variables are left without an entry in the dictionary, the evaluation is aborted.
		"""
		
		# evaluate top and bottom
		t = self.top().evaluate(**d)
		b = self.bottom().evaluate(**d)
		
		# divide
		c = t.divide(b)
		
		# attributes
		n = self.name
		s = self.jot()
		
		return Pa([c],n,s,d)

	def integrate(self,*g,**f):
		"""Integrate the expression to a value.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, name of independent variable
				1) number, left limit, defaults to -2.  
				2) number, right limit, defaults to 2.  
				3) number, steps, defaults to 64.
				4) boolean, view graph?, defaults to True.
				
			**f: unpacked dictionary mapping variables to numbers or function objects
			
		Returns:
			Page instance
		"""
		
		# get lists of solutions using draw
		s = self.draw(*g,**f)
		
		# integrate
		t = s.integrate()
			
		return t
		
	def invert(self):
		"""Invert an expression.
		
		Arguments:
			None
			
		Returns:
			Expression instance
		"""
		
		# make copies
		t = self.top()
		b = self.bottom()
		n = self.name
		if n:
			n = '1/' + n
	
		# reverse top, bottom
		v = Ex(b,t,n)
		
		# maintain equation
		v.__class__ = self.__class__
		
		return v
		
	def jot(self):
		"""Jot down an expression as a string.
		
		Arguments:
			None
			
		Returns:
			string
		"""
		
		# start with top expression
		t = self.top()
		s = t.jot()
		
		# if bottom is not trivial, add to string
		o = Li(1)
		b = self.bottom()
		if not b.compare(o):
			g = b.jot()
			s += ' / ' + g
		
		return s
		
	def multiply(self,e):
		"""Multiply by another expression.
		
		Arguments:
			e: Expression instance, Line instance, Term instance, pair of integers, or integer
			
		Returns: 
			Expression instance
		"""
		
		# convert to expression
		e = Ex(e)
			
		# multiply tops
		t = self.top()
		u = e.top()
		p = t.multiply(u)
		
		# multiply bottoms
		b = self.bottom()
		c = e.bottom()
		q = b.multiply(c)
		
		# get name from multiplier
		try:
			a = e.name
		except:
			a = None
			
		# adjust name
		n = self.name
		if n and a:
			n = n + ' * ' + a
		
		# pass on equation subclass
		m = Ex(p,q,n)
		m.__class__ = self.__class__
		
		return m
		
	def plug(self,y,x):
		"""Plug a term, variable, or number in for a variable.
		
		Arguments:
			y: Term instance, string, integer, or pair of integers
			x: string, name of replaced variable, possibly with its exponent
			
		Examples:
			In the expression (3x^2 + 5x + 2), plugging in '2z' for 'x' leads to (12z^2 + 10z + 2).
			
			Plugginf in '2z' for 'x2' leads to (6z + 5x + 2).  The single x remains unreplaced because the replacement was for x^2.
			
		Returns:
			Expression instance
		"""
		
		# replace top and bottom
		t = self.top().plug(y,x)
		b = self.bottom().plug(y,x)
		
		# keep name
		n = self.name
		
		# keep equation status
		r = Ex(t,b,n)
		r.__class__ = self.__class__
		
		return r
		
	def power(self,n):
		"""Take the expression to a power.
		
		Arguments:
			n: integer, an exponent
			
		Returns:
			Expression instance
		"""
		
		# make sure n is an integer
		n = int(n)
		
		# take top and bottom to power
		t = self.top().power(n)
		b = self.bottom().power(n)
		
		# if power is negative, invert expression
		if n < 0:
			t,b = b,t
			
		# keep name
		n = self.name
		
		# new expression
		w = Ex(t,b,n)
			
		# reinstate equation status
		w.__class__ = self.__class__
			
		return w

	def sample(self,*a,**f):
		"""Sample expression at every point given.
		
		Arguments:
			*a: unpacked tuple:
				0) string, variable to sample
				1) list of values for variable
				2) string, possible second variable
				3) value for second variable
				
			**f: unpacked dictionary, variable names mapped to values or function objects that evaluate to a value using x.
			
		Returns:
			Book instance
		"""
		
		# unpack args
		x = a[0]
		p = a[1]
		
		# retrieve secondary variable if present
		try:
			y = a[2]
			q = a[3]
		except:
			y = None
			q = None
		
		# evaluate results
		u = []
		for i in p:
			
			# reckon dictionary
			d = Ex._reckon(f,x,i,y,q)
			
			# evaluate
			u.append(self.evaluate(**d))
		
		# make book
		r = Bo(u,x)
				
		return r
		
	def scale(self,n,d=1):
		"""Scale the expression by a constant factor.
		
		Arguments:
			n: integer, numerator of scale factor
			d=1: denominator of scale factor
			
		Returns:
			Expression instance
		"""
		
		# scale top by numerator
		t = self.top().scale(n)
		
		# scale bottom by denominator
		b = self.bottom().scale(d)
		
		# keep name
		n = self.name
				
		# maintain equation 
		s = Ex(t,b,n)
		s.__class__ = self.__class__
				
		return s

	def scan(self,p=False):
		"""Get variables in expression.
		
		Arguments:
			p=True: boolean, print to screen?
			
		Returns:
			list of variables
		"""
		
		# get variables from top and bottom
		t = self.top().scan(p=False)
		b = self.bottom().scan(p=False)
		
		# parse into lower case, upper case
		l = []
		u = []
		for i in (t + b):
			if i[0].isupper():
				u.append(i)
			else:
				l.append(i)
				
		# remove duplicates and sort
		l = list(set(l))
		l.sort()
		u = list(set(u))
		u.sort()
		
		# combine lists
		v = l + u
		
		# print to screen
		if p: 
			s = ''
			for i in v:
				s += '%s,' % (i)
			print(s[:-1])
		
		return v

	def sculpt(self,*g,**f):
		"""Sculpt a 3d plot.
		
		Arguments:
			*g: *args, unpacked tuple of: 
				0) string, name of variable
				1) if string, indicates a second variable. 
				1...) complex numbers or lists of numbers, by default (-2,-2) and (2,2).  Integers thereafter designate numbers of steps for the x and y axes, by default 64.
				2) boolean, plot graph? By default this is True.
				
			**f: **kwargs, unpacked dictionary mapping variables to functions or constants
			
		Returns:
			Shelf instance
			
		Notes:
			This method allows the 3d plotting of an expression over the real axes of two variables or the complex plane of one variable.  The rectangular plotting area is specified by two corner points, the lower left and the upper right.
		"""
		
		# remove booleans from *args
		g,r = Ex._distil(g)
		
		# parse *args into strings and numbers
		s,n = Ex._segregate(g)
		
		# set first variable
		x = s[0]
		
		# set second variable
		try:
			y = s[1]
		except:
			y = None
		
		# set lower left corner as complex number
		try:
			a = Re(n[0],n[1])
		except:
			a = Re(-2,-2)
			
		# set upper right corner as complex number
		try:
			b = Re(n[2],n[3])
		except:
			b = Re(2,2)
			
		# set x-axis resolution
		try:
			p = int(n[4])
		except:
			p = 32
			
		# set y-axis resolution
		try:
			q = int(n[5])
		except:
			q = 32
			
		# calculate first axis points
		u = Ex._points(a.real,b.real,p)
			
		# calculate second axis points
		v = Ex._points(a.imag,b.imag,q)
		
		# loop through second axis to make shelf
		h = []
		for i in v:
			
			# progress tracker
			print('.', end='')
			
			# add to **kwargs
			# two real variables? 
			if y:
				f[y] = i
				w = u
				
			# one complex variable?
			else:
				w = [Re(j,i) for j in u]
				
			# evaluate for book
			if y:
				z = self.sample(x,w,y,i,**f)
			else:
				z = self.sample(x,w,**f)
			
			# put into list of books
			h.append(z)
			
		# end tracker
		print('\n')
			
		# make Shelf
		if not y:
			y = x
		h = Sh(h,y)
			
		# sculpt
		if False not in r:
			h.sculpt()
		
		return h

	def section(self,x):
		"""Section expression into one expression for every power of x
		
		Arguments:
			x: string, name of variable
			
		Returns:
			list of Expression instances
		"""
		
		# place terms into dictionary of lists keyed by power
		d = {}
		t = self.top()
		for i in t:
			p = i.look(x)
			
			# multiply out x
			v = Te({x:-p})
			if p not in d:
				d[p] = []
			d[p].append(i.multiply(v))
		
		# create expressions
		for k,i in d.items():
			l = Li(i)
			b = self.bottom()
			n = '%s%d' % (x,k)
			d[k] = Ex(l,b,n)
			
		# sort and make list
		y = sorted(d.keys())
		g = [d[k] for k in y]
		
		return g

	def simplify(self):
		"""Simplify an expression.
		
		Arguments:
			None
			
		Returns:
			Expression instance
			
		Notes:
			The greatest common factor is extracted from top and bottom.  If these two factors have common factors among them, they are cancelled out.
			
			Effectively this method removes all fractions and negative exponents.
		"""
		
		# factor top, T = A * B
		t = self.top()
		a,b = t.factor()
		
		# factor bottom, M = C * D
		m = self.bottom()
		c,d = m.factor()
		
		# get gcf for two gcfs
		f = Li([b,d],c=False)
		g = f.extract()
		
		# divide out gcf and make lists
		# B = G * P
		# D = G * Q
		p = Li([b.divide(g)])
		q = Li([d.divide(g)])
		
		# check to see if a = c
		if not a.compare(c):
			p = p.multiply(a)
			q = q.multiply(c)
		
		# retain name
		n = self.name
		
		return Ex(p,q,n)
		
	def substitute(self,s,x):
		"""Substitute an expression for a variable.
		
		Arguments:
			s: Expression instance or string, Line instance, Term instance, pair of integers or integer, substitutes for variable
			x: string, variable name with optional exponent
			
		Examples:
			Consider the expression (2x^2 + 3y - 5).  Substituting (z - 3) for 'x':
				
				self.substitute('z - 3','x')
				
			leads to (2z^2 -12z + 3y + 13).
				
			However, substituting (z - 3) for 'x2':
				
				self.substitute('z - 3','x2')
				
			leads to (2z + 3y - 11).
			
		Returns:
			Expression instance
		"""
		
		# convert expression
		s = Ex(s)
		
		# substitute top and bottom
		t = self.top().substitute(s,x)
		b = self.bottom().substitute(s,x)
		
		# divide
		w = Ex(t).divide(Ex(b))
			
		# keep name
		w.name = self.name
		
		# maintain equation subclass
		w.__class__ = self.__class__
			
		return w
			
	def subtract(self,e):
		"""Subtract one expression from another
		
		Arguments:
			e: Expression instance or string, Line instance, Term instance, pair of integers, or integet
			
		Returns:
			Expression instance
		"""
		
		# convert to Expression
		e = Ex(e)
		
		# scale by -1 and add
		n = e.scale(-1)
		s = self.add(n)
		
		# keep equation status
		s.__class__ = self.__class__
		
		# adjust name
		m = self.name
		a = e.name
		if m and a:
			m = m + ' - ' + a
		s.name = m
		
		return s
			
	def top(self):
		"""Get the top Line of Terms.
		
		Arguments:
			None
			
		Returns:
			Line instance
		"""
		
		# top is first member
		t = self[0].copy()
		
		return t

	def view(self):
		"""View the expression.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# print name
		if self.name:
			print(self.name + ' =')
			
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
			
		# spacer
		print(' ')
			
		return None
			
			
# Abbreviations
Ex = Expression


