import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import plugins
import pkgutil
import importlib
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
import io
import json

from plugins.base_extractor import BaseExtractor

available_extractors = {}
dashboard_data = {
        "none": 0        
    }

def prepare_dashboard_dict():
    for i in available_extractors:
        dashboard_data[i] = 0

def report_dashboard(dashboard_data, output_path):
    template_path = os.path.join(os.path.dirname(__file__), "..", "dashboard", "dashboard.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
        
    html = template.replace("{{BARCHARTDATA}}", json.dumps(dashboard_data, ensure_ascii=False))

    
    output_file = os.path.join(output_path, "metadata_report.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"Dashboard vygenerován: {output_file}")

def load_plugins():
    for loader, module_name, is_pkg in pkgutil.iter_modules(plugins.__path__):
        module = importlib.import_module(f"plugins.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, BaseExtractor) and attr is not BaseExtractor:
                instance = attr()
                for ext in instance.supported_extensions:
                    if ext not in available_extractors:
                        available_extractors[ext] = instance
                        print(f"  Plugin '{attr.__name__}' zaregistrován pro příponu '{ext}'.")
    prepare_dashboard_dict()
                        

def extract_metadata(file_path):
    _, ext = os.path.splitext(file_path)
    
    if ext not in available_extractors:
        print(f"Žádný extraktor pro příponu: {ext}")
        dashboard_data["none"] +=1
    try:
        extractor = available_extractors[ext]
        metadata = extractor.extract_meta(file_path)
        dashboard_data[ext] +=1
        return metadata
    except Exception as e:
        return {}
    
def convert_to_xml(filename, metadata, export_path):
    # Ujisti se, že metadata je slovník s popisnými klíči
    xml_bytes = dicttoxml({}, custom_root="FILE", attr_type=False)
    data_element = ET.fromstring(xml_bytes.decode("utf-8"))
    
    data_element.set("path", str(os.path.abspath(filename)))

    dir_element = ET.Element("DIR", attrib={"path": str(os.path.abspath(""))})
    dir_element.append(data_element)
    
    metadata_element = ET.Element("METADATA")
    data_element.append(metadata_element)
    
    for key, value in metadata.items():
        child = ET.Element(key)
        if value is not None:
            child.text = str(value)
        else: 
            child.text = ""
        metadata_element.append(child)
    
    tree = ET.ElementTree(dir_element)

    f = io.BytesIO()
    tree.write(f, encoding='utf-8', xml_declaration=True)

    xml_pretty = parseString(f.getvalue()).toprettyxml(indent="  ")

    output_file = os.path.join(export_path, f"{os.path.splitext(os.path.basename(filename))[0]}.xml")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(xml_pretty)

    print(f"XML bylo uloženo do souboru: {output_file}")
    
def join_xml_files(export_path, output_file):
    dir_map = {}

    for root, _, files in os.walk(export_path):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                tree = ET.parse(file_path)
                root_elem = tree.getroot() 
                dir_path = root_elem.attrib.get('path')
                
                if dir_path not in dir_map:
                    new_dir_elem = ET.Element('DIR', {'path': dir_path})
                    dir_map[dir_path] = new_dir_elem

                for file_elem in root_elem.findall('FILE'):
                    dir_map[dir_path].append(file_elem)

    combined_root = ET.Element('DIRS')

    for dir_elem in dir_map.values():
        combined_root.append(dir_elem)


    combined_tree = ET.ElementTree(combined_root)
    combined_tree.write(output_file, encoding='utf-8', xml_declaration=True)

    
if __name__ == "__main__":
    load_plugins()

    test_dir = "test-files"
    all_metadata = {}

    for root, dirs, files in os.walk(test_dir):
        for file in files:
            full_path = os.path.join(root, file)
            metadata = extract_metadata(full_path)
            all_metadata[full_path] = metadata
    for file, metadata in all_metadata.items():
        print(f"{file}:")
        convert_to_xml(file, metadata, "exports")
        join_xml_files("exports", "G:/Programování/sipky/metadata-extractor/nested_exports/all.xml")
        report_dashboard(dashboard_data, "G:/Programování/sipky/metadata-extractor/exports/reports")


    