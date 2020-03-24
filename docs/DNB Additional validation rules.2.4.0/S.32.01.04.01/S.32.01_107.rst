===========
S.32.01_107
===========

Rule definition
---------------

IF {S.32.01.04.01,c0020} <> " " AND ({S.32.01.04.01,c0050}="LIFE UNDERTAKINGS" AND {S.32.01.04.01,c0050}="NON-LIFE UNDERTAKINGS" AND {S.32.01.04.01,c0050}="REINSURANCE UNDERTAKINGS" AND {S.32.01.04.01,c0050}="COMPOSITE INSURER") THEN {S.32.01.04.01,c0120} <> 0


Template references
-------------------

S.32.01.04.01

Datapoints labels
-----------------

S.32.01.04.01,c0020 [unknown label]
S.32.01.04.01,c0050 [unknown label]
S.32.01.04.01,c0120 [unknown label]


