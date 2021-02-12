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
# $ python3 runCubeDomain.py [CASES.CSV] [TEMPLATE.IN] [RUNOPTION]
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
#from numpy.core import numeric
from pandas import read_csv
from os import system
import sys

## New functions 
import jupypft.model as mo
import jupypft.parameter as pm
buildDXYZ = mo.buildDXYZ

## Case Name
titleCase = pm.JustText("<Name>")

## Grid creation
CellRatioX = pm.Real("<CellRatioX>")
CellRatioY = pm.Real("<CellRatioY>")
CellRatioZ = pm.Real("<CellRatioZ>")
nX = pm.Integer("<nX>")
nY = pm.Integer("<nY>")
nZ = pm.Integer("<nZ>")
dX = pm.JustText("<dX>")
dY = pm.JustText("<dY>")
dZ = pm.JustText("<dZ>")

## GEOMETRY  
Len     	  = pm.Real("<AquiferLen>")
H         	= pm.Real("<DomainDepth>")
H_1         = pm.Real("<zInBetweenLayers>")
r_s	      	= pm.Real("<setbackDist>")
r_sl_s   	  = pm.Real("<setbackPlusLeak>")
LeakingYN   = pm.Real("<leakingYNorth>")
LeakingYS   = pm.Real("<leakingYSouth>")
z_t       	= pm.Real("<wellZTop>")
z_b	      	= pm.Real("<wellZBottom>")
xyWell	   	= pm.Real("<wellXY>")

## MATERIALS
### Layer(1) | Top
theta1     = pm.Real("<porosity1>")
k_x1       = pm.Real("<permX1>")
k_y1       = pm.Real("<permY1>")
k_z1       = pm.Real("<permZ1>")
### Layer(2) | Bottom
theta2    	= pm.Real("<porosity2>")
k_x2        = pm.Real("<permX2>")
k_y2        = pm.Real("<permY2>")
k_z2        = pm.Real("<permZ2>")
## FLOW CONDITIONS 
WaterTable  = pm.Real("<boundaryWaterTable>")
q_in        = pm.Real("<rateLeaking>")
Q_out       = pm.Real("<rateExtraction>")
C0          = pm.Real("<initialConcentration>")
## BIOPARTICLE
AttachRate  = pm.Real("<katt>")
DetachRate  = pm.Real("<kdet>")
#DecayAq     = jpvar.Simple("<decayAq>")
DecayIm     = pm.Real("<decayIm>")
## BREAKTHROUGH CURVE
IOdT        = pm.Real("<obsTimeStep>")
IOObsZ      = pm.Real("<observationAtWell>")
## TIMESTEPPING
deltaT      = pm.Real("<desiredTimeStep>")
warmUpT     = pm.Real("<warmUpTime>")
## TEMPERATURE
TEMP_0      = pm.Real("<initialTemperature>")
TEMP_Atm    = pm.Real("<atmosphereTemperature>")
TEMP_Leak   = pm.Real("<leakageTemperature>")

listOfObjs = pm.Parameter.list_of_vars()

## Modes

try:
  runMode = str(sys.argv[3])
except IndexError:
  print("Runmode not specified, debug assumed")
  runMode = "debugLaptop"

if "debug" in runMode:
  mo.Model._execPath = "/home/edwin/Apps/PFLOTRAN/pflotran/buildExperimental/pflotran"
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
wholeTable = read_csv(parameters_file)
total_rows = wholeTable.shape[0]

# Check that tags in CSV are in dictionary

## Delete previous cases
system("rm -rf CASE*")


for i in range(total_rows):
  f = wholeTable.loc[i]
  caseName = f.loc[titleCase.tag] 
  
  ## Create a folder for the case
  current_folder = "./CASE" + "{0:02}".format(i+1)
  current_file = current_folder + "/" + caseName +".in"
  system("mkdir " + current_folder)
  
  caseModel = mo.Model(
    templateFile=template_file,
    runFile = current_file
    )
    
  ## Copy template input file to folder
  caseModel.cloneTemplate()
  
  ## Replace tags for values in case
  for qp in listOfObjs:
    t = qp.tag
    if "dX" in t:
      value = buildDXYZ(
        f.loc[Len.tag],
        f.loc[CellRatioX.tag],
        f.loc[nX.tag],
        hasBump=True)
    elif "dY" in t:
      value = buildDXYZ(
        f.loc[Len.tag],
        f.loc[CellRatioY.tag],
        f.loc[nY.tag],
        hasBump=True)
    elif "dZ" in t:
      value = buildDXYZ(
        f.loc[H.tag],
        f.loc[CellRatioZ.tag],
        f.loc[nZ.tag],
        hasBump=False)
    else:
      value = f.loc[t]
    
    qp.value= value
    print(qp.tag,
          qp.value,
          qp.strValue)
    caseModel.replaceTagInFile(qp)
  
  ## Run case
  #system(PFLOTRAN_path + "-pflotranin " + current_file + " &")
if "debug" in runMode:
  caseModel.runModel()
elif "deploy" in runMode:
  mo.Model.runAllModels(folderPrefix="CASE",nProcs=4)
else:
  print("Run mode not recognized. Defaulted to debug in laptop")
  
system('''
  rm -rf CASE_GroupedResults; mkdir CASE_GroupedResults
  cp CASE**/*mas* CASE_GroupedResults
  ''')

mo.Model.folderFixedToCSV(folder="CASE_GroupedResults")