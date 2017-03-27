## This module facilitates common tasks for archiving with the zipfile module,
##      while hiding all that atrocious and repetitive zipfile module verbiage.
##
##
## The public functions are:
##
## ZipDirectory() - Creates a zipfile and writes to it all directories,
##      subdirectories, and files from within the given root directory,
##      maintaining paths relative to their original locations.
##
## Unzip() - Extracts all directories, subdirectories, and files from
##      the zipfile and places them in the given root directory, maintaining
##      paths relative to their original locations.
##
## AddToZipfile() - Adds the passed file to the given zipfile.
##
## UnzipAll() - Unzips all the files in the passed directory
##

import zipfile, os, zlib


#####################
## Zip the given directory
def ZipDirectory(rootDir, outFile):
    '''
    (string, string) -> boolean

    Creates a zipfile at the given output path and zips all files and
    directories (recursively) within the given input root directory.

    Returns True if the function ran successfully. Otherwise, returns False.

    Will overwrite the output file if it already exists. Also, if the passed
    output filename does not end in '.zip', that extension will be appended.

    Arguments:
    rootDir -- The full, absolute path to the directory you wish to zip.
    outFile -- The full, absoluate path of the zipfile you wish to create or
        overwrite.

    Example:
    >>> ZipDirectory('C:\\temp\\t', 'C:\\temp\\output\\t.zip')
    True
    '''
    try:
        # Verify that the passed directory is actually a directory
        if os.path.isdir(rootDir) == False:
            print 'The first argument that you submitted to the ZipDirectory() function is not a valid directory. The path you submitted was %s.' % rootDir
            return False

        # Ensure that the output file is a zipfile
        if outFile.endswith('.zip') is False:
            outFile = outFile + '.zip'

        # If the output file already exists, delete it
        if os.path.exists(outFile):
            os.remove(outFile)

        # Create the zipfile object
        zipObj = zipfile.ZipFile(outFile, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)

        try:
            # Walk the directory
            for root, dirs, files in os.walk(rootDir):
                # For each level, set the output root as the root sans the system levels
                newRoot = root.replace(rootDir + '\\', '')
                # Create a list that contains the directories and the files in the root
                files = [i for i in files if not i.endswith('.lock')]
                l = dirs + files
                # For each directory and file in the root
                for item in l:
                    # To avoid creating redundant folders, if the file's root is the
                    # same as the rootDir, the output path will just be the item name;
                    # otherwise, the output path will include the root
                    if root != rootDir:
                        outPath = os.path.join(newRoot, item)
                    else:
                        outPath = item
                    # Add it to the zip object, with the path set properly
                    zipObj.write(os.path.join(root, item), outPath)

        except Exception as e:
            print e
            return False

        finally:
            # Close the zip object to prevent locking
            zipObj.close()

        return True

    except Exception as e:
        print e
        return False



def Unzip(inZipfile, outDirectory):
    '''
    (string, string) -> boolean

    Extracts all content of the given .zip file or .gz file and places the
    content in the given output directory.

    If the passed file is a .gz file, the script writes the content to a file
    inheriting its name from the input gzip file, sans extension, in the given
    output directory.

    Returns True if the function ran successfully. Otherwise, returns False.

    Arguments:
    inZipfile -- The absolute path to the zipfile from which you wish to extract
    outDirectory -- The absolute path to the output directory into which you
        wish to place the extracted content.

    Example:
    >>> Unzip('C:\\temp\\t.zip', 'C:\\temp\\mine\\t2')
    True
    '''
    if not os.path.exists(outDirectory):
        os.makedirs(outDirectory)

    x = False
    if inZipfile.lower().endswith('.zip'):
        x = __UnzipZip(inZipfile, outDirectory)
    elif inZipfile.lower().endswith('.gz'):
        x = __UnzipGZ(inZipfile, outDirectory)
    elif inZipfile.lower().endswith('.tar'):
        x = __UnzipTar(inZipfile, outDirectory)

    return x


#####################
## Unzip to the passed directory
def __UnzipZip(inZipfile, outDirectory):
    '''
    (string, string) -> boolean

    Extracts all content of the given zipfile and places the content in the
    given output directory.

    Returns True if the function ran successfully. Otherwise, returns False.

    Arguments:
    inZipfile -- The absolute path to the zipfile from which you wish to extract
    outDirectory -- The absolute path to the output directory into which you
        wish to place the extracted content.

    Example:
    >>> Unzip('C:\\temp\\t.zip', 'C:\\temp\\mine\\t2')
    True
    '''
    try:
        # Create the zip object
        zipObj = zipfile.ZipFile(inZipfile)
        try:
            # Extract everything from the object to the output directory
            zipObj.extractall(outDirectory)
        except Exception as e:
            print 'exception in Unzip()'
            print e
            return False
        finally:
            zipObj.close()

        return True
    except Exception as e:
        print inZipfile, '-', e
        return False


def __UnzipGZ(inZipfile, outDirectory):
    '''
    (string, string) -> boolean

    Extracts the content of the given gzip file and writes it to a file
    inheriting its name from the input gzip file, sans extension, in the given
    output directory.

    Returns True if the function ran successfully. Otherwise, returns False.

    Arguments:
    inZipfile -- The absolute path to the .gz from which you wish to extract
    outDirectory -- The absolute path to the output directory into which you
        wish to place the extracted content.

    Example:
    >>> Unzip('C:\\temp\\t.zip', 'C:\\temp\\mine\\t2')
    True
    '''
    try:
        import gzip
        # Unzip and read the content
        with gzip.open(inZipfile, 'rb') as z:
            content = z.read()

        # Construct the name and path for the output file
        outName = os.path.basename(inZipfile).split('.gz')[0].split('.GZ')[0]
        outDoc = os.path.join(outDirectory, outName)

        # Write content to the output file
        with open(outDoc, 'wb') as out:
            out.write(content)

        return True

    except Exception as e:
        print e
        return False


def __UnzipTar(inZipfile, outDirectory):
    '''
    (string, string) -> boolean

    Extracts the content of the given tar file to the given output directory.

    Returns True if the function ran successfully. Otherwise, returns False.

    Arguments:
    inZipfile -- The absolute path to the .tar from which you wish to extract
    outDirectory -- The absolute path to the output directory into which you
        wish to place the extracted content.

    Example:
    >>> Unzip('C:\\temp\\t.zip', 'C:\\temp\\mine\\t2')
    True
    '''
    try:
        import tarfile
        # Extract all items from the tar file
        with tarfile.open(inZipfile) as z:
            z.extractall(outDirectory)

        return True

    except Exception as e:
        print e
        return False



def UnzipAll(directory, outputDirectory):
    '''
    (str, str) -> boolean

    Unzips all the .zip files and/or .gz files in the passed directory.

    Arguments:
    directory -- The path to the directory containing the zip files.
    outputDirectory -- The path to the directory in which you wish to place
        the unzipped contents.
    '''
    # store the original working directory, in order to revert to it before
    # returning
    oDir = os.getcwd()

    try:
        # change to the passed directory
        os.chdir(directory)
        # List all zip files in the directory
        zs = [i for i in os.listdir(directory) if i.lower().endswith('.zip') or i.lower().endswith('.gz') or i.lower().endswith('.tar')]
        print zs
        # for each zip file
        for z in zs:
            # unzip it to the output directory
            Unzip(z, outputDirectory)
        return True
    except:
        pass
        return False
    finally:
        os.chdir(oDir)

    return False




#####################
## Add a file to an existing zip archive
def AddToZipfile(inputZipfile, inputFile, outputFolder=''):
    '''
    (string, string, [string]) -> boolean

    Adds the input file to the input zipfile.

    Returns True if the function ran successfully. Otherwise, returns False.

    Arguments:
    inputZipfile -- The absolute path of a zipfile to which you wish to add a
        file. If the zipfile does not yet exist, it will be created.
    inputFile -- The file you wish to add to the zipfile
    outputFolder -- An optional parameter to specify a subdiretory or set of
        subdirectories to which you wish to add the file. If the directories do
        not exist, they will be created.

    Examples:
    >>> AddToZipfile('C:\\temp\\t.zip', 'C:\\temp\\TestFolder\\tables.py', 'flurb\\durf')
    True
    >>> AddToZipfile('C:\\temp\\t.zip', 'C:\\temp\\TestFolder\\tables.py')
    True
    '''
    try:
        # Ensure that the archive file is a zipfile
        if inputZipfile.endswith('.zip') is False:
            print 'The zip file that you passed to the AddToZipfile() function is not actually a zip file.'
            print "The 'zip' file you passed was %s." % inputZipfile
            return False
        # If the output file already exists, set method to append;
        if os.path.exists(inputZipfile):
            method = 'a'
        # otherwise, set the method to write
        else:
            method = 'w'

        # Create the zip object
        zipObj = zipfile.ZipFile(inputZipfile, method, zipfile.ZIP_DEFLATED, allowZip64=True)

        try:
            # Output path to be used within the zipfile
            outPath = os.path.join(outputFolder, os.path.basename(inputFile))

            # Write the file to the zipfile
            zipObj.write(inputFile, outPath)

        except Exception as e:
            print e
            # In case of exception, return False
            return False

        # Be sure to close the zip object to prevent locking
        finally:
            zipObj.close()

    except Exception as e:
        print e
        return False

    # Return True if the function completed successfully.
    return True



#####################
## Main function
def __main():
    pass



## If the module is run directly, call the main function
if __name__ == '__main__':
    __main()
