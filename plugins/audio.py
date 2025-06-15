import mutagen
import os
from plugins.base_extractor import BaseExtractor
import re

class AudioExtractor(BaseExtractor):
    
    def __init__(self):
        self._supported_extensions = [".mp3", ".ogg"]
        
    @property
    def supported_extensions(self):
        return self._supported_extensions
        
    def extract_meta(self, file_path):
        formated_metadata = {}
        extension = os.path.splitext(file_path)[1]
        
        if extension not in self._supported_extensions:
            return {}
        
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
        
        formated_metadata = {
            re.sub(r"[ \(\)]", "_", key): value
            for key, value in formated_metadata.items()
        }
        return formated_metadata

#test
#x = extract_meta("test-files/mp3-test.mp3")
#y = extract_meta("test-files/ogg-test.ogg")
#print(x)
#print(y)

