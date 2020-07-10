# alliquator_group.py
# classes to manipulate groups of algebraic expressions

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

# import cases
import alliquator_cases as aq_ca
Ca = aq_ca.Case

# import terms
import alliquator_terms as aq_te
Te = aq_te.Term

# import lines
import alliquator_lines as aq_li
Li = aq_li.Line

# import expressions
import alliquator_expressions as aq_ex
Ex = aq_ex.Expression

# import equations
import alliquator_equations as aq_eq
Eq = aq_eq.Equation


# Group class for groups of expressions
# Group of Expressions class
class Group (list):
	"""Group several expressions into one object.
	"""
	
	def __init__(self,*e):
		"""Group several expressions together.
		
		Arguments:
			*e: unpacked tuple of expressions, equations, or strings
			
		Attributes:
			None
		"""
		
		# load group
		for i in e:
			
			# convert from strings
			try:
				p = i.split('=')
				
				# if two parts, make equation
				try:
					i = Eq(p[0],p[1])
					
				# otherwise, expression
				except:
					i = Ex(p[0])
						
			# otherwise assume already equation or expression
			except:
				pass
			
			# append
			self.append(i)
		
		
	# instance methods
	def __ilshift__(self,g):
		"""Use the <<= shortcut to substitute an expression into every member of the group and reassign the pointer.
		
		Arguments:
			g: tuple:
				0) Expression instance, or string
				1) string, name of variable with optional exponent
				
		Returns:
			Group instance
		"""
		
		return self.substitute(*g)
		
	def __irshift__(self,g):
		"""Use the >>= shortcut to substitute an expression into every member of the group and reassign the pointer.
		
		Arguments:
			g: tuple:
				0) Expression instance, or string
				1) string, name of variable with optional exponent
				
		Returns:
			Group instance
		"""
		
		return self.substitute(*g)
	
	def __invert__(self):
		"""Use the ~ operator as a shortcut to simplify.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# simplify
		s = self.simplify()
		
		return s
	
	def __lshift__(self,g):
		"""Use the << shortcut to substitute an expression into every member of the group.
		
		Arguments:
			g: tuple:
				0) Expression instance, or string
				1) string, name of variable with optional exponent
				
		Returns:
			Group instance
		"""
		
		return self.substitute(*g)
	
	def __pos__(self):
		"""Use the + prefix as a shortcut to view.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# view
		self.view()
		
		return None
	
	def __rshift__(self,g):
		"""Use the >> shortcut to substitute an expression into every member of the group.
		
		Arguments:
			g: tuple:
				0) Expression instance, or string
				1) string, name of variable with optional exponent
				
		Returns:
			Group instance
		"""
		
		return self.substitute(*g)

	def apply(self,*a,**d):
		"""Apply specific function definitions to generic functions and their derivatives.
		
		Arguments:
			*a: unpacked tuple: 
				0) string, the variable to be replaced.  
				1) expresion or string denoting the replacement function. 
				2...) additional strings, names of any additional differentiable functions or their functionalities
				
			**d: unpacked dictionary mapping any new functions or derivatives encountered to their expressions or strings representing their expressions
			
		Returns:
			Group instance
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
		v = [j for i in v for j in i]
		p = set(v)
		p = [i for i in p if i.startswith(f)]
		
		# build derivatives
		b = Ex._build(f,p,a,d)
		
		# substitute
		s = self
		for k in b:
			s = s.substitute(b[k],k)
		s = Gr(*s)
			
		# transfer subclass
		s.__class__ = self.__class__
		
		return s
		
	def assimilate(self,*g,**f):
		"""Integrate all expressions along two axes.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, name of variable
				1) if string indicates a second variable. 
				2...) complex numbers or lists of numbers, by default (-2,-2) and (2,2).  Integers thereafter designate numbers of steps for the x and y axes, by default 64.
				3) boolean, view graph?
				
			**f: unpacked dictionary mapping variables to functions or constants
			
		Returns:
			Book instance
		"""
		
		# get lists of solutions using sculpt
		s = self.sculpt(*g,**f)
		
		# assimilate
		t = s.assimilate()
		
	def copy(self):
		"""Make a copy of the group.
		
		Arguments:
			None
			
		Returns:
			Group instance
		"""
		
		# make copy
		g = [i.copy() for i in self]
		g = Gr(*g)
		
		# transfer subclass
		g.__class__ = self.__class__
			
		return g
		
	def draw(self,*g,**f):
		"""Draw a plot of the expression.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, name of independent variable
				1) number, left limit, defaults to -2.  
				2) number, right limit, defaults to 2.  
				3) number, steps, defaults to 64.
				4) boolean, False indicates the graph is not to be viewed, defaults to True.
				
			**f: unpacked dictionary variables mapped to numbers or function objects
			
		Returns:
			Shelf instance
		"""

		# distil booleans
		h,b = Ex._distil(g)

		# draw all expressions
		r = []
		for n,i in enumerate(self):
			try:
				i = i.detach()
			except:
				pass
			if False not in b:
				print('%d:' % (n))
			p = i.draw(*g,**f)
			r.append(p)
		
		return Sh(r)

	def evaluate(self,**d):
		"""Evaluate all expressions in the group.
		
		Arguments:
			**d: unpacked dictionary mapping variables to number values.
			
		Returns:
			Page instance
		"""
		
		# put evaluations in a list
		m = [i.evaluate(**d) for i in self]
		
		return Bo(m)
		
	def extend(self,e):
		"""Extend the group with another expression.
		
		Arguments:
			e: Expression instance.
			
		Returns:
			Group instance
		"""
		
		# make copy
		s = self.copy()
		
		# try to convert if string
		try:
			p = e.split('=')
			
			# convert to equation
			try:
				e = Eq(p[0],p[1])
				
			# or expression
			except:
				e = Ex(p[0])
				
		# or assume expression already
		except:
			pass
				
		# make new group
		s.append(e)
		
		return s

	def integrate(self,*g,**f):
		"""Integrate the expression.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, name of independent variable
				1) number, left limit, defaults to -2.  
				2) number, right limit, defaults to 2.  
				3) number, steps, defaults to 64.
				4) boolean, False indicates the graph is not to be viewed, defauts to True.
				
			**f: unpacked dictionary mapping variables to numbers or function objects
			
		Returns:
			Page instance
			
		Notes:
			If the expression is quadratic or cubic in v, there will be multiple integration results, one for each sequence of solutions.
		"""
		
		# integrate all expressions
		t = []
		for i in self:
			s = i.integrate(*g,**f)
			t.append(s)
		
		return Bo(t,g[0])

	def jot(self):
		"""Jot down all expressions in the group as strings.
		
		Arguments:
			None
			
		Returns:
			list of strings
		"""
		
		# jot all
		l = [i.jot() for i in self]
		
		return l

	def pick(self,n):
		"""Pick a particular expression from s group.
		
		Arguments:
			n: index of particular expression
			
		Returns:
			Expression instance
		"""
		
		# retrieve expression
		p = self[n].copy()
		
		return p

	def plug(self,y,x):
		"""Plug in a variable, number, or term for a variable throughout the group.
		
		Arguments:
			y: string, Term instance, pair of integers, or integer
			x: string, name of variable to be replaced optionally with exponent

		Returns:
			Group instance
		"""
		
		# replace
		g = [i.plug(y,x) for i in self]
		g = Gr(*g)
		
		# transfer subclass
		g.__class__ = self.__class__

		return g

	def sample(self,*a,**f):
		"""Sample expression at every point given for all expressions in the group.
		
		Arguments:
			*a: unpacked tuple:
				0) string, variable to sample
				1) list of values for variable
				
			**f: unpacked dictionary: function objects or numbers mapped to variable names to evaluate based on  the dependent variable
			
		Returns:
			Shelf instance
		"""
		
		# evaluate results expression by expression
		r = []
		for i in self:
			try:
				i = i.detach()
			except:
				pass
			s = i.sample(*a,**f)
			r.append(s)
				
		# make Shelf
		r = Sh(r)
				
		return r

	def scan(self,p=False):
		"""List variables in each expression.
		
		Arguments:
			p=True: boolean: print to screen?
			
		Returns:
			list of lists of variables
		"""
		
		# list variables in each
		v = []
		for n,i in enumerate(self):
			l = i.scan(p=False)
			v.append(l)
			
			# print if designated
			if p:
				s = '%d: ' % (n)
				for j in l:
					s += '%s,' % (j)
				print(s[:-1])
			
		# spacer if necessary
		if p:
			print(' ')
		
		return v
		
	def sculpt(self,*g,**f):
		"""Sculpt a 3d plot.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, name of variable
				1) if string indicates a second variable. 
				2...) complex numbers or lists of numbers, by default (-2,-2) and (2,2).  Integers thereafter designate numbers of steps for the x and y axes, by default 64.
				3) boolean, view graph?
				
			**f: unpacked dictionary mapping variables to functions or constants
			
		Returns:
			Case instance
		"""
		
		# distil booleans
		a,b =Ex._distil(g)
		
		# sculpt all
		c = []
		for n,i in enumerate(self):
			
			# convert to expression()
			try:
				i = i.detach()
			except:
				pass
				
			# print header?
			if False not in b:
				print('%d: ' % (n))
			
			# sculpt
			h = i.sculpt(*g,**f)
			c.append(h)
			
		return Ca(c)
		
	def simplify(self):
		"""Simplify all expressions or equations in the group.
		
		Arguments:
			None
			
		Returns:
			Group instance.
		"""
		
		# simplify
		s = [i.simplify() for i in self]
		s = Gr(*s)
		
		# transfer subclass
		s.__class__ = self.__class__
		
		return s
		
	def substitute(self,b,x):
		"""Substitute an expression for all occurrences of a variable in the group.
		
		Arguments:
			b: Expression instance or expression string to substitute for x
			x: string, name of variable with optional power
			
		Returns:
			Group instance
		"""
		
		# substitute each one
		g = [i.substitute(b,x) for i in self]
		g = Gr(*g)
		
		# transfer subclass
		g.__class__ = self.__class__
		
		return g

	def view(self):
		"""View all expressions in the group.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# view all
		for n,i in enumerate(self):
			print('%d:' % (n))
			i.view()
			
		return None


# Abbreviation
Gr = Group


