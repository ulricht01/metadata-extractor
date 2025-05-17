import docx
import datetime

def extract_meta(file_path):
    file = docx.Document(file_path)
    metadata = file.core_properties
    
    def format_date(value):
        if isinstance(value, datetime.datetime):
            return value.strftime("%d.%m.%Y %H:%M:%S")
        return None
    
    # všechny metadata, které jdou vytáhnout pomocí knihovny docx
    formated_metadata = {
        "author" : metadata.author,
        "category" : metadata.category,
        "comments" : metadata.comments,
        "content_status" : metadata.content_status,
        "created" : format_date(metadata.created),
        "identifier" : metadata.identifier,
        "keywords" : metadata.keywords,
        "language" : metadata.language,
        "last_modified_by" : metadata.last_modified_by,
        "last_printed" : format_date(metadata.last_printed),
        "modified" : format_date(metadata.modified),
        "revision" : metadata.revision,
        "subject" : metadata.subject,
        "title" : metadata.title,
        "version" : metadata.version
    }
    
    return formated_metadata

#test
x = extract_meta("test-files/word-test.docx")

print(x)
