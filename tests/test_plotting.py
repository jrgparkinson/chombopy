import unittest
from chombopy.plotting import PltFile
import matplotlib.pyplot as plt
import logging
import os


class TestPltFile(unittest.TestCase):
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    DATA_FILE = os.path.join(THIS_DIR, "data/plt000100.2d.hdf5")
    CHK_DATA_FILE = os.path.join(THIS_DIR, "data/chk000100.2d.hdf5")
    DATA_FILE_3D = os.path.join(THIS_DIR, "data/3D/plt000100.3d.hdf5")

    def test_load(self):

        # Test loading a file that doesn't exist
        pf = PltFile("file that does not exist")
        self.assertEqual(pf.defined, False)

        # Test loading a file that does exist
        pf = PltFile(self.DATA_FILE, load_data=True)
        self.assertEqual(pf.num_levels, 3)
        self.assertEqual(pf.plot_prefix, "plt")
        self.assertEqual(pf.frame, 100)

        # Test pretty printing object
        logging.info(pf)

        # Test loading after data already loaded (should do nothing)
        pf.load_data()

        # Check data is correct
        pf.load_data()
        max_enthalpy = float(pf.get_level_data("Enthalpy", level=0).max())
        self.assertAlmostEqual(max_enthalpy, 6.302214, 6)
        max_enthalpy = float(pf.get_level_data("Enthalpy", level=2).max())
        self.assertAlmostEqual(max_enthalpy, 6.307355035152367, 6)

        # Test removing data
        pf.unload_data()
        self.assertEqual(pf.data_loaded, False)

        pf_no_name = PltFile("data/pltnoframe.2d.hdf5")
        self.assertEqual(pf_no_name.frame, -1)

        pf_no_inputs = PltFile("data/plt000100.2d.hdf5", inputs_file="does not exist")
        self.assertIsNone(pf_no_inputs.inputs)

        # Checkpoint files
        cf = PltFile(self.CHK_DATA_FILE, load_data=True)

    def test_plotting(self):
        pf = PltFile(self.DATA_FILE)
        pf.load_data(zero_x=True)
        porosity = pf.get_level_data("Porosity")

        fig = plt.figure()
        ax = fig.gca()
        ax.pcolormesh(porosity.x, porosity.y, porosity)

        # Can only execute these tests if latex is installed
        if is_installed('latex'):
            pf.plot_outlines(ax)
            pf.plot_field("Porosity")


    def test_3d(self):
        pf = PltFile(self.DATA_FILE_3D, load_data=True)

        porosity = pf.get_level_data("Porosity")
        coords = porosity.coords
        x = coords["x"]
        y = coords["y"]
        z = coords["y"]

        self.assertEqual(pf.space_dim, 3)
        self.assertEqual(len(z), 32)
        self.assertEqual(len(x), 32)
        self.assertEqual(len(y), 32)

    def test_static_methods(self):
        pf = PltFile(self.DATA_FILE, load_data=True)

        x, y = pf.get_mesh_grid()
        self.assertEqual(len(x), 16)

        x, y = pf.get_mesh_grid(extend_grid=False)
        self.assertEqual(len(x), 15)

        porosity = pf.get_level_data("Porosity")
        x, y = PltFile.get_mesh_grid_n(porosity)
        self.assertEqual(len(x), 16)

def is_installed(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None

if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPltFile)
    unittest.TextTestRunner(verbosity=2).run(suite)
