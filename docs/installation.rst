Installation
=============


chombopy can be most easily installed from PyPI using pip:

.. code-block:: bash

   $ pip install chombopy

Alternatively, you can download the code and install manually:

.. code-block:: bash

    $ git clone https://github.com/jrgparkinson/chombopy.git
    $ cd chombopy
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ python setup.py install

Which will then allow you to run the tests with pytest:

.. code-block:: bash

    $ py.test

Or compile the documentation locally:

.. code-block:: bash

    $ cd docs
    $ make html

