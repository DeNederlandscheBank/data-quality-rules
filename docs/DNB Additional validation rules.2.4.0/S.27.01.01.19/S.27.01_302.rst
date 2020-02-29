===========
S.27.01_302
===========

Rule definition
---------------

IF {S.27.01.01.19,r3270,c1140}<>0 THEN {S.27.01.01.19,r3270,c1140}=MAX(0;(({S.27.01.01.19,r3200,c1140}+{S.27.01.01.19,r3210,c1140})**2)+{S.27.01.01.19,r3220,c1140}**2+{S.27.01.01.19,r3230,c1140}**2+{S.27.01.01.19,r3240,c1140}**2)**0.5


Template references
-------------------

S.27.01.01.19 Man made catastrophe risk - Other non-life catastrophe risk


Datapoints
----------

S.27.01.01.19,r3200,c1140 [MAT other than Marine and Aviation , Man made catastrophe risk - Other non-life catastrophe risk|Catastrophe Risk Charge Other non-life catastrophe risk before risk mitigation]

S.27.01.01.19,r3210,c1140 [Non-proportional MAT reinsurance other than Marine and Aviation , Man made catastrophe risk - Other non-life catastrophe risk|Catastrophe Risk Charge Other non-life catastrophe risk before risk mitigation]

S.27.01.01.19,r3220,c1140 [Miscellaneous financial loss , Man made catastrophe risk - Other non-life catastrophe risk|Catastrophe Risk Charge Other non-life catastrophe risk before risk mitigation]

S.27.01.01.19,r3230,c1140 [Non-proportional Casualty reinsurance other than General liability , Man made catastrophe risk - Other non-life catastrophe risk|Catastrophe Risk Charge Other non-life catastrophe risk before risk mitigation]

S.27.01.01.19,r3240,c1140 [Non-proportional Credit & Surety reinsurance , Man made catastrophe risk - Other non-life catastrophe risk|Catastrophe Risk Charge Other non-life catastrophe risk before risk mitigation]

S.27.01.01.19,r3270,c1140 [Total after diversification , Man made catastrophe risk - Other non-life catastrophe risk|Catastrophe Risk Charge Other non-life catastrophe risk before risk mitigation]



