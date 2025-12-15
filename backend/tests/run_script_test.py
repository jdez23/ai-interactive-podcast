"""
Quick test runner for script generator with local PDF.

This is a simplified test script that makes it easy to test
the script generator with your own PDF files.
"""

import sys
import os
import asyncio
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.script_generator import generate_podcast_script
from services.document_processor import process_document


async def quick_test(pdf_path: str, length: str = "short"):
    """
    Quick test of script generation with a PDF.
    
    Args:
        pdf_path: Path to PDF file
        length: "short", "medium", or "long"
    """
    print("\n" + "="*70)
    print(f"QUICK SCRIPT GENERATOR TEST - {length.upper()}")
    print("="*70)
    
    pdf_file = Path(pdf_path)
    
    if not pdf_file.exists():
        print(f"❌ File not found: {pdf_path}")
        return
    
    print(f"\n📄 Processing: {pdf_file.name}")
    
    document_id = f"quick_test_{pdf_file.stem}"
    
    try:
        print("   Processing document...")
        await process_document(document_id, pdf_file)
        print("   ✓ Document processed")
        
        print(f"   Generating {length} script...")
        script = await generate_podcast_script(document_id, length)
        print(f"   ✓ Script generated ({len(script)} exchanges)")
        
        print("\n" + "="*70)
        print("PODCAST SCRIPT")
        print("="*70)
        
        for line in script:
            speaker = line["speaker"].upper()
            text = line["text"]
            print(f"\n{speaker}: {text}")
        
        print("\n" + "="*70)
        print("✅ SUCCESS!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python run_script_test.py <pdf_path> [length]")
        print("\nExample:")
        print("  python run_script_test.py ~/Documents/article.pdf short")
        print("  python run_script_test.py /path/to/file.pdf medium")
        print("\nLength options: short, medium, long (default: short)")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    length = sys.argv[2] if len(sys.argv) > 2 else "short"
    
    asyncio.run(quick_test(pdf_path, length))