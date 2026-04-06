📄 Personal Research Paper Q&A Project

This is a personal project I built to help me quickly get answers from research papers in PDF format. I wanted a tool that could read a PDF, understand its content, and answer questions without me having to go through the entire paper manually.

What I Did and Why:

**PDF Text Extraction**
Made the system extract text from any uploaded PDF so it could read and understand the content.
This allows the project to work with research papers in a usable format.

**Text Chunking**
Split the extracted text into smaller, overlapping sections called chunks.
This ensures each part is small enough to retrieve relevant information efficiently.

**Text Embedding**
Converted each chunk into a numerical representation (embedding) that captures its meaning.
This makes it possible to find answers based on the meaning of the text, not just keywords.

**Storing Data in ChromaDB**
Stored all embeddings and metadata in a local database called ChromaDB.
This made searching for relevant parts of the PDF fast and easy.

**Retrieving Relevant Chunks**
When I asked a question, the system could find the most relevant sections from the PDF.
This helps the answer be accurate and based on the content of the paper.

**Generating Answers Using a Local Language Model**
Used a local language model (llama3.2) to generate answers from the retrieved chunks.
If the answer wasn’t in the paper, the system would let me know instead of guessing.

**Interactive Web Interface**
Created a simple Streamlit interface to upload PDFs and ask questions easily.
This made the project easy to use, even for someone without programming knowledge.

Why I Built This

I built this project as a personal experiment to combine my interest in AI, natural language processing, and research productivity. It helps me:

Quickly get answers from long research papers.
Experiment with semantic search and local language models.
Learn how to integrate PDF processing, embeddings, and AI-based answer generation in one project.
Future Improvements
Support multiple PDF uploads at once.
Improve answer quality with more advanced language models.
Show the source chunks and metadata for transparency.
Highlight answers directly in the PDF.
