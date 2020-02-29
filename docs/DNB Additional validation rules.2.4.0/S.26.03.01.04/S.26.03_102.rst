===========
S.26.03_102
===========

Rule definition
---------------

IF ({S.26.03.01.04,r0200,c0060}>0 OR {S.26.03.01.04,r0200,c0080}>0)THEN ({S.26.03.01.03,r0020,c0010}="SIMPLIFICATIONS USED" OR {S.26.03.01.03,r0020,c0010}="SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.03.01.03 Simplifications used

S.26.03.01.04 Life underwriting risk


Datapoints
----------

S.26.03.01.03,r0020,c0010 [Simplifications - longevity risk , Simplifications used]

S.26.03.01.04,r0200,c0060 [Longevity risk , Absolute values after shock|Net solvency capital requirement]

S.26.03.01.04,r0200,c0080 [Longevity risk , Absolute values after shock|Gross solvency capital requirement]



