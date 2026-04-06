#!/usr/bin/env python
# coding: utf-8

# In[5]:


# pip install anthropic chromadb sentence-transformers


# In[6]:


# Let's use a simple text file for now
# Save this as "my_doc.txt" and put whatever text you want in it

with open("rag_doc.rtf", "r") as f:
    text = f.read()

print(f"Loaded {len(text)} characters")


# In[7]:


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # overlap keeps context between chunks
    return chunks

chunks = chunk_text(text)
print(f"Created {len(chunks)} chunks")
print(f"\nFirst chunk preview:\n{chunks[0][:200]}")
print(f"\nSecond chunk preview:\n{chunks[1][:400]}")


# In[ ]:





# In[8]:


from sentence_transformers import SentenceTransformer

# This model runs locally, no API key needed
embedder = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = embedder.encode(chunks)
print(f"Each embedding shape: {embeddings[0].shape}")
# You'll see something like (384,) — 384 numbers per chunk


# In[ ]:





# In[ ]:




