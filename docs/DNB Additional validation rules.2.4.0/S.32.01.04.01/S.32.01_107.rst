===========
S.32.01_107
===========

Rule definition
---------------

IF {S.32.01.04.01,c0020} <> " " AND ({S.32.01.04.01,c0050}="LIFE UNDERTAKINGS" AND {S.32.01.04.01,c0050}="NON-LIFE UNDERTAKINGS" AND {S.32.01.04.01,c0050}="REINSURANCE UNDERTAKINGS" AND {S.32.01.04.01,c0050}="COMPOSITE INSURER") THEN {S.32.01.04.01,c0120} <> 0


Template references
-------------------

S.32.01.04.01

Datapoints
----------

S.32.01.04.01,c0020 [Y-axis (CE): Identification code of entity , Y-axis (CE): Identification code and type of code of the undertaking]

S.32.01.04.01,c0050 [Identification code of entity , Type of undertaking]

S.32.01.04.01,c0120 [Identification code of entity , Ranking criteria (in the group currency)|Written premiums net of reinsurance ceded under IFRS or local GAAP for (re)insurance undertakings]



