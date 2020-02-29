===========
S.27.01_232
===========

Rule definition
---------------

IF {S.27.01.01.08,r2100,c0540}<>0 THEN {S.27.01.01.08,r2100,c0540}=MAX(6000000, 50000*({S.27.01.01.08,r2100,c0520}+0.05*{S.27.01.01.08,r2100,c0530}+0.95*MIN({S.27.01.01.08,r2100,c0530}, 20000))**0.5)


Template references
-------------------

S.27.01.01.08 Man made catastrophe risk - Motor Vehicle Liability


Datapoints
----------

S.27.01.01.08,r2100,c0520 [Motor Vehicle Liability , Man made catastrophe risk - Motor Vehicle Liability|Number of vehicles policy limit above 24MÃ¢ÂÂ¬]

S.27.01.01.08,r2100,c0530 [Motor Vehicle Liability , Man made catastrophe risk - Motor Vehicle Liability|Number of vehicles policy limit below or equal to 24MÃ¢ÂÂ¬]

S.27.01.01.08,r2100,c0540 [Motor Vehicle Liability , Man made catastrophe risk - Motor Vehicle Liability|Catastrophe Risk Charge Motor Vehicle Liability before risk mitigation]



