# Breakthrough curves from a column experiment

## Description

1D saturated flow.

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
|Isoelectric point| *IEP*| ~3.5| - |
|Initial concentration| *C<sub>0</sub>*| 10<sup>5</sup>	| pfp/mL|
| | |1.7 × 10<sup>-16</sup>|mol/L|

***

## **Plug flow case**

|Parameter | | Value | Unit |
|---|---|--:|:--|
|Dispersion coef.| *α<sub>L</sub>* |0 |cm|
|Attachment rate| *k<sub>att</sub>* |0|1/s|
|Detachment rate| *k<sub>det</sub>* |0|1/s|
|Decay while in aqueous phase| *λ<sub>aq</sub>* |0|1/s|
|Decay while adsorbed to solid phase| *λ<sub>im</sub>* |0|1/s|
<p>&nbsp;</p>

**Results**

![plugFlow](./plugFlow/breakthrough.png)

***

## **With longitudinal dispersion**

|Parameter | | Value | Unit |
|---|---|--:|:--|
|Dispersion coef.| *α<sub>L</sub>* |0.2 |cm|
|Attachment rate| *k<sub>att</sub>* |0|1/s|
|Detachment rate| *k<sub>det</sub>* |0|1/s|
|Decay while in aqueous phase| *λ<sub>aq</sub>* |0|1/s|
|Decay while adsorbed to solid phase| *λ<sub>im</sub>* |0|1/s|
<p>&nbsp;</p>

**Results**

![plugFlow](./longitudinalDispersion/breakthrough.png)

***

## **Only attachment (sink)**
|Parameter | | Value | Unit |
|---|---|--:|:--|
|Dispersion coef.| *α<sub>L</sub>* |0.2 |cm|
|Attachment rate| *k<sub>att</sub>* |1.11 × 10<sup>-5</sup>|1/s|
|Detachment rate| *k<sub>det</sub>* |0|1/s|
|Decay while in aqueous phase| *λ<sub>aq</sub>* |0|1/s|
|Decay while adsorbed to solid phase| *λ<sub>im</sub>* |0|1/s|
<p>&nbsp;</p>

**Results**

![plugFlow](./onlyAttachment/breakthrough.png)

***

## **Attachment & detachment (source + sink)**
|Parameter | | Value | Unit |
|---|---|--:|:--|
|Dispersion coef.| *α<sub>L</sub>* |0 |cm|
|Attachment rate| *k<sub>att</sub>* |1.11 × 10<sup>-5</sup>|1/s|
|Detachment rate| *k<sub>det</sub>* |7.22 × 10<sup>-7</sup>|1/s|
|Decay while in aqueous phase| *λ<sub>aq</sub>* |0|1/s|
|Decay while adsorbed to solid phase| *λ<sub>im</sub>* |0|1/s|
<p>&nbsp;</p>

**Results**

![plugFlow](./attachDetachment/breakthrough.png)

***

## **Attachment, detachment & decay**
|Parameter | | Value | Unit |
|---|---|--:|:--|
|Dispersion coef.| *α<sub>L</sub>* |0 |cm|
|Attachment rate| *k<sub>att</sub>* |1.11 × 10<sup>-5</sup>0|1/s|
|Detachment rate| *k<sub>det</sub>* |7.22 × 10<sup>-7</sup>|1/s|
|Decay while in aqueous phase| *λ<sub>aq</sub>* |1.94 × 10<sup>-6</sup>|1/s|
|Decay while adsorbed to solid phase| *λ<sub>im</sub>* |9.72 × 10<sup>-6</sup>|1/s|
<p>&nbsp;</p>

**Results**

![plugFlow](./allProcesses/breakthrough.png)

_______

[![OS<3](https://badges.frapsoft.com/os/v1/open-source.png?v=103)]()