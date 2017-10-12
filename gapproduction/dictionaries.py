## This module stores dictionaries commonly used in processing GAP data as well
## as general functions for manipulating dictionaries.
##
##
## Public functions:
##
## InvertDictionary() -- Returns a dictionary in which the keys are the values
##      from the input dictionary, and the values are a list of keys that had
##      that value in the input dictionary
##
## ReverseDictionary() -- Returns a dictionary in which the keys and values have
##      been swapped.
##
## IterableOfIterablesToDictionary() - Converts a list/tuple of lists/tuples to a
##      dictionary
##
##
## Public variables:
##
## stateDict_To_Abbr -- A dictionary in which the keys are state/territory names
##      and the values are the states' two-character postal code abbreviations.
##
## stateDict_From_Abbr -- A dictionary in which the keys are the states' two-
##      character postal code abbreviations, and the values are the state names.
##
## taxaDict -- A dictionary in which the keys are the class letter, used as the
##      the first character in the six-character GAP unique IDs for species, and
##      the values are the class common name
##
## taxaDict_Latin -- A dictionary in which the keys are the class letter, used
##      as the the first character in the six-character GAP unique IDs for
##      species, and the values are the class scientific name
##
## stateFIPS_Code_to_Name -- A dictionary in which the keys are the state FIPS
##      codes (as int) and the values are the state names
##
## stateFIPS_Name_to_Code -- A dictionary in which the keys are the state names
##      and the values are the state FIPS codes (as int)
##
## regionsDict_Num_To_Name = A dictionary in which the keys are the GAP modeling
##      regions by numerical code (as int) and the values are the names of the
##      modeling regions
##
## regionsDict_Num_To_Abbr = A dictionary in which the keys are the GAP modeling
##      regions by numerical code (as int) and the values are the abbreviations
##      of the modeling regions
##
## regionsDict_Abbr_To_Num = A dictionary in which the keys are the GAP modeling
##      region abbreviations and the values are the modeling region codes (as
##      int)
##
## regionsDict_Name_To_Num = A dictionary in which the keys are the GAP modeling
##      region names and the values are the modeling region codes (as int)
##
## regionsDict_Abbr_To_Name = A dictionary in which the keys are the GAP
##      modeling region abbreviations and the vlaues are the modeling region
##      names
##
## rangeCodesDict = A dictionary of dictionaries with a key for each GAP range map 
##      attribute and a value that's a dictionary of definitions.
##
## staffDict = A dictionary of staff's initials.

stateDict_To_Abbr = {'Alabama':'AL','Alaska':'AK','American Somoa':'AS','Arizona':'AZ',
                     'Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT',
                     'Delaware':'DE','Florida':'FL','Georgia':'GA','Guam':'GU','Hawaii':'HI',
                     'Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS',
                     'Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD',
                     'Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS',
                     'Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV',
                     'New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY',
                     'North Carolina':'NC','North Dakota':'ND','Northern Mariana Islands':'MP',
                     'Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA',
                     'Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD',
                     'Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA',
                     'Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY',
                     'Puerto Rico':'PR','Virgin Islands':'VI','District of Columbia':'DC'}

stateDict_From_Abbr = {'AS':'American Somoa','GU':'Guam','MP':'Northern Mariana Islands',
                       'MS':'Mississippi','OK':'Oklahoma','DE':'Delaware','MN':'Minnesota',
                       'IL':'Illinois','AR':'Arkansas','NM':'New Mexico','IN':'Indiana',
                       'LA':'Louisiana','TX':'Texas','WI':'Wisconsin','KS':'Kansas',
                       'CT':'Connecticut','VI':'Virgin Islands','CA':'California',
                       'WV':'West Virginia','GA':'Georgia','ND':'North Dakota',
                       'PA':'Pennsylvania','PR':'Puerto Rico','AK':'Alaska','MO':'Missouri',
                       'SD':'South Dakota','CO':'Colorado','NJ':'New Jersey','WA':'Washington',
                       'NY':'New York','NV':'Nevada','MD':'Maryland','ID':'Idaho','WY':'Wyoming',
                       'AZ':'Arizona','IA':'Iowa','MI':'Michigan','UT':'Utah','VA':'Virginia',
                       'OR':'Oregon','MT':'Montana','NH':'New Hampshire','MA':'Massachusetts',
                       'SC':'South Carolina','VT':'Vermont','FL':'Florida','HI':'Hawaii',
                       'KY':'Kentucky','RI':'Rhode Island','NE':'Nebraska','OH':'Ohio',
                       'AL':'Alabama','NC':'North Carolina','TN':'Tennessee','ME':'Maine',
                       'DC':'District of Columbia'}

stateDict_From_Abbr_CONUS = {'MS':'Mississippi','OK':'Oklahoma','DE':'Delaware','MN':'Minnesota',
                             'IL':'Illinois','AR':'Arkansas','NM':'New Mexico','IN':'Indiana',
                             'LA':'Louisiana','TX':'Texas','WI':'Wisconsin','KS':'Kansas',
                             'CT':'Connecticut','CA':'California','WV':'West Virginia',
                             'GA':'Georgia','ND':'North Dakota','PA':'Pennsylvania','MO':'Missouri',
                             'SD':'South Dakota','CO':'Colorado','NJ':'New Jersey',
                             'WA':'Washington','NY':'New York','NV':'Nevada','MD':'Maryland',
                             'ID':'Idaho','WY':'Wyoming','AZ':'Arizona','IA':'Iowa','MI':'Michigan',
                             'UT':'Utah','VA':'Virginia','OR':'Oregon','MT':'Montana',
                             'NH':'New Hampshire','MA':'Massachusetts','SC':'South Carolina',
                             'VT':'Vermont','FL':'Florida','KY':'Kentucky','RI':'Rhode Island',
                             'NE':'Nebraska','OH':'Ohio','AL':'Alabama','NC':'North Carolina',
                             'TN':'Tennessee','ME':'Maine','DC':'District of Columbia'}

taxaDict = {'a':'Amphibians', 'b':'Birds', 'm':'Mammals', 'r':'Reptiles'}

taxaDict_Latin = {'a':'Amphibia', 'b':'Aves', 'm':'Mammalia', 'r':'Reptilia'}

regionsDict_Num_To_Name = {1:'Northwest', 2:'Upper Midwest', 3:'Northeast', 4:'Southwest',
                           5:'Great Plains', 6:'Southeast'}

regionsDict_Num_To_Abbr = {1:'NW', 2:'UM', 3:'NE', 4:'SW', 5:'GP', 6:'SE'}

regionsDict_Abbr_To_Num = {'NW':1, 'UM':2, 'NE':3, 'SW':4, 'GP':5, 'SE':6}

regionsDict_Name_To_Num = {'Northwest':1, 'Upper Midwest':2, 'Northeast':3, 'Southwest':4,
                           'Great Plains':5, 'Southeast':6}

regionsDict_Abbr_To_Name = {'NW':'Northwest', 'UM':'Upper Midwest', 'NE':'Northeast', 
                            'SW':'Southwest', 'GP':'Great Plains', 'SE':'Southeast'}

stateFIPS_Code_To_Name = {1: u'ALABAMA', 4: u'ARIZONA', 5: u'ARKANSAS', 6: u'CALIFORNIA', 
                          8: u'COLORADO', 9: u'CONNECTICUT', 10: u'DELAWARE', 
                          11: u'DISTRICT OF COLUMBIA', 12: u'FLORIDA', 13: u'GEORGIA', 
                          16: u'IDAHO', 17: u'ILLINOIS', 18: u'INDIANA', 19: u'IOWA', 
                          20: u'KANSAS', 21: u'KENTUCKY', 22: u'LOUISIANA', 23: u'MAINE', 
                          24: u'MARYLAND', 25: u'MASSACHUSETTS', 26: u'MICHIGAN', 
                          27: u'MINNESOTA', 28: u'MISSISSIPPI', 29: u'MISSOURI', 
                          30: u'MONTANA', 31: u'NEBRASKA', 32: u'NEVADA', 33: u'NEW HAMPSHIRE',
                          34: u'NEW JERSEY', 35: u'NEW MEXICO', 36: u'NEW YORK', 
                          37: u'NORTH CAROLINA', 38: u'NORTH DAKOTA', 39: u'OHIO', 
                          40: u'OKLAHOMA', 41: u'OREGON', 42: u'PENNSYLVANIA', 
                          44: u'RHODE ISLAND', 45: u'SOUTH CAROLINA', 46: u'SOUTH DAKOTA', 
                          47: u'TENNESSEE', 48: u'TEXAS', 49: u'UTAH', 50: u'VERMONT',
                          51: u'VIRGINIA', 53: u'WASHINGTON', 54: u'WEST VIRGINIA', 
                          55: u'WISCONSIN', 56: u'WYOMING'}

stateFIPS_Name_To_Code = {u'VERMONT': 50, u'GEORGIA': 13, u'IOWA': 19, u'KANSAS': 20,
                          u'FLORIDA': 12, u'VIRGINIA': 51, u'NORTH CAROLINA': 37, u'NEBRASKA': 31,
                          u'NEW YORK': 36, u'CALIFORNIA': 6, u'ALABAMA': 1, u'IDAHO': 16,
                          u'DELAWARE': 10, u'TENNESSEE': 47, u'ILLINOIS': 17, u'SOUTH DAKOTA': 46, 
                          u'CONNECTICUT': 9, u'MONTANA': 30, None: 0, u'MASSACHUSETTS': 25,
                          u'NEW HAMPSHIRE': 33, u'MARYLAND': 24, u'NEW MEXICO': 35, 
                          u'MISSISSIPPI': 28, u'WYOMING': 56, u'COLORADO': 8, u'NEW JERSEY': 34,
                          u'UTAH': 49, u'MICHIGAN': 26, u'WEST VIRGINIA': 54, u'WASHINGTON': 53, 
                          u'MINNESOTA': 27, u'OREGON': 41, u'OHIO': 39, u'SOUTH CAROLINA': 45,
                          u'INDIANA': 18, u'NEVADA': 32, u'LOUISIANA': 22, u'ARIZONA': 4, 
                          u'WISCONSIN': 55, u'NORTH DAKOTA': 38, u'PENNSYLVANIA': 42, 
                          u'OKLAHOMA': 40, u'KENTUCKY': 21, u'RHODE ISLAND': 44, 
                          u'DISTRICT OF COLUMBIA': 11, u'ARKANSAS': 5, u'MISSOURI': 29, 
                          u'TEXAS': 48, u'MAINE': 23}

RangeCodesDict = {"Presence": {1: "Known/extant", 2: "Possibly present", 3: "Potential for presence", 
                               4: "Extirpated/historical presence", 
                               5: "Extirpated purposely (applies to introduced species only)",
                                6: "Occurs on indicated island chain", 7: "Unknown"},
                "Origin": {1: "Native", 2: "Introduced", 3: "Either introducted or native", 
                           4: "Reintroduced", 5: "Either introduced or reintroduced",
                           6: "Vagrant", 7: "Unkown"},
                "Reproduction": {1: "Breeding", 2: "Nonbreeding", 
                                 3: "Both breeding and nonbreeding", 4: "Unkown"},
                 "Season": {1: "Year-round", 2: "Migratory", 3: "Winter", 4: "Summer", 
                            5: "Passage migrant or wanderer", 6: "Seasonal permanence uncertain", 
                            7: "Unkown", 8: "Vagrant"}}
                
staffDict = {"mjr": "Matthew Rubino", "nmt": "Nathan Tarr", "jjl": "Jeff Lonneker",
             "tl": "Thomas Laxon", "rta": "Robert Adair", "mjb": "Matthew Rubino",
             "mbr": "Matthew Rubino", "kb": "Ken Boykin", "jla": "Jocelyn Aycrigg"}     
                
##################################
#### Function to reverse the keys and values in a dictionary
def InvertDictionary(d, listsToTuples=False):
    '''
    (dict) -> dict

    Returns a dictionary in which the keys are the values from the input
      dictionary, and the values are a list of keys that had that value in
      the input dictionary.

    Note that this differs from ReverseDictionary() in that this retains all
      information from the input dictionary (given that all values are hashable)
      and in that the output values here are always lists.

    Arguments:
    d - The dictionary that you wish to invert
    listToTuples - An optional, boolean parameter indicating whether you wish to
      convert input values that are lists into tuples so that they can be used
      as keys in the output dictionary. By default, it is set to False, meaning
      that any entry in the input dictionary that has a value that is a list will
      not be included in the output dictionary in any form. If set to true, the
      list will be converted to a tuple, and that tuple will be a key in the
      output dictionary.

    Examples:
    >>> InvertDictionary({'a':'Amphibians', 'b':'Birds', 'm':'Mammals', 'r':'Reptiles'})
    {'Amphibians':['a'], 'Birds':['b'], 'Mammals':['m'], 'Reptiles':['r']}
    >>> InvertDictionary({'one':1, 'two':2, 'dos':2, 'three':3, 'uno':1})
    {1: ['uno', 'one'], 2: ['dos', 'two'], 3: ['three']}
    '''
    if type(d) is not dict:
        print "The variable that you entered into the ReverseDictionary function is not of type 'dict'; an empty dictionary will be returned."
        return dict()

    outDict = dict()

    if not listsToTuples:
        oVs = list(set([i for i in d.values() if i.__hash__]))
        for oV in oVs:
            outDict[oV] = list()

        # For each entry in the dictionary
        for k, v in d.iteritems():
            try:
                outDict[v].append(k)
            except:
                pass
    else:
        oVs = d.values()
        for oV in oVs:
            try:
                outDict[oV] = list()
            except:
                if type(oV) is list:
                    outDict[tuple(oV)] = list()
        for k, v in d.iteritems():
            try:
                outDict[v].append(k)
            except:
                if type(v) is list:
                    outDict[tuple(v)].append(k)

    # Return the new dictionary
    return outDict


##################################
#### Function to reverse the keys and values in a dictionary
def ReverseDictionary(d):
    '''
    (dict) -> dict

    Returns a dictionary in which the keys and values have been swapped.

    Note that this function differs from InvertDictionary() in that the output
      values here are always single items and in that some information may be
      lost (given recurring values in the input dictionary).

    Values in the original dictionary that are of hashable data types are the
    only entries included in the output dictionary.

    Examples:
    >>> ReverseDictionary({'a':'Amphibians', 'b':'Birds', 'm':'Mammals', 'r':'Reptiles'})
    {'Amphibians':'a', 'Birds':'b', 'Mammals':'m', 'Reptiles':'r'}
    >>> ReverseDictionary({'b':['Birds','others'], 'm':'Mammals', 'r':('Reptiles','and more'), 'f':38, 24:'Twenty-four'})
    {('Reptiles', 'and more'): 'r', 'Mammals': 'm', 38: 'f', 'Twenty-four': 24}
    >>> ReverseDictionary({'one':1, 'two':2, 'dos':2, 'three':3, 'uno':1})
    {1: 'one', 2: 'two', 3: 'three'}
    '''
    if type(d) is not dict:
        print "The variable that you entered into the ReverseDictionary function is not of type 'dict'; an empty dictionary will be returned."
        return {}

    # Initialize empty lists to temporarily store the dictionary's keys and values
    list1 = []
    list2 = []

    # For each entry in the dictionary
    for i, j in d.iteritems():
        # Check that the value is hashable, otherwise trying to set a key as
        # hashable results in a type error.
        if j.__hash__:
            # If the value is hashable, add the key and value to their
           # respective lists
            list1.append(i)
            list2.append(j)

    # Initialize an empty dictionary to store the reversed values
    nD = dict()

    # If there are items in the temp list
    if len(list2) > 0:
        # for each item in the list:
        for i in range(len(list2)):
            # Create new dictionary entries
            nD[list2[i]] = list1[i]

    # Return the new dictionary
    return nD


def IterableOfIterablesToDictionary(lot, itemsInKey=1):
    '''
    (list/tuple, integer) -> dictionary

    Converts a list/tuple of lists/tuples to a dictionary, in which the key is
        the first item from each tuple, and the value is the second item. If a
        tuple holds more than two items, the value is a tuple of all the
        remaining items.
        The optional parameter 'itemsInKey', takes an integer of the number of
            items to be joined in a tuple as the key.

    Arguments:
    lot -- A list/tuple of lists/tuples.
    itemsInKey -- An optional integer parameter indicating the number of items
        you wish to hold in the dictionary's keys. Items are taken from the
        beginning of the list and are stored in the key as a tuple.

    Example:
    >>> myList1 = [(1, 13204036), (2, 47693447), (3, 97988818), (4, 386758918)]
    >>> IterableOfIterablesToDictionary(myList1)
    {1: 13204036, 2: 47693447, 3: 97988818, 4: 386758918}
    >>> myList2 = [(1, 'summer', 13204036), (2, 'summer', 47693447), (3, 'winter', 97988818), (4, 'winter', 386758918)]
    >>> IterableOfIterablesToDictionary(myList2)
    {1: ('summer', 13204036), 2: ('summer', 47693447), 3: ('winter', 97988818), 4: ('winter', 386758918)}
    >>> IterableOfIterablesToDictionary(myList2, 2)
    {(4, 'winter'): 386758918, (1, 'summer'): 13204036, (2, 'summer'): 47693447, (3, 'winter'): 97988818}
    >>> myList3 = [(1, 'summer', 'testVal', 13204036), (2, 'summer', 47693447), (3, 'winter', 'testVal', 97988818), (4, 'winter', 386758918)]
    >>> IterableOfIterablesToDictionary(myList3, itemsInKey = 2)
    {(4, 'winter'): 386758918, (1, 'summer'): ('testVal', 13204036), (2, 'summer'): 47693447, (3, 'winter'): ('testVal', 97988818)}
    '''

    dict = {}

    n = itemsInKey + 1
    breakIndexLeft = itemsInKey - 1
    breakIndexRight = itemsInKey

    # For each
    for i in lot:
        if itemsInKey == 1:
            if len(i) == n:
                dict[i[breakIndexLeft]] = i[breakIndexRight]
            elif len(i) > n:
                dict[i[breakIndexLeft]] = tuple(i[breakIndexRight:])
        elif itemsInKey > 1:
            if len(i) == n:
                dict[tuple(i[0:itemsInKey])] = i[itemsInKey]
            elif len(i) > n:
                dict[tuple(i[0:itemsInKey])] = tuple(i[itemsInKey:])

    return dict


def StateFIPSDict(stateKeys=False):

    if stateKeys:
        return stateFIPS_Name_To_Code
    else:
        return stateFIPS_Code_To_Name

