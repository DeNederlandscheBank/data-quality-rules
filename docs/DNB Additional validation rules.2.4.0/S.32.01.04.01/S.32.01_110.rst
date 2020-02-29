===========
S.32.01_110
===========

Rule definition
---------------

IF {S.32.01.04.01,c0020} <> " " AND {S.32.01.04.01,c0020} <> {S.01.02.04.01,r0020,c0010} THEN SUM({S.32.01.04.01,c0230},0) <> 0


Template references
-------------------

S.01.02.04.01
S.32.01.04.01

Datapoints
----------

S.01.02.04.01,r0020,c0010 [nan]

S.32.01.04.01,c0020 [Y-axis (CE): Identification code of entity , Y-axis (CE): Identification code and type of code of the undertaking]

S.32.01.04.01,c0230 [Identification code of entity , Criteria of influence|Proportional share used for group solvency calculation]



