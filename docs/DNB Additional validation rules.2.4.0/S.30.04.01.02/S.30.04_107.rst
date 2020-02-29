===========
S.30.04_107
===========

Rule definition
---------------

IF {S.30.04.01.02,c0180} <>" " AND {S.30.04.01.02,c0250} <> "NO RATING AVAILABLE" THEN  {S.30.04.01.02,c0230} <>" "


Template references
-------------------

S.30.04.01.02 Information on reinsurers


Datapoints
----------

S.30.04.01.02,c0180 [Y-axis (RF): Code reinsurer , Y-axis (RF): Code and type of code of the reinsurer]

S.30.04.01.02,c0230 [Code reinsurer , External rating assessment by nominated ECAI]

S.30.04.01.02,c0250 [Code reinsurer , Credit quality step]



