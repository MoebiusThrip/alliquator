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

# import groups
import alliquator_groups as aq_gr
Gr = aq_gr.Group


# Chain, a specialized group 
class Chain(Gr):
	"""Chain is a group of expressions representing the results of a sequence of eliminations.
	
	Inherits from Group."""
	
	def __init__(self,g):
		"""Form a chain from a group.
		
		Arguments:
			g: Group instance
			
		Attributes:
			None
		"""
		
		# convert first expression to an equation
		q = Eq(g[0])
		self.append(q)
		
		# convert the rest to expressions
		for i in g[1:]:
			e = Ex(i)
			self.append(e)
			
	
	# instance methods
	def assimilate(self,*g,**f):
		"""Integrate all expressions along two axes after solving the top equation and propagating the results.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, variable to solve for
				1) string, name of variable to graph
				2) if string indicates a second variable. 
				2...) complex numbers or lists of numbers, by default (-2,-2) and (2,2).  Integers thereafter designate numbers of steps for the x and y axes, by default 16.
				5) boolean, view graph?, defaults to True
				6) boolean, crisp solutions?, defaults to False
				
			**f: unpacked dictionary mapping variables to functions or constants
			
		Returns:
			Case instance
			
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
	
	def draw(self,*g,**f):
		"""Draw a plot of the expressions after solving.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, name of variable to solve for
				1) string, name of independent variable
				2) number, left limit, defaults to -2.  
				3) number, right limit, defaults to 2.  
				4) number, steps, defaults to 64.
				5) boolean, view graph?, defaults to True.
				6) boolean, crisp solutions?, defaults to False
				
			**f: unpacked dictionary variables mapped to numbers or function objects
			
		Returns:
			Shelf instance
			
		Examples:
			For the equation (3xc^2 + 5xc + 2) = 0, setting v = 'c' will first solve the equation in terms of.  In this example, the equation is quadratic in c, so two solutions will be calculated at each point, and both will be plotted.  The return value will be a list of two lists of ComplexNumber instances because there are two possible solutions calculated at each point.
			
		Notes:
			All numerical solutions are in the form of complex numbers, so the real and imaginary parts of the solutions are plotted separately in related colors.
			
			Endpoints themselves of the drawing range are not actually calculated.  The range is broken into steps and the midpoint of each step is calculated.
		"""
		
		# distil booleans
		o = g
		g,u = Ex._distil(g)
		
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
		
		# if no v given, draw normal
		if not v:
			e = Gr(*self)
			r = e.draw(*o,**f)
			
			return r
		
		# get points
		p = Ex._points(a,b,n)
			
		# get results
		s = self
		if True in u:
			r = s.sample(v,x,p,True,**f)
		else:
			r = s.sample(v,x,p,**f)
			
		# draw graph to screen?
		if False not in u:
			r.draw()
		
		return r
		
	def integrate(self,*g,**f):
		"""Integrate a plot of the expressions after solving.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, name of variable to solve for
				1) string, name of independent variable
				2) number, left limit, defaults to -2.  
				3) number, right limit, defaults to 2.  
				4) number, steps, defaults to 64.
				5) boolean, view graph?, defaults to True.
				6) boolean, crisp solutions?, defaults to False
				
			**f: unpacked dictionary variables mapped to numbers or function objects
			
		Returns:
			Book instance
		"""
		
		# perform draw
		d = self.draw(*g,**f)
		
		# integrate
		t = d.integrate()
		
		return t
	
	def sample(self,*a,**f):
		"""Sample the chain at every point given, first solving the top equation and propagating the solutions through the rest of the expressions.
		
		Arguments:
			*a: unpacked tuple:
				0) string, variable to first solve for
				1) string, variable to sample at (independent variable)
				2) list of numbers, sampling points
				3) string, possible secondary sampling variable 
				4) number, value of secondary variable
				5) boolean, crisp solutions?, defaults to False
			
			**f: unpacked dictionary of function objects or numbers mapped to variable names to evaluate based on independent variable
			
		Returns:
			Shelf instance
			
		Examples:
			If the top equation is (3a^2x + 2ay - 1) = 0, solving first for 'a' will result in a quadratic, and hence two solutions per value of x. 
		  If the next expression is (b = 2a + x^2), each of the aforementioned solutions will used to calculate values of b, and onward down the chain.
		"""
		
		# distil booleans
		a,c = Ex._distil(a)
		
		# assume solving variable and two plotting variables
		try:
			v = a[0]
			x = a[1]
			p = a[2]
			y = a[3]
			q = a[4]
			
		# unless not enough *args, assume no solving variable
		except:
			try:
				v = None
				x = a[0]
				p = a[1]
				y = a[2]
				q = a[3]
				
			# or no secondary variable
			except:
				try:
					v = a[0]
					x = a[1]
					p = a[2]
					y = None
					q = None
					
				# or neither solving nor secondary variable
				except:
					v = None
					x = a[0]
					p = a[1]
					y = None
					q = None
		
		# if no v is given, sample like a normal group
		if not v:
			w = Gr(*self)
			z = w.sample(*a,**f)
			
			return z
		
		# return booleans
		if True in c:
			a += True,
		
		# otherwise solve and sample top equation
		t = self.pick(0).sample(*a,**f)
		
		# begin list of books on shelf
		h = [t]
		
		# go through all other expressions
		for i in self[1:]:
			
			# for each page in first book
			b = []
			for m,j in enumerate(t):
				
				# for each solution on page
				g = []
				for n,k in enumerate(j):
					
					# add inputs to dictionary
					f[v] = k
					f[x] = p[m]
					
					# check in books already made 
					for l in h[1:]:
						e = l.name
						f[e] = l[m][n]
						
					# evaluate
					d = Ex._reckon(f,x,p[m],y,q)
					u = i.evaluate(**d)
					g.append(u)
					
				# make book from list of evaluation pages
				o = Bo(g)
				
				# condense into one page
				g = Pa([k[0] for k in g])
				
				# get common attributes
				g.name = o.name
				g.source = o.source
				g.inputs = o.inputs
				
				# add to book
				b.append(g)
				
			# add book to list
			b = Bo(b,x)
			h.append(b)
			
		# make shelf
		h = Sh(h)
					
		return h
		
	def sculpt(self,*g,**f):
		"""Make a 3d plot of all expressions after solving the top equation and propagating the results.
		
		Arguments:
			*g: unpacked tuple: 
				0) string, variable to solve for
				1) string, name of variable to graph
				2) if string indicates a second variable. 
				2...) complex numbers or lists of numbers, by default (-2,-2) and (2,2).  Integers thereafter designate numbers of steps for the x and y axes, by default 16.
				5) boolean, view graph?, defaults to True
				6) boolean, crisp solutions?, defaults to False
				
			**f: unpacked dictionary mapping variables to functions or constants
			
		Returns:
			Case instance
			
		Notes:
			If three variables are given before **kwargs, the equation will be solved for the first and plotted against the real coordinates of the second and third variables.
			
			If two variables are given, the equation will be solved for the first variable and plotted against the complex plane of the second variable.
			
			If only one variable is given, the equation will be plotted against the complex plane of this variable without solving.
			
			Function objects are limited to being functions of the first variable.
		"""
		
		# distil booleans
		r = g
		g,u = Ex._distil(g)
		
		# check *args for strings
		s = []
		for i in g:
			
			# add to strings if all letters
			try:
				if i.isalpha():
					s.append(i)
				
			# otherwise pass
			except:
				pass
		
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
		
		# if no solving variable, sculpt as a normal group
		if not z:
			
			return Gr(*self).sculpt(*r,**f)
			
		# add False into *args to avoid plotting yet
		g += False,
		
		# add True for crisping
		if True in u:
			g += True,
			
		# solve top equation 
		t = self.pick(0).sculpt(*g,**f)
		
		# begin list of shelves on a case
		c = [t]
		
		# for each expression thereafter
		for i in self[1:]:
			
			# calculate a new shelf from each book
			h = []
			for m,j in enumerate(t):
				
				# from each page
				b = []
				for n,k in enumerate(j):
					
					# from each solution
					p = []
					for o,l in enumerate(k):
					
						# transfer inputs to **kwargs
						f[z] = l
						a = k.inputs[x]
						f[x] = a
						w = None
						if y:
							w = k.inputs[y]
							f[y] = w
					
						# check in shelves so far
						for e in c[1:]:
							f[e.name] = e[m][n][o]
						
						# evaluate
						d = Ex._reckon(f,x,a,y,w)
						d = i.evaluate(**d)
						p.append(d)
					
					# make book from list of pages
					q = Bo(p)
				
					# condense into one page
					v = Pa([l[0] for l in p])
				
					# get common attributes
					v.name = q.name
					v.source = q.source
					v.inputs = q.inputs
				
					# add to book
					b.append(v)
				
				# add book to shelf
				b = Bo(b,x)
				h.append(b)
			
			# add shelf to case
			if y:
				h = Sh(h,y)
			else:
				h = Sh(h,x)
			c.append(h)
			
		# make case
		c = Ca(c)
		
		# show graphs?
		if False not in u:
			c.sculpt()
					
		return c
		
		
# Abbreviation
Ch = Chain

		

