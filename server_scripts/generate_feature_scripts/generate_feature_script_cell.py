"""
python script to generate server scripts for feature extraction from AHN3 in cells using laserchicken following current implementation
"""

import os
import argparse
import numpy as np



def read_inputfile(infile):

    retval = 0
    if os.path.isfile(infile) == True:

        input_params={}
        
        with open(infile,"r") as ifo:
            for line in ifo:
                line = line.split('#',1)[0]
                key_val = line.strip().split("::")
                if len(key_val) == 2 :
                    input_params[key_val[0].strip()] = key_val[1].strip()

        if len(input_params) != 13:
            print('mismatched number of input parameters')
            retval =1

    else:
        print('invalid/non-existent input file')
        retval = 1
            

    return retval, input_params





parser = argparse.ArgumentParser()

parser.add_argument('parameter_input_file',help='input file containing required parameters')


args = parser.parse_args()

input_file = args.parameter_input_file

retval, input_params = read_inputfile(input_file)

if retval == 1:
    pass

else:


    #print(input_params)

    
    loc_VM = input_params['location_of_VMs']
    loc_master_VM = input_params['loc_master_VM']
    num_VM_in = input_params['number_of_VMs']
    num_procs = input_params['number_of_processes']
    fs_path_VM = input_params['feature_script_path_VM']
    webdav_path = input_params['webdav_path']
    clone_data_path = input_params['local_clone_data_path']
    in_data_dir = input_params['input_data_dir']
    out_data_dir = input_params['output_data_dir']
    sc_lc = input_params['script_laserchicken']
    spat_resol = input_params['spatial_resolution_cell']
    lc_path = input_params['laserchicken_path']
    targ_path = input_params['targets_path']

    #data type conversion as required

    numVM = int(num_VM_in) -1
    numpr = int(num_procs)
    sr = int(spat_resol)

    

    
    #-----------------------------------------
    #feature_run_all.sh
    
    #input lines ---
    feature_run_all_line1 = 'for f in `seq 1 '+str(numVM)+'`; do echo "Running feature extraction on server $f"; nohup ssh -i /tmp/id_rsa '+loc_VM+' "'+fs_path_VM+'/feature_run_tiles_$f.sh;" & done; \ '
    
    feature_run_all_line2 = 'echo "Running feature extraction on server 0"; nohup '+fs_path_VM+'/feature_run_tiles_0.sh; '
    #---
    
    with open("feature_run_all.sh","w") as tf:
        tf.write(feature_run_all_line1+'\n')
        tf.write(feature_run_all_line2+'\n')
        
        
    #-----------------------------------------
    
    
    
    #-----------------------------------------
    #feature_run_tiles_?.sh
    
    for i in np.arange(numVM):
        
        istr = str(i)
        
        #input lines --
        l1 = 'xargs --arg-file=/'+fs_path_VM+'/feature_tiles_'+istr+'.sh \ '
        l2 = '      --max-procs='+str(numpr)+'  \ '
        l3 = '      --replace \ '
        l4 = '      --verbose \ '
        l5_1 = '      /bin/sh -c "[ -f '+clone_data_path+'/'+out_data_dir+'/{}.ply ] && echo '
        l5_2 = "'File {}.ply already exists' || echo 'Creating file {}.ply'; "
        l5_3 = 'python '+fs_path_VM+'/'+sc_lc+' '+lc_path+' '+clone_data_path+'/'+in_data_dir+'/{}.LAZ '+targ_path+'/{}_target.laz '+str(sr)+' '+clone_data_path+'/'+out_data_dir+'/{}.ply;"'
        l5 = l5_1+l5_2+l5_3
        
        with open("feature_run_tiles_"+istr+".sh","w") as tf:
            tf.write(l1+'\n')
            tf.write(l2+'\n')
            tf.write(l3+'\n')
            tf.write(l4+'\n')
            tf.write(l5+'\n')

    #-----------------------------------------


    #-----------------------------------------
    #feature_run_tiles_redo.sh

    l1 = 'echo "Running redo feature extraction on server 0"; \ '
    l2 = 'nohup xargs --arg-file=/'+fs_path_VM+'/feature_tiles_redo.sh \ '
    l3 = '      --max-procs=1  \ '
    l4 = '      --replace \ '
    l5 = '      --verbose \ '
    l6_1 = '      /bin/sh -c "[ -f '+clone_data_path+'/'+out_data_dir+'/{}.ply ] && echo '
    l6_2 = "'File {}.ply already exists' || echo 'Creating file {}.ply'; "
    l6_3 = 'python '+fs_path_VM+'/'+sc_lc+' '+lc_path+' '+clone_data_path+'/'+in_data_dir+'/{}.LAZ '+targ_path+'/{}_target.laz '+str(sr)+' '+clone_data_path+'/'+out_data_dir+'/{}.ply;"'
    l6 = l5_1+l5_2+l5_3

    with open("feature_run_tiles_"+istr+".sh","w") as tf:
        tf.write(l1+'\n')
        tf.write(l2+'\n')
        tf.write(l3+'\n')
        tf.write(l4+'\n')
        tf.write(l5+'\n')
        tf.write(l6+'\n')

    #-----------------------------------------


    #-----------------------------------------
    #feature_copy_files.sh

    l1 = '"Copying feature scripts to server 0"; \ '
    l2 = 'scp feature_run_all.sh '+loc_master_VM+':'+fs_path_VM+'/; \ '
    l3 = 'scp feature_move_all.sh '+loc_master_VM+':'+fs_path_VM+'/; \ '
    l4 = 'scp feature_run_tiles_redo.sh '+loc_master_VM+':'+fs_path_VM+'/; \ '
    l5 = 'scp feature_tiles_redo.sh '+loc_master_VM+':'+fs_path_VM+'/; \ '
    l6 = 'scp feature_move_redo.sh '+loc_master_VM+':'+fs_path_VM+'/; \ '
    l7 = 'for f in `seq 0 '+str(numVM)+'`; do echo "Copying feature scripts to server $f"; echo $f; scp '+sc_lc+' '+loc_VM+'/'+fs_path_VM+'/ ; scp feature_run_tiles_$f.sh '+loc_VM+'/'+fs_path_VM+'/ ; scp feature_tiles_$f.sh '+loc_VM+'/'+fs_path_VM+'/ ; done '

    with open("feature_copy_files.sh", "w") as tf:
        tf.write(l1+'\n')
        tf.write(l2+'\n')
        tf.write(l3+'\n')
        tf.write(l4+'\n')
        tf.write(l5+'\n')
        tf.write(l6+'\n')
        tf.write(l7+'\n')

    #------------------------------------------

    #------------------------------------------
    #feature_get_files.sh

    l1 = 'for f in `seq 0 '+str(numVM)+'`; do echo "Getting files from server $f"; scp -r '+loc_VM+':'+clone_data_path+'/'+out_data_dir+'/ ../../data/; done; '

    with open("feature_get_files.sh", "w") as tf:
        tf.write(l1+'\n')


    #-------------------------------------------
    #feature_move_all.sh
    l1 = 'for f in `seq 1 '+str(numVM)+'`; do echo "Moving feature files on server $f"; nohup ssh -i /tmp/id_rsa '+loc_VM+' "/bin/cp -rf '+clone_data_path+'/'+out_data_dir+'/ '+webdav_path+'/ ;" & done; \ '
    l2 = 'echo "Moving feature files on server 0"; nohup /bin/cp -rf '+clone_data_path+'/'+out_data_dir+'/ '+webdav_path+'/ ; '

    with open("feature_move_all.sh","w") as tf:
        tf.write(l1+'\n')
        tf.write(l2+'\n')

    #--------------------------------------------
    #feature_move_redo.sh
    l1 = 'echo "Moving redo feature files on server 0"; \ "'
    l2 = 'nohup /bin/cp -n '+clone_data_path+'/'+out_data_dir+'/ '+webdav_path+'/ ; '

    with open('feature_move_redo.sh','w') as tf:
        tf.write(l1+'\n')
        tf.write(l2+'\n')


    #---------------------------------------------

    #---------------------------------------------
    # feature_get_lists.sh
    l1 = 'for f in `seq 0 '+str(numVM)+'`; do echo "Creating list on server $f"; ssh '+loc_VM+' "echo -n > '+fs_path_VM+'/feature_list_$f.txt;" done; \ '
    l2 = 'for f in `seq 0 '+str(numVM)+'`; do echo " Getting list from server $f"; scp  '+loc_VM+':'+fs_path_VM+'/feature_list_$f.txt ../../data/lists/; done: \ '
    l3 = 'for f in `seq 0 '+str(numVM)+'`; do echo "Deleting list from server $f"; ssh '+loc_VM+' "rm  '+fs_path_VM+'/feature_list_$f.txt;" done; '

    with open('feature_get_lists.sh','w') as tf:
        tf.write(l1+'\n')
        tf.write(l2+'\n')
        tf.write(l3+'\n')







"""
Example usage:

python generate_feature_script_cell.py input_file

e.g.

                                        ahn3_100m_filtered_scriptgen_input.txt


"""
                
