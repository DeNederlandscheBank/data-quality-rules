===========
S.26.04_101
===========

Rule definition
---------------

IF ({S.26.04.04.01,r0100,c0060} > 0 OR {S.26.04.04.01,r0100,c0080} > 0) THEN ({S.26.04.04.09,r0010,c0010} = "SIMPLIFICATIONS USED" OR {S.26.04.04.09,r0010,c0010} = "SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.04.04.01 SLT health underwriting risk

S.26.04.04.09 Simplifications used


Datapoints labels
-----------------

S.26.04.04.01,r0100,c0060 [health mortality risk, net solvency capital requirement]

S.26.04.04.01,r0100,c0080 [health mortality risk, gross solvency capital requirement]

S.26.04.04.09,r0010,c0010 [simplifications - health mortality risk, simplifications used]



