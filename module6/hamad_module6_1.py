# Module 6 - Exercise 01: My RAG
# Read a Word .doc file using Microsoft Word.
# Store text embeddings using LangChain.
# Retrieve the top 3 relevant chunks.
# Generate an answer using the retrieved context.

from pathlib import Path
import win32com.client

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama

# Configuration
BASE_DIR = Path(__file__).resolve().parent
DOC_FILE = BASE_DIR / "knowledge.doc"
INDEX_FILE = BASE_DIR / "hamad_module6_1_index.json"

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen2.5:0.5b"

# Step 1: Read the Word .doc file
def read_word_file(file_path):

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    document = None

    try:
        document = word.Documents.Open(
            str(file_path.resolve()),
            ReadOnly=True,
            AddToRecentFiles=False
        )

        return document.Content.Text.strip()

    finally:
        if document is not None:
            document.Close(SaveChanges=False)

        word.Quit()

# Step 2: Build or load the search index
def prepare_search():

    embeddings = OllamaEmbeddings(model=EMBED_MODEL)

    # Reuse saved index if the document has not changed
    if (
        INDEX_FILE.exists()
        and INDEX_FILE.stat().st_mtime >= DOC_FILE.stat().st_mtime
    ):
        print("Loading saved search index...")

        return InMemoryVectorStore.load(
            str(INDEX_FILE),
            embedding=embeddings
        )

    print("Reading Word document...")
    text = read_word_file(DOC_FILE)

    if not text:
        raise ValueError("The Word document is empty.")

    # Create a LangChain document
    document = Document(
        page_content=text,
        metadata={"source": DOC_FILE.name}
    )

    # Split into small searchable chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=350,
        chunk_overlap=50
    )

    chunks = splitter.split_documents([document])

    print("Total chunks:", len(chunks))

    # Create vector store
    store = InMemoryVectorStore(embedding=embeddings)
    store.add_documents(chunks)

    # Save index for future runs
    store.dump(str(INDEX_FILE))

    print("Search index saved successfully!")

    return store

# Step 3: Retrieve the 3 best matches
def search_document(store, question):

    results = store.similarity_search(
        query=question,
        k=3
    )

    print("\nTOP 3 SEARCH RESULTS")
    print("-" * 40)

    for number, document in enumerate(results, start=1):
        print(f"\nResult {number}:")
        print(document.page_content)

    return results

# Step 4: Generate an answer from the retrieved text
def generate_answer(question, results):

    context = "\n\n".join(
        document.page_content for document in results
    )

    llm = ChatOllama(
        model=CHAT_MODEL,
        temperature=0.2
    )

    messages = [
        (
            "system",
            "Answer using only the provided document context. "
            "If the answer is not present, say you cannot find it."
        ),
        (
            "human",
            f"Context:\n{context}\n\nQuestion: {question}"
        )
    ]

    response = llm.invoke(messages)

    return response.content

# Main program
def main():

    if not DOC_FILE.is_file():
        print("Error: knowledge.doc not found!")
        return

    print("Welcome to Hamad RAG Assistant!")

    try:
        store = prepare_search()

        while True:
            question = input("\nYour question (or exit): ").strip()

            if question.lower() == "exit":
                break

            if not question:
                continue

            results = search_document(store, question)

            print("\nAI ANSWER")
            print("-" * 40)

            answer = generate_answer(question, results)
            print(answer)

    except Exception as error:
        print("Error:", error)
        print("Check Word, Ollama and the installed models.")

if __name__ == "__main__":
    main()
