===========
S.26.03_110
===========

Rule definition
---------------

IF ({S.26.03.01.04,r0700,c0060}>0 OR {S.26.03.01.04,r0700,c0080}>0) THEN ({S.26.03.01.03,r0060,c0010}="SIMPLIFICATIONS USED" OR {S.26.03.01.03,r0060,c0010}="SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.03.01.03 Simplifications used

S.26.03.01.04 Life underwriting risk


Datapoints labels
-----------------

S.26.03.01.03,r0060,c0010 [simplifications - life catastrophe risk, simplifications used]

S.26.03.01.04,r0700,c0060 [life catastrophe risk, net solvency capital requirement]

S.26.03.01.04,r0700,c0080 [life catastrophe risk, gross solvency capital requirement]



