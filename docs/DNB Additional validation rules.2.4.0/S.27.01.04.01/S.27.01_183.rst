===========
S.27.01_183
===========

Rule definition
---------------

IF {S.27.01.04.01,r0210,c0010} < >0 THEN {S.27.01.04.01,r0210,c0010} = (({S.27.01.04.01,r0010,c0010}+{S.27.01.04.01,r0060,c0010})**2+{S.27.01.04.01,r0090,c0010}**2+{S.27.01.04.01,r0170,c0010}**2)**0.5


Template references
-------------------

S.27.01.04.01 Non-life and Health catastrophe risk - Summary


Datapoints labels
-----------------

S.27.01.04.01,r0010,c0010 [natural catastrophe risk, scr before risk mitigation]

S.27.01.04.01,r0060,c0010 [subsidence, scr before risk mitigation]

S.27.01.04.01,r0090,c0010 [man-made catastrophe risk, scr before risk mitigation]

S.27.01.04.01,r0170,c0010 [other non-life catastrophe risk, scr before risk mitigation]

S.27.01.04.01,r0210,c0010 [total non-life catastrophe risk after diversification, scr before risk mitigation]



