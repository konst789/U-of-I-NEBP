# PBL-Lapse-Rate-Response

Files Included:
1)PBL_RunFile
2)LapseRate_700mb
3)readGrawProfile_alg
4)AlgorithmFunctions
-----
5)AlgorithmFunctions_Plots - added code to plot inidividual methods (currently commented)
6)readGrawProfile_deprecated - old version that did NOT include addition of launch DateTime 

If for any reason issues arrise due to time based plotting features, it is recommened to revert to 5&6 as the new files have 
not been tested as strenuously. Using these requires changing package titles in PBL_RunFile Program.

Files 1 & 2 are main programs for Planetary Boundary Layer Determination & Lapse Rate Determination
Each program explains function in top lines of file. 

When utilizing the main programs listed, ensure subprograms are contained in the same folder that main program is in
3 & 4 are utilized as callible function packages in 1 & 2
File Structure:
  PBL_RunFile
    -> Utilizes readGrawProfile_alg
    -> Utilizes Algorithm Functions
  LapseRate_700mb
    -> Utilizes readGrawProfile_alg
   
  
These programs are inteded to run GRAWMET atmospheric profiles. The programs will prompt user to input a folder containing profiles
and run any profiles contained in the folder. This hunting program will continue into each subfolder sequentially and run all
contained profiles, as well as run multiple profiles listed in one folder.

These programs will ask the user for input for what folder to run, if the user would like to save the results,
and where the saved results should go.

For best reporting, ensure filenames are consistent and have same number of characters

NOTE: Errors may occur if different package versions are released. It may be neccessary to perform debugging if packages depricate or update.


 
