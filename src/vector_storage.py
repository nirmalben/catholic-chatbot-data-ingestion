from abc import ABC, abstractmethod

from models import Document
from typing import List

class VectorStorage(ABC):
    def __init__(self, documents: List[Document], embedding_model) -> None:
        self.documents = documents
        self.embedding_model = embedding_model
        self.collection = None
        self._load_storage()
  
    @abstractmethod
    def _load_storage(self) -> None:
        # Populates self.vector_store
        pass

    def get_vector_store(self):
        return self.collection