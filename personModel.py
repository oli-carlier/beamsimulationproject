# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 17:51:00 2016

@author: ik3e16

Part of the CENV1026 Design and Computing assignment.
**You do not need to edit this module**
"""


class person(object):
    """This class models the displacement of a person's load as they run at
    'speed' in one dimension. It assumes that the load is always concentrated
    in a single point and that the displacement of that point is less than or
    equal to the displacement of the person's centre of mass. Also the
    displacement of the load will always be a multiple of 'gait'.
    """
    def __init__(self, arrivalTime, weight, gait, speed):
        """This constructor function defines the person's weight, gait and
        running speed as well as the time that they arrive at the position of
        zero displacement.
        """
        self.weight = weight
        self.gait = gait
        self.speed = speed
        self.arrivalTime = arrivalTime

    def loadDisplacement(self, time):
        """This function returns the load and displacement of the person's
        weight at time 'time', in a tuple: (load,displacement).
        """
        dTime = time - self.arrivalTime
        if dTime < 0:
            return (0.0, 0.0)
        else:
            displacement = self.speed * dTime
            steps = int(displacement/self.gait)
            stepDisplacement = steps*self.gait

            return (9.81*self.weight, stepDisplacement)
