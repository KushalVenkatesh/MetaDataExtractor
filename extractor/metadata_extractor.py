import zipfile
import lxml.etree
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'


def metadata(path):
    document = zipfile.ZipFile(path)

    # use lxml to parse the xml file we are interested in
    doc = lxml.etree.fromstring(document.read('docProps/core.xml'))

    # retrieve creator
    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
    creator = doc.xpath('//dc:creator', namespaces=ns)[0].text

    return creator
