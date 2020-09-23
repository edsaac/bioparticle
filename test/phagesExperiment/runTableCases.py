import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from os import system
import sys

parameters_file = str(sys.argv[1])
template_file = str(sys.argv[2])

setParameters = read_csv(parameters_file)
total_rows = setParameters.shape[0]

tags =	{
  "Porosity"  : "<porosity>",
  "FlowVel"   : "<flow>",
  "PoreVolume": "<poreVol>",
  "AttachRate": "<katt>",
  "DetachRate": "<kdet>",
  "DecayAq"   : "<decayAq>",
  "DecayIm"   : "<decayIm>",
}

system("rm -rf CASE*")

for i in range(total_rows):
  current_folder = "CASE_" + "{0:03}".format(i+1)
  system("mkdir " + current_folder)
  system("cp " + template_file + " " + current_folder+"/pflotran.in")
  current_file = current_folder + "/pflotran.in" 
 
  for current_tag in tags:
    COMM = "sed -i 's/" + tags[current_tag] + "/"\
      +'{:.3E}'.format(setParameters.loc[i,tags[current_tag]])\
      + "/g' " + current_file
    system(COMM)
  
  print(i)