# import sys
# import pprint

# pprint.pprint(sys.path)

import os
from plixel.SheetAnalyser import SheetAnalyser


path = "C:/Users/Chaitanya/Downloads/Sample Data.xlsx"

if os.path.exists(path):
    sa = SheetAnalyser(file_path=path)
