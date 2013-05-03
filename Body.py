import numpy as np

class Vector(np.ndarray):
    # np.ndarray(stuff) != np.array(stuff)
    # either need to use np.ndarray.new() or grab source code from np.array()
    def __new__(cls, *args):
        if len(args) > 1:
            return np.asarray(args).view(Vector)
        elif len(args) == 1:
            return np.asarray(*args).view(Vector)
        else:
            # ooooh boy
            assert(False)

    def __mul__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError('__mul__ is not defined for %s and %s' 
                            %(type(self), type(other)))
        return self.dot(other)

    def mag(self):
        return np.linalg.norm(self)

    def norm(self):
        return self / self.mag()

class Body(object):
    def __init__(self, m, x, y, z, v_x = 0, v_y = 0, v_z = 0):
        self._G = 6.67e-11
        self.r = Vector(x, y, z)
        self.v = Vector(v_x, v_y, v_z)
        self.a = Vector(0, 0, 0)
        self.m = np.float64(m)

    def displacement(self, other):
        return Vector(other.r - self.r)

    def force(self, other):
        R = self.displacement(other)
        f = self.m * other.m * self._G / R.mag()**2
        return f * R.norm()
        
    def step(self, t):
        self.r += self.a * t*t / 2 + self.v * t
