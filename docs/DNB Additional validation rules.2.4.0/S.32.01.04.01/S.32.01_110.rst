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

Datapoints labels
-----------------

S.01.02.04.01,r0020,c0010 [unknown label]
S.32.01.04.01,c0020 [unknown label]
S.32.01.04.01,c0230 [unknown label]


