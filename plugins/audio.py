import mutagen
import os

def extract_meta(file_path):
    formated_metadata = {}
    extension = os.path.splitext(file_path)[1]
    file = mutagen.File(file_path)
    if extension == ".ogg":
        for key,value in file.items():
            if isinstance(value, list):
                formated_metadata[key] = ", ".join(value)
            else:
                formated_metadata[key] = str(value)
    elif extension == ".mp3":
        for key,value in file.items():
            if isinstance(value, list):
                formated_metadata[key] = ", ".join(value)
            elif key.startswith("TXXX"):
                desc = value.desc
                formated_metadata[desc] = str(value.text[0])
            elif key.startswith("TDRC"):
                formated_metadata["Date"] = str(value.text[0])
            else:
                formated_metadata[key] = str(value)
    
    # všechny metadata, které jdou vytáhnout pomocí knihovny docx
    
    
    return formated_metadata

#test
x = extract_meta("test-files/mp3-test.mp3")
y = extract_meta("test-files/ogg-test.ogg")
print(x)
print(y)
