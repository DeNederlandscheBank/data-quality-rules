=====
Usage
=====

Data format requirements
========================

We added a tutorial that converts an XBRL instance file to csv files for all reporting template in the instance. If you want to use data from another source you have to make sure that the data is in the correct format.

Solvency 2
----------

- the template name follows the standard Solvency 2 code, for example S.02.01.02.01 and S.28.02.01.02;
- the file names of the individual templates is the template name plus an extension (.csv or .pickle), for example S.01.02.07.01.pickle;
- the file name of all closed axes templates combined is the instance file name plus an extension, for example qrs_240_instance.pickle (the example instance for qrs);
- the column names and the index names for all templates have the following format: {reporting template name},R????,C???? or {reporting template name},C????, depending on the definition; for example S.02.01.02.01,R0030,C0010 or S.06.02.01.01,C0040;
 
FTK
---

- the template name follows the standard FTK code with prefix FTK, for example FTK.K101-1 or FTK.K209B;
- the file names of the individual templates is the template name plus an extension (.csv or .pickle), for example FTK.K101-1.pickle;
- the file name of all closed axes templates combined is the instance file name plus an extension, for example DNB-NR_FTK-2019-06_2019-12-31_MOD_FTK-BEL.pickle (the example instance for FTK-BEL);
- the column names and the index names for all templates have the following format: {reporting template name},R???,C??? or {reporting template name},C???, depending on the definition; for example FTK.K101-1,R010,C010 or FTK.K209B,C150;

