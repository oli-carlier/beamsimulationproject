# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 14:25:47 2020

@author: Oli
"""
import personModel as pm
import matplotlib.pyplot as plt
import numpy
import beamModel

def createPersonList(fileName):
    '''
    Creates a list of person objects from a table of data.
    '''
    person_data = open(fileName)
    persons = []
    person_list = []
    
    for line in person_data:
        line_split = line.split("\n")
        persons.append(line_split[0])
    for element in persons[1:]:
        element_list = element.split(", ")
        data_list = [float(i) for i in element_list]
        person_list.append(pm.person(data_list[0], data_list[1],
                                     data_list[2], data_list[3]))
    return person_list


def simulateBeamRun(personList, beam, times):
    '''
    Takes a list of person objects, a beam object
    and a list of times (s). The function calculates the
    value and location of maximum deflection at each
    time in the list, produces a graph of the value
    and location of maximum deflection against time
    and returns a list of tuples with maximum deflection
    and position of maximum deflection, one for each time in the list.
    '''
    max_deflection_list = []
    yd = []
    yp = []
    
    for time in times:
        load_list = []
        for person_data in personList:
            if 0.0 < person_data.loadDisplacement(time)[1] < beam.L:
                load_list.append(person_data.loadDisplacement(time))
        beam.setLoads(load_list)
        max_deflection_list.append(beam.getMaxDeflection())
        yd.append(beam.getMaxDeflection()[0]*10**3)
        yp.append(beam.getMaxDeflection()[1])
    
    plt.figure()
    plt.plot(times, yd)
    plt.plot(times, yp)
    plt.legend(["Maximum Deflection (mm)",
                "Position of Maximum Deflection (m)"])
    plt.xlabel("time (s)")
    return max_deflection_list


def bonusFunction(personList, beam, time):
    '''
    Takes a list of person objects, a beam object
    and a time (s). Plots a graph of the deflections
    along the beam at any given time.
    '''
    plt.figure("Deflection at t = " + str(time) + " (s)")
    plt.axes(xLim=(0, beam.L), yLim=(-5, 5))
    plt.xlabel("Position (m)")
    plt.ylabel("Deflection (mm)")
    x = numpy.linspace(0.0, beam.L, 500)
    load_list = []
    deflections = []
    
    for person_data in personList:
        if 0.0 < person_data.loadDisplacement(time)[1] < 5.0:
            load_list.append(person_data.loadDisplacement(time))
    beam.setLoads(load_list)
    for displacement in x:
        deflections.append(-beam.getTotalDeflection(displacement)
                           * 10**3)
    y = deflections
    plt.plot(list(x), y)
    