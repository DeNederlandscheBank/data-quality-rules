===========
S.06.01_110
===========

Rule definition
---------------

IF {S.01.01.01.01,r0140,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35" THEN {S.06.01.01.01,r0090,c0010} + {S.06.01.01.01,r0090,c0020} +{S.06.01.01.01,r0090,c0030} +{S.06.01.01.01,r0090,c0040} +  {S.06.01.01.01,r0090,c0050} + {S.06.01.01.01,r0090,c0060} = {S.02.01.01.01,r0180,c0010}


Template references
-------------------

S.01.01.01.01 Content of the submission

S.02.01.01.01 Balance sheet

S.06.01.01.01 Summary of assets


Datapoints labels
-----------------

S.01.01.01.01,r0140,c0010 [s.06.02.01 - list of assets, none]

S.02.01.01.01,r0180,c0010 [collective investments undertakings, solvency ii value]

S.06.01.01.01,r0090,c0010 [collateralised securities, life]

S.06.01.01.01,r0090,c0020 [collateralised securities, non-life]

S.06.01.01.01,r0090,c0030 [collateralised securities, ring-fenced funds]

S.06.01.01.01,r0090,c0040 [collateralised securities, other internal funds]

S.06.01.01.01,r0090,c0050 [collateralised securities, shareholders' funds]

S.06.01.01.01,r0090,c0060 [collateralised securities, general]



