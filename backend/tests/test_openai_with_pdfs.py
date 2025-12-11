"""
Integration test for OpenAI service with real PDF documents.

This test demonstrates the full pipeline:
1. Load PDF from your local computer
2. Extract and chunk text
3. Generate podcast dialogue from the content

Run this test with your own PDF files!
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.document_processor import extract_text_from_pdf, chunk_text
from services.openai_service import generate_podcast_dialogue


def test_with_pdf_file(pdf_path: str, topic: str = None):
    """
    Test OpenAI service with a real PDF file.
    
    Args:
        pdf_path: Path to your PDF file (can be absolute or relative)
        topic: Optional topic override (if None, will use filename)
    
    Example usage:
        python test_openai_with_pdfs.py /path/to/your/document.pdf "Machine Learning"
    """
    print("\n" + "="*60)
    print("OPENAI SERVICE - PDF INTEGRATION TEST")
    print("="*60)
    
    pdf_file = Path(pdf_path)
    
    if not pdf_file.exists():
        print(f"❌ ERROR: File not found: {pdf_path}")
        print(f"   Please provide a valid path to a PDF file")
        return False
    
    if not pdf_file.suffix.lower() == '.pdf':
        print(f"❌ ERROR: File is not a PDF: {pdf_path}")
        return False
    
    print(f"\n📄 PDF File: {pdf_file.name}")
    print(f"   Path: {pdf_file.absolute()}")
    
    if not topic:
        topic = pdf_file.stem.replace('_', ' ').replace('-', ' ').title()
    
    print(f"   Topic: {topic}")
    
    print("\n🔍 Step 1: Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_file)
    
    if not text:
        print("❌ ERROR: Could not extract text from PDF")
        print("   The PDF might be empty, image-based, or corrupted")
        return False
    
    print(f"✓ Extracted {len(text)} characters")
    print(f"   Preview: {text[:200]}...")
    
    print("\n✂️  Step 2: Chunking text...")
    chunks = chunk_text(text)
    
    if not chunks:
        print("❌ ERROR: No chunks created from text")
        return False
    
    print(f"✓ Created {len(chunks)} chunks")
    print(f"   First chunk preview: {chunks[0][:150]}...")
    
    print("\n📝 Step 3: Preparing content for podcast...")
    num_chunks_to_use = min(3, len(chunks))
    combined_content = "\n\n".join(chunks[:num_chunks_to_use])
    
    print(f"✓ Using {num_chunks_to_use} chunks ({len(combined_content)} characters)")
    
    print("\n🎙️  Step 4: Generating podcast dialogue...")
    print("   (This may take 10-30 seconds...)")
    
    try:
        result = generate_podcast_dialogue(
            topic=topic,
            document_chunks=combined_content,
            duration_minutes=3,
            model="gpt-4o-mini"
        )
        
        dialogue = result["dialogue"]
        usage = result["usage"]
        
        print(f"\n✓ Podcast dialogue generated!")
        print(f"   Length: {len(dialogue)} characters")
        print(f"   Token usage: {usage['total_tokens']} tokens")
        print(f"   Cost estimate: ~${usage['total_tokens'] * 0.00000015:.4f} (gpt-4o-mini)")
        
        host_a_count = dialogue.count("Host A:")
        host_b_count = dialogue.count("Host B:")
        print(f"   Host A lines: {host_a_count}")
        print(f"   Host B lines: {host_b_count}")
        
        print("\n" + "="*60)
        print("GENERATED PODCAST DIALOGUE")
        print("="*60)
        print(dialogue)
        print("="*60)
        
        print("\n✅ TEST PASSED - Successfully generated podcast from PDF!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR generating podcast: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def interactive_mode():
    """
    Interactive mode - prompts user for PDF path and topic.
    """
    print("\n" + "="*60)
    print("INTERACTIVE PDF PODCAST GENERATOR")
    print("="*60)
    print("\nThis will:")
    print("1. Load a PDF from your computer")
    print("2. Extract and process the text")
    print("3. Generate a podcast dialogue about the content")
    print("\nYou'll need:")
    print("- A PDF file on your computer")
    print("- OpenAI API key configured in .env")
    
    print("\n" + "-"*60)
    pdf_path = input("Enter the path to your PDF file: ").strip()
    
    pdf_path = pdf_path.strip('"').strip("'")
    
    print("\n" + "-"*60)
    topic = input("Enter podcast topic (or press Enter to use filename): ").strip()
    
    if not topic:
        topic = None
    
    test_with_pdf_file(pdf_path, topic)


if __name__ == "__main__":
    from config.settings import OPENAI_API_KEY
    
    if not OPENAI_API_KEY:
        print("\n❌ ERROR: OPENAI_API_KEY not found in environment variables")
        print("   Please set your API key in the .env file")
        sys.exit(1)
    
    print(f"✓ API Key configured: {OPENAI_API_KEY[:8]}...{OPENAI_API_KEY[-4:]}")
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        topic = sys.argv[2] if len(sys.argv) > 2 else None
        test_with_pdf_file(pdf_path, topic)
    else:
        interactive_mode()