===========
S.27.01_302
===========

Rule definition
---------------

IF {S.27.01.01.19,r3270,c1140}<>0 THEN {S.27.01.01.19,r3270,c1140}=MAX(0;(({S.27.01.01.19,r3200,c1140}+{S.27.01.01.19,r3210,c1140})**2)+{S.27.01.01.19,r3220,c1140}**2+{S.27.01.01.19,r3230,c1140}**2+{S.27.01.01.19,r3240,c1140}**2)**0.5


Template references
-------------------

S.27.01.01.19 Man made catastrophe risk - Other non-life catastrophe risk


Datapoints labels
-----------------

S.27.01.01.19,r3200,c1140 [mat other than marine and aviation, catastrophe risk charge other non-life catastrophe risk before risk mitigation]

S.27.01.01.19,r3210,c1140 [non-proportional mat reinsurance other than marine and aviation, catastrophe risk charge other non-life catastrophe risk before risk mitigation]

S.27.01.01.19,r3220,c1140 [miscellaneous financial loss, catastrophe risk charge other non-life catastrophe risk before risk mitigation]

S.27.01.01.19,r3230,c1140 [non-proportional casualty reinsurance other than general liability, catastrophe risk charge other non-life catastrophe risk before risk mitigation]

S.27.01.01.19,r3240,c1140 [non-proportional credit & surety reinsurance, catastrophe risk charge other non-life catastrophe risk before risk mitigation]

S.27.01.01.19,r3270,c1140 [total after diversification, catastrophe risk charge other non-life catastrophe risk before risk mitigation]



