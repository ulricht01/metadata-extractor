import subprocess
import json
import os
from plugins.base_extractor import BaseExtractor



class FotoExtractor(BaseExtractor):
    
    def __init__(self):
        self._supported_extensions = [".CR3"]
        
    @property
    def supported_extensions(self):
        return self._supported_extensions
    
    def extract_meta(self, file_path):
        formated_metadata = {}
        extension = os.path.splitext(file_path)[1]
        
        if extension not in self._supported_extensions:
            return {}
        
        if extension == ".CR3":
            # Cesta k exiftool.exe (relativní cesta)
            exiftool_path = os.path.join(os.path.dirname(__file__), '../tools/exiftool/exiftool.exe')

            try:
                result = subprocess.run(
                    [exiftool_path, '-json', file_path],
                    capture_output=True,
                    text=True,
                    check=True
                )
                metadata = json.loads(result.stdout)[0]
                #print(metadata) -> Je tam toho mnoho

                # Vytáhnout jen některé zajímavé klíče (přizpůsob dle potřeby)
                keys_of_interest = [
                    'FileName', 'FileType', 'ImageSize', 'CameraModelName',
                    'CreateDate', 'ISO', 'ExposureTime', 'FNumber', 'Lens'
                ]
                for key in keys_of_interest:
                    if key in metadata:
                        formated_metadata[key] = metadata[key]

            except subprocess.CalledProcessError as e:
                print("Chyba při volání exiftool:", e)
            except Exception as e:
                print("Obecná chyba:", e)

        return formated_metadata

#test
#x = extract_meta("test-files/raw-foto-test.CR3")

#print(x)

