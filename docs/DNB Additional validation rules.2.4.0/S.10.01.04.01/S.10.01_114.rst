===========
S.10.01_114
===========

Rule definition
---------------

IF({S.10.01.04.01,C0120} = "BUYER IN A REPO" OR {S.10.01.04.01,C0120} = "SELLER IN A REPO") THEN {S.10.01.04.01,c0140} <> 0


Template references
-------------------

S.10.01.04.01

Datapoints
----------

S.10.01.04.01,C0120 [unknown label]
S.10.01.04.01,c0140 [Identification code of entity|Number of fund|S.10.01.zz.01 line identification , Far leg amount]



