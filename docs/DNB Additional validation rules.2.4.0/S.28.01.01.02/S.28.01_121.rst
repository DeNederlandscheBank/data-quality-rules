===========
S.28.01_121
===========

Rule definition
---------------

IF {S.28.01.01.02,r0120,c0020} <> 0 AND ({S.05.01.01.01,r0110,c0110} + {S.05.01.01.01,r0120,c0110}) > 0   THEN {S.28.01.01.02,r0120,c0030} > 0


Template references
-------------------

S.05.01.01.01 Non-Life (direct business/accepted proportional reinsurance and accepted non-proportional reinsurance)

S.28.01.01.02 Background information


Datapoints
----------

S.05.01.01.01,r0110,c0110 [Premiums written|Gross - Direct Business , Line of Business for: non-life insurance and reinsurance obligations (direct business and accepted proportional reinsurance)|Assistance]

S.05.01.01.01,r0120,c0110 [Premiums written|Gross - Proportional reinsurance accepted , Line of Business for: non-life insurance and reinsurance obligations (direct business and accepted proportional reinsurance)|Assistance]

S.28.01.01.02,r0120,c0020 [Assistance and proportional reinsurance , Background information|Net (of reinsurance/SPV) best estimate and TP calculated as a whole]

S.28.01.01.02,r0120,c0030 [Assistance and proportional reinsurance , Background information|Net (of reinsurance) written premiums in the last 12 months]



