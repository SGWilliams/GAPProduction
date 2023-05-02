## This module facilitates common tasks for searching/manipulating text files.
##

##
## The public functions are:
##
## Write() - appends to (default) or overwrites a file with the text of the second
##      argument; creates the file and even the directories, if necessary.
##
## DocReplace() - replaces selected text in a given document; any number of text
##      replacement pairs may be submitted.
##
## GetLines() - returns a list containing the complete text of every line that
##      contains the search text
##
## SearchInFiles() - searches for the given text in the files of the given root
##      directory, including all subdirectories
##
## SearchFilenames() - searches for the given text in the filenames of a given
##      root directory, including all subdirectories
##
## SearchDirectoryNames() -- searches the given text in the directory names of
##      given root directory, including all subdirectories
##
##

import os


##################################
#### Public function to write the given text to a given document.
def Write(document, text, mode='append'):
    '''
    (string, string, [string]) -> boolean

    Writes text to a document. If necessary, the function will create the
        directories and the file itself. Ensures closure of the document.

    Returns True if the function ran successfully. Otherwise, returns False.

    Arguments:
    document -- The file to which the text will be added.
    text -- The text you wish to write to the document.
    mode -- Indicates whether you wish to append or overwrite the document. The
        only valid entries are 'Append' or 'Overwrite' (capitalization is
        irrelevant). 'Append' is the default option.
        Technically, 'a' or 'o' can be entered instead.

    Examples:
    >>> Write('mydoc.txt', 'Write this test')
    True
    >>> Write('mydoc.txt', 'Write this test', 'overwrite')
    True
    '''
    try:
        # Ensure that the user enters a valid entry for the mode
        while True:
            mode = mode.lower()
            if mode == 'a':
                mode = 'append'
            elif mode == 'o':
                mode = 'overwrite'
            if mode == 'append' or mode == 'overwrite':
                break
            else:
                mode = raw_input('The second argument to the Write function should be\neither \'append\' to add to an existing document or \'overwrite\' to\nreplace/create the file.\n\nPlease enter a valid argument: ')

        modeDict = {'append':'a', 'overwrite':'w'}

        # For the next step, you must treat the document by its absolute path,
        # in case it was passed as just the document name with the working
        # directory set
        document = os.path.abspath(document)
        # If the document's directory does not exist, create it
        if not os.path.exists(os.path.dirname(document)):
            os.makedirs(os.path.dirname(document))

        # Write the content to the output document
        with open(document, modeDict[mode]) as d:
            d.write(str(text) + '\n')

        return True

    except Exception as e:
        print 'Exception in function Write():', e
        return False



def __Replacement(oText, item):
    '''
    Private function that should only be called by other fucntions within this
    module.
    '''
    # If the item is a dictionary, replace text accordingly
    if type(item) is dict:
        for key, value in item.iteritems():
            oText = oText.replace(str(key), str(value))
    # If the item is a list or a tuple
    elif type(item) is tuple or type(item) is list:
        # If the list/tuple holds only two items, both of type string...
        if len(item) == 2 and type(item[0]) is str and type(item[1]) is str:
            # ...replace the text accordingly
            oText = oText.replace(item[0], item[1])
        # If the list is not just of two strings
        else:
            # For each item in the list...
            for subitem in item:
            # ...recursively call this __Replacement function
                oText = __Replacement(oText, subitem)
    else:
        pass

    return oText



##################################
#### Public function to apply the replace method to a given document, using
#### the given pairs of replace text.
def DocReplace(document, *replacePairs):
    '''
    (string, [tuples/dictionaries/lists]) -> boolean

    Replaces text within the given document.

    Returns True if the function ran successfully. Otherwise, returns False.

    Arguments:
    document -- The full, absolute path to the file you wish to edit.
    replacePairs -- Any number of tuples, lists, and/or dictionaries. The first
        item or key is the text you wish to replace, and the second item or
        value is the text with which you wish to replace it. All text is
        case-sensitive.
        For the sake of simplicity, I would recommend just submitting a single
        dictionary, but I wanted to make the function flexible enough that
        as-yet-unseen situations can be handled...Plus it gave me a chance to
        code my first (and therefore sloppy) recursive function (see private
        function __Replacement()). So...
        Technically, the function can handle odd combinations,
        such as lists containing dictionaries, tuples, and other lists (see
        the third example, below)...the function will search recursively through
        each list/tuple until it reaches a pair of strings or a dictionary.
        Note: The content of dictionary entries is not required to be of type
        str.

    Example:
    >>> DocReplace('test.txt', ('text', 'string'), ('test', 'trial'))
    True
    [In the above example, instances of the word 'text' are replaced by the word
    'string', and instances of 'test' are replaced by 'trial']
    >>> DocReplace('testDoc.txt', {'text':'string','test':'trial'})
    True
    >>> DocReplace('testDoc.txt', [('1', 'ONE'),{'text':'string','test':'trial'},('two', 'DOS')], ['this', 'THAT'], ('4', 'QUATTRO'), {"Test":"TEST"})
    True
    '''
    try:
        d = os.path.abspath(document)
        # If the document does not exist or is not a legitimate file, return
        # False.
        if os.path.exists(d) == False or os.path.isfile(d) == False:
            print 'The document you passed as the argument to DocReplace() does not exist or is a directory.'
            return False

        # Open and read the document
        oDoc = open(d, 'r+b')
        oText = oDoc.read()
        # For each replacement pair submitted,
        for item in replacePairs:
            # Send the text and the pair to the __Replacement function
            oText = __Replacement(oText, item)

        # Reset the cursor to the beginning of the document
        oDoc.seek(0)
        # Write the new content
        oDoc.write(oText)
        # Delete any excess content after the cursor
        oDoc.truncate()
        # Close the document
        oDoc.close()

        return True

    except Exception as e:
        print e
        return False



##################################
#### Public function to get a list of lines in a document that contain the
#### search string.
def GetLines(document, searchText):
    '''
    (string, string) -> list

    Returns a list of the text from every line that contains the search text.

    Arguments:
    document -- The full, absolute path to the document to be searched.
    searchText -- The text for which you wish to search.

    Example:
    >>> GetLines('test.txt', 'zz')
    [returns a list of strings]
    '''
    # Create an empty list
    l = []

    try:
        # If the file does not exist, notify the user and return False
        if os.path.exists(os.path.dirname(document)) is False:
            print 'The document %s does not exist.' % document
            return False

        # Open the document
        cont = open(document, 'r')

        try:
            # For each line in the document
            for line in cont.readlines():
                # If the search text is in the line
                if searchText in line:
                    # Add that line to the list
                    l.append(line.strip())

        except Exception as e:
            print 'Exception in function GetLines():', e

        finally:
            # Close the document
            cont.close()

    except Exception as e:
        print 'Exception in function GetLines():', e

    # Return the list
    return l



##################################
#### A private function that should only be called by other functions within
#### this module.
def __StandardizeExtensions(inList):
    '''
    Private function that should only be called by other functions within this
    module.
    '''
    # Initialize an empty list
    outList = []
    # For each item in the passed list...
    for item in inList:
        # If the item is a string...
        if type(item) is str:
            # If the item starts with a period...
            if item.startswith('.') == True:
                # Add it to the list
                outList.append(item)
            # If the item does not start with a period...
            else:
                # Preface the item with a period and add the combined string to
                # the list
                outList.append('.' + item)
        # If the item is not a string, just ignore it
        else:
            pass

    # Return the list
    return outList



##################################
#### A private function that should only be called by other functions within
#### this module.
def __SearchInFile(l, r, f, searchText):
    '''
    Private function that should only be called by other functions within this
    module.
    '''
    # Set the path to the file
    p = os.path.join(r, f)
    # Open the file, read it's contents, and close it
    t = open(p, 'r')
    content = t.read()
    t.close()
    # If the search string is in the contents
    if searchText in content:
        # Add the file to the list
        l.append(p)

    return l



##################################
#### Function to search for a given piece of text within the files of a given
#### directory and subdirectories
def SearchInFiles(rootDirectory, searchText, *extensions):
    '''
    (string, string, [string]) -> list

    Walks a directory, identifying files that contain the search text.

    Arguments:
    rootDirectory -- The root directory within which all files will be searched.
    searchText -- The text for which the function searches.
    *extensions -- any number of file extensions to search; if none entered,
        script will search for all files. The extensions arguments can
        technically be any combination of lists, tuples, and/or strings, with
        nesting accepted; the function will flatten any nesting to retrieve
        only the base strings from within the iterables.

    Example:
    >>> SearchInFiles('C:\\temp\\mine', 'combine', '.py', 'txt')
    ['C:\\temp\\notes.txt', 'C:\\temp\\script_one.py', 'C:\\temp\\script_four.py']
    '''
    import match_and_filter

    # Call the Flatten function to remove nested lists/tuples
    extensions = match_and_filter.Flatten(extensions)
    # If the user has entered at least one extension
    if len(extensions) > 0:
        # Call the function to standardize the extensions
        extensions = __StandardizeExtensions(extensions)

    # Initialize an empty list
    l = []
    # Walk the root directory
    for r, d, fs in os.walk(rootDirectory):
        # For each file
        for f in fs:
            # If the user has not specified any extensions
            if len(extensions) == 0:
                # Call the search function
                l = __SearchInFile(l, r, f, searchText)
            # If the user has not specified extensions
            else:
                # If the file's extension is in the extension list
                if os.path.splitext(f)[1] in extensions:
                    # Call the search function
                    l = __SearchInFile(l, r, f, searchText)
                else:
                    pass

    # Return the list of files containing the search string
    return l



##################################
#### Function to search for a given piece of text within the filenames in a given
#### directory and subdirectories
def SearchFilenames(rootDirectory, searchText):
    '''
    (string, string) -> list

    Walks a directory, identifying filenames that contain the search text.

    Arguments:
    searchText -- The text for which the function searches.
    rootDirectory -- The root directory within which all files will be searched.

    Example:
    >>> SearchFilenames('C:\\temp', 'map')
    ['C:\\temp\\rangeMap.mxd', 'C:\\temp\\myfolder\\new_map.mxd']
    '''

    # Initialize an empty list to store the matching file names
    l = []

    # Walk the directory...
    for r, d, fs in os.walk(rootDirectory):
        # For each file...
        for f in fs:
            # If the searched text is in the filename...
            if searchText in f:
                # Get the full path to the file
                p = os.path.join(r, f)
                # Add the file's path to the list
                l.append(p)

    # Return the list of matching files
    return l



##################################
#### Function to search for a given piece of text within the directory names in
#### a given directory and its subdirectories
def SearchDirectoryNames(rootDirectory, searchText):
    '''
    (string, string) -> list

    Walks a directory, identify directories that contain the search text.

    Arguments:
    searchText -- The text for which the function searches.
    rootDirectory -- The root directory within which all files will be searched.

    Example:
    >>> SearchDirectoryNames('C:\\temp', 'test')
    ['C:\\Users\\tlaxson\\Desktop\\temp\\test', 'C:\\Users\\tlaxson\\Desktop\\temp\\delete\\test', 'C:\\Users\\tlaxson\\Desktop\\temp\\delete\\test\\test2']
    '''

    # Initialize an empty list to store the matching directory names
    l = []

    # Walk the directory
    for r, d, fs in os.walk(rootDirectory):
        # For each file
        for d1 in d:
            # If the searched text is in the directory name
            if searchText in d1:
                # Get the full path to the directory
                p = os.path.join(r, d1)
                # Add the directory's path to the list
                l.append(p)

    # Return the list of matching directory names
    return l



##################################
#### Module's main function
def __main():
    pass



# If the module was run directly, call the main function
if __name__ == '__main__':
    __main()
