Inputs
============

Inputs for Chombo simulation take the form of a text file listing parameters and their values, e.g.

.. code-block:: text

    main.num_cells=16 16 16
    main.verbosity=1
    main.max_time=0.4
    main.plt_prefix=plt

The chombopy.inputs package provides utilities for reading, modifying, and writing these input files.

.. code-block:: python

    >>> from chombopy.inputs import read_inputs, write_inputs
    >>> inputs = read_inputs('/path/to/inputs')

Inputs are stored in appropriate python objects, i.e.

.. code-block:: python

    >>> inputs['main.num_cells']
    [16, 16, 16]
    >>> inputs['main.plt_prefix'])
    'plt'
    >>> inputs['main.verbosity']
    0

You can edit them

.. code-block:: python

    inputs['main.verbosity'] = 1

And then write them back out

.. code-block:: python

    write_inputs('/path/to/new_inputs', inputs)


Reference
----------

.. automodule:: chombopy.inputs
   :members: