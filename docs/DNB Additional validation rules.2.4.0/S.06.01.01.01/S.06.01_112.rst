===========
S.06.01_112
===========

Rule definition
---------------

IF {S.01.01.01.01,r0140,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35" THEN {S.06.01.01.01,r0100,c0010} + {S.06.01.01.01,r0100,c0020} +{S.06.01.01.01,r0100,c0030} +{S.06.01.01.01,r0100,c0040} +  {S.06.01.01.01,r0100,c0050} + {S.06.01.01.01,r0100,c0060} = {S.02.01.01.01,r0200,c0010} + {S.02.01.01.01,r0410,c0010}


Template references
-------------------

S.01.01.01.01 Content of the submission

S.02.01.01.01 Balance sheet

S.06.01.01.01 Summary of assets


Datapoints labels
-----------------

S.01.01.01.01,r0140,c0010 [s.06.02.01 - list of assets, none]

S.02.01.01.01,r0200,c0010 [deposits other than cash equivalents, solvency ii value]

S.02.01.01.01,r0410,c0010 [cash and cash equivalents, solvency ii value]

S.06.01.01.01,r0100,c0010 [cash and deposits, life]

S.06.01.01.01,r0100,c0020 [cash and deposits, non-life]

S.06.01.01.01,r0100,c0030 [cash and deposits, ring-fenced funds]

S.06.01.01.01,r0100,c0040 [cash and deposits, other internal funds]

S.06.01.01.01,r0100,c0050 [cash and deposits, shareholders' funds]

S.06.01.01.01,r0100,c0060 [cash and deposits, general]



