import numpy as np

class Vector(np.ndarray):
    '''
    A wrapper to np.ndarray that provides useful functions when dealing with
    vectors (in the mathematical sense).
    
    '''
    def __new__(cls, *args):
        # create a vector from an np.ndarray
        if len(args) > 1:
            return np.asarray(args).view(Vector)
        elif len(args) == 1:
            return np.asarray(*args).view(Vector)
        else:
            return np.array(*args).view(Vector)

    def __mul__(self, other):
        if not isinstance(other, type(self)):
            # if we're not multiplying with another Vector, default to 
            # np.ndarray methods
            return super(Vector, self).__mul__(other)
        return self.dot(other)

    def mag(self):
        '''The magnitude of the vector (total length)'''
        return np.linalg.norm(self)

    def norm(self):
        '''The normalized vector (same direction, magnitude = 1)'''
        return self / self.mag()

class Body(object):
    '''
    A body with position, velocity, acceleration and mass
    '''
    def __init__(self, m, x, y, z, 
                 v_x = 0, v_y = 0, v_z = 0, 
                 a_x = 0, a_y = 0, a_z = 0):
        '''
        Create the body.
        
        Parameters
        ----------
        m: float
            mass, in kg
        x, y, z: float
            x, y, and z position in meters
        v_x, v_y, v_z: float, optional
            x, y, and z velocity in meters per second.  defaults to zero
        a_x, a_y, a_z, float, optional
            x, y, and z velocities in meters per second^2.  defaults to zero
        '''
        self._G = 6.67e-11
        self.r = Vector(x, y, z)
        self.v = Vector(v_x, v_y, v_z)
        self.a = Vector(0, 0, 0)
        self.m = np.float64(m)

    def displacement(self, other):
        '''The vector displacement from `self` to `other`'''
        return Vector(other.r - self.r)

    def force(self, other):
        '''
        The vector force on `self` from `other`
        other.force(self) == -self.force(other)
        '''
        R = self.displacement(other)
        f = self.m * other.m * self._G / R.mag()**2
        return f * R.norm()
        
    def step(self, t):
        '''
        Step the body forward `t` seconds
        '''
        self.r += self.a * t*t / 2 + self.v * t
