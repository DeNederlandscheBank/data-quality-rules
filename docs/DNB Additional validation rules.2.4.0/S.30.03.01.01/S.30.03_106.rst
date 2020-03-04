===========
S.30.03_106
===========

Rule definition
---------------

IF {S.30.03.01.01,c0090} = "QUOTA SHARE" OR {S.30.03.01.01,c0090}="STOP LOSS" THEN {S.30.03.01.01,c0200} >= 0


Template references
-------------------

S.30.03.01.01 Outgoing Reinsurance Program basic data


Datapoints labels
-----------------

S.30.03.01.01,c0090 [type of reinsurance treaty]

S.30.03.01.01,c0200 [retention or priority (%)]



