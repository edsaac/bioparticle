# Setback distance for a well 

<p align="right"> <b>Source code <a href="https://github.com/edsaac/bioparticle/tree/master/test/setbackDistanceWell"><img src="https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/code.svg"></a></b></p>

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
|Lenght| *L* |25.5|cm|
|Diameter| *Ø* | 1.27|cm|
|Grain size| *d<sub>50</sub>*|0.300|mm|
|Porosity| *φ*|0.33|-|
|Long. Dispersivity| *α<sub>L</sub>*|0.015|cm|

<p>&nbsp;</p>

|Particle parameters | | Value | Unit |
|---|---|--:|:--|
|Size | *d<sub>p</sub>*| ?? | nm |
|Initial concentration| *C<sub>0</sub>*| 1.0 × 10<sup>-5</sup>|mol/L|

<p>&nbsp;</p>

***

## **List of parameters**

<p>&nbsp;</p>

<table>
	<thead>
	<tr>
		<th>Set<br></th>
		<th>Case</th>
	  <th>k<sub>att</sub></th>
    <th>k<sub>det</sub></th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td rowspan=5>Only Attachment</td>
    <td>1A</td>
		<td>0</td>
		<td>0</td>
	</tr>
	<tr>
		<td>2A</td>
		<td>1.0 × 10<sup>-4</sup></td>
		<td>0</td>
	</tr>
	<tr>
		<td>3A</td>
		<td>5.0 × 10<sup>-4</sup></td>
		<td>&nbsp;0</td>
	</tr>
	<tr>
		<td>4A</td>
		<td>1.0 × 10<sup>-3</sup></td>
		<td>0</td>
	</tr>
	<tr>
		<td>5A</td>
		<td>1.0 × 10<sup>-2</sup></td>
		<td>0</td>
	</tr>
	<tr>
    <td rowspan=5>Vary Detachment</td>
    <td>1B</td>
		<td>1.0 × 10<sup>-3</sup></td>
    <td>0</td>
	</tr>
	<tr>
		<td>2B</td>
		<td>1.0 × 10<sup>-3</sup></td>
		<td>1.0 × 10<sup>-4</sup></td>
	</tr>
	<tr>
		<td>3B</td>
		<td>1.0 × 10<sup>-3</sup></td>
		<td>1.0 × 10<sup>-3</sup></td>
	</tr>
	<tr>
		<td>4B</td>
		<td>1.0 × 10<sup>-3</sup></td>
		<td>1.0 × 10<sup>-2</sup></td>
	</tr>
	<tr>
		<td>5B</td>
		<td>1.0 × 10<sup>-3</sup></td>
		<td>1.0 × 10<sup>-1</sup></td>
	</tr>
	</tbody>
</table>

<p align="right">k and λ units in [s<sup>-1</sup>]</p>

***

## **PFLOTRAN Simulation**

<img src="./AtDetCol_media/plot/OnlyAttachment.png" alt="Column flow" width=800>

<img src="./AtDetCol_media/plot/VariableDetachment.png" alt="Column flow" width=800>

<p>&nbsp;</p>

_______

<a href="https://edsaac.github.io/bioparticle/listTests.html">
	<img alt="Back" src="https://img.shields.io/badge/&#11013;-Go back-purple?style=for-the-badge">
</a>

<p align="right">
    <img src="https://img.shields.io/badge/Works on-my machine-purple?style=for-the-badge">
    <img src="https://img.shields.io/badge/-&#127802;-purple?style=for-the-badge">
</p>
