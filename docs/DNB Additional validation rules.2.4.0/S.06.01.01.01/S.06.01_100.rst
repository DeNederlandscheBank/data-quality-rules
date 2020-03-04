===========
S.06.01_100
===========

Rule definition
---------------

IF {S.01.01.01.01,r0140,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35"  THEN {S.06.01.01.01,r0040,c0010} + {S.06.01.01.01,r0040,c0020} +{S.06.01.01.01,r0040,c0030} +{S.06.01.01.01,r0040,c0040} +  {S.06.01.01.01,r0040,c0050} + {S.06.01.01.01,r0040,c0060} = {S.02.01.01.01,r0140,c0010}


Template references
-------------------

S.01.01.01.01 Content of the submission

S.02.01.01.01 Balance sheet

S.06.01.01.01 Summary of assets


Datapoints labels
-----------------

S.01.01.01.01,r0140,c0010 [s.06.02.01 - list of assets, none]

S.02.01.01.01,r0140,c0010 [government bonds, solvency ii value]

S.06.01.01.01,r0040,c0010 [government bonds, life]

S.06.01.01.01,r0040,c0020 [government bonds, non-life]

S.06.01.01.01,r0040,c0030 [government bonds, ring-fenced funds]

S.06.01.01.01,r0040,c0040 [government bonds, other internal funds]

S.06.01.01.01,r0040,c0050 [government bonds, shareholders' funds]

S.06.01.01.01,r0040,c0060 [government bonds, general]



