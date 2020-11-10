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
# $ python3 runSetbackWell.py [CASES.CSV] [TEMPLATE.IN]
# 
# Where:
#   - [CASES.CSV] path to csv file with the list of 
#     parameters and the corresponding tags
#   - [TEMPLATE.IN] input file template for PFLOTRAN and 
#     the corresponding tags
#
###############################################################

import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from os import system
import sys

## Tags dictionary for variables in input file
tagsReplaceable =	{
  "H"         	: "<AquiferThickness>",
  "z_t"       	: "<zTop>",
  "z_b"	      	: "<zBottom>",
  "r_2"	      	: "<AquiferLen>",
  "r_s"	      	: "<setbackDist>",
  "r_s+l_s"   	: "<setbackPlusLeak>",
  "Porosity"  	: "<porosity>",
  "k_x"       	: "<permeabilityX>",
  "k_y"       	: "<permeabilityY>",
  "k_z"       	: "<permeabilityZ>",
  "LongDisp"  	: "<longDisp>",
  "ySpan"     	: "<dummyY>",
  "rateLeaking" : "<rateLeaking>",
  "rateExtract" : "<rateExtraction>",
  "AttachRate"  : "<katt>",
  "DetachRate"  : "<kdet>",
  "DecayAq"     : "<decayAq>",
  "DecayIm"     : "<decayIm>"
}

## Path to PFLOTRAN executable
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

## Delete previous cases
system("rm -rf CASE*")

for i in range(total_rows):
  
  ## Create a folder for the case
  current_folder = "./CASE_" + "{0:03}".format(i+1)
  system("mkdir " + current_folder)
  
  ## Copy template input file to folder
  system("cp " + template_file + " " + current_folder+"/pflotran.in")
  current_file = current_folder + "/pflotran.in" 
 
  ## Replace tags for values in case
  for current_tag in tagsReplaceable:
    COMM = "sed -i 's/" + tagsReplaceable[current_tag] + "/"\
      +'{:.3E}'.format(setParameters.loc[i,tagsReplaceable[current_tag]])\
      + "/g' " + current_file
    system(COMM)
  
  ## Run case
  system(PFLOTRAN_path + "-pflotranin " + current_file + " &")