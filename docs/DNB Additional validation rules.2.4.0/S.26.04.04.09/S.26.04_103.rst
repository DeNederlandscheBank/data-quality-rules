===========
S.26.04_103
===========

Rule definition
---------------

IF ({S.26.04.04.01,r0400,c0060} > 0 OR {S.26.04.04.01,r0400,c0080} > 0) THEN ({S.26.04.04.09,r0050,c0010} = "SIMPLIFICATIONS USED" OR {S.26.04.04.09,r0050,c0010} = "SIMPLIFICATIONS NOT USED")


Template references
-------------------

S.26.04.04.01 SLT health underwriting risk

S.26.04.04.09 Simplifications used


Datapoints labels
-----------------

S.26.04.04.01,r0400,c0060 [slt health lapse risk, net solvency capital requirement]

S.26.04.04.01,r0400,c0080 [slt health lapse risk, gross solvency capital requirement]

S.26.04.04.09,r0050,c0010 [simplifications - slt lapse risk, simplifications used]



