import logging
import xml.etree.ElementTree as ET


logger = logging.getLogger('dts')
namespaces = {'mets': 'http://www.loc.gov/METS/', 
              'xlink': 'http://www.w3.org/1999/xlink',
              'dim': 'http://www.dspace.org/xmlns/dspace/dim'}

class MetsExtractor:
    
    def __init__(self, mets_path) -> None:
        tree = ET.parse(mets_path)
        self.root = tree.getroot()
        self.fileSec = {}
        self.degree_date = None
        self.identifier = None

    def get_amdid_and_mimetype(self, filename):
        '''Get the amdid and mimetype from the fileSec'''
        # Get the file elements
        files = self.root.findall(".//mets:file", namespaces)
        for file in files:
            # Get the flocat element for the file
            flocat = file.find(".//mets:FLocat", namespaces)
            href = flocat.get("{" + namespaces['xlink'] + "}href")
            # If the href attribute matches the filename, 
            # return the amdid and mimetype
            if href and href == filename:
                amdid = file.get("ADMID")
                mimetype = file.get("MIMETYPE")
                if amdid and mimetype:
                    fileSecInfo = FileSecInfo(amdid, mimetype)
                    self.fileSec[filename] = fileSecInfo
                    return fileSecInfo
        return FileSecInfo()
    
    def get_degree_date(self):
        '''Get the degree date from 
        <dim:field mdschema="thesis" element="degree" qualifier="date">'''
        if self.degree_date is None:
            field = self.root.find(".//dim:field[@mdschema='thesis'][@element='degree'][@qualifier='date']", namespaces)
            if field is not None:
                self.degree_date = field.text
        return self.degree_date
    
    def get_identifier(self):
        '''Get the identifier from 
        <dim:field mdschema="dc" element="identifier" qualifier="other">'''
        if self.identifier is None:
            field = self.root.find(".//dim:field[@mdschema='dc'][@element='identifier'][@qualifier='other']", namespaces)
            if field is not None:
                self.identifier = field.text
        return self.identifier
    
    def get_embargo_until(self):
        '''Get the identifier from 
        <dim:field mdschema="dash" element="embargo" qualifier="until">'''
        if self.embargo_until is None:
            field = self.root.find(".//dim:field[@mdschema='dash'][@element='embargo'][@qualifier='until']", namespaces)
            if field is not None:
                self.embargo_until = field.text
        return self.embargo_until

class FileSecInfo:
    def __init__(self, amdid=None, mimetype=None):
        self.amdid = amdid
        self.mimetype = mimetype
