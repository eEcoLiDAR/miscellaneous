"""
This script runs the consecutive pdal waterpipe2 pipelines to obtain a classification of water points based on the ALS data and the ground identification alone
"""

import os
import glob
import numpy as np
from invoke import run
import argparse
import time


"""
---------------------------------------------------------------------------------
Define subroutines. These include:

    waterpipe_commands : create pdal pipeline commands based on input data. 

    run_pipe           : run individual pdal pipelines

----------------------------------------------------------------------------------
"""


#define commands for pdal pipelines
def waterpipe_commands(gfilebase, ofilebase, mergefilebase, stcounterstr, zcut, num_k):
    

    
    #waterpipe2_1; read in files, set classifications, merge and normalize to HAG    
    cmd_wp2_1 = "pdal pipeline 'waterpipe2_1.json' --writers.las.filename="+mergefilebase+"_"+stcounterstr+"_norm_class#.las --stage.in_ground_laz.filename="+gfilebase+"_"+stcounterstr+".laz --stage.in_objects_laz.filename="+ofilebase+"_"+stcounterstr+".laz --nostream"
        
    
    #waterpipe2_2; read in ground and unclassified, produce voters       
    cmd_wp2_2 = "pdal pipeline 'waterpipe2_2.json' --writers.las.filename="+mergefilebase+"_"+stcounterstr+"_voters_norm.las --stage.ofnc.filename="+mergefilebase+"_"+stcounterstr+"_norm_class1.las --stage.gfnc.filename="+mergefilebase+"_"+stcounterstr+"_norm_class2.las "
        
        
    #waterpipe2_3; read in unclassed, filter vegetation (i.e non-water) and water candidates, perform neighbor classification using voters file from previous stage,explicitly load voters, merge and write output       
    cmd_wp2_3 = "pdal pipeline 'waterpipe2_3.json' --writers.las.filename="+mergefilebase+"_"+stcounterstr+"_norm_prov_waterclassed.laz --stage.ofnc.filename="+mergefilebase+"_"+stcounterstr+"_norm_class1.las --stage.pot_veg.limits='Z("+str(zcut)+":]' --stage.pot_wc.limits='Z[0.:"+str(zcut)+"]' --stage.voting.candidate="+mergefilebase+"_"+stcounterstr+"_voters_norm.las --stage.voting.k="+str(num_k)+" --stage.read_voters.filename="+mergefilebase+"_"+stcounterstr+"_voters_norm.las "
        
    #waterpipe2_norm; optional; read in normalized files before classification and create merged normalized subtile file WITHOUT any updated classifications
    cmd_wp2_norm = "pdal pipeline 'waterpipe2_norm.json' --stage.ofnc.filename="+mergefilebase+"_"+stcounterstr+"_norm_class1.las --stage.gfnc.filename="+mergefilebase+"_"+stcounterstr+"_norm_class2.las --stage.out.filename="+mergefilebase+"_"+stcounterstr+"_norm_wp.laz "

    #waterpipe2_clean; remove las output files created by waterpipe2 excep[t for the desired final output stages    
    cmd_wp2_clean = "rm "+mergefilebase+"_"+stcounterstr+"_norm_class1.las "+mergefilebase+"_"+stcounterstr+"_norm_class2.las "+mergefilebase+"_"+stcounterstr+"_voters_norm.las "   


    return cmd_wp2_1, cmd_wp2_2, cmd_wp2_3, cmd_wp2_norm, cmd_wp2_clean
    
        

#run a pdal pipeline with a specifed command <cmd>
def run_pipe(cmd,pipestr,tile,subtile):

    result_pipe = run(cmd, hide=True, warn=True)

    if result_pipe.ok != True :
        print('failure to correctly run '+pipestr+' for tile '+tile+' subtile '+subtile)
        print(result_pipe.stdout)
        print(result_pipe.stderr)

    return result_pipe
        
        
        

"""
-------------------------------------------------------------------------------------
Run waterpipe2 pipeline

Main()
-------------------------------------------------------------------------------------
"""


#-----------------------------------------------
# get file name and options from command line

parser = argparse.ArgumentParser()

parser.add_argument('AHN2_tile_descriptor', help='Tile id of AHN2 tile as specifed in the baldindex AHN2')

parser.add_argument('ground_file_dir', help='path to directory containing ground files')

parser.add_argument('object_file_dir', help='path to directory containing object files')

parser.add_argument('merge_file_dir', help='path to directory to contain merged files; must have been created')

parser.add_argument('Z_cutoff', help='Cutoff HAG value below which points will be considered as water points if surrounded by water')

parser.add_argument('k',help='Number of neighbour points considered in the k-neighbour vote classification')

parser.add_argument('--retain_norm',dest='retain_norm',default=False,action='store_true', help='set to retain merged pre-classification HAG normalized file')

args = parser.parse_args()

ahn2tile = args.AHN2_tile_descriptor

gfdir = args.ground_file_dir

ofdir = args.object_file_dir

mergedir = args.merge_file_dir

zcut= args.Z_cutoff

num_k = args.k

retain_norm = args.retain_norm

#-----------------------------------------------



#-----------------------------------------------
#define filename bases

gfilebase = gfdir+'/g'+ahn2tile
ofilebase = ofdir+'/u'+ahn2tile
mergefilebase = mergedir+'/ahn2_'+ahn2tile

#-----------------------------------------------

start = time.time()

#-----------------------------------------------
#check if tile exists

print('----- checking whether tile '+ahn2tile+' is present -----')

if os.path.isfile(glob.glob(gfilebase+'*')[0]):

    print('-- tile is present ')

    print('----- looping over subtiles -----')
    

    #-----------------------------------------------

    #-----------------------------------------------
    #begin loop over sub-tiles.
    #There are 25 at most, but not all are always present

    #for i in (np.arange(25) +1):
    for i in (np.arange(1) + 25):
        #print(str(i))
        if i < 10:
            stcounterstr='0'+str(i)
            
        else:
            stcounterstr=str(i)
            
            
        gfsubtile = gfilebase+'_'+stcounterstr+'.laz'
            
        if os.path.isfile(gfsubtile) :

            print('-- processing subtile '+stcounterstr)
        
        
                #get commands
            cmd_wp2_1, cmd_wp2_2, cmd_wp2_3, cmd_wp2_norm, cmd_wp2_clean = waterpipe_commands(gfilebase, ofilebase, mergefilebase, stcounterstr, zcut, num_k)
                
                
                
            #--------------------------------------------------
            # run waterpipe2 pipelines
            print('- waterpipe2_1')
            startwp1 = time.time()
            
            #waterpipe2_1
            result_wp2_1 = run_pipe(cmd_wp2_1,"waterpipe2_1",ahn2tile,stcounterstr)
            if result_wp2_1.ok != True :
                continue
            
            endwp1 = time.time()
            print('- waterpipe2_2')
            startwp2 = time.time()
            
            #waterpipe2_2
            result_wp2_2 = run_pipe(cmd_wp2_2,"waterpipe2_2",ahn2tile,stcounterstr)
            if result_wp2_2.ok != True :
                continue
            
            endwp2 = time.time()
            print('- waterpipe2_3')
            startwp3 = time.time()
            
            #waterpipe2_3
            result_wp2_3 = run_pipe(cmd_wp2_3,"waterpipe2_3",ahn2tile,stcounterstr)
            if result_wp2_3.ok != True :
                continue
            
            endwp3 = time.time()

            
            startwpn = time.time()
            #waterpipe2_norm
            if retain_norm == True :

                print('- waterpipe2_norm')
                result_wp2_norm = run_pipe(cmd_wp2_norm, "waterpipe2_norm",ahn2tile,stcounterstr)
                if result_wp2_norm.ok != True :
                    continue
                
            endwpn = time.time()
            print('- waterpipe2_clean')
            startwpc = time.time()
            #waterpipe2_clean
            result_wp2_clean = run_pipe(cmd_wp2_clean, "waterpipe2_clean",ahn2tile,stcounterstr)
            if result_wp2_clean.ok != True :
                continue
                
            endwpc = time.time()
                
                
                
        else:
            print('-- no subtile '+stcounterstr+' present.')
                
                
    if i==25:
        print('done with tile '+ahn2tile+'.')
                        
        
else:

    print('tile '+ahn2tile+' not present in files considered ')
                        

end= time.time()

totaldifftime = end - start
difftimewp1 = endwp1 - startwp1
difftimewp2 = endwp2 - startwp2
difftimewp3 = endwp3 - startwp3
difftimewpn = endwpn - startwpn
difftimewpc = endwpc - startwpc

print(("total elapsed time for tile: % sec") % (totaldifftime))
print(("elapsed time in waterpipe2_1 : % sec") % (difftimewp1))
print(("elapsed time in waterpipe2_2 : % sec") % (difftimewp2))
print(("elapsed time in waterpipe2_3 : % sec") % (difftimewp3))
print(("elapsed time in waterpipe2_norm : % sec") % (difftimewpn))
print(("elapsed time in waterpipe2_clean : % sec") % (difftimewpc))




"""
Example usage:

Call from command line as

python run_waterpipe.py AHN2_tile_descriptor ground_file_dir object_file_dir merge_file_dir  Z_cutoff k [--retain_norm]

                                                                                               [0.06] [9]

"""
