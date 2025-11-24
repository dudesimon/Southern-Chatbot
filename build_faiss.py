#!/usr/bin/env python3
"""
FAISS Vector Database Builder for Southern Adventist University Chatbot
Splits text into chunks, creates embeddings, and builds a searchable vector store.
"""

import os
import sys
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document


def build_faiss_index(clean_texts: List[Dict[str, str]]) -> FAISS:
    """
    Build a FAISS vector database from cleaned text data.
    
    Args:
        clean_texts: List of dictionaries with 'source' and 'content' keys
        
    Returns:
        FAISS vectorstore object
    """
    print("Building FAISS Vector Database...")
    print("=" * 50)
    
    # Step 1: Initialize text splitter
    print("1. Initializing text splitter...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Step 2: Split texts into chunks while preserving source information
    print("2. Splitting texts into chunks...")
    documents = []
    total_chunks = 0
    
    for page_data in clean_texts:
        source_url = page_data['source']
        content = page_data['content']
        
        print(f"   Processing: {source_url}")
        
        # Split the content into chunks
        chunks = text_splitter.split_text(content)
        
        # Create Document objects with metadata
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    'source': source_url,
                    'chunk_id': i,
                    'total_chunks': len(chunks)
                }
            )
            documents.append(doc)
        
        chunk_count = len(chunks)
        total_chunks += chunk_count
        print(f"   Created {chunk_count} chunks from {source_url}")
    
    print(f"\n✓ Total text chunks created: {total_chunks}")
    
    # Step 3: Initialize Ollama embeddings
    print("\n3. Initializing Ollama embeddings...")
    try:
        embedding = OllamaEmbeddings(model="llama3")
        print("✓ Ollama embeddings initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing Ollama embeddings: {e}")
        print("Make sure Ollama is running and llama3 model is available")
        raise
    
    # Step 4: Create FAISS vector store
    print("\n4. Creating FAISS vector store...")
    print("   This may take a few minutes depending on the amount of text...")
    
    try:
        # Extract texts and metadatas for FAISS
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        # Create the vector store
        vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=embedding,
            metadatas=metadatas
        )
        
        print(f"✓ FAISS vector store created with {len(texts)} embeddings")
        
    except Exception as e:
        print(f"✗ Error creating FAISS vector store: {e}")
        raise
    
    # Step 5: Save the vector store locally
    print("\n5. Saving FAISS index locally...")
    index_path = "southern_faiss_index"
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(index_path, exist_ok=True)
        
        # Save the vector store
        vectorstore.save_local(index_path)
        
        print(f"✓ FAISS index saved successfully to: {index_path}/")
        
        # Verify the files were created
        expected_files = ['index.faiss', 'index.pkl']
        created_files = []
        
        for file in expected_files:
            file_path = os.path.join(index_path, file)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                created_files.append(f"{file} ({file_size:,} bytes)")
        
        if created_files:
            print("   Created files:")
            for file_info in created_files:
                print(f"   - {file_info}")
        
    except Exception as e:
        print(f"✗ Error saving FAISS index: {e}")
        raise
    
    return vectorstore


def load_faiss_index(index_path: str = "southern_faiss_index") -> FAISS:
    """
    Load a previously saved FAISS index.
    
    Args:
        index_path: Path to the saved FAISS index
        
    Returns:
        Loaded FAISS vectorstore object
    """
    print(f"Loading FAISS index from: {index_path}")
    
    try:
        # Initialize embeddings (needed for loading)
        embedding = OllamaEmbeddings(model="llama3")
        
        # Load the vector store
        vectorstore = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
        
        print("✓ FAISS index loaded successfully")
        return vectorstore
        
    except Exception as e:
        print(f"✗ Error loading FAISS index: {e}")
        raise


def test_vectorstore(vectorstore: FAISS, query: str = "undergraduate programs") -> None:
    """
    Test the vector store with a sample query.
    
    Args:
        vectorstore: FAISS vectorstore to test
        query: Test query string
    """
    print(f"\n6. Testing vector store with query: '{query}'")
    
    try:
        # Perform similarity search
        results = vectorstore.similarity_search(query, k=3)
        
        print(f"✓ Found {len(results)} similar documents")
        
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get('source', 'Unknown')
            chunk_id = doc.metadata.get('chunk_id', 'Unknown')
            content_preview = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
            
            print(f"\n   Result {i}:")
            print(f"   Source: {source}")
            print(f"   Chunk ID: {chunk_id}")
            print(f"   Content: {content_preview}")
        
    except Exception as e:
        print(f"✗ Error testing vector store: {e}")


def main():
    """Main function to demonstrate the FAISS building process."""
    # For demonstration, we'll import the clean_texts from collect_data
    # In practice, you would pass your actual clean_texts data
    
    try:
        from collect_data import fetch_and_clean_pages
        
        print("Southern Adventist University Chatbot - FAISS Builder")
        print("=" * 60)
        
        # Get sample data (you would replace this with your actual clean_texts)
        print("Collecting sample data...")
        urls = ["https://www.southern.edu/undergrad"]
        clean_texts = fetch_and_clean_pages(urls)
        
        if not clean_texts:
            print("No data collected. Cannot build FAISS index.")
            return None
        
        print(f"Using {len(clean_texts)} pages of data")
        
        # Build the FAISS index
        vectorstore = build_faiss_index(clean_texts)
        
        # Test the vector store
        test_vectorstore(vectorstore)
        
        print("\n" + "=" * 60)
        print("✅ FAISS Vector Database Build Complete!")
        print("=" * 60)
        print("Next steps:")
        print("1. Use load_faiss_index() to load the saved index")
        print("2. Use vectorstore.similarity_search(query) for retrieval")
        print("3. Integrate with your chatbot's retrieval system")
        
        return vectorstore
        
    except ImportError:
        print("Error: collect_data module not found.")
        print("Make sure you have the collect_data.py file in the same directory.")
        return None
    except Exception as e:
        print(f"Error in main execution: {e}")
        return None


if __name__ == "__main__":
    try:
        vectorstore = main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        sys.exit(1)