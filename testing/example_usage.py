#!/usr/bin/env python3
"""
Example usage of the collect_data module with multiple URLs.
This shows how to easily add more URLs later.
"""

from collect_data import fetch_and_clean_pages, print_summary


def main():
    """Example of using the data collection with multiple URLs."""
    
    # Example URLs - you can easily add more here later
    urls = [
        "https://www.southern.edu/undergrad",
        # Add more URLs here as needed:
        # "https://www.southern.edu/academics",
        # "https://www.southern.edu/admissions",
        # "https://www.southern.edu/campus-life",
    ]
    
    print("Example: Collecting data from Southern Adventist University")
    print("=" * 60)
    
    # Use the modular function
    clean_texts = fetch_and_clean_pages(urls)
    
    # Print summary
    print_summary(clean_texts)
    
    # Example of accessing the data
    if clean_texts:
        print("\n" + "=" * 60)
        print("EXAMPLE: How to access the collected data")
        print("=" * 60)
        
        print(f"Total pages collected: {len(clean_texts)}")
        print(f"First page URL: {clean_texts[0]['source']}")
        print(f"First page content length: {len(clean_texts[0]['content'])} characters")
        
        # Show how to iterate through all pages
        print("\nAll collected pages:")
        for i, page in enumerate(clean_texts, 1):
            print(f"  {i}. {page['source']} ({len(page['content'])} chars)")
    
    return clean_texts


if __name__ == "__main__":
    collected_data = main()