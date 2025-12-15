"""
Comprehensive tests for script_generator.py

Tests the full pipeline from document chunks to podcast script,
including different content types and target lengths.
"""

import sys
import os
from pathlib import Path
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.script_generator import (
    generate_podcast_script,
    validate_script,
    ScriptGenerationError
)
from services.document_processor import process_document
from database.vector_store import get_collection


async def test_script_generation_with_pdf(pdf_path: str, target_length: str = "short"):
    """
    Test script generation with a real PDF file.
    
    Args:
        pdf_path: Path to PDF file
        target_length: "short", "medium", or "long"
    """
    print("\n" + "="*70)
    print(f"SCRIPT GENERATOR TEST - {target_length.upper()} LENGTH")
    print("="*70)
    
    pdf_file = Path(pdf_path)
    
    if not pdf_file.exists():
        print(f"❌ ERROR: File not found: {pdf_path}")
        return False
    
    print(f"\n📄 PDF File: {pdf_file.name}")
    print(f"   Path: {pdf_file.absolute()}")
    print(f"   Target Length: {target_length}")
    
    print("\n🔍 Step 1: Processing document and storing chunks...")
    document_id = f"test_{pdf_file.stem}_{target_length}"
    
    try:
        result = await process_document(document_id, pdf_file)
        print(f"✓ Document processed: {result['chunks_count']} chunks stored")
    except Exception as e:
        print(f"❌ ERROR processing document: {str(e)}")
        return False
    
    print(f"\n🎙️  Step 2: Generating {target_length} podcast script...")
    print("   (This may take 10-30 seconds...)")
    
    try:
        script = await generate_podcast_script(document_id, target_length)
        
        print(f"\n✓ Script generated successfully!")
        print(f"   Total exchanges: {len(script)}")
        
        host_count = sum(1 for e in script if e["speaker"] == "host")
        guest_count = sum(1 for e in script if e["speaker"] == "guest")
        
        print(f"   Host lines: {host_count}")
        print(f"   Guest lines: {guest_count}")
        
        total_words = sum(len(e["text"].split()) for e in script)
        print(f"   Total words: {total_words}")
        
        estimated_duration = total_words / 150
        print(f"   Estimated duration: {estimated_duration:.1f} minutes")
        
    except ScriptGenerationError as e:
        print(f"❌ ERROR generating script: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n✅ Step 3: Validating script quality...")
    
    is_valid = validate_script(script)
    
    if not is_valid:
        print("❌ Script validation failed")
        return False
    
    print("✓ Script validation passed")
    
    print("\n" + "="*70)
    print("GENERATED SCRIPT SAMPLE (First 5 exchanges)")
    print("="*70)
    
    for i, line in enumerate(script[:5]):
        speaker_label = line["speaker"].upper()
        print(f"\n{speaker_label}: {line['text']}")
    
    if len(script) > 5:
        print(f"\n... ({len(script) - 5} more exchanges)")
    
    print("\n" + "="*70)
    
    print("\n🔍 Step 5: Quality checks...")
    
    has_reactions = any(
        word in line["text"].lower() 
        for line in script 
        for word in ["wow", "interesting", "fascinating", "really", "amazing"]
    )
    print(f"   Natural reactions: {'✓' if has_reactions else '⚠️  (might be too formal)'}")
    
    has_questions = any("?" in line["text"] for line in script)
    print(f"   Contains questions: {'✓' if has_questions else '⚠️  (might lack engagement)'}")
    
    alternation_breaks = 0
    for i in range(1, len(script)):
        if script[i]["speaker"] == script[i-1]["speaker"]:
            alternation_breaks += 1
    
    alternation_rate = 1 - (alternation_breaks / len(script))
    print(f"   Speaker alternation: {alternation_rate*100:.0f}% ({'✓' if alternation_rate > 0.7 else '⚠️'})")
    
    avg_words_per_line = total_words / len(script)
    print(f"   Avg words per line: {avg_words_per_line:.1f} ({'✓' if 10 < avg_words_per_line < 50 else '⚠️'})")
    
    print("\n✅ TEST PASSED - Script generated successfully!")
    print("="*70)
    
    return True


async def test_all_lengths(pdf_path: str):
    """
    Test all three target lengths with the same PDF.
    
    Args:
        pdf_path: Path to PDF file
    """
    print("\n" + "="*70)
    print("COMPREHENSIVE LENGTH TEST")
    print("Testing short, medium, and long scripts with same document")
    print("="*70)
    
    lengths = ["short", "medium", "long"]
    results = {}
    
    for length in lengths:
        success = await test_script_generation_with_pdf(pdf_path, length)
        results[length] = success
        
        if not success:
            print(f"\n⚠️  {length.upper()} test failed, continuing with others...")
        
        await asyncio.sleep(2)
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for length, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{length.upper():8} - {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n⚠️  Some tests failed - review output above")
    
    return all_passed


async def test_empty_document():
    """
    Test error handling with non-existent document.
    """
    print("\n" + "="*70)
    print("ERROR HANDLING TEST - Non-existent Document")
    print("="*70)
    
    try:
        script = await generate_podcast_script("nonexistent_doc_123", "short")
        print("❌ ERROR: Should have raised ScriptGenerationError")
        return False
    except ScriptGenerationError as e:
        print(f"✓ Correctly raised ScriptGenerationError: {str(e)}")
        return True
    except Exception as e:
        print(f"❌ ERROR: Unexpected exception type: {type(e).__name__}")
        return False


async def test_script_structure():
    """
    Test that script structure matches specification.
    """
    print("\n" + "="*70)
    print("STRUCTURE VALIDATION TEST")
    print("="*70)
    
    mock_script = [
        {"speaker": "host", "text": "Welcome to the show!"},
        {"speaker": "guest", "text": "Thanks for having me."},
        {"speaker": "host", "text": "Let's dive in."},
        {"speaker": "guest", "text": "Sounds great!"}
    ]
    
    print("\n✓ Testing valid script structure...")
    is_valid = validate_script(mock_script)
    
    if not is_valid:
        print("❌ Valid script failed validation")
        return False
    
    print("✓ Valid script passed validation")
    
    print("\n✓ Testing invalid script structures...")
    
    short_script = [{"speaker": "host", "text": "Hi"}]
    if validate_script(short_script):
        print("❌ Too-short script passed validation (should fail)")
        return False
    print("✓ Too-short script correctly rejected")
    
    invalid_script = [{"speaker": "host"}]
    if validate_script(invalid_script):
        print("❌ Script with missing fields passed validation (should fail)")
        return False
    print("✓ Script with missing fields correctly rejected")
    
    bad_speaker_script = [
        {"speaker": "narrator", "text": "Once upon a time..."}
    ]
    if validate_script(bad_speaker_script):
        print("❌ Script with invalid speaker passed validation (should fail)")
        return False
    print("✓ Script with invalid speaker correctly rejected")
    
    print("\n✅ All structure tests passed!")
    return True


async def run_all_tests(pdf_path: str = None):
    """
    Run all tests.
    
    Args:
        pdf_path: Optional path to PDF file for integration tests
    """
    print("\n" + "="*70)
    print("SCRIPT GENERATOR - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    results = {}
    
    results["structure"] = await test_script_structure()
    
    results["error_handling"] = await test_empty_document()
    
    if pdf_path:
        results["pdf_integration"] = await test_all_lengths(pdf_path)
    else:
        print("\n⚠️  Skipping PDF integration tests (no PDF path provided)")
        print("   Run with: python test_script_generator.py /path/to/file.pdf")
    
    print("\n" + "="*70)
    print("FINAL TEST SUMMARY")
    print("="*70)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:20} - {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED")
    print("="*70)
    
    return all_passed


def interactive_mode():
    """
    Interactive mode - prompts user for PDF path.
    """
    print("\n" + "="*70)
    print("INTERACTIVE SCRIPT GENERATOR TEST")
    print("="*70)
    print("\nThis will test the podcast script generation pipeline:")
    print("1. Process a PDF document")
    print("2. Generate scripts in different lengths")
    print("3. Validate script quality")
    print("\nYou'll need:")
    print("- A PDF file on your computer")
    print("- OpenAI API key configured in .env")
    
    print("\n" + "-"*70)
    pdf_path = input("Enter the path to your PDF file (or press Enter to skip): ").strip()
    
    if pdf_path:
        pdf_path = pdf_path.strip('"').strip("'")
        asyncio.run(run_all_tests(pdf_path))
    else:
        print("\nRunning tests without PDF integration...")
        asyncio.run(run_all_tests())


if __name__ == "__main__":
    from config.settings import OPENAI_API_KEY
    
    if not OPENAI_API_KEY:
        print("\n❌ ERROR: OPENAI_API_KEY not found in environment variables")
        print("   Please set your API key in the .env file")
        sys.exit(1)
    
    print(f"✓ API Key configured: {OPENAI_API_KEY[:8]}...{OPENAI_API_KEY[-4:]}")
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        asyncio.run(run_all_tests(pdf_path))
    else:
        interactive_mode()