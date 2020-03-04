===========
S.30.04_107
===========

Rule definition
---------------

IF {S.30.04.01.02,c0180} <>" " AND {S.30.04.01.02,c0250} <> "NO RATING AVAILABLE" THEN  {S.30.04.01.02,c0230} <>" "


Template references
-------------------

S.30.04.01.02 Information on reinsurers


Datapoints labels
-----------------

S.30.04.01.02,c0180 [*natural key*|"mandatory"]

S.30.04.01.02,c0230 [external rating assessment by nominated ecai]

S.30.04.01.02,c0250 [credit quality step]



