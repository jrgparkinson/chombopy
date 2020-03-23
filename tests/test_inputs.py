import unittest
from chombopy import inputs
import os
from unittest.mock import Mock

# Run with e.g.
# coverage run -m unittest testUtils.py; coverage html
# python -m unittest
class TestInputs(unittest.TestCase):
    def test_add_params(self):
        self.assertEqual(
            {"a": 1, "b": 2, "c": 4},
            inputs.add_params({"a": 1, "c": 0}, {"b": 2, "c": 4}),
        )

    def test_isfloat(self):
        self.assertTrue(inputs.isfloat(0.1))
        self.assertTrue(inputs.isfloat(-0.1))
        self.assertTrue(inputs.isfloat(0.0))
        self.assertTrue(inputs.isfloat(10))
        self.assertTrue(inputs.isfloat("1.01"))

    def test_isint(self):
        self.assertTrue(inputs.isint(1))
        self.assertTrue(inputs.isint(0))
        self.assertTrue(inputs.isint(-3))
        self.assertTrue(inputs.isint("5"))
        self.assertFalse(inputs.isint(1.01))
        self.assertFalse(inputs.isint("1.0"))

    def test_read_inputs(self):
        pass

    def test_write_inputs(self):

        # Test basic writing of different data types
        inputs.write_inputs(
            "test.inputs",
            {"a": [0, 0], "b": 1.04, "c": True, "d": 1, "e": "some string"},
        )
        with open("test.inputs", "r") as f:
            assert f.readlines() == [
                "\n",
                "a=0 0\n",
                "b=1.04\n",
                "c=True\n",
                "d=1\n",
                "e=some string",
            ]
        os.remove("test.inputs")

        # Test ignoring keys
        inputs.write_inputs(
            "test.inputs",
            {"a": [0, 0], "b": 1.04, "c": True, "d": 1, "e": "some string"},
            ignore_list=["b", "c"],
        )
        with open("test.inputs", "r") as f:
            assert f.readlines() == ["\n", "a=0 0\n", "d=1\n", "e=some string"]
        os.remove("test.inputs")

        #  Test sorting
        inputs.write_inputs(
            "test.inputs.sorted", {"b": 1.04, "a": [0, 0],}, do_sort=True
        )
        inputs.write_inputs(
            "test.inputs.unsorted", {"b": 1.04, "a": [0, 0],}, do_sort=False
        )
        with open("test.inputs.sorted", "r") as f:
            assert f.readlines() == ["\n", "a=0 0\n", "b=1.04"]
        os.remove("test.inputs.sorted")
        with open("test.inputs.unsorted", "r") as f:
            assert f.readlines() == ["\n", "b=1.04\n", "a=0 0"]
        os.remove("test.inputs.unsorted")

    def test_time_since_folder_updated(self):
        pass

    def test_time_since_file_updated(self):
        pass

    def test_get_restart_file(self):
        pass

    def test_get_final_plot_file(self):
        pass

    def test_get_final_chk_file(self):
        pass

    def test_is_power_of_two(self):
        self.assertTrue(inputs.is_power_of_two(8))
        self.assertTrue(inputs.is_power_of_two(2))
        self.assertTrue(inputs.is_power_of_two(1))

        self.assertFalse(inputs.is_power_of_two(9))
        self.assertFalse(inputs.is_power_of_two(257))
        self.assertFalse(inputs.is_power_of_two(64.3))

    def test_string_to_array(self):
        self.assertEqual(inputs.string_to_array("1 2 3"), [1, 2, 3])
        self.assertEqual(
            inputs.string_to_array("1 2 3", conversion=float), [1.0, 2.0, 3.0]
        )
        self.assertEqual(inputs.string_to_array([4, 5, 6]), [4, 5, 6])

    def test_array_to_string(self):
        self.assertEqual(inputs.array_to_string([1, 2, 3]), "1 2 3")
        self.assertEqual(inputs.array_to_string([1.0, 2.0, 3.0]), "1.0 2.0 3.0")
