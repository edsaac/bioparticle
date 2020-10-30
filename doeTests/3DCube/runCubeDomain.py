###############################################################
#  _     _                        _   _      _
# | |__ (_) ___  _ __   __ _ _ __| |_(_) ___| | ___
# | '_ \| |/ _ \| '_ \ / _` | '__| __| |/ __| |/ _ \
# | |_) | | (_) | |_) | (_| | |  | |_| | (__| |  __/
# |_.__/|_|\___/| .__/ \__,_|_|   \__|_|\___|_|\___|
#               |_|
# 
###############################################################
#
# $ python3 runLeakingPoints.py [CASES.CSV] [TEMPLATE.IN]
# 
# Where:
#   - [CASES.CSV] path to csv file with the list of 
#     parameters and the corresponding tags
#   - [TEMPLATE.IN] input file template for PFLOTRAN and 
#     the corresponding tags
#   - [RUNOPTION]:
#       - debugLaptop (default)
#       - deployWorkStation
#
###############################################################

import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from os import system
import sys

def buildDXYZ(L,R,N,bump=False):
  if abs(R) < 1e-10:
    R = 1
  
  if bump:
    L = L/2.0
    N = int(N/2.0)
  
  # Cell-to-cell ratio
  K = np.power(np.abs(R),1/(N-1))
  KPow = np.power(np.ones(N)*K,np.arange(0,N,1,dtype="int16"))

  # Smallest element
  D1 = L/(np.sum(KPow))

  # Array of distances
  Distances = np.zeros(N)
  Distances[0] = D1
  for i in range(1,N-1):
    Distances[i] = Distances[i-1] * K
  Distances[N-1] = L - np.sum(Distances)
  
  if R < 0:
    Distances = np.flip(Distances)
  if bump:
    Definitive = np.concatenate((Distances,np.flip(Distances)))
  else:
    Definitive = Distances
  
  Formatted = ""
  for i in range(len(Definitive)):
    Formatted+="{:.8E} ".format(Definitive[i])
    if i == len(Definitive):
      Formatted+=" \\n    "
    elif i % 2 == 1 and i+1 < len(Definitive):
      Formatted+="\\\\ \\n    "
  
  return Formatted

tagsCaseName =  {  
  "Title"	   	  : "<Name>"
}

tagsGridding = {
  "CellRatioX"  : "<CellRatioX>",
  "CellRatioY"  : "<CellRatioY>",
  "CellRatioZ"  : "<CellRatioZ>"
} 

## Tags dictionary for variables in input file
tagsReplaceable =	{
  ## GEOMETRY  
  "L"	      	  : "<AquiferLen>",
  "H"         	: "<DomainDepth>",
  "H_1"         : "<zInBetweenLayers>",
  "r_s"	      	: "<setbackDist>",
  "r_s+l_s"   	: "<setbackPlusLeak>",
  "LeakingYN"   : "<leakingYNorth>",
  "LeakingYS"   : "<leakingYSouth>",
  "z_t"       	: "<wellZTop>",
  "z_b"	      	: "<wellZBottom>",
  "xyWell"	   	: "<wellXY>",
  ## GRID
  "nX"          : "<nX>",
  "nY"          : "<nY>",
  "nZ"          : "<nZ>",
  "dX"          : "<dX>",
  "dY"          : "<dY>",
  "dZ"          : "<dZ>",
  ## MATERIALS
  ### Layer(1) | Top
  "theta1"    	: "<porosity1>",
  "k_x1"       : "<permX1>",
  "k_y1"       : "<permY1>",
  "k_z1"       : "<permZ1>",
  ### Layer(2) | Bottom
  "theta2"    	: "<porosity2>",
  "k_x2"        : "<permX2>",
  "k_y2"        : "<permY2>",
  "k_z2"        : "<permZ2>",
  ## FLOW CONDITIONS 
  "WaterTable"  : "<boundaryWaterTable>",
  "q_in"        : "<rateLeaking>",
  "Q_out"       : "<rateExtraction>",
  "C0"          : "<initialConcentration>",
  ## BIOPARTICLE
  "AttachRate"  : "<katt>",
  "DetachRate"  : "<kdet>",
  "DecayAq"     : "<decayAq>",
  "DecayIm"     : "<decayIm>",
  ## BREAKTHROUGH CURVE
  "IOdT"        : "<obsTimeStep>",
  "IOObsZ"      : "<observationAtWell>",
  ## TIMESTEPPING
  "deltaT"      : "<desiredTimeStep>",
  "warmUpT"     : "<warmUpTime>"
}

## Path to PFLOTRAN executable
try:
  runMode = str(sys.argv[3])
except IndexError:
  print("Runmode not specified, debug assumed")
  runMode = "debugLaptop"

if "debug" in runMode:
  PFLOTRAN_path = "$PFLOTRAN_DIR/src/pflotran/pflotran "
elif "deploy" in runMode:
  PFLOTRAN_path = "mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran "
else:
  print("Run mode not recognized. Defaulted to debug in laptop")
  PFLOTRAN_path = "$PFLOTRAN_DIR/src/pflotran/pflotran "

## Table with the set of parameters
try:
	parameters_file = str(sys.argv[1])
except IndexError:
	sys.exit("Parameters file not defined :(")

## Template for the PFLOTRAN input file
try:
	template_file = str(sys.argv[2])
except IndexError:
	sys.exit("Template file not found :(")

# Read CSV file with cases 
setParameters = read_csv(parameters_file)
total_rows = setParameters.shape[0]

# Check that tags in CSV are in dictionary

## Delete previous cases
system("rm -rf CASE*")

for i in range(total_rows):
  
  ## Create a folder for the case
  current_folder = "./CASE" + "{0:02}".format(i+1)
  system("mkdir " + current_folder)
  
  ## Copy template input file to folder
  fileName = setParameters.loc[i,tagsCaseName["Title"]]
  system("cp " + template_file + " " + current_folder+"/" + fileName + ".in")
  
  current_file = current_folder + "/" + fileName +".in"
  
  ## Replace tags for values in case
  for current_tag in tagsReplaceable:
    if "nX" in current_tag or "nZ" in current_tag:
      Value2Text = '{:}'.format(setParameters.loc[i,tagsReplaceable[current_tag]])
    elif "dX" in current_tag:
      Value2Text = buildDXYZ(\
      setParameters.loc[i,tagsReplaceable["L"]],\
      setParameters.loc[i,tagsGridding["CellRatioX"]],\
      setParameters.loc[i,tagsReplaceable["nX"]],\
      bump=True)
    elif "dY" in current_tag:
      Value2Text = buildDXYZ(\
      setParameters.loc[i,tagsReplaceable["L"]],\
      setParameters.loc[i,tagsGridding["CellRatioY"]],\
      setParameters.loc[i,tagsReplaceable["nY"]],\
      bump=True)
    elif "dZ" in current_tag:
      Value2Text = buildDXYZ(\
      setParameters.loc[i,tagsReplaceable["H"]],\
      setParameters.loc[i,tagsGridding["CellRatioZ"]],\
      setParameters.loc[i,tagsReplaceable["nZ"]],\
      bump=False) 
    else:
      Value2Text = '{:.3E}'.format(setParameters.loc[i,tagsReplaceable[current_tag]])
    
    COMM = "sed -i 's/" + tagsReplaceable[current_tag] + "/"\
      + Value2Text \
      + "/g' " + current_file
    system(COMM)
  
  ## Run case
  #system(PFLOTRAN_path + "-pflotranin " + current_file + " &")
  if "debug" in runMode:
    system(PFLOTRAN_path + "-pflotranin " + current_file)  ##This will onlt run the last one
  elif "deploy" in runMode:
    system("./miscellaneous/handlePIDS.sh")
  else:
    print("Run mode not recognized. Defaulted to debug in laptop")