===========
S.01.01_114
===========

Rule definition
---------------

IF {S.02.01.01.01,r0160,c0010} > 0.05*({S.02.01.01.01,r0070,c0010}+{S.02.01.01.01,r0220,c0010}) THEN {S.01.01.01.01,r0160,c0010} = "REPORTED"


Template references
-------------------

S.01.01.01.01 Content of the submission

S.02.01.01.01 Balance sheet


Datapoints labels
-----------------

S.01.01.01.01,r0160,c0010 [s.07.01.01 - structured products, none]

S.02.01.01.01,r0070,c0010 [investments (other than assets held for index-linked and unit-linked contracts), solvency ii value]

S.02.01.01.01,r0160,c0010 [structured notes, solvency ii value]

S.02.01.01.01,r0220,c0010 [assets held for index-linked and unit-linked contracts, solvency ii value]



