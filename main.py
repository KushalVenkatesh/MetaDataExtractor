import os
from format.data_formatting import luke_oswalker
path = os.getcwd() + "/data/data"

luke_oswalker(path, save=True, R=True)
