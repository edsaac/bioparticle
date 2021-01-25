import jupypft.model as mo
import jupypft.parameter as pm

## Case Name
titleCase = pm.JustText("<Name>")

## Number of elements
nX = pm.Integer("<nX>")
nY = pm.Integer("<nY>")
nZ = pm.Integer("<nZ>")

## Individual separation of cells
dX = pm.JustText("<dX>")
dY = pm.JustText("<dY>")
dZ = pm.JustText("<dZ>")

CellRatioX = pm.Real("<CellRatioX>")
CellRatioY = pm.Real("<CellRatioY>")
CellRatioZ = pm.Real("<CellRatioZ>")

## Geometry
Len     	= pm.Real("<AquiferLen>")
H         	= pm.Real("<DomainDepth>")
H_1         = pm.Real("<zInBetweenLayers>")
r_s	      	= pm.Real("<setbackDist>")
r_sl_s   	= pm.Real("<setbackPlusLeak>")
LeakingYN   = pm.Real("<leakingYNorth>")
LeakingYS   = pm.Real("<leakingYSouth>")
z_t       	= pm.Real("<wellZTop>")
z_b	      	= pm.Real("<wellZBottom>")
xyWell	   	= pm.Real("<wellXY>")

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

## Flow Conditions
WaterTable  = pm.Real("<boundaryWaterTable>")
q_in        = pm.Real("<rateLeaking>")
Q_out       = pm.Real("<rateExtraction>")
C0          = pm.Real("<initialConcentration>")

## Head Gradient
HeadGradient = pm.Real("<headGradientX>")

## Bioparticle Reaction Sandbox
AttachRate  = pm.Real("<katt>")
DetachRate  = pm.Real("<kdet>")
DecayAq     = pm.Real("<decayAq>")
DecayIm     = pm.Real("<decayIm>")

## Probe location on the extraction well
IOObsZ      = pm.Real("<observationAtWell>")

## Timestepping
deltaT      = pm.Real("<desiredTimeStep>")
warmUpT     = pm.Real("<warmUpTime>")
endTime     = pm.Real("<endTime>")
writeTime   = pm.Real("<obsTimeStep>")
