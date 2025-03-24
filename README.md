# GAPProduction
Code used for producing and managing GAP species data.  This package includes handy functions to save time performing many tedious tasks and it facilitates convenient interaction with the internal GAP database with Python.  It is for internal use and data development and is not usable by those without permission to access GAP databases.

# Functions
Functions are listed by module below.  Consult version 1 for many more that could be updated and added to version 2.

## Database
Functions that facilitate interactions with the GAP databases.

* ConnectDB() - Provides a cursor within and a connection to the database.

## Citations
Functions that facilitate management and addition of citations to the GAP databases.

* CitationExists() - Looks for a citation in the database.  Matches would unlikely be exact, so the function uses a wildcard expression to match the citation to the database and prints protential matches.
* Availability() - Check if a reference code is available for use. 
* BuildStrRefCode() - Build a reference code (strRefCode) from a reference string.
* AddReference() - Add a reference to the database if the reference code doesn't exit.

## Taxonomy
Functions that do things related to taxon concepts and lists.

* GetTaxonInfo() - Returns a dictionary of : GAP species code, full scientific name, common name, and ITIS TSN.  The function will try to lookup the species by GAP species code, then scientific name, then common name.
* AllSpeciesList() - Returns a list of codes for all the currently valid GAP species concepts.

## Ranges
Functions to support GAP range map production and management.

* RangeEVTs_season() - Returns a list of EVTs occuring within a speicies' seasonal range.
* RangeShapefile() - Creates a shapefile and geodataframe of the range of a species based on the species code and season list.
* V2FortblRanges() - Reads a v2 range output database and returns a dataframe that fits the 2016 GAP database ranges table format.
* V2FortblRangeEdit() - Reads a compilation info table from a v2 output database and returns a dataframe suitable for tblRangeEdit.
* RangeEditsDict() - Returns a dictionary of range edits for a given species code.

## Strings
Functions that facilitate common tasks for searching and filtering lists, strings, etc.

* GapCase() - Returns an input string in the Gap Code capitalization ('mAMROx').
* FilterList() -- Returns a list containing items from the input list that match the search string.
* LegalChars() -- Returns the string with all illegal characters removed/replaced.
* RemoveRepeats() -- Returns the string with all adjacent, duplicate occurrences of the given search string reduced to a single occurrence.

## Documents
Functions that facilitate common tasks for searching and manipulating text files.

* Write() - appends to (default) or overwrites a file with the text of the second argument; creates the file and even the directories, if necessary.
* DocReplace() - replaces selected text in a given document; any number of text replacement pairs may be submitted.
* GetLines() - returns a list containing the complete text of every line that contains the search text.
* SearchInFiles() - searches for the given text in the files of the given root directory, including all subdirectories.
* SearchFilenames() - searches for the given text in the filenames of a given root directory, including all subdirectories.
* SearchDirectoryNames() -- searches the given text in the directory names of given root directory, including all subdirectories.

## Habitat
Functions related to GAP habitat models.

* ProcessingNotesDict() - Returns a dictionary of processing notes for a given species code.
* ModelEVTs() -  Returns two lists, primary and secondary EVT selections for a model.
* EVTsInRegion() - Returns a list of EVTs occurring in a list of regions.
* ModelAsDictionary() - Returns model parameters as a dictionary.
* ReviewNotesDict() - Returns a dictionary of model review notes.
* SpeciesModelList() - Returns a list of all the region season models for a species, excludes ysnInclude = 0 models.

## Dictionaries
Dictionaries commonly used in processing GAP data as well as general functions for manipulating dictionaries.

* InvertDictionary() -- Returns a dictionary in which the keys are the values from the input dictionary, and the values are a list of keys that had that value in the input dictionary.
* ReverseDictionary() -- Returns a dictionary in which the keys and values have been swapped.
* IterableOfIterablesToDictionary() - Converts a list/tuple of lists/tuples to a dictionary.
* stateDict_To_Abbr -- A dictionary in which the keys are state/territory names and the values are the states' two-character postal code abbreviations.
* stateDict_From_Abbr -- A dictionary in which the keys are the states' two-character postal code abbreviations, and the values are the state names.
* taxaDict -- A dictionary in which the keys are the class letter, used as the the first character in the six-character GAP unique IDs for species, and the values are the class common name.
* taxaDict_Latin -- A dictionary in which the keys are the class letter, used as the the first character in the six-character GAP unique IDs for species, and the values are the class scientific name.
* stateFIPS_Code_to_Name -- A dictionary in which the keys are the state FIPS codes (as int) and the values are the state names.
* stateFIPS_Name_to_Code -- A dictionary in which the keys are the state names and the values are the state FIPS codes (as int).
* regionsDict_Num_To_Name = A dictionary in which the keys are the GAP modeling regions by numerical code (as int) and the values are the names of the modeling regions.
* regionsDict_Num_To_Abbr = A dictionary in which the keys are the GAP modeling regions by numerical code (as int) and the values are the abbreviations of the modeling regions.
* regionsDict_Abbr_To_Num = A dictionary in which the keys are the GAP modeling region abbreviations and the values are the modeling region codes (as int).
* regionsDict_Name_To_Num = A dictionary in which the keys are the GAP modeling region names and the values are the modeling region codes (as int).
* regionsDict_Abbr_To_Name = A dictionary in which the keys are the GAP modeling region abbreviations and the vlaues are the modeling region names.
* rangeCodesDict = A dictionary of dictionaries with a key for each GAP range map attribute and a value that's a dictionary of definitions.
* staffDict = A dictionary of staff's initials.

## Package Dependencies
python 3.x
sqlalchemy
pyodbc
pandas

# Git Workflow
sqwilliams is the upstream repo and all other users should fork it and treat it as such.  Use the github interface to manage pull requests/syncing or create an upstream remote locally and pull commits via that remote.  For development, create a feature branch and push it to your github repo and submit a pull request to sgwilliams for him to review and accept.