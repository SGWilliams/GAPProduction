## Module for converting between measurement units.


def AsNumber(i):
    '''
    (any) -> number/boolean

    Casts the input as a number, if possible, and returns the numeric version.
        If the input is boolean, then 1 will be returned for True and 0 will be
          returned for False
        If the input cannot be cast as a number, False will be returned.
    '''
    # If the user passed a boolean...
    if type(i) is bool:
        # If it's true, return 1; if false, return 0
        if i:
            return 1
        else:
            return 0
    # If the user passed any type of number...
    if isinstance(i, (int, long, float, complex)):
        # Return the number
        return i
    # Otherwise,
    else:
        # Try to cast the passed value as a float
        try:
            n = float(i)
            # Return the float
            return n
        # If the value cannot be cast as a float
        except:
            # Return False
            return False


def CellsToHectares(cellCount):
    '''
    (number) -> number

    Returns the area, in hectares, of the passed cell count.

    NOTE: this is only applies to 30 meter * 30 meter cells.

    Argument:
    cellCount -- The number of 30 meter by 30 meter raster cells.
    '''
    # Cast the passed value as a number
    n = AsNumber(cellCount)
    # If a legitimate number was returned
    if n:
        # Calculate the hectare area of the cells, and return that value
        return (n*0.09)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def CellsToSqMiles(cellCount):
    '''
    (number) -> number

    Returns the area, in square miles, of the passed cell count.

    NOTE: this is only applies to 30 meter * 30 meter cells.

    Argument:
    cellCount -- The number of 30 meter by 30 meter raster cells.
    '''
    # Cast the passed value as a number
    n = CellsToHectares(cellCount)
    # If a legitimate number was returned
    if n:
        # Calculate the hectare area of the cells, and return that value
        return HectaresToSqMiles(n)
    # If the passed value is not a legitimate number
    else:
        # Return
        return 0


def CellsToSqMeters(cellCount):
    '''
    (number) -> number

    Returns the area, in square meters, of the passed cell count.

    NOTE: this is only applies to 30 meter * 30 meter cells.

    Argument:
    cellCount -- The number of 30 meter by 30 meter raster cells.
    '''
    # Cast the passed value as a number
    n = AsNumber(cellCount)
    # If a legitimate number was returned
    if n:
        # Calculate the hectare area of the cells, and return that value
        return (n*900)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def CellsToAcres(cellCount):
    '''
    (number) -> number

    Returns the area, in acres, of the passed cell count.

    NOTE: this is only applies to 30 meter * 30 meter cells.

    Argument:
    cellCount -- The number of 30 meter by 30 meter raster cells.
    '''
    # Cast the passed value as a number
    n = CellsToHectares(cellCount)
    # If a legitimate number was returned
    if n:
        # Calculate the hectare area of the cells, and return that value
        return HectaresToAcres(n)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def SqMetersToHectares(sqMeters):
    '''
    (number) -> number

    Returns the area, in hectares.

    Argument:
    sqMeters -- any number, representing square meters
    '''
    # Cast the passed value as a number
    n = AsNumber(sqMeters)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*0.0001)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def HectaresToSqMeters(hectares):
    '''
    (number) -> number

    Returns the area, in square meters.

    Argument:
    hectares -- any number, representing hectares
    '''
    # Cast the passed value as a number
    n = AsNumber(hectares)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*10000)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def HectaresToAcres(hectares):
    '''
    (number) -> number

    Returns the area, in acres.

    Argument:
    hectares -- any number, representing hectares
    '''
    # Cast the passed value as a number
    n = AsNumber(hectares)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*2.4710538)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def AcresToHectares(acres):
    '''
    (number) -> number

    Returns the area, in hectares.

    Argument:
    acres -- any number, representing acres
    '''
    # Cast the passed value as a number
    n = AsNumber(acres)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n/2.4710538)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def SqMetersToAcres(sqMeters):
    '''
    (number) -> number

    Returns the area, in acres.

    Argument:
    sqMeters -- any number, representing square meters
    '''
    # Cast the passed value as a number
    n = AsNumber(sqMeters)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*0.00024710538)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def AcresToSqMeters(acres):
    '''
    (number) -> number

    Returns the area, in square meters.

    Argument:
    acres -- any number, representing acres
    '''
    # Cast the passed value as a number
    n = AsNumber(acres)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*4046.8564224)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def HectaresToSqMiles(hectares):
    '''
    (number) -> number

    Returns the area, in square miles.

    Argument:
    hectares -- any number, representing hectares
    '''
    # Cast the passed value as a number
    n = AsNumber(hectares)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*0.0038610216)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def SqMilesToHectares(sqMiles):
    '''
    (number) -> number

    Returns the area, in hectares.

    Argument:
    sqMiles -- any number, representing square miles
    '''
    # Cast the passed value as a number
    n = AsNumber(sqMiles)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*258.99881103)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def AcresToSqMiles(acres):
    '''
    (number) -> number

    Returns the area, in square miles.

    Argument:
    acres -- any number, representing acres
    '''
    # Cast the passed value as a number
    n = AsNumber(acres)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*0.0015625)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def SqMilesToAcres(sqMiles):
    '''
    (number) -> number

    Returns the area, in acres.

    Argument:
    sqMiles -- any number, representing square miles
    '''
    # Cast the passed value as a number
    n = AsNumber(sqMiles)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*639.999999)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def SqMilesToSqMeters(sqMiles):
    '''
    (number) -> number

    Returns the area, in square meters.

    Argument:
    sqMiles -- any number, representing square miles
    '''
    # Cast the passed value as a number
    n = AsNumber(sqMiles)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*2589988.1103)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def SqMetersToSqMiles(sqMeters):
    '''
    (number) -> number

    Returns the area, in square miles.

    Argument:
    sqMeters -- any number, representing square meters
    '''
    # Cast the passed value as a number
    n = AsNumber(sqMeters)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n/2589988.1103)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def MetersToMiles(meters):
    '''
    (number) -> number

    Returns the length/distance, in miles

    Argument:
    meters -- any number, representing meters
    '''
    # Cast the passed value as a number
    n = AsNumber(meters)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n/1609.344)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def MilesToMeters(miles):
    '''
    (number) -> number

    Returns the length/distance, in meters

    Argument:
    miles -- any number, representing miles
    '''
    # Cast the passed value as a number
    n = AsNumber(miles)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*1609.344)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def MilesToKilometers(miles):
    '''
    (number) -> number

    Returns the length/distance, in kilometers

    Argument:
    miles -- any number, representing miles
    '''
    # Cast the passed value as a number
    n = AsNumber(miles)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n*1.609344)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0


def KilometersToMiles(kilometers):
    '''
    (number) -> number

    Returns the length/distance, in miles

    Argument:
    kilometers -- any number, representing kilometers
    '''
    # Cast the passed value as a number
    n = AsNumber(kilometers)
    # If a legitimate number was returned
    if n:
        # Return the converted value
        return (n/1.609344)
    # If the passed value is not a legitimate number
    else:
        # Return False
        return 0
    

    
def __main():
    pass


if __name__ == '__main__':
    __main()