"""
This script demonstrates how to use the V2As2016() function to extract
data from a version 2 output database into a format that matches the 2016
database.

Paths would need to be changed accordingly.

N. Tarr
5/24/2023
"""
import sys
sys.path.append("C:/ENTER PATH TO YOUR /GAPProduction")
from gapproduction import ranges

# Run the function
df = ranges.V2As2016("K:/ ENTER A PATH /mAMMAx2016.sqlite")

# Write the dataframe to a csv file
df.to_csv("L:/mAMMAx2016.csv", index=False)

# Instead of writing to a csv, you could write to the database (insert into)