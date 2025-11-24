#!/usr/bin/env python3
"""
Test script to verify all dependencies are working correctly
for the Southern Adventist University Chatbot project.
"""

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing package imports...")
    
    try:
        import langchain
        print(f"✓ LangChain: {langchain.__version__}")
    except Exception as e:
        print(f"✗ LangChain: {e}")
    
    try:
        import langchain_community
        print(f"✓ LangChain Community: {langchain_community.__version__}")
    except Exception as e:
        print(f"✗ LangChain Community: {e}")
    
    try:
        import langgraph
        print(f"✓ LangGraph: Available")
    except Exception as e:
        print(f"✗ LangGraph: {e}")
    
    try:
        import ollama
        print(f"✓ Ollama: Available")
    except Exception as e:
        print(f"✗ Ollama: {e}")
    
    try:
        import faiss
        print(f"✓ FAISS: {faiss.__version__}")
    except Exception as e:
        print(f"✗ FAISS: {e}")
    
    try:
        import pypdf
        print(f"✓ PyPDF: {pypdf.__version__}")
    except Exception as e:
        print(f"✗ PyPDF: {e}")
    
    try:
        import bs4
        print(f"✓ BeautifulSoup4: {bs4.__version__}")
    except Exception as e:
        print(f"✗ BeautifulSoup4: {e}")
    
    try:
        import requests
        print(f"✓ Requests: {requests.__version__}")
    except Exception as e:
        print(f"✗ Requests: {e}")
    
    try:
        import streamlit
        print(f"✓ Streamlit: {streamlit.__version__}")
    except Exception as e:
        print(f"✗ Streamlit: {e}")
    
    # Gradio removed - using Streamlit instead
    
    try:
        import chainlit
        print(f"✓ Chainlit: Available")
    except Exception as e:
        print(f"✗ Chainlit: {e}")

def test_ollama():
    """Test Ollama connectivity."""
    print("\nTesting Ollama...")
    try:
        import ollama
        response = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': 'Say "Environment test successful!"'}]
        )
        print(f"✓ Ollama working: {response['message']['content']}")
        return True
    except Exception as e:
        print(f"✗ Ollama test failed: {e}")
        return False

def test_faiss():
    """Test FAISS vector database."""
    print("\nTesting FAISS...")
    try:
        import faiss
        import numpy as np
        
        # Create a simple test index
        dimension = 128
        index = faiss.IndexFlatL2(dimension)
        
        # Add some test vectors
        test_vectors = np.random.random((10, dimension)).astype('float32')
        index.add(test_vectors)
        
        # Search
        query = np.random.random((1, dimension)).astype('float32')
        distances, indices = index.search(query, 3)
        
        print(f"✓ FAISS working: Created index with {index.ntotal} vectors")
        return True
    except Exception as e:
        print(f"✗ FAISS test failed: {e}")
        return False

if __name__ == "__main__":
    print("Southern Adventist University Chatbot - Environment Test")
    print("=" * 60)
    
    test_imports()
    ollama_ok = test_ollama()
    faiss_ok = test_faiss()
    
    print("\n" + "=" * 60)
    if ollama_ok and faiss_ok:
        print("🎉 All tests passed! Environment is ready for development.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")