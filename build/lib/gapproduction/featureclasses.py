## This module contains functions to facilitate the processing of feature
## classes (shapefiles and geodatabase feature classes).
##
## Public Functions:
##
## UseDACursor() -- Returns a boolean indicating whether the current system
##      supports the data access module.
##
## ListValues() -- Return a list of all the values that occur in the given field
##      in a feature class.
##
## CountOccurrencesOfValue() -- Counts the number of times that the given value
##      occurs in the given field in the feature class.
##
## CountOccurrencesOfAllValues() -- Returns a dictionary within which the keys
##      represent each unique value found in the field and the values
##      represent the number of times that each value is found in the attribute
##      table.
##
## FindDuplicateValues() -- Returns a list of values that occur multiple times
##      in the given field.
##
## DeleteDuplicates() -- Delete records that share a value with another record.
##      NOTE: This function will delete every matching record, not just the
##      second and subsequent occurrences of the value.
##
## FieldsDictionary() -- Creates a dictionary where the keys and values are
##      the field values from the passed fields for each record in the table/
##      feature class. The key field must be a unique identifier to retain all
##      data.
##
## FieldsDictionary_Inverse() -- Creates a dictionary where the keys and values
##      are the field values from the passed fields for each record in the
##      table/feature class. Differs from FieldsDictionary() in that, here, the
##      keys do not need to be unique identifiers. Also, can only address a
##      single value field. Furthermore, the returned dictionary values are
##      lists.
##
## ListFromTable() -- Creates a list of lists. Each sub-list contains the values
##     for a row in the input table/feature class.
##
## ListFields() -- Creates of a list of field names from the passed layer
##
## SetNulls() -- In the given attribute field(s), sets all Null values
##	to match the passed value.
##
## ReplaceValue() -- In the given attribute field(s), sets all
##	occurrences of the given value/string to match the new value/string
##
## ReplaceValues() -- In the given attribute field(s), sets all
##	occurrences of any of the given values/strings to match the new value/string
##
## ReplaceValuesFromDict() -- In the given attribute field, updates
##	occurrences of any of the dictionary's keys to match the key's corresponding value
##
## AttributeTableToCsv() - Exports the attribute table from the passed
##      shapefile, feature class, raster, or geodatabase table to a csv.
##
## DomainAsDictionary() -- Returns the field's coded attribute domain as a
##      dictionary, in which the keys are the codes and the values are the coded
##      strings.
##
## RenameField() -- Renames the passed attribute field.
##
## CopyValues() -- For each feature in the feature class, copies the values from
##	one field to another.
##
## ChangeFieldLength() -- Change the length property of a text field in the
##	attribute table.
##
## GetMaxLength() -- Get the number of characters in the longest value from the
##      passed field. If multiple fields are passed, returns the number of
##      of characters in the longest concatenated string of values.
##
## ConcatenateFields() -- For each feature/row, concatenates the values in the
##	passed fields to the output field, optionally adding a user-defined
##	separator between each value.
##
## GetLinearUnit() -- Identify the linear unit of the feature class' spatial
##      reference.
##
## SummarizeXByY_Area() -- Summarize the area and proportion area of features
##      in the X column by features in the Y column. Writes output to a csv.
##
import os, tables

try:
    import arcpy
    def UseDACursor():
        '''
        Returns a boolean, indicating whether the current system can support data
        access cursors
        '''
        try:
            # Get the ArcGIS for Desktop version number
            arcVersion = arcpy.GetInstallInfo()['Version']
            # If the version is greater than or equal to 10.1
            if arcVersion >= '10.1':
                # Return True
                return True
        except:
            pass
        # Return False
        return False
    
    
    # A private, boolean variable, indicating whether the current system supports
    # the data access module.
    __daCursor = UseDACursor()
    
    
    
    def __FieldExists(featureClass, field):
        '''
        A private function to be called only by other functions within this module.
    
        Returns a boolean indicating whether the field exists in the passed feature
            class.
        '''
        # A list of special, 'hidden' field names.
        specials = ['SHAPE@XY', 'SHAPE@TRUECENTROID', 'SHAPE@X', 'SHAPE@Y', \
                    'SHAPE@Z', 'SHAPE@M', 'SHAPE@JSON', 'SHAPE@WKB', 'SHAPE@WKT', \
                    'SHAPE@', 'SHAPE@AREA', 'SHAPE@LENGTH', 'OID@']
        # If the field is one of those special fields, return True
        if field in specials:
            return True
    
        # Get a list of the feature class' fields
        fields = arcpy.ListFields(featureClass)
    
        # For each field
        for f in fields:
            # If the field's name matches the passed field name
            if f.name == field:
                # Return True
                return True
        # If no matches were found, return False
        return False
    
    
    
    def ListValues(featureClass, field, unique=False):
        '''
        (str, str, [boolean]) -> list
    
        Return a list of all the values that occur in the given field in a feature
            class.
    
        Arguments:
        featureClass -- The path to the feature class you wish to assess.
        field -- The name of the field within which you want to find values.
        unique -- An optional boolean, indicating whether you wish to remove repeated
            values. By default, it is set to False, indicating that duplicates will
            not be reduced.
    
        Example:
        >>> ListValues('bbaeax_range.shp', 'season', True)
        [1, 3, 4]
        '''
        try:
            # If the passed field exists...
            if __FieldExists(featureClass, field):
                # If the system supports the data access module...
                if __daCursor:
                    # Call the matching function to get all values
                    values = __ListValues_da(featureClass, field)
                # Otherwise, if the system does not support the data access module...
                else:
                    # Call the matching function to get all values
                    values = __ListValues_nonDA(featureClass, field)
    
                # If the user opted to return only unique values...
                if unique:
                    # Remove duplicate items in the list
                    values = list(set(values))
    
                # Return the list of values
                return values
    
            else:
                raise Exception('No field matches the field name %s in %s.' % (field, featureClass))
    
        except Exception as e:
            print 'Error in function ListValues():'
            print e
    
    
    def __ListValues_da(featureClass, field):
        '''
        A private function to be called only by other functions within this module.
    
        Lists the values in the passed feature class' passed field, using the data
            access module.
        '''
        # Initialize an empty list to store the values
        values = []
        # Create a cursor
        rows = arcpy.da.SearchCursor(featureClass, field)
    
        # For each row...
        for row in rows:
            # Add its value to the list
            values.append(row[0])
    
        # Delete the cursor
        del rows
        # Return the list of values
        return values
    
    
    def __ListValues_nonDA(featureClass, field):
        '''
        A private function to be called only by other functions within this module.
    
        Lists the values in the passed feature class' passed field, not using the
            data access module.
        '''
        # Initialize an empty list to store the values
        values = []
        # Create a search cursor
        rows = arcpy.SearchCursor(featureClass)
    
        # For each row...
        for row in rows:
            # Add the row's value to the list
            values.append(row.getValue(field))
    
        # Delete the cursor
        del rows
    
        # Return the list of values
        return values
    
    
    
    def CountOccurrencesOfValue(featureClass, searchField, value):
        '''
        (str, str, str/number) -> int
    
        Counts the number of times that the given value occurs in the given field
            in the feature class.
    
        Arguments:
        featureClass -- The path to the feature class in which you wish to search.
        searchField -- The name of the field in which you wish to search.
        value -- The value for which you wish to generate a count.
    
        Examples:
        >>> CountOccurrencesOfValue('bbaeax_range.shp', 'season', 3)
        22347
        >>> CountOccurrencesOfValue('bbsRoutes', 'rtename', 'WHITEHOUSE')
        6
        '''
        try:
            # Check that the passed field name exists; if so...
            if __FieldExists(featureClass, searchField):
                # Initialize a count at zero
                count = 0
                # If the system can support data access cursors...
                if __daCursor:
                    count = __CountOccurrences_da(featureClass, searchField)
                # Otherwise, if the system cannot support data access cursors...
                else:
                    count = __CountOccurrences_nonDA(featureClass, searchField)
                # Return the count
                return count
    
            # If the field does not exist...
            else:
                # Notify the user
                raise Exception('No fied matches the field name %s in %s.' % (searchField, featureClass))
    
        except Exception as e:
            print 'Error in function CountOccurrencesOfValue:'
            print e
    
    
    def __CountOccurrences_da(featureClass, searchField):
        # Create a search cursor
        rows = arcpy.da.SearchCursor(featureClass, searchField)
        # For each row...
        for row in rows:
            # If the row's value equals the passed value...
            if row[0] == value:
                # Increment the count by one
                count += 1
        # Delete the cursor
        del rows
    
        return count
    
    
    def __CountOccurrences_nonDA(featureClass, searchField):
        # Create a search cursor
        rows = arcpy.SearchCursor(featureClass)
        # For each row...
        for row in rows:
            # If the row's value equals the passed value...
            if row.getValue(searchField) == value:
                # Increment the count by one
                count += 1
        # Delete the cursor
        del rows
    
        return count
    
    
    def CountOccurrencesOfAllValues(featureClass, searchField):
        '''
        (str, str) -> dict
    
        Returns a dictionary, within which the keys represent each unique value
            found in the field, and the values represent the number of times that
            each value is found in the attribute table.
    
        Arguments:
        featureClass -- The path to the feature class.
        searchField -- The name of the field for which you wish to return the counts.
    
        Example:
        >>> CountOccurrencesOfAllValues('bbaeax.shp', 'season')
        {1:24009, 3:17859, 4:22347}
        '''
    
        try:
            # Get a list of all the values that occur in the field
            values = ListValues(featureClass, searchField, unique=True)
    
            # Initialize an empty dictionary to store the counts for each value
            vDict = {}
    
            # For each value that occurs in the field...
            for v in values:
                # Create a dictionary entry for the value, and set it to zero
                vDict[v] = 0
    
            # If the system support da cursors...
            if __daCursor:
                # Create a cursor
                rows = arcpy.da.SearchCursor(featureClass, searchField)
                # For each row...
                for row in rows:
                    # Get the value
                    v = row[0]
                    # Increment that value's dictionary value by 1
                    vDict[v] += 1
                # Delete the cursor
                del rows
            # If the system does not support the data access module...
            else:
                # Create a cursor
                rows = arcpy.SearchCursor(featureClass)
                # For each row...
                for row in rows:
                    # Get the value...
                    v = row.getValue(searchField)
                    # Increment that value's dictionary value by 1
                    vDict[v] += 1
                # Delete the cursor
                del rows
    
            # Return the dictionary
            return vDict
    
        except Exception as e:
            print 'Error in CountOccurrencesOfAllValues:'
            print e
    
    
    
    def FieldsDictionary(featureClass, keyField, valueFields):
        '''
        (str, str, str/list/tuple) -> dict
    
        Return a dictionary of the key field and value field(s).
    
        Arguments:
        featureClass -- The path to the feature class you wish to assess.
        keyField -- The name of the field of which the values will serve as the
            dictionary's keys.
        valueFields -- The name of the field of which the values will serve as the
            dictionary's values; or a list/tuple of fields that will serve as the
            dictionary's values.
    
        Examples:
        >>> FieldsDictionary(lyr, 'ComID', 'AreaSqKM')
        {2664067: 3.0059999999999998, 2663939: 1.962, 2664085: 3.6143999999999998, 2665683: 0.027900000000000001}
        >>> FieldsDictionary(lyr, 'ComID', ['AreaSqKM', 'Hydroseq', 'ToNode','FromNode'])
        {2664067: [3.0059999999999998, 10089508.0, 10006216.0, 10005836.0], 2663939: [1.962, 10139601.0, 10006156.0, 10093319.0], 2664085: [3.6143999999999998, 10002250.0, 10006218.0, 10093356.0]}
        '''
        try:
    
            # If the user passed a single string as the value field:
            if isinstance(valueFields, basestring):
    
                # Verify that both fields exist
                if __FieldExists(featureClass, keyField) and __FieldExists(featureClass, valueFields):
                    # Initialize an empty dictionary
                    attDict = dict()
    
                    # If the system can handle arcpy.da cursors...
                    if __daCursor:
                        # create a list with both field names
                        fields = [keyField, valueFields]
                        # Create a search cursor
                        rows = arcpy.da.SearchCursor(featureClass, fields)
                        # For each
                        for row in rows:
                            k = row[0]
                            v = row[1]
                            # Set the key field's value as the key, and set its
                            # value field's value as the dictionary value
                            attDict[k] = v
                        # Delete the cursor
                        del rows
                    # If the system cannot handle arcpy.da cursors...
                    else:
                        print 'no da'
                        # Create a cursor
                        rows = arcpy.SearchCursor(featureClass)
                        # For each record...
                        for row in rows:
                            # Get the key
                            k = row.getValue(keyField)
                            # Get the value
                            v = row.getValue(valueFields)
                            # Create the new dictionary entry
                            attDict[k] = v
                        # delete the cursor
                        del rows
    
                    # Return the dictionary
                    return attDict
    
                else:
                    raise Exception('No field matches one or both of the passed field names: %s and/or %s.' % (keyField, valueFields))
    
            # If the user did not pass a single string for the value fields...
            else:
                # If the passed key field name is not in the feature class...
                if not __FieldExists(featureClass, keyField):
                    # raise an exception
                    raise Exception('The passed key field %s does not exist in the feature class %s.' % (keyField, featureClass))
                # For each passed value field...
                for valueField in valueFields:
                    # ...if the field name is not in the feature class...
                    if not __FieldExists(featureClass, valueField):
                        # raise an exception
                        raise Exception('The passed value field %s does not exist in the feature class %s.' % (valueField, featureClass))
    
                # Initialize an empty dictionary
                attDict = {}
    
                # If the system can run an arcpy.da cursor:
                if __daCursor:
                    # Create a list to store all the fields, placing the key field
                    # first
                    fields = [keyField]
                    # Add all the value fields to the list
                    fields.extend(valueFields)
                    # Create a search cursor
                    rows = arcpy.da.SearchCursor(featureClass, fields)
                    # For each row...
                    for row in rows:
                        # Set the row's key field value as the dictionary's key and
                        # set a list of the value fields' values as the dictionary's
                        # value
                        attDict[row[0]] = list(row[1:])
                    # Delete the cursor
                    del rows
                # If the system cannot run an arcpy.da cursor:
                else:
                    # Create a cursor
                    rows = arcpy.SearchCursor(featureClass)
                    # For each record...
                    for row in rows:
                        # Get the key
                        k = row.getValue(keyField)
                        # Create an empty list to store the values
                        vs = []
                        # For each value field
                        for valueField in valueFields:
                            # Get the row's value for that field...
                            v = row.getValue(valueField)
                            # ...and add that value to the value list
                            vs.append(v)
                        # Create the new dictionary entry for that row
                        attDict[k] = vs
                    # Delete the cursor
                    del rows
    
                # Return the dictionary
                return attDict
    
        except Exception as e:
            print 'Error in function FieldsDictionary():'
            print e
    
    
    
    def FieldsDictionary_Inverse(featureClass, keyField, valueField):
        '''
        (str, str, str) -> dict
    
        Returns a dictionary in which the keys are the content found in the key field
            in the given table and the values are lists of the associated values
            from the value field.
    
        NOTE: This function essentially creates the inverse of the dictionary
            created by the FieldsDictionary() function (in which the keys' values
            need to be unique identifiers). In this function, The keys need not be
            unique identifiers; nor do the values.
            This function would be applicable in a situation for which you wish to
            identify all unique ids that have a given value in a particular field.
            E.g., the keys could be county names, and the values could be
            all the states that have a county by that name.
    
        Arguments:
        featureClass -- The path to the feature class you wish to assess.
        keyField -- The name of the field of which the values will serve as the
            dictionary's keys.
        valueFields -- The name of the field of which the values will serve as the
            dictionary's values.
    
        Examples:
        >>> FieldsDictionary_Inverse(lyr, 'StreamOrde', 'ComID')
        {0: [2665693, 2665681, 2665687, 2665685], 1: [2664003, 2664019, 2663915], 2: [2664005]}
        >>> FieldsDictionary_Inverse(spRange, 'Season', 'HUC12')
        {1: [132475896547, 654876214568, 452187954236], 3: [253654856954, 154879645780], 4: [854759412546, 152315478569]}
        '''
        try:
            # Verify that both fields exist
            if __FieldExists(featureClass, keyField) and __FieldExists(featureClass, valueField):
    
                # Get a list of the unique values in the key field
                keyList = ListValues(featureClass, keyField, unique=True)
    
                # Initialize an empty dictionary
                attDict = {}
    
                # For each unique key value, create a dictionary entry, with the
                # value being an empty list
                for key in keyList:
                    attDict[key] = []
    
                # If the system can use arcpy.da cursors...
                if __daCursor:
                    # Create a list of both fields to gather
                    fields = [keyField, valueField]
                    # Create a search cursor
                    rows = arcpy.da.SearchCursor(featureClass, fields)
                    # For each feature
                    for row in rows:
                        # Get the key's current dictionary value
                        currentVal = attDict[row[0]]
                        # Add the row's value field value to the current list
                        currentVal.append(row[1])
                        # Set the key's dictionary entry to be equal to the updated
                        # list
                        attDict[row[0]] = currentVal
                    # Delete the cursor
                    del rows
    
                # If the system cannot use arcpy.da cursors
                else:
                    # Create a cursor
                    rows = arcpy.SearchCursor(featureClass)
                    # For each record...
                    for row in rows:
                        # Get the key
                        k = row.getValue(keyField)
                        # Get the value
                        v = row.getValue(valueField)
                        # Get the key's current dictionary value
                        currentVal = attDict[k]
                        # Add the row's value to the current list
                        currentVal.append(v)
                        # Set the key's dictionary entry to be equal to the updated
                        # list
                        attDict[k] = currentVal
                    # Delete the cursor
                    del rows
    
                # Return the dictionary
                return attDict
    
            else:
                raise Exception('No field matches one or both of the passed field names: %s and/or %s.' % (keyField, valueField))
    
        except Exception as e:
            print 'Error in function FieldsDictionary2():'
            print e
    
    
    
    def FindDuplicateValues(featureClass, searchField):
        '''
        (str, str) -> list
    
        Returns a list of values that occur multiple times in the given field.
    
        Arguments:
        featureClass -- The path to the feature class you wish to search.
        searchField -- The name of the field in which you wish to search.
    
        Example:
        >>> FindDuplicateValues('bbsRoutes.shp', 'rtename')
        ['WHITEHOUSE', 'GROVE HILL', 'CLAIBORNE']
        '''
        try:
            # Get a dictionary of counts for each value
            vDict = CountOccurrencesOfAllValues(featureClass, searchField)
            # Initialize an empty list to store duplicate values
            dupes = []
            # For each item in the dictionary...
            for i, j in vDict.iteritems():
                # If the item's value is greater than one
                if j > 1:
                    # Add the key to the list of duplicates
                    dupes.append(i)
    
            # Return the list of duplicate values
            return dupes
    
        except Exception as e:
            print 'Error in FindDuplicateValues():'
            print e
    
    
    
    def __SelectRecords(featureClass, query):
        '''
        A private function to be called only by other functions within this module.
    
        Select features in the passed feature class.
        '''
        # Create a feature layer of the feature class
        lyr = 'featureLyr'
        arcpy.MakeFeatureLayer_management(featureClass, lyr)
        # Clear any existing selection
        arcpy.SelectLayerByAttribute_management(lyr, 'CLEAR_SELECTION')
        # Execute the passed selection query
        arcpy.SelectLayerByAttribute_management(lyr, 'NEW_SELECTION', query)
    
        # Get a describe object for the layer
        d = arcpy.Describe(lyr)
        # If no features are selected
        if d.FIDSet == '':
            # Set the count to zero
            count = 0
        # If features were selected
        else:
            # Get the count of selected features
            count = int(arcpy.GetCount_management(lyr).getOutput(0))
    
        # Return the layer and count of selected features
        return lyr, count
    
    
    
    def DeleteDuplicates(featureClass, searchField):
        '''
        (str, str) -> None
    
        Delete records that share a value with another record.
        NOTE: This function will delete every matching record, not just the second
        and subsequent occurrences of the value. To save an arbitrary record, use
        arcpy.DeleteIdentical_management.
    
        Arguments:
        featureClass -- The path to the feature class from which you wish to delete
            duplicate records.
        searchField -- The field in which you wish to search for duplicates.
        '''
        # Get a list of values that are duplicated
        dupes = FindDuplicateValues(featureClass, searchField)
    
        # If no values are duplicated...
        if not dupes or len(dupes) < 1:
            # ...return
            return
    
        # Cast the duplicates as strings
        dupes = [str(i) for i in dupes]
    
        # Construct the query:
        # The beginning of the query
        queryPt1 = '"' + searchField + '"='
        # The query separator
        querySep = ' OR ' + queryPt1
        # Create a string that contains the duplicate values separated by the query
        # separator
        queryPt2 = querySep.join(dupes)
        # Finalize the query
        query = queryPt1 + queryPt2
    
        # Select the relevant features
        lyr, count = __SelectRecords(featureClass, query)
        # If features were selected
        if count > 0:
            # Delete the selected features
            arcpy.DeleteRows_management(lyr)
    
    
    
    def ListFromTable(table):
        '''
        Refer to tables.ListFromTable()
        '''
        headers = [i.name for i in arcpy.ListFields(table)]
    
        l = [headers]
    
        cur = arcpy.da.SearchCursor(table, '*')
        for row in cur:
            l.append(list(row))
    
        return l
    
    
    def ListFields(table):
        '''
        Refer to tables.ListHeaders()
        '''
        f = [i.name for i in arcpy.ListFields(table)]
        return f
    
    
    def SetNulls(table, fields, value=0):
        '''
        (str, str/list/tuple, [any]) -> None
    
        Sets null values to the passed value
    
        Arguments:
        table -- Path of the table to be updated
        fields -- Name of the field(s) to be updated. Note that you can pass a string
            of a single field name or a list/tuple of a single or multiple field names.
        value -- An optional parameter indicating the value with which you wish to
            replace nulls. By default it is set to zero. Note that the passed value
            must match the field type(s).
    
        Example:
        >>> SetNulls('MyShp.shp', 'My_Field')
    
        >>> SetNulls('MyShp.shp', ['My_Field'], -9999)
    
        >>> SetNulls('MyShp.shp', 'My_Field', 'No comment')
    
        >>> SetNulls('MyShp.shp', ['MyFirstField', 'MySecondField'], -9999)
    
        '''
        # If a single field name was passed
        if isinstance(fields, basestring) or len(fields) == 1:
            with arcpy.da.UpdateCursor(table, fields) as cur:
                for row in cur:
                    if row[0] is None:
                        row[0] = value
                        cur.updateRow(row)
        # If multiple field names were passed
        else:
            with arcpy.da.UpdateCursor(table, fields) as cur:
                for row in cur:
                    for x in range(len(fields)):
                        if row[x] is None:
                            row[x] = value
                            cur.updateRow(row)
    
        return
    
    
    def ReplaceValue(table, fields, originalValue, newValue):
        '''
        (str, str/list/tuple, any, any) -> None
    
        Sets values matching the originalValue to the newValue.
    
        Note that this does not replace text within a given cell's value; rather,
        it identifies cell values that identically match the originalValue and
        replaces the entire cell value with the newValue.
    
        Arguments:
        table -- Path of the table to be updated
        fields -- Name of the field(s) to be updated. Note that you can pass a string
            of a single field name or a list/tuple of a single or multiple field names.
        originalValue -- The value (i.e., string, number, etc.) that you wish to
            update
        newValue -- The value (i.e., string, number, etc., but it must match the
            field type) to which you wish to change occurrences of the originalValue.
            Note that the newValue must match the field type.
    
        Examples:
        >>> ReplaceValue('MyShp.shp', 'My_Field', 999, 1000)
    
        >>> ReplaceValue('MyShp.shp', ['My_Field'], 'Flurb', 'Flurbington')
    
        >>> ReplaceValue('MyShp.shp', ['Field_1', Field_b'], 'Durf', 'Durfington')
    
        '''
        # If a single field name was passed
        if isinstance(fields, basestring) or len(fields) == 1:
            with arcpy.da.UpdateCursor(table, fields) as cur:
                for row in cur:
                    if row[0] == originalValue:
                        row[0] = newValue
                        cur.updateRow(row)
        # If multiple field names were passed
        else:
            with arcpy.da.UpdateCursor(table, fields) as cur:
                for row in cur:
                    for x in range(len(fields)):
                        if row[x] == originalValue:
                            row[x] = newValue
                            cur.updateRow(row)
    
        return
    
    
    def ReplaceValues(table, fields, originalValues, newValue):
        '''
        (str, str/list/tuple, list/tuple, any) -> None
    
        Sets values matching any of the originalValues to the newValue
    
        Arguments:
        table -- Path of the table to be updated
        fields -- Name of the field(s) to be updated. Note that you can pass a string
            of a single field name or a list/tuple of a single or multiple field names.
        originalValues -- A list of values (i.e., strings, numbers, etc.) that you
            wish to update
        newValue -- The value (i.e., string, number, etc., but it must match the
            field type) to which you wish to change occurrences of the
            originalValues. Note that the newValue must match the field type.
    
        Examples:
        >>> ReplaceValues('MyShp.shp', 'My_Field', [0, 1, 2], 5)
    
        >>> ReplaceValues('MyShp.shp', ['My_Field'], ['Flurb', 'Flurbington'], 'Durf')
    
        >>> ReplaceValues('MyShp.shp', ['FirstField', 'FieldNum2', 'Field3'], ['Durfington', 'Durf'], 'Flurb')
    
        '''
    
        # If a single field name was passed
        if isinstance(fields, basestring) or len(fields) == 1:
            with arcpy.da.UpdateCursor(table, fields) as cur:
                for row in cur:
                    if row[0] in originalValues:
                        row[0] = newValue
                        cur.updateRow(row)
    
        # If multiple field names were passed
        else:
            with arcpy.da.UpdateCursor(table, fields) as cur:
                for row in cur:
                    for x in range(len(fields)):
                        if row[x] in originalValues:
                            row[x] = newValue
                            cur.updateRow(row)
    
        return
    
    
    def ReplaceValuesFromDict(table, field, replacementDict):
        '''
        (str, str, dict) -> None
    
        Update values in the given field by changing occurrences of the dictionary's
            keys to their corresponding values
    
        Arguments:
        table -- Path of the table to be updated
        field -- Name of the field to be updated
        replacementDict -- A dictionary from which values will be updated.
            In the given field, occurrences of a key will be replaced by the key's
            corresponding value. Note that the values must match the field type.
    
        Examples:
        >>> ReplaceValuesFromDict('myPoints.shp', 'MyField', {0:10, 100:1000}
    
        >>> ReplaceValuesFromDict('myPoints.shp', 'ParkName', {'YNP':'Yellowstone', \
            GCNP:'Grand Canyon'}
    
        '''
        with arcpy.da.UpdateCursor(table, field) as cur:
            for row in cur:
                try:
                    row[0] = replacementDict[row[0]]
                    cur.updateRow(row)
                except KeyError:
                    pass
    
        return
    
    
    def AttributeTableToCsv(layer, outputFile, keepOID=True, keepShape=False):
        '''
        (str, str, [bool], [bool]) -> str
    
        Exports the attribute table from the passed shapefile, feature class, raster,
            or geodatabase table to a csv. Returns the output csv path.
    
        Arguments:
        layer -- The path to the shapefile, feature class, raster, or geodatabase
           table, the attribute table of which will be written to a csv
        outputFile -- The path/name of the csv table you wish to create. Note that
           if a file already exists at that location, the rows (inclusive of the
           field names) will be appended to the existing table.
        keepOID -- An optional, boolean parameter, indicating whether you wish for
           each record's Object ID to be included in the output table. By default,
           it is set to True, meaning that the Object ID will be included.
        keepShape -- An optional, boolean parameter, indicating whether you wish for
           each record's shape object to be included in the output. By default, it
           is set to False, meaning that the shape information will not be included.
           Note that for polygons and/or lines, the shape objects can be quite
           large, as they contain the coordinates of every vertex.
    
        '''
        return tables.AttributeTableToCsv(layer, outputFile, keepOID, keepShape)
    
    
    
    def DomainAsDictionary(featureClass, fieldName):
        '''
        (str, str) -> dict
    
        Returns the field's coded attribute domain as a dictionary, in which
            the keys are the codes and the values are the coded strings.
    
        Arguments:
        featureClass -- The path/name of the feature class for which you wish to get
            the domain
        fieldName -- The name of the field for which you wish to get the domain
    
        Example:
        >>> DomainAsDictionary('MyFeatureClass', 'Own_Type')
        {u'02': u'Native American', u'03': u'State', u'01': u'Federal'}
        '''
        if 'gdb' not in featureClass.lower():
            gdb = arcpy.env.workspace
            featureClass = os.path.join(gdb, featureClass)
    
        fields = arcpy.ListFields(featureClass, fieldName)
    
        if len(fields) < 1:
            print 'No field named {0} exists in the feature class {1}'.format(fieldName, featureClass)
            return
    
        field = fields[0]
    
        doms = arcpy.da.ListDomains(os.path.dirname(featureClass))
    
        for d in doms:
            if d.name == field.domain:
                return d.codedValues
    
    
    def RenameField(featureClass, inputField, outputField):
        '''
        (str, str, str) -> None
    
        Renames the attribute field. Note that this creates a new field and copies
          the values and then deletes the original field, so the field will be in a
          different position in the attribute table. This function applies all
          properties and domains from the original field.
    
        Arguments:
        featureClass -- The path/name of the feature class within which you wish to
            make the change
        inputField -- The full name (not the alias name) of the field that you wish
            to rename.
        outputField -- The name that you want to apply to the field.
        '''
        # Get the field object of the original field
        try:
            f = arcpy.ListFields(featureClass, inputField)[0]
        except:
            print 'WARNING: The field {0} does not occur within {1}.'.format(inputField, featureClass)
            return
    
        # Create the new field, applying all the properties of the original field
        arcpy.AddField_management(featureClass, outputField, f.type, f.precision, f.scale, f.length, f.aliasName, f.isNullable, f.required, f.domain)
    
        CopyValues(featureClass, inputField, outputField, True)
    
    
    def GetMaxLength(featureClass, fields):
        '''
        (str, str/list/tuple) -> int
    
        Get the number of characters in the longest value from the passed field.
          If multiple fields are passed, returns the number of characters in the
          longest concatenated string of values (i.e., of values from the same
          feature/row). This number can be used, for example, to shorten the length
          of a text field (to save space) or to set the length of a new field that
          will store concatenations of values from other fields.
    
        Arguments:
        featureClass - The path/name of the feature class you wish to process
        fields - The field name of the field you wish to examine or a list/tuple of
          multiple field names from which you wish to examine concatenations.
    
        Example:
        >>> GetMaxLength('MyFeatureClass', 'State')
        14
        >>> # That is, the string 'North Carolina' contains 14 characters
    
        '''
        # If the user passed a single field
        if isinstance(fields, basestring):
            with arcpy.da.SearchCursor(featureClass, fields) as cur:
                # Set a maximum length variable
                maxCount = 0
                for row in cur:
                    # If the value is null, skip to the next row
                    if row[0] is None:
                        continue
                    # Get the character length of a string of the row's field value
                    try:
                        count = len((row[0]).encode('utf-8'))
                    except:
                        count = len(str(row[0]))
                    # Set the maximum variable as the largest of the existing max
                    # length or the current row's length
                    maxCount = max([maxCount, count])
        # If the user passed multiple fields
        else:
            with arcpy.da.SearchCursor(featureClass, fields) as cur:
                maxCount = 0
                for row in cur:
                    count = 0
                    for x in range(len(fields)):
                        # If the value is null, skip to the next row
                        if row[x] is None:
                            continue
                        # Get the character length of a string of the row's field value
                        try:
                            count += len((row[x]).encode('utf-8'))
                        except Exception as e:
                            count += len(str(row[x]))
                    # Set the maximum variable as the largest of the existing max
                    # length or the current row's length
                    maxCount = max([maxCount, count])
        # Return the length of the value with the most characters
        return maxCount
    
    
    
    def ChangeFieldLength(featureClass, field, newLength):
        '''
        (str, str, int) -> None
    
        Change the length of a text field. Note that the function creates a new
          field and copies the values from the original, so it will be in a
          different position.
    
        Arguments:
        featureClass -- The name/path of the feature class you wish to update
        field -- The name of the field to which you wish to apply the new length
            property
        newLength -- The number of characters that you want the field will hold
    
        Example:
        >>> ChangeFieldLength('MyFeatureClass', 'Comments', '300')
    
        '''
        f = arcpy.ListFields(featureClass, field)[0]
        tempField = field + '_'
    
        RenameField(featureClass, field, tempField)
    
        arcpy.AddField_management(featureClass, field, f.type, f.precision, f.scale, newLength, f.aliasName, f.isNullable, f.required, f.domain)
    
        CopyValues(featureClass, tempField, field, True)
    
        return
    
    
    def ConcatenateFields(featureClass, fields, outputField, separator=''):
        '''
        (str, list/tuple, str, [str]) -> str
    
        Concatenate the values from the input fields into a string in the passed
          output fields, separated by the optional separator.
    
        Arguments:
        featureClass - The path/name of the feature class you wish to update.
        fields - A string or tuple of field names for the fields from which you wish
          to concatenate values.
        outputField - The name of the field to which you wish to write the
          concatenated values. If the field does not exist, it will be created
          automatically. If the field exists, but its length is insufficient to
          store all concatenated values, the field's length will be updated as
          necessary.
        separator - An optional parameter of the string that you wish to insert
          between the concatenated values. By default, it is an empty string, which
          means that values will be concatenated without even a space or underscore
          between them.
    
        Example:
        >>> ConcatenateValues('myfeatureclass', ['City', 'State', 'ZipCode'], \
               'AddressLine2', ', ')
    
        '''
        # Get the number of characters you'll need in the field
        length = GetMaxLength(featureClass, fields)
        lengthPlusSep = length + (len(separator) * (len(fields) - 1))
    
        # Get a list of all existing fields in the feature class
        fs = [i.name for i in arcpy.ListFields(featureClass)]
        # If the output field does not already exist, create it, setting the length
        # to that required to concatenate the fields
        if not outputField in fs:
            arcpy.AddField_management(featureClass, outputField, 'TEXT', field_length = lengthPlusSep)
        # If the field already exists, ensure that it's length is sufficient to
        # fully concatenate the necessary fields
        else:
            f = arcpy.ListFields(featureClass, outputField)[0]
            if f.length < lengthPlusSep:
                ChangeFieldLength(featureClass, outputField, lengthPlusSep)
    
        # Add the output field to the end of the fields list
        fields.append(outputField)
        # Start an update cursor
        with arcpy.da.UpdateCursor(featureClass, fields) as cur:
            # For each feature/row
            for row in cur:
                # Instantiate an empty string to store the concatenated values
                concat = ''
                # For all but the last fields (the last field is the output field)
                for x in range(len(fields) - 1):
                    # Get the value in the cell
                    value = row[x]
                    # If the value is null, skip to the next field
                    if value is None:
                        continue
                    # Stringify the value
                    try:
                        s = value.encode('utf-8')
                    except:
                        s = str(value)
                    # Extend the concatenated string
                    concat = '{0}{1}{2}'.format(concat, separator, valueString)
                # Set the output field's value to the concatenated string
                row[-1] = concat
                cur.updateRow(row)
    
        return outputField
    
    
    def CopyValues(featureClass, inputField, outputField, deleteInputField=False):
        '''
        (str, str, str, [bool])
    
        For each feature in the feature class, copy the values from one attribute
          field to another
    
        Arguments:
        featureClass -- The name/path of the layer/feature class you wish to update
        inputField -- The name of the field from which you wish to copy values
        outputField -- The name of the field to which you wish to copy values.
        deleteInputField -- An optional, boolean parameter indicating whether you
            wish to delete the inputField after the values have been copied. By
            default, it is set to False, meaning that the field will not be deleted.
    
        Example:
        >>> CopyValues(r'C:\temp\mygdb.gdb\SpeciesRange', 'OldRangeCode', 'NewRangeCode')
    
        '''
        with arcpy.da.UpdateCursor(featureClass, [inputField, outputField]) as cur:
            for row in cur:
                row[1] = row[0]
                cur.updateRow(row)
    
        if deleteInputField:
            # Delete the original field
            try:
                arcpy.DeleteField_management(featureClass, inputField)
            except:
                print 'WARNING: Could not delete the field {0} from {1}.'.format(inputField, featureClass)
    
        return
    
    
    class __RowByColumn:
        def __init__(self, row, columns):
            self.row = row
            self.totalArea = 0
            # Create a dictionary in which the keys are the column values and the
            # values are initialized as zero
            self.columns = dict()
            for column in columns:
                self.columns[column] = 0
    
    
    def SummarizeXByY_Area(featureClass, rowField, columnField, outputPath):
        '''
        (str, str, str, str) -> str
    
        Writes to a csv a summary of the area and proportion area of each value in
          rowField by each value in the columnField. That is, say that the row field
          is PAD-US Owner Type and the column field is GAP Status. The resulting csv
          table would list owner types as the row headings (column A) and the four
          possible GAP statuses as the column headings (row 1). The first row in the
          output table would look like:
    
          Owner_Type, Total_Area_in_Square_Meters, 1, 2, 3, 4, Proportion_1, Proportion_2, Proportion_3, Proportion_4
    
          An example row might look like:
          Private, 200500, 0, 10500, 140000, 50000, 0, 0.052, 0.698, 0.249
    
          Returns the outputPath
    
        Arguments:
        featureClass -- The path of the feature class from which you wish to derive
          the numbers
        rowField -- The name of the field from which you wish to use the values as
          row headings in the output table
        columnField -- The name of the field from which you wish to use the values
          as column headings in the output table
        outputPath -- The path and filename to where you wish to write the output
          table
    
        Example:
        >>> SummarizeXByY_Area('PADUS_13', 'OwnerType', 'GAP_Status_code', r'C:\temp\OT_by_GS.csv')
    
        '''
    
        # List all values occurring in the row field
        rows = ListValues(featureClass, rowField, True)
        # List all values occurring in the column field
        columns = ListValues(featureClass, columnField, True)
        # Instantiate an empty dictionary to store row objects
        rowsDict = dict()
        # For each row, create a dictionary entry for which the key is the row value
        # and the value is a row object
        for row in rows:
            rowsDict[row] = __RowByColumn(row, columns)
    
        # Read the input table and populate the dictionaries with the values
        with arcpy.da.SearchCursor(featureClass, [rowField, columnField, 'SHAPE@AREA']) as cur:
            for feature in cur:
                rowHeading = feature[0]
                columnHeading = feature[1]
                area = feature[2]
                # Increment the row's column's value by the current feature's area
                rowsDict[rowHeading].columns[columnHeading] += area
                # Increment the row's total area by the current feature's area
                rowsDict[rowHeading].totalArea += area
    
        rows.sort()
        columns.sort()
    
        # The feature class' spatial unit
        lun = GetLinearUnit(featureClass)
    
        # If the areas will be in square meters, set a function to calculate hectares
        if lun == 'Meter':
            unit = 'Hectares'
            def f(x): return x / 10000
        # If the areas will be in square feet, set a function to calculate acres
        elif lun == 'Foot':
            unit = 'Acres'
            def f(x): return x / 43560
        # Otherwise, set a function just to return the input value
        else:
            unit = 'Square_{0}s'.format(lun)
            def f(x): return x
    
        # Set a string of the total area column's heading
        totalHeader = 'Total_Area_In_{0}'.format(unit)
    
        # Start putting together the headings
        headings = [rowField, totalHeader]
        # Set the heading names for the raw area columns
        columnsHeadings = ['Area_in_{0}_{1}_{2}'.format(unit, columnField, i) for i in columns]
        headings.extend(columnsHeadings)
        # Set the heading names for the proportion area columns
        columnsProp = ['Proportion_Area_{0}_{1}'.format(columnField, i) for i in columns]
        headings.extend(columnsProp)
    
        # Instantiate a list to store the output rows, and put the headings into it
        outRows = [headings]
    
        # For each unique value in the rowField
        for row in rows:
            # Get the total area
            totalArea = f(rowsDict[row].totalArea)
            # Instantiate a list to store the output row, and start populating it
            # with the value from the input rowField along with the total area of
            # that value
            outRow = [row, totalArea]
            # For each value in the column field, add the row's associated value
            for column in columns:
                outRow.append(f(rowsDict[row].columns[column]))
            # For each value in the column field, add the row's associated value divided
            # by the row's total area
            for column in columns:
                outRow.append(f(rowsDict[row].columns[column]) / totalArea)
            # Add the row to the list of output rows
            outRows.append(outRow)
    
        # Write the rows to the passed csv
        tables.WriteListToCsv(outRows, outputPath)
    
        return outputPath
    
    
    def GetLinearUnit(featureClass):
        '''
        (str) -> str
    
        Return the linear unit of the feature class' spatial reference. Can be used,
          for example, to interpret the length/area attributes of features.
    
        Argument:
        featureClass -- The path to the feature class for which you wish to identify
          the linear unit.
    
        Example:
        >>> GetLinearUnit('myShapefile.shp')
        'Meter'
        '''
        d = arcpy.Describe(featureClass)
        return d.spatialReference.linearUnitName
    
    
    def __main():
        pass
    
    if __name__ == '__main__':
        __main()

except:
    print("May not have been able to import arcpy")