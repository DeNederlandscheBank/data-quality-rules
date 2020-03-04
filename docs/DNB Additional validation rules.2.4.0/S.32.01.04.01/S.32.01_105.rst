===========
S.32.01_105
===========

Rule definition
---------------

IF ({S.32.01.04.01,c0050}="LIFE UNDERTAKINGS" OR {S.32.01.04.01,c0050}="NON-LIFE UNDERTAKINGS" OR {S.32.01.04.01,c0050}="REINSURANCE UNDERTAKINGS" OR {S.32.01.04.01,c0050}="COMPOSITE INSURER") THEN SUM({S.32.01.04.01,c0090},0) <> 0


Template references
-------------------

S.32.01.04.01 Undertakings in the scope of the group


Datapoints labels
-----------------

S.32.01.04.01,c0050 [type of undertaking]

S.32.01.04.01,c0090 [total balance sheet (for (re)insurance undertakings)]



