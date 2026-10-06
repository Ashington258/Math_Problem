import numpy as np

R3_TO_R2 = np.array([[1., 1., 0.], [0., 0., 0.]])
R2_TO_R3 = np.array([[1., 0.], [0., 1.], [1., 1.]])
SQUARE_TRAP = np.array([[0., 1., 0.], [0., 0., 0.], [0., 0., 0.]])

# The same semantic colors are used in MP4 and HTML.
COLORS = dict(kernel="#F472B6", row="#60A5FA", column="#34D399",
              left_null="#FBBF24", vector="#E2E8F0", bg="#0B1020")
