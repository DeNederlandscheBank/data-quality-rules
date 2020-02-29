===========
S.31.01_111
===========

Rule definition
---------------

IF {S.31.01.01.02,c0160} <> " " AND {S.31.01.01.02,c0230} <> "NO RATING AVAILABLE" THEN {S.31.01.01.02,c0210} <> " "


Template references
-------------------

S.31.01.01.02 Information on reinsurers


Datapoints
----------

S.31.01.01.02,c0160 [Y-axis (RF): Code reinsurer , Y-axis (RF): Code and type of code of the reinsurer]

S.31.01.01.02,c0210 [Code reinsurer , External rating assessment by nominated ECAI]

S.31.01.01.02,c0230 [Code reinsurer , Credit quality step]



