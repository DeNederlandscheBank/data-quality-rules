===========
S.32.01_105
===========

Rule definition
---------------

IF ({S.32.01.04.01,c0050}="LIFE UNDERTAKINGS" OR {S.32.01.04.01,c0050}="NON-LIFE UNDERTAKINGS" OR {S.32.01.04.01,c0050}="REINSURANCE UNDERTAKINGS" OR {S.32.01.04.01,c0050}="COMPOSITE INSURER") THEN SUM({S.32.01.04.01,c0090},0) <> 0


Template references
-------------------

S.32.01.04.01

Datapoints
----------

S.32.01.04.01,c0050 [Identification code of entity , Type of undertaking]

S.32.01.04.01,c0090 [Identification code of entity , Ranking criteria (in the group currency)|Total Balance Sheet (for (re)insurance undertakings)]



