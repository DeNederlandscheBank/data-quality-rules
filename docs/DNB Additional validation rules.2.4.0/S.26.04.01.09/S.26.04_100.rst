===========
S.26.04_100
===========

Rule definition
---------------

IF ({S.26.04.01.01,r0100,c0060} > 0 OR {S.26.04.01.01,r0100,c0080} > 0) THEN ({S.26.04.01.09,r0010,c0010} = "SIMPLIFICATIONS USED" OR {S.26.04.01.09,r0010,c0010} = "SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.04.01.01 SLT health underwriting risk

S.26.04.01.09 Simplifications used


Datapoints
----------

S.26.04.01.01,r0100,c0060 [Health mortality risk , Absolute values after shock|Net solvency capital requirement]

S.26.04.01.01,r0100,c0080 [Health mortality risk , Absolute values after shock|Gross solvency capital requirement]

S.26.04.01.09,r0010,c0010 [Simplifications - health mortality risk , Simplifications used]



