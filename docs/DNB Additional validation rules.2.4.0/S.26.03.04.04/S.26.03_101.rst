===========
S.26.03_101
===========

Rule definition
---------------

IF ({S.26.03.04.04,r0100,c0060}>0 OR {S.26.03.04.04,r0100,c0080}>0) THEN ({S.26.03.04.03,r0010,c0010}="SIMPLIFICATIONS USED" OR {S.26.03.04.03,r0010,c0010}="SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.03.04.03
S.26.03.04.04

Datapoints
----------

S.26.03.04.03,r0010,c0010 [Simplifications - mortality risk , Simplifications used]

S.26.03.04.04,r0100,c0060 [Mortality risk , Absolute values after shock|Net solvency capital requirement]

S.26.03.04.04,r0100,c0080 [Mortality risk , Absolute values after shock|Gross solvency capital requirement]



