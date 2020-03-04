===========
S.28.01_113
===========

Rule definition
---------------

IF {S.28.01.01.02,r0040,c0020} <> 0 AND ({S.05.01.01.01,r0110,c0030} + {S.05.01.01.01,r0120,c0030}) > 0  THEN {S.28.01.01.02,r0040,c0030} > 0


Template references
-------------------

S.05.01.01.01 Non-Life (direct business/accepted proportional reinsurance and accepted non-proportional reinsurance)

S.28.01.01.02 Background information


Datapoints labels
-----------------

S.05.01.01.01,r0110,c0030 [gross - direct business, workers' compensation insurance]

S.05.01.01.01,r0120,c0030 [gross - proportional reinsurance accepted, workers' compensation insurance]

S.28.01.01.02,r0040,c0020 [workers' compensation insurance and proportional reinsurance, net (of reinsurance/spv) best estimate and tp calculated as a whole]

S.28.01.01.02,r0040,c0030 [workers' compensation insurance and proportional reinsurance, net (of reinsurance) written premiums in the last 12 months]



