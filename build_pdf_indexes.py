#!/usr/bin/env python3
"""
PDF FAISS Index Builder for Southern Adventist University Chatbot
Creates separate FAISS vector databases for Undergraduate Handbook and Catalog.
"""

import os
import sys
from typing import Tuple, List
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


def load_pdf(pdf_path: str) -> str:
    """
    Load and extract text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a single string
    """
    print(f"Loading PDF: {pdf_path}")
    
    try:
        reader = PdfReader(pdf_path)
        text = ""
        
        # Extract text from all pages
        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            text += page_text + "\n"
        
        print(f"✓ PDF loaded successfully")
        print(f"  - Total pages: {len(reader.pages)}")
        print(f"  - Total characters: {len(text):,}")
        
        return text
        
    except FileNotFoundError:
        print(f"✗ Error: PDF file not found at {pdf_path}")
        raise
    except Exception as e:
        print(f"✗ Error loading PDF: {e}")
        raise


def split_text_into_chunks(text: str, doc_name: str) -> List[str]:
    """
    Split text into chunks using RecursiveCharacterTextSplitter.
    
    Args:
        text: Text to split
        doc_name: Name of document for logging
        
    Returns:
        List of text chunks
    """
    print(f"\nSplitting {doc_name} into chunks...")
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Split the text
    chunks = text_splitter.split_text(text)
    
    print(f"✓ Created {len(chunks)} chunks from {doc_name}")
    
    # Show sample chunk info
    if chunks:
        avg_length = sum(len(chunk) for chunk in chunks) / len(chunks)
        print(f"  - Average chunk length: {avg_length:.0f} characters")
        print(f"  - First chunk preview: {chunks[0][:100]}...")
    
    return chunks


def create_faiss_index(chunks: List[str], doc_name: str) -> FAISS:
    """
    Create a FAISS vector store from text chunks.
    
    Args:
        chunks: List of text chunks
        doc_name: Name of document for logging
        
    Returns:
        FAISS vectorstore object
    """
    print(f"\nCreating FAISS index for {doc_name}...")
    
    try:
        # Initialize Ollama embeddings
        print("  - Initializing Ollama embeddings (llama3)...")
        embedding = OllamaEmbeddings(model="llama3")
        
        # Create FAISS vector store
        print(f"  - Embedding {len(chunks)} chunks (this may take a few minutes)...")
        vectorstore = FAISS.from_texts(chunks, embedding)
        
        print(f"✓ FAISS index created successfully for {doc_name}")
        print(f"  - Total vectors: {len(chunks)}")
        
        return vectorstore
        
    except Exception as e:
        print(f"✗ Error creating FAISS index: {e}")
        raise


def save_faiss_index(vectorstore: FAISS, save_path: str, doc_name: str) -> None:
    """
    Save FAISS index to local directory.
    
    Args:
        vectorstore: FAISS vectorstore to save
        save_path: Directory path to save the index
        doc_name: Name of document for logging
    """
    print(f"\nSaving FAISS index for {doc_name}...")
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        
        # Save the vector store
        vectorstore.save_local(save_path)
        
        print(f"✓ FAISS index saved successfully to: {save_path}/")
        
        # Verify files were created
        index_file = os.path.join(save_path, "index.faiss")
        pkl_file = os.path.join(save_path, "index.pkl")
        
        if os.path.exists(index_file) and os.path.exists(pkl_file):
            index_size = os.path.getsize(index_file)
            pkl_size = os.path.getsize(pkl_file)
            print(f"  - index.faiss: {index_size:,} bytes")
            print(f"  - index.pkl: {pkl_size:,} bytes")
        
    except Exception as e:
        print(f"✗ Error saving FAISS index: {e}")
        raise


def build_pdf_faiss_indexes() -> Tuple[FAISS, FAISS]:
    """
    Main function to build FAISS indexes for both PDF documents.
    
    Returns:
        Tuple of (handbook_store, catalog_store)
    """
    print("=" * 60)
    print("Building FAISS Indexes for PDF Documents")
    print("=" * 60)
    
    # Define PDF paths
    handbook_pdf = "pdf/Undergraduate-Handbook-2025-2026.pdf"
    catalog_pdf = "pdf/Undergraduate-Catalog-2025-2026.pdf"
    
    # Define save paths
    handbook_index_path = "faiss_handbook_index"
    catalog_index_path = "faiss_catalog_index"
    
    # ========================================
    # STEP 1: Load PDFs
    # ========================================
    print("\n" + "=" * 60)
    print("STEP 1: Loading PDF Documents")
    print("=" * 60)
    
    handbook_text = load_pdf(handbook_pdf)
    catalog_text = load_pdf(catalog_pdf)
    
    # ========================================
    # STEP 2: Split into chunks
    # ========================================
    print("\n" + "=" * 60)
    print("STEP 2: Splitting Text into Chunks")
    print("=" * 60)
    
    handbook_chunks = split_text_into_chunks(handbook_text, "Undergraduate Handbook")
    catalog_chunks = split_text_into_chunks(catalog_text, "Undergraduate Catalog")
    
    # ========================================
    # STEP 3: Create FAISS indexes
    # ========================================
    print("\n" + "=" * 60)
    print("STEP 3: Creating FAISS Vector Stores")
    print("=" * 60)
    
    handbook_store = create_faiss_index(handbook_chunks, "Undergraduate Handbook")
    catalog_store = create_faiss_index(catalog_chunks, "Undergraduate Catalog")
    
    # ========================================
    # STEP 4: Save FAISS indexes
    # ========================================
    print("\n" + "=" * 60)
    print("STEP 4: Saving FAISS Indexes")
    print("=" * 60)
    
    save_faiss_index(handbook_store, handbook_index_path, "Undergraduate Handbook")
    save_faiss_index(catalog_store, catalog_index_path, "Undergraduate Catalog")
    
    # ========================================
    # Summary
    # ========================================
    print("\n" + "=" * 60)
    print("✅ PDF FAISS INDEXES BUILD COMPLETE!")
    print("=" * 60)
    
    print("\nSummary:")
    print(f"  📚 Undergraduate Handbook:")
    print(f"     - Chunks: {len(handbook_chunks)}")
    print(f"     - Index saved to: {handbook_index_path}/")
    
    print(f"\n  📚 Undergraduate Catalog:")
    print(f"     - Chunks: {len(catalog_chunks)}")
    print(f"     - Index saved to: {catalog_index_path}/")
    
    print("\nNext Steps:")
    print("  1. Use these indexes in your chatbot agents")
    print("  2. Load indexes with: FAISS.load_local(path, embeddings)")
    print("  3. Query with: vectorstore.similarity_search(query, k=3)")
    
    return handbook_store, catalog_store


def test_indexes():
    """Test the created indexes with sample queries."""
    print("\n" + "=" * 60)
    print("Testing FAISS Indexes")
    print("=" * 60)
    
    try:
        # Initialize embeddings
        embedding = OllamaEmbeddings(model="llama3")
        
        # Load both indexes
        print("\nLoading indexes...")
        handbook_store = FAISS.load_local("faiss_handbook_index", embedding, allow_dangerous_deserialization=True)
        catalog_store = FAISS.load_local("faiss_catalog_index", embedding, allow_dangerous_deserialization=True)
        
        print("✓ Both indexes loaded successfully")
        
        # Test queries
        test_queries = [
            ("academic policies", "Handbook"),
            ("degree requirements", "Catalog"),
            ("student conduct", "Handbook")
        ]
        
        for query, doc_type in test_queries:
            print(f"\n🔍 Query: '{query}' (searching {doc_type})")
            
            store = handbook_store if doc_type == "Handbook" else catalog_store
            results = store.similarity_search(query, k=1)
            
            if results:
                content = results[0].page_content[:150] + "..."
                print(f"   Result: {content}")
        
        print("\n✅ Index testing complete!")
        
    except Exception as e:
        print(f"✗ Error testing indexes: {e}")


def main():
    """Main execution function."""
    try:
        # Build the indexes
        handbook_store, catalog_store = build_pdf_faiss_indexes()
        
        # Test the indexes
        test_indexes()
        
        return handbook_store, catalog_store
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()