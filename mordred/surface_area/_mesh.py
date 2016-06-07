import numpy as np

# http://prideout.net/blog/?p=44
# http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html


class SphereMesh(object):
    def __init__(self, level=4):
        t = (1.0 + np.sqrt(5.0)) / 2.0
        self.vertices = np.array([
            (-1, t, 0),
            (1, t, 0),
            (-1, -t, 0),
            (1, -t, 0),

            (0, -1, t),
            (0, 1, t),
            (0, -1, -t),
            (0, 1, -t),

            (t, 0, -1),
            (t, 0, 1),
            (-t, 0, -1),
            (-t, 0, 1),
        ], dtype='float')

        self.faces = np.array([
            (0, 11, 5),
            (0, 5, 1),
            (0, 1, 7),
            (0, 7, 10),
            (0, 10, 11),

            (1, 5, 9),
            (5, 11, 4),
            (11, 10, 2),
            (10, 7, 6),
            (7, 1, 8),

            (3, 9, 4),
            (3, 4, 2),
            (3, 2, 6),
            (3, 6, 8),
            (3, 8, 9),

            (4, 9, 5),
            (2, 4, 11),
            (6, 2, 10),
            (8, 6, 7),
            (9, 8, 1),
        ], dtype='int')

        self.normalize(self.vertices)

        self.level = 1
        self.subdivide(level)

    @staticmethod
    def normalize(vs):
        vs /= np.sqrt((vs ** 2).sum(axis=1))[:, np.newaxis]

    def _subdivide(self):
        self.level += 1

        Nv = len(self.vertices)
        Nf = len(self.faces)

        A = self.faces[:, 0]
        B = self.faces[:, 1]
        C = self.faces[:, 2]

        Av = self.vertices[A]
        Bv = self.vertices[B]
        Cv = self.vertices[C]

        newVs = np.r_[
            Av + Bv,
            Bv + Cv,
            Av + Cv
        ]
        self.normalize(newVs)
        self.vertices = np.r_[self.vertices, newVs]

        AB = np.arange(len(self.faces)) + Nv
        BC = AB + Nf
        AC = AB + 2 * Nf

        self.faces = np.r_[
            np.c_[A, AB, AC],
            np.c_[B, AB, BC],
            np.c_[C, AC, BC],
            np.c_[AB, AC, BC],
        ]

    def subdivide(self, level):
        for _ in range(level - self.level):
            self._subdivide()

    def __len__(self):
        return len(self.vertices)
