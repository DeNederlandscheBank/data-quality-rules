===========
S.32.01_107
===========

Rule definition
---------------

IF {S.32.01.04.01,c0020} <> " " AND ({S.32.01.04.01,c0050}="LIFE UNDERTAKINGS" AND {S.32.01.04.01,c0050}="NON-LIFE UNDERTAKINGS" AND {S.32.01.04.01,c0050}="REINSURANCE UNDERTAKINGS" AND {S.32.01.04.01,c0050}="COMPOSITE INSURER") THEN {S.32.01.04.01,c0120} <> 0


Template references
-------------------

S.32.01.04.01 Undertakings in the scope of the group


Datapoints labels
-----------------

S.32.01.04.01,c0020 [*natural key*|"mandatory"]

S.32.01.04.01,c0050 [type of undertaking]

S.32.01.04.01,c0120 [written premiums net of reinsurance ceded under ifrs or local gaap for (re)insurance undertakings]



