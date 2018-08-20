import argparse
import time
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('path_of_laserchicken', help='The path of laserchicken')
parser.add_argument('input', help='absolute path of input point cloud')
parser.add_argument('target', help='target points as las file')
parser.add_argument('radius', help='radius of the volume')
parser.add_argument('output', help='absolute path of output point cloud')
args = parser.parse_args()

import sys
sys.path.insert(0, args.path_of_laserchicken)

from laserchicken import read_las
from laserchicken.keys import point
from laserchicken.volume_specification import Cell
from laserchicken.compute_neighbors import compute_neighborhoods
from laserchicken.feature_extractor import compute_features
from laserchicken.write_ply import write

print("------ Import is started ------")

pc = read_las.read(args.input)
target = read_las.read(args.target)

print(("Number of points: %s ") % (pc[point]['x']['data'].shape[0]))
print(("Number of points in target: %s ") % (target[point]['x']['data'].shape[0]))

print("------ Computing neighborhood is started ------")

start = time.time()

#compute_neighborhoods is now a generator. To get the result of a generator the user
#needs to call next(compute_neighborhoods). The following shows how to get the results.
#
#indices_cyl=compute_neighborhoods(pc, target, InfiniteCylinder(np.float(args.radius)))
#
neighbors=compute_neighborhoods(pc, target, Cell(np.float(args.radius)))
iteration=0
target_idx_base=0
for x in neighbors:
  end = time.time()
  difftime=end - start
  print(("build kd-tree: %f sec") % (difftime))
  print("Computed neighborhoods list length at iteration %d is: %d" % (iteration,len(x)))

  start1 = time.time()
  print("------ Feature calculation is started ------")
  compute_features(pc, x, target_idx_base, target, ['max_z','min_z','mean_z','median_z','std_z','var_z','coeff_var_z','skew_z','kurto_z',
#'sigma_z','perc_20','perc_40','perc_60','perc_80','perc_90','echo_ratio','pulse_penetration_ratio','point_density','eigenv_1','eigenv_2','eigenv_3'], Cell(np.float(args.radius)))
'perc_20','perc_40','perc_60','perc_80','perc_90','pulse_penetration_ratio','point_density','eigenv_1','eigenv_2','eigenv_3'], Cell(np.float(args.radius)))
  target_idx_base+=len(x)
  end1 = time.time()
  difftime1=end1 - start1
  print(("feature calc: %f sec") % (difftime1))
  iteration+=1


write(target,args.output)

#
# example usage: computefea_wtargets_cylinder.py D:/GitHub/eEcoLiDAR/develop-branch/eEcoLiDAR/ D:/GitHub/eEcoLiDAR/myPhD_escience_analysis/test_data/testdata.las D:/GitHub/eEcoLiDAR/myPhD_escience_analysis/test_data/testdata.las 50 D:/GitHub/eEcoLiDAR/myPhD_escience_analysis/test_data/testdata.ply
#
