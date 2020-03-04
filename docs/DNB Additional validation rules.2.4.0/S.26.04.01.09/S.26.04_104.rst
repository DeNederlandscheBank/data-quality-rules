===========
S.26.04_104
===========

Rule definition
---------------

IF ({S.26.04.01.01,r0500,c0060}>0 OR {S.26.04.01.01,r0500,c0080}>0) THEN ({S.26.04.01.09,r0060,c0010}="SIMPLIFICATIONS USED" OR {S.26.04.01.09,r0060,c0010}="SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.04.01.01 SLT health underwriting risk

S.26.04.01.09 Simplifications used


Datapoints labels
-----------------

S.26.04.01.01,r0500,c0060 [health expense risk, net solvency capital requirement]

S.26.04.01.01,r0500,c0080 [health expense risk, gross solvency capital requirement]

S.26.04.01.09,r0060,c0010 [simplifications - health expense risk, simplifications used]



