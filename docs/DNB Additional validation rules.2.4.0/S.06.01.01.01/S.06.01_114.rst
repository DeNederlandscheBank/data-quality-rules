===========
S.06.01_114
===========

Rule definition
---------------

IF {S.01.01.01.01,r0140,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35"  THEN {S.06.01.01.01,r0110,c0010} + {S.06.01.01.01,r0110,c0020} +{S.06.01.01.01,r0110,c0030} +{S.06.01.01.01,r0110,c0040} +  {S.06.01.01.01,r0110,c0050} + {S.06.01.01.01,r0110,c0060} = {S.02.01.01.01,r0230,c0010}


Template references
-------------------

S.01.01.01.01 Content of the submission

S.02.01.01.01 Balance sheet

S.06.01.01.01 Summary of assets


Datapoints labels
-----------------

S.01.01.01.01,r0140,c0010 [s.06.02.01 - list of assets, none]

S.02.01.01.01,r0230,c0010 [loans and mortgages, solvency ii value]

S.06.01.01.01,r0110,c0010 [mortgages and loans, life]

S.06.01.01.01,r0110,c0020 [mortgages and loans, non-life]

S.06.01.01.01,r0110,c0030 [mortgages and loans, ring-fenced funds]

S.06.01.01.01,r0110,c0040 [mortgages and loans, other internal funds]

S.06.01.01.01,r0110,c0050 [mortgages and loans, shareholders' funds]

S.06.01.01.01,r0110,c0060 [mortgages and loans, general]



