# alliquator_lines.py
# class to manipulate lists of terms

# import results
import alliquator_results as aq_re
Re = aq_re.Result

# import pages
import alliquator_pages as aq_pa
Pa = aq_pa.Page

# import terms
import alliquator_terms as aq_te
Te = aq_te.Term

# import timing decorator
time_process = aq_re.time_process


# Line class
class Line (list):
	"""A Line is a list of Term instances
	
	Line class inherits from list.
	"""
	
	def __init__(self,l=None,c=True):
		"""Define a line as a list of Term instances.
		
		Arguments:
			l=None: string, list of Term instances, Term instance, number, or list of two numbers
			c=True: boolean, condense upon creation?
			
		Attributes:
			None
			
		Notes:
			If the line is defined by a string, separate terms must be separated by a space and + or -.  Omitting the space will be interpretted as an exponent.
			
			Condensation will add together compatible terms.
			
		Examples:
			The line (3x + (5/2)y^2 -2x y) is a list of 3 terms, 3x, (5/2)y^2, and -2x y.  It may be entered as the string:
				
				Li('3x +5/2y2 -2x y').
		"""
		
		# default None to zero
		if l is None:
			l = 0
			
		if l == []:
			l = 0
		
		# attempt to translate from string
		try:
			l = Li._translate(l)
			
		# otherwise try to make a Term in a list
		except:
			try:
				l = [Te(l)]
					
			# or assume already list of Terms
			except:
				l = [Te(i) for i in l]
			
		# condense?
		if c:
			l = Li._condense(l)
			
		# deposit terms, skip zeroes
		for i in l:
			if 0 not in i:
				self.append(i)
		
	
	# static methods
	@staticmethod
	def _condense(a,b=None):
		"""Condense two lists of terms into one list by adding the first into the second.
		
		Arguments:
			a: list of Term instances
			b=None: list of Term instances
			
		Returns:
			list of Term instances
		"""
		
		# second is by default empty
		if b is None:
			b = []
		
		# add first into second
		for i in a:
			
			# try to add onto all terms
			t = [i.add(j) for j in b]
			
			# check for match
			m = False
			for n,j in enumerate(t):
				if j is not None:
						
					# replace with combination
					b[n] = j
						
					# stop searching
					m = True
					break
				
			# otherwise append
			if not m:
				b.append(i)
			
			# remove zeroes
			zo = lambda x: 0 in x
			b = [i for i in b if not zo(i)]
			
		return b
		
		
	@staticmethod
	def _distribute(p,t):
		"""Distribute a number of exponents amongst a number of terms in all ways possible.
		
		Arguments:
			p: integer, exponent
			t: integer, number of terms
			
		Returns:
			list of tuples, the distributions
		"""
		
		# begin list with power
		l = [[p]]
		for i in range(t - 1):
			
			# expand the first members
			for n,j in enumerate(l):
				f = Li._fracture(j[0])
				
				# recombine with tails
				l[n] = [k + j[1:] for k in f]
			
			# unpack lists
			l = [k for j in l for k in j]
			
		# make tuples
		l = [tuple(i) for i in l]
				
		return l
			
	@staticmethod
	def _expand(l,p,d=None):
		"""Expand a list of terms taken to a power.
		
		Arguments:
			l: list of Term instances
			p: integer, power
			d=None: dictionary mapping tuples of exponents to calculated terms
			
		Returns:
			tuple:
				list of Term instances,
				dictionary mapping tuples of exponents to calculated terms
		"""
		
		# number of terms
		t = len(l)
		
		# make power positive
		p = abs(int(p))
		
		# return 1 if power is zero:
		if p == 0:
			
			return [{}],d
			
		# or return zero if length is zero
		if t < 1:
			
			return [],d
		
		# initiate dictionary
		if d is None:
			
			# begin with tuple of zeroes, i.e., all terms to the power of zero
			o = (0,) * t
			d = {o: Te(1)}
		
		# build matrix of each term
		m = []
		for i in range(t):
			
			# taken to each power
			r = []
			for j in range(p + 1):
				
				# make tuple
				o = [0] * t
				o[i] = j
				o = tuple(o)
				
				# try to find in dictionary
				try:
					x = d[o]
				
				# otherwise calculate and put in dictionary
				except:
					x = l[i].power(j)
					d[o] = x
				
				# put in matrix
				r.append(x)
				
			# add row
			m.append(r)
			
		# get permutations
		u = Li._distribute(p,t)
		
		# multinomial corfficient is p! / k1! k2! k3! ...
		# compute leading factorial
		f = Te.factorials
		try:
			a = f[p]
		except:
			a = fac(p)
			
		# compute terms
		w = []
		for i in u:
			
			# compute multinomial
			b = 1
			c = []
			for n,j in enumerate(i):
				
				# look for factorial or compute
				try:
					b *= f[j]
				except:
					b *= fac(j)
					
				# append term
				c.append(m[n][j])
			
			# multiply out term
			w.append(Te(a,b,*c))
		
		return w,d
		
	@staticmethod
	def _fracture(n):
		"""Fractute an integer into all possible pairs.
		
		Arguments:
			n: integer
			
		Returns:
			list of lists, combinations.
		"""
		
		# make all fractures
		f = []
		for i in range(n + 1):
			f.append([n - i, i])
			
		return f
		
	@staticmethod
	def _translate(s):
		"""Generate a list of Term instances from a string.
		
		Arguments:
			s: string
			
		Returns:
			list of Term instances
			
		Notes:
			The string for the expression generally follows this format: n/d ax by cz + n/d ax by cz, where n and d are the numerator and denominator of the coefficient, a,b,c represent variables, and x,y,z are their exponents.
			
			If the exponent of the variable is simply 1, it need not be explicitly stated.
			
			Generally spacing is optional.  However, because unspecified exponents default to 1, a space must be placed between separate variables in the same term or they will be translated as a single multi-lettered variable.  
			
			Also, separate terms must be indicated with a space followed by + or - to distinguish the beginning of a new term from a positive or negative exponent on the final variable of the previous term.
			
		Examples:
			The string '3/2 x2 y1 + 5/2 x1 y1 z1' is equivalent to '3/2 x2 y +5/2 x y z', or even '3/2x2y +5/2x y z', but not equuvalent to '3/2x2y+5/2xyz'.
		"""
		
		# new term is determined by a space followed by + or -
		# replace with _ and split into terms
		s = s.replace(' +','_+')
		s = s.replace(' -','_-')
		
		# split string into terms
		p = s.split('_')
		t = [Te(i) for i in p]
		
		return t
		
		
	#instance methods
	def __add__(self,l):
		"""Use the + shortcut for addition.
		
		Arguments:
			l: Line instance
			
		Returns:
			Line instance
		"""
		
		# add
		a = self.add(l)
		
		return a
	
	def __eq__(self,y):
		"""Use the == shortcut for comparison.
		
		Arguments:
			y: Line instance
			
		Returns:
			boolean, lines equal?.
		"""
	
		# compare
		q = self.compare(y)
			
		return q
	
	def __iadd__(self,l):
		"""Use the += shortcut for addition and reassignment to the same pointer.
		
		Arguments:
			l: Line instance, Term instance, string, pair of integers, or integer
			
		Returns:
			Line instance
		"""
		
		return self.add(l)
		
	def __imul__(self,l):
		"""Use the *= shortcut for multiplication and reassignment to the same pointer.
		
		Arguments:
			l: Line instance, Term instance, string, pair of integers, or integer
			
		Returns:
			Line instance
		"""
		
		return self.multiply(l)
	
	def __ipow__(self,n):
		"""Use the **= shortcut for exponentiation and reassignment to the same pointer.
		
		Arguments:
			n: integer, the exponent
			
		Returns:
			Line instance
		"""
		
		return self.power(n)
		
	def __irshift__(self,g):
		"""Use the >>= shortcut to plug in an integer, fraction, variable, or Term instance for another variable, and reassign the pointer.
		
		Arguments:
			g: tuple:
				0) Term instance, string, pair of integers, or integer
				1) string, name of variable with optional exponent
				
		Returns:
			Line instance
		"""
		
		return self.plug(*g)
		
	def __isub__(self,l):
		"""Use the -= shortcut for subtraction and reassignment to the same pointer.
		
		Arguments:
			l: Line instance, Term instance, string, pair of integers, or integer
			
		Returns:
		Line instance
		"""
		
		return self.subtract(l)
	
	def __lshift__(self,g):
		"""Use the << shortcut to substitute an expression.
		
		Arguments:
			g: tuple:
				0) pair of Line instances, or string
				1) string, name of variable with optional exponent
				
		Returns:
			list of Line instances
		"""
		
		return self.substitute(*g)
	
	def __mul__(self,l):
		"""Use the * shortcut for multiplication.
		
		Arguments:
			l: Line instance, Term instance, tuple of integers, or integer
			
		Returns:
			Line instance.
		"""
		
		# multiply
		m = self.multiply(l)
		
		return m
	
	def __neg__(self):
		"""Use the - shortcut for the additive inverse.
		
		Arguments:
			None
			
		Returns:
			Line instance
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
			Line instance
		"""
		
		# take power
		p = self.power(n)
		
		return p
	
	def __rshift__(self,g):
		"""Use the >> shortcut to plug in an integer, fraction, variable, or Term instance for another variable.
		
		Arguments:
			g: tuple:
				0) Term instance, string, pair of integers, or integer
				1) string, name of variable with optional exponent
				
		Returns:
			Line instance
		"""
		
		return self.plug(*g)
	
	def __sub__(self,l):
		"""Use the - shortcut to subtract lines.
		
		Arguments:
			l: Line instance, Term instance, string, pair of integers. or integer
			
		Returns:
			Line instance
		"""
		
		# add negative
		s = self.subtract(l)
		
		return s
	
	def add(self,l,s=True):
		"""Add two lines together.
		
		Arguments:
			l: Line instance, Term instance, pair of integers, or integer 
			s: boolean, sort terms afterward?
			
		Returns:
			Line instance
		"""
				
		# make line
		s = self.copy()
		l = Li(l)
		a = Li._condense(l,s)
		a = Li(a,c=False)
			
		# sort?
		if s:
			a = a.sort()
			
		return a
	
	def compare(self,l):
		"""Test whether two lines are equal.
		
		Arguments:
			l: Line instance
			
		Returns:
			boolean, lines equal?
		"""
		
		# assume equality
		q = True
		
		# test term by term
		for i,j in zip(self,l):
			
			# break at first mismatch
			if not i.compare(j):
				q = False
				break
				
		# make sure lengths are also equal
		if len(self) != len(l):
			q = False
				
		return q

	def copy(self):
		"""Copy a line.
		
		Arguments:
			None
			
		Returns:
			Line instance
		"""
		
		# copy list
		c = [i.copy() for i in self]
		
		return Li(c,c=False)

	def derive(self,x,*f):
		"""Take the derivative of all terms in a line.
		
		Arguments:
			x: string, variable name
			*f: unpacked tuple of strings, derivable function names
		
		Returns:
			Line instance
		"""
		
		# initiate zero line
		z = Li([])
		
		# derive term by term
		for i in self:
			d = i.derive(x,*f)
			z = z.add(d)
			
		return z

	def evaluate(self,**d):
		"""Evaluate a line to a complex number.
		
		Arguments:
			**d: unpacked dictionary mapping variables to numbers
			
		Returns:
			Result instance
		"""
		
		# evaluate terms
		v = [i.evaluate(**d) for i in self]
		
		# sum results
		c = Pa(v).sum()
		
		return c

	def extract(self):
		"""Extract the greatest common factor among a list of terms.
		
		Arguments:
			None
			
		Returns:
			Term instance
			
		Notes:
			This method seeks the lowest exponent among all terms of every variable or prime present.  If it is not present in every term, the lowest exponent is simply zero.  Less obviously, if there is a negative exponent present, it will be in the extracted greatest common factor because it is the lowest exponent.
			
		Examples:
			In the line (21 x^2 -42 i x + 14 x y), the greatest common factor is 7x.
			
			In the line (1/2 x + 3/2 y - 5/4 x^-1), the extracted greatest common factor is 1/4 x^-1, because x is present at exponents 1,0, and -1, so -1 is the lowest.  2 is present at exponents -1,-1,-2, so -2 is the lowest.  Hence 2^-2 * x^-1, or 1/4 x^-1.
		"""
		
		# create list
		s = self
		a = [k for i in s for k in i.keys()]
		a = set(a)
		
		# find minimum exponent 
		g = {}
		for i in a:
			h = [j.look(i) for j in s]
			m = min(h)
			if m != 0:
				g[i] = m
		g = Te(g)
		
		return g

	def factor(self):
		"""Factor out the greatest common factor among a line of terms.
		
		Arguments:
			None
			
		Returns:
			tuple:
				Line instance, factored terms,
				Term instance, greatest common factor
		"""
		
		# get gcf
		g = self.extract()
		
		# invert and multiply
		v = g.invert()
		f = self.multiply(v)
		
		return f,g

	def jot(self):
		"""Jot down a Line instance as an equivalent string.
		
		Arguments:
			None
			
		Returns:
			string
		"""
		
		# empty list?
		if len(self) < 1:
		
			return '(0)'
		
		# go through terms
		s = ''
		for i in self:
			
			# positive or negative
			if i.look('i') % 4 in (0,1):
				s += ' +('
			if i.look('i') % 4 in (2,3):
				s += ' -('
				
			# list of variables
			y = i.keys()
			y = [str(j) for j in y if j != 'i']
			y = [j for j in y if j.isalpha()]
			y = Pa._tidy(y)
				
			# coefficient
			n,d = i.fuse()
			if n > 1 or d > 1 or len(y) < 1:
				s += str(n)
			if d > 1:
				s += '/' + str(d)
			if i.look('i') % 4 in (1,3):
				s += 'i'
			
			# add variables to string
			for k in y:
				if s[-1] == '(':
					s += k
				else:
					s += ' ' + k
				if i[k] != 1:
					s += str(i[k])
					
			# close
			s += ')'
				
		# remove leading ' '
		if s[0] == ' ':
			s = s[1:]
				
		# remove leading +
		if s[0] == '+':
			s = s[1:]
				
		return s

	def multiply(self,l,s=True):
		"""Multiply a line by another line, term, integer, or fraction.
		
		Arguments:
			l: Line instance, Term instance, pair of numbers or number
			s=True: boolean, sort terms afterward?
			
		Returns:
			Line instance
		"""
		
		# convert to line
		l = Li(l,c=False)
		
		# new term list
		w = []
		
		# for every term in first
		for i in self:
				
			# multiply each member of second
			for j in l:
				
				# multiply together
				m = i.multiply(j)
				
				# append into new line
				w.append(m)

		# new line, condenses
		w = Li(w)
					
		# sort new line
		if s:
			w = w.sort()
		
		return w
		
	def plug(self,y,x):
		"""Plug in an integer, fraction, or term for all occurrences of a variable.
		
		Arguments:
			y: string, integer, Term instance, or pair of integers
			x: string, name of replaced variable with optional exponent
			
		Returns:
			Line instance
			
		Examples:
			To plug in 4/3 for all instances of x^2, use:
				
				self.plug((4,3),'x2')
		"""
		
		# replace
		l = [i.plug(y,x) for i in self]
		
		return Li(l)
		
	def power(self,p):
		"""Raise line to a power.
		
		Arguments:
			p: integer, the power
			
		Returns:
			Line instance
		"""
		
		# raise to power
		r,o = Li._expand(self,p)
		
		return Li(r)
		
	def scale(self,n,d=1):
		"""Scale all terms by a constant.
		
		Arguments:
			n: integer, numetator
			d=1: integer, denominator
			
		Returns:
			Line instance
		"""
		
		# scale all terms
		s = [i.scale(n,d) for i in self]
		
		return Li(s)

	def scan(self,p=False):
		"""Scan for all variables in a line of terms.
		
		Arguments:
			p=False: boolean, print to screen?
			
		Returns:
			list of strings, variable names
		"""
		
		# get variables from all terms
		v = []
		for i in self:
			a,b,c = i.parse()
			
			# add keys
			v += b.keys()
			
		# remove duplicates
		v = set(v)
		
		# sort into upper case, lower case
		l = []
		u = []
		for i in v:
			if i[0].isupper():
				u.append(i)
			else:
				l.append(i)
				
		# alphabetize and recombine
		l.sort()
		u.sort()
		v = l + u
		
		# print to screen if selected
		if p:
			s = ''
			for i in v:
				s += '%s, ' % (i)
			print(s[:-2])
		
		return v

	def sort(self):
		"""Sort a list of terms by variable and exponent.
		
		Arguments:
			None
			
		Returns:
			Line instance
		"""
		
		# get variables, add i
		v = self.scan(p=False)
		v.append('i')
		
		# reverse so least weighted variables come first
		v.reverse()
		
		# assign a weight to each variable, based on position in list
		w = {}
		for n,i in enumerate(v):
			w[i] = 1000 ** (n + 1)
			
		# assign score based on weights and exponents
		s = {}
		for i in self:
			
			# sum weights
			c = 0
			for k,j in i.items():
				
				# adjust weights based on exponent
				if k != 'i':
					c += w.get(k,0) * (100 + j)
					
				# i is adjusted based on even or odd exponents
				else:
					c += w.get(k,0) * (100 + j % 2)
					
			# use score as key
			s[c] = i
				
		# sort keys largest to smallest
		y = s.keys()
		y.sort()
		y.reverse()
		
		# new term list
		n = [s[k] for k in y]
		
		return Li(n,c=False)

	def subtract(self,l):
		"""Subtract from a Line instance.
		
		Arguments:
			l: Line instance, Term instance, pair of integers, or integer
			
		Returns:
			Line instance
		"""
		
		# convert to line
		l = Li(l)
		
		# scale by -1 and add
		l = l.scale(-1)
		s = self.add(l)
		
		return s

	def substitute(self,s,x):
		"""Substitute a list of Terms for a variable.
		
		Arguments:
			s: integer, string, Term instance, Line instance, or pair of Line instances.
			x: string, variable name with optional exponent
			
		Returns:
			List of two Line instances
			
		Notes:
			If a pair of Line instances is given, the first represents the numerator expression of the substitution and the second represents the denominator.
			
		Examples:
			If (y + 1) is to substitute for x:
				
				self.substitute('y + 1','x').
				
			If (y + 1) is to substitute for x^2:
				
				self.substitute('y + 1','x2').
		"""
		
		# turn substitution into top line
		try:
			t = Li(s)
			b = Li(1)
			
		# unless it is a list of lines
		except:
			t = Li(s[0])
			b = Li(s[1])
		
		# split variable from power
		h = Te._chop(x)
		x = h[0]
		
		# assume power of 1 for substituted variable, but revise if found in string
		p = 1
		try:
			p = int(h[1])
		except:
			pass
		
		# exponents in each term
		e = [i.look(x) for i in self]
		
		# adjust for power of substituted variable
		e = [i // p for i in e]
		
		# max, min powers of substitution
		try:
			a = max(e)
			m = min(e)
		except:
			a = 0
			m = 0
		
		# truncate max and min powers 
		if a < 0:
			a = 0
		if m > 0:
			m = 0
			
		# dictionaries of calculated terms for top and bottom
		f = {}
		g = {}
			
		# expand top and bottom to truncated max and min
		q,f = Li._expand(t,-m,f)
		r,g = Li._expand(b,a,g)
		q = Li(q,c=False)
		r = Li(r,c=False)
		
		# store results in dictionaries
		y = {-m: q}
		z = {a: r}
		
		# make denominator
		d = q.multiply(r)
		
		# convert each term
		l = Li([])
		for n,i in enumerate(self):
			
			# exponent of substitution
			w = e[n]
			
			# divide out variable
			v = Te({x: -w * p})
			i = i.multiply(v)
			
			# retrieve top expansion
			if (w - m) in y:
				u = y[w - m]
				
			# or calculate
			else:
				u,f = Li._expand(t,w - m,f)
				u = Li(u,c=False)
				y[w - m] = u
			
			# retrieve bottom expansion
			if (a - w) in z:
				c = z[a - w]
			
			# or calculate
			else:
				c,g = Li._expand(b,a - w,g)
				c = Li(c,c=False)
				z[a - w] = c
			
			# multiply and add
			u = u.multiply(c)
			u = u.multiply(i)
			l = l.add(u)
		
		return [l,d]

	def view(self):
		"""Display line term by term.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# add zero term
		t = self
		if t == []:
			t = [Te(0)]
		
		# display
		for i in t:
			i.view()
			
		# spacer
		print(' ')
			
		return None


# Abbreviaton
Li = Line



