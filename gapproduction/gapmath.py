# This module facilitates standard math operations for which there is no simple,
# single function in Python's standard library.
#
# Public Functions:
#
# Mean() -- Returns the arithmetic mean of the values in the passed list/tuple.
#
# Median() -- Returns the median of the values in the passed list/tuple.
#
# Range() -- Returns the range of values in the passed list/tuple.
#
# Quantiles() -- Identifies the given quantiles of the values in the passed
#    list/tuple
#
# Quartiles() -- Identifies the quartiles of the values in the passed list/tuple
#
# Quintiles() -- Identifies the quintiles of the values in the passed list/tuple
#
# PartialCorrelation() -- Returns the correlation coefficient of X and Y,
#    after controlling for Z
#
# PartialCorrelation_Reg() -- Returns the correlation coefficient of X and Y,
#    after controlling for Z, based on using the residuals of an OLS regression
#
#


import os


def Mean(values):
    '''
    (list/tuple) -> float/int

    Returns the mean of the values in the passed list.

    Example:
    >>> Mean([4, 6, 7, 3])
    5
    '''
    count = len(values)
    try:
        total = float(sum(values))
        avg = total/count
        return avg
    except:
        return 'N/A'


def Average(values):
    '''
    (list/tuple) -> float/int

    Returns the mean of the values in the passed list.
    '''
    return Mean(values)


def Median(values, valueInList=False):
    '''
    (list/tuple) -> float/int

    Returns the median of the values in the passed list. If the number of values
        is odd, returns the average of the two middle values.

    Parameters:
    values -- The list of values for which you wish to calculate the median
    valueInList -- An optional, boolean parameter indicating whether you wish
        for the median to be a value from the input list. That is, if False, the
        median can be the average of the two middle values from a list
        containing an even number of values.
        For example, if False, the median of [1, 2, 3, 4] is 2.5; if True, the
        median is 3.
        By default, it is set to False.

    Examples:
    >>> Median([3, 5, 4, 6, 8, 1])
    4.5
    >>> Median([4, 7, 8, 9, 2])
    7
    >>> Median([3, 5, 4, 6, 8, 1], True)
    5
    '''
#    values.sort()
#    count = len(values)
#    if count % 2 == 0:
#        part1 = values[(count/2) - 1]
#        part2 = values[count/2]
#        median = (part1 + part2) / 2
#    else:
#        median = values[count/2]
#
#    return median
    return Quantiles(values, 2, valueInList, False)[0]


def Quartiles(values, valuesInList=False, includeMinMax=False):
    '''
    Find the quartiles of the passed list.

    See Quantiles() for additional information.

    Beware the subtle difference between these function names in this module:
      Quartiles() as in 4
        vs.
      Quintiles() as in 5
        vs.
      Quantiles() like quantum/quanta or quantitative

    The first and second are merely shortcuts to the latter, employing the
    common 4-group and 5-group splits, respectively.
    '''
    return Quantiles(values, 4, valuesInList, includeMinMax)


def Quintiles(values, valuesInList=False, includeMinMax=False):
    '''
    Find the quartiles of the passed list.

    See Quantiles() for additional information.

    Beware the subtle difference between these function names in this module:
      Quartiles() as in 4
        vs.
      Quintiles() as in 5
        vs.
      Quantiles() like quantum/quanta or quantitative

    The first and second are merely shortcuts to the latter, employing the
    common 4-group and 5-group splits, respectively.
    '''
    return Quantiles(values, 5, valuesInList, includeMinMax)


#def Quantiles(values, groupCount, includeMinMax=False):
#    values.sort()
#    count = len(values)
#    quantiles = list()
#    countPerGroup = count/groupCount
#
#    # For each value in the range of the desired quantiles
#    for x in range(1, groupCount):
#        thresholdPosition = countPerGroup * x
#        # If the count of values is a multiple of the quantile count
#        if count % groupCount == 0:
#            # Then get the average of the two values on either side of the
#            # position
#            part1 = values[thresholdPosition - 1]
#            part2 = values[thresholdPosition]
#            # Calculate the average of those two values
#            median = (part1 + part2) / 2.0
#        # If the count of values is not a multiple of the quantile count
#        else:
#            median = values[thresholdPosition]
#        # Add the quantile threshold to the list
#        quantiles.append(median)
#
#    # If the user wishes to include the minimum value, insert it at the
#    # beginning of the list
#    if includeMinMax:
#        quantiles.insert(0, min(values))
#        # Add the list's maximum value to the end of the list
#        quantiles.append(max(values))
#
#    return quantiles

def Quantiles(values, groupCount, valuesInList=False, includeMinMax=False):
    '''
    (list/tuple, int, [boolean]) -> list

    Find the values in the passed list representing the quantile thresholds, or
        boundaries between equally-sized subsets of the ordered values.

    Beware the subtle difference between these function names in this module:
      Quartiles() as in 4
        vs.
      Quintiles() as in 5
        vs.
      Quantiles() like quantum/quanta or quantitative

    The first and second are merely shortcuts to the latter, employing the
    common 4-group and 5-group splits, respectively.

    Note that there are many ways to identify (or even to define) quantiles.
    While optional parameters here provide options to specify your desired
    method, additional methods exist, so the results here may not be identical
    to those derived from another package or software.

    Arguments:
    values -- A list or tuple of the values for which you wish to calculate the
        quantiles
    groupCount -- The number of groups into which you wish to split the list;
        Note that the returned numbers represent the boundaries between the
        evenly-sized groups. This can lead to one or both of two confusing
        results:
           1) If a given value occurs many times, it may be the treshold for
               more than a single group.
           2) The number of values returned is one less than the passed
               groupCount. This is because splitting a set into, e.g., three
               equally-sized groups only requires three threshold values.
               E.g., taking all the integers from 1 to 100, and splitting them
               into three equally-sized groups, the quantiles would be ~33 and
               ~67.
    valuesInList -- An optional, boolean parameter indicating whether you wish
        for the returned values to be restricted to values occurring in the
        input list, as opposed to accepting averages of values, where the
        number of elements in the input list is not a multiple of the
        passed groupCount.
        By default, it is set to False, meaning that if the number of values in
        the passed list is evenly divisible by the groupCount, then the average
        of the two nearest values will be returned for each quantile threshold.
        For example, the median (or the quantile with a groupCount of 2) of
        the values [1, 2, 3, 4] will be 2.5.
        When set to True, the median of [1, 2, 3, 4] will be 3.
    includeMinMax -- An optional, boolean parameter, indicating whether you
        wish for the passed list's minimum and maximum values to be included in
        the returned list. By default, it is set to False, meaning that they
        will not be returned. If set to true, the first value in the returned
        list will be the minimum value from the input list, or the lower bound
        of the first quantile group, and the last value in the returned list
        will be the maximum value from the input list, or the upper bound of the
        last quantile group.

    Examples:
    >>> l = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> Quantiles(l, 4)
    [2.5, 4.5, 6.5]
    >>> Quantiles(l, 3)
    [3, 5]
    >>> l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> Quantiles(l, 3)
    [3.5, 6.5]
    >>> Quantiles(l, 3, False, True)
    [1, 3.5, 6.5, 9]
    >>> Quantiles(l, 3, True)
    [4, 7]
    '''
    values.sort()

    if valuesInList:
        quantiles = __QuantilesInList(values, groupCount)
    else:
        quantiles = __QuantilesMeansAllowed(values, groupCount)

    # If the user wishes to include the minimum value, insert it at the
    # beginning of the list
    if includeMinMax:
        quantiles.insert(0, min(values))
        # Add the list's maximum value to the end of the list
        quantiles.append(max(values))

    return quantiles


def __QuantilesInList(values, groupCount):
    '''
    Private function to identify the quantiles when the user wishes to restrict
      the results to values occurring in the input list.
    '''
    import math

    count = len(values)
    quantiles = list()

    for x in range(1, groupCount):
        fraction = (float(x)/groupCount)
        position =  fraction * (count + 1)
        position = int(math.ceil(position))

        quantiles.append(values[position - 1])

    return quantiles


def __QuantilesMeansAllowed(values, groupCount):
    '''
    Private function to identify the quantiles when the user wishes to averages
      to be calculated when the group boundaries fall between elements in the
      list.
    '''
    count = len(values)
    quantiles = list()
    countPerGroup = count/groupCount

    # For each value in the range of the desired quantiles
    for x in range(1, groupCount):
        thresholdPosition = countPerGroup * x
        # If the count of values is a multiple of the quantile count
        if count % groupCount == 0:
            # Then get the average of the two values on either side of the
            # position
            part1 = values[thresholdPosition - 1]
            part2 = values[thresholdPosition]
            # Calculate the average of those two values
            median = (part1 + part2) / 2.0
        # If the count of values is not a multiple of the quantile count
        else:
            median = values[thresholdPosition]
        # Add the quantile threshold to the list
        quantiles.append(median)

    return quantiles


def Range(values):
    '''
    (list/tuple) -> float

    Returns a value of the numeric range of the values in the given iterable.

    Example:
    >>> Range([2, 1, 5, 3])
    4
    '''
    low = min(values)
    high = max(values)
    r = high - low

    return r


def PartialCorrelation(X, Y, Z, method='pearson'):
    '''
    (list, list, list, [str]) -> float

    Calculate the partial correlation coefficient controlled for a third
        variable.
        NOTE: The scipy package must be installed for the function to execute
           properly.

    Formulas derived from:
      http://www.unc.edu/courses/2008spring/psyc/270/001/partials.html
      http://vassarstats.net/textbook/index.html - section 3a

    Arguments:
    X - A list or tuple of numbers
    Y - A list or tuple of numbers
    Z - A list or tuple of numbers, representing the variable for which you
        wish to control
    method - The correlation method you wish to use. Accepted values: pearson,
        spearman, kendall, tau. 'Kendall' and 'tau' both refer to kendall's tau
        correlation. Capitalization is irrelevant.

    Returns:
    The correlation coefficient of X and Y after controlling for Z
    '''
    import math
    from scipy import stats
    method = method.lower()
    try:
        methodDict = {'pearson':stats.pearsonr, 'spearman':stats.spearmanr, \
                  'kendall':stats.kendalltau, 'tau':stats.kendalltau}
    except:
        print 'You must have scipy installed in order to run PartialCorr().'
        return None

    try:
        rXY, p = methodDict[method](X, Y)
        rXZ, p = methodDict[method](X, Z)
        rYZ, p = methodDict[method](Y, Z)
    except:
        print 'You entered an invalid correlation method into PartialCorr().'
        return None

    numerator = rXY - (rXZ*rYZ)
    denominator = math.sqrt(1 - rXZ**2) * math.sqrt(1 - rYZ**2)
    return (numerator / denominator)


def PartialCorrelation_Reg(X, Y, Z):
    '''
    Partial correlation calculated by the residuals of an OLS regression.
    '''
    import statsmodels.api as sm
    import pandas
    from scipy import stats

    exog = sm.add_constant(pandas.DataFrame(Z))
    resids = sm.OLS(X, exog).fit().resid
    return stats.pearsonr(resids, Y)



if __name__ == '__main__':
    pass