## Module to create species-specific metadata for a range table or model raster.
##
## Public Function:
##
## Run() -- Creates and processes the metadata for the input species and file.
##
##
##

import dictionaries, gapdb, os, time, gapageconfig


class __MD:
    def __init__(self, sp, fPath):
        # The species' GAP code
        self.sp = sp
        # Get the full path to the input file
        self.fPath = os.path.abspath(fPath)
        # Gets the name of the input file
        self.outName = os.path.basename(fPath)
        # Determines whether to process a model or range
        self.x = _GetX(fPath)


##############################
## Primary function that intializes the process
def Run(sp, fPath):
    '''
    (string, string)

    Creates dynamic, species-specific metadata for the input range or model.

    Returns True if the function ran successfully. Otherwise, returns False.

    Arguments:
    sp -- The species' unique GAP ID
    fPath -- The complete, absolute path to the range table or model raster
        for which you wish to create metadata

    Example:
    >>> import gapmetadata as gm
    >>> gm.Run('aadsax', 'des_apa_adsax')
    '''

    try:
        md = __MD(sp, fPath)

        if md.x:
            md.tSpXML = _Get_XML(md)
            # Applies the species-specific xml to the range/model metadata
            _ApplyMD(md)
        else:
            return False

        return True

    except Exception as e:
        print 'Error in metadata module:\n', e
        return False



##############################
## Delete the file, if it exists
def _Clear(f):
    '''
    A private function that should only be called by other functions within
    this module.
    '''
    if os.path.exists(f):
        os.remove(f)
    else:
        pass
    return



##############################
## Determine whether the file is a model, range table, or shapefile and
## return one of three strings: 'Model', 'Range', or 'Shapefile'
def _GetX(fPath):
    '''
    A private function that should only be called by other functions within
    this module.
    '''
    try:
        import arcpy
        try:
            # if the file does not exist, end
            if not arcpy.Exists(fPath):
                return False
    
            # if the file is either a raster dataset or a dbase table, return 'Model' or 'Range'
            while True:
                desc = arcpy.Describe(fPath)
                dt = desc.datatype
                if dt == 'RasterDataset':
                    return 'Model'
                elif dt == 'DbaseTable':
                    return 'Range'
                elif dt == 'ShapeFile':
                    return 'Shp'
                else:
                    fPath = raw_input("Please enter the full path to the range dbase table\nor to the raster dataset: ")
    
        except Exception as e:
            print 'Exception in _GetX:\n', e
            return False
    except:
        print("Couldn't import arcpy")


##############################
## Process the xml, return the species' temp xml metadata
def _Get_XML(md):
    '''
    A private function that should only be called by other functions within
    this module.
    '''
    try:
        # The metadata template file
        md.mdT = _Template(md.x)

        # The species-specific metadata text
        md.text = _MD_Text(md)

        return

    except Exception as e:
        print 'Exception in _Get_XML:\n', e
        return False



##############################
## Find the metadata template file for this file type
def _Template(x):
    '''
    A private function that should only be called by other functions within
    this module.
    '''
    # Get the directory name within which this script is stored
    ##scriptDir = os.path.dirname(__file__)
    
    mdDir = gapageconfig.meta_templates_dir

    try:
        mdTName = x.lower() + "_metadata_template.xml"

        # The path of the metadata template file:
        mdT = os.path.join(mdDir, mdTName)

        # If the md template exists, go on; otherwise, get the proper path from the user:
        while True:
            if os.path.exists(mdT) and mdT.endswith(".xml"):
                return mdT
            else:
                mdT = raw_input("The path to the metadata template file is incorrect.\nThe file should be located at\n%s\nPlease enter the correct, full path of to the file, including the file name: " % mdT)

    except Exception as e:
        print 'Exception in _Template:\n', e
        return False


##############################
## Retrieve and update the text for the xml metadata
def _MD_Text(md):
    '''
    A private function that should only be called by other functions within
    this module.
    '''
    try:
        taxDict = dictionaries.taxaDict
        # Get the list of states in which the species occurs
        spStates = gapdb.States(md.sp)
        # Format the state list for inclusion in the xml
        states = '</placekey><placekey>'.join(spStates)

        with open(md.mdT, 'r') as tXML:
            # oContent holds the text of the metadata template
            text = tXML.read()
        text = unicode(text, errors='ignore')

        # Replace the 'Insert...' text of the template content
        text = text.replace('[InsertStates]', states)
        text = text.replace('[InsertCommonName]', gapdb.NameCommon(md.sp))
        text = text.replace('[InsertSciName]', gapdb.NameSci(md.sp))
        text = text.replace('[InsertSpeciesCode]', md.sp)
        text = text.replace('[InsertGapCaseCode]', gapdb.GapCase(md.sp))
        text = text.replace('[InsertDownloadFileName]', md.outName)
        text = text.replace('[InsertFileName]', os.path.basename(md.fPath))
        text = text.replace('[InsertClass]', taxDict[md.sp[0]])

        # Insert the current date
        now = time.strftime("%Y%m%d", time.localtime())
        text = text.replace('[InsertDate]', now)
        year = time.strftime('%Y', time.localtime())
        text = text.replace('[InsertYear]', year)

        # Insert the line breaks
        text = text.replace('InsertBreak', '&#xD;')

        return text

    except Exception as e:
        print 'Exception in _MD_Text:'
        print e
        return False



def _ApplyMD(md):
    _GetMDPath(md)
    _Clear(md.mdP)

    with open(md.mdP, 'w') as od:
        od.write(md.text)

    return


def _GetMDPath(md):
    if md.x == 'Model':
        if md.fPath.endswith('.tif'):
            p = md.fPath + '.xml'
        else:
            p = os.path.join(md.fPath, 'metadata.xml')
    if md.x == 'Range' or md.x == 'Shp':
        p = md.fPath + '.xml'

    md.mdP = p
    return



def __main():
    pass

if __name__ == '__main__':
    __main()