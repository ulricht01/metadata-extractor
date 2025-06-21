import mutagen
import os
from plugins.base_extractor import BaseExtractor

class AudioExtractor(BaseExtractor):
    
    def __init__(self):
        self._supported_extensions = [".mp3", ".ogg"]
        
    @property
    def supported_extensions(self):
        return self._supported_extensions
        
    def extract_meta(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()
        
        dc_fields = {
            "title": "",
            "creator": "",
            "subject": "",
            "description": "",
            "publisher": "",
            "contributor": "",
            "date": "",
            "type": "Sound",
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

        file = mutagen.File(file_path)

        if file is None:
            return dc_fields

        if extension == ".ogg":
            dc_fields.update({
                "title": file.get("TITLE", [""])[0],
                "creator": file.get("ARTIST", [""])[0],
                "description": file.get("ALBUM", [""])[0],
                "publisher": file.get("ORGANIZATION", [""])[0],
                "contributor": file.get("PERFORMER", [""])[0],
                "date": file.get("DATE", [""])[0],
                "language": file.get("LANGUAGE", [""])[0],
                "rights": file.get("COPYRIGHT", [""])[0],
                 "subject": file.get("GENRE", [""])[0],
                "identifier": file.get("ISRC", [""])[0],
                "relation": file.get("RELATED", [""])[0],   # custom
                "source": file.get("SOURCE", [""])[0],
                "coverage": file.get("LOCATION", [""])[0]   # custom nebo vlastní pole
            })

        elif extension == ".mp3":
            for key, value in file.items():
                if key.startswith("TIT2"):
                    dc_fields["title"] = str(value)
                elif key.startswith("TPE1"):
                    dc_fields["creator"] = str(value)
                elif key.startswith("TALB"):
                    dc_fields["description"] = str(value)
                elif key.startswith("TPUB"):
                    dc_fields["publisher"] = str(value)
                elif key.startswith("TPE2"):
                    dc_fields["contributor"] = str(value)
                elif key.startswith("TDRC"):
                    dc_fields["date"] = str(value)
                elif key.startswith("TLAN"):
                    dc_fields["language"] = str(value)
                elif key.startswith("TCOP"):
                    dc_fields["rights"] = str(value)
                elif key.startswith("TCON"):  # genre → subject
                    dc_fields["subject"] = str(value)
                elif key.startswith("UFID") or key.startswith("TSRC"):
                    dc_fields["identifier"] = str(value)
                elif key.startswith("WOAR"):  # official artist website
                    dc_fields["source"] = str(value)
                elif key.startswith("WXXX"):  # user-defined URL
                    dc_fields["relation"] = str(value)
                elif key.startswith("TOWN"):  # place of recording
                    dc_fields["coverage"] = str(value)

        return dc_fields
