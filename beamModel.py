# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 17:48:59 2016

@author: ik3e16
"""

from scipy.misc import derivative
from scipy.optimize import brentq
import matplotlib.pyplot as plt
import numpy as np


class beam(object):
    '''
    This class is models the deflection of a simply supported
    beam under multiple point loads, following Euler-Bernoulli
    theory and the principle of superposition
    '''

    def __init__(self, E, I, L):
        '''
        The class costructor
        '''
        self.E = E  # Young's modulus of the beam in N/m^2
        self.I = I  # Second moment of area of the beam in m^4
        self.L = L  # Length of the beam in m
        self.Loads = [(0.0, 0.0)]  # the list of loads applied to the beam

    def setLoads(self, Loads):
        '''
        This function allows multiple point loads to
        be applied to the beam using a list of tuples
        of the form (load, position).
        '''
        self.Loads = Loads

    def beamDeflection(self, Load, x):
        """
        Returns the deflection of the beam at point x
        due to the application of a single load.
        """
        P1 = Load[0]
        a = Load[1]
        b = self.L - a
        
        if x > a:
            return (((P1 * b) / (6 * self.L * self.E * self.I)) *
                    ((self.L/b) * ((x - a)**3) - (x**3) +
                     ((self.L**2)-(b**2)) * x))
        else:
            return ((P1 * b * x)/(6 * self.L * self.E * self.I) *
                    ((self.L**2) - (x**2) - (b**2)))
        
    def getTotalDeflection(self, x):
        """
        Returns the total deflection of a beam at point x
        due to the application of multiple loads.
        """
        deflections = []
        for Load in self.Loads:
            deflections.append(self.beamDeflection(Load, x))
        return sum(deflections)

    def getSlope(self, x):
        """
        Returns the slope of a beam at point x due to deflection
        from multiple point loads.
        """
        return derivative(self.getTotalDeflection, x, dx=10**-6)
    
    def getMoment(self, x):
        """
        Returns the bending moment at point x of a beam
        due to the application of multiple point loads.
        """
        return -(self.E * self.I *
                 derivative(self.getSlope, x,
                            dx=10**-6,))
        
    def getMaxDeflection(self):
        """
        Returns the magnitude and position of the maximum
        deflection of the beam as a tuple.
        """
        xMax = brentq(self.getSlope, -0, self.L)
        return (self.getTotalDeflection(xMax), xMax)
        
    def plotBeamData(self, xs):
        """
        Plots the deflection, slope and bending moment
        on a singular graph.
        """
        yd = (self.createPlotData(self.getTotalDeflection, xs))*10**3
        ys = (self.createPlotData(self.getSlope, xs))*10**3
        yb = (self.createPlotData(self.getMoment, xs))*10**-3
        
        plt.figure()
        plt.plot(xs, yd)
        plt.plot(xs, ys)
        plt.plot(xs, yb)
        plt.legend(['deflection (mm)', 'slope (mm/m)',
                   'bending moment (kNm)'])
        plt.xlabel('beam position - x(m)')
        
    def createPlotData(self, f, xs):
        y = []
        for element in xs:
            y.append(f(element))
        return np.array(y)
    