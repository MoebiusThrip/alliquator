# alliquator_shelves.py
# manipulations of lists of books of calculation results
 
# import math
import math
sqrt = math.sqrt
 
# import plotting
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# import results
import alliquator_results as aq_re
Re = aq_re.Result

# import pages
import alliquator_pages as aq_pa
Pa = aq_pa.Page

# import books
import alliquator_books as aq_bo
Bo = aq_bo.Book

 
# Class for a list of Book instances
class Shelf(list):
	"""A Shelf instance is a list of Book instances, representing the evaluation of one expression over two dimensions or the evaluation of multiple expressions over one dimension.
	
	Shelf class inherits from list.
	"""
	
	def __init__(self,l=None,x=None):
		"""Define a Shelf instance as a list of Book instances.
		
		Arguments:
			l=None: list of Book instances
			x=None: string, name of second independent variable along which expression is evaluated
			
		Attributes:
			first: string, name of first axis variable
			inputs: dictionary mapping variables to values
			second: string, name of second axis variable
			name: string, name of results
			source: source expression

		"""
		
		# fill in books
		if l:
			for i in l:
				self.append(i)
		
		# first axis is common axis
		a = None
		if l:
			a = self[0].axis
			t = [i.axis == a for i in self]
			if False in t:
				a = None
		self.first = a
		
		# second axis
		self.second = None
		if x:
			self.second = x
		
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
			t = [j == u for j in t]
			if not False in t:
				c[k] = u
		self.inputs = c
		
	
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
		
		return '<Shelf object>'
		
	def assimilate(self):
		"""Integrate over both axes.
		
		Arguments:
			None
			
		Returns:
			Page instance
		"""
		
		# perform first integration
		t = self.integrate()
		
		# perform second integration
		u = t.integrate()
		
		return u
		
	def copy(self):
		"""Copy the shelf.
		
		Arguments:
			None
			
		Returns:
			Shelf instance
		"""
		
		# copy each book
		c = [i.copy() for i in self]
		
		# transfer attributes
		c = Sh(c,self.second)
		c.first = self.first
		c.name = self.name
		c.source = self.source
		c.inputs = self.inputs
		
		return c
		
	def deposit(self,l):
		"""Deposit a list of strings from a file into an empty shelf.
		
		Arguments:
			l: list of strings
			
		Returns:
			None
		"""
		
		# reverse list
		l.reverse()
		
		# get first axis, skipping header
		p = l.pop()
		p = l.pop()
		if p != '___':
			self.first = p
		
		# get second axis, skipping header
		p = l.pop()
		p = l.pop()
		if p != '___':
			self.second = p
		
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
		while p != 'books:':
			self.inputs[p] = Re(l.pop())
			p = l.pop()
		
		# get books
		g = []
		a = []
		while len(l) > 0:
			
			# next element
			p = l.pop()
			
			# begin new page if header found
			if p.startswith('[book'):
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
			e = Bo()
			e.deposit(i)
			self.append(e)
		
		return None
		
	def draw(self):
		"""Draw all data.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# draw each book
		for n,i in enumerate(self):
			print(str(n) + ':')
			i.draw()
			print(' ')
			
		return None
	
	def flip(self):
		"""Flip first and second axes.
		
		Arguments:
			None
			
		Returns:
			Shelf instance
		"""
		
		# make a copy
		c = self.copy()
		
		# transpose pages
		h = [i for i in zip(*c)]
		
		# flip axes
		a = self.second
		b = self.first
		
		# make books
		h = [Bo(i,a) for i in h]
		
		# make shelf
		h = Sh(h,b)
		
		return h
		
	def gather(self):
		"""Gather the data into a list of strings for writing to a file.
		
		Arguments:
			None
			
		Returns:
			list of strings
		"""
		
		# begin list
		l = []
		
		# gather first axis
		l.append('first:')
		a = '___'
		if self.first:
			a = self.first
		l.append(a)
		
		# gather second axis
		l.append('second:')
		b = '___'
		if self.second:
			b = self.second
		l.append(b)
		
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
		
		# gather books
		l.append('books:')
		for n,i in enumerate(self):
			l.append('[book ' + str(n) + ']')
			g = i.gather()
			for j in g:
				l.append(j)
		
		return l
	
	def glance(self,a,b=None):
		"""View a specified book or books.
		
		Arguments:
			a: integer, index of starting Page instance
			b=None: integer, index of ending Page instance
			
		Returns:
			None
		"""
		
		# multiple pages
		if b:
			for i in range(a, b + 1):
				print('book %d:' % (i))
				self[i].view(2)
			
		# single page
		else:
			print('book %d:' % (a))
			self[a].view(2)
	
	def hone(self):
		"""Smooth solutions of a multi-solution problem along one direction into the set with the tightest functions, for each book in the shelf.
		
		Arguments:
			None
			
		Returns:
			Shelf instance
			
		Notes:
			Attempts to find tightest set by arranging points so that the functions are of shortest length.
		"""
		
		# copy shelf
		h = self.copy()
		
		# hone all books
		for n,i in enumerate(h):
			h[n] = i.hone()
			
		return h
	
	def integrate(self):
		"""Integrate each Book in a Shelf of books.
		
		Arguments:
			None
			
		Returns:
			Book instance
		"""
		
		# integrate
		p = []
		for i in self:
			t = i.integrate()
			p.append(t)
			
		return Bo(p,self.second)
			
	def load(self,f=None):
		"""Load data from a file into the shelf.
		
		Arguments:
			f=None: string, file name
			
		Returns:
			None
			
		Notes:
			The Shelf instance must be initialized before loading.  An empty shelf can be initialized with no arguments.
			
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
			
	def pick(self,n):
		"""Pick a book from the shelf.
		
		Arguments:
			n: integer, index of book to pick
			
		Returns:
			Book instance
		"""
		
		# copy book
		b = self[n].copy()
		
		return b
			
	def polish(self):
		"""Smooth solutions of a multi-solution problem along two directions into the set with the tightest functions.
		
		Arguments:
			None
			
		Returns:
			Shelf instance
			
		Notes:
			Attempts to find the flattest set of points by honing along both directions and optimizing any mismatched points.
			
			Subsequent polishings may improve optimization.
		"""
		
		# make list of point indices
		l = range(len(self))
		m = range(len(self[0]))
		p = [[(i,j) for j in m] for i in l]
		
		# make list of point triples
		t = []
		
		# for each row
		for i in p:
			
			# make triples
			z = zip(i[:-2],i[1:-1],i[2:])
			
			# append each
			for j in z:
				t.append(j)
				
		# transpose points
		p = [[j for j in i] for i in zip(*p)]
		
		# for each row
		for i in p:
			
			# make triples
			z = zip(i[:-2],i[1:-1],i[2:])
			
			# append each
			for j in z:
				t.append(j)
				
		# hone all books
		h = self.hone()
		
		# flip and hone all books
		f = self.flip()
		f = f.hone()
		f = f.flip()
		
		# get misaligned points
		q = []
		
		# for every row
		for i in p:
			
			# and every entry
			for j,k in i:
				
				# compare order of results
				if h[j][k] != f[j][k]:
					
					# add to list if no match
					q.append((j,k))
					
		# segregate triples into inclusions and exclusions
		u = []
		x = []
		while len(t) > 0:
			
			# pop off each
			o = t.pop()
			
			# check misaligned points
			e = True
			for i in q:
				
				# append to exclusions
				if i in o:
					x.append(o)
					e = False
					break
					
			# otherwise keep
			if e:
				u.append(o)
				
		# get summed curvatures for inclusions
		u = h.survey(u)
		
		# get permutations
		p = Re.permutations
		p = p[len(self[0][0])]
		p = p[:]
		p.reverse()
		
		# take excluded points
		q.reverse()
		while len(q) > 0:
			
			# pop off point
			o = q.pop()
			
			# separate into new inclusions and exclusions
			y = x[:]
			w = []
			x = []
			while len(y) > 0:
				
				# pop off each
				a = y.pop()
				
				# check misaligned points
				e = True
				for i in q:
					
					# append to exclusions
					if i in a:
						x.append(a)
						e = False
						break
						
				# otherwise keep
				if e:
					w.append(a)
						
			# try all permutations
			b,c = o
			g = h[b][c].copy()
			d = []
			for i in p:
				
				# twist page
				h[b][c] = g.twist(*i)
				
				# survey new inclusions
				r = h.survey(w)
				
				# determine flatness
				f = Bo._flatten(zip(u,r))
				
				# append
				d.append((i,f))
				
			# find flattest set
			d.sort(key=lambda x: x[1])
			
			# pop and twist
			d = d.pop()[0]
			h[b][c] = g.twist(*d)
			r = h.survey(w)
			
			# recombine inclusions
			u = [i.add(j) for i,j in zip(u,r)]
			
		return h
			
	def save(self,f=None):
		"""Save a shelf to a text file.
		
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
			
	def scissor(self,f=None,t=None):
		"""Scissor out a subsection of books from the shelf.

		Arguments:
			f=None: integer or float, beginning index or dependent variable value, defaults to 0
			t=None: integer or float, ending index or dependent variable value, defaults to length
			
		Returns:
			Shelf instance
			
		Notes:
			Designating indices with a decimal point will instead take the slice between two points on the secondary axis.
		"""
		
		# Flip axes
		p = self.flip()
		
		# perform slice
		s = p.slice(f,t)
		
		# flip back
		h = s.flip()
		
		return h
		
	def sculpt(self):
		"""Sculpt a 3d plot of results.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# colors for real and imaginary plots
		f = ['r-','g-','b-','m-']
		g = ['r--','g--','b--','m--']
		t = len(f)
		
		# prepare lists for points
		x = []
		y = []
		z = []
		
		# axes
		a = self.first
		b = self.second
		
		# for each book
		for i in self:

			# get first axis projection
			u,q = i.project()
			x.append(u)
			
			# get second axis coordinate
			v = i[0].inputs[b].real
			
			# if both axes are the same, make the second imaginary unless the first aleady is
			if a == b and not q:
					v = i[0].inputs[b].imag
					
			# extend and append
			v = [v for j in i]
			y.append(v)
			
			# transpose pages for z coordinate
			z.append([j for j in zip(*i)])
			
		# transpose z coordinates again
		z = [i for i in zip(*z)]
				
		# print source
		s = self.source
		if s:
			print(s + '\n')
				
		# print axes
		print('axes:')
		if q:
			print(a + ', imaginary')
			print(b + ', real')
		else:
			print(a + ', real')
			if a == b:
				print(b + ', imaginary')
			else:
				print(b + ', real')
		print(' ')
			
		# print inputs
		p = self.inputs
		if p:
			print('inputs:')
			for k in p:
				q = str(p[k])
				try:
					if p[k].imag == 0:
						q = str(p[k].real)
				except:
					pass
				print('%s = ' % (k) + q)
			print(' ')
			
		# print name
		e = self.name
		if e:
			print(e + ' =')
			print(' ')
			
		# subplot
		sb = lambda x: x.add_subplot
		
		# for each solution layer
		for n,i in enumerate(z):
			
			# print solution number
			if len(z) > 1:
				print('%d:' % (n))
			
			# real plot
			c = plt.figure()
			d = sb(c)(111,projection='3d')
			
			# plot lines
			for m,j in enumerate(i):
				r = [k.real for k in j]
				plt.plot(x[m],y[m],r,f[n % t])
			
			# show plot
			plt.margins(0.1,0.1,0.1)
			plt.show()
			plt.close()
			print('real')
			
			# imaginary plot
			c = plt.figure()
			d = sb(c)(111,projection='3d')
			
			# plot lines
			for m,j in enumerate(i):
				r = [k.imag for k in j]
				plt.plot(x[m],y[m],r,g[n % t])
			
			# show plot
			plt.margins(0.1,0.1,0.1)
			plt.show()
			plt.close()
			print('imaginary')
			print(' ')
			print(' ')

		return None
			
	def slash(self,*a):
		"""Slash all pages in all books by keeping only certain solutions on each page.
		
		Arguments:
			*a: unpacked tuple of integers
			
		Returns:
			Shelf instance
		"""
		
		# copy shelf
		h = self.copy()
		
		# for every book in the shelf
		for n,i in enumerate(h):
			
			# replace with slashed version
			h[n] = i.slash(*a)
		
		return h
				
	def slice(self,f=None,t=None):
		"""Slice a section of pages from all books.
		
		Arguments:
			f=None: integer or float, beginning index or dependent variable value, defaults to 0
			t=None: integer or float, ending index or dependent variable value, defaults to length
			
		Returns:
			Shelf instance
			
		Notes:
			Designating indices with a decimal point will instead take the slice between two points on the axis.
		"""
			
		# copy shelf
		h = self.copy()
		
		# replace with sliced versions
		for n,i in enumerate(h):
			h[n] = i.slice(f,t)
		
		return h

	def survey(self,l):
		"""Survey the curvatures across the shelf, avoiding points given.
		
		Arguments:
			l: list of tuples, triples of index pairs
			
		Returns:
			list of complex numbers, the summed curvatures
		"""
		
		# for each triple
		v = []
		for i in l:
			
			# get pages
			g = [self[j][k] for j,k in i]
			
			# for each solution
			w = []
			for a,b,c in zip(*g):
				
				# calculate curvature
				u = b.scale(-2)
				u = u.add(a)
				u = u.add(c)
				u = Re(abs(u.real),abs(u.imag))
				w.append(u)
				
			# append
			v.append(w)
			
		# transpose and sum
		v = [i for i in zip(*v)]
		v = [Pa(list(i)).sum() for i in v]
		
		return v
	
	def switch(self,a,b,f=None,t=None):
		"""Switch the order of two functions between two points.
		
		Arguments:
			a: integer, solution index
			b: integer, solution index
			f=None: integer or float, beginning index or dependent variable value, defaults to 0
			t=None: integer or float, ending index or dependent variable value, defaults to length
			
		Returns:
			Shelf instance
			
		Notes:
			Designating indices with a decimal point will instead take the slice between two points on the axis.
		"""
			
		# copy shelf
		h = self.copy()
		
		# switch all books
		for n,i in enumerate(h):
			h[n] = i.switch(a,b,f,t)
		
		return h
	
	def twist(self,*a):
		"""Twist all functions into a new order at a particular location.
		
		Arguments:
			*a: unpacked tuple of *args:
				0..2) integers: indices of permutation
				3) integer or float: beginning index or independent variable value, first index
				by default
				4) integer or float: ending index or value, end by default
			
		Returns:
			Shelf instance
			
		Notes:
			The permutation represents the new ordering based on the old positions.
			
		Examples:
			The permutation (2,0,1) will twist the function that was at position 2 into position 0, the function at position 0 into position 1, and the function at position 1 into position 2.
		"""
		
		# copy shelf
		h = self.copy()
		
		# twist all books
		for n,i in enumerate(h):
			h[n] = i.twist(*a)
			
		return h
			
	def view(self,p=0):
		"""View a shelf of results.
		
		Arguments:
			p=0: indentation spaces
			
		Returns:
			None
		"""
		
		# tab
		t = ' ' * p
				
		# spacer
		print(' ')
				
		# print source
		s = self.source
		if s:
			print(t + 'source:')
			print(t + s + '\n')
			
		# print first axis
		x = self.first
		if x:
			print(t + 'first axis:')
			print(t + x + ', real\n')
			
		# print second axis
		y = self.second
		if y:
			print(t + 'second axis:')
			if x == y:
				print(t + y + ', imaginary\n')
			else:
				print(t + y + ', real\n')
			
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
		
		# books
		for n,i in enumerate(self):
			
			# book number
			print(t + 'book %d:' % (n))
			
			# set book source to None if already printed
			b = i.source
			if s:
				b = None
				
			# set axis to None if already printed
			d = i.axis
			if x:
				d = None
			
			# view recrafted book
			o = []
			for j in i:
				
				# remove common inputs
				w = j.inputs
				c = {}
				for k,m in w.items():
					if k not in u:
						c[k] = m
				
				# construct abbreviated pages
				a = j.name
				o.append(Pa(j,a,b,c))
			
			# view book
			Bo(o,d).view(p + 2)
			
		return None
			
	
# Abbreviation
Sh = Shelf


 


