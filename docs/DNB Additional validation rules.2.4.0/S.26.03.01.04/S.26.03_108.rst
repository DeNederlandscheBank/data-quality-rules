===========
S.26.03_108
===========

Rule definition
---------------

IF ({S.26.03.01.04,r0500,c0060}>0 OR {S.26.03.01.04,r0500,c0080}>0) THEN ({S.26.03.01.03,r0050,c0010}="SIMPLIFICATIONS USED" OR {S.26.03.01.03,r0050,c0010}="SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.03.01.03 Simplifications used

S.26.03.01.04 Life underwriting risk


Datapoints
----------

S.26.03.01.03,r0050,c0010 [Simplifications - life expense risk , Simplifications used]

S.26.03.01.04,r0500,c0060 [Life expense risk , Absolute values after shock|Net solvency capital requirement]

S.26.03.01.04,r0500,c0080 [Life expense risk , Absolute values after shock|Gross solvency capital requirement]



