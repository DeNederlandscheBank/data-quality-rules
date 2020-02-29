===========
S.06.01_115
===========

Rule definition
---------------

IF {S.01.01.04.01,r0140,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35"  THEN {S.06.01.01.01,r0110,c0010} + {S.06.01.01.01,r0110,c0020} +{S.06.01.01.01,r0110,c0030} +{S.06.01.01.01,r0110,c0040} +  {S.06.01.01.01,r0110,c0050} + {S.06.01.01.01,r0110,c0060} = {S.02.01.01.01,r0230,c0010}


Template references
-------------------

S.01.01.04.01
S.02.01.01.01
S.06.01.01.01 Summary of assets


Datapoints
----------

S.01.01.04.01,r0140,c0010 [nan]

S.02.01.01.01,r0230,c0010 [Assets|Loans and mortgages , Solvency II value]

S.06.01.01.01,r0110,c0010 [By category|Mortgages and loans , Life]

S.06.01.01.01,r0110,c0020 [By category|Mortgages and loans , Non-life]

S.06.01.01.01,r0110,c0030 [By category|Mortgages and loans , Ring-fenced funds]

S.06.01.01.01,r0110,c0040 [By category|Mortgages and loans , Other internal funds]

S.06.01.01.01,r0110,c0050 [By category|Mortgages and loans , Shareholders' funds]

S.06.01.01.01,r0110,c0060 [By category|Mortgages and loans , General]



