===========
S.26.03_105
===========

Rule definition
---------------

IF ({S.26.03.04.04,r0300,c0060}>0 OR {S.26.03.04.04,r0300,c0080}>0) THEN ({S.26.03.04.03,r0030,c0010}="SIMPLIFICATIONS USED" OR {S.26.03.04.03,r0030,c0010}="SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.03.04.03 Simplifications used

S.26.03.04.04 Life underwriting risk


Datapoints labels
-----------------

S.26.03.04.03,r0030,c0010 [simplifications - disability-morbidity risk, simplifications used]

S.26.03.04.04,r0300,c0060 [disability-morbidity risk, net solvency capital requirement]

S.26.03.04.04,r0300,c0080 [disability-morbidity risk, gross solvency capital requirement]



