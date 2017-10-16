## Module for retrieving information about ArcGIS web services
##
##
## ListServices() -- Returns a list of the services within the given directory.
##
## MissingServices() -- Returns a list of GAP species codes for species that are
##      published but that do not have map services published on the
##      gis1.usgs.gov server.
##
##
##
##


import urllib, gapdb


def __GetNextFolder(page):
    # Find the folder:
    startPoint = page.find('href=')
    # If the startPoint is not found,
    if startPoint == -1:
        # Return None
        return None, 0, 0
    # Find the start of the folder
    start = page.find('>', startPoint) + 1
    # Find the end of the folder
    end = page.find('<', start)
    # Populate the snowfall variable
    fName = page[start:end]
    # Return the folder name and the end position
    return fName, end


def __GetFolders(page):
    fs = []
    # Until GetNext returns no data:
    while True:
        # Gets a folder and the end position
        tup = __GetNextFolder(page)
        # If getNext returned legitimate data:
        if len(tup) == 2:
            # Assign the folder and end position
            fs.append(tup[0])
            endPos = tup[1]
            # Set the page to start at the end of the most recent data:
            page = page[endPos:]
        # If the getNextHeader returned illegitimate data:
        else:
            return fs
    return fs


def __openURL(url):
    # Set the page as the source code for the station's page
    return urllib.urlopen(url).read()


def __FoldersSection(content):
    # If the page contains folders...
    if "Folders:" in content:
        # Set the start and end points
        start = content.find('Folders:')
        end = content.find('</ul', start)
        # Return the relevant portion of the page
        return content[start:end]
    else:
        return None


def __Walk(content):
    # Get the relevant excerpt
    fSection = __FoldersSection(content)
    # If there isn't any relevant page section, return a blank list
    if type(fSection) is not str:
        return []
    # Return a list of sub-folders
    return __GetFolders(fSection)



def __ServicesSection(content):
    # If there are services on the page
    if "Services:" in content:
        # Set the start and end points
        start = content.find('Services:')
        end = content.find('</ul', start)
        # Return the excerpt from the page
        return content[start:end]
    else:
        return None


def __GetNextService(page):
    # Find the folder:
    signal = "/rest/services/"
    startPoint = page.find(signal)
    # If the startPoint is not found,
    if startPoint == -1:
        # Return None
        return None, 0, 0
    # Find the start of the folder
    startPoint = startPoint + len(signal) + 1
    start = page.find('/', startPoint) + 1
    # Find the end of the folder
    end = page.find('"', start)
    # Populate the service name variable
    fName = page[start:end]
    # Return the folder name and the end position
    return fName, end


def __GetServices(page):
    fs = []
    # Until GetNext returns no data:
    while True:
        # Gets a folder and the end position
        tup = __GetNextService(page)
        # If getNext returned legitimate data:
        if len(tup) == 2:
            # Assign the folder and end position
            fs.append(tup[0])
            endPos = tup[1]
            # Set the page to start at the end of the most recent data:
            page = page[endPos:]
        # If the getNextService returned illegitimate data:
        else:
            return fs



def ListServices(url, serviceWildcard='', folderWildcard='', searchFolders=True):
    '''
    (string, [string], [string], [boolean]) -> list

    Returns a list of the services within a given directory.

    Arguments:
    url -- The full url to the directory.
    serviceWildcard -- An optional parameter to indicate text that must be
        within a service's name for that service to be included in the output
        list.
    folderWildcard -- An optional parameter to indicate text that must be
        within a sub-directory's name for that sub-directory to be searched.
    searchFolders -- An optional, boolean parameter, indicating whether you wish
        to search for services within sub-directories. By default, this is set
        to True, meaning that sub-directories will be searched.

    Examples:
    >>> ListServices('http://gis1.usgs.gov/ArcGIS/rest/services')

    >>> ListServices('http://gis1.usgs.gov/ArcGIS/rest/services', 'x', 'birds')

    '''
    # Open the page's source code
    content = __openURL(url)
    # Create a list to store the directories, and put the base url in it.
    dirs = [url]
    # If the user opted to search subfolders...
    if searchFolders == True:
        # Get a list of the subfolders and concatenate each with the base url
        subDirs = [url + '/' + i for i in (__Walk(content)) if folderWildcard.lower() in i.lower()]
        # Merge the two lists
        dirs = dirs + subDirs

    # Create a blank list to store the service urls
    allServices = []

    # For each directory
    for d in dirs:
        # Open the folder's source code
        content = __openURL(d)
        # Extract the relevant section of code
        sSection = __ServicesSection(content)
        # Create a list of the services concatenated with the directory's url
        services = [d + '/' + i for i in __GetServices(sSection) if serviceWildcard.lower() in i.lower()]
        # Merge the lists
        allServices = allServices + services

    # Return the final list of web services
    return allServices



def MissingServicesOriginal():
    '''
    () -> list

    Returns a list of GAP species codes for species that are published but
        that do not have map services published on the gis1.usgs.gov server.
    '''
    # A list of all species with published models
    comp = [i.lower() for i in gapdb.SppModelCompleted()]

    # A list of all the services in folders containing the text 'species'
    # within the gis1.usgs.gov server
    services = ListServices('http://gis1.usgs.gov/ArcGIS/rest/services', '', 'species')
    # Grabs the species' codes from the services
    services = [i.split('/')[-2].lower() for i in services if 'Species' in i]

    # A new empty list
    inc = []
    # For each completed species code
    for i in comp:
        # If the code is not in the list of available services
        if i not in services:
            # Append that code to the new list
            inc.append(i)

    # Return the list of species codes for published species that do not have a
    # service on gis1.usgs.gov
    return inc


def MissingServices():
    '''
    () -> list

    Returns a list of GAP species codes for species that are published but
        that do not have map services published on the gis1.usgs.gov server.
    '''
    # A list of all species with published models
    comp = [i.lower() for i in gapdb.SppModelCompleted()]

    # A list of all the services in folders containing the text 'species'
    # within the gis1.usgs.gov server
    services = []
    amphServices = ListServices(r'http://gis1.usgs.gov/arcgis/rest/services/NAT_Species_Amphibians')
    repServices = ListServices(r'http://gis1.usgs.gov/arcgis/rest/services/NAT_Species_Reptiles')
    mamServices = ListServices(r'http://gis1.usgs.gov/arcgis/rest/services/NAT_Species_Mammals')
    birdServices = ListServices(r'http://gis1.usgs.gov/arcgis/rest/services/NAT_Species_Birds')
    for ss in [amphServices, repServices, mamServices, birdServices]:
        services.extend(ss)

    # Grabs the species' codes from the services
    services = [i.split('/')[-2].lower() for i in services if 'Species' in i]

    # A new empty list
    inc = []
    # For each completed species code
    for i in comp:
        # If the code is not in the list of available services
        if i not in services:
            # Append that code to the new list
            inc.append(i)

    # Return the list of species codes for published species that do not have a
    # service on gis1.usgs.gov
    return inc


##################################
#### Module's main function
def __main():
    pass


# If the module was run directly, call the main function
if __name__ == '__main__':
    __main()
