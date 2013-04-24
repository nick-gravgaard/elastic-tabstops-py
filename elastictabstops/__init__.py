"""
ElasticTabstops package
Converts text indented/aligned with elastic tabstops
see: http://nickgravgaard.com/elastictabstops/
"""

# Copyright (c) 2007-2013 Nick Gravgaard <me@nickgravgaard.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# This file tries to follow the Style Guide for Python Code (PEP 8) *EXCEPT*
#  * it uses tabs for indenting (like Guido used to recommend)
#  * it doesn't follow the Maximum Line Length rule
# use pylint as following: pylint --indent-string='\t' --max-line-length=1000 elastictabstops

from collections import namedtuple
import math
import re

__all__ = ['to_elastic_tabstops', 'to_spaces']

# This code can be used to convert large amounts of text, so performance matters.
# For this reason we use namedtuples and __slots__ to create readable but well-performing data structures.

PositionedText = namedtuple('PositionedText', 'text position')

class SizedText(object):
	"""Class used to store text and the width of the cell it's in."""

	__slots__ = ['text', 'size']

	def __init__(self, text, tab_size):
		self.text = text
		# size initially stores the minimum width of the cell
		self.size = self.calc_fixed_cell_size(tab_size)

	def calc_fixed_cell_size(self, tab_size):
		"""Given the length of the text inside a cell, return the size the cell should be."""

		# we add two to provide padding - one is not enough as it could be confused for a non-aligning space
		return int((math.ceil((len(self.text) + 2) / float(tab_size)))) * tab_size

	def get_padded_text(self):
		"""Returns self.text plus spaces to match the number of characters in self.size."""

		nof_spaces = self.size - len(self.text)
		return self.text + (' ' * nof_spaces)


def _cell_exists(list_of_lists, line_num, cell_num):
	"""Check that an item exists in a list of lists."""

	return line_num < len(list_of_lists) and cell_num < len(list_of_lists[line_num])


def _sub_tabs(line, tab_size, repl_char):
	"""Return a line of text where tab characters have been substituted with the correct number of replacement chaaracters."""

	str_list = []
	pos = 0
	for char in line:
		if char == '\t':
			expand = tab_size - (pos % tab_size)
			str_list.append(expand * repl_char)
			pos += expand
		else:
			str_list.append(char)
			pos += 1
	return ''.join(str_list)


def _get_positions_contents(text, tab_size):
	"""Given a piece of text and how long tabs should be, return a list of lists of PositionedText named tuples."""

	repl_char = '\x1a' # the 'substitute character' in unicode
	text = '\n'.join([_sub_tabs(line, tab_size, repl_char) for line in text.split('\n')])

	# Look for a char that is (not a space or \x1a) followed by any number of chars that are either (not a space or \x1a) or a space followed by (not a space or \x1a)
	# This allows the substrings to have spaces, but only if that space is followed by a non-space char
	compiled = re.compile(r'[^%(repl_char)s\s](?:[^%(repl_char)s\s]|\s(?=[^%(repl_char)s\s]))*' % {'repl_char': repl_char})
	return [[PositionedText(match.group(), match.start()) for match in compiled.finditer(line)] for line in text.split('\n')]


def to_elastic_tabstops(text, tab_size=8):
	"""Convert text from using spaces to using tabs with elastic tabstops."""

	if not isinstance(text, str) or not isinstance(tab_size, int):
		raise TypeError('The to_elastic_tabstops function takes a string and an integer.')
	if tab_size < 2:
		raise ValueError("The second parameter of to_elastic_tabstops ('tab_size') should be 2 or greater.")

	# '\r's before '\n's are just left at the end of lines
	# solitary '\r's aren't dealt with as these days no one uses CRs on their own for new lines
	lines = _get_positions_contents(text, tab_size)
	max_cells = max([len(line) for line in lines])
	nof_lines = len(lines)

	# not a "for cell_num in (range(max_cells)):" loop because max_cells may increase
	cell_num = 0
	while cell_num < max_cells:
		starting_new_block = True
		start_range = 0
		end_range = 0

		for line_num in range(nof_lines + 1):
			if _cell_exists(lines, line_num, cell_num):
				# if we're at the start of a block remember what line we're on
				if starting_new_block:
					start_range = line_num
					starting_new_block = False
				end_range = line_num
			# if there's no cell and we're not starting a block then we're at the end of a column block
			elif not starting_new_block:
				block_positions = [lines[block_line_num][cell_num].position for block_line_num in range(start_range, end_range + 1)]

				min_indent = min(block_positions)

				for block_line_offset, block_position in enumerate(block_positions):
					block_line_num = start_range + block_line_offset
					# if the current block is to the right we need to insert an empty cell
					if block_position > min_indent:
						# insert an empty cell to shift existing cells across
						lines[block_line_num].insert(cell_num, PositionedText('', 0))
						max_cells = max(max_cells, len(lines[block_line_num]))
					# otherwise if we're in the first column we need to insert empty cells for every line in this block
					elif cell_num == 0:
						nof_cells_missing = int(block_position / tab_size)
						for _ in range(nof_cells_missing):
							# insert empty indentation cells
							lines[block_line_num].insert(cell_num, PositionedText('', 0))
							max_cells = max(max_cells, len(lines[block_line_num]))

				starting_new_block = True

		cell_num += 1

	return '\n'.join(['\t'.join([cell.text for cell in line]) for line in lines])


def to_spaces(text, tab_size=8):
	"""Convert text from using tabs with elastic tabstops to using spaces."""

	if not isinstance(text, str) or not isinstance(tab_size, int):
		raise TypeError('The to_spaces function takes a string and an integer.')
	if tab_size < 2:
		raise ValueError("The second parameter of to_spaces ('tab_size') should be 2 or greater.")

	# '\r's before '\n's are just left at the end of lines
	# solitary '\r's aren't dealt with as these days no one uses CRs on their own for new lines
	lines = [[SizedText(cell, tab_size) for cell in line.split('\t')] for line in text.split('\n')]
	max_cells = max([len(line) for line in lines])
	nof_lines = len(lines)

	for cell_num in range(max_cells):
		starting_new_block = True
		start_range = 0
		end_range = 0
		max_width = 0
		for line_num in range(nof_lines):
			# check if there's a cell to the right of this column (which means this cell ends in a tab) - we only care about terminated cells
			if _cell_exists(lines, line_num, cell_num + 1):
				# if we're at the start of a block remember what line we're on
				if starting_new_block:
					start_range = line_num
					starting_new_block = False
				# record the max width of the block so far
				max_width = max(max_width, lines[line_num][cell_num].size)
				end_range = line_num
			# if the cell has not been terminated and we're not starting a block then we're at the end of a column block
			elif not starting_new_block:
				# iterate over all cells in the block and set their width to the max width
				for block_line_num in range(start_range, end_range + 1):
					lines[block_line_num][cell_num].size = max_width
				starting_new_block = True
				max_width = 0

		# if we got to the last line without setting the size of the current block, do that now
		if not starting_new_block:
			for block_line_num in range(start_range, end_range + 1):
				lines[block_line_num][cell_num].size = max_width

	# append text and spaces to new_text
	new_text = [''] * nof_lines
	for line_num in range(nof_lines):
		if len(lines[line_num]) > 0:
			for cell_num in range(len(lines[line_num]) - 1):
				new_text[line_num] += lines[line_num][cell_num].get_padded_text()
			last_cell_num = len(lines[line_num]) - 1
			new_text[line_num] += lines[line_num][last_cell_num].text

	return '\n'.join(new_text)
