# alliquator_books.py
# manipulations of lists calculation results

# import math
import math
log = math.log10
sqrt = math.sqrt

# import plotting
import matplotlib.pyplot as plt

# import results
import alliquator_results as aq_re
Re = aq_re.Result
time_process = aq_re.time_process

# import pages
import alliquator_pages as aq_pa
Pa = aq_pa.Page
 
 
# Class for a list of pages of results
class Book(list):
	"""A Book instance is a list of Page instances, representing multiple evaluations of an expression or a single evaluations of multiple expressions.
	
	Book class inherits from list.
	"""
	
	def __init__(self,l=None,x=None):
		"""Define a Book instance as a list of Page instances.
		
		Arguments:
			l=None: list of Page instances
			x=None: string, name of independent variable
			
		Attributes:
			axis: string, independent variable
			inputs: dictionary mapping variables to values
			name: string, name for results
			source: string, expression from which evaluation is made

		"""
		
		# fill in pages
		if l:
			for i in l:
				self.append(i)
		
		# axis
		self.axis = None
		if x:
			self.axis = x
		
		# name is common name 
		n = None
		if l:
			n = self[0].name
			t = [i.name == n for i in self]
			if False in t:
				n = None
		self.name = n
			
		# source is common source
		r = None
		if l:
			r = self[0].source
			t = [i.source == r for i in self]
			if False in t:
				r = None
		self.source = r
		
		# get all input keys
		y = []
		for i in self:
			y += i.inputs.keys()
		y = set(y)
		
		# check for common inputs
		c = {}
		s = self
		for k in y:
			u = s[0].inputs.get(k,0)
			t = [j.inputs.get(k,0) for j in s]
			t = [Re(j) == Re(u) for j in t]
			if not False in t:
				c[k] = u
				
		# assign to inputs
		self.inputs = c
		
		
	# static methods
	@staticmethod
	def _flatten(l):
		"""Calculate the total flatness from a list of lists of curvatures.
		
		Arguments:
			l: list of lists of complex numbers, curvatures
			
		Returns:
			float, flatness
		"""
		
		# flatness = [1/(1 + r) + 1/(10 + m)]
		f = 0.0
		
		# go through each member
		for i in l:
			
			# sum curvatures
			u = Pa(i)
			u = u.sum()
			
			# real flatness
			f += 1.0 / (1.0 + u.real)
			
			# imaginary flatness, weighted less
			f += 1.0 / (10.0 + u.imag)
			
		return f
		
	# instance methods
	def __pos__(self):
		"""Use the + prefix to view the page.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# view
		self.view()
		
		return None
		
	def __repr__(self):
		"""Create string for representing object on screen.
		
		Arguments:
			None
			
		Returns:
			string
		"""
		
		return '<Book object>'
		
	def copy(self):
		"""Copy the book.
		
		Arguments:
			None
			
		Returns:
			Book instance
		"""
		
		# copy each page
		c = [i.copy() for i in self]
		
		# transfer attributes
		c = Bo(c,self.axis)
		c.name = self.name
		c.source = self.source
		c.inputs = self.inputs
		
		return c
		
	def deposit(self,l):
		"""Deposit a list of strings from a file into an empty book.
		
		Arguments:
			l: list of strings
			
		Returns:
			None
		"""
		
		# reverse list
		l.reverse()
		
		# get axis, skipping header
		p = l.pop()
		p = l.pop()
		if p != '___':
			self.axis = p
		
		# get name, skipping header
		p = l.pop()
		p = l.pop()
		if p != '___':
			self.name = p
		
		# get source, skipping header
		p = l.pop()
		p = l.pop()
		if p != '___':
			self.source = p
			
		# get inputs, skipping header
		p = l.pop()
		p = l.pop()
		while p != 'pages:':
			self.inputs[p] = Re(l.pop())
			p = l.pop()
		
		# get pages
		g = []
		a = []
		while len(l) > 0:
			
			# next element
			p = l.pop()
			
			# begin new page if header found
			if p.startswith('[page'):
				if a:
					g.append(a)
				a = []
				
			# otherwise add next element
			else:
				a.append(p)
				
		# add final page
		g.append(a)
		
		# deposit pages
		for i in g:
			e = Pa()
			e.deposit(i)
			self.append(e)
		
		return None
		
	def draw(self):
		"""Draw a plot of results in the Book.
		
		Arguments:
			None
			
		Returns:
			None
			
		Notes:
			The graph is project along the real axis of the independent variable unless there is greater spread along the imaginary axis, in which case the drawing is projected along the imaginary.
		"""
		
		# plot colors
		c = ['r-','g-','b-','m-']
		d = ['r--','g--','b--','m--']
		l = len(c)
		
		# get axis if present
		a = self.axis
		if not a:
			print('No axis variable available.  Draw aborted.\n')
			
			return None
			
		# find independent variable points
		p,y = self.project()
		
		# transpose data to get lists of continuous points
		t = [i for i in zip(*self)]
		
		# draw each
		for n,i in enumerate(t):
			r = [j.real for j in i]
			g = [j.imag for j in i]
			plt.plot(p,r,c[n % l])
			plt.plot(p,g,d[n % l])
			
		# source name
		print(' \n')
		s = self.source
		if s:
			print(s)
			print(' ')
			
		# axis
		if a:
			print('axis: ')
			if y:
				print(a + ', imaginary')
			else:
				print(a + ', real')
			print(' ')
			
		# inputs
		z = self.inputs
		if z:
			print('inputs:')
			k = z.keys()
			k = Pa._tidy(k)
			for i in k:
				w = z[i]
				try:
					if w.imag == 0:
						w = w.real
				except:
					pass
				print(i + ' = ' + str(w))
			print(' ')
		
		# results name
		m = self.name
		if m:
			print(m + ' =')
			
		# plot graph
		plt.margins(0.1,0.1)
		plt.show()
		plt.close()
			
		return None

	def gather(self):
		"""Gather the data into a list of strings for writing to a file.
		
		Arguments:
			None
			
		Returns:
			list of strings
		"""
		
		# begin list
		l = []
		
		# gather axis
		l.append('axis:')
		a = '___'
		if self.axis:
			a = self.axis
		l.append(a)
		
		# gather name
		l.append('name:')
		m = '___'
		if self.name:
			m = self.name
		l.append(m)
		
		# gather source
		l.append('source:')
		s = '___'
		if self.source:
			s = self.source
		l.append(s)
		
		# gather inputs
		l.append('inputs:')
		u = self.inputs
		for k,i in u.items():
			l.append(k)
			l.append(str(i))
		
		# gather pages
		l.append('pages:')
		for n,i in enumerate(self):
			l.append('[page ' + str(n) + ']')
			g = i.gather()
			for j in g:
				l.append(j)
		
		return l
	
	def gauge(self,f=None,t=None):
		"""Gauge the curvatures between two indices.
		
		Arguments:
			f=None: integer, beginning index, defaults to 0
			t=None: integer, ending index, defaults to length
			
		Returns:
			list of lists of complex numbers, the curvatures at each window
		"""
		
		# set default beginning
		if f is None or f < 0:
			f = 0
			
		# set default end
		if t is None or t > len(self):
			t = len(self)
			
		# zip together triples
		a = self[f:t - 2]
		b = self[f + 1:t - 1]
		c = self[f + 2:t]
		z = zip(a,b,c)
		
		# transpose
		z = [zip(*i) for i in z]
		
		# for every triple
		u = []
		for i in z:
			
			# and every solution set
			v = []
			for j in i:
				
				# calculate the curvature
				# w = a -2b + c
				w = j[1].scale(-2)
				w = w.add(j[0])
				w = w.add(j[2])
				w = Re(abs(w.real),abs(w.imag))
				v.append(w)
				
			# append to list
			u.append(v)
			
		# transpose
		u = [list(i) for i in zip(*u)]
			
		return u
	
	def glance(self,a,b=None):
		"""View a specified page or pages.
		
		Arguments:
			a: integer, index of starting Page instance
			b=None: integer, index of ending Page instance
			
		Returns:
			None
		"""
		
		# multiple pages
		if b:
			for i in range(a, b + 1):
				print('page %d:' % (i))
				self[i].view()
			
		# single page
		else:
			print('page %d:' % (a))
			self[a].view()
	
	def hone(self):
		"""Smooth solutions of a multisolution problem into the flattest set, the set with lowest total curvature.
		
		Arguments:
			None
			
		Returns:
			Book instance
			
		Notes:
			Hone may need to be performed twice, because the first pass may make available flatter options for the second pass.
		"""
		
		# pick permutation
		p = Re.permutations[len(self[0])]
		p = p[:]
		
		# reverse to restore on last permutation
		p.reverse()
		
		# copy the book
		c = self.copy()
		
		# calculate all curvatures
		v = c.gauge()
		
		# for every point except first
		l = len(c)
		for n in range(1,l):
				
			# store page at index
			g = c[n].copy()
				
			# store page after index
			if n < l - 1:
				h = c[n + 1].copy()
				
			# for every permutation
			q = []
			for j in p:
					
				# twist pages
				c[n] = g.twist(*j)
				if n < l - 1:
					c[n + 1] = h.twist(*j)
						
				# gauge affected region
				# (a twist at point n affects curves n-1 and n-2, comprising points n-2 through n+1)
				u = c.gauge(n - 2, n + 2)
				
				# insert new curvatures into copy
				w = [k[:] for k in v]
				for k,m in zip(w,u):
					if n > 1:
						k[n - 2] = m[0]
						if n < l - 1:
							k[n - 1] = m[1]
					else:
						k[n - 1] = m[0]
						
				# reassociate permutated ends
				for k,m in zip(j,w):
					m[n:] = v[k][n:]
				
				# convert to flatness
				f = Bo._flatten(w)
				q.append((j,f))
					
			# assess maximum flatness
			q.sort(key=lambda x: x[1])
			a = q.pop()[0]
				
			# if permutation is different
			if a != p[-1]:
					
				# twist
				a = list(a) + [n]
				c = c.twist(*a)
					
				# recalculate curvatures
				v = c.gauge()
		
		# correct isolated points
		# for every point except ends
		for n in range(1,l - 1):
				
			# store page at index
			g = c[n].copy()
				
			# for every permutation
			q = []
			for j in p:
					
				# twist page
				c[n] = g.twist(*j)
						
				# gauge affected region
				u = c.gauge(n - 2, n + 3)
				
				# insert new curvatures into copy
				w = [k[:] for k in v]
				for k,m in zip(w,u):
					if n > 1:
						k[n - 2] = m[0]
						k[n - 1] = m[1]
						if n < l - 2:
							k[n] = m[2]
					else:
						k[n - 1] = m[0]
						k[n] = m[1]
				
				# convert to flatness
				f = Bo._flatten(w)
				q.append((j,f))
					
			# assess maximum flatness
			q.sort(key=lambda x: x[1])
			a = q.pop()[0]
				
			# if permutation is different
			if a != p[-1]:
					
				# twist
				a = list(a)
				c[n] = c[n].twist(*a)
					
				# recalculate curvatures
				v = c.gauge()
		
		return c
	
	def integrate(self):
		"""Integrate each solution in a book of results.
		
		Arguments:
			None
			
		Returns:
			Page instance
		"""
		
		# get axis
		a = self.axis
		if not a:
			print('No dependent variable defined.  Integration aborted.\n')
			
			return None
		
		# calculate dx from beginning and end
		z = Re(0)
		p = [i.inputs.get(a,z) for i in self]
		b = Re(p[0])
		e = Re(p[-1])
		l = len(self)
		d = b.subtract(e).divide(l)
		
		# transpose data
		t = [i for i in zip(*self)]
		
		# sum all complex numbers and multiply by dx
		m = []
		for i in t:
			s = Pa(i).sum()
			s = s.multiply(d)
			m.append(s)
			
		# get source if common
		c = self.source
			
		# get name if common
		n = self.name
		if n:
			n = 'I (' + n + ') d' + a
			
		# get inputs
		u = self.inputs
		
		# imaginary and real projections
		r = [i.real for i in p]
		g = [i.imag for i in p]
		
		# add real to inputs if constant
		f = [i == r[0] for i in r]
		if False not in f:
			u[a] = r[0]
			
		# add imaginary to inputs if constant
		f = [i == g[0] for i in g]
		if False not in f:
			u[a] = g[0]
		
		return Pa(m,n,c,u)
	
	def load(self,f=None):
		"""Load data from a file into the book.
		
		Arguments:
			f=None: string, file name
			
		Returns:
			None
			
		Notes:
			The Book instance must be initialized before loading.  An empty book can be initialized with no arguments.
			
			If no filename is given, a file called 'test' will be sought.
		"""
		
		# default
		if not f:
			f = 'test.txt'
		
		# add .txt
		if not f.endswith('.txt'):
			f += '.txt'
		
		# get file name
		a = open(f,'r')
		
		# get list
		l = []
		for i in a:
			l.append(i.strip('\n'))
		
		# close file
		a.close()
		
		# deposit
		self.deposit(l)
		
		return None
	
	def notch(self,f,t):
		"""Identify the indices for slicing, switching, and twisting.
		
		Arguments:
			f: integer, float, or None, beginning index
			t: integer, float, or None,
			ending index
			
		Returns:
			tuple:
				beginning index, ending index
		"""
	
		# set default starting index
		if f is None:
			f = 0
			
		# get projection
		p,y = self.project()
			
		# get first index from point on axis
		if '.' in str(f):
			
			# search through projection
			for n,i in enumerate(p):
				
				# look until point is greater
				if i > f:
					f = n
					break
				
		# set default ending index
		if t is None:
			t = len(self)
			
		# get last index from point on axis
		if '.' in str(t):
			
			# search through projection
			for n,i in enumerate(p):
				
				# keep until no longer less
				if i > t:
					t = n - 1
					break
					
		return f,t
	
	def pick(self,n):
		"""Pick a page from the book.
		
		Arguments:
			n: integer, index of page to pick
			
		Returns:
			Page instance
		"""
		
		# copy page
		p = self[n].copy()
		
		return p
	
	def project(self):
		"""Project the independent coordinates along either the real or imaginary axis.
		
		Arguments:
			None
			
		Returns:
			tuple:
				list of floats, the projection,
				boolean, imaginary axis?
				
		Notes:
			By default, the projection is along the real axis, unless the spread along the imaginary axis is greater.
		"""
		
		# get axis
		a = self.axis
		if a is None:
			
			return None,None
		
		# find independent variable points
		o = Re(0)
		p = [i.inputs.get(a,o) for i in self]
		
		# determine projections
		u = [i.real for i in p]
		v = [i.imag for i in p]
		
		# axis of greatest spread determines projection
		y = False
		p = u
		if max(v) - min(v) > max(u) - min(u):
			y = True
			p = v
			
		return p,y
	
	def save(self,f=None):
		"""Save a book to a text file.
		
		Arguments:
			f=None: string, the file name
			
		Returns:
			None
			
		Notes:
			If no file name is given, by default the file name will be the name attribute plus '.txt'.  If there is no name attribute, 'test' will be used.
			
			'.txt' will be appended to the filename unless it is already given.
			
			If there is already a file with the same name, it will be overwritten.
		"""
	
		# get file name
		if f:
			if not f.endswith('.txt'):
				f += '.txt'
		else:
			n = self.name
			if n:
				f = n + '.txt'
			else:
				f = 'test.txt'
				
		# gather elements
		g = self.gather()
		g = [i + '\n' for i in g]
		
		# write file
		a = open(f,'w')
		a.writelines(g)
		a.close()
		
		return None
	
	def slash(self,*a):
		"""Slash all Pages by keeping only certain solutions on each page.
		
		Arguments:
			*a: unpacked tuple of integers
			
		Returns:
			Book instance
		"""
		
		# for every page in the book
		b = []
		for i in self:
			
			# perform slash
			b.append(i.slash(*a))
			
		# make book
		b = Bo(b,self.axis)
		
		return b
				
	def slice(self,f=None,t=None):
		"""Slice a section of pages from the book.
		
		Arguments:
			f=None: integer or float, beginning index or dependent variable value, defaults to 0
			t=None: integer or float, ending index or dependent variable value, defaults to length
			
		Returns:
			Book instance
			
		Notes:
			Designating indices with a decimal point will instead take the slice between two points on the axis.
		"""
			
		# copy pages
		b = []
		for i in self:
			b.append(i.copy())
			
		# make slice
		f,t = self.notch(f,t)
		b = b[f:t]
		b = Bo(b)
		
		# transfer attributes
		b.axis = self.axis
		b.name = self.name
		b.source = self.source
		b.inputs = self.inputs
		
		return b

	def switch(self,a,b,f=None,t=None):
		"""Switch the order of two functions between two points.
		
		Arguments:
			a: integer, solution index
			b: integer, solution index
			f=None: integer or float, beginning index or dependent variable value, defaults to 0
			t=None: integer or float, ending index or dependent variable value, defaults to length
			
		Returns:
			Book instance
			
		Notes:
			Designating indices with a decimal point will instead take the slice between two points on the axis.
		"""
			
		# get indices
		f,t = self.notch(f,t)
			
		# copy book
		c = self.copy()
		
		# switch pages
		for n,i in enumerate(c):
			
			# switch if between indices
			if n < t and n >= f:
				c[n] = i.switch(a,b)
		
		return c
	
	def twist(self,*a):
		"""Twist all functions into a new order at a particular location.
		
		Arguments:
			*a: unpacked tuple of *args:
				0..2) integers: indices of permutation
				3) integer or float: beginning index or independent variable value, first index
				by default
				4) integer or float: ending index or value, end by default
			
		Returns:
			Book instance
			
		Notes:
			The permutation represents the new ordering based on the old positions.
			
		Examples:
			The permutation (2,0,1) will twist the function that was at position 2 into position 1, the function at position 0 into position 1, and the function at position 1 into position 2.
		"""
		
		# get permutation
		l = len(self[0])
		
		# fill in arguments
		p = []
		f = None
		t = None
		for n,i in enumerate(a):
			
			# first fill in p
			if n < l:
				p.append(i)
			
			# then try f
			if n == l:
				f = i
				
			# then try t
			if n > l:
				t = i
			
		# get indices
		f,t = self.notch(f,t)
		
		# construct new pages
		b = []
		for n,i in enumerate(self):
			
			# rearrange between indices
			if n < t and n >= f:
				
				# twist page
				b.append(i.twist(*p))
				
			# otherwise make copy
			else:
				b.append(i.copy())
		
		# make book
		b = Bo(b,self.axis)
		
		return b
	
	def view(self,p=0):
		"""View a book of results.
		
		Arguments:
			p=0: indentation spaces
			
		Returns:
			None
		"""
				
		# tab
		t = ' ' * p
				
		# space
		print(' ')
				
		# print source
		s = self.source
		if s:
			print(t + 'source:')
			print(t + s + '\n')
			
		# print axis
		x = self.axis
		if x:
			print(t + 'axis:')
			print(t + x + '\n')
			
		# print inputs
		u = self.inputs
		z = u.keys()
		z = Pa._tidy(z)
		if len(z) > 0:
			print(t + 'inputs:')
			for k in z:
				
				# strip imaginary 0
				v = Re(u[k])
				if v.imag == 0:
					v = v.real
					
				# print
				print(t + '%s = ' % (k) + str(v))
				
			# spacer
			print(' ')
		
		# pages
		for n,i in enumerate(self):
			
			# page number
			print(t + 'page %d:' % (n))
			
			# set page source to None if already printed
			a = i.source
			if s:
				a = None
				
			# remove common inputs
			d = i.inputs
			b = {}
			for k,j in d.items():
				if k not in u:
					b[k] = j
					
			# get name
			e = i.name
			
			# view recrafted page indented
			Pa(i,e,a,b).view(p + 2)
			
		return None
	

# Abbreviation
Bo = Book
 



