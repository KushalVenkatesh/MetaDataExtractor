import json
import os
import xml
import re
import pandas as pd
from extractor.metadata_extractor import metadata
from datetime import datetime


def df_from_json(path):

    js_metadata = pd.read_json(path)
    df_metadata = pd.DataFrame({'Title':js_metadata.iloc[0,],
                                'Author(s)':js_metadata.iloc[1,],
                                'Created Date':js_metadata.iloc[2,],
                                'Modified Date':js_metadata.iloc[3,],
                                'Last Modified By': js_metadata.iloc[4,]})

    return df_metadata


def xml_printer(zip_file, xml_toread):
    xml_raw = zip_file.read(str(xml_toread))
    ugly_xml = xml.dom.minidom.parseString(xml_raw).toprettyxml(indent='   ')
    text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
    pretty_xml = text_re.sub('>\g<1></', ugly_xml)

    print(pretty_xml)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def to_json(dic, file_name="metadata.json"):
    js = json.dumps(dic, indent=1, cls=DateTimeEncoder)

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


def luke_oswalker(path, save=False, R=False):
    global df
    files = {}
    index = 1
    paths = get_arbo(path)
    for path in paths:
        filename = os.path.basename(path)
        if filename.endswith(".pptx") or filename.endswith(".docx") or filename.endswith(".xlsx"):
            try:
                print("------------------")
                print(filename)
                temp = metadata(path, filename)
                print(temp)
                files[str(index)] = temp
                index += 1
            except Exception as e:
                print(e)

    if save:
        to_json(files)
        if R:
            path = os.getcwd() + '/data/data/' + "metadata.json"
            df = df_from_json(path)
            df.to_csv('metadata.csv')