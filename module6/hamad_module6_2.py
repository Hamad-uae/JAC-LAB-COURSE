# Module 6 - Exercise 02: Chat RAG
# Combine Module 5 Exercise 07 (full chat) with Module 6 Exercise 01 (RAG).
# Retrieve the top 3 relevant chunks from knowledge.doc and use Ollama to answer.

import streamlit as st
from langchain_ollama import ChatOllama

# Reuse the working document reader, index, and embeddings from Exercise 01.
from hamad_module6_1 import DOC_FILE, prepare_search

CHAT_MODEL = "qwen2.5:0.5b"
TOP_K = 3

st.set_page_config(page_title="Hamad Chat RAG", page_icon="🤖")
st.title("🤖 Hamad Chat RAG")
st.caption("Streamlit + LangChain + Word document + Ollama")


@st.cache_resource
def load_search_index(document_modified_at):
    """Build or load the index; refresh it when the Word file changes."""
    return prepare_search()


if not DOC_FILE.is_file():
    st.error(f"Word document not found: {DOC_FILE}")
    st.stop()

try:
    vector_store = load_search_index(DOC_FILE.stat().st_mtime)
except Exception as exc:
    st.error(f"Unable to prepare the RAG search index: {exc}")
    st.stop()

# Keep the current conversation in Streamlit's session state.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def answer_with_rag(question, history):
    """Retrieve up to 3 document chunks and answer using chat history."""
    matches = vector_store.similarity_search(question, k=TOP_K)
    sources = [document.page_content for document in matches]

    if not sources:
        return "I could not find information in the document.", []

    context = "\n\n".join(
        f"Document excerpt {index}:\n{content}"
        for index, content in enumerate(sources, start=1)
    )

    system_prompt = (
        "You are a helpful document question-answering assistant. "
        "Answer factual questions using only the document excerpts below. "
        "Use prior chat messages to understand follow-up questions, but do not "
        "treat earlier AI answers as evidence. "
        "If the document does not contain the answer, say that you cannot "
        "find it in the document. Reply in the user's language.\n\n"
        f"Document excerpts:\n{context}"
    )

    messages = [("system", system_prompt)]
    # Keep some recent messages so follow-up questions have context.
    messages.extend(
        ("human" if message["role"] == "user" else "ai", message["content"])
        for message in history[-10:]
    )
    messages.append(("human", question))

    llm = ChatOllama(model=CHAT_MODEL, temperature=0.2)
    response = llm.invoke(messages)
    return str(response.content), sources


with st.sidebar:
    st.header("RAG Settings")
    st.write("LLM:", CHAT_MODEL)
    st.write("Document:", DOC_FILE.name)
    st.write("Top results:", TOP_K)
    st.write("Chat messages:", len(st.session_state.chat_history))

    if st.button("New Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Redisplay chat messages when Streamlit reruns the script.
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("Top 3 retrieved document excerpts"):
                for number, text in enumerate(message["sources"], start=1):
                    st.markdown(f"**Result {number}**")
                    st.text(text)

question = st.chat_input("Ask a question about knowledge.doc...")

if question and question.strip():
    question = question.strip()
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching the document and asking Ollama..."):
                answer, sources = answer_with_rag(
                    question, st.session_state.chat_history
                )

            st.write(answer)
            with st.expander("Top 3 retrieved document excerpts"):
                for number, text in enumerate(sources, start=1):
                    st.markdown(f"**Result {number}**")
                    st.text(text)

        except Exception as exc:
            st.error(f"RAG error: {exc}")
        else:
            # Save only successful question/answer pairs in chat history.
            st.session_state.chat_history.extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer, "sources": sources},
            ])
