# config.py

# configuration constants for XPoint Consulting Project Management.

from Products.Archetypes.public import DisplayList

# project name.
PROJECTNAME = "XPointProjectManagement"

# skins directory for this project, contains gif, vie pt ...
SKINS_DIR = "skins"

# A global name space when this product is loaded into Python is 
# preserved. It passes to the package_home() etc.
GLOBALS = globals()

# build journal project names, will be eliminated when the
# configuration module is ready.
BUILD_JOURNAL_PROJECT_NAMES = DisplayList ((
        ('Express3.2-GR', 'Express 3.2 GeneralRelease'),
        ('Express3.3-ML', 'Express 3.3 Multi Lender'),
        ('Express3.3-BDN', 'Express 3.3 Bilangual Deal Notes'),
        ))
