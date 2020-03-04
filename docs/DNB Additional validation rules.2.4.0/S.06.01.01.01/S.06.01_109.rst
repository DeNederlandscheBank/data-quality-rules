===========
S.06.01_109
===========

Rule definition
---------------

IF {S.01.01.04.01,r0140,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35" THEN {S.06.01.01.01,r0080,c0010} + {S.06.01.01.01,r0080,c0020} +{S.06.01.01.01,r0080,c0030} +{S.06.01.01.01,r0080,c0040} +  {S.06.01.01.01,r0080,c0050} + {S.06.01.01.01,r0080,c0060} = {S.02.01.01.01,r0180,c0010}


Template references
-------------------

S.01.01.04.01 Content of the submission

S.02.01.01.01 Balance sheet

S.06.01.01.01 Summary of assets


Datapoints labels
-----------------

S.01.01.04.01,r0140,c0010 [s.06.02.04 - list of assets, none]

S.02.01.01.01,r0180,c0010 [collective investments undertakings, solvency ii value]

S.06.01.01.01,r0080,c0010 [structured notes, life]

S.06.01.01.01,r0080,c0020 [structured notes, non-life]

S.06.01.01.01,r0080,c0030 [structured notes, ring-fenced funds]

S.06.01.01.01,r0080,c0040 [structured notes, other internal funds]

S.06.01.01.01,r0080,c0050 [structured notes, shareholders' funds]

S.06.01.01.01,r0080,c0060 [structured notes, general]



