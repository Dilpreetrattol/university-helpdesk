import os
import time
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from llama_index.core.schema import QueryBundle
from llama_index.core import Settings, StorageContext, load_index_from_storage, PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from google import genai as google_genai
from llama_index.core.llms import CustomLLM, CompletionResponse, LLMMetadata
from llama_index.core.llms.callbacks import llm_completion_callback
from typing import Any, Generator

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
STORAGE_DIR = "./storage"

SUGGESTED_TOPICS = [
    "Hostel fees",
    "Scholarships",
    "Branch-wise seats",
    "Refund policy",
]


# ---- CUSTOM LLM ----
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


# ---- SYSTEM PROMPT ----
SYSTEM_PROMPT = PromptTemplate(
    "You are a helpful assistant for first-year students (freshers) at Thapar Institute of Engineering and Technology (TIET), Patiala.\n\n"
    "Your job is to answer questions strictly based on the official TIET documents provided to you as context.\n\n"
    "Rules you must follow:\n"
    "- Only answer using information present in the context below.\n"
    "- If the answer is not in the context, say exactly: I do not have that information in the documents I was given. Please contact the TIET administration directly.\n"
    "- Do not use any general knowledge or outside information.\n"
    "- Keep answers clear, concise, and helpful for a fresher who is new to the campus.\n"
    "- If the question is about fees, rules, or deadlines, be precise and quote the relevant detail directly.\n"
    "- When referencing information, mention which document it comes from.\n"
    "- If the user refers to something mentioned earlier in the conversation, use that context to understand their question.\n\n"
    "Previous conversation:\n"
    "{conversation_history}\n\n"
    "Context from documents:\n"
    "{context_str}\n\n"
    "Current question: {query_str}\n\n"
    "Answer:"
)

FOLLOWUP_TRIGGERS = ["and for", "what about", "and what", "tell me about", "name them", "list them"]


# ---- LOAD INDEX ----
@st.cache_resource(show_spinner=False)
def load_query_engine():
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    llm = GeminiLLM(api_key=GEMINI_API_KEY)
    Settings.llm = llm
    Settings.embed_model = embed_model

    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    index = load_index_from_storage(storage_context)

    return index.as_query_engine(
        llm=llm,
        similarity_top_k=6,
        text_qa_template=SYSTEM_PROMPT,
        response_mode="simple_summarize"
    )


# ---- RETRY LOGIC ----
def query_with_retry(query_engine, query, retrieval_text=None, max_retries=3):
    bundle = QueryBundle(query_str=query, custom_embedding_strs=[retrieval_text or query])
    for attempt in range(max_retries):
        try:
            return query_engine.query(bundle)
        except Exception as e:
            err = str(e).lower()
            if "429" in str(e) or "rate_limit" in err or "quota" in err or "resource_exhausted" in err:
                wait_time = 5 * (attempt + 1)
                st.warning(f"API limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    return None


def build_query_with_history(prompt, messages):
    """Attach recent conversation turns as context, expanding vague follow-ups."""
    recent = messages[:-1][-4:]
    conversation_history = ""
    for msg in recent:
        role = "User" if msg["role"] == "user" else "Assistant"
        content = msg["content"][:400] if msg["role"] == "assistant" else msg["content"]
        conversation_history += f"{role}: {content}\n"

    if not conversation_history:
        return prompt

    is_followup = any(prompt.lower().startswith(t) for t in FOLLOWUP_TRIGGERS)
    if is_followup:
        return (
            f"{prompt}\n\n"
            f"[Conversation so far:\n{conversation_history}]\n\n"
            f"Note: Answer the current question in the context of the ongoing conversation. "
            f"The topic being discussed is TIET hostels, fees, facilities, and scholarships for students."
        )
    return f"{prompt}\n\n[Conversation so far:\n{conversation_history}]"


def render_sources(sources):
    if not sources:
        return
    with st.expander(f"View sources ({len(sources)})", icon=":material/description:"):
        for src in sources:
            score = src.get("score")
            score_text = f"{score:.4f}" if isinstance(score, (int, float)) else "n/a"
            st.markdown(f"**{src['source']}** — relevance score: {score_text}")
            st.caption(src["text"])
            st.divider()


# ---- UI ----
st.set_page_config(page_title="TIET Fresher Help Desk", page_icon="🎓", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

with st.sidebar:
    st.subheader("TIET Fresher Help Desk")
    st.caption(
        "Answers are drawn only from official TIET admission, fee, hostel, and policy documents — "
        "not general knowledge."
    )
    st.divider()
    st.caption("Try asking")
    for topic in SUGGESTED_TOPICS:
        if st.button(topic, width="stretch"):
            st.session_state.pending_prompt = topic
    st.divider()
    if st.button("Clear conversation", icon=":material/delete:", width="stretch"):
        st.session_state.messages = []
        st.rerun()

st.title("🎓 TIET Fresher Help Desk")
st.caption("Ask anything about hostels, fees, academics, or campus life.")

if not GEMINI_API_KEY:
    st.error(
        "GEMINI_API_KEY is not set. Add it to your .env file (see .env.example) before using the assistant.",
        icon=":material/key_off:",
    )
    st.stop()

try:
    with st.spinner("Loading knowledge base..."):
        query_engine = load_query_engine()
except Exception as e:
    st.error(
        f"Could not load the knowledge base from `{STORAGE_DIR}`: {e}\n\n"
        "Run `python ingest.py` first to build the index from the PDFs in `pdfs/`.",
        icon=":material/error:",
    )
    st.stop()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        render_sources(msg.get("sources"))

# Chat input
prompt = st.chat_input("Type your question here...", key="main_input")
if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            query_with_history = build_query_with_history(prompt, st.session_state.messages)
            # Embed only the question (plus the previous user turn for vague follow-ups),
            # so earlier answers don't pull retrieval toward the old topic.
            retrieval_text = prompt
            if any(prompt.lower().startswith(t) for t in FOLLOWUP_TRIGGERS):
                prev_user = [m["content"] for m in st.session_state.messages[:-1] if m["role"] == "user"]
                if prev_user:
                    retrieval_text = f"{prev_user[-1]} {prompt}"
            response = query_with_retry(query_engine, query_with_history, retrieval_text)

        if response is None:
            answer = "I am temporarily unavailable due to API rate limits. Please wait 30 seconds and try again."
            st.warning(answer)
            sources = []
        else:
            answer = str(response)
            st.markdown(answer)

            sources = [
                {
                    "source": node.metadata.get("source", "Unknown document"),
                    "score": node.score,
                    "text": node.text[:400],
                }
                for node in response.source_nodes
            ]
            render_sources(sources)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })
