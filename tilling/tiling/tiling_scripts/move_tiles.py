#!/usr/bin/env python

import sys, os, argparse, subprocess


def shellExecute(command, showOutErr = False):
    """ Execute the command in the SHELL and shows both stdout and stderr
    """
    print(command)
    (out,err) = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    r = '\n'.join((out.decode("utf-8") , err.decode("utf-8")))
    if showOutErr:
        print(r)


"""
main()
"""

parser=argparse.ArgumentParser("Script to move tiles from processed subsets to aggregate structure prior to merging")

parser.add_argument('tilesPath')
parser.add_argument('subsetHandle')
parser.add_argument('subsetId')
parser.add_argument('aggregateTileHandle')

arguments=parser.parse_args()

tilesPath=arguments.tilesPath
subsetHandle=arguments.subsetHandle
subsetId=arguments.subsetId
aggregateTileHandle=arguments.aggregateTileHandle

currentDir=os.getcwd()

tiles=os.listdir(tilesPath+'/'+subsetHandle+subsetId)


#print(tiles)

for tile in tiles:
    if not tile.endswith('.js'):
        sourcePath=tilesPath+'/'+subsetHandle+subsetId+'/'+tile
        destPath=tilesPath+'/'+aggregateTileHandle+'/'+tile
        moveCommand='mv '+sourcePath+'/*.LAZ '+destPath+'/'
        
        print(tile)
        #print(sourcePath)
        #print(destPath)
        #print(moveCommand)
        
        
        shellExecute(moveCommand)
    
