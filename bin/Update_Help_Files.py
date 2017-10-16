# Simply run this module (no inputs or modifications needed) to update the help
# files for all of the gappack modules.
#

import sys, pydoc, os

#Where's the config module? Must be named gapconfig.py
sys.path.append("")
#Where's the gappack code located?
sys.path.append('')
import gapproduction as gp

helpDir = '/GAPProduction/documentation'
if not os.path.exists(helpDir):
    os.makedirs(helpDir)

for mod in gp.__all__:
    s = pydoc.plain(pydoc.render_doc('gapproduction.' + mod))
    gp.docs.Write(os.path.join(helpDir, 'Help_' + mod + '.txt'), s, 'o')
