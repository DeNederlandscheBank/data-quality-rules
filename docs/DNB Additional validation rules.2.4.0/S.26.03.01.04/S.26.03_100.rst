===========
S.26.03_100
===========

Rule definition
---------------

IF ({S.26.03.01.04,r0100,c0060}>0 OR {S.26.03.01.04,r0100,c0080}>0) THEN ({S.26.03.01.03,r0010,c0010}="SIMPLIFICATIONS USED" OR {S.26.03.01.03,r0010,c0010}="SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.03.01.03 Simplifications used

S.26.03.01.04 Life underwriting risk


Datapoints labels
-----------------

S.26.03.01.03,r0010,c0010 [simplifications - mortality risk, simplifications used]

S.26.03.01.04,r0100,c0060 [mortality risk, net solvency capital requirement]

S.26.03.01.04,r0100,c0080 [mortality risk, gross solvency capital requirement]



