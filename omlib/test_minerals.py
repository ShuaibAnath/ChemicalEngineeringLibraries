# test_minerals.py
import unittest
import minerals


class TestClass(unittest.TestCase):
    def test_get_mill_critical_speed(self):
        mill_obj = minerals.Milling()
        self.assertAlmostEqual(mill_obj.get_mill_critical_speed(2, 1), 42.3)

    def test_gys_method(self):
        sample_obj = minerals.Sampling()
        self.assertEqual(sample_obj.gys_method(sampling_constant=1,
                                               sampling_error_variance=1, largest_particle_dimension=2), 8)
