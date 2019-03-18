#!/usr/bin/env python

import sys, os, subprocess, struct, numpy, math, argparse


def shellExecute(command, showOutErr = False):
    """ Execute the command in the SHELL and shows both stdout and stderr"""
    print(command)
    (out,err) = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    r = '\n'.join((out.decode("utf-8") , err.decode("utf-8")))
    if showOutErr:
        print(r)
    return r




def getPCFileDetails(absPath):
    """ Get the details (count numPoints and extent) of a LAS/LAZ file (using LAStools, hence it is fast)"""
    count = None
    (minX, minY, minZ, maxX, maxY, maxZ) = (None, None, None, None, None, None)
    (scaleX, scaleY, scaleZ) = (None, None, None)
    (offsetX, offsetY, offsetZ) = (None, None, None)

    command = 'lasinfo ' + absPath + ' -nc -nv -nco'
    for line in shellExecute(command).split('\n'):
        if line.count('min x y z:'):
            [minX, minY, minZ] = line.split(':')[-1].strip().split(' ')
            minX = float(minX)
            minY = float(minY)
            minZ = float(minZ)
        elif line.count('max x y z:'):
            [maxX, maxY, maxZ] = line.split(':')[-1].strip().split(' ')
            maxX = float(maxX)
            maxY = float(maxY)
            maxZ = float(maxZ)
        elif line.count('number of point records:'):
            count = int(line.split(':')[-1].strip())
        elif line.count('scale factor x y z:'):
            [scaleX, scaleY, scaleZ] = line.split(':')[-1].strip().split(' ')
            scaleX = float(scaleX)
            scaleY = float(scaleY)
            scaleZ = float(scaleZ)
        elif line.count('offset x y z:'):
            [offsetX, offsetY, offsetZ] = line.split(':')[-1].strip().split(' ')
            offsetX = float(offsetX)
            offsetY = float(offsetY)
            offsetZ = float(offsetZ)
    return (count, minX, minY, minZ, maxX, maxY, maxZ, scaleX, scaleY, scaleZ, offsetX, offsetY, offsetZ)
    


#main()
parser=argparse.ArgumentParser("simple script to test performance of lasinfo on cluster")

parser.add_argument('fullpath')
arguments=parser.parse_args()

fullpath=arguments.fullpath

print(fullpath)

lasinfooutput=getPCFileDetails(fullpath)

print(lasinfooutput)

