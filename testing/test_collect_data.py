#!/usr/bin/env python3
"""
Test script for the data collection functionality.
"""

from collect_data import fetch_and_clean_pages


def test_data_collection():
    """Test the data collection with a small set of URLs."""
    print("Testing data collection functionality...")
    
    # Test URLs
    test_urls = [
        "https://www.southern.edu/undergrad"
    ]
    
    # Run the function
    results = fetch_and_clean_pages(test_urls)
    
    # Verify results
    print(f"\nTest Results:")
    print(f"- URLs processed: {len(test_urls)}")
    print(f"- Successful results: {len(results)}")
    
    if results:
        first_result = results[0]
        print(f"- First result source: {first_result['source']}")
        print(f"- First result content length: {len(first_result['content'])} characters")
        print(f"- Content preview: {first_result['content'][:200]}...")
        
        # Verify structure
        assert 'source' in first_result, "Missing 'source' key"
        assert 'content' in first_result, "Missing 'content' key"
        assert len(first_result['content']) > 0, "Empty content"
        
        print("✅ All tests passed!")
    else:
        print("❌ No results returned")


if __name__ == "__main__":
    test_data_collection()