===========
S.35.01_108
===========

Rule definition
---------------

IF {S.35.01.04.01,c0020}<>" " AND {S.35.01.04.01,c0040}<>"DEDUCTION AND AGGREGATION METHOD [METHOD 2]" THEN ({S.35.01.04.01,c0070} + {S.35.01.04.01,c0100} + {S.35.01.04.01,c0130} + {S.35.01.04.01,c0160} + {S.35.01.04.01,c0190} <> 0)


Template references
-------------------

S.35.01.04.01

Datapoints
----------

S.35.01.04.01,c0020 [Y-axis (CE): Identification code of entity , Y-axis (CE): Identification code and type of code of the undertaking]

S.35.01.04.01,c0040 [Identification code of entity , Method of group solvency calculation used]

S.35.01.04.01,c0070 [Identification code of entity , Technical Provisions - Non-Life (excluding Health)|Amount of TP gross of IGT]

S.35.01.04.01,c0100 [Identification code of entity , Technical Provisions - Health (similar to non-life)|Amount of TP gross of IGT]

S.35.01.04.01,c0130 [Identification code of entity , Technical Provisions - Health (similar to life)|Amount of TP gross of IGT]

S.35.01.04.01,c0160 [Identification code of entity , Technical Provisions - Life (excluding health and index-linked and unit-linked)|Amount of TP gross of IGT]

S.35.01.04.01,c0190 [Identification code of entity , Technical Provisions - Index-linked and unit-linked insurance|Amount of TP gross of IGT]



