"""
This script demonstrates how to use the citations functions.

N. Tarr, May 9, 2023
"""
import sys
sys.path.append("ENTERPATHTOCODEREPO/gapproduction")
from gapproduction import citations

# Designate a database (2001 or 2016 GAP db) -----------------------------------
db = 'One_of_the_GAP_databases'

# Define the reference textstring ---------------------------------------------
reference = "Fake, H. C. 1914. This is a TEST DELETE ME. Auk 31: 168–177."

# Check if reference already exists -------------------------------------------
taken, matches = citations.CitationExists(reference, db)
if taken:
    print("The reference may already exist in the database, here are the matches:")
    print(matches['strRefCode'])

if not taken:
    print("The reference doesn't appear to exist in the database.")

    # Build reference code ----------------------------------------------------
    reference_type = 'A' # Identify the code for the reference type.  They are listed in the build_strRefCode docstring.
    reference_code = citations.BuildStrRefCode(reference, 'A', db)
    print(reference_code)

    # Add reference to database ---------------------------------------------------
    citations.AddReference(reference, reference_code, db)

