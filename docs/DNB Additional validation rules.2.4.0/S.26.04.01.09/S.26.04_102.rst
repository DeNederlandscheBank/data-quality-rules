===========
S.26.04_102
===========

Rule definition
---------------

IF ({S.26.04.01.01,r0400,c0060} > 0 OR {S.26.04.01.01,r0400,c0080} > 0) THEN ({S.26.04.01.09,r0050,c0010} = "SIMPLIFICATIONS USED" OR {S.26.04.01.09,r0050,c0010} = "SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.04.01.01 SLT health underwriting risk

S.26.04.01.09 Simplifications used


Datapoints
----------

S.26.04.01.01,r0400,c0060 [SLT health lapse risk , Absolute values after shock|Net solvency capital requirement]

S.26.04.01.01,r0400,c0080 [SLT health lapse risk , Absolute values after shock|Gross solvency capital requirement]

S.26.04.01.09,r0050,c0010 [Simplifications - SLT lapse risk , Simplifications used]



