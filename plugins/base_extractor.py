from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    
    @abstractmethod
    def extract_meta(self, file_path: str) -> dict:
        """
        Vrací metadata ze souboru uvedeného v souborové cestě.
        """
        pass
    
    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """
        Vrací seznam podporvaných připon.
        """
        pass