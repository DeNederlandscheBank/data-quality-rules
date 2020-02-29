===========
S.36.02_110
===========

Rule definition
---------------

IF {S.36.02.01.01,c0010} <> " " AND {S.36.02.01.01,c0100} <> "SWAPS-CURRENCY" THEN {S.36.02.01.01,c0130} <> " "


Template references
-------------------

S.36.02.01.01 IGT - Derivatives


Datapoints
----------

S.36.02.01.01,c0010 [Y-axis (GX): ID of intragroup transaction|Identification code of investor/buyer/transferee/payer/reinsured/beneficiary|URI|S.36.02.zz.01 line identification|Identification code of issuer/seller/transferor/receiver/reinsurer/provider , Y-axis (GX): ID of intragroup transaction]

S.36.02.01.01,c0100 [ID of intragroup transaction|Identification code of investor/buyer/transferee/payer/reinsured/beneficiary|URI|S.36.02.zz.01 line identification|Identification code of issuer/seller/transferor/receiver/reinsurer/provider , Transaction type]

S.36.02.01.01,c0130 [ID of intragroup transaction|Identification code of investor/buyer/transferee/payer/reinsured/beneficiary|URI|S.36.02.zz.01 line identification|Identification code of issuer/seller/transferor/receiver/reinsurer/provider , Currency]



