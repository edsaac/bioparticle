# Setback distance for a well 

<p align="right" style="font-size:10px;">
<a href="https://github.com/edsaac/bioparticle/tree/master/test/setbackDistanceWell">
	<img src="https://img.shields.io/badge/Find me -in the repo-purple?style=for-the-badge&logo=github">
</a>
</p>

<p align="center" style="font-size:10px;">
<a href="https://github.com/edsaac/bioparticle/tree/master/test/setbackDistanceWell">
	<img src="https://img.shields.io/badge/IsThisWorking&#10067; -NO :(-red ?style=for-the-badge">
</a>
</p>


### What is this experiment?
Flow towards a well with a leaking source at some distance. 

### What does the code do?
`mycode.py` reads a CSV file with a list of cases of parameters for the case to run:

```
  REACTION_SANDBOX
    BIOPARTICLE
      RATE_ATTACHMENT <katt> 1/s
      RATE_DETACHMENT <kdet> 1/s
    /
  /
```
the tags `<katt>` and `<kdet>` are replaced for the list of values indicated in the csv-file, in the column with the same header. 

### How to run this test?
```
$ python3 runMultipleCases.py [CSV_PARAMETERS] [TEMPLATE_FILE] -run
```
Where:
- `[CASES.CSV]`: path to csv file with the list of parameters and the corresponding tags
- `[TEMPLATE.IN]`: input file template for PFLOTRAN and the corresponding tags

### References for this experiment:

- Schijven, J. F., Hassanizadeh, S. M., & de Roda Husman, A. M. (2010). Vulnerability of unconfined aquifers to virus contamination. Water Research, 44(4), 1170–1181. [![DOI:10.1016/j.watres.2010.01.002](https://zenodo.org/badge/DOI/10.1016/j.watres.2010.01.002.svg)](https://linkinghub.elsevier.com/retrieve/pii/S0043135410000126)
<p>&nbsp;</p>

***

## Description

<p>
A leaking pipe at some distance from an extraction well.
</p>

|Aquifer geometry | | Value | Unit |
|---|---|--:|:--|


<p>&nbsp;</p>

|Particle parameters | | Value | Unit |
|---|---|--:|:--|

<p>&nbsp;</p>

***

## **List of parameters**


***

## **PFLOTRAN Simulation**

<p>&nbsp;</p>

_______

<a href="https://edsaac.github.io/bioparticle/listTests.html">
	<img alt="Back" src="https://img.shields.io/badge/&#11013;-Go back-purple?style=for-the-badge">
</a>

<p align="right">
    <img src="https://img.shields.io/badge/Works on-my machine-purple?style=for-the-badge">
    <img src="https://img.shields.io/badge/-&#127802;-purple?style=for-the-badge">
</p>
