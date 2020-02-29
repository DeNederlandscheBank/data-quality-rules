===========
S.32.01_106
===========

Rule definition
---------------

IF {S.32.01.04.01,c0020} <> " " AND ({S.32.01.04.01,c0050}<>"LIFE UNDERTAKINGS" AND {S.32.01.04.01,c0050}<>"NON-LIFE UNDERTAKINGS" AND {S.32.01.04.01,c0050}<>"REINSURANCE UNDERTAKINGS" AND {S.32.01.04.01,c0050}<>"COMPOSITE INSURER") THEN SUM(({S.32.01.04.01,c0100} + {S.32.01.04.01,c0110}),0) <> 0 


Template references
-------------------

S.32.01.04.01

Datapoints
----------

S.32.01.04.01,c0020 [Y-axis (CE): Identification code of entity , Y-axis (CE): Identification code and type of code of the undertaking]

S.32.01.04.01,c0050 [Identification code of entity , Type of undertaking]

S.32.01.04.01,c0100 [Identification code of entity , Ranking criteria (in the group currency)|Total Balance Sheet (for other regulated undertakings)]

S.32.01.04.01,c0110 [Identification code of entity , Ranking criteria (in the group currency)|Total Balance Sheet (non-regulated undertakings)]



