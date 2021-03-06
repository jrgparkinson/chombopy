.. chombopy documentation master file, created by
   sphinx-quickstart on Sat Mar  7 16:45:33 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


chombopy documentation
----------------------------

chombopy is a Python package for running, analysing, and plotting Chombo_ simulations.

To install:

.. code-block:: bash

   $ pip install chombopy

Then to load a Chombo output file:

.. code-block:: python

   >>> from chombopy.plotting import PltFile
   >>> plot_file = PltFile('/path/to/plt1234.hdf5')
   >>> plot_file.comp_names
   ['Enthalpy', 'Bulk concentration', 'Temperature']
    >>> plot_file.get_level_data('Temperature', level=0).mean()
   <xarray.DataArray 'Temperature' ()>
   array(1.19985756)
   Coordinates:
       level    int64 0


See below for more examples and guides.

.. _Chombo: https://commons.lbl.gov/display/chombo/Chombo+-+Software+for+Adaptive+Solutions+of+Partial+Differential+Equations




.. toctree::
   :maxdepth: 1

   installation
   examples
   plotting
   inputs
   timing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

