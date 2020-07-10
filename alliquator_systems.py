# alliquator_systems.py
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

# import chains
import alliquator_chains as aq_ch
Ch = aq_ch.Chain


# System, a group of equations
class System(Gr):
	"""System is a group where all expressions are equations equaling zero.
	
	Inherits from Group
	"""
	
	def __init__(self,*g):
		"""Define a system of as a system of equations equalling zero.
		
		Arguments:
			*g: unpacked args of a single Group instance or multiple expressions.
			
		Returns:
			System instance
			
		Attributes:
			None
		"""
		
		# one argument means already a group
		if len(g) < 2:
			g = g[0]
		
		# convert to equations
		for i in g:
			i = Eq(i)
			self.append(i)
			

	# instance methods
	def annihilate(self,v,n,f=None):
		"""Eliminate a series of variables from the group, and chain all variable relations together in one group.
		
		Arguments:
			v: a list of strings, the names of variables in the order to br eliminated
			n: a list of integers, the indices of the corresponding expressions to use for isolation
			f=None: integer, the index of the final remaining equation
			
		Returns:
			Chain instance
			
		Notes:
			The returned chain will have as its first expression as the final equation, followed by all the substituting expression in reverse order.
			
			Elimination depends on all original expressions being valid equations when set to 0.  The resulting chain does not have this property, as all expressions after the first are equal to variables, not zero.
			
			If no final equation index is specified, the first number missing from the elimination sequence will be chosen.
		"""
		
		# eliminate, store subs in dictionary
		d = {}
		s = self
		for i,j in zip(v,n):
			b = s.pick(j).isolate(i)
			s = s.eliminate(i,j)
			s = s.simplify()
			d[i] = b
		
		# if not specified, final expression is assumed to be first index missing from elimination indices
		if not f:
			a = 0
			while a in n:
				a += 1
			f = a
			
		# new group begins with final expression
		f = s.pick(f)
		e = [f]
		
		# fill in group with isolations in reverse order
		v.reverse()
		for i in v:
			e.append(d[i])
			
		return Ch(Gr(*e))
		
	def eliminate(self,x,n):
		"""Eliminate a variable from the group, and retain the substitution
		
		Arguments:
			x: string, variable to eliminate
			n: integer, index of expression to use for isolation
			
		Returns:
			System instance
			
		Notes:
			x must be at a power of one in the expression used for isolation.
			
			Performs condensation afterwards.
			
			The equation used for eliminaton should be empty after substitution.
		"""
		
		# make substituting expression
		b = self[n].isolate(x)
		
		# substitute into group
		y = self.substitute(b,x)
		
		# simplify eliminated equation
		y[n] = y[n].simplify()
		
		return y
		
		
# Abbreviation
Sy = System



