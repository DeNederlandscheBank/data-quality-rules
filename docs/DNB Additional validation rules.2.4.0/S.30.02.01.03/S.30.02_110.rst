===========
S.30.02_110
===========

Rule definition
---------------

IF {S.30.02.01.03,c0280} <> " " AND {S.30.02.01.03,c0350} <> "NO RATING AVAILABLE" THEN  {S.30.02.01.03,c0340} <>" "


Template references
-------------------

S.30.02.01.03 Reinsurer-specific information


Datapoints
----------

S.30.02.01.03,c0280 [Y-axis (RF): Code reinsurer , Y-axis (RF): Code and type of code of the reinsurer]

S.30.02.01.03,c0340 [Code reinsurer , Nominated ECAI]

S.30.02.01.03,c0350 [Code reinsurer , Credit quality step]



