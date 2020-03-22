import unittest
from chombopy.plotting import PltFile
import matplotlib.pyplot as plt
import logging
import os
import numpy as np

class ChildPltFileForTesting(PltFile):

    def __init__(self, filename):
        super().__init__(filename)


    def should_negate_field_upon_reflection(self, field):
        if field in ['streamfunction'] or field[0] == 'x':
            return True

        return False

class TestPltFile(unittest.TestCase):
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    DATA_FILE = os.path.join(THIS_DIR, "data/plt000100.2d.hdf5")
    CHK_DATA_FILE = os.path.join(THIS_DIR, "data/chk000100.2d.hdf5")
    DATA_FILE_3D = os.path.join(THIS_DIR, "data/3D/plt000100.3d.hdf5")
    DATA_FILE_3D_CHK = os.path.join(THIS_DIR, "data/3D/chk000100.3d.hdf5")
    DATA_FILE_NO_FRAME = os.path.join(THIS_DIR, "data/pltnoframe.2d.hdf5")

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
        for pf in [PltFile(self.CHK_DATA_FILE), PltFile(self.DATA_FILE)]:
            pf.load_data()
            max_enthalpy = float(pf.get_level_data("Enthalpy", level=0).max())
            self.assertAlmostEqual(max_enthalpy, 6.302214, 6)
            max_enthalpy = float(pf.get_level_data("Enthalpy", level=2).max())
            self.assertAlmostEqual(max_enthalpy, 6.307355035152367, 6)

            # Test removing data
            pf.unload_data()
            self.assertEqual(pf.data_loaded, False)

            pf.load_data(zero_x=True)
            assert pf.get_level_data('Enthalpy').coords['x'][0] == 0

        pf_no_name = PltFile(self.DATA_FILE_NO_FRAME)
        self.assertEqual(pf_no_name.frame, -1)

        pf_no_inputs = PltFile(self.DATA_FILE, inputs_file="does not exist")
        self.assertIsNone(pf_no_inputs.inputs)
        assert str(pf_no_inputs) == '<PltFile object for %s>' % self.DATA_FILE

    def test_get_level_data(self):
        pf = PltFile(self.DATA_FILE)

        assert pf.num_levels == 3
        assert pf.get_level_data('does not exist') is None

        valid_only = pf.get_level_data('Porosity', valid_only=True)
        all_data = pf.get_level_data('Porosity', valid_only=False)

        assert len(valid_only.coords['x']) == 16
        assert len(valid_only.coords['y']) == 16
        assert np.isnan(valid_only[5,5])
        assert not all_data.equals(valid_only)

        valid_only = pf.get_level_data('Porosity', level=1, valid_only=True)
        all_data = pf.get_level_data('Porosity', level=1, valid_only=False)
        assert len(valid_only.coords['x']) == 32
        assert len(valid_only.coords['y']) == 24
        assert np.isnan(valid_only[20,20])
        assert not all_data.equals(valid_only)

        valid_only = pf.get_level_data('Porosity', level=2, valid_only=True)
        all_data = pf.get_level_data('Porosity', level=2, valid_only=False)
        assert len(valid_only.coords['x']) == 64
        assert len(valid_only.coords['y']) == 40
        assert valid_only.equals(all_data)

    def test_get_box_comp_data(self):
        pf = PltFile(self.DATA_FILE)

        data = pf.get_box_comp_data(np.array([]), 0, (0, 0), 'A',  (0, 0), {'i': [], 'j': []})

        assert len(data.coords['i']) == 0
        assert len(data) == 0

        # Test when n_cells_dir is inconsistent with coords
        data = pf.get_box_comp_data(np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6]), 0, (0, 6), 'A',
                                    n_cells_dir=(3, 2),
                                    coords={'i': [0, 1], 'j': [0,1,2]})
        assert len(data.coords['i']) == 2
        assert data[1,2] == 0.6

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
        data_files = [PltFile(self.DATA_FILE_3D),
                      PltFile(self.DATA_FILE_3D_CHK)]

        for pf in data_files:

            porosity = pf.get_level_data("Enthalpy")
            coords = porosity.coords
            x = coords["x"]
            y = coords["y"]
            z = coords["y"]

            self.assertEqual(pf.space_dim, 3)
            self.assertEqual(len(z), 32)
            self.assertEqual(len(x), 32)
            self.assertEqual(len(y), 32)

            x, y, z = pf.get_mesh_grid(extend_grid=True)
            assert len(x) == 33
            assert x[0, 0, 0] == 0.0
            assert x[-1, -1, -1] == 1.0

            x, y, z = pf.get_mesh_grid(extend_grid=False)
            dx = 1.0/32
            assert len(x) == 32
            assert x[0, 0, 0] == dx/2
            assert x[-1, -1, -1] == 1.0 - dx/2

    def test_static_methods(self):
        pf = PltFile(self.DATA_FILE, load_data=True)

        x, y = pf.get_mesh_grid()
        self.assertEqual(len(x), 16)

        x, y = pf.get_mesh_grid(extend_grid=False)
        self.assertEqual(len(x), 15)

        porosity = pf.get_level_data("Porosity")
        x, y = PltFile.get_mesh_grid_n(porosity)
        self.assertEqual(len(x), 16)

        x, y = PltFile.get_mesh_grid_xarray(porosity)
        dx = 0.0625
        assert len(x) == 16
        assert len(y) == 16
        assert x[0] == dx/2
        assert y[0] == dx/2
        assert x[-1] == 1 - dx/2
        assert y[-1] == 1 - dx/2

        x, y = PltFile.get_mesh_grid_xarray(porosity, grow=True)
        assert len(x) == 17
        assert x[0] == 0.0
        assert y[0] == 0.0
        assert x[-1] == 1.0
        assert y[-1] == 1.0

    def test_child_methods(self):
        pf = PltFile(self.DATA_FILE)
        child = ChildPltFileForTesting(self.DATA_FILE)

        pf.reflect = True
        child.reflect = True
        streamfunction_unreflected = pf.get_level_data('streamfunction')
        streamfunction_reflected = child.get_level_data('streamfunction')

        assert float(streamfunction_reflected[4,4]) == -float(streamfunction_unreflected[4,4])

    def test_get_mesh_grid_3D(self):
        pass

    def test_scale_slice_transform(self):
        pf = PltFile(self.DATA_FILE)

        indices = dict(y=slice(0,3), x=slice(3,5))

        pf.set_scale_slice_transform(indices, True)

        assert pf.indices == indices
        assert pf.reflect == True

        porosity = pf.get_level_data('Porosity')

        assert len(porosity.coords['x']) == 2
        assert len(porosity.coords['y']) == 3
        assert float(porosity[0,0]) == 1.0

        pf.reset_scale_slice_transform()

        assert pf.indices is None
        assert pf.reflect is None

    def test_get_data(self):
        pf = PltFile(self.DATA_FILE)
        assert float(pf.get_data('Porosity')[13,14]) == 1.0

        pf = PltFile('no data')
        assert pf.get_data('Porosity') is None


def is_installed(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None

if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPltFile)
    unittest.TextTestRunner(verbosity=2).run(suite)
