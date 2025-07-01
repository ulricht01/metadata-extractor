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
    """
    Extrahuje metadata z dokumentových formátů jako DOCX, ODT, PDF, RTF, TXT, XLSX a jejich variant.

    Podporované přípony: 
    .docx, .odt, .pdf, .rtf, .txt, .xlsx, .xlsm, .xltx, .xltm

    Metody:
        - supported_extensions: vrací seznam podporovaných přípon.
        - extract_meta: extrahuje metadata ze souboru a vrací je jako slovník Dublin Core polí.
    """
    
    def __init__(self):
        """
        Inicializuje extraktor a nastaví podporované přípony dokumentových souborů.
        """
        self._supported_extensions = [".docx", ".odt", ".pdf", ".rtf", ".txt", ".xlsx", ".xlsm", ".xltx", ".xltm"]
        
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
        Extrahuje metadata z dokumentového souboru podle jeho typu.

        Args:
            file_path (str): Cesta k dokumentovému souboru.

        Returns:
            dict: Slovník s metadaty dle Dublin Core polí, naplněný daty extrahovanými ze souboru.
                  Pokud není soubor podporován nebo nelze metadata získat, vrací výchozí prázdná pole.
        """
        def format_date(value):
            """
            Pomocná funkce pro formátování data do řetězce ve formátu 'DD.MM.YYYY HH:MM:SS'.

            Args:
                value (datetime.datetime|int|float): Datum jako datetime objekt nebo timestamp.

            Returns:
                str: Naformátovaný datumový řetězec, nebo prázdný řetězec pokud nelze konvertovat.
            """
            if isinstance(value, datetime.datetime):
                return value.strftime("%d.%m.%Y %H:%M:%S")
            elif isinstance(value, (int, float)):
                return datetime.datetime.fromtimestamp(value).strftime("%d.%m.%Y %H:%M:%S")
            return ""

        extension = os.path.splitext(file_path)[1].lower()
        
        dc_fields = {
            "title": "",
            "creator": "",
            "subject": "",
            "description": "",
            "publisher": "",
            "contributor": "",
            "date": "",
            "type": "",
            "format": "",
            "identifier": "",
            "source": "",
            "language": "",
            "relation": "",
            "coverage": "",
            "rights": ""
        }
        
        if extension not in self._supported_extensions:
            return dc_fields

        if extension == ".docx":
            file = docx.Document(file_path)
            core = file.core_properties

            dc_fields.update({
                "title": core.title or "",
                "creator": core.author or "",
                "subject": core.subject or "",
                "description": core.comments or "",
                "publisher": "",  
                "contributor": core.last_modified_by or "",
                "date": format_date(core.created),
                "type": "",  
                "format": extension,
                "identifier": core.identifier or "",
                "source": "",  
                "language": core.language or "",
                "relation": "",  
                "coverage": "",  
                "rights": "", 
            })

        elif extension == ".odt":
            file = odf.opendocument.load(file_path)
            for child in file.meta.childNodes:
                if isinstance(child, Element):
                    tag = child.qname[1].lower()
                    if tag in dc_fields:
                        dc_fields[tag] = child.firstChild.data if child.firstChild else ""

            dc_fields["format"] = extension

        elif extension == ".pdf":
            file = PyPDF2.PdfReader(file_path)
            core = file.metadata

            dc_fields.update({
                "title": getattr(core, "title", "") or "",
                "creator": getattr(core, "author", "") or "",
                "subject": getattr(core, "subject", "") or "",
                "description": getattr(core, "producer", "") or "",
                "publisher": "",
                "contributor": getattr(core, "creator", "") or "",
                "date": format_date(getattr(core, "creation_date", "")),
                "type": "",
                "format": extension,
                "identifier": "",
                "source": "",
                "language": "",
                "relation": "",
                "coverage": "",
                "rights": ""
            })

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
                            return ""
                    else:
                        tag_data = re.search(rf'{{\\{tag} (.*?)}}', content)
                        return tag_data.group(1) if tag_data else ""
                
                dc_fields.update({
                    "title": extract_tag("title"),
                    "creator": extract_tag("author"),
                    "subject": "",
                    "description": extract_tag("comment"),
                    "publisher": "",
                    "contributor": "",
                    "date": extract_tag("creatim"),
                    "type": "",
                    "format": extension,
                    "identifier": "",
                    "source": "",
                    "language": "",
                    "relation": "",
                    "coverage": "",
                    "rights": ""
                })

        elif extension == ".txt":
            file_metadata = os.stat(file_path)
            dc_fields.update({
                "title": os.path.basename(file_path),
                "creator": "",
                "subject": "",
                "description": "",
                "publisher": "",
                "contributor": "",
                "date": format_date(file_metadata.st_ctime),
                "type": "",
                "format": extension,
                "identifier": "",
                "source": "",
                "language": "",
                "relation": "",
                "coverage": "",
                "rights": ""
            })

        elif extension in [".xlsx", ".xlsm", ".xltx", ".xltm"]:
            file = openpyxl.load_workbook(file_path)
            core = file.properties

            dc_fields.update({
                "title": core.title or "",
                "creator": core.creator or "",
                "subject": core.subject or "",
                "description": core.description or "",
                "publisher": "",
                "contributor": core.lastModifiedBy or "",
                "date": format_date(core.created),
                "type": "",
                "format": extension,
                "identifier": core.identifier or "",
                "source": "",
                "language": core.language or "",
                "relation": "",
                "coverage": "",
                "rights": ""
            })

        return dc_fields
