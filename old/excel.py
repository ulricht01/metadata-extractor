import openpyxl
import datetime
# funguje na -> xlsx/xlsm/xltx/xltm

def extract_meta(file_path):
    file = openpyxl.load_workbook(file_path)
    metadata = file.properties
    
    def format_date(value):
        if isinstance(value, datetime.datetime):
            return value.strftime("%d.%m.%Y %H:%M:%S")
        return None
    
    # všechny metadata, které jdou vytáhnout pomocí knihovny docx
    formated_metadata = {
        "category" : metadata.category,
        "contentStatus" : metadata.contentStatus,
        "created" : format_date(metadata.created),
        "creator" : metadata.creator,
        "description" : metadata.description,
        "identifier" : metadata.identifier,
        "keywords" : metadata.keywords,
        "language" : metadata.language,
        "lastModifiedBy" : metadata.lastModifiedBy,
        "lastPrinted" : format_date(metadata.lastPrinted),
        "last_modified_by" : metadata.last_modified_by,
        "modified" : format_date(metadata.modified),
        "revision" : metadata.revision,
        "subject" : metadata.subject,
        "tagname " : metadata.tagname,
        "title" :  metadata.title,
        "version" : metadata.version
    }
    
    return formated_metadata

#test
x = extract_meta("test-files/excel-test.xlsx")

print(x)
