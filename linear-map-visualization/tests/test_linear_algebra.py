"""Numerical acceptance checks: invariants, fibers, and near-singular ranks."""
import unittest
import numpy as np
from utils.linear_algebra import (fundamental_subspaces, collapse, matrix_rank,
                                  null_space, row_space, column_space, left_null_space)
from utils.examples import R3_TO_R2, R2_TO_R3, SQUARE_TRAP


class LinearAlgebraTests(unittest.TestCase):
    def test_four_subspace_invariants(self):
        rng = np.random.default_rng(2026)
        matrices = [R3_TO_R2, R2_TO_R3, SQUARE_TRAP, np.zeros((2,3)),
                    np.eye(3), np.zeros((1,4)), rng.normal(size=(4,2)),
                    rng.normal(size=(3,2)) @ rng.normal(size=(2,5)),
                    np.diag([1.,1e-18,0.])]
        for A in matrices:
            with self.subTest(shape=A.shape):
                s = fundamental_subspaces(A)
                m,n = A.shape
                self.assertEqual(s.rank+s.kernel.shape[1],n)
                self.assertEqual(s.rank+s.left_null.shape[1],m)
                np.testing.assert_allclose(A@s.kernel,0,atol=1e-12)
                np.testing.assert_allclose(A.T@s.left_null,0,atol=1e-12)
                np.testing.assert_allclose(s.row.T@s.kernel,0,atol=1e-12)
                np.testing.assert_allclose(s.column.T@s.left_null,0,atol=1e-12)
                np.testing.assert_allclose(s.row_projector+s.kernel_projector,np.eye(n),atol=1e-12)
                np.testing.assert_allclose(s.column@s.column.T+s.left_null@s.left_null.T,np.eye(m),atol=1e-12)
                np.testing.assert_allclose(s.column@s.column.T@A,A,atol=1e-12)
                for basis in (s.kernel,s.row,s.column,s.left_null):
                    np.testing.assert_allclose(basis.T@basis,np.eye(basis.shape[1]),atol=1e-12)
                self.assertEqual(matrix_rank(A),s.rank)
                for function,basis in [(null_space,s.kernel),(row_space,s.row),
                                       (column_space,s.column),(left_null_space,s.left_null)]:
                    np.testing.assert_allclose(function(A)@function(A).T,basis@basis.T,atol=1e-12)

    def test_projection_preserves_outputs_and_fibers(self):
        s = fundamental_subspaces(R3_TO_R2)
        p = np.random.default_rng(1).normal(size=(50,3))
        np.testing.assert_allclose(collapse(p,s,0),p,atol=1e-12)
        np.testing.assert_allclose(collapse(p,s,1)@s.kernel,0,atol=1e-12)
        for t in np.linspace(0,1,11):
            np.testing.assert_allclose(collapse(p,s,t)@s.matrix.T,p@s.matrix.T,atol=1e-12)
        x0 = np.array([1.,0.,0.])
        shifts = np.random.default_rng(2).normal(size=(50,2))@s.kernel.T
        np.testing.assert_allclose((x0+shifts)@s.matrix.T,np.tile(s.matrix@x0,(50,1)),atol=1e-12)

    def test_examples(self):
        b = fundamental_subspaces(R2_TO_R3)
        self.assertEqual(b.rank,2)
        self.assertEqual(b.kernel.shape,(2,0))
        p = np.array([[1.,2.],[-2.,1.]])@b.matrix.T
        np.testing.assert_allclose(p[:,2],p[:,0]+p[:,1])
        square = fundamental_subspaces(SQUARE_TRAP)
        np.testing.assert_allclose(square.kernel_projector@square.column,square.column)
        self.assertLess(np.linalg.matrix_rank(np.column_stack([square.kernel,square.column])),3)

    def test_invalid_matrices(self):
        for A in ([1,2],[],[[np.nan]],np.zeros((0,3))):
            with self.assertRaises(ValueError):
                fundamental_subspaces(A)
        for tol in (-1,np.nan):
            with self.assertRaises(ValueError):
                fundamental_subspaces(np.eye(2),tol)


if __name__ == '__main__':
    unittest.main()
