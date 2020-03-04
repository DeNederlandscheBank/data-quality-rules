===========
S.30.02_110
===========

Rule definition
---------------

IF {S.30.02.01.03,c0280} <> " " AND {S.30.02.01.03,c0350} <> "NO RATING AVAILABLE" THEN  {S.30.02.01.03,c0340} <>" "


Template references
-------------------

S.30.02.01.03 Reinsurer-specific information


Datapoints labels
-----------------

S.30.02.01.03,c0280 [*natural key*|"mandatory"]

S.30.02.01.03,c0340 [nominated ecai]

S.30.02.01.03,c0350 [credit quality step]



