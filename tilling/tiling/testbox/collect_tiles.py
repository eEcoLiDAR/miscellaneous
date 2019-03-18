#!/usr/bin/env python

import sys, os, argparse



"""
def shellExecute(command, showOutErr = False):
    """ #Execute the command in the SHELL and shows both stdout and stderr
    """
    print(command)
    (out,err) = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    r = '\n'.join((out.decode("utf-8") , err.decode("utf-8")))
    if showOutErr:
        print(r)
    return r

"""




"""
main()
"""

parser=argparse.ArgumentParser("Script to identify all tiles created and make infrastructure for merging them")

parser.add_argument('tilesPath')
parser.add_argument('subsetHandle')
parser.add_argument('numberSubsets')
parser.add_argument('aggregateTileHandle')                               

arguments=parser.parse_args()

tilesPath=arguments.tilesPath
subsetHandle=arguments.subsetHandle
numberSubsets=arguments.numberSubsets
aggregateTileHandle=arguments.aggregateTileHandle

currentDir=os.getcwd()
##change to tiles directory
#os.chdir(tilesPath)



tiles=[]
for i in range(int(numberSubsets)):
    #os.chdir(tilesPath+'/'+subsetHandle+str(i))
    fp=tilesPath+'/'+subsetHandle+str(i)
    for line in os.listdir(fp):
        if not line.endswith('.js'):
            tiles.append(line)
    #os.chdir(tilesPath)

utiles=list(set(tiles))

os.makedirs(tilesPath+'/'+aggregateHandle,exist_ok=True)
#os.chdir(tilesPath+'/all_tiles')

for tile in utiles:
    print('making directory '+tile)
    ofp=tilesPath+'/'+aggregateHandle+'/'+tile
    os.makedirs(ofp,exist_ok=True)

#os.chdir(currentDir)

