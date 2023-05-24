"""
This script demonstrates how to use the V2ForRangeEdit function

N. Tarr, 5/24/2023
"""
import sys
sys.path.append("T:/Code/gapproduction")
from gapproduction import ranges

# Get a dataframe with the necessary columns and values
df = ranges.V2ForRangeEdit("C:/Workspaces/RangeMaps/marten/mAMMAx2016.sqlite")

# From here you could insert the dataframe into the tblRangeEdit table in the
# GAP database.