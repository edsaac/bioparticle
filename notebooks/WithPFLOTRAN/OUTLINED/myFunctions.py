from os import system
import pickle

## PFLOTRAN
import jupypft.model as mo
import jupypft.parameter as pm
import jupypft.plotBTC as plotBTC

def resetPickle():
    mo.Model.resetListOfModels()
    global caseDict
    with open('caseDict.pkl', 'rb') as f:
        caseDict = pickle.load(f)
    
    pm.Parameter.rebuildListOfObjects(caseDict)
    
    global listOfAllParameters
    listOfAllParameters = pm.Parameter.list_of_vars()
    
    system("rm -rf CASE*")
    
def plotResults():
    system("rm -rf MASSBALANCES; mkdir MASSBALANCES")
    system("cp ./CASE**/*-mas.dat ./MASSBALANCES")
    mo.Model.folderFixedToCSV("MASSBALANCES")

    waterDensity = 999.65
    m3ToL = 1000.

    plotBTC.plotMassBalancesInFolder(
        folderToPlot="MASSBALANCES",
        indices = {'t':"Time [d]",\
                   'q':"ExtractWell Water Mass [kg/d]",\
                   'm':"ExtractWell Vaq [mol/d]"},
        normalizeWith={'t':1.0,'q':waterDensity/m3ToL,'m':1.0},
        legendTitle = legendTitle)
    
def buildSim(caseName):
    ## Create a folder for the case
    currentFolder = "./CASE_{0}".format(caseName)
    currentFile = currentFolder + "/" + caseName +".in"
    system("mkdir " + currentFolder)
    
    ## Initialize PFLOTRAN model
    BoxModel = mo.Model(
        templateFile = templateFile,
        runFile = currentFile,
        execPath = execPath,
        verbose=True
        )
       
    ## Copy template input file to folder
    BoxModel.cloneTemplate()
    
    ## Replace tags for values in case
    for parameter in listOfAllParameters:
        BoxModel.replaceTagInFile(parameter)

    return BoxModel