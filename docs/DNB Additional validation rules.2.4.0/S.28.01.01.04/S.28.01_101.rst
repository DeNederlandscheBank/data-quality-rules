===========
S.28.01_101
===========

Rule definition
---------------

{S.28.01.01.03,r0200,c0040} = MAX(0;(MAX(0; {S.28.01.01.04,r0210,c0050} * 0.037) - MAX(0;{S.28.01.01.04,r0220,c0050} * 0.052) + MAX(0; {S.28.01.01.04,r0230,c0050} * 0.007) + MAX(0; {S.28.01.01.04,r0240,c0050} *  0.021) + MAX(0; {S.28.01.01.04,r0250,c0060} * 0.0007)))


Template references
-------------------

S.28.01.01.03 Linear formula component for life insurance and reinsurance obligations

S.28.01.01.04 Total capital at risk for all life (re)insurance obligations


Datapoints labels
-----------------

S.28.01.01.03,r0200,c0040 [mcrl result, none]

S.28.01.01.04,r0210,c0050 [obligations with profit participation - guaranteed benefits, net (of reinsurance/spv) best estimate and tp calculated as a whole]

S.28.01.01.04,r0220,c0050 [obligations with profit participation - future discretionary benefits, net (of reinsurance/spv) best estimate and tp calculated as a whole]

S.28.01.01.04,r0230,c0050 [index-linked and unit-linked insurance obligations, net (of reinsurance/spv) best estimate and tp calculated as a whole]

S.28.01.01.04,r0240,c0050 [other life (re)insurance and health (re)insurance obligations, net (of reinsurance/spv) best estimate and tp calculated as a whole]

S.28.01.01.04,r0250,c0060 [total capital at risk for all life (re)insurance obligations, net (of reinsurance/spv) total capital at risk]



