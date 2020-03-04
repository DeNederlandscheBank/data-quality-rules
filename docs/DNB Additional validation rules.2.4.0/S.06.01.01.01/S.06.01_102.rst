===========
S.06.01_102
===========

Rule definition
---------------

IF {S.01.01.01.01,r0140,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35"  THEN {S.06.01.01.01,r0050,c0010} + {S.06.01.01.01,r0050,c0020} +{S.06.01.01.01,r0050,c0030} +{S.06.01.01.01,r0050,c0040} +  {S.06.01.01.01,r0050,c0050} + {S.06.01.01.01,r0050,c0060} = {S.02.01.01.01,r0150,c0010}


Template references
-------------------

S.01.01.01.01 Content of the submission

S.02.01.01.01 Balance sheet

S.06.01.01.01 Summary of assets


Datapoints labels
-----------------

S.01.01.01.01,r0140,c0010 [s.06.02.01 - list of assets, none]

S.02.01.01.01,r0150,c0010 [corporate bonds, solvency ii value]

S.06.01.01.01,r0050,c0010 [corporate bonds, life]

S.06.01.01.01,r0050,c0020 [corporate bonds, non-life]

S.06.01.01.01,r0050,c0030 [corporate bonds, ring-fenced funds]

S.06.01.01.01,r0050,c0040 [corporate bonds, other internal funds]

S.06.01.01.01,r0050,c0050 [corporate bonds, shareholders' funds]

S.06.01.01.01,r0050,c0060 [corporate bonds, general]



