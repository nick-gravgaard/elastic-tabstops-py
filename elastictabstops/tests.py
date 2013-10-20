"""Test cases for testing ElasticTabstops."""

import unittest

from elastictabstops.classes import Text, Table
from elastictabstops.convert import _cell_exists, _get_positions_contents


ET_TEXT_1 = r"""
abc

	def
	ghi

		jkl
		mno

			pqr
			stu

vwx
"""

FT_TEXT_1 = r"""
abc

	def
	ghi

		jkl
		mno

			pqr
			stu

vwx
"""

SPACE_TEXT_1 = r"""
abc

        def
        ghi

                jkl
                mno

                        pqr
                        stu

vwx
"""

TABLE_1 = [
	[''],
	['abc'],
	[''],
	['', 'def'],
	['', 'ghi'],
	[''],
	['', '', 'jkl'],
	['', '', 'mno'],
	[''],
	['', '', '', 'pqr'],
	['', '', '', 'stu'],
	[''],
	['vwx'],
	[''],
]

ET_TEXT_2 = r"""aaa

	abc
	def
		ghi
		jkl

	mno
	pqr

		stu
		vwx
"""

FT_TEXT_2 = r"""aaa

	abc
	def
		ghi
		jkl

	mno
	pqr

		stu
		vwx
"""

SPACE_TEXT_2 = r"""aaa

        abc
        def
                ghi
                jkl

        mno
        pqr

                stu
                vwx
"""

TABLE_2 = [
	['aaa'],
	[''],
	['', 'abc'],
	['', 'def'],
	['', '', 'ghi'],
	['', '', 'jkl'],
	[''],
	['', 'mno'],
	['', 'pqr'],
	[''],
	['', '', 'stu'],
	['', '', 'vwx'],
	[''],
]

ET_TEXT_3 = r"""
	abc
	def

	ghi
x	jkl

	mno
xxxxxxxxx	pqr
"""

FT_TEXT_3 = r"""
	abc
	def

	ghi
x	jkl

		mno
xxxxxxxxx	pqr
"""

SPACE_TEXT_3 = r"""
        abc
        def

        ghi
x       jkl

           mno
xxxxxxxxx  pqr
"""

SPACE_TEXT_MULTIPLES_3 = r"""
        abc
        def

        ghi
x       jkl

                mno
xxxxxxxxx       pqr
"""

TABLE_3 = [
	[''],
	['', 'abc'],
	['', 'def'],
	[''],
	['', 'ghi'],
	['x', 'jkl'],
	[''],
	['', 'mno'],
	['xxxxxxxxx', 'pqr'],
	[''],
]

SPACE_TEXT_3_POSITIONS_CONTENTS = [
	[],
	[('abc', 8)],
	[('def', 8)],
	[],
	[('ghi', 8)],
	[('x', 0), ('jkl', 8)],
	[],
	[('mno', 11)],
	[('xxxxxxxxx', 0), ('pqr', 11)],
	[],
]

ET_TEXT_4 = r"""
	abc
	def	ghi
	jkl	mno
	pqr
"""

FT_TEXT_4 = r"""
	abc
	def	ghi
	jkl	mno
	pqr
"""

SPACE_TEXT_4 = r"""
        abc
        def     ghi
        jkl     mno
        pqr
"""

TABLE_4 = [
	[''],
	['', 'abc'],
	['', 'def', 'ghi'],
	['', 'jkl', 'mno'],
	['', 'pqr'],
	[''],
]

ET_TEXT_5 = r"""
	abc
	def	ghi
	jkl	mno
	pqr"""

FT_TEXT_5 = r"""
	abc
	def	ghi
	jkl	mno
	pqr"""

SPACE_TEXT_5 = r"""
        abc
        def     ghi
        jkl     mno
        pqr"""

TABLE_5 = [
	[''],
	['', 'abc'],
	['', 'def', 'ghi'],
	['', 'jkl', 'mno'],
	['', 'pqr'],
]

ET_TEXT_6 = r"""// eeeeeeee.cpp : Defines the entry point for the console application.
//

#include \"stdafx.h\"


int _tmain(int argc, _TCHAR* argv[])
{
	return 0;
	kkkkkkkkkkkkkk	kkkkkkkk
	llllllllllllllllllllll	llllllllllll

	aa	bb	cc
	a	b	c
}

"""

FT_TEXT_6 = r"""// eeeeeeee.cpp : Defines the entry point for the console application.
//

#include \"stdafx.h\"


int _tmain(int argc, _TCHAR* argv[])
{
	return 0;
	kkkkkkkkkkkkkk		kkkkkkkk
	llllllllllllllllllllll	llllllllllll

	aa	bb	cc
	a	b	c
}

"""

SPACE_TEXT_6 = r"""// eeeeeeee.cpp : Defines the entry point for the console application.
//

#include \"stdafx.h\"


int _tmain(int argc, _TCHAR* argv[])
{
                return 0;
                kkkkkkkkkkkkkk          kkkkkkkk
                llllllllllllllllllllll  llllllllllll

                aa              bb              cc
                a               b               c
}

"""

SPACE_TEXT_MULTIPLES_6 = r"""// eeeeeeee.cpp : Defines the entry point for the console application.
//

#include \"stdafx.h\"


int _tmain(int argc, _TCHAR* argv[])
{
                return 0;
                kkkkkkkkkkkkkk                  kkkkkkkk
                llllllllllllllllllllll          llllllllllll

                aa              bb              cc
                a               b               c
}

"""

TABLE_6 = [
	['// eeeeeeee.cpp : Defines the entry point for the console application.'],
	['//'],
	[''],
	['#include \\"stdafx.h\\"'],
	[''],
	[''],
	['int _tmain(int argc, _TCHAR* argv[])'],
	['{'],
	['', 'return 0;'],
	['', 'kkkkkkkkkkkkkk', 'kkkkkkkk'],
	['', 'llllllllllllllllllllll', 'llllllllllll'],
	[''],
	['', 'aa', 'bb', 'cc'],
	['', 'a', 'b', 'c'],
	['}'],
	[''],
	[''],
]

ET_TEXT_7 = r"""	Hallo
	Pupallo
	Gugu	gaga
	hhghga	hghghhghg
	adsdasdasdasda		ghghghgghghg
"""

FT_TEXT_7 = r"""	Hallo
	Pupallo
	Gugu		gaga
	hhghga		hghghhghg
	adsdasdasdasda		ghghghgghghg
"""

SPACE_TEXT_7 = r"""        Hallo
        Pupallo
        Gugu            gaga
        hhghga          hghghhghg
        adsdasdasdasda          ghghghgghghg
"""

SPACE_TEXT_MULTIPLES_7 = r"""        Hallo
        Pupallo
        Gugu            gaga
        hhghga          hghghhghg
        adsdasdasdasda          ghghghgghghg
"""

TABLE_7 = [
	['', 'Hallo'],
	['', 'Pupallo'],
	['', 'Gugu', 'gaga'],
	['', 'hhghga', 'hghghhghg'],
	['', 'adsdasdasdasda', '', 'ghghghgghghg'],
	[''],
]

ET_TEXT_8 = """	push
		(
		@{$self->{struct}},
			{
			source	=> $source,
			filename	=> $filename,
			pathname	=> $pathname,
			lang	=> $lang,
			level	=> $level,
			back	=> $back,
			url	=> $url,
			modified	=> $modified,
			id	=> Digest::MD5::md5_hex($url),
			file	=> $file,
			}
		);
	}
"""

# tab_width = 4
FT_TEXT_8 = """	push
		(
		@{$self->{struct}},
			{
			source		=> $source,
			filename	=> $filename,
			pathname	=> $pathname,
			lang		=> $lang,
			level		=> $level,
			back		=> $back,
			url			=> $url,
			modified	=> $modified,
			id			=> Digest::MD5::md5_hex($url),
			file		=> $file,
			}
		);
	}
"""

SPACE_TEXT_8 = """    push
        (
        @{$self->{struct}},
            {
            source    => $source,
            filename  => $filename,
            pathname  => $pathname,
            lang      => $lang,
            level     => $level,
            back      => $back,
            url       => $url,
            modified  => $modified,
            id        => Digest::MD5::md5_hex($url),
            file      => $file,
            }
        );
    }
"""

SPACE_TEXT_MULTIPLES_8 = """    push
        (
        @{$self->{struct}},
            {
            source      => $source,
            filename    => $filename,
            pathname    => $pathname,
            lang        => $lang,
            level       => $level,
            back        => $back,
            url         => $url,
            modified    => $modified,
            id          => Digest::MD5::md5_hex($url),
            file        => $file,
            }
        );
    }
"""

TABLE_8 = [
	['', 'push'],
	['', '', '('],
	['', '', '@{$self->{struct}},'],
	['', '', '', '{'],
	['', '', '', 'source', '=> $source,'],
	['', '', '', 'filename', '=> $filename,'],
	['', '', '', 'pathname', '=> $pathname,'],
	['', '', '', 'lang', '=> $lang,'],
	['', '', '', 'level', '=> $level,'],
	['', '', '', 'back', '=> $back,'],
	['', '', '', 'url', '=> $url,'],
	['', '', '', 'modified', '=> $modified,'],
	['', '', '', 'id', '=> Digest::MD5::md5_hex($url),'],
	['', '', '', 'file', '=> $file,'],
	['', '', '', '}'],
	['', '', ');'],
	['', '}'],
	[''],
]

SPACE_TEXT_9 = r"""
/* Hopefully this Java program should demonstrate how elastic tabstops work.               */
/* Try inserting and deleting different parts of the text and watch as the tabstops move.  */
/* If you like this, please ask the writers of your text editor to implement it.           */
"""

SPACE_TEXT_9_POSITIONS_CONTENTS = [
	[],
	[('/* Hopefully this Java program should demonstrate how elastic tabstops work.', 0), ('*/', 91)],
	[('/* Try inserting and deleting different parts of the text and watch as the tabstops move.', 0), ('*/', 91)],
	[('/* If you like this, please ask the writers of your text editor to implement it.', 0), ('*/', 91)],
	[],
]


ET_TEXT_10 = r"""
/* Hopefully this Java program should demonstrate how elastic tabstops work.	*/
/* Try inserting and deleting different parts of the text and watch as the tabstops move.	*/
/* If you like this, please ask the writers of your text editor to implement it.	*/

#include <stdio.h>

struct ipc_perm
{
	key_t	key;
	ushort	uid;	/* owner euid and egid	*/
	ushort	gid;	/* group id	*/
	ushort	cuid;	/* creator euid and egid	*/
	cell-missing		/* for test purposes	*/
	ushort	mode;	/* access modes	*/
	ushort	seq;	/* sequence number	*/
};

int someDemoCode(	int fred,
	int wilma)
{
	x();	/* try making	*/
	printf("hello!\n");	/* this comment	*/
	doSomethingComplicated();	/* a bit longer	*/
	for (i = start; i < end; ++i)
	{
		if (isPrime(i))
		{
			++numPrimes;
		}
	}
	return numPrimes;
}

---- and now for something completely different: a table ----

Title	Author	Publisher	Year
Generation X	Douglas Coupland	Abacus	1995
Informagic	Jean-Pierre Petit	John Murray Ltd	1982
The Cyberiad	Stanislaw Lem	Harcourt Publishers Ltd	1985
The Selfish Gene	Richard Dawkins	Oxford University Press	2006
"""

FT_TEXT_10 = r"""
/* Hopefully this Java program should demonstrate how elastic tabstops work.			*/
/* Try inserting and deleting different parts of the text and watch as the tabstops move.	*/
/* If you like this, please ask the writers of your text editor to implement it.		*/

#include <stdio.h>

struct ipc_perm
{
	key_t		key;
	ushort		uid;	/* owner euid and egid		*/
	ushort		gid;	/* group id			*/
	ushort		cuid;	/* creator euid and egid	*/
	cell-missing		/* for test purposes		*/
	ushort		mode;	/* access modes			*/
	ushort		seq;	/* sequence number		*/
};

int someDemoCode(	int fred,
			int wilma)
{
	x();				/* try making		*/
	printf("hello!\n");		/* this comment		*/
	doSomethingComplicated();	/* a bit longer		*/
	for (i = start; i < end; ++i)
	{
		if (isPrime(i))
		{
			++numPrimes;
		}
	}
	return numPrimes;
}

---- and now for something completely different: a table ----

Title			Author			Publisher			Year
Generation X		Douglas Coupland	Abacus				1995
Informagic		Jean-Pierre Petit	John Murray Ltd			1982
The Cyberiad		Stanislaw Lem		Harcourt Publishers Ltd		1985
The Selfish Gene	Richard Dawkins		Oxford University Press		2006
"""

SPACE_TEXT_10 = r"""
/* Hopefully this Java program should demonstrate how elastic tabstops work.               */
/* Try inserting and deleting different parts of the text and watch as the tabstops move.  */
/* If you like this, please ask the writers of your text editor to implement it.           */

#include <stdio.h>

struct ipc_perm
{
        key_t         key;
        ushort        uid;    /* owner euid and egid    */
        ushort        gid;    /* group id               */
        ushort        cuid;   /* creator euid and egid  */
        cell-missing          /* for test purposes      */
        ushort        mode;   /* access modes           */
        ushort        seq;    /* sequence number        */
};

int someDemoCode(  int fred,
                   int wilma)
{
        x();                       /* try making    */
        printf("hello!\n");        /* this comment  */
        doSomethingComplicated();  /* a bit longer  */
        for (i = start; i < end; ++i)
        {
                if (isPrime(i))
                {
                        ++numPrimes;
                }
        }
        return numPrimes;
}

---- and now for something completely different: a table ----

Title             Author             Publisher                Year
Generation X      Douglas Coupland   Abacus                   1995
Informagic        Jean-Pierre Petit  John Murray Ltd          1982
The Cyberiad      Stanislaw Lem      Harcourt Publishers Ltd  1985
The Selfish Gene  Richard Dawkins    Oxford University Press  2006
"""

SPACE_TEXT_MULTIPLES_10 = r"""
/* Hopefully this Java program should demonstrate how elastic tabstops work.                    */
/* Try inserting and deleting different parts of the text and watch as the tabstops move.       */
/* If you like this, please ask the writers of your text editor to implement it.                */

#include <stdio.h>

struct ipc_perm
{
        key_t           key;
        ushort          uid;    /* owner euid and egid          */
        ushort          gid;    /* group id                     */
        ushort          cuid;   /* creator euid and egid        */
        cell-missing            /* for test purposes            */
        ushort          mode;   /* access modes                 */
        ushort          seq;    /* sequence number              */
};

int someDemoCode(       int fred,
                        int wilma)
{
        x();                            /* try making           */
        printf("hello!\n");             /* this comment         */
        doSomethingComplicated();       /* a bit longer         */
        for (i = start; i < end; ++i)
        {
                if (isPrime(i))
                {
                        ++numPrimes;
                }
        }
        return numPrimes;
}

---- and now for something completely different: a table ----

Title                   Author                  Publisher                       Year
Generation X            Douglas Coupland        Abacus                          1995
Informagic              Jean-Pierre Petit       John Murray Ltd                 1982
The Cyberiad            Stanislaw Lem           Harcourt Publishers Ltd         1985
The Selfish Gene        Richard Dawkins         Oxford University Press         2006
"""

TABLE_10 = [
	[''],
	['/* Hopefully this Java program should demonstrate how elastic tabstops work.', '*/'],
	['/* Try inserting and deleting different parts of the text and watch as the tabstops move.', '*/'],
	['/* If you like this, please ask the writers of your text editor to implement it.', '*/'],
	[''],
	['#include <stdio.h>'],
	[''],
	['struct ipc_perm'],
	['{'],
	['', 'key_t', 'key;'],
	['', 'ushort', 'uid;', '/* owner euid and egid', '*/'],
	['', 'ushort', 'gid;', '/* group id', '*/'],
	['', 'ushort', 'cuid;', '/* creator euid and egid', '*/'],
	['', 'cell-missing', '', '/* for test purposes', '*/'],
	['', 'ushort', 'mode;', '/* access modes', '*/'],
	['', 'ushort', 'seq;', '/* sequence number', '*/'],
	['};'],
	[''],
	['int someDemoCode(', 'int fred,'],
	['', 'int wilma)'],
	['{'],
	['', 'x();', '/* try making', '*/'],
	['', 'printf("hello!\\n");', '/* this comment', '*/'],
	['', 'doSomethingComplicated();', '/* a bit longer', '*/'],
	['', 'for (i = start; i < end; ++i)'],
	['', '{'],
	['', '', 'if (isPrime(i))'],
	['', '', '{'],
	['', '', '', '++numPrimes;'],
	['', '', '}'],
	['', '}'],
	['', 'return numPrimes;'],
	['}'],
	[''],
	['---- and now for something completely different: a table ----'],
	[''],
	['Title', 'Author', 'Publisher', 'Year'],
	['Generation X', 'Douglas Coupland', 'Abacus', '1995'],
	['Informagic', 'Jean-Pierre Petit', 'John Murray Ltd', '1982'],
	['The Cyberiad', 'Stanislaw Lem', 'Harcourt Publishers Ltd', '1985'],
	['The Selfish Gene', 'Richard Dawkins', 'Oxford University Press', '2006'],
	[''],
]

#def show_diffs(string1, string2):
#	import difflib
#	print(''.join(difflib.unified_diff(string1, string2)))


def show_diffs(string1, string2):
	"""
	Unify operations between two compared strings
	see: http://stackoverflow.com/questions/774316/python-difflib-highlighting-differences-inline
	"""
	import difflib
	seqm = difflib.SequenceMatcher(None, string1, string2)
	changed = False
	output = []
	for opcode, a_0, a_1, b_0, b_1 in seqm.get_opcodes():
		if opcode == 'equal':
			output.append(seqm.a[a_0:a_1])
		elif opcode == 'insert':
			output.append("<ins>" + seqm.b[b_0:b_1] + "</ins>")
			changed = True
		elif opcode == 'delete':
			output.append("<del>" + seqm.a[a_0:a_1] + "</del>")
			changed = True
		elif opcode == 'replace':
			#raise NotImplementedError, "what to do with 'replace' opcode?"
			output.append("<rep>" + seqm.a[a_0:a_1] + "<became>" + seqm.a[b_0:b_1] + "</rep>")
			changed = True
		else:
			raise RuntimeError("unexpected opcode")
	if changed:
		print(''.join(output))


def show_debug_info(string1, string2):
	"""Show differences and other debug info about 2 strings."""
	show_diffs(string1, string2)
	if string1 != string2:
		print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv string 1 vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
		print(string1)
		print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ string 1 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
		print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv string 2 vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
		print(string2)
		print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ string 2 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')


TEST_STRINGS_LIST = [
	{'et_text': ET_TEXT_1, 'ft_text': FT_TEXT_1, 'space_text': SPACE_TEXT_1, 'table': TABLE_1, 'tab_width': 8},
	{'et_text': ET_TEXT_2, 'ft_text': FT_TEXT_2, 'space_text': SPACE_TEXT_2, 'table': TABLE_2, 'tab_width': 8},
	{'et_text': ET_TEXT_3, 'ft_text': FT_TEXT_3, 'space_text': SPACE_TEXT_3, 'space_text_multiples': SPACE_TEXT_MULTIPLES_3, 'table': TABLE_3, 'tab_width': 8},
	{'et_text': ET_TEXT_4, 'ft_text': FT_TEXT_4, 'space_text': SPACE_TEXT_4, 'table': TABLE_4, 'tab_width': 8},
	{'et_text': ET_TEXT_5, 'ft_text': FT_TEXT_5, 'space_text': SPACE_TEXT_5, 'table': TABLE_5, 'tab_width': 8},
	{'et_text': ET_TEXT_6, 'ft_text': FT_TEXT_6, 'space_text': SPACE_TEXT_6, 'space_text_multiples': SPACE_TEXT_MULTIPLES_6, 'table': TABLE_6, 'tab_width': 16},
	{'et_text': ET_TEXT_7, 'ft_text': FT_TEXT_7, 'space_text': SPACE_TEXT_7, 'space_text_multiples': SPACE_TEXT_MULTIPLES_7, 'table': TABLE_7, 'tab_width': 8},
	{'et_text': ET_TEXT_8, 'ft_text': FT_TEXT_8, 'space_text': SPACE_TEXT_8, 'space_text_multiples': SPACE_TEXT_MULTIPLES_8, 'table': TABLE_8, 'tab_width': 4},
	{'et_text': ET_TEXT_10, 'ft_text': FT_TEXT_10, 'space_text': SPACE_TEXT_10, 'space_text_multiples': SPACE_TEXT_MULTIPLES_10, 'table': TABLE_10, 'tab_width': 8},
]


class TestElasticTabstops(unittest.TestCase):
	"""Test case for testing ElasticTabstops."""

	def test_type_value_errors(self):
		"""Test to_elastic_tabstops()."""
		with self.assertRaises(TypeError):
			Text(99)
		with self.assertRaises(TypeError):
			Text('abc').from_spaces(tab_width='')
		with self.assertRaises(TypeError):
			Text('abc').from_fixed_tabstops(tab_width='')
		with self.assertRaises(TypeError):
			Table(99)
		with self.assertRaises(TypeError):
			Table([['abc']]).to_spaces(tab_width='')
		with self.assertRaises(TypeError):
			Table([['abc']]).to_fixed_tabstops(tab_width='')

		with self.assertRaises(ValueError):
			Text('abc').from_spaces(1)
		with self.assertRaises(ValueError):
			Text('abc').from_fixed_tabstops(tab_width=1)
		with self.assertRaises(ValueError):
			Table([['abc']]).to_spaces(tab_width=1)

	def test_to_elastic_tabstops(self):
		"""Test to_elastic_tabstops()."""
		for test_strings in TEST_STRINGS_LIST:
			orig_elastic = test_strings['et_text']
			new_elastic = Table(test_strings['table']).to_elastic_tabstops()
			self.assertEqual(orig_elastic, new_elastic, show_debug_info(orig_elastic, new_elastic))

			orig_table = test_strings['table']
			new_table = Text(test_strings['et_text']).from_elastic_tabstops()
			self.assertEqual(orig_table, new_table)

	def test_to_fixed_tabstops(self):
		"""Test to_fixed_tabstops()."""
		for test_strings in TEST_STRINGS_LIST:
			orig_fixed = test_strings['ft_text']
			new_fixed = Table(test_strings['table']).to_fixed_tabstops(test_strings['tab_width'])
			self.assertEqual(orig_fixed, new_fixed, show_debug_info(orig_fixed, new_fixed))

			orig_table = test_strings['table']
			new_table = Text(test_strings['ft_text']).from_fixed_tabstops(test_strings['tab_width'])
			self.assertEqual(orig_table, new_table)

	def test_to_spaces(self):
		"""Test to_spaces()."""
		for test_strings in TEST_STRINGS_LIST:
			orig_spaces = test_strings['space_text']
			new_spaces = Table(test_strings['table']).to_spaces(test_strings['tab_width'])
			self.assertEqual(orig_spaces, new_spaces, show_debug_info(orig_spaces, new_spaces))

			if 'space_text_multiples' in test_strings:
				orig_spaces_multiples = test_strings['space_text_multiples']
				new_spaces_multiples = Table(test_strings['table']).to_spaces(test_strings['tab_width'], multiples_of_tab_width=True)
				self.assertEqual(orig_spaces_multiples, new_spaces_multiples, show_debug_info(orig_spaces_multiples, new_spaces_multiples))

			orig_table = test_strings['table']
			new_table = Text(test_strings['space_text']).from_spaces(test_strings['tab_width'])
			self.assertEqual(orig_table, new_table)

	def test_cell_exists(self):
		"""Test _cell_exists()."""
		list_of_lists = [[], [1], [2, 3], [4, 5, 6], ]
		self.assertFalse(_cell_exists(list_of_lists, 0, 0))
		self.assertFalse(_cell_exists(list_of_lists, 1, 1))
		self.assertFalse(_cell_exists(list_of_lists, 2, 2))
		self.assertFalse(_cell_exists(list_of_lists, 3, 3))
		self.assertFalse(_cell_exists(list_of_lists, 4, 0))
		self.assertTrue(_cell_exists(list_of_lists, 1, 0))
		self.assertTrue(_cell_exists(list_of_lists, 2, 1))
		self.assertTrue(_cell_exists(list_of_lists, 3, 2))

	def test_get_positions_contents(self):
		"""Test _get_positions_contents()."""
		self.assertEqual(_get_positions_contents(SPACE_TEXT_3, 8), SPACE_TEXT_3_POSITIONS_CONTENTS)
		self.assertEqual(_get_positions_contents(SPACE_TEXT_9, 8), SPACE_TEXT_9_POSITIONS_CONTENTS)


if __name__ == '__main__':
	unittest.main()
