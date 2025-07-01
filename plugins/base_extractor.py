from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """
    Abstraktní základní třída pro extraktory metadat z různých typů souborů.
    Definuje rozhraní, které musí implementovat konkrétní extraktory.
    """
    
    @abstractmethod
    def extract_meta(self, file_path: str) -> dict:
        """
        Extrahuje metadata ze souboru.

        Args:
            file_path (str): Cesta k souboru, ze kterého se mají metadata extrahovat.

        Returns:
            dict: Slovník obsahující extrahovaná metadata.
        """
        pass
    
    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """
        Vrací seznam přípon souborů, které extraktor podporuje.

        Returns:
            list[str]: Seznam přípon (např. ['.mp3', '.pdf', '.docx']).
        """
        pass
