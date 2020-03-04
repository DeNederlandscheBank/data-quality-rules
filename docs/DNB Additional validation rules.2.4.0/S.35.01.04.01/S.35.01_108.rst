===========
S.35.01_108
===========

Rule definition
---------------

IF {S.35.01.04.01,c0020}<>" " AND {S.35.01.04.01,c0040}<>"DEDUCTION AND AGGREGATION METHOD [METHOD 2]" THEN ({S.35.01.04.01,c0070} + {S.35.01.04.01,c0100} + {S.35.01.04.01,c0130} + {S.35.01.04.01,c0160} + {S.35.01.04.01,c0190} <> 0)


Template references
-------------------

S.35.01.04.01 Contribution to group Technical Provisions


Datapoints labels
-----------------

S.35.01.04.01,c0020 [*natural key*|"mandatory"]

S.35.01.04.01,c0040 [method of group solvency calculation used]

S.35.01.04.01,c0070 [amount of tp gross of igt]

S.35.01.04.01,c0100 [amount of tp gross of igt]

S.35.01.04.01,c0130 [amount of tp gross of igt]

S.35.01.04.01,c0160 [amount of tp gross of igt]

S.35.01.04.01,c0190 [amount of tp gross of igt]



