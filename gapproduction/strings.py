import re
import collections

def GapCase(spCode : str) -> str:
    '''
    Returns an input string in the Gap Code capitalization

    Parameters
    ----------
    spCode : the species' unique GAP ID

    Returns
    -------
    spCode : the GAP ID in the Gap Code capitalization

    Example:
    >>> GapCase('bbaeax')
    bBAEAx
    >>> GapCase('BbAEax')
    bBAEAx
    >>> GapCase('BBAEAX')
    bBAEAx
    '''

    spCode = spCode[0].lower() + spCode[1:5].upper() + spCode[5].lower()

    return spCode

def LegalChars(inText):
    '''
    (str) -> str

    Returns the passesd string with all non-numeric and non-alphabetical
      characters (except for underscores) removed/replaced.

    Note that runs of multiple "illegal" characters will be processed to replace
      the entire run with just a single underscore.

    Argument:
    inText -- The string from which you wish to remove "illegal" characters

    Example:
    >>> gap.match_and_filter.LegalChars('Flurbington*87$##@, durfington---""!')
    'Flurbington_87_durfington_'
    '''
    t = inText.strip()

    badChars = [',', '.', "'", '/', '"', ' ', '\n', '\t', '-', '(', ')', '*', \
                '#', '@', '$', '^', '&', '!', '+', '=', '\\', '{', '}', '[', \
                ']', ':', ';', '?', '>', '<', '~', '`']
    for x in badChars:
        t = t.replace(x, '_')

    t = re.sub(r'\W+', '', t)
    #t = re.sub(r'[a-zA-Z0-9_]', '',

    t = RemoveRepeats(t, '_')

    return t


def RemoveRepeats(inText, searchString):
    '''
    (str, str) -> str

    Returns a processed version of the input string from which adjacent,
      repeating occurrences of the search string have been removed

    Arguments:
    inText -- The input string to be processed
    searchString -- The sub-string, adjacent duplicates of which will be removed
        from the inText

    Example:
    >>> RemoveRepeats('fflurbinngtoned ddurfingtoneddd blah', 'd')
    'fflurbinngtoned durfingtoned blah'
    >>> RemoveRepeats('In the the CONUS extent, the data were processed', 'the ')
    'In the CONUS extent, the data were processed'
    '''
    double = '{0}{0}'.format(searchString)
    while True:
        if double in inText:
            inText = inText.replace(double, searchString)
        else:
            break
    return inText


def FilterList(inputList, searchString, regex=r'[\s\S]*'):
    '''
    (list, string) -> list

    Returns a list containing all items from the input list that contain the
        input search string.

    Arguments:
    list -- A list of strings to be filtered.
    searchString -- The string to search for in the input list; asterisks are
        treated as one or more characters.
    regex -- An optional parameter to set your own regular expression to replace
        asterisks in the search string. By default, the expression will treat
        the user's asterisks as any or no characters, including spaces, numbers,
        punctuation, etc. For example, if you wanted to omit items that contain
        spaces, you would set regex='[\S]*'. If you wish to include only items
        that are comprised entirely of letters, you would set regex='[a-zA-Z]*'.
        For examples of regular expressions and the meanings of them, see:
        http://gskinner.com/RegExr/?30ote and
        https://developers.google.com/edu/python/regular-expressions

    Example:
    >>> l = ['bbaeax', 'mnarox', 'mnarop', 'rflapn', 'bbxaox', 'bbxaor', 'bbaeaf', 'xflurb']
    >>> FilterList(l, 'x')
    []
    >>> FilterList(l, '*x')
    ['bbaeax', 'mnarox', 'bbxaox']
    >>> FilterList(l, '*x*')
    ['bbaeax', 'mnarox', 'bbxaox', 'bbxaor', 'xflurb']
    >>> FilterList(l, 'x*')
    ['xflurb']
    '''

    # Convert the search string into a regular expression, beginning it with a
    # string begin character, replacing asterisks with the code to search for
    # any number of characters and ending with a string end character.
    wc = '^' + searchString.replace('*', regex) + '$'

    # Initialize an empty list to store the results
    newList = []

    # For each item in the input list
    for i in inputList:
        # If the item is a valid string
        if isinstance(i, basestring):
            # Ignore capitalization
            iTemp = i.lower()
            # If the string matches the search string
            if re.match(wc, iTemp):
                # Add the string to the output list
                newList.append(i)

    # Return the new list
    return newList


def __FlattenGenerator(iterable):
    '''
    A private function that should only be called from other
        functions within this module.
    '''
    # For each item in the passed iterable
    for item in iterable:
        # If the item is iterable and is not a string
        if isinstance(item, collections.Iterable) and not isinstance(item, basestring):
            # Recursively call this function to return sub-subitems
            for sub in __FlattenGenerator(item):
                yield sub
        # Otherwise, if the item is not iterable or is a string, return the item
        else:
            yield item


def Flatten(iterable):
    '''
    (list/tuple) -> list

    Returns a 'flattened' list containing all the elements of the passed,
        nested list/tuple of lists/tuples/dictionaries. Note that
        if the passed argument contains dictionaries, the keys only
        are included in the flattened list.

    Argument:
    iterable -- Any list or tuple, including those that contain any
        configuration of nested lists/tuples/dictionaries.

    Example:
    >>> l=([[['test', 'test2'],[('test3')],[1, 3]], {'x':'24', 'z':'26'}])
    >>> Flatten(l)
    ['test', 'test2', 'test3', 1, 3, 'x', 'z']
    '''

    if isinstance(iterable, collections.Iterable) and not isinstance(iterable, basestring):
        outList = list(__FlattenGenerator(iterable))
    else:
        outList = [iterable]

    return outList


def __main():
    pass


if __name__ == '__main__':
    __main()
