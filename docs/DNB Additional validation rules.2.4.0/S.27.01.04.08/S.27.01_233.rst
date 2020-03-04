===========
S.27.01_233
===========

Rule definition
---------------

IF {S.27.01.04.08,r2100,c0540}<>0 THEN {S.27.01.04.08,r2100,c0540}=MAX(6000000, 50000*({S.27.01.04.08,r2100,c0520}+0.05*{S.27.01.04.08,r2100,c0530}+0.95*MIN({S.27.01.04.08,r2100,c0530}, 20000))**0.5)


Template references
-------------------

S.27.01.04.08 Man made catastrophe risk - Motor Vehicle Liability


Datapoints labels
-----------------

S.27.01.04.08,r2100,c0520 [motor vehicle liability, number of vehicles policy limit above 24m€]

S.27.01.04.08,r2100,c0530 [motor vehicle liability, number of vehicles policy limit below or equal to 24m€]

S.27.01.04.08,r2100,c0540 [motor vehicle liability, catastrophe risk charge motor vehicle liability before risk mitigation]



