<link rel="shortcut icon" type="image/x-icon" href="../images/favicon.png">

# Breakthrough curves from a column experiment

<p align="right" style="font-size:10px;">
<a href="https://github.com/edsaac/bioparticle/tree/master/test/breakthroughCurves">
	<img src="https://img.shields.io/badge/Find me -in the repo-purple?style=for-the-badge&logo=github">
</a>
</p>

**What is a breakthrough curve?**<br>
It's a plot of concentration at some point over time

**What is a column experiment?**<br>
A fluid with some solute concentration is injected at one end of a cilyndrical soil sample and its concentration is registered at the other end. 

**More details at:** <br>
- Kirkham, M. B. (2014). Pore Volume. In Principles of Soil and Plant Water Relations (pp. 229–241). Elsevier. [![DOI:10.1016/B978-0-12-420022-7.00014-8](https://zenodo.org/badge/DOI/10.1016/B978-0-12-420022-7.00014-8.svg)](https://linkinghub.elsevier.com/retrieve/pii/B9780124200227000148)

<p>&nbsp;</p>

***

## Description
<p align="center">
	<img src="./btCol_media/gifs/descriptionProblem.png" alt="Breakthrough curve" height=400>
</p>

<p>
An injection of some bioparticle (e.g. a virus) concentration is set at the inlet of a column experiment. The bioparticle can either attach to the solid matrix, dettach and reenter the aqueous phase, and decay into another species. After some time, the bioparticle injection is stopped and only clean water keeps runing through the column. 
</p>

|Column parameters | | Value | Unit |
|---|---|--:|:--|
|Lenght| *L* |50|cm|
|Diameter| *Ø* | 5|cm|
|Darcy flow| *q* |2.05|cm/h|
|Porosity| *φ* |0.37|-|
|Grain size| *d<sub>50</sub>*|0.44|mm|

<p>&nbsp;</p>

|Particle parameters | | Value | Unit |
|---|---|--:|:--|
|Size | *d<sub>p</sub>*| 62 | nm |
|Isoelectric point| *IEP*| ~ 3.5| - |
|Initial concentration| *C<sub>0</sub>*| 1.66 × 10<sup>-16</sup>|mol/L|

<p>&nbsp;</p>

***

## **Plug flow case**

|Parameter | | Value | Unit |
|---|---|--:|:--|
|Long. dispersion coefficient| *α<sub>L</sub>* |0 |cm|
|Attachment rate| *k<sub>att</sub>* |0|1/s|
|Detachment rate| *k<sub>det</sub>* |0|1/s|
|Decay while in aqueous phase| *λ<sub>aq</sub>* |0|1/s|
|Decay while adsorbed to solid phase| *λ<sub>im</sub>* |0|1/s|

<p>&nbsp;</p>

**Results**

<p align="center">
	<img src="./btCol_media/plots/bt_plugFlow.png" alt="Breakthrough curve" width=500>
</p>

***

## **With longitudinal dispersion**

|Parameter | | Value | Unit |
|---|---|--:|:--|
|Long. dispersion coefficient| *α<sub>L</sub>* |0.2 |cm|
|Attachment rate| *k<sub>att</sub>* |0|1/s|
|Detachment rate| *k<sub>det</sub>* |0|1/s|
|Decay while in aqueous phase| *λ<sub>aq</sub>* |0|1/s|
|Decay while adsorbed to solid phase| *λ<sub>im</sub>* |0|1/s|

<p>&nbsp;</p>

**Results**

<p align="center">
	<img src="./btCol_media/plots/bt_longDispersion.png" alt="Breakthrough curve" width=500><img src="./btCol_media/gifs/onlyDispersion.gif" alt="Breakthrough curve" width=100>
</p>

***

## **Only attachment (sink)**

|Parameter | | Value | Unit |
|---|---|--:|:--|
|Long. dispersion coefficient| *α<sub>L</sub>* |0.2 |cm|
|Attachment rate| *k<sub>att</sub>* |1.11 × 10<sup>-5</sup>|1/s|
|Detachment rate| *k<sub>det</sub>* |0|1/s|
|Decay while in aqueous phase| *λ<sub>aq</sub>* |0|1/s|
|Decay while adsorbed to solid phase| *λ<sub>im</sub>* |0|1/s|

<p>&nbsp;</p>

**Results**

<p align="center">
	<img src="./btCol_media/plots/bt_onlyAttachment.png" alt="Breakthrough curve" width=500><img src="./btCol_media/gifs/onlyAttachment.gif" alt="Breakthrough curve" width=100>
</p>

***

## **Attachment & detachment (source + sink)**

|Parameter | | Value | Unit |
|---|---|--:|:--|
|Long. dispersion coefficient| *α<sub>L</sub>* |0.2 |cm|
|Attachment rate| *k<sub>att</sub>* |1.11 × 10<sup>-5</sup>|1/s|
|Detachment rate| *k<sub>det</sub>* |7.22 × 10<sup>-7</sup>|1/s|
|Decay while in aqueous phase| *λ<sub>aq</sub>* |0|1/s|
|Decay while adsorbed to solid phase| *λ<sub>im</sub>* |0|1/s|

<p>&nbsp;</p>

**Results**

<p align="center">
	<img src="./btCol_media/plots/bt_attachDetachment.png" alt="Breakthrough curve" width=400><img src="./btCol_media/gifs/attachDetachment.gif" alt="Breakthrough curve" width=200>
</p>

***

## **Attachment, detachment & decay**

|Parameter | | Value | Unit |
|---|---|--:|:--|
|Long. dispersion coefficient| *α<sub>L</sub>* |0.2 |cm|
|Attachment rate| *k<sub>att</sub>* |1.11 × 10<sup>-5</sup>|1/s|
|Detachment rate| *k<sub>det</sub>* |7.22 × 10<sup>-7</sup>|1/s|
|Decay while in aqueous phase| *λ<sub>aq</sub>* |1.94 × 10<sup>-6</sup>|1/s|
|Decay while adsorbed to solid phase| *λ<sub>im</sub>* |9.72 × 10<sup>-6</sup>|1/s|

<p>&nbsp;</p>

**Results**

<p align="center">
	<img src="./btCol_media/plots/bt_allProcesses.png" alt="Breakthrough curve" width=500>
</p>

_______

<a href="https://edsaac.github.io/bioparticle/listTests.html">
	<img alt="Back" src="https://img.shields.io/badge/&#11013;-Go back-purple?style=for-the-badge">
</a>

<p align="right">
    <img src="https://img.shields.io/badge/Works on-my machine-purple?style=for-the-badge">
    <img src="https://img.shields.io/badge/-&#127802;-purple?style=for-the-badge">
</p>
