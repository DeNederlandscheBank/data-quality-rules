===========
S.06.01_117
===========

Rule definition
---------------

IF {S.01.01.04.01,r0180,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35" THEN {S.06.01.01.01,r0140,c0010} + {S.06.01.01.01,r0140,c0020} + {S.06.01.01.01,r0140,c0030} + {S.06.01.01.01,r0140,c0040} +  {S.06.01.01.01,r0140,c0050} + {S.06.01.01.01,r0140,c0060} + {S.06.01.01.01,r0150,c0010} + {S.06.01.01.01,r0150,c0020} + {S.06.01.01.01,r0150,c0030} + {S.06.01.01.01,r0150,c0040} +  {S.06.01.01.01,r0150,c0050} + {S.06.01.01.01,r0150,c0060} +{S.06.01.01.01,r0180,c0010} + {S.06.01.01.01,r0180,c0020} + {S.06.01.01.01,r0180,c0030} +{S.06.01.01.01,r0180,c0040} +  {S.06.01.01.01,r0180,c0050} + {S.06.01.01.01,r0180,c0060} + {S.06.01.01.01,r0180,c0010} + {S.06.01.01.01,r0180,c0020} +{S.06.01.01.01,r0180,c0030} +{S.06.01.01.01,r0180,c0040} +  {S.06.01.01.01,r0180,c0050} + {S.06.01.01.01,r0180,c0060} + {S.06.01.01.01,r0180,c0010} + {S.06.01.01.01,r0180,c0020} + {S.06.01.01.01,r0180,c0030} + {S.06.01.01.01,r0180,c0040} +  {S.06.01.01.01,r0180,c0050} + {S.06.01.01.01,r0180,c0060} + {S.06.01.01.01,r0190,c0010} + {S.06.01.01.01,r0190,c0020} +{S.06.01.01.01,r0190,c0030} +{S.06.01.01.01,r0190,c0040} +  {S.06.01.01.01,r0190,c0050} + {S.06.01.01.01,r0190,c0060} = {S.02.01.01.01,r0190,c0010} - {S.02.01.01.01,r0790,c0010}


Template references
-------------------

S.01.01.04.01
S.02.01.01.01
S.06.01.01.01 Summary of assets


Datapoints
----------

S.01.01.04.01,r0180,c0010 [nan]

S.02.01.01.01,r0190,c0010 [Assets|Investments (other than assets held for index-linked and unit-linked contracts)|Derivatives , Solvency II value]

S.02.01.01.01,r0790,c0010 [Liabilities|Derivatives , Solvency II value]

S.06.01.01.01,r0140,c0010 [By category|Futures , Life]

S.06.01.01.01,r0140,c0020 [By category|Futures , Non-life]

S.06.01.01.01,r0140,c0030 [By category|Futures , Ring-fenced funds]

S.06.01.01.01,r0140,c0040 [By category|Futures , Other internal funds]

S.06.01.01.01,r0140,c0050 [By category|Futures , Shareholders' funds]

S.06.01.01.01,r0140,c0060 [By category|Futures , General]

S.06.01.01.01,r0150,c0010 [By category|Call Options , Life]

S.06.01.01.01,r0150,c0020 [By category|Call Options , Non-life]

S.06.01.01.01,r0150,c0030 [By category|Call Options , Ring-fenced funds]

S.06.01.01.01,r0150,c0040 [By category|Call Options , Other internal funds]

S.06.01.01.01,r0150,c0050 [By category|Call Options , Shareholders' funds]

S.06.01.01.01,r0150,c0060 [By category|Call Options , General]

S.06.01.01.01,r0180,c0010 [By category|Forwards , Life]

S.06.01.01.01,r0180,c0020 [By category|Forwards , Non-life]

S.06.01.01.01,r0180,c0030 [By category|Forwards , Ring-fenced funds]

S.06.01.01.01,r0180,c0040 [By category|Forwards , Other internal funds]

S.06.01.01.01,r0180,c0050 [By category|Forwards , Shareholders' funds]

S.06.01.01.01,r0180,c0060 [By category|Forwards , General]

S.06.01.01.01,r0190,c0010 [By category|Credit derivatives , Life]

S.06.01.01.01,r0190,c0020 [By category|Credit derivatives , Non-life]

S.06.01.01.01,r0190,c0030 [By category|Credit derivatives , Ring-fenced funds]

S.06.01.01.01,r0190,c0040 [By category|Credit derivatives , Other internal funds]

S.06.01.01.01,r0190,c0050 [By category|Credit derivatives , Shareholders' funds]

S.06.01.01.01,r0190,c0060 [By category|Credit derivatives , General]



