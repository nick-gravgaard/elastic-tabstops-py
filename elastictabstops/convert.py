# Copyright (c) 2007-2022 Nick Gravgaard <nick@nickgravgaard.com>
# This code is licensed under the MIT Licence - see LICENCE.txt

# This file tries to follow the Style Guide for Python Code (PEP 8) *EXCEPT*
#  * it uses tabs for indenting (like Guido used to recommend)
#  * it doesn't follow the Maximum Line Length rule
# use pylint as following: pylint --indent-string='\t' --max-line-length=1000 elastictabstops

from collections import namedtuple
import math
import re

# This code can be used to convert large amounts of text, so performance matters.
# For this reason we use namedtuples and __slots__ to create readable but well-performing data structures.

PositionedText = namedtuple('PositionedText', ['text', 'position'])

class SizedText(object):
	"""Class used to store text and the width of the cell it's in."""

	__slots__ = ['text', 'size']

	def __init__(self, text, tab_width, multiples_of_tab_width):
		self.text = text
		# size initially stores the minimum width of the cell
		# we add two to provide padding - one is not enough as it could be confused for a non-aligning space
		if multiples_of_tab_width:
			self.size = int((math.ceil((len(self.text) + 2) / float(tab_width)))) * tab_width
		else:
			self.size = max(len(self.text) + 2, tab_width)

	def get_padded_text(self):
		"""Returns self.text plus spaces to match the number of characters in self.size."""

		nof_spaces = self.size - len(self.text)
		return self.text + (' ' * nof_spaces)


def _cell_exists(list_of_lists, line_num, cell_num):
	"""Check that an item exists in a list of lists."""

	return line_num < len(list_of_lists) and cell_num < len(list_of_lists[line_num])


def _sub_tabs(line, tab_width, repl_char):
	"""Return a line of text where tab characters have been substituted with the correct number of replacement characters."""

	str_list = []
	pos = 0
	for char in line:
		if char == '\t':
			expand = tab_width - (pos % tab_width)
			str_list.append(expand * repl_char)
			pos += expand
		else:
			str_list.append(char)
			pos += 1
	return ''.join(str_list)


def _get_positions_contents(text, tab_width):
	"""Given a piece of text and how long tabs should be, return a list of lists of PositionedText named tuples."""

	repl_char = '\x1a' # the 'substitute character' in unicode
	text = '\n'.join([_sub_tabs(line, tab_width, repl_char) for line in text.split('\n')])

	# Look for a char that is (not a space or \x1a) followed by any number of chars that are either (not a space or \x1a) or a space followed by (not a space or \x1a)
	# This allows the substrings to have spaces, but only if that space is followed by a non-space char
	compiled = re.compile(r'[^%(repl_char)s\s](?:[^%(repl_char)s\s]|\s(?=[^%(repl_char)s\s]))*' % {'repl_char': repl_char})
	return [[PositionedText(match.group(), match.start()) for match in compiled.finditer(line)] for line in text.split('\n')]


def _from_spaces(text, tab_width):
	"""Convert spaces aligned text to table."""

	if not isinstance(text, str):
		raise TypeError("The first parameter of _from_spaces ('text') should be a string.")
	if not isinstance(tab_width, int):
		raise TypeError("The second parameter of _from_spaces ('tab_width') should be an integer.")
	if tab_width < 2:
		raise ValueError("The second parameter of _from_spaces ('tab_width') should be 2 or greater.")

	# '\r's before '\n's are just left at the end of lines
	# solitary '\r's aren't dealt with as these days no one uses CRs on their own for new lines
	lines = _get_positions_contents(text, tab_width)
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
						nof_cells_missing = int(block_position / tab_width)
						for _ in range(nof_cells_missing):
							# insert empty indentation cells
							lines[block_line_num].insert(cell_num, PositionedText('', 0))
							max_cells = max(max_cells, len(lines[block_line_num]))

				starting_new_block = True

		cell_num += 1

	return [([cell.text for cell in line] or ['']) for line in lines]


def _to_elastic_tabstops(table):
	"""Convert table to elastic tabstops aligned text."""

	if not isinstance(table, list):
		raise TypeError("The first parameter of _to_elastic_tabstops ('table') should be a list.")

	return '\n'.join(['\t'.join(row) for row in table])


def _to_fixed_tabstops(table, tab_width):
	"""Convert table to fixed tabstops aligned text."""

	if not isinstance(table, list):
		raise TypeError("The first parameter of _to_fixed_tabstops ('table') should be a list.")
	if not isinstance(tab_width, int):
		raise TypeError("The second parameter of _to_fixed_tabstops ('tab_width') should be an integer .")
	if tab_width < 2:
		raise ValueError("The second parameter of _to_fixed_tabstops ('tab_width') should be 2 or greater.")

	spaced_text = _to_spaces(table, tab_width, multiples_of_tab_width=True)

	lines = _get_positions_contents(spaced_text, tab_width)

	tabbed_text = []
	for line in lines:
		pos = 0
		tabbed_line = ''
		for cell in line:
			gap = cell.position - pos
			num_tabs = int(math.floor((gap + (tab_width - 1))/ tab_width))
			num_spaces = cell.position % tab_width
			tabbed_line += ('\t' * num_tabs) + (' ' * num_spaces) + cell.text
			pos = cell.position + len(cell.text)
		tabbed_text.append(tabbed_line)
	return '\n'.join(tabbed_text)


def _from_fixed_tabstops(text, tab_width):
	"""Convert fixed tabstops aligned text to table."""

	if not isinstance(text, str):
		raise TypeError("The first parameter of _from_fixed_tabstops ('text') should be a string.")
	if not isinstance(tab_width, int):
		raise TypeError("The second parameter of _from_fixed_tabstops ('tab_width') should be an integer.")
	if tab_width < 2:
		raise ValueError("The second parameter of _from_fixed_tabstops ('tab_width') should be 2 or greater.")

	expanded = text.expandtabs(tab_width)
	return _from_spaces(expanded, tab_width)


def _from_elastic_tabstops(text):
	"""Convert elastic tabstops aligned text to table."""

	if not isinstance(text, str):
		raise TypeError("The first parameter of _from_elastic_tabstops ('text') should be a string.")

	# '\r's before '\n's are just left at the end of lines
	# solitary '\r's aren't dealt with as these days no one uses CRs on their own for new lines
	return [line.split('\t') for line in text.split('\n')]


def _to_spaces(table, tab_width, multiples_of_tab_width=False):
	"""Convert table to spaces aligned text."""

	if not isinstance(table, list):
		raise TypeError("The first parameter of _to_spaces ('table') should be a list.")
	if not isinstance(tab_width, int):
		raise TypeError("The second parameter of _to_spaces ('tab_width') should be an integer .")
	if tab_width < 2:
		raise ValueError("The second parameter of _to_spaces ('tab_width') should be 2 or greater.")

	lines = [[SizedText(cell, tab_width, multiples_of_tab_width) for cell in row] for row in table]
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
