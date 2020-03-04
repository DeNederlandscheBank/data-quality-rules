===========
S.32.01_110
===========

Rule definition
---------------

IF {S.32.01.04.01,c0020} <> " " AND {S.32.01.04.01,c0020} <> {S.01.02.04.01,r0020,c0010} THEN SUM({S.32.01.04.01,c0230},0) <> 0


Template references
-------------------

S.01.02.04.01 Basic Information - General

S.32.01.04.01 Undertakings in the scope of the group


Datapoints labels
-----------------

S.01.02.04.01,r0020,c0010 [group identification code and type of code, none]

S.32.01.04.01,c0020 [*natural key*|"mandatory"]

S.32.01.04.01,c0230 [proportional share used for group solvency calculation]



