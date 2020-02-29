===========
S.01.01_115
===========

Rule definition
---------------

IF {S.02.01.01.01,r0160,c0010} > 0.05*({S.02.01.01.01,r0070,c0010}+{S.02.01.01.01,r0220,c0010}) THEN {S.01.01.04.01,r0160,c0010} = "REPORTED"


Template references
-------------------

S.01.01.04.01
S.02.01.01.01

Datapoints
----------

S.01.01.04.01,r0160,c0010 [nan]

S.02.01.01.01,r0070,c0010 [Assets|Investments (other than assets held for index-linked and unit-linked contracts) , Solvency II value]

S.02.01.01.01,r0160,c0010 [Assets|Investments (other than assets held for index-linked and unit-linked contracts)|Bonds|Structured notes , Solvency II value]

S.02.01.01.01,r0220,c0010 [Assets|Assets held for index-linked and unit-linked contracts , Solvency II value]



