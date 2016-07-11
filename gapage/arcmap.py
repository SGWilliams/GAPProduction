
'''
Functions for tasks performed in the python window within ESRI ArcMap.
'''
try:
    import arcpy

    def AddSelections(raster, MUlist):
        '''
        (raster, list) -> selection

        For use in ArcMap python window.  Selects pixels for map unit codes specified
            in MUlist for viewing and review.

        Arguments:
        raster -- the raster layer you want to select from.
        MUlist -- a python list of codes to select from the "VALUE" field.
        '''
        import arcpy
        selectionType = "ADD_TO_SELECTION"
        sql = '"VALUE" = ' + str(MUlist[0])
        for m in MUlist[1:]:
            sql = sql + ' OR "VALUE" = ' + str(m)
        arcpy.SelectLayerByAttribute_management(raster, selectionType, sql)


    def RemoveSelections(raster, MUlist):
        '''
        (raaster, list) -> selection

        For use in ArcMap python window.  Removes pixels for map unit codes specified
            in MUlist from selection for viewing and review.

        Arguments:
        raster -- the raster layer you want to select from.
        MUlist -- a python list of codes to select from the "VALUE" field.
        '''
        import arcpy
        selectionType = "REMOVE_FROM_SELECTION"
        sql = '"VALUE" = ' + str(MUlist[0])
        for m in MUlist[1:]:
            sql = sql + ' OR "VALUE" = ' + str(m)
        arcpy.SelectLayerByAttribute_management(raster, selectionType, sql)


    def New_Selections(raster, MUlist):
        '''
        (raster, list) -> selection

        For use in ArcMap python window.  Creates a new selection of pixels for
            map unit codes specified in MUlist for viewing and review.  Previous
            selections are cleared first.

        Arguments:
        raster -- the raster layer you want to select from.
        MUlist -- a python list of codes to select from the "VALUE" field.
        '''
        import arcpy
        selectionType = "NEW_SELECTION"
        sql = '"VALUE" = ' + str(MUlist[0])
        for m in MUlist[1:]:
            sql = sql + ' OR "VALUE" = ' + str(m)
        arcpy.SelectLayerByAttribute_management(raster, selectionType, sql)
except:
    print("Arcpy is unavailable, the arcmap module will not work")
    pass
