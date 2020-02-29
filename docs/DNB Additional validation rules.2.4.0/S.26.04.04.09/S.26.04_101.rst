===========
S.26.04_101
===========

Rule definition
---------------

IF ({S.26.04.04.01,r0100,c0060} > 0 OR {S.26.04.04.01,r0100,c0080} > 0) THEN ({S.26.04.04.09,r0010,c0010} = "SIMPLIFICATIONS USED" OR {S.26.04.04.09,r0010,c0010} = "SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.04.04.01
S.26.04.04.09

Datapoints
----------

S.26.04.04.01,r0100,c0060 [Health mortality risk , Absolute values after shock|Net solvency capital requirement]

S.26.04.04.01,r0100,c0080 [Health mortality risk , Absolute values after shock|Gross solvency capital requirement]

S.26.04.04.09,r0010,c0010 [Simplifications - health mortality risk , Simplifications used]



