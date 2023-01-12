## PFLOTRAN
import jupypft.model as mo
import jupypft.parameter as pm
import jupypft.attachmentRateCFT as arCFT
import jupypft.plotBTC as plotBTC

import numpy as np
import matplotlib.pyplot as plt
import pathlib
import streamlit as st
from os import system

def dx_to_str(Dx):
    Dx_string = np.array_str(Dx, max_line_width=32, precision=4)
    Dx_string = Dx_string.replace("[","").replace("]","").replace("\n","\\\\ \\n    ")
    return Dx_string

def generateDX(setbackDistance):
    rs = setbackDistance
    templatefile = pathlib.Path("xline.tpl.geo")
    geofile = pathlib.Path("xline.geo")
    gmshfile = pathlib.Path("xline.msh")

    system(f"cp {templatefile} {geofile}; sed -i 's/<setbackDistance>/{rs:.2f}/' {geofile}")
    system(f"gmsh -1 {geofile} > /dev/null")

    nodes = []
    inNodes = False
    with open(gmshfile, 'rb') as f:
        while True:
            line = f.readline().decode("utf-8")
            if "$Nodes" in line: inNodes = True
            if inNodes: nodes.append(line.strip().split(" "))
            if "$EndNodes" in line: break
    geofile.unlink()
    gmshfile.unlink()

    nodes.pop()
    nodes.pop(0)
    nodes.pop(0)

    xcoords = [float(node[1]) for node in nodes]
    xcoords.sort()
    xcoords = np.array(xcoords)

    Dx = np.around(np.diff(xcoords), 2)
    return Dx

def generateDY():

    templatefile = pathlib.Path("yline.tpl.geo")
    geofile = pathlib.Path("yline.geo")
    gmshfile = pathlib.Path("yline.msh")

    system(f"cp {templatefile} {geofile}")
    system(f"gmsh -1 {geofile} > /dev/null")

    nodes = []
    inNodes = False
    with open(gmshfile, 'rb') as f:
        while True:
            line = f.readline().decode("utf-8")
            if "$Nodes" in line: inNodes = True
            if inNodes: nodes.append(line.strip().split(" "))
            if "$EndNodes" in line: break

    geofile.unlink()
    gmshfile.unlink()

    nodes.pop()
    nodes.pop(0)
    nodes.pop(0)

    xcoords = [float(node[1]) for node in nodes]
    xcoords.sort()
    xcoords = np.array(xcoords)

    Dx = np.around(np.diff(xcoords), 2)  
    return Dx

## Setback distance
setbackDist = 15.

## Temperatures
Ref,Atm,Tin = pm.Real(tag="<initialTemp>",value=10.,units="C",mathRep="$$T_{0}$$"),\
              pm.Real(tag="<atmosphereTemp>",value=10,units="C",mathRep="$$T_{atm}$$"),\
              pm.Real(tag="<leakageTemp>",value=10., units="m³/d",mathRep="$$T_{in}$$")

LongDisp  = pm.Real(tag="<longDisp>",value=1e-1,units="m",mathRep="$$\\alpha_L$$")
TransDisp = pm.Real(tag="<transDisp>",value=1e-3,units="m",mathRep="$$\\alpha_T$$")

#Gradients
GX,GY,GZ  = pm.Real(tag="<GradientX>",value=0.,units="-",mathRep="$$\partial_x h$$"),\
            pm.Real(tag="<GradientY>",value=0.,units="-",mathRep="$$\partial_y h$$"),\
            pm.Real(tag="<Gradient>>",value=0.,units="-",mathRep="$$\partial_z h$$")

## Dimensions
## LX = setbackDistance + 10m downstream + 5m upstream
LX,LY,LZ = pm.Real("<LenX>",value=setbackDist+15,units="m",mathRep="$$LX$$"),\
           pm.Real("<LenY>",value=10,units="m",mathRep="$$LY$$"),\
           pm.Real("<LenZ>",value=10,units="m",mathRep="$$LZ$$")

## Permeability
kX,kY,kZ = pm.Real(tag="<PermX>",value=1.0E-8,units="m²",mathRep="$$k_{xx}$$"),\
           pm.Real(tag="<PermY>",value=1.0E-8,units="m²",mathRep="$$k_{yy}$$"),\
           pm.Real(tag="<PermZ>",value=1.0E-8,units="m²",mathRep="$$k_{zz}$$")

theta = pm.Real(tag="<porosity>",value=0.35,units="adim",mathRep="$$\\theta$$")

## Extraction well
outX1,outX2 = pm.Real(tag="<outX1>",value=10.0,units="m",mathRep="$$x_{1,Q_{out}}$$"),\
              pm.Real(tag="<outX2>",value=10.0,units="m",mathRep="$$x_{2,Q_{out}}$$")

outY1,outY2 = pm.Real(tag="<outY1>",value=LY.value/2.,units="m",mathRep="$$y_{1,Q_{out}}$$"),\
              pm.Real(tag="<outY2>",value=LY.value/2.,units="m",mathRep="$$y_{2,Q_{out}}$$")

outZ1,outZ2 = pm.Real(tag="<outZ1>",value=LZ.value/2.   ,units="m",mathRep="$$z_{1,Q_{out}}$$"),\
              pm.Real(tag="<outZ2>",value=LZ.value - 1.0,units="m",mathRep="$$z_{2,Q_{out}}$$")

## Extraction rate
Qout = pm.Real(tag="<outRate>",value=-21.0,units="m³/d",mathRep="$$Q_{out}$$")

## Injection point
inX1,inX2 = pm.Real(tag="<inX1>",value=outX1.value + setbackDist,units="m",mathRep="$$x_{1,Q_{in}}$$"),\
            pm.Real(tag="<inX2>",value=outX2.value + setbackDist,units="m",mathRep="$$x_{2,Q_{in}}$$")

inY1,inY2 = pm.Real(tag="<inY1>",value=outY1.value + 0.0,units="m",mathRep="$$y_{1,Q_{in}}$$"),\
            pm.Real(tag="<inY2>",value=outY2.value + 0.0,units="m",mathRep="$$y_{2,Q_{in}}$$")

inZ1,inZ2 = pm.Real(tag="<inZ1>",value=LZ.value - 5.0,units="m",mathRep="$$z_{1,Q_{in}}$$"),\
            pm.Real(tag="<inZ2>",value=LZ.value - 1.0,units="m",mathRep="$$z_{2,Q_{in}}$$")

## Concentration
C0 = pm.Real("<initialConcentration>", value=1.0, units="mol/L")

## Injection rate
Qin = pm.Real(tag="<inRate>",value=0.24, units="m³/d",mathRep="$$Q_{in}$$")

## Grid
# nX,nY,nZ = pm.Integer("<nX>",value=41,units="-",mathRep="$$nX$$"),\
#            pm.Integer("<nY>",value=41 ,units="-",mathRep="$$nY$$"),\
#            pm.Integer("<nZ>",value=1,units="-",mathRep="$$nZ$$")

Dxx, Dyy, Dzz = generateDX(setbackDistance=setbackDist), generateDY(), [1]

## Fix rounding errors
deltaDxx = Dxx.sum() - LX.value
Dxx[-1] = Dxx[-1] - deltaDxx

deltaDyy = Dyy.sum() - LY.value
Dyy[-1] = Dyy[-1] - deltaDyy

nX,nY,nZ = pm.Integer("<nX>",value=len(Dxx),units="-",mathRep="$$nX$$"),\
            pm.Integer("<nY>",value=len(Dyy) ,units="-",mathRep="$$nY$$"),\
            pm.Integer("<nZ>",value=len(Dzz),units="-",mathRep="$$nZ$$")

dX,dY,dZ = pm.JustText("<dX>"),\
           pm.JustText("<dY>"),\
           pm.JustText("<dZ>")

CellRatio = { 'X' : 2.0, 'Y' : 3.0, 'Z' : 0.75 }
#CellRatio = { 'X' : 1.00, 'Y' : 0.50, 'Z' : 0.75 }

dX.value = dx_to_str(Dxx)
dY.value = dx_to_str(Dyy)

if nZ.value == 1:
    dZ.value = LZ.strValue
else:
    dZ.value = mo.buildDXYZ(LZ.value,CellRatio['Z'],nZ.value,hasBump=False)

# print("DX", dX.value)
# print("DY", dY.value)

# Time config
endTime = pm.Real("<endTime>",value=20.,units="d")

## Bioparticle
dc = pm.Real(tag="<diamCollector>",value=0.0, units="m",mathRep="$$d_{c}$$")
dp = pm.Real(tag="<diamParticle>",value=0.0, units="m",mathRep="$$d_{c}$$")
Hamaker = pm.Real(tag="<hamakerConstant>",value=0.0, units="m",mathRep="$$d_{c}$$")
rhop = pm.Real(tag="<rhoParticle>",value=0.0, units="m",mathRep="$$d_{c}$$")
alpha = pm.Real(tag="<stickingEfficiency>",value=0.0, units="m",mathRep="$$d_{c}$$")

kDet = pm.Real(tag="<kdet>",value=1.0E-30,units="1/s",mathRep="$$k_{det}$$")

decayAq,decayIm = pm.Real(tag="<decayAq>",value=1.0E-30,units="1/s",mathRep="$$\lambda_{aq}$$"),\
                  pm.Real(tag="<decayIm>",value=1.0E-30,units="1/s",mathRep="$$\lambda_{im}$$")

caseDict = {
    "Temp":{
        "Reference" : Ref,
        "Atmosphere": Atm,
        "Injection" : Tin },
   "longDisp":LongDisp,
   "transDisp":TransDisp,
   "Gradient":{
       "X" :GX,
       "Y" :GY,
       "Z" :GZ },
   "L":{
       "X" :LX,
       "Y" :LY,
       "Z" :LZ },
   "k":{
       "X" :kX,
       "Y" :kY,
       "Z" :kZ },
   "theta":theta,
   "outCoord":{
       "X" : { 1 : outX1,
               2 : outX2},
       "Y" : { 1 : outY1,
               2 : outY2},
       "Z" : { 1 : outZ1,
               2 : outZ2}},
   "inCoord":{
       "X" : { 1 : inX1,
               2 : inX2},
       "Y" : { 1 : inY1,
               2 : inY2},
       "Z" : { 1 : inZ1,
               2 : inZ2}},
    "C0":C0,
    "Q":{"In":Qin,
         "Out":Qout},
    "nGrid":{"X":nX,
             "Y":nY,
             "Z":nZ},
    "dGrid":{"X":dX,
             "Y":dY,
             "Z":dZ},
    "endTime":endTime,
    "BIOPARTICLE":{
        "katt" : {
            "dc":dc,
            "dp":dp,
            "Hamaker":Hamaker,
            "rhop":rhop,
            "alpha":alpha
            },
        "kdet" : kDet,
        "decayAq" : decayAq,
        "decayIm" : decayIm}
           }

import pickle
with open('caseDict.pkl', 'wb') as f:
    pickle.dump(caseDict,f)