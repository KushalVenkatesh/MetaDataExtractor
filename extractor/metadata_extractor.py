from __future__ import print_function
from PIL import Image, ExifTags
from lxml import etree
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import os
import zipfile
from datetime import datetime as dt
from xml.etree import ElementTree as etree
import re
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

def posix_from_s(element):
    year = element[2:6]
    month = element[6:8]
    day = element[8:10]
    hour = element[10:12]
    minute = element[12:14]
    second = element[14:16]
    date = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second

    return dt.strptime(date, "%Y-%m-%d %H:%M:%S")


def decoder(element):
    try:
        decoded = element.decode("utf-8")
        decoded = re.sub('\x00', "", decoded)
        decoded = re.sub('0xfe', "", decoded)

    except Exception as e:
        print(e)
        decoded = element.decode("latin-1")
        decoded = re.sub('\x00', "", decoded)
        decoded = re.sub('0xfe', "", decoded)

    return decoded


def msoffice_metadata(path, filename=None):
    if zipfile.is_zipfile(path):
        zfile = zipfile.ZipFile(path)
        core_xml = etree.fromstring(zfile.read('docProps/core.xml'))
        app_xml = etree.fromstring(zfile.read('docProps/app.xml'))
        metadata = {}
        metadata['Title'] = os.path.basename(path)
        valid_name = ['Author(s)', 'Created Date', 'Modified Date', 'Last Modified By']

        # Key elements
        core_mapping = {
            'title': 'Title',
            'subject': 'Subject',
            'creator': 'Author(s)',
            'keywords': 'Keywords',
            'description': 'Description',
            'lastModifiedBy': 'Last Modified By',
            'modified': 'Modified Date',
            'created': 'Created Date',
            'category': 'Category',
            'contentStatus': 'Status',
            'revision': 'Revision'
        }
        for element in core_xml.getchildren():
            for key, title in core_mapping.items():
                if key in element.tag:
                    if 'date' in title.lower():
                        text = dt.strptime(element.text, "%Y-%m-%dT%H:%M:%SZ")
                    else:
                        text = element.text
                    print("{}: {}".format(title, text))
                    if title in valid_name:
                        metadata[str(title)] = text

        # Statistical information
        app_mapping = {
            'TotalTime': 'Edit Time (minutes)',
            'Pages': 'Page Count',
            'Words': 'Word Count',
            'Characters': 'Character Count',
            'Lines': 'Line Count',
            'Paragraphs': 'Paragraph Count',
            'Company': 'Company',
            'HyperlinkBase': 'Hyperlink Base',
            'Slides': 'Slide count',
            'Notes': 'Note Count',
            'HiddenSlides': 'Hidden Slide Count',
        }
        for element in app_xml.getchildren():
            for key, title in app_mapping.items():
                if key in element.tag:
                    if 'date' in title.lower():
                        text = dt.strptime(element.text, "%Y-%m-%dT%H:%M:%SZ")
                    else:
                        text = element.text
                    print("{}: {}".format(title, text))
                    if title in valid_name:
                        metadata[str(title)] = text

    return metadata


def pdf_metadata(path):
    metadata = {}
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    try:
        metadata['Title'] = decoder(doc.info[0]["Title"])
    except KeyError:
        metadata['Title'] = os.path.basename(path)
    try:
        metadata['Author(s)'] = decoder(doc.info[0]["Author"])
    except KeyError:
        metadata['Author(s)'] = decoder(doc.info[0]["Creator"])
    try:
        metadata['Last Modified By'] = decoder(doc.info[0]["Author"])
    except Exception as e:
        print(e)
        print('No modification found in metadata')
        metadata['Last Modified By'] = None
    metadata['Created Date'] = posix_from_s(decoder(doc.info[0]["CreationDate"]))
    try:
        metadata['Modified Date'] = posix_from_s(decoder(doc.info[0]["ModDate"]))
    except Exception as e:
        print(e)
        print('No modification found in metadata')
        metadata['Modified Date'] = None

    return metadata

def img_metadata(path):
    infoDict = {}  # Creating the dict to get the metadata tags
    exifToolPath = 'D:/ExifTool/exifTool.exe'  # for Windows user have to specify the Exif tool exe path for metadata extraction.
    # For mac and linux user it is just
    """exifToolPath = exiftool"""



    process = subprocess.Popen(path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           universal_newlines=True)
    for tag in process.stdout:
        line = tag.strip().split(':')
        infoDict[line[0].strip()] = line[-1].strip()

    return infoDict