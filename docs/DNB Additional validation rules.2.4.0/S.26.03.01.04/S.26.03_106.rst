===========
S.26.03_106
===========

Rule definition
---------------

IF ({S.26.03.01.04,r0400,c0060}>0 OR {S.26.03.01.04,r0400,c0080}>0) THEN ({S.26.03.01.03,r0040,c0010}="SIMPLIFICATIONS USED" OR {S.26.03.01.03,r0040,c0010}="SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.03.01.03 Simplifications used

S.26.03.01.04 Life underwriting risk


Datapoints
----------

S.26.03.01.03,r0040,c0010 [Simplifications - lapse risk , Simplifications used]

S.26.03.01.04,r0400,c0060 [Lapse risk , Absolute values after shock|Net solvency capital requirement]

S.26.03.01.04,r0400,c0080 [Lapse risk , Absolute values after shock|Gross solvency capital requirement]



