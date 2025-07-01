import subprocess
import json
import os
from plugins.base_extractor import BaseExtractor


class FotoExtractor(BaseExtractor):
    """
    Extraktor metadat pro obrazové soubory (.CR3, .png) využívající exiftool.

    Metadata jsou mapována na pole Dublin Core.
    """

    def __init__(self):
        """
        Inicializuje extraktor s podporou přípon .CR3 a .png.
        """
        self._supported_extensions = [".CR3", ".png"]

    @property
    def supported_extensions(self):
        """
        Vrací seznam podporovaných přípon souborů.

        Returns:
            list[str]: Seznam přípon, které extraktor podporuje.
        """
        return self._supported_extensions

    def extract_meta(self, file_path):
        """
        Extrahuje metadata ze zadaného obrazového souboru pomocí exiftool.

        Args:
            file_path (str): Cesta k souboru, ze kterého se extrahují metadata.

        Returns:
            dict: Slovník s klíči odpovídajícími Dublin Core metadatům.
                  Pokud je přípona souboru nepodporovaná nebo nastane chyba,
                  vrací slovník s prázdnými hodnotami.
        """
        extension = os.path.splitext(file_path)[1].upper()

        # Inicializace DC slovníku s prázdnými hodnotami
        dc_fields = {
            "title": "",
            "creator": "",
            "subject": "",
            "description": "",
            "publisher": "",
            "contributor": "",
            "date": "",
            "type": "Image",
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

        if extension in [".CR3", ".png"]:
            exiftool_path = os.path.join(os.path.dirname(__file__), '../tools/exiftool/exiftool.exe')

            try:
                result = subprocess.run(
                    [exiftool_path, '-json', file_path],
                    capture_output=True,
                    text=True,
                    check=True
                )
                metadata = json.loads(result.stdout)[0]

                # Mapování konkrétních EXIF klíčů na Dublin Core pole:
                dc_fields["title"] = metadata.get("FileName", "")
                dc_fields["creator"] = metadata.get("CameraModelName", "")
                dc_fields["subject"] = metadata.get("Subject", "")  # často chybí, ale pokud je, vložit
                dc_fields["description"] = ", ".join(filter(None, [
                    metadata.get("Lens", ""),
                    f"{metadata.get('ExposureTime', '')}s" if metadata.get("ExposureTime") else "",
                    f"ISO {metadata.get('ISO', '')}" if metadata.get("ISO") else "",
                    f"f/{metadata.get('FNumber', '')}" if metadata.get("FNumber") else ""
                ]))
                dc_fields["publisher"] = metadata.get("Publisher", "")  # EXIF často neobsahuje
                dc_fields["contributor"] = metadata.get("Software", "")
                dc_fields["date"] = metadata.get("CreateDate", "")
                dc_fields["type"] = "Image"
                dc_fields["format"] = metadata.get("FileType", extension)
                dc_fields["identifier"] = metadata.get("FileInodeNumber", "")  # nebo FileModifyDate, apod.
                dc_fields["source"] = metadata.get("SourceFile", "")
                dc_fields["language"] = metadata.get("Language", "")  # EXIF asi neobsahuje
                dc_fields["relation"] = metadata.get("RelatedImageFile", "")  # pokud existuje
                dc_fields["coverage"] = metadata.get("GPSPosition", "")  # souřadnice, pokud jsou
                dc_fields["rights"] = metadata.get("Rights", "")  # info o autorských právech

            except subprocess.CalledProcessError as e:
                print("Chyba při volání exiftool:", e)
            except Exception as e:
                print("Obecná chyba:", e)
        return dc_fields

