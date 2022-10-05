# Copyright (c) 2007-2022 Nick Gravgaard <nick@nickgravgaard.com>
# This code is licensed under the MIT Licence - see LICENCE.txt

# This file tries to follow the Style Guide for Python Code (PEP 8) *EXCEPT*
#  * it uses tabs for indenting (like Guido used to recommend)
#  * it doesn't follow the Maximum Line Length rule
# use pylint as following: pylint --indent-string='\t' --max-line-length=1000 elastictabstops

# Abstract Base Classes ("abc") of the "collection" module were moved to "collections.abc" 
# with Python:3.3, see https://docs.python.org/3.9/library/collections.html#module-collections
import sys
if sys.version_info.major >= 3 and sys.version_info.minor >= 3:
	from collections.abc import Sequence
else:
	from collections import Sequence

from elastictabstops.convert import _from_spaces, _from_elastic_tabstops, _from_fixed_tabstops, _to_spaces, _to_elastic_tabstops, _to_fixed_tabstops


class Text(Sequence):
	__slots__ = ['string']

	def __init__(self, val=''):
		self.check(val)
		self.string = val

	def check(self, val):
		if not isinstance(val, str):
			raise TypeError(("Expected a string (but got %s)." % val))

	def __len__(self): return len(self.string)

	def __getitem__(self, i): return self.string[i]

	def __str__(self): return str(self.string)

	def __repr__(self): return self.string.__repr__()

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.string == other.string
		elif isinstance(other, str):
			return self.string == other
		else:
			return False

	def __ne__(self, other): return not self.__eq__(other)

	def from_spaces(self, tab_width=8):
		return Table(_from_spaces(self.string, tab_width))

	def from_elastic_tabstops(self):
		return Table(_from_elastic_tabstops(self.string))

	def from_fixed_tabstops(self, tab_width=8):
		return Table(_from_fixed_tabstops(self.string, tab_width))


class Table(Sequence):
	__slots__ = ['list']

	def __init__(self, val):
		self.check(val)
		self.list = val

	def check(self, val):
		if not isinstance(val, list) or len(val) == 0 or any([not isinstance(i, list) or any([not isinstance(j, str) for j in i]) for i in val]):
			raise TypeError(("Expected a list of lists of strings (but got %s)." % val))

	def __len__(self): return len(self.list)

	def __getitem__(self, i): return self.list[i]

	def __str__(self): return str(self.list)

	def __repr__(self): return self.list.__repr__()

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.list == other.list
		elif isinstance(other, list):
			return self.list == other
		else:
			return False

	def __ne__(self, other): return not self.__eq__(other)

	def to_spaces(self, tab_width=8, multiples_of_tab_width=False):
		return Text(_to_spaces(self.list, tab_width, multiples_of_tab_width=multiples_of_tab_width))

	def to_elastic_tabstops(self):
		return Text(_to_elastic_tabstops(self.list))

	def to_fixed_tabstops(self, tab_width=8):
		return Text(_to_fixed_tabstops(self.list, tab_width))
