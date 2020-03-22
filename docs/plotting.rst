Plotting
==========

The core of the plotting module is the PltFile object, which represents a Chombo HDF5 output file.

.. code-block:: python

    >>> from chombopy.plotting import PltFile
    >>> pf = PltFile('plt000100.2d.hdf5')

N-dimensional volumetric data on each level of refinement is represented by an xarray.DataSet object, which can be analysed and plotted using standard Python packages.

.. code-block:: python

    >>> pf.comp_names
    ['Enthalpy', 'Bulk concentration', 'Temperature', 'Porosity', 'Liquid concentration', 'streamfunction', 'Permeability', 'lambda', 'Pressure', 'xDarcy velocity', 'yDarcy velocity', 'xAdvection velocity', 'yAdvection velocity', 'xFs', 'yFs']
    >>> pf.get_level_data('Enthalpy', 0)
    <xarray.DataArray 'Enthalpy' (y: 16, x: 16)>


Reference
----------

.. automodule:: chombopy.plotting
   :members: