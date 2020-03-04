===========
S.06.01_104
===========

Rule definition
---------------

IF {S.01.01.01.01,r0140,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35"  THEN {S.06.01.01.01,r0060,c0010} + {S.06.01.01.01,r0060,c0020} +{S.06.01.01.01,r0060,c0030} +{S.06.01.01.01,r0060,c0040} +  {S.06.01.01.01,r0060,c0050} + {S.06.01.01.01,r0060,c0060} = {S.02.01.01.01,r0100,c0010}


Template references
-------------------

S.01.01.01.01 Content of the submission

S.02.01.01.01 Balance sheet

S.06.01.01.01 Summary of assets


Datapoints labels
-----------------

S.01.01.01.01,r0140,c0010 [s.06.02.01 - list of assets, none]

S.02.01.01.01,r0100,c0010 [equities, solvency ii value]

S.06.01.01.01,r0060,c0010 [equity, life]

S.06.01.01.01,r0060,c0020 [equity, non-life]

S.06.01.01.01,r0060,c0030 [equity, ring-fenced funds]

S.06.01.01.01,r0060,c0040 [equity, other internal funds]

S.06.01.01.01,r0060,c0050 [equity, shareholders' funds]

S.06.01.01.01,r0060,c0060 [equity, general]



