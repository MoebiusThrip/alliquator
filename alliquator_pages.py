# alliquator_pages.py
# manipulations of lists of calculation results
 
# import plotting
import matplotlib.pyplot as plt
 
# import results
import alliquator_results as aq_re
Re = aq_re.Result
 
# import timing decorator
time_process = aq_re.time_process
 
 
# Class for list of results
class Page (list):
	"""A Page instance is a list of results from the evaluation of an expression or equation.
	
	Page class inherits from list.
	"""
	
	def __init__(self,l=None,n=None,s=None,u=None):
		"""Define a Page instance as a list of Result instances.
		
		Arguments:
			l=None: list of Result instances
			n=None: string, name of results
			s=None: string, expression from which evaluations were made
			u=None: dictionary mapping variables to values
			
		Attributes:
			inputs: dictionary mapping variables to their values
			name: string, name of results
			source: string, the expression that produced the results
		"""
		
		# convert to Result instances
		if l:
			for i in l:
				self.append(Re(i))
			
		# attributes
		self.inputs = {}
		if u:
			self.inputs = u
		self.name = n
		self.source = s
	
	
	# static methods
	@staticmethod
	def _tidy(k):
		"""Tidy up a list of keys by sorting alphabetically.
		
		Arguments:
			k: list of strings, keys
			
		Returns:
			list of keys
			
		Notes:
			Capitalized keys will come after lowercase keys.
		"""
		
		# split keys into upper and lower
		u = [i for i in k if i[0].isupper()]
		l = [i for i in k if i[0].islower()]
		
		# sort
		u.sort()
		l.sort()
		
		# recombine
		y = l + u
		
		return y
	
	
	# instance methods
	def __pos__(self):
		"""Use the + operator to view the page.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# view
		self.view()
		
		return None
		
	def copy(self):
		"""Copy the page.
		
		Arguments:
			None
			
		Returns:
			Page instance
		"""
		
		# begin list
		p = []
		for i in self:
			p.append(i.copy())
			
		# make page
		p = Pa(p)
		
		# transfer attributes
		p.name = self.name
		p.source = self.source
		p.inputs = self.inputs
		
		return p
		
	def deposit(self,l):
		"""Deposit a list of strings from a file into an empty page.
		
		Arguments:
			l: list of strings
			
		Returns:
			None
		"""
		
		# reverse list
		l.reverse()
		
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
		while p != 'results:':
			self.inputs[p] = Re(l.pop())
			p = l.pop()
		
		# get results
		while len(l) > 0:
			self.append(Re(l.pop()))
		
		return None
		
	def draw(self):
		"""Draw all results on the page as vectors in the complex plane.
		
		Arguments:
			None
			
		Returns:
			None
		"""
		
		# colors
		c = ['r-','g-','b-']
		
		# print name
		if self.name:
			print(self.name)
		
		# plot vectors
		for n,i in enumerate(self):
			x = [0,i.real]
			y = [0,i.imag]
			k = c[n % 3]
			plt.plot(x,y,k)
			
		# show plot
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
		
		# gather name
		l.append('name:')
		n = '___'
		if self.name:
			n = self.name
		l.append(n)
		
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
		
		# gather results
		l.append('results:')
		for i in self:
			l.append(str(i))
		
		return l
		
	def load(self,f=None):
		"""Load data from a file into the page.
		
		Arguments:
			f=None: string, file name
			
		Returns:
			None
			
		Notes:
			The Page instance must be initialized before loading.  An empty page can be initialized with no arguments.
			
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
		"""Pick a particular result from the page.
		
		Arguments:
			n: integer, index of Result
			
		Returns:
			Result instance
		"""
		
		# pick result
		p = self[n].copy()
		
		return p
		
	def save(self,f=None):
		"""Save a page to a text file.
		
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
		"""Slash a page, retaining only the specified indices.
		
		Arguments:
			*a: unpacked tuple of indices
			
		Returns:
			Page instance
		"""
		
		# start results list
		r = []
		for n,i in enumerate(self):
			if n in a:
				r.append(i.copy())
				
		# start page
		p = Pa(r)
		
		# transfer attributes
		p.name = self.name
		p.source = self.source
		p.inputs = self.inputs
		
		return p
		
	def sum(self):
		"""Sum all Result instances.
		
		Arguments:
			None
			
		Returns:
			Result instance
		"""
		
		# separate real and imaginary
		r = [i.real for i in self]
		m = [i.imag for i in self]
		
		# sum
		s = Re(sum(r),sum(m))
		
		return s
		
	def switch(self,a,b):
		"""Switch the order of two results on the page.
		
		Arguments:
			a: integer, first index
			b: integer, second index
			
		Returns:
			Page instance
		"""
		
		# make a copy of results
		c = [i.copy() for i in self]
		
		# make a copy of page
		p = self.copy()
		
		# switch results
		p[a] = c[b]
		p[b] = c[a]
		
		return p
		
	def twist(self,*p):
		"""Permute the order of results on the page.
		
		Arguments:
			*p: unpacked tuple of indices 
			
		Returns:
			Page instance
			
		Notes:
			The permutation refers to the new order based on the old indices.
			
		Examples:
			Twisting (1,2,0) will put the result that was at position 1 into position 0, the result that was at position 2 into position 1, and the result that was at position 0 into position 2.
		"""
		
		# copy page
		g = self.copy()
				
		# step through permutation
		for m,j in enumerate(p):
			g[m] = self[j].copy()
			
		return g
		
	def view(self,a=0):
		"""View the Page instance.
		
		Arguments:
			a=0: integer, indentation spaces
			
		Returns:
			None
		"""
		
		# attributes
		s = self.source
		p = self.inputs
		n = self.name
		
		# tab
		t = ' ' * a
	
		# view source
		print(' ')
		if s:
			print(t + 'source:')
			print(t + s + '\n')
			
		# view inputs
		if p:
			
			# sort keys
			y = p.keys()
			y = Pa._tidy(y)
			
			# print inputs
			print(t + 'inputs:')
			for k in y:
				
				# remove imaginary 0's
				v = Re(p[k])
				if v.imag == 0:
					v = v.real
				
				# print
				print(t + '%s = ' % (k) + str(v))
				
			# spacer
			print(' ')
			
		# view results
		if len(self) > 0:
			print(t + 'results:')
		
		# name
		if n:
			print(t + '%s = ' % (n))
			
		# results
		for i in self:
			i.view(a)
		print(' ')
		
		return None
	

# Abbreviation
Pa = Page

