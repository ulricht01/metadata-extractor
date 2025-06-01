import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import plugins
import pkgutil
import importlib

from plugins.base_extractor import BaseExtractor

available_extractors = {}

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
                        

def extract_metadata(file_path):
    _, ext = os.path.splitext(file_path)
    
    if ext not in available_extractors:
        print(f"Žádný extraktor pro příponu: {ext}")
    
    try:
        extractor = available_extractors[ext]
        metadata = extractor.extract_meta(file_path)
        return metadata
    except Exception as e:
        return {}

if __name__ == "__main__":
    load_plugins()

    test_dir = "test-files"
    all_metadata = {}

    for filename in os.listdir(test_dir):
        file_path = os.path.join(test_dir, filename)
        if os.path.isfile(file_path):
            metadata = extract_metadata(file_path)
            all_metadata[filename] = metadata

    for file, metadata in all_metadata.items():
        print(f"{file}:")
        print(metadata)