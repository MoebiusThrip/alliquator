# alliquator_terms.py
# class to manipulate algebraic terms

# import math
import math
fac = math.factorial

# import results
import alliquator_results as aq_re
Re = aq_re.Result

# import timing decorator
time_process = aq_re.time_process


# Term class
class Term (dict):
	"""Manipulate an algebraic term.
	
	Term class inherits from dict.
	
	class attributes:
		primes: tuple of prime numbers
		factorials: list of factorials
	"""
	
	# prime numbers
	primes =  2,3,5,7,11,13,17,19,23,29,31
	primes += 37,41,43,47,53,59,61,67,71,73 
	primes += 79,83,89,97,101
	
	# factorials
	factorials = [fac(i) for i in range(10)]
	
	def __init__(self,*a,**w):
		"""Define a Term instance as a dictionary mapping variables or prime numbers to exponents.
		
		Arguments:
			*a: unpacked tuple of numbers, strings, tuples, or dictionaries.
			**w: unpacked dictionary, maps numbers or strings to integers
			
		Attributes:
			None
			
		Notes:
			Integers are broken into their prime factors with associated exponents.
			
			Negative numbers are represented using the imaginary unit squared, i^2.
			
			Variable names may be any number of letters, but no numbers or other symbols.
			
			Terms may be defined with varied arguments.  The first two numbers become the integer numerator and denominator of a fractional coefficient.  These numbers may be on their own or inside a tuple, or within a string separated by a a comma, space, or slash.
			
			Variables may be listed as separate strings or may be within a string.  A space or number must separate two variables, or they will be considered a single multi-letter variable.
			
			If no number follows a variable to indicate its exponent, an exponent of 1 is assumed. 
			
			If the same variable is listed in multiple places, the exponents will be combined.
			
		Examples:
			The term 28x^2 is represented as (2)^2 * (7)^1 * (x)^2, or as a dictionary of primes and variables: {2:2, 7:1, 'x':2}.  This could be entered as:
				
				Te(28,'x',2)
				
				or
				
				Te(28,x=2)
				
				or
				
				Te('28x2')
				
				or
				
				Te('28 x 2')
			
			The term (-3/16) x y^2 / z is represented as (i)^2 * (2)^-4 * (3)^1 * (x)^1 * (y)^2 * (z)^-1, or as a dictionary of primes and variables: {'i':2, 2:-4, 3:1, 'x':1, 'y':2, 'z':-1}.  This could be entered as:
				
				Te(-3,16,x=1,y=2,z=-1)
				
				or
				
				Te((-3,16),'x','y',2,'z',-1)
				
				or
				
				Te('3/16x y2 z-1')
				
				or
				
				Te('3 16 x y 2 z -1')
		"""
		
		# begin dictionary
		d = {}
		
		# deposit **kwargs into dictionary
		for k,i in w.items():
			
			# only accept integer exponents
			try:
				i = int(i)
				d[k] = d.get(k,0) + i
			except:
				pass
				
		# look for dictionaries in *args
		s = []
		for i in a:
			
			# deposit if dictionary
			try:
				for k,j in i.items():
					
					# only accept integers
					try:
						j = int(j)
						d[k] = d.get(k,0) + j
					except:
						pass
						
			# otherwise test for strings
			except:
				
				# remove / and ,
				try:
					i = i.replace('/',' ')
					i = i.replace(',',' ')
					s.append(i)
					
				# otherwise test for integers
				except:
					
					# make integer into string
					try:
						i = int(i)
						s.append(str(i))
						
					# otherwise assume composite
					except:
						
						# and search for integers
						try:
							for j in i:
								j = int(j)
								s.append(str(j))
									
						# or raise type error
						except:
							raise TypeError
				
		# extract from strings
		if s:
			
			# join and chop
			s = ' '.join(s)
			s = Te._chop(s)
				
			# make coefficients
			c = Te._coefficients(s)
			for k,i in c.items():
				d[k] = d.get(k,0) + i
			
			# make variables
			v = Te._variables(s)
			for k,i in v.items():
				d[k] = d.get(k,0) + i
			
		# filter
		d = Te._filter(d)
		
		# put keys into Term
		for k,i in d.items():
			self[k] = i
			
	
	# static methods
	@staticmethod
	def _chop(g):
		"""Chop string into strings of letters or numbers.
		
		Arguments:
			g: string
			
		Returns:
			list of strings
			
		Notes:
			Only letters, numbers, or +,-,. will be passed on.
		"""
		
		# allowed symbols
		y = ('+','-','.')
		
		# split string by spaces
		p = g.split()
		
		# segregate letters and numbers
		l = []
		for i in p:
			s = ''
			a = False
			
			# examine characters
			for j in i:
				
				# combine alphas
				if j.isalpha():
					
					# continue adding alphas
					if a:
						s += j
						
					# or start new alpha chunk
					else:
						l.append(s)
						s = j
						a = True
						
				# or combine nonalphas
				else:
					
					# continue adding digits
					if not a:
						if j.isdigit() or j in y:
							s += j
					
					# or start new digit chunk
					else:
						l.append(s)
						if j.isdigit() or j in y:
							s = j
						else:
							s = ''
						a = False
						
			# append final chunk
			l.append(s)
			
		# remove empty strings
		l = [i for i in l if i != '']
			
		return l
			
	@staticmethod
	def _coefficients(l):
		"""Create a prime factors dictionary from coefficient strings.
		
		Arguments:
			l: list of strings
			
		Returns:
			dictionary mapping prime factors to exponents.
		"""
		
		# peel off pre-letter strings
		p = []
		for i in l:
			if i.isalpha():
				break
			else:
				p.append(i)
				
		# pad with extra ones in case of only + or -
		p += ['1'] * 4
		
		# convert to integers
		n = []
		s = ''
		for i in p:
			
			# make an integer
			try:
				n.append(int(float(s + i)))
				s = ''
				
			# or keep to stick on the next
			except ValueError:
				
				# unless one is already saved
				if s:
					s = ''
				else:
					s = i
					
		# prime factor numerator from first
		c = Te._prime(n[0])
		
		# prime factor denominator from second and flip
		d = Te._prime(n[1])
		d = Te._flip(d)
		
		# combine exponents
		for k,i in d.items():
			c[k] = c.get(k,0) + i
				
		return c
			
	@staticmethod
	def _filter(d):
		"""Filter out extraneous keys from the dictionary.
		
		Arguments:
			d: dictionary
			
		Returns:
			dictionary 
		"""
		
		# filter
		f = {}
		
		# check for zero
		if 0 in d and d[0] != 0:
			
			# return zero if divided by zero
			if d[0] < 0:
				print('Division by zero not allowed!\n')
			
			return {0:1}
		
		# otherwise filter
		p = Te.primes
		for k,i in d.items():
			
			# reduce imaginary unit
			if k == 'i':
				i = i % 4
		
			# skip zero exponents
			if i != 0:
				
				# variables
				try:
					if k.isalpha():
						f[k] = i
						
				# prime numbers
				except AttributeError:
					if k in p:
						f[k] = i
						
					# or big numbers
					elif k > p[-1]:
						f[k] = i
		
		return f
			
	@staticmethod
	def _flip(d):
		"""Flip all exponents in dictionary to their negatives.
		
		Arguments:
			d: dictionary of exponents
			
		Returns:
			dictionary
		"""
		
		# flip exponents
		f = {}
		for k,i in d.items():
			f[k] = -i
		
		return f
			
	@staticmethod
	def _prime(n):
		"""Factor integer into primes.
		
		Arguments:
			n: integer
			
		Returns:
			dictionary mapping prime factors to exponents
		"""
			
		# default to 1 for noninteger
		try:
			n = int(n)
		except TypeError:
			n = 1
	
		# check for zero
		if n == 0:
			
			return {0:1}
	
		# primes
		p = Te.primes
		
		# begin dictionary of prime factors
		f = {}
		
		# change -1 into i^2
		if n < 0:
			f['i'] = 2
			n = abs(n)
		
		# scan through primes
		for i in p:
			
			# until prime bigger than dividend
			if i > n:
				break
				
			# divide out primes, add to factors
			while n % i == 0:
				n /= i
				f[i] = f.get(i,0) + 1
			
		# add remainder as its own entry
		if n > 1:
			f[n] = 1
				
		return f
	
	@staticmethod
	def _variables(l):
		"""Extract variables and their exponents from a list of strings.
		
		Arguments:
			l: list of strings
			
		Returns:
			dictionary mapping variables to exponents.
		"""
		
		# variables begin with first lettered string
		s = []
		a = False
		for i in l:
			if i.isalpha():
				a = True
			if a:
				s.append(i)
				
		# make pairs dictionary
		p = {}
		v = None
		for i in s:
			
			# give variables a default exponent of one
			if i.isalpha():
				p[i] = 1
				v = i
				
			# but revise upon encountering a nonletter string
			else:
				try:
					p[v] = int(i)
					
				# unless it cannot be made into an integer
				except:
					pass
					
		return p
	
	# instance methods
	def __add__(self,t):
		"""Use the + shortcut for addition.
		
		Arguments:
			t: Term instance
			
		Returns:
			Term instance, or
			None if incompatible
		"""
		
		# add
		a = self.add(t)
		
		return a
	
	def __div__(self,t):
		"""Use the / shortcut for division.
		
		Arguments:
			t: Term instance, tuple of integers, or integer
			
		Returns:
			Term instance
		"""
		
		# divide
		d = self.divide(t)
		
		return d
	
	def __iadd__(self,t):
		"""Use the += shortcut for addition and reassignment to the same pointer.
		
		Arguments:
			t: Term instance, string, pair of integers, or integer
			
		Returns:
			Term instance
		"""
		
		return self.add(t)
		
	def __idiv__(self,t):
		"""Use the /= shortcut for division and reassignment to the same pointer.
		
		Arguments:
			t: Term instance, string, pair of integers, or integer
			
		Returns:
			Term instance
		"""
		
		return self.divide(t)
		
	def __imul__(self,t):
		"""Use the *= shortcut for multiplication and reassignment to the same pointer.
		
		Arguments:
			t: Term instance, string, pair of integers, or integer
			
		Returns:
			Term instance
		"""
		
		return self.multiply(t)
	
	def __invert__(self):
		"""Use the ~ shortcut for inversion.
		
		Arguments:
			None
			
		Returns:
			Term instance
		"""
		
		# invert
		v = self.invert()
		
		return v
	
	def __ipow__(self,n):
		"""Use the **= shortcut for exponentiation and reassignment to the same pointer.
		
		Arguments:
			n: integer, exponent
			
		Returns:
			Term instance
		"""
		
		return self.power(t)
		
	def __irshift__(self,g):
		"""Use the >>= shortcut to plug in an integer, fraction, variable, or Term instance for another variable, and reassign the pointer.
		
		Arguments:
			g: tuple:
				0) Term instance, string, pair of integers, or integer
				1) string, name of variable with optional exponent
				
		Returns:
			Term instance
		"""
		
		return self.plug(*g)
		
	def __isub__(self,t):
		"""Use the -= shortcut for subtraction and reassignment to the same pointer.
		
		Arguments:
			t: Term instance, string, pair of integers, or integer
			
		Returns:
			Term instance
		"""
		
		return self.subtract(t)
	
	def __mul__(self,t):
		"""Use the * shortcut for multiplication.
		
		Arguments:
			m: Term instance, tuple of integers, or integer
			
		Returns:
			Term instance.
		"""
		
		# multiply
		m = self.multiply(t)
		
		return m
	
	def __neg__(self):
		"""Use the - shortcut for the additive inverse.
		
		Arguments:
			None
			
		Returns:
			Term instance
		"""
		
		# take negative
		n = self.scale(-1)
		
		return n

	def __pos__(self):
		"""Use the + operator as a shortcut to view the term.
		
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
			Term instance
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
			Term instance
		"""
		
		return self.plug(*g)
	
	def __sub__(self,t):
		"""Use the - shortcut to subtract terms.
		
		Arguments:
			t: Term instance
			
		Returns:
			Term instance, or
			None if incompatible
		"""
		
		# add negative
		s = self.subtract(t)
		
		return s
	
	def add(self,t):
		"""Add two terms if they are compatible.
		
		Arguments:
			t: Term instance
			
		Returns:
			Term instance, or
			None if not compatible
		"""
		
		# convert to term
		t = Te(t)
		
		# check for zero in self
		if 0 in self:
			
			return t.copy()
			 
		# check for zero in added term
		if 0 in t:
			
			return self.copy()
		
		# parse term into numbers, variables, and imaginary unit
		u,v,w = self.parse()
		x,y,z = t.parse()
		
		# test variables for equality
		if not v.compare(y):
			
			return None
			
		# test for equal or opposite imaginary units
		g = abs(w.look('i') - z.look('i'))
		if g % 2 != 0:
			
			return None
			
		# make fractions
		b,c = u.fuse()
		p,q = x.fuse()
				
		# cross-multiply and add or subtract to get nunerator, depending on i
		if g == 0:
			n = (b * q) + (p * c)
		if g == 2:
			n = (b * q) - (p * c)
			
		# new denominator
		d = c * q
			
		# retain variables and imaginary unit 
		a = Te(n,d,v,w)
		
		return a

	def compare(self,t):
		"""Compare two Term instances for equality.
		
		Arguments:
			t: Term instance
		
		Returns:
			boolean, terms equal?
		"""
		
		# compare terms
		q = False
		if cmp(self,t) == 0:
			q = True
		
		return q
	
	def copy(self):
		"""Copy the Term instance.
		
		Arguments:
			None
			
		Returns:
			Term instance.
		"""
		
		return Te(self)
		
	def derive(self,x,*f):
		"""Take the derivative.
		
		Arguments:
			x: string, the deriving variable
			*f: unpacked tuple of strings, other derivable functions of x
			
		Returns:
			list of Term instances
			
		Examples:
			Deriving the term (3x^2) with respect to x is 6x by the power rule.
			
			Deriving the term (3x^2 F) with respect to x, where F is a function of x, is (6x F + 3x^2 Fx) by the product rule.  Fx represents the partial derivative of F with respect to x, or dF/dx.  'F' must be included in the *args, or it will be assumed a nonfunction of x.
		"""

		# new term list
		w = []
		
		# power rule for x if present
		p = self.look(x)
		if p != 0:
			
			# multiply by exponent and reduce exponent of variable
			t = Te(p,self,{x:-1})
			w.append(t)
		
		# product rule generates new term for every function of x
		v = self.parse()[1]
		for i in v:
			
			# check for stems
			s = [i.startswith(j) for j in f]
			if True in s:
				p = self.look(i)
				if p != 0:
					
					# multiply by exponent, reduce exponent of stem, and add subscripted stem
					t = Te(p,self,{i:-1, i + x:1})
					w.append(t)
			
		return w
	
	def divide(self,t):
		"""Divide the Term instance by another Term instance, fraction, or integer:
			
		Arguments:
			t: Term instance, tuple of integers, or integer
				
		Returns:
			Term instance
		"""
		
		# invert self, multiply, revert
		v = self.invert()
		d = v.multiply(t)
		d = d.invert()
		
		return d

	def evaluate(self,**d):
		"""Evaluate the Term instance to a complex number (Result instance).
		
		Arguments:
			**d: unpacked dictionary, maps variable names to numerical values.
			
		Returns:
			Result instance
		
		Notes:
			Any number type may be used in the dictionary.  They all get converted to complex numbers.
			
			If any variables are left without an entry in the dictionary, the evaluation is aborted.
		"""
				
		# add imaginary unit to dictionary
		d['i'] = Re(0,1)
				
		# parse term, recombine variables and imaginary
		n,v,m = self.parse()
		v = Te(v,m)
		
		# multiply in variables
		c = Re(1)
		for k,i in v.items():
			
			# catch missing keys
			try:
				r = Re(d[k])
				c = c.multiply(r.power(i))
			except:
				print('Not all variables accounted for, evaluation aborted.\n')
					
				raise ValueError('Not all variables accounted for, evaluation aborted.\n')
					
		# make fraction
		f,g = n.fuse()
		c = c.multiply(Re(f))
		c = c.divide(Re(g))
					
		return c

	def fuse(self):
		"""Fuse prime factors into a fraction.
		
		Arguments:
			None
			
		Returns:
			tuple:
				integer, numerator,
				integer, denominator
		"""
		
		# check for zero
		if 0 in self:
			
			return 0,1
		
		# make numerator and denominator
		n = 1
		d = 1
		for k,i in self.items():
			
			# integer atoms
			try:
				if i < 0:
					d *= k ** -i
				else:
					n *= k ** i
						
			# ignore non number atoms
			except:
				pass
					
		return n,d
	
	def invert(self):
		"""Invert the Term instancr.
		
		Arguments:
			None
			
		Returns:
			Term instance
		"""
		
		# flip and filter
		v = Te._flip(self)
		v = Te._filter(v)
		
		return Te(v)
	
	def look(self,k):
		"""Look up the exponent associated with a variable or prime.
		
		Arguments:
			k: integer or string keyword
			
		Returns:
			integer: exponent of variable or prime in Term instance
		"""
		
		# get exponent, default to zero
		p = self.get(k,0)
		
		return p
	
	def multiply(self,t):
		"""Multiply by another Term instance, fraction, or integer.
			
		Arguments:
			t: Term instance, tuple of integers, or integer
				
		Returns:
			Term instance
		"""
		
		# make new term from elements
		m = Te(t,self)
				
		return m
		
	def parse(self):
		"""Parse Term instance into numbers, variables, and imaginary unit.
		
		Arguments:
			None
			
		Returns:
			tuple:
				Term instance for numbers,
				Term instance for variables,
				Term instance for imaginary unit
		"""
		
		# initiate dictionaries for numbers, variables, and imaginary unit
		n = {}
		v = {}
		m = {}
		
		# parse powers
		for k,i in self.items():
				
			# segregate numbers
			try:
				k = int(k)
				n[k] = i
					
			# and variables
			except:
				if k == 'i':
					m[k] = i
				else:
					v[k] = i
				
		return Te(n),Te(v),Te(m)
		
	def plug(self,y,x):
		"""Plug in a Term instance, fraction, or integer for a variable.
		
		Arguments:
			y: Term integer, tuple of integers, integer, or string
			x: string, name and power of replaced variable
			
		Returns:
			Term instance
			
		Examples:
			If the term is (5x^3), and 'x' is to be replaced by 'z', the result will be (5z^3).
			
			If the term is (5x^3), and 'x2' is to be replaced by 'z', the result will be (5x z), because z is replacing x^2, and there were not enough x's for two full replacements.
		"""
		
		# split variable from power
		s = Te._chop(x)
		x = s[0]
		
		# assume power of 1 for replacement, but revise if found in string
		p = 1
		try:
			p = int(s[1])
		except:
			pass
		
		# get power of variable in term
		n = self.look(x)
		
		# calculate power of replacement
		w = n // p
		
		# make replacing term
		r = Te(y).power(w)
		
		# combine with inverted variable taken to appropriate power
		t = Te(self, r, {x: -w * p})
		
		return t
		
	def power(self,n):
		"""Raise the Term instance to a power.
		
		Arguments:
			n: integer
			
		Returns:
			Term instance
		"""
		
		# multiply all exponents
		p = {}
		n = int(n)
		for k,i in self.items():
			p[k] = i * n
			
		return Te(p)
		
	def scale(self,n,d=1):
		"""Scale the term by a constant.
		
		Arguments:
			n: integer, numerator
			d=1: integer, denominator
			
		Returns:
			Term instance
		"""
		
		# multiply for new term
		s = self.multiply((n,d))
		
		return s

	def subtract(self,t):
		"""Subtract another Term instance from the Term instance if they are compatible.
		
		Arguments:
			t: Term instance, string, pair of integers, or integer
			
		Returns:
			Term instance, or
			None if not compatible
		"""
			
		# convert to term
		t = Te(t)
			
		# scale by -1 and add
		t = t.scale(-1)
		s = self.add(t)
		
		return s

	def view(self):
		"""View the term in readable form.
		
		Arguments:
			None
		
		Returns:
			None
		"""
		
		# begin string
		s = '('
			
		# check for zero
		if 0 in self:
			s += '0)'
			print(s)
			
			return None
		
		# parse term into numbers, variables, imaginay unit
		b,v,m = self.parse()
		
		# create numerator, denominator
		n,d = b.fuse()
		
		# add negative?
		m = m.look('i')
		if m % 4 in (2,3):
			s += '-'
			
		# add numerator
		s += '%d' % (n)
		
		# add denominator?
		if d > 1:
			s += '/%d' % (d)
		s += ')'
		
		# add imaginary unit?
		if m % 4 in (1,3):
			s += 'i'
		s += ' '
		
		# parse variables into upper, lower case
		l = []
		u = []
		for k in v:
			if k[0].isupper():
				u.append(k)
			else:
				l.append(k)
				
		# sort alphabetically 
		l.sort()
		u.sort()
		
		# add variables to string
		for k in (l + u):
			s += '%s' % (k)
			i = v.look(k)
			if i != 1:
				s += '%d' % (i)
			s += ' '
		
		# print string
		print(s)
		
		return None


# Abbreviation
Te = Term

