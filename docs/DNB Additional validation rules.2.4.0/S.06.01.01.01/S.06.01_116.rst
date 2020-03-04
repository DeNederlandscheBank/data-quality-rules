===========
S.06.01_116
===========

Rule definition
---------------

IF {S.01.01.01.01,r0180,c0010}="NOT DUE IN ACCORDANCE WITH ARTICLE 35" THEN {S.06.01.01.01,r0140,c0010} + {S.06.01.01.01,r0140,c0020} + {S.06.01.01.01,r0140,c0030} + {S.06.01.01.01,r0140,c0040} +  {S.06.01.01.01,r0140,c0050} + {S.06.01.01.01,r0140,c0060} + {S.06.01.01.01,r0150,c0010} + {S.06.01.01.01,r0150,c0020} + {S.06.01.01.01,r0150,c0030} + {S.06.01.01.01,r0150,c0040} +  {S.06.01.01.01,r0150,c0050} + {S.06.01.01.01,r0150,c0060} +{S.06.01.01.01,r0180,c0010} + {S.06.01.01.01,r0180,c0020} + {S.06.01.01.01,r0180,c0030} +{S.06.01.01.01,r0180,c0040} +  {S.06.01.01.01,r0180,c0050} + {S.06.01.01.01,r0180,c0060} + {S.06.01.01.01,r0180,c0010} + {S.06.01.01.01,r0180,c0020} +{S.06.01.01.01,r0180,c0030} +{S.06.01.01.01,r0180,c0040} +  {S.06.01.01.01,r0180,c0050} + {S.06.01.01.01,r0180,c0060} + {S.06.01.01.01,r0180,c0010} + {S.06.01.01.01,r0180,c0020} + {S.06.01.01.01,r0180,c0030} + {S.06.01.01.01,r0180,c0040} +  {S.06.01.01.01,r0180,c0050} + {S.06.01.01.01,r0180,c0060} + {S.06.01.01.01,r0190,c0010} + {S.06.01.01.01,r0190,c0020} +{S.06.01.01.01,r0190,c0030} +{S.06.01.01.01,r0190,c0040} +  {S.06.01.01.01,r0190,c0050} + {S.06.01.01.01,r0190,c0060} = {S.02.01.01.01,r0190,c0010} - {S.02.01.01.01,r0790,c0010}


Template references
-------------------

S.01.01.01.01 Content of the submission

S.02.01.01.01 Balance sheet

S.06.01.01.01 Summary of assets


Datapoints labels
-----------------

S.01.01.01.01,r0180,c0010 [s.08.02.01 - derivatives transactions, none]

S.02.01.01.01,r0190,c0010 [derivatives, solvency ii value]

S.02.01.01.01,r0790,c0010 [derivatives, solvency ii value]

S.06.01.01.01,r0140,c0010 [futures, life]

S.06.01.01.01,r0140,c0020 [futures, non-life]

S.06.01.01.01,r0140,c0030 [futures, ring-fenced funds]

S.06.01.01.01,r0140,c0040 [futures, other internal funds]

S.06.01.01.01,r0140,c0050 [futures, shareholders' funds]

S.06.01.01.01,r0140,c0060 [futures, general]

S.06.01.01.01,r0150,c0010 [call options, life]

S.06.01.01.01,r0150,c0020 [call options, non-life]

S.06.01.01.01,r0150,c0030 [call options, ring-fenced funds]

S.06.01.01.01,r0150,c0040 [call options, other internal funds]

S.06.01.01.01,r0150,c0050 [call options, shareholders' funds]

S.06.01.01.01,r0150,c0060 [call options, general]

S.06.01.01.01,r0180,c0010 [forwards, life]

S.06.01.01.01,r0180,c0020 [forwards, non-life]

S.06.01.01.01,r0180,c0030 [forwards, ring-fenced funds]

S.06.01.01.01,r0180,c0040 [forwards, other internal funds]

S.06.01.01.01,r0180,c0050 [forwards, shareholders' funds]

S.06.01.01.01,r0180,c0060 [forwards, general]

S.06.01.01.01,r0190,c0010 [credit derivatives, life]

S.06.01.01.01,r0190,c0020 [credit derivatives, non-life]

S.06.01.01.01,r0190,c0030 [credit derivatives, ring-fenced funds]

S.06.01.01.01,r0190,c0040 [credit derivatives, other internal funds]

S.06.01.01.01,r0190,c0050 [credit derivatives, shareholders' funds]

S.06.01.01.01,r0190,c0060 [credit derivatives, general]



