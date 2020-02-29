===========
S.26.04_116
===========

Rule definition
---------------

IF {S.26.04.01.06,r1400,c0240} <> 0 THEN {S.26.04.01.06,r1400,c0240} = (({S.26.04.01.04,r1100,c0180}**2) + ({S.26.04.01.05,r1200,c0230}**2))**0.5


Template references
-------------------

S.26.04.01.04 Total NSLT health premium and reserve risk

S.26.04.01.05 NSLT health lapse risk

S.26.04.01.06 Total NSLT health underwriting risk


Datapoints
----------

S.26.04.01.04,r1100,c0180 [Total NSLT health premium and reserve risk , Solvency capital requirement]

S.26.04.01.05,r1200,c0230 [NSLT health lapse risk , Absolute values after shock|Solvency capital requirement]

S.26.04.01.06,r1400,c0240 [Total NSLT health underwriting risk , Solvency capital requirement]



