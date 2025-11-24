#!/usr/bin/env python3
"""
Test script to demonstrate querying the PDF FAISS indexes.
"""

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


def test_pdf_indexes():
    """Test both PDF indexes with various queries."""
    print("Testing PDF FAISS Indexes")
    print("=" * 60)
    
    # Initialize embeddings
    print("Initializing Ollama embeddings...")
    embedding = OllamaEmbeddings(model="llama3")
    
    # Load both indexes
    print("Loading FAISS indexes...")
    handbook_store = FAISS.load_local(
        "faiss_handbook_index", 
        embedding, 
        allow_dangerous_deserialization=True
    )
    catalog_store = FAISS.load_local(
        "faiss_catalog_index", 
        embedding, 
        allow_dangerous_deserialization=True
    )
    print("✓ Both indexes loaded successfully\n")
    
    # Test queries for Handbook
    handbook_queries = [
        "What are the residence hall policies?",
        "What is the dress code?",
        "What are the rules about alcohol?",
        "How do I appeal a decision?"
    ]
    
    print("=" * 60)
    print("TESTING UNDERGRADUATE HANDBOOK")
    print("=" * 60)
    
    for query in handbook_queries:
        print(f"\n🔍 Query: {query}")
        results = handbook_store.similarity_search(query, k=2)
        
        for i, doc in enumerate(results, 1):
            content = doc.page_content[:200].replace('\n', ' ')
            print(f"   Result {i}: {content}...")
    
    # Test queries for Catalog
    catalog_queries = [
        "What are the general education requirements?",
        "What majors are available in business?",
        "What are the graduation requirements?",
        "How do I declare a minor?"
    ]
    
    print("\n" + "=" * 60)
    print("TESTING UNDERGRADUATE CATALOG")
    print("=" * 60)
    
    for query in catalog_queries:
        print(f"\n🔍 Query: {query}")
        results = catalog_store.similarity_search(query, k=2)
        
        for i, doc in enumerate(results, 1):
            content = doc.page_content[:200].replace('\n', ' ')
            print(f"   Result {i}: {content}...")
    
    print("\n" + "=" * 60)
    print("✅ Testing Complete!")
    print("=" * 60)
    print("\nBoth indexes are working correctly and ready for use in your chatbot.")


if __name__ == "__main__":
    test_pdf_indexes()