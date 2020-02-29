===========
S.06.01_113
===========

Rule definition
---------------

IF {S.01.01.04.01,r0140,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35" THEN {S.06.01.01.01,r0100,c0010} + {S.06.01.01.01,r0100,c0020} +{S.06.01.01.01,r0100,c0030} +{S.06.01.01.01,r0100,c0040} +  {S.06.01.01.01,r0100,c0050} + {S.06.01.01.01,r0100,c0060} = {S.02.01.01.01,r0200,c0010} + {S.02.01.01.01,r0410,c0010}


Template references
-------------------

S.01.01.04.01
S.02.01.01.01
S.06.01.01.01 Summary of assets


Datapoints
----------

S.01.01.04.01,r0140,c0010 [nan]

S.02.01.01.01,r0200,c0010 [Assets|Investments (other than assets held for index-linked and unit-linked contracts)|Deposits other than cash equivalents , Solvency II value]

S.02.01.01.01,r0410,c0010 [Assets|Cash and cash equivalents , Solvency II value]

S.06.01.01.01,r0100,c0010 [By category|Cash and deposits , Life]

S.06.01.01.01,r0100,c0020 [By category|Cash and deposits , Non-life]

S.06.01.01.01,r0100,c0030 [By category|Cash and deposits , Ring-fenced funds]

S.06.01.01.01,r0100,c0040 [By category|Cash and deposits , Other internal funds]

S.06.01.01.01,r0100,c0050 [By category|Cash and deposits , Shareholders' funds]

S.06.01.01.01,r0100,c0060 [By category|Cash and deposits , General]



