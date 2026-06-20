import faiss
import os

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
    load_index_from_storage,
)
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

DATA_DIR = "./data"
PERSIST_DIR = "./storage"

def build_or_load_index():
    # Local embedding model
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-base-en-v1.5"
    )

    # Local LLM via Ollama
    Settings.llm = Ollama(
        model="gpt-oss:20b",
        request_timeout=120.0
    )

    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        print("Loading existing index from storage...")

        vector_store = FaissVectorStore.from_persist_dir(PERSIST_DIR)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
            persist_dir=PERSIST_DIR,
        )
        index = load_index_from_storage(storage_context)
        return index

    print("Creating new index from local documents...")

    documents = SimpleDirectoryReader(DATA_DIR).load_data()

    # bge-base-en-v1.5 produces 768-dim embeddings
    d = 768
    faiss_index = faiss.IndexFlatL2(d)

    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
    )

    index.storage_context.persist(persist_dir=PERSIST_DIR)
    return index

def main():
    index = build_or_load_index()
    query_engine = index.as_query_engine(similarity_top_k=3)

    print("\nLocal RAG is ready. Type 'exit' to quit.\n")

    while True:
        q = input("Ask: ").strip()
        if q.lower() in {"exit", "quit"}:
            break

        response = query_engine.query(q)
        print("\nAnswer:\n", response, "\n")

if __name__ == "__main__":
    main()