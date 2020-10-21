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
#
###############################################################

import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from os import system
import sys

tagsCaseName =	{  
  "Title"	   	  : "<Name>"
}

## Tags dictionary for variables in input file
tagsReplaceable =	{
  ## GEOMETRY  
  "L"	      	  : "<AquiferLen>",
  "H"         	: "<DomainDepth>",
  ## DISCRETIZATION
  "dX"          : "<dX>",
  "dZ"          : "<dZ>"
}

## Path to PFLOTRAN executable
GMSH_path = "/home/edwin/Apps/gmsh-4.6.0-Linux64/bin/gmsh "

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
  current_folder = "./"
    
  ## Copy template input file to folder
  fileName = setParameters.loc[i,tagsCaseName["Title"]]
  system("cp " + template_file + " " + fileName + ".geo")
  
  current_file = current_folder + "/" + fileName +".geo"
 
  ## Replace tags for values in case
  for current_tag in tagsReplaceable:
    if "nX" in current_tag or "nZ" in current_tag:
      Value2Text = '{:}'.format(setParameters.loc[i,tagsReplaceable[current_tag]])
    else:
      Value2Text = '{:.2E}'.format(setParameters.loc[i,tagsReplaceable[current_tag]])
    
    COMM = "sed -i 's/" + tagsReplaceable[current_tag] + "/"\
      + Value2Text \
      + "/g' " + current_file
    system(COMM)
  
  ## Run case
  #system(PFLOTRAN_path + "-pflotranin " + current_file + " &")
  system(GMSH_path + " " + current_file)