import unittest
from Elasticipy.tensors.fourth_order import FourthOrderTensor, SymmetricFourthOrderTensor
import numpy as np

from Elasticipy.tensors.second_order import SecondOrderTensor


class TestFourthOrderTensor(unittest.TestCase):
    def test_multidimensionalArrayTensors(self):
        m = 5
        a = np.random.random((m, 6, 6))
        T = FourthOrderTensor(a)
        np.testing.assert_array_almost_equal(a, T.matrix)
        T2 = FourthOrderTensor(T.full_tensor())
        np.testing.assert_array_almost_equal(a, T2.matrix)

    def test_nonsymmetry(self):
        a = np.random.random((3,3,3,3))
        with self.assertRaises(ValueError) as context:
            _ = FourthOrderTensor(a)
        self.assertEqual(str(context.exception), 'The input array does not have minor symmetry')
        T = FourthOrderTensor(a, force_minor_symmetry=True)
        Tfull = T.full_tensor()
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        b = 0.25 * (a[i,j,k,l] + a[j,i,k,l] + a[i,j,l,k] + a[j,i,l,k])
                        np.testing.assert_array_almost_equal(Tfull[i,j,k,l], b)

    def test_inversion(self):
        m = 5
        a = np.random.random((m, 6, 6))
        T = FourthOrderTensor(a)
        Tinv = T.inv()
        TTinv = Tinv.ddot(T)
        eye = FourthOrderTensor.identity(m)
        for i in range(m):
            np.testing.assert_array_almost_equal(TTinv[i].full_tensor(), eye[i].full_tensor())

    def test_mult(self):
        m, n, o = 5, 4, 3
        a = np.random.random((m,n,o,6,6))
        a = FourthOrderTensor(a)
        b = 5
        ab = a * b
        for i in range(m):
            for j in range(n):
                for k in range(o):
                    np.testing.assert_array_equal(ab[i,j,k].matrix, a[i,j,k].matrix * b)

        b = np.random.random((n,o))
        ab = a * b
        for i in range(m):
            for j in range(n):
                for k in range(o):
                    np.testing.assert_array_equal(ab[i,j,k].matrix, a[i,j,k].matrix * b[j,k])

    def test_zeros_setitem(self):
        m, n = 4, 5
        t = FourthOrderTensor.zeros()
        assert t.shape == ()
        assert np.all(t.full_tensor()==0.)

        t = FourthOrderTensor.zeros(n)
        assert t.shape == (n,)

        t = FourthOrderTensor.zeros((m,n))
        assert t.shape == (m, n)

        t[1,3] = np.ones((6,6))
        for i in range(m):
            for j in range(n):
                if (i == 1) and (j == 3):
                    assert np.all(t[i,j] == 1.)
                else:
                    assert np.all(t[i, j] == 0.)

        t0 = t == 0.
        t0_th = np.ones((m, n))
        t0_th[1,3] = 0.
        assert np.all(t0== t0_th)

    def test_div(self):
        m, n, o = 5, 4, 3
        a = np.random.random((m, n, o, 6, 6))
        a = FourthOrderTensor(a)
        a_div_a = a / a
        np.testing.assert_array_almost_equal(a_div_a.full_tensor(), FourthOrderTensor.identity(return_full_tensor=True, shape=(m,n,o)))

        half_a = a / 2
        np.testing.assert_array_almost_equal(half_a.full_tensor(), a.full_tensor()/2)

        b = SecondOrderTensor.rand(shape=(4,3))
        a_div_b = a / b
        np.testing.assert_array_almost_equal(a_div_b.matrix, (a * b.inv()).matrix)



class TestSymmetricFourthOrderTensor(unittest.TestCase):
    def test_inversion(self):
        m = 5
        a = np.random.random((m, 6, 6))
        T = SymmetricFourthOrderTensor(a, force_symmetries=True)
        Tinv = T.inv()
        TTinv = Tinv.ddot(T)
        eye = SymmetricFourthOrderTensor.identity(m)
        for i in range(m):
            np.testing.assert_array_almost_equal(TTinv[i].full_tensor(), eye[i].full_tensor())

if __name__ == '__main__':
    unittest.main()
