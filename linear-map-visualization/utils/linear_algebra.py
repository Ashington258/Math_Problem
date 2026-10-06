"""Four fundamental subspaces, with basis vectors stored as COLUMNS.

One full SVD and one shared tolerance determine all four subspaces.
This avoids contradictory ranks near a numerical threshold.
"""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Subspaces:
    matrix: np.ndarray
    rank: int
    singular_values: np.ndarray
    tolerance: float
    kernel: np.ndarray
    row: np.ndarray
    column: np.ndarray
    left_null: np.ndarray

    @property
    def row_projector(self):
        return self.row @ self.row.T

    @property
    def kernel_projector(self):
        return self.kernel @ self.kernel.T


def fundamental_subspaces(A, rtol=None):
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or min(A.shape) == 0 or not np.isfinite(A).all():
        raise ValueError("A must be a nonempty, finite real matrix")
    if rtol is not None and (not np.isfinite(rtol) or rtol < 0):
        raise ValueError("rtol must be finite and nonnegative")
    U, s, Vt = np.linalg.svd(A, full_matrices=True)
    relative = max(A.shape) * np.finfo(float).eps if rtol is None else rtol
    tolerance = float(relative * s[0])
    rank = int(np.count_nonzero(s > tolerance))
    result = Subspaces(A, rank, s, tolerance, Vt[rank:].T,
                       Vt[:rank].T, U[:, :rank], U[:, rank:])
    m, n = A.shape
    if rank + result.kernel.shape[1] != n:
        raise ArithmeticError("Input rank-nullity failed")
    if rank + result.left_null.shape[1] != m:
        raise ArithmeticError("Output rank-nullity failed")
    return result


def matrix_rank(A, rtol=None):
    return fundamental_subspaces(A, rtol).rank


def null_space(A, rtol=None):
    return fundamental_subspaces(A, rtol).kernel


def row_space(A, rtol=None):
    return fundamental_subspaces(A, rtol).row


def column_space(A, rtol=None):
    return fundamental_subspaces(A, rtol).column


def left_null_space(A, rtol=None):
    return fundamental_subspaces(A, rtol).left_null


def collapse(points, spaces, t):
    """C_t x = P_row x + (1-t) P_kernel x, in the INPUT space.

    This is a homotopy from identity to orthogonal projection, NOT the
    rectangular map A. A C_t x = A x for every t (up to SVD roundoff).
    """
    if not 0 <= t <= 1:
        raise ValueError("t must lie in [0, 1]")
    points = np.asarray(points, dtype=float)
    return points @ (spaces.row_projector + (1-t)*spaces.kernel_projector).T
