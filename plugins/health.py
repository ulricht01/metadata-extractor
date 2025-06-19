import os
from plugins.base_extractor import BaseExtractor
import xml.etree.ElementTree as ET
import pydicom 
#from base_extractor import BaseExtractor
 
class HealthExtractor(BaseExtractor):
    
    def __init__(self):
        self._supported_extensions = [".xml", ".dcm"]
        
    @property
    def supported_extensions(self):
        return self._supported_extensions
        
    def extract_meta(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()
        
        dc_fields = {
            "title": "",
            "creator": [],
            "subject": "",
            "description": [],
            "publisher": "",
            "contributor": "",
            "date": "",
            "type": "",
            "format": extension,
            "identifier": "",
            "source": "",
            "language": "",
            "relation": "",
            "coverage": "",
            "rights": ""
        }
        
        if extension not in self._supported_extensions:
            return dc_fields

        if extension == ".xml":
            tree = ET.parse(file_path)
            root = tree.getroot()

            if tree is None:
                return dc_fields
            
            for element in root:
                tag = element.tag
                text = element.text.strip() if element.text else ""
                
                if tag == "title":
                    dc_fields["title"] = text
                elif tag == "specialty":
                    dc_fields["subject"] = text
                elif tag == "publisher":
                    dc_fields["publisher"] = text
                elif tag == "articleDate":
                    dc_fields["date"] = text    
                elif tag == "articleType":
                    dc_fields["type"] = text
                elif tag == "uId":
                    dc_fields["identifier"]= element.attrib.get("id", "")
                elif tag == "articleurl":
                    dc_fields["source"]= text   
                elif tag == "licenseType":
                    dc_fields["rights"]= text
                

            author_list, abstract_list = root.find(".//AuthorList"), root.find(".//Abstract")
            
            for author in author_list.findall("Author"):
                full_name = f"{author.findtext("ForeName", default="")} {author.findtext("LastName", default="")}"
                dc_fields["creator"].append(full_name)
                
            for abstract in abstract_list.findall("AbstractText"):
                dc_fields["description"].append(abstract.text)
            
            dc_fields["contributor"] = root.find(".//Affiliation").text
            dc_fields["language"] = root.find(".//Language").text
            dc_fields["relation"] = root.find(".//parentImage").attrib.get("id", "")
                
        elif extension == ".dcm":
            data = pydicom.dcmread(file_path)
        
            dc_fields["title"] = getattr(data, "StudyDescription", "")
            dc_fields["creator"] = [getattr(data, "ReferringPhysicianName", "")] if getattr(data, "ReferringPhysicianName", "") else []
            dc_fields["subject"] = getattr(data, "BodyPartExamined", "")
            dc_fields["description"] = [getattr(data, "SeriesDescription", ""), " ".join(getattr(data, "ImageType", [])) if hasattr(data, "ImageType") else ""]
            dc_fields["publisher"] = getattr(data, "Manufacturer", "")
            dc_fields["contributor"] = getattr(data, "ImplementationClassUID", "")
            dc_fields["date"] = f"{getattr(data, 'StudyDate', '')} {getattr(data, 'StudyTime', '')}".strip()
            dc_fields["type"] = " ".join(getattr(data, "ImageType", [])) if hasattr(data, "ImageType") else getattr(data, "Modality", "")
            dc_fields["format"] = extension
            dc_fields["identifier"] = getattr(data, "AccessionNumber", "") or getattr(data, "StudyInstanceUID", "") or getattr(data, "SOPInstanceUID", "")
            dc_fields["source"] = ""
            dc_fields["language"] = ""
            dc_fields["relation"] = ""
            dc_fields["coverage"] = ""
            dc_fields["rights"] = ""
        return dc_fields
 

            
    
#i = HealthExtractor()

#print(i.extract_meta("G:/Programování/sipky/metadata-extractor/test-files/health_data/dicom/1.2.826.0.1.3680043.8.498.10606529710873585120949488696315239902-c.dcm"))


