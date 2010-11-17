"""
ElasticTabstops package
Provides functionality for handling text indented/aligned with elastic tabstops
see: http://nickgravgaard.com/elastictabstops/
"""

# Copyright (c) 2007-2010 Nick Gravgaard <me@nickgravgaard.com>
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

from __future__ import division # means dividing 2 ints will give us a float rather than an int
import math
import re

__all__ = ['to_elastic_tabstops', 'to_spaces']


def _cell_exists(list_of_lists, line_num, cell_num):
	"""Check that an item exists in a list of lists."""
	return True if line_num < len(list_of_lists) and cell_num < len(list_of_lists[line_num]) else False


def _calc_fixed_cell_size(text_len, tab_size):
	"""Given the length of the text inside a cell, return the size the cell should be."""

	# we add two to provide padding - one is not enough as it could be confused for a non-aligning space
	assert(tab_size)
	return int((math.ceil((text_len + 2) / tab_size))) * tab_size


def _get_positions_contents(text, tab_size):

	def sub_tabs(line, tab_size, repl_char):
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

	repl_char = '\x1a' # the 'substitute character'
	text = '\n'.join([sub_tabs(line, tab_size, repl_char) for line in text.split('\n')])

	# Look for a char that is (not a space or \x1a) followed by any number of chars that are either (not a space or \x1a) or a space followed by (not a space or \x1a)
	# This allows the substrings to have spaces, but only if that space is followed by a non-space char
	p = re.compile(r'[^%(repl_char)s\s](?:[^%(repl_char)s\s]|\s(?=[^%(repl_char)s\s]))*' % {'repl_char': repl_char})
	return [[(m.start(), m.group()) for m in p.finditer(line)] for line in text.split('\n')]


def to_elastic_tabstops(text, tab_size=8):
	"""Convert text from using spaces to using tabs with elastic tabstops."""

	# '\r's before '\n's are just left at the end of lines
	# solitary '\r's aren't dealt with as no one has pre Mac OS X files anymore
	lines_cells = _get_positions_contents(text, tab_size)
	max_cells = max([len(line) for line in lines_cells])
	nof_lines = len(lines_cells)

	# not a "for cell_num in (range(max_cells)):" loop because max_cells may increase 
	cell_num = 0
	while cell_num < max_cells:
		starting_new_block = True
		start_range = 0
		end_range = 0

		for line_num in range(nof_lines + 1):
			if _cell_exists(lines_cells, line_num, cell_num):
				if starting_new_block is True:
					start_range = line_num
					starting_new_block = False
				end_range = line_num
			else:
				# end column block
				if starting_new_block is False:
					sliced_list = [lines_cells[blockcell_num][cell_num][0] for blockcell_num in range(start_range, end_range + 1)]

					min_indent = min(sliced_list)

					for blockcell_num, blockcell in enumerate(sliced_list):
						if blockcell > min_indent:
							# shift cells across
							lines_cells[start_range + blockcell_num].insert(cell_num, (0, ''))
							max_cells = max(max_cells, len(lines_cells[start_range + blockcell_num]))
						elif cell_num == 0 and blockcell > 1:
							for i in range(int(blockcell / tab_size)):
								# insert empty indentation cells
								lines_cells[start_range + blockcell_num].insert(cell_num, (0, ''))
								max_cells = max(max_cells, len(lines_cells[start_range + blockcell_num]))

					starting_new_block = True

		cell_num += 1

	return '\n'.join(['\t'.join([cell[1] for cell in line]) for line in lines_cells])


def to_spaces(text, tab_size=8):
	"""Convert text from using tabs with elastic tabstops to using spaces."""

	# '\r's before '\n's are just left at the end of lines
	# solitary '\r's aren't dealt with as no one has pre Mac OS X files anymore
	lines = [line.split('\t') for line in text.split('\n')]
	sizes = [[_calc_fixed_cell_size(len(cell), tab_size) for cell in line] for line in lines]
	max_cells = max([len(line) for line in lines])
	nof_lines = len(lines)

	for cell_num in range(max_cells):
		starting_new_block = True
		start_range = 0
		end_range = 0
		max_width = 0
		for line_num in range(nof_lines):
			if _cell_exists(sizes, line_num, cell_num + 1) and _cell_exists(sizes, line_num, cell_num):
				if starting_new_block is True:
					start_range = line_num
					starting_new_block = False
				max_width = max(max_width, sizes[line_num][cell_num])
				end_range = line_num
			else:
				# end column block
				if starting_new_block is False:
					for blockcell_num in range(start_range, end_range + 1):
						sizes[blockcell_num][cell_num] = max_width
					starting_new_block = True
					max_width = 0

		if starting_new_block is False:
			for blockcell_num in range(start_range, end_range + 1):
				sizes[blockcell_num][cell_num] = max_width

	# append text and spaces to new_text
	new_text = [''] * nof_lines
	for line_num in range(nof_lines):
		for cell_num in range(max_cells):
			try:
				if cell_num < len(lines[line_num]) - 1:
					nof_spaces = sizes[line_num][cell_num] - len(lines[line_num][cell_num])
					new_text[line_num] += lines[line_num][cell_num] + (' ' * nof_spaces)
				else:
					new_text[line_num] += lines[line_num][cell_num]
			except IndexError:
				pass

	return '\n'.join(new_text)
