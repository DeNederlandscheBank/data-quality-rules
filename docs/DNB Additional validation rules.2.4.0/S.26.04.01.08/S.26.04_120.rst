===========
S.26.04_120
===========

Rule definition
---------------

{S.26.04.01.08,r1700,c0270}=(({S.26.04.01.01,r0800,c0080}**2)+({S.26.04.01.06,r1400,c0240}**2)+({S.26.04.01.07,r1540,c0260}**2)+({S.26.04.01.01,r0800,c0080}*{S.26.04.01.06,r1400,c0240})+(0.5*{S.26.04.01.01,r0800,c0080}*{S.26.04.01.07,r1540,c0260})+(0.5*{S.26.04.01.06,r1400,c0240}*{S.26.04.01.07,r1540,c0260}))**0.5


Template references
-------------------

S.26.04.01.01 SLT health underwriting risk

S.26.04.01.06 Total NSLT health underwriting risk

S.26.04.01.07 Health catastrophe risk - basic information

S.26.04.01.08 Total health underwriting risk


Datapoints labels
-----------------

S.26.04.01.01,r0800,c0080 [total slt health underwriting risk, gross solvency capital requirement]

S.26.04.01.06,r1400,c0240 [total nslt health underwriting risk, solvency capital requirement]

S.26.04.01.07,r1540,c0260 [total health catastrophe risk, gross solvency capital requirement]

S.26.04.01.08,r1700,c0270 [total health underwriting risk, net solvency capital requirement]



