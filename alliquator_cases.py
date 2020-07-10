# alliquator_cases.py
# manipulations of lists of lists of calculation results
 
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

# import shelves
import alliquator_shelves as aq_sh
Sh = aq_sh.Shelf


# Class for a list of Shelf instances
class Case(list):
	"""A Case is a list of Shelves, representing the 3d plotting of multiple expressions
	
	Case class inherits from list.
	"""
	
	def __init__(self,l=None):
		"""Define a Case as a list of Shelf instances.
		
		Arguments:
			l=None: list of Shelf instances
			
		Attributes:
			None
		"""
		
		# fill in shelves
		if l:
			for i in l:
				self.append(i)
		
	# static methods
	@staticmethod
	def _ravel(a,b):
		"""Find the permutation that ravels a into b.
		
		Arguments:
			a: list of complex numbers
			b: permuted list of same complex numbers
			
		Returns:
			tuple, permuted integers
		"""
		
		# link integers
		e = [i for i in enumerate(a)]
		
		# sort by equality
		l = []
		for i in b:
			e.sort(key=lambda x: x[1] == i)
			l.append(e.pop())
			
		# pull off integers
		l = [i[0] for i in l]
			
		return l
		
	# instance methods
	def __pos__(self):
		"""Use the + operator to view the Case.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# view
		self.view()
		
		return None
		
	def __repr__(self):
		"""Create string for representing Case object on screen.
		
		Arguments:
			None
			
		Returns:
			string
		"""
		
		return '<Case object>'
			
	def assimilate(self):
		"""Integrate each Shelf over both axes.
		
		Arguments:
			None
			
		Returns:
			Book instance
		"""
		
		# assimilate each shelf
		u = [i.assimilate() for i in self]
		
		# make book
		b = Bo(u)
		
		return b
			
	def copy(self):
		"""Copy the Case.
		
		Arguments:
			None
			
		Returns:
			Case instance
		"""
		
		# copy each shelf
		c = [i.copy() for i in self]
		c = Ca(c)
		
		return c
			
	def deposit(self,l):
		"""Deposit a list of strings from a file into an empty case.
		
		Arguments:
			l: list of strings
			
		Returns:
			None
		"""
		
		# reverse list
		l.reverse()

		# skip header
		p = l.pop()
		
		# get shelves
		g = []
		a = []
		while len(l) > 0:
			
			# next element
			p = l.pop()
			
			# begin new page if header found
			if p.startswith('[shelf'):
				if a:
					g.append(a)
				a = []
				
			# otherwise add next element
			else:
				a.append(p)
				
		# add final shelf
		g.append(a)
		
		# deposit shelves
		for i in g:
			e = Sh()
			e.deposit(i)
			self.append(e)
		
		return None
			
	def flip(self):
		"""Flip first and second axes of every shelf.
		
		Arguments:
			None
			
		Returns:
			Case instance
		"""
		
		# flip every shelf
		c = [i.flip() for i in self]
		
		return Ca(c)
			
	def gather(self):
		"""Gather the data into a list of strings for writing to a file.
		
		Arguments:
			None
			
		Returns:
			list of strings
		"""
		
		# begin list
		l = []
		
		# gather shelves
		l.append('shelves:')
		for n,i in enumerate(self):
			l.append('[shelf ' + str(n) + ']')
			g = i.gather()
			for j in g:
				l.append(j)
		
		return l
	
	def glance(self,a,b=None):
		"""View a specified shelf or shelves.
		
		Arguments:
			a: integer, index of starting Shelf instance
			b=None: integer, index of ending Shelf instance
			
		Returns:
			None
		"""
		
		# multiple shelves
		if b:
			for i in range(a, b + 1):
				print('shelf %d:' % (i))
				self[i].view(2)
			
		# single shelf
		else:
			print('shelf %d:' % (a))
			self[a].view(2)
			
		return None
			
	def load(self,f=None):
		"""Load data from a file into the case.
		
		Arguments:
			f=None: string, file name
			
		Returns:
			None
			
		Notes:
			The Case instance must be initialized before loading.  An empty case can be initialized with no arguments.
			
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
		"""Pick a shelf from the case.
		
		Arguments:
			n: integer, index of book to pick
			
		Returns:
			Shelf instance
		"""
		
		# copy book
		h = self[n].copy()
		
		return h
			
	def polish(self,l=True):
		"""Smooth solutions of a multi-solution problem along two directions into the set with the tightest functions.
		
		Arguments:
			l=True: boolean, link solutions?
			
		Returns:
			Case instance
			
		Notes:
			Attempts to find tightest set by polishing first set and rearranging all other sets in accordance.
			
			If the individual shelves are from a chain of linked equations, only the first equation will be polished, and the corresponding changes will propagate throughout.  Otherwise, unlinking will cause each shelf to be polished on its own terms.
		"""
		
		# copy
		c = self.copy()
		
		# if not linked
		if not l:
			
			# polish each
			c = [i.polish() for i in c]
			
			return Ca(c)
		
		# pick first set
		f = c.pick(0)
		
		# polish first set
		c[0] = f.polish()
		
		# go through each book
		for n,i in enumerate(f):
			
			# and each page
			for o,j in enumerate(i):
				
				# determine permutation
				p = Ca._ravel(j,c[0][n][o])
				
				# propagate twist
				for k in c[1:]:
					
					# assign page
					g = k[n][o]
					k[n][o] = g.twist(*p)
					
		return c
					
	def save(self,f=None):
		"""Save a case to a text file.
		
		Arguments:
			f=None: string, the file name
			
		Returns:
			None
			
		Notes:
			If no file name is given, by default 'test' will be used.
			
			'.txt' will be appended to the filename unless it is already given.
			
			If there is already a file with the same name, it will be overwritten.
		"""
	
		# get file name
		if f:
			if not f.endswith('.txt'):
				f += '.txt'
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
		"""Scissor out a subsection of books from every shelf in the case.

		Arguments:
			f=None: integer or float, beginning index or dependent variable value, defaults to 0
			t=None: integer or float, ending index or dependent variable value, defaults to length
			
		Returns:
			Case instance
			
		Notes:
			Designating indices with a decimal point will instead take the slice between two points on the secondary axis.
		"""
		
		# scissor every shelf
		c = [i.scissor(f,t) for i in self]
		
		return Ca(c)
			
	def sculpt(self):
		"""Show all 3dplots in the case.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		for i in self:
			i.sculpt()
		
		return None
			
	def slash(self,*a):
		"""Slash all pages in all books by keeping only certain solutions on each page, for every book on the shelf.
		
		Arguments:
			*a: unpacked tuple of integers
			
		Returns:
			Case instance
		"""
		
		# slash each shelf
		c = [i.slash(*a) for i in self]
		
		return Ca(c)
				
	def slice(self,f=None,t=None):
		"""Slice a section of pages from all books for every shelf.
		
		Arguments:
			f=None: integer or float, beginning index or dependent variable value, defaults to 0
			t=None: integer or float, ending index or dependent variable value, defaults to length
			
		Returns:
			Case instance
			
		Notes:
			Designating indices with a decimal point will instead take the slice between two points on the axis.
		"""
			
		# slice all shelves
		c = [i.slice(f,t) for i in self]
		
		return Ca(c)

	def switch(self,a,b,f=None,t=None):
		"""Switch the order of two functions between two points, for every Shelf.
		
		Arguments:
			a: integer, solution index
			b: integer, solution index
			f=None: integer or float, beginning index or dependent variable value, defaults to 0
			t=None: integer or float, ending index or dependent variable value, defaults to length
			
		Returns:
			Case instance
			
		Notes:
			Designating indices with a decimal point will instead take the slice between two points on the axis.
		"""
			
		# switch each shelf
		c = [i.switch(a,b,f,t) for i in self]
		
		return Ca(c)
	
	def twist(self,*a):
		"""Twist all functions into a new order at a particular location, for every Shelf.
		
		Arguments:
			*a: unpacked tuple of *args:
				0..2) integers: indices of permutation
				3) integer or float: beginning index or independent variable value, first index
				by default
				4) integer or float: ending index or value, end by default
			
		Returns:
			Case instance
			
		Notes:
			The permutation represents the new ordering based on the old positions.
			
		Examples:
			The permutation (2,0,1) will twist the function that was at position 2 into position 0, the function at position 0 into position 1, and the function at position 1 into position 2.
		"""
		
		# twist each shelf
		c = [i.twist(*a) for i in self]
		
		return Ca(c)
			
	def view(self):
		"""View a Case of shelves.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# view all
		for n,i in enumerate(self):
			print('shelf %d:' % (n))
			i.view(2)
			
		return None
		

# Abbreviation
Ca = Case
 



