import streamlit as st
import fitz
from sentence_transformers import SentenceTransformer
import chromadb
import subprocess

# ---------- Helper functions ----------

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF using PyMuPDF."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    full_text = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        if text.strip():
            full_text.append(f"[Page {page_num}]\n{text}")

    doc.close()
    return "\n".join(full_text)

def chunk_text(text, chunk_size=300, overlap=50):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

# ---------- Initialize embeddings & ChromaDB collection ----------

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection_name = "research_papers"
collection = client.get_or_create_collection(name=collection_name)

def get_embedding(text):
    """Return embedding as a list for ChromaDB."""
    return model.encode(text).tolist()

def add_chunks_to_collection(chunks):
    """Add text chunks to ChromaDB with proper metadata."""
    if not chunks:
        st.warning("No text chunks to insert into the collection!")
        return

    ids = [str(i) for i in range(len(chunks))]
    documents = chunks
    # Make sure metadata is non-empty for every chunk
    metadatas = [{"source": "uploaded_pdf", "chunk_index": i} for i in range(len(chunks))]

    # Debug: print first 3 chunks
    for i in range(min(3, len(chunks))):
        print(f"Chunk {i}: {chunks[i][:50]}...")
        print(f"Metadata: {metadatas[i]}")

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    st.success(f"Inserted {len(chunks)} chunks into collection with metadata.")

def retrieve_chunks(question, top_k=3):
    """Retrieve relevant chunks from ChromaDB using semantic search."""
    query_embedding = get_embedding(question)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]  # Returns a list of chunks

def generate_answer_local(question, retrieved_chunks, model_path=r"C:\Users\kruta\AppData\Local\Programs\Ollama\ollama.exe", model_name="llama3.2"):
    """Generate answer from local LLM using subprocess."""
    context = "\n\n".join(retrieved_chunks)
    prompt = f"""
You are a research paper assistant.
Answer the question using only the context below.
If the answer is not in the context, say:
"I could not find the answer in the provided paper."

Context:
{context}

Question:
{question}
"""
    result = subprocess.run(
        [model_path, "run", model_name],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()

# ---------- Streamlit UI ----------

st.title("📄 Research Paper Q&A")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    if text.strip():  # Ensure PDF has readable text
        chunks = chunk_text(text)
        add_chunks_to_collection(chunks)

        question = st.text_input("Ask a question about the paper:")

        if question:
            retrieved_chunks = retrieve_chunks(question)
            answer = generate_answer_local(question, retrieved_chunks)
            st.subheader("Answer:")
            st.write(answer)
    else:
        st.error("The uploaded PDF has no readable text!")