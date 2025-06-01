import docx
import odf.opendocument
from odf.element import Element
import datetime
import os
import PyPDF2
import re
import openpyxl
from plugins.base_extractor import BaseExtractor

class DocsExtractor(BaseExtractor):
    
    def __init__(self):
        self._supported_extensions = [".docx", ".odt", ".pdf", ".rtf", ".txt", ".xlsx", ".xlsm", ".xltx", ".xltm"]
        
    @property
    def supported_extensions(self):
        return self._supported_extensions
    
    def extract_meta(self, file_path):
        
        def format_date(value):
            if isinstance(value, datetime.datetime):
                return value.strftime("%d.%m.%Y %H:%M:%S")
            elif isinstance(value, (int, float)):
                return datetime.datetime.fromtimestamp(value).strftime("%d.%m.%Y %H:%M:%S")
            return None


        extension = os.path.splitext(file_path)[1].lower()
        metadata = {}
        
        if extension not in self._supported_extensions:
            return {}

        if extension == ".docx":
            file = docx.Document(file_path)
            core = file.core_properties
            
            metadata = {
                "author": core.author,
                "category": core.category,
                "comments": core.comments,
                "content_status": core.content_status,
                "created": format_date(core.created),
                "identifier": core.identifier,
                "keywords": core.keywords,
                "language": core.language,
                "last_modified_by": core.last_modified_by,
                "last_printed": format_date(core.last_printed),
                "modified": format_date(core.modified),
                "revision": core.revision,
                "subject": core.subject,
                "title": core.title,
                "version": core.version
            }

        elif extension == ".odt":
            file = odf.opendocument.load(file_path)
            for child in file.meta.childNodes:
                if isinstance(child, Element):
                    tag = child.qname[1]
                    metadata[tag] = child.firstChild.data if child.firstChild else ""

        elif extension == ".pdf":
            file = PyPDF2.PdfReader(file_path)
            core = file.metadata
            metadata = {
            "author" : core.author,
            "author_raw" : core.author_raw,
            "creation_date" : format_date(core.creation_date),
            "creation_date_raw" : core.creation_date_raw,
            "creator" : core.creator,
            "creator_raw" : core.creator_raw,
            "modification_date" : format_date(core.modification_date),
            "modification_date_raw" : core.modification_date_raw,
            "producer" : core.producer,
            "producer_raw" : core.producer_raw,
            "subject" :  core.subject,
            "subject_raw" : core.subject_raw,
            "title" : core.title,
            "title_raw" : core.title_raw,
        }
        
        elif extension == ".rtf":
            with open(file_path, encoding="utf-8") as file:
                content = file.read()
            match = re.search(r'{\\info(.*?)}', content, re.DOTALL)
            if match:
                def extract_tag(tag):
                    if tag == "creatim":
                        match = re.search(r'\\creatim\\yr(\d+)\\mo(\d+)\\dy(\d+)\\hr(\d+)\\min(\d+)', content)
                        if match:
                            y, m, d, h, mi = map(int, match.groups())
                            return f"{d:02d}.{m:02d}.{y} {h:02d}:{mi:02d}"
                        else:
                            return None
                    else:
                        tag_data = re.search(rf'{{\\{tag} (.*?)}}', content)
                        return tag_data.group(1) if tag_data else None
                    
                metadata = {
                    "title" : extract_tag("title"),
                    "author": extract_tag("author"),
                    "creatim": extract_tag("creatim"),
                    "keywords": extract_tag("keywords"),
                    "comment" :  extract_tag("comment")
                }
            else:
                return None
        
        elif extension == ".txt":
            file_metadata = os.stat(file_path)
            metadata = {
                "filesizeBytes": file_metadata.st_size, # Velikost souboru
                "lastChangeDate": format_date(file_metadata.st_mtime), # Čas poslední změny souboru
                "lastMetadataChange": format_date(file_metadata.st_ctime), # Čas poslední změny metadat souboru
                "birthDate": format_date(file_metadata.st_birthtime), # Čas vytvoření souboru
            }
                    
        elif extension == ".xlsx" or extension == ".xlsm" or extension == ".xltx" or extension == ".xltm":
            file = openpyxl.load_workbook(file_path)
            properties = file.properties
            
            metadata = {
            "category" : properties.category,
            "contentStatus" : properties.contentStatus,
            "created" : format_date(properties.created),
            "creator" : properties.creator,
            "description" : properties.description,
            "identifier" : properties.identifier,
            "keywords" : properties.keywords,
            "language" : properties.language,
            "lastModifiedBy" : properties.lastModifiedBy,
            "lastPrinted" : format_date(properties.lastPrinted),
            "last_modified_by" : properties.lastModifiedBy,
            "modified" : format_date(properties.modified),
            "revision" : properties.revision,
            "subject" : properties.subject,
            "tagname " : properties.tagname,
            "title" :  properties.title,
            "version" : properties.version
        }
        return metadata

# Test DOCX
#x = extract_meta("test-files/word-test.docx")

# Test ODT
#x = extract_meta("test-files/test.odt")
#print(x)

# Test PDF
#x = extract_meta("test-files/pdf-test.pdf")

#print(x)

# Test RTF
#x = extract_meta("test-files/test.rtf")

#print(x)


# Test TXT
#x = extract_meta("test-files/test.txt")

#print(x)

#test XLSX
#x = extract_meta("test-files/excel-test.xlsx")

#print(x)