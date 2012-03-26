#!/usr/bin/env python2
import numpy as np

class lha_sensor:
    def __init__(self):
        self.a=[0.0305, 0.0015, 40]
        self.kappa=5.39e-3

    def get_sigma(self, r, theta):
        a = self.a
        g = a[0]+a[1]*(a[2]-r)**2
        sigma = g*self.kappa/np.cos(theta)**2
        return sigma

    def sample_from(self, r, bearing, N):
        sigma = self.get_sigma(r,bearing)
        s = np.random.normal(bearing, sigma, N)
        return s

if __name__=='__main__':
    from sys import stdout

    sensor = lha_sensor()
    r = 200
    bearing = np.pi/3
    N = 10000
    s = sensor.sample_from(r, bearing, N)
    mean = s.mean()
    var = s.std()**2
    
    print "Generated %d samples of measurements at a range of %2.2f, bearing %2.2fpi" % (len(s), r, bearing/np.pi)
    print "Mean: %2.2f, Variance: %2.4f" % (mean, var)
