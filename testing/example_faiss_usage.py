#!/usr/bin/env python3
"""
Example showing how to use build_faiss.py with your own clean_texts data.
"""

from build_faiss import build_faiss_index, load_faiss_index


def example_with_custom_data():
    """Example of using build_faiss_index with custom clean_texts data."""
    
    # Example clean_texts data (replace this with your actual data)
    clean_texts = [
        {
            "source": "https://www.southern.edu/housing",
            "content": "Southern Adventist University offers various housing options for students. Our residence halls provide a safe and supportive environment for learning and personal growth. Students can choose from traditional dormitory-style rooms or apartment-style living. All residence halls are equipped with modern amenities including Wi-Fi, laundry facilities, and study areas."
        },
        {
            "source": "https://www.southern.edu/academics",
            "content": "Southern offers over 60 undergraduate programs across various disciplines including business, education, health sciences, and liberal arts. Our faculty-to-student ratio ensures personalized attention and mentorship. Students benefit from hands-on learning experiences, internships, and research opportunities."
        }
    ]
    
    print("Example: Building FAISS Index with Custom Data")
    print("=" * 50)
    
    # Build the FAISS index
    vectorstore = build_faiss_index(clean_texts)
    
    # Test some queries
    test_queries = ["housing options", "academic programs", "student support"]
    
    print("\nTesting retrieval with custom data:")
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = vectorstore.similarity_search(query, k=1)
        
        if results:
            doc = results[0]
            print(f"  Best match from: {doc.metadata['source']}")
            print(f"  Content preview: {doc.page_content[:150]}...")


def example_loading_existing_index():
    """Example of loading and using an existing FAISS index."""
    
    print("\nExample: Loading Existing FAISS Index")
    print("=" * 40)
    
    try:
        # Load the existing index
        vectorstore = load_faiss_index("southern_faiss_index")
        
        # Perform a search
        query = "What programs does Southern offer?"
        results = vectorstore.similarity_search(query, k=3)
        
        print(f"Query: '{query}'")
        print(f"Found {len(results)} results:")
        
        for i, doc in enumerate(results, 1):
            print(f"\n  {i}. Source: {doc.metadata['source']}")
            print(f"     Content: {doc.page_content[:100]}...")
            
    except Exception as e:
        print(f"Error loading index: {e}")


if __name__ == "__main__":
    # Run examples
    example_with_custom_data()
    example_loading_existing_index()