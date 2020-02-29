===========
S.26.04_107
===========

Rule definition
---------------

IF {S.26.04.04.05,r1200,c0230} <>0 THEN {S.26.04.04.05,r1200,c0230} = MAX({S.26.04.04.05,r1200,c0190} - {S.26.04.04.05,r1200,c0200} - {S.26.04.04.05,r1200,c0210} + {S.26.04.04.05,r1200,c0220},0)


Template references
-------------------

S.26.04.04.05

Datapoints
----------

S.26.04.04.05,r1200,c0190 [NSLT health lapse risk , Initial absolute values before shock|Assets]

S.26.04.04.05,r1200,c0200 [NSLT health lapse risk , Initial absolute values before shock|Liabilities]

S.26.04.04.05,r1200,c0210 [NSLT health lapse risk , Absolute values after shock|Assets]

S.26.04.04.05,r1200,c0220 [NSLT health lapse risk , Absolute values after shock|Liabilities]

S.26.04.04.05,r1200,c0230 [NSLT health lapse risk , Absolute values after shock|Solvency capital requirement]



