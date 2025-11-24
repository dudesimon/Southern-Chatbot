# Southern Adventist University Chatbot - PDF FAISS Indexes

## Step 3 (PDF Part) Complete: Two Separate FAISS Vector Databases Built

### 🎯 **Main Deliverable: `build_pdf_indexes.py`**

A comprehensive script that creates separate FAISS vector databases for the Undergraduate Handbook and Undergraduate Catalog.

---

## ✅ **What Was Built:**

### **1. PDF Text Extraction**
- ✅ Loaded `Undergraduate-Handbook-2025-2026.pdf` (41 pages, 249,923 characters)
- ✅ Loaded `Undergraduate-Catalog-2025-2026.pdf` (226 pages, 1,614,988 characters)
- ✅ Extracted all text using `pypdf` library

### **2. Text Chunking**
- ✅ Used `RecursiveCharacterTextSplitter` with:
  - `chunk_size = 1000`
  - `chunk_overlap = 200`
- ✅ **Handbook**: 319 chunks created (avg 932 chars/chunk)
- ✅ **Catalog**: 2,008 chunks created (avg 955 chars/chunk)

### **3. FAISS Vector Stores Created**
- ✅ Used Ollama embeddings with llama3 model
- ✅ Created two independent FAISS indexes:
  - **Handbook Store**: 319 vectors
  - **Catalog Store**: 2,008 vectors

### **4. Saved Locally**
- ✅ **Handbook Index**: `faiss_handbook_index/`
  - `index.faiss`: 5.2 MB
  - `index.pkl`: 333 KB
- ✅ **Catalog Index**: `faiss_catalog_index/`
  - `index.faiss`: 32.9 MB
  - `index.pkl`: 2.1 MB

---

## 📊 **Build Statistics:**

| Document | Pages | Characters | Chunks | Index Size |
|----------|-------|------------|--------|------------|
| **Undergraduate Handbook** | 41 | 249,923 | 319 | 5.6 MB |
| **Undergraduate Catalog** | 226 | 1,614,988 | 2,008 | 35.0 MB |

---

## 🔧 **Key Function:**

```python
from build_pdf_indexes import build_pdf_faiss_indexes

# Build both indexes
handbook_store, catalog_store = build_pdf_faiss_indexes()
```

---

## 🚀 **How to Use the Indexes:**

### **Loading the Indexes:**
```python
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# Initialize embeddings
embedding = OllamaEmbeddings(model="llama3")

# Load handbook index
handbook_store = FAISS.load_local(
    "faiss_handbook_index", 
    embedding, 
    allow_dangerous_deserialization=True
)

# Load catalog index
catalog_store = FAISS.load_local(
    "faiss_catalog_index", 
    embedding, 
    allow_dangerous_deserialization=True
)
```

### **Querying the Indexes:**
```python
# Search handbook for policies
results = handbook_store.similarity_search("residence hall policies", k=3)

# Search catalog for degree requirements
results = catalog_store.similarity_search("business major requirements", k=3)

# Access results
for doc in results:
    print(doc.page_content)
```

---

## ✅ **Testing Results:**

The script includes automatic testing that verified:
- ✅ Both indexes load successfully
- ✅ Queries return relevant results:
  - "academic policies" → Found relevant handbook content
  - "degree requirements" → Found relevant catalog content
  - "student conduct" → Found relevant handbook content

---

## 📁 **Files Created:**

1. **`build_pdf_indexes.py`** - Main script to build both indexes
2. **`test_pdf_indexes.py`** - Test script for querying indexes
3. **`faiss_handbook_index/`** - Handbook vector database
4. **`faiss_catalog_index/`** - Catalog vector database
5. **`PDF_FAISS_SUMMARY.md`** - This documentation

---

## 🎯 **Current Project Status:**

You now have **THREE** separate FAISS vector databases:

1. **Website Index** (`southern_faiss_index/`) - 13 chunks from southern.edu/undergrad
2. **Handbook Index** (`faiss_handbook_index/`) - 319 chunks from Undergraduate Handbook
3. **Catalog Index** (`faiss_catalog_index/`) - 2,008 chunks from Undergraduate Catalog

**Total**: 2,340 searchable text chunks covering:
- University website information
- Student handbook policies and procedures
- Academic catalog with degree requirements and course descriptions

---

## 🚀 **Ready for Step 4:**

Your vector databases are now ready for:
- Creating specialized agents (Handbook Agent, Catalog Agent, Website Agent)
- Building a LangGraph multi-agent system
- Implementing RAG-based question answering
- Integrating with Streamlit/Chainlit web interface

Each agent can now access its own specialized knowledge base to answer student questions about campus life, policies, and academic programs!

---

## 💡 **Example Use Cases:**

**Handbook Agent** can answer:
- "What are the residence hall quiet hours?"
- "What is the dress code policy?"
- "How do I appeal an academic decision?"

**Catalog Agent** can answer:
- "What are the requirements for a Biology major?"
- "What general education courses do I need?"
- "How many credits do I need to graduate?"

**Website Agent** can answer:
- "How do I schedule a campus visit?"
- "What undergraduate programs are available?"
- "How do I apply to Southern?"