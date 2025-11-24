#!/usr/bin/env python3
"""
Data Collection Script for Southern Adventist University Chatbot
Fetches and cleans web content from university pages.
"""

import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict
import sys


def fetch_and_clean_pages(urls: List[str]) -> List[Dict[str, str]]:
    """
    Fetch HTML content from URLs and extract clean text.
    
    Args:
        urls: List of URLs to process
        
    Returns:
        List of dictionaries with 'source' and 'content' keys
    """
    clean_texts = []
    
    # Request headers to appear as a regular browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for url in urls:
        try:
            print(f"Processing: {url}")
            
            # Fetch the page with timeout
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted tags
            unwanted_tags = ['script', 'style', 'nav', 'header', 'footer']
            for tag_name in unwanted_tags:
                for tag in soup.find_all(tag_name):
                    tag.decompose()
            
            # Extract visible text
            text = soup.get_text()
            
            # Clean up the text
            cleaned_text = clean_text(text)
            
            # Store the result
            clean_texts.append({
                'source': url,
                'content': cleaned_text
            })
            
            print(f"✓ Successfully processed: {url}")
            
            # Small delay to be respectful to the server
            time.sleep(1)
            
        except requests.exceptions.Timeout:
            print(f"✗ Timeout error for: {url}")
            continue
            
        except requests.exceptions.ConnectionError:
            print(f"✗ Connection error for: {url}")
            continue
            
        except requests.exceptions.HTTPError as e:
            print(f"✗ HTTP error for {url}: {e}")
            continue
            
        except Exception as e:
            print(f"✗ Unexpected error for {url}: {e}")
            continue
    
    return clean_texts


def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text.
    
    Args:
        text: Raw text from HTML
        
    Returns:
        Cleaned text string
    """
    # Split into lines and clean each line
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Strip whitespace
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Skip lines that are too short (likely navigation elements)
        if len(line) < 3:
            continue
            
        cleaned_lines.append(line)
    
    # Join lines with single spaces
    cleaned_text = ' '.join(cleaned_lines)
    
    # Remove multiple spaces
    while '  ' in cleaned_text:
        cleaned_text = cleaned_text.replace('  ', ' ')
    
    return cleaned_text.strip()


def print_summary(clean_texts: List[Dict[str, str]]) -> None:
    """
    Print a summary of the collected data.
    
    Args:
        clean_texts: List of processed page data
    """
    print("\n" + "="*60)
    print("DATA COLLECTION SUMMARY")
    print("="*60)
    
    print(f"Successfully processed: {len(clean_texts)} pages")
    
    if not clean_texts:
        print("No pages were successfully processed.")
        return
    
    print("\nPage previews:")
    print("-" * 40)
    
    for i, page_data in enumerate(clean_texts, 1):
        url = page_data['source']
        content = page_data['content']
        
        # Show first 300 characters
        preview = content[:300] + "..." if len(content) > 300 else content
        
        print(f"\n{i}. {url}")
        print(f"   Content length: {len(content)} characters")
        print(f"   Preview: {preview}")


def main():
    """Main function to run the data collection."""
    # URLs to process - starting with the provided URL
    urls = [
        "https://www.southern.edu/undergrad"
    ]
    
    print("Southern Adventist University Chatbot - Data Collection")
    print("="*60)
    print(f"Processing {len(urls)} URL(s)...")
    
    # Fetch and clean the pages
    clean_texts = fetch_and_clean_pages(urls)
    
    # Print summary
    print_summary(clean_texts)
    
    # Optional: Save to file for later use
    if clean_texts:
        print(f"\n💾 Data collected successfully!")
        print(f"   Use the 'clean_texts' variable in your next steps.")
        print(f"   Example: clean_texts[0]['content'] to access first page content")
    
    return clean_texts


if __name__ == "__main__":
    try:
        collected_data = main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        sys.exit(1)