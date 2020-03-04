===========
S.26.04_107
===========

Rule definition
---------------

IF {S.26.04.04.05,r1200,c0230} <>0 THEN {S.26.04.04.05,r1200,c0230} = MAX({S.26.04.04.05,r1200,c0190} - {S.26.04.04.05,r1200,c0200} - {S.26.04.04.05,r1200,c0210} + {S.26.04.04.05,r1200,c0220},0)


Template references
-------------------

S.26.04.04.05 NSLT health lapse risk


Datapoints labels
-----------------

S.26.04.04.05,r1200,c0190 [nslt health lapse risk, assets]

S.26.04.04.05,r1200,c0200 [nslt health lapse risk, liabilities]

S.26.04.04.05,r1200,c0210 [nslt health lapse risk, assets]

S.26.04.04.05,r1200,c0220 [nslt health lapse risk, liabilities]

S.26.04.04.05,r1200,c0230 [nslt health lapse risk, solvency capital requirement]



