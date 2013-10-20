Description
===========

This package provides functionality for handling text indented/aligned with elastic tabstops. If you have an editor which uses elastic tabstops but work on a project that uses spaces, you might use this to convert a file from using spaces to using elastic tabstops, edit it in an elastic tabstops enabled editor and then convert it back to using spaces before saving to disk.

Alternatively, it can be a nice way to create text from tables of data.

Usage
=====

Instantiate a Text object with the string one wants to convert, and then call one of the from_* methods to create a Table object. Table objects have to_* methods which can be called to create new Text objects.

Text methods are from_spaces, from_elastic_tabstops and from_fixed_tabstops, while Table methods are to_spaces, to_elastic_tabstops and to_fixed_tabstops.

So, to convert text from using spaces to using tabs with elastic tabstops one might use the following:

.. code:: python

    from elastictabstops import Text
    elastic_text = Text(spaces_text).from_spaces().to_elastic_tabstops()

Whereas to convert text from using tabs with elastic tabstops to using spaces the following might be used:

.. code:: python

    from elastictabstops import Text
    spaces_text = Text(elastic_text).from_elastic_tabstops().to_spaces()
    # or alternatively
    spaces_text = Text(elastic_text).from_elastic_tabstops().to_spaces(multiples_of_tab_width=True)

If you want to use this package to print a table of strings you can use something like this:

.. code:: python

    from elastictabstops import Table
    my_table = [
        ['Title', 'Author', 'Publisher', 'Year'],
	['Generation X', 'Douglas Coupland', 'Abacus', '1995'],
	['Informagic', 'Jean-Pierre Petit', 'John Murray Ltd', '1982'],
	['The Cyberiad', 'Stanislaw Lem', 'Harcourt Publishers Ltd', '1985'],
	['The Selfish Gene', 'Richard Dawkins', 'Oxford University Press', '2006'],
    ]
    spaces_text = Table(my_table).to_spaces()
    # or if you're displaying the text in a widget which understands elastic tabstops
    elastic_text = Table(my_table).to_elastic_tabstops()

If you have aligned text which you'd like to get a table from you can do things like this:

.. code:: python

    from elastictabstops import Text
    table = Text(elastic_text).from_elastic_tabstops()
    table = Text(fixed_text).from_fixed_tabstops()
    table = Text(spaces_text).from_spaces()

Author and licence
==================

This package is by Nick Gravgaard and is licensed under an MIT/X11 licence.
