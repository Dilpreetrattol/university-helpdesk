import os
from dotenv import load_dotenv

load_dotenv()

from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from groq import Groq as GroqClient
from llama_index.core.llms import CustomLLM, CompletionResponse, LLMMetadata
from llama_index.core.llms.callbacks import llm_completion_callback
from typing import Any, Generator

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
STORAGE_DIR = "./storage"

# ---- CUSTOM LLM WRAPPER (same as ingest.py) ----
class GroqLLM(CustomLLM):
    model_name: str = "groq/compound-mini"
    api_key: str = ""

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            model_name=self.model_name,
            num_output=1024,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        client = GroqClient(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return CompletionResponse(text=response.choices[0].message.content)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> Generator:
        raise NotImplementedError("Streaming not implemented")

# ---- MODELS ----
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = GroqLLM(api_key=GROQ_API_KEY)

Settings.llm = llm
Settings.embed_model = embed_model

# ---- LOAD INDEX ----
print("Loading index from disk...")
storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
index = load_index_from_storage(storage_context)
print("Index loaded successfully\n")

# ---- QUERY ENGINE ----
query_engine = index.as_query_engine(
    llm=llm,
    similarity_top_k=6
)

# ---- INTERACTIVE LOOP ----
while True:
    query = input("\nAsk a question (or type 'exit'): ").strip()
    if query.lower() == "exit":
        break

    response = query_engine.query(query)

    print("\n--- ANSWER ---")
    print(response)

    print("\n--- RETRIEVED CHUNKS (what the LLM was given) ---")
    for i, node in enumerate(response.source_nodes):
        print(f"\nSource {i+1} (score: {node.score:.4f}):")
        print(node.text[:300])
        print("-" * 40)