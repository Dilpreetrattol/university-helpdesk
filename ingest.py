import os
from dotenv import load_dotenv

load_dotenv()

from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from google import genai as google_genai
from llama_index.core.llms import CustomLLM, CompletionResponse, LLMMetadata
from llama_index.core.llms.callbacks import llm_completion_callback
from typing import Any, Generator

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PDF_DIR = "./pdfs"
STORAGE_DIR = "./storage"

class GeminiLLM(CustomLLM):
    model_name: str = "gemini-3.5-flash-lite"
    api_key: str = ""

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(model_name=self.model_name, num_output=2048)

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        client = google_genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return CompletionResponse(text=response.text)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> Generator:
        raise NotImplementedError("Streaming not implemented")

embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = GeminiLLM(api_key=GEMINI_API_KEY)
Settings.llm = llm
Settings.embed_model = embed_model

print("Loading PDFs...")
documents = SimpleDirectoryReader(PDF_DIR, filename_as_id=True).load_data()

for doc in documents:
    raw_path = doc.metadata.get("file_path", "")
    clean_name = os.path.splitext(os.path.basename(raw_path))[0]
    doc.metadata["source"] = clean_name

print(f"Loaded {len(documents)} document chunks from PDFs")

from inject_tables import get_table_documents
table_docs = get_table_documents(PDF_DIR)
documents.extend(table_docs)
print(f"Injected {len(table_docs)} table documents")
print(f"Total documents: {len(documents)}")

splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
nodes = splitter.get_nodes_from_documents(documents)
print(f"Total chunks created: {len(nodes)}")

print("\n--- SAMPLE CHUNKS ---")
for i, node in enumerate(nodes[:3]):
    print(f"\nChunk {i+1}:")
    print(f"  Source: {node.metadata.get('source', 'MISSING')}")
    print(f"  Text preview: {node.text[:100]}...")

print("\nBuilding index and saving to disk...")
storage_context = StorageContext.from_defaults()
index = VectorStoreIndex(nodes, storage_context=storage_context)
index.storage_context.persist(persist_dir=STORAGE_DIR)
print(f"Index saved to {STORAGE_DIR}")