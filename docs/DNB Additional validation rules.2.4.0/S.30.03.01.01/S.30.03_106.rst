===========
S.30.03_106
===========

Rule definition
---------------

IF {S.30.03.01.01,c0090} = "QUOTA SHARE" OR {S.30.03.01.01,c0090}="STOP LOSS" THEN {S.30.03.01.01,c0200} >= 0


Template references
-------------------

S.30.03.01.01 Outgoing Reinsurance Program basic data


Datapoints
----------

S.30.03.01.01,c0090 [Line of business [general]|Progressive number of surplus/layer in program|Treaty identification code|Reinsurance program code|Section code in the treaty , Type of reinsurance treaty]

S.30.03.01.01,c0200 [Line of business [general]|Progressive number of surplus/layer in program|Treaty identification code|Reinsurance program code|Section code in the treaty , Retention or priority (%)]



