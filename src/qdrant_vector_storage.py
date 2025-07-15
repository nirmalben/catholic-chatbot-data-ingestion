from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from typing import List
from models import Document
from vector_storage import VectorStorage
import os

class QdrantVectorStorage(VectorStorage):
    def __init__(self, documents: List[Document], embedding_model, collection_name="catholic") -> None:
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.documents = documents

        self.client = QdrantClient(
            url=os.environ["QDRANT_HOST"], 
            api_key=os.environ["QDRANT_API_KEY"]
        )

        super().__init__(documents=documents, embedding_model=embedding_model)

    def _load_storage(self) -> None:
        # Delete if exists
        try:
            self.client.delete_collection(collection_name=self.collection_name)
        except Exception:
            pass

        # Create new collection
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=self.embedding_model.get_sentence_embedding_dimension(), distance=Distance.COSINE)
        )

        print("Indexing documents...")

        batch_size = 1000
        for i in range(0, len(self.documents), batch_size):
            batch_docs = self.documents[i:i+batch_size]
            texts = [doc.text for doc in batch_docs]
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True).tolist()

            points = [
                PointStruct(
                    id=doc.id,
                    vector=vec,
                    payload=doc.metadata
                )
                for doc, vec in zip(batch_docs, embeddings)
            ]

            print(f"LOAD Documents of batch {i+batch_size} into vectorstore...")
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

        print("Qdrant vector storage load complete.")