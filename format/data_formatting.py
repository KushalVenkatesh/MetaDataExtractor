import json
import os
from extractor.metadata_extractor import metadata
import xml
import re


def xml_printer(zip_file, xml_toread):
    xml_raw = zip_file.read(str(xml_toread))
    ugly_xml = xml.dom.minidom.parseString(xml_raw).toprettyxml(indent='   ')
    text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
    pretty_xml = text_re.sub('>\g<1></', ugly_xml)

    print(pretty_xml)


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
        if filename.endswith(".pptx") or filename.endswith(".docx") or filename.endswith(".xlsx"):
            print("------------------")
            print(filename)
            author = metadata(path, filename)
            print(author)
