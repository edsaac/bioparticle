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
# $ python3 runCubeDomain.py \
#           [CASES.CSV] [TEMPLATE.IN] [RUNOPTION] [FLOW.h5]
# 
# Where:
#   - [CASES.CSV] path to csv file with the list of 
#     parameters and the corresponding tags
#   - [TEMPLATE.IN] input file template for PFLOTRAN and 
#     the corresponding tags
#   - [RUNOPTION]:
#       - debugLaptop (default)
#       - deployWorkStation
#       - flowGiven
#         - [FLOW.h5] path to hdf5 file from flow simulation
#
###############################################################

import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from os import system
import sys
import h5py as hdf5

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

def buildHDF5Flow(filePath,outFile):
  f = hdf5.File(filePath,mode="r")
  t_Key  = 'Time:  2.00000E+00 d'
  f1 = f[t_Key]

  uX_Key = 'Liquid X-Flux Velocities'
  uY_Key = 'Liquid Y-Flux Velocities'
  uZ_Key = 'Liquid Z-Flux Velocities'
  ID_Key = 'Natural_ID'

  ID3D = np.transpose(f1[ID_Key],(2,1,0))
  NX = np.shape(ID3D)[2]
  NY = np.shape(ID3D)[1]
  NZ = np.shape(ID3D)[0]

  uX3D = np.transpose(f1[uX_Key],(2,1,0))
  uY3D = np.transpose(f1[uY_Key],(2,1,0))
  uZ3D = np.transpose(f1[uZ_Key],(2,1,0))

  fillX = np.zeros((NZ,NY,1))
  fillY = np.zeros((NZ,1,NX))
  fillZ = np.zeros((1,NY,NX))

  uXAdd = np.append(uX3D,fillX,axis=2)
  uYAdd = np.append(uY3D,fillY,axis=1)
  uZAdd = np.append(uZ3D,fillZ,axis=0)

  uX = np.reshape(uXAdd,-1)
  uY = np.reshape(uYAdd,-1)
  uZ = np.reshape(uZAdd,-1)
  ID = np.reshape(ID3D,-1)

  daysToSeconds = 1./86400.
  uX *= daysToSeconds
  uY *= daysToSeconds
  uZ *= daysToSeconds

  fOUT = hdf5.File(outFile,mode='w')

  fOUT.create_dataset('Internal Velocity X', data=uX)
  fOUT.create_dataset('Internal Velocity Y', data=uY)
  fOUT.create_dataset('Internal Velocity Z', data=uZ)
  fOUT.create_dataset('Cell Ids', data=ID)

  ## Boundary conditions ??
  fOUT.create_dataset('leaking_top', data=uZ)
  fOUT.create_dataset('noFlowSide_right', data=uX)
  fOUT.create_dataset('noFlowSide_left', data=uX)
  fOUT.create_dataset('noFlowSide_north', data=uY)
  fOUT.create_dataset('noFlowSide_south', data=uY)

  fOUT.close()

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
  PFLOTRAN_path = "mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran "
elif "deploy" in runMode:
  PFLOTRAN_path = "mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran "
elif "flow" in runMode:
  PFLOTRAN_path = "mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran "
  try:
    flowFile = str(sys.argv[4])
  except IndexError:
    sys.exit("Flow HDF5 file not found")
  system("rm -rf FLOW; mkdir FLOW")
  buildHDF5Flow(flowFile,"./FLOW/ReadyToTransport.h5")
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
    if ("nX" in current_tag or "nZ" in current_tag) or "nY" in current_tag:
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
if "debug" in runMode or "flow" in runMode:
  system(PFLOTRAN_path + "-pflotranin " + current_file)  ##This will onlt run the last one
elif "deploy" in runMode:
  system("./miscellaneous/handlePIDS.sh")
else:
  print("Run mode not recognized. Defaulted to debug in laptop")