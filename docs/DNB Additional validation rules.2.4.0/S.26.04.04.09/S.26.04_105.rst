===========
S.26.04_105
===========

Rule definition
---------------

IF ({S.26.04.04.01,r0500,c0060} > 0 OR {S.26.04.04.01,r0500,c0080} > 0) THEN ({S.26.04.04.09,r0060,c0010} = "SIMPLIFICATIONS USED" OR {S.26.04.04.09,r0060,c0010} = "SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.04.04.01
S.26.04.04.09

Datapoints
----------

S.26.04.04.01,r0500,c0060 [Health expense risk , Absolute values after shock|Net solvency capital requirement]

S.26.04.04.01,r0500,c0080 [Health expense risk , Absolute values after shock|Gross solvency capital requirement]

S.26.04.04.09,r0060,c0010 [Simplifications - health expense risk , Simplifications used]



