===========
S.32.01_106
===========

Rule definition
---------------

IF {S.32.01.04.01,c0020} <> " " AND ({S.32.01.04.01,c0050}<>"LIFE UNDERTAKINGS" AND {S.32.01.04.01,c0050}<>"NON-LIFE UNDERTAKINGS" AND {S.32.01.04.01,c0050}<>"REINSURANCE UNDERTAKINGS" AND {S.32.01.04.01,c0050}<>"COMPOSITE INSURER") THEN SUM(({S.32.01.04.01,c0100} + {S.32.01.04.01,c0110}),0) <> 0 


Template references
-------------------

S.32.01.04.01 Undertakings in the scope of the group


Datapoints labels
-----------------

S.32.01.04.01,c0020 [*natural key*|"mandatory"]

S.32.01.04.01,c0050 [type of undertaking]

S.32.01.04.01,c0100 [total balance sheet (for other regulated undertakings)]

S.32.01.04.01,c0110 [total balance sheet (non-regulated undertakings)]



