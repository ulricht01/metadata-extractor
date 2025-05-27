import PyPDF2
import datetime

def extract_meta(file_path):
    file = PyPDF2.PdfReader(file_path)
    metadata = file.metadata
    
    def format_date(value):
        if isinstance(value, datetime.datetime):
            return value.strftime("%d.%m.%Y %H:%M:%S")
        return None
    
    formated_metadata = {
        "author" : metadata.author,
        "author_raw" : metadata.author_raw,
        "creation_date" : format_date(metadata.creation_date),
        "creation_date_raw" : metadata.creation_date_raw,
        "creator" : metadata.creator,
        "creator_raw" : metadata.creator_raw,
        "modification_date" : format_date(metadata.modification_date),
        "modification_date_raw" : metadata.modification_date_raw,
        "producer" : metadata.producer,
        "producer_raw" : metadata.producer_raw,
        "subject" :  metadata.subject,
        "subject_raw" : metadata.subject_raw,
        "title" : metadata.title,
        "title_raw" : metadata.title_raw,
    }
    return formated_metadata
    
    
    
#test
x = extract_meta("test-files/pdf-test.pdf")

print(x)