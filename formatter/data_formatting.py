import json
import os
from extractor.metadata_extractor import metadata


def to_json(dic, file_name="metadata.json"):
    js = json.dumps(dic, indent=1)

    # Open new json file if not exist it will create
    fp = open(os.getcwd() + '/data/data/' + str(file_name), 'w')

    # write to json file
    fp.write(js)

    # close the connection
    fp.close()


def get_arbo(location):
    # Initialize list of directories
    paths = []

    for file in os.listdir(location):
        path = str(location) + "/" + str(file)
        paths.append(path)

    return paths


def luke_oswalker(path):
    paths = get_arbo(path)
    for path in paths:
        filename = os.path.basename(path)
        print(filename)
        author = metadata(path)
        print(author)

    return(author)