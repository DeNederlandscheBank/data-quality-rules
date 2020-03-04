===========
S.31.01_111
===========

Rule definition
---------------

IF {S.31.01.01.02,c0160} <> " " AND {S.31.01.01.02,c0230} <> "NO RATING AVAILABLE" THEN {S.31.01.01.02,c0210} <> " "


Template references
-------------------

S.31.01.01.02 Information on reinsurers


Datapoints labels
-----------------

S.31.01.01.02,c0160 [*natural key*|"mandatory"]

S.31.01.01.02,c0210 [external rating assessment by nominated ecai]

S.31.01.01.02,c0230 [credit quality step]



