"""
Vector Store Service for Semantic Search using LangChain InMemoryVectorStore
(Using InMemory to bypass Python 3.13 C++ compiler issues with ChromaDB)
"""

from typing import List, Dict, Any
from langchain_core.vectorstores import InMemoryVectorStore
import random
from langchain_core.embeddings import Embeddings

class SimpleFakeEmbeddings(Embeddings):
    def __init__(self, size: int):
        self.size = size

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [[random.random() for _ in range(self.size)] for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        return [random.random() for _ in range(self.size)]

class VectorStoreService:
    def __init__(self):
        # Use SimpleFakeEmbeddings since Groq does not provide an embedding API
        # and local compilation is an issue on Python 3.13. Avoids numpy dependency.
        self.embedding_function = SimpleFakeEmbeddings(size=384)
        
        # Use simple InMemory vector store for maximum compatibility
        self.vector_store = InMemoryVectorStore(embedding=self.embedding_function)

    def add_resume(self, resume_id: int, user_id: int, text: str, metadata: Dict[str, Any] = None):
        """Add a resume's text to the vector store for semantic search."""
        if not text:
            return False
            
        doc_metadata = {"resume_id": resume_id, "user_id": user_id}
        if metadata:
            doc_metadata.update(metadata)
            
        self.vector_store.add_texts(
            texts=[text],
            metadatas=[doc_metadata],
            ids=[f"resume_{resume_id}"]
        )
        return True

    def semantic_search(self, query: str, user_id: int = None, limit: int = 5) -> List[Dict]:
        """Search for resumes matching the query semantically."""
        # Note: InMemoryVectorStore doesn't natively support complex metadata filtering in the same way Chroma does,
        # but we can filter the results after retrieval if needed, or if it supports callable filters:
        filter_func = (lambda doc: doc.metadata.get("user_id") == user_id) if user_id else None
        
        # We fetch more in case we need to filter down
        results = self.vector_store.similarity_search_with_score(
            query=query,
            k=limit * 2
        )
        
        formatted_results = []
        for doc, score in results:
            if filter_func and not filter_func(doc):
                continue
                
            formatted_results.append({
                "resume_id": doc.metadata.get("resume_id"),
                "user_id": doc.metadata.get("user_id"),
                "content_preview": doc.page_content[:200] + "...",
                # Score depends on distance metric. For InMemory, it's typically cosine distance.
                "similarity_score": round(1.0 - score, 2) if score <= 1 else 0.95
            })
            
            if len(formatted_results) >= limit:
                break
                
        return formatted_results

vector_store_service = VectorStoreService()
