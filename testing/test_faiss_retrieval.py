#!/usr/bin/env python3
"""
Test script to demonstrate FAISS retrieval functionality.
"""

from build_faiss import load_faiss_index


def test_retrieval():
    """Test the FAISS retrieval with various queries."""
    print("Testing FAISS Retrieval System")
    print("=" * 40)
    
    try:
        # Load the saved FAISS index
        vectorstore = load_faiss_index()
        
        # Test queries related to Southern Adventist University
        test_queries = [
            "undergraduate programs",
            "campus visit",
            "admissions requirements",
            "student life",
            "academic support"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: '{query}'")
            print("-" * 30)
            
            # Perform similarity search
            results = vectorstore.similarity_search(query, k=2)
            
            for i, doc in enumerate(results, 1):
                source = doc.metadata.get('source', 'Unknown')
                chunk_id = doc.metadata.get('chunk_id', 'Unknown')
                content = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                
                print(f"  Result {i}:")
                print(f"    Source: {source}")
                print(f"    Chunk: {chunk_id}")
                print(f"    Content: {content}")
                print()
        
        print("✅ Retrieval test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during retrieval test: {e}")


if __name__ == "__main__":
    test_retrieval()