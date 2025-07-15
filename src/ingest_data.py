from json_document_loader import JsonDocumentLoader
from qdrant_vector_storage import QdrantVectorStorage
from models import Document
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List

import itertools

parent_path = Path(__file__).resolve().parent.parent.as_posix()

def load_bible() -> List[Document]:
    def metadata_func(record: dict, metadata: dict) -> dict:
        metadata["book"] = record.get("book")
        metadata["chapter"] = record.get("chapter")
        metadata["verse"] = record.get("verse")
        metadata["from"] = "New American Bible (Revised Edition) (NABRE)"
        return metadata

    return JsonDocumentLoader(
        json_file_path=parent_path + '/data/nabre.json',
        metadata_func=metadata_func,
        jq_schema='.[] | . as $grandparent | .chapters[] | . as $parent | .verses[] | {book: $grandparent.book, chapter: $parent.chapter, verse: .verse, text: .text}'
    ).get_documents()

def load_documents() -> List[Document]:
    nabre_bible_doc = load_bible()

    catechism_doc = JsonDocumentLoader(
        json_file_path=parent_path + '/data/catechism.json',
        jq_schema='.[] | {id: (.id | tonumber), text: .text, from: "Catechism of the Catholic Church" }'
    ).get_documents()

    canon_doc = JsonDocumentLoader(
        json_file_path=parent_path + '/data/canon.json',
        jq_schema='.[] | if has("sections") then . as $section | .sections[] | {id: [($section.id | tostring), (.id | tostring)] | join(".") | tonumber, text: .text, from: "Canon law of the Catholic Church"} else {id: (.id | tonumber), text: .text, from: "Canon law of the Catholic Church" } end'
    ).get_documents()

    # General Instruction of the Roman Missal
    girm_doc = JsonDocumentLoader(
        json_file_path=parent_path + '/data/girm.json',
        jq_schema='.[] | {id: (.id | tonumber), text: .text, from: "General Instruction of the Roman Missal"}'
    ).get_documents() 

    documents = [nabre_bible_doc, catechism_doc, canon_doc, girm_doc]
    return list(itertools.chain(*documents)) # converts List[List[Documents]] to List[Documents]


print("Loading Documents...")
documents = load_documents()

print("Initialize embeddings...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Initialize vectorstore...")
vector_store = QdrantVectorStorage(documents=documents, embedding_model=embedding_model).get_vector_store()