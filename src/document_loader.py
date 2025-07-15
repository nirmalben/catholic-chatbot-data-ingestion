from abc import ABC, abstractmethod

from models import Document
from typing import List

class DocumentLoader(ABC):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.documents = []
        self._load()
  
    @abstractmethod
    def _load(self) -> None:
        # Populates self.documents
        pass

    def get_documents(self) -> List[Document]:
        return self.documents