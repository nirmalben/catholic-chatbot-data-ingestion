import jq
import json
import uuid
from models import Document
from document_loader import DocumentLoader

class JsonDocumentLoader(DocumentLoader):
    def _default_metadata_func(record: dict, metadata: dict) -> dict:
        metadata["id"] = record.get("id")
        if "from" in record:
            metadata["from"] = record["from"]
        return metadata

    def __init__(self, json_file_path: str, jq_schema='.[]', metadata_func=_default_metadata_func, content_key='text') -> None:
        self.jq_schema = jq_schema
        self.metadata_func = metadata_func
        self.content_key = content_key
        super().__init__(json_file_path)

    def _load(self) -> None:
        with open(self.file_path, "r", encoding='utf-8') as f:
            data = json.load(f)
        jq_data = jq.compile(self.jq_schema).input(data).all()
        for _, content in enumerate(jq_data):
            metadata = self.metadata_func(content, {})
            self.documents.append(Document(
                id=str(uuid.uuid4()),
                text=content[self.content_key],
                metadata=metadata
            ))