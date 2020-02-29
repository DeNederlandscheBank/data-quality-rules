===========
S.28.01_139
===========

Rule definition
---------------

IF {S.28.01.01.02,r0140,c0020} <> 0 AND {S.05.01.01.01,r0130,c0130}  < 0  THEN {S.28.01.01.02,r0140,c0030} = 0


Template references
-------------------

S.05.01.01.01 Non-Life (direct business/accepted proportional reinsurance and accepted non-proportional reinsurance)

S.28.01.01.02 Background information


Datapoints
----------

S.05.01.01.01,r0130,c0130 [Premiums written|Gross - Non-proportional reinsurance accepted , Line of Business for: accepted non-proportional reinsurance|Health]

S.28.01.01.02,r0140,c0020 [Non-proportional health reinsurance , Background information|Net (of reinsurance/SPV) best estimate and TP calculated as a whole]

S.28.01.01.02,r0140,c0030 [Non-proportional health reinsurance , Background information|Net (of reinsurance) written premiums in the last 12 months]



