import unittest
from matplotlib import pyplot as plt
import numpy as np

from Elasticipy.tensors.elasticity import StiffnessTensor
from pytest import approx

from Elasticipy.spherical_function import HyperSphericalFunction

C = StiffnessTensor.cubic(C11=186, C12=134, C44=77)
E = C.Young_modulus # SphericalFunction
E_mean = 126.28067650635076
E_std = 31.58751357560234
G = C.shear_modulus # HypersphericalFunction
G_mean = 47.07147379585229
G_std = 14.14600864639266
SEED = 123  # Used for Monte Carlo integrations (e.g. for G.mean())

import re


def template_test_repr(result, class_name, expected_min, expected_max):
    # First, check if the string if correctly formated
    pattern = r'{} function\nMin=(\d+\.\d+), Max=(\d+\.\d+)'.format(class_name)
    match = re.match(pattern, result)
    assert match is not None

    # Now check the returned values
    min_val = float(match.group(1))
    max_val = float(match.group(2))
    assert expected_min == approx(min_val)
    assert expected_max == approx(max_val)


class TestSphericalFunction(unittest.TestCase):
    def test_plot3D(self):
        fig = plt.figure()
        _, ax = E.plot3D(fig=fig)
        np.testing.assert_allclose(ax.xaxis.v_interval, [-174.66981, 175.43156])
        np.testing.assert_allclose(ax.yaxis.v_interval, [-175.05069, 175.05069])
        np.testing.assert_allclose(ax.zaxis.v_interval, [-131.28802, 131.28802])

    def test_plot_xyz_section(self):
        fig = plt.figure()
        _, axs = E.plot_xyz_sections(fig=fig)
        assert axs[0].title._text == 'X-Y plane'
        assert axs[1].title._text == 'X-Z plane'
        assert axs[2].title._text == 'Y-Z plane'

    def test_plot_as_pole_figure(self):
        _, ax = E.plot_as_pole_figure(show=False)
        np.testing.assert_allclose(ax.dataLim.intervalx, [-0.01578689775673263, 6.298972204936319])
        np.testing.assert_allclose(ax.dataLim.intervaly, [-0.0160285339468867, 1.5868248607417832])

    def test_add_sub_mult_div(self):
        E_plus = E + E
        E_min = E - E
        E_mult = 2 * E
        E_plus_one = E + 1
        E_minus_one = E - 1
        E_div = E / E
        E_div_two = E / 2
        E_square = E * E
        assert E_plus.mean() == approx(2 * E_mean, rel=1e-3)
        assert E_min.mean() == approx(0)
        assert E_mult.mean() == approx(2 * E_mean, rel=1e-3)
        assert E_plus_one.mean() == approx(E_mean + 1, rel=1e-3)
        assert E_minus_one.mean() == approx(E_mean - 1, rel=1e-3)
        assert E_div.mean() == approx(1, rel=1e-3)
        assert E_div_two.mean() == approx(E_mean/2, rel=1e-3)
        assert E_square.eval([1,0,0]) == approx(E.eval([1,0,0])**2, rel=1e-3)

        expected_error = 'A Spherical function can only be added to another Spherical function or a scalar value.'
        with self.assertRaises(NotImplementedError) as context:
            _ = E + G
        self.assertEqual(str(context.exception), expected_error)

        expected_error = 'A Spherical function can only be multiplied by another Spherical function or a scalar value.'
        with self.assertRaises(NotImplementedError) as context:
            _ = E * G
        self.assertEqual(str(context.exception), expected_error)

        expected_error ='A SphericalFunction can only be divided by a scalar value of another SphericalFunction.'
        with self.assertRaises(NotImplementedError) as context:
            _ = E / G
        self.assertEqual(str(context.exception), expected_error)

    def test_mean_std(self):
        for method in ('exact', 'trapezoid', 'Monte Carlo'):
            assert E_mean == approx(E.mean(method=method, seed=SEED), rel=1e-2)
            assert E_std == approx(E.std(method=method, seed=SEED), rel=1e-2)


    def test_repr(self):
        template_test_repr(E.__repr__(), 'Spherical', 73.775, 197.50282485875343)

    def test_eval_spherical(self):
        assert E.eval_spherical([0, 0], degrees=True) == approx(E.eval([0, 0, 1]))
        assert E.eval_spherical([0, 90], degrees=True) == approx(E.eval([1, 0, 0]))
        assert E.eval_spherical([90, 90], degrees=True) == approx(E.eval([0, 1, 0]))


class TestHyperSphericalFunction(unittest.TestCase):
    def test_plot3D(self):
        fig = plt.figure()
        _, ax = G.plot3D(fig=fig)
        np.testing.assert_allclose(ax.xaxis.v_interval, [-86.363067,  87.737754])
        np.testing.assert_allclose(ax.yaxis.v_interval, [-87.435894,  87.435894])
        np.testing.assert_allclose(ax.zaxis.v_interval, [-80.208333,  80.208333])

    def test_plot_xyz_section(self):
        fig = plt.figure()
        _, axs = G.plot_xyz_sections(fig=fig)
        assert axs[0].title._text == 'X-Y plane'
        assert axs[1].title._text == 'X-Z plane'
        assert axs[2].title._text == 'Y-Z plane'

    def test_plot_as_pole_figure(self):
        _, ax = G.plot_as_pole_figure(show=False)
        np.testing.assert_allclose(ax.dataLim.intervalx, [-0.01578689775673263, 6.298972204936319])
        np.testing.assert_allclose(ax.dataLim.intervaly, [-0.0160285339468867, 1.5868248607417832])

    def test_add_sub_mult_div(self):
        G_plus = G + G
        G_min = G - G
        G_mult = 2 * G
        Gplus_one = G + 1
        G_div = G / G
        G_div_two = G / 2
        assert G_plus.mean() == approx(2 * G_mean, rel=5e-3)
        assert G_min.mean() == approx(0)
        assert G_mult.mean() == approx(2 * G_mean, rel=5e-3)
        assert Gplus_one.mean() == approx(G_mean + 1, rel=1e-3)
        assert G_div.mean() == approx(1, rel=1e-3)
        assert G_div_two.mean() == approx(G_mean/2, rel=1e-3)

    def test_mean_std(self):
        for method in ('trapezoid', 'Monte Carlo'):
            assert G_mean == approx(G.mean(method=method, seed=SEED), rel=5e-3)
            assert G_std  == approx(G.std( method=method, seed=SEED), rel=5e-2)


    def test_repr(self):
        template_test_repr(G.__repr__(), 'Hyperspherical', 26., 77)

    def test_eval_along_null_direction(self):
        directions = ([0,0,0],
                      np.array([[1,0,0], [0,1,0], [0,0,0]]))
        for direction in directions:
            with self.assertRaises(ValueError) as context:
                _ = E.eval(direction)
            self.assertEqual(str(context.exception), 'The input vector cannot be zeros')

    def test_eval_along_parallel_directions(self):
        directions = [([1, 0, 0], [1, 1, 0]), (np.array([[1, 0, 0], [0, 1, 0]]),
                                               np.array([[0, 1, 0], [0, 1, 1]]))]
        for direction in directions:
            with self.assertRaises(ValueError) as context:
                _ = G.eval(*direction)
            self.assertEqual(str(context.exception), 'The two directions must be orthogonal.')

    def test_eval_spherical(self):
        assert G.eval_spherical([0,0,0]) == approx(G.eval([0,0,1], [1,0,0]))
        assert G.eval_spherical([0, 0, 90], degrees=True) == approx(G.eval([0, 0, 1], [0, 1, 0]))

    def test_exact_mean(self):
        def fun(u,v):
            return [1.0]

        a = HyperSphericalFunction(fun)
        assert a.mean(method='exact') == approx(1.0)

if __name__ == '__main__':
    unittest.main()