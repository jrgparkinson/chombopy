import matplotlib.pyplot as plt
from chombopy.plotting import PltFile, setup_mpl_latex
import matplotlib.cm as cm

pf = PltFile("../tests/data/plt000100.2d.hdf5")

setup_mpl_latex(14)
fig = plt.figure()
ax = plt.gca()
cmap = "viridis"
field = "Temperature"

# Get data for the temperature variable on level 2
for level in pf.get_levels():
    temperature = pf.get_level_data(field, level)

    # temperature is an xarray.DataSet object, which can be plotted using matplotlib
    x, y = pf.get_mesh_grid_for_level(level=level, grow=True)
    ax.pcolormesh(x, y, temperature, cmap=cmap)

    # Or you can do some analysis using the xarray/numpy functionality
    print(temperature.mean())


pf.plot_outlines(ax)

cbar = fig.colorbar(cm.ScalarMappable(norm=pf.get_norm(field), cmap=cmap), ax=ax)
cbar.ax.set_ylabel(field)


plt.savefig("../docs/images/plt000100.jpg")
plt.show()
