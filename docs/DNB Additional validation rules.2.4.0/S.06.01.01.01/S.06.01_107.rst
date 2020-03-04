===========
S.06.01_107
===========

Rule definition
---------------

IF {S.01.01.04.01,r0140,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35"  THEN {S.06.01.01.01,r0070,c0010} + {S.06.01.01.01,r0070,c0020} +{S.06.01.01.01,r0070,c0030} +{S.06.01.01.01,r0070,c0040} +  {S.06.01.01.01,r0070,c0050} + {S.06.01.01.01,r0070,c0060} = {S.02.01.01.01,r0180,c0010}


Template references
-------------------

S.01.01.04.01 Content of the submission

S.02.01.01.01 Balance sheet

S.06.01.01.01 Summary of assets


Datapoints labels
-----------------

S.01.01.04.01,r0140,c0010 [s.06.02.04 - list of assets, none]

S.02.01.01.01,r0180,c0010 [collective investments undertakings, solvency ii value]

S.06.01.01.01,r0070,c0010 [collective investment undertakings, life]

S.06.01.01.01,r0070,c0020 [collective investment undertakings, non-life]

S.06.01.01.01,r0070,c0030 [collective investment undertakings, ring-fenced funds]

S.06.01.01.01,r0070,c0040 [collective investment undertakings, other internal funds]

S.06.01.01.01,r0070,c0050 [collective investment undertakings, shareholders' funds]

S.06.01.01.01,r0070,c0060 [collective investment undertakings, general]



