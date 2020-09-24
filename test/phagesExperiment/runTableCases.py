import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from os import system
import sys

## Path to PFLOTRAN executable
PFLOTRAN_path = "$PFLOTRAN_DIR/src/pflotran/pflotran "

## Table with the set of parameters
try:
	parameters_file = str(sys.argv[1])
except IndexError:
	sys.exit("Parameters file not defined :(")

setParameters = read_csv(parameters_file)
total_rows = setParameters.shape[0]

## Template for the PFLOTRAN input file
try:
	template_file = str(sys.argv[2])
except IndexError:
	sys.exit("Template file not found :(")

## Run cases?
try:
	shouldRunPFLOTRAN = "-run" in str(sys.argv[3])
except IndexError:
	shouldRunPFLOTRAN = False


## Tags dictionary for variables in input file
tags =	{
  "Porosity"  : "<porosity>",
  "FlowVel"   : "<flow>",
  "PoreVolume": "<poreVol>",
  "AttachRate": "<katt>",
  "DetachRate": "<kdet>",
  "DecayAq"   : "<decayAq>",
  "DecayIm"   : "<decayIm>",
}

## Delete previous cases
system("rm -rf CASE*")

## Row in the set of parameters table = case to be run
for i in range(total_rows):
  
  ## Create a folder for the case
  current_folder = "./CASE_" + "{0:03}".format(i+1)
  system("mkdir " + current_folder)
  
  ## Copy template input file to folder
  system("cp " + template_file + " " + current_folder+"/pflotran.in")
  current_file = current_folder + "/pflotran.in" 
 
  ## Replace tags for values in case
  for current_tag in tags:
    COMM = "sed -i 's/" + tags[current_tag] + "/"\
      +'{:.3E}'.format(setParameters.loc[i,tags[current_tag]])\
      + "/g' " + current_file
    system(COMM)
  
  ## Run PFLOTRAN in that case
  if shouldRunPFLOTRAN:
    #print(PFLOTRAN_path + "-pflotranin " + current_file)
    system(PFLOTRAN_path + "-pflotranin " + current_file)
  