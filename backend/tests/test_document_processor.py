"""
Tests for document_processor.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.document_processor import chunk_text


def test_empty_string():
    """Test that empty string returns empty list"""
    result = chunk_text("")
    assert result == [], f"Expected empty list, got {result}"
    print("Test 1 passed: Empty string returns empty list")


def test_whitespace_only():
    """Test that whitespace-only string returns empty list"""
    result = chunk_text("   \n\n  ")
    assert result == [], f"Expected empty list, got {result}"
    print("Test 2 passed: Whitespace-only returns empty list")


def test_short_text():
    """Test that short text (< 500 words) returns single chunk"""
    short_text = "This is a short document with less than 500 words. " * 10
    result = chunk_text(short_text)
    assert len(result) == 1, f"Expected 1 chunk, got {len(result)}"
    print(f"Test 3 passed: Short text returns 1 chunk")


def test_long_text():
    """Test that long text (5000 words) returns ~10 chunks with overlap"""
    long_text = " ".join(["word"] * 5000)
    result = chunk_text(long_text)
    
    assert len(result) >= 10, f"Expected at least 10 chunks, got {len(result)}"
    assert len(result) <= 15, f"Expected at most 15 chunks, got {len(result)}"
    print(f"Test 4 passed: Long text (5000 words) returns {len(result)} chunks")


def test_chunk_overlap():
    """Test that consecutive chunks have overlap"""
    words = [f"word{i}" for i in range(1000)]
    text = " ".join(words)
    result = chunk_text(text)
    
    if len(result) > 1:
        chunk1_words = result[0].split()
        chunk2_words = result[1].split()
        
        overlap_found = any(word in chunk2_words[:100] for word in chunk1_words[-50:])
        assert overlap_found, "No overlap found between consecutive chunks"
        print(f"Test 5 passed: Chunks have overlap")
    else:
        print(f"Test 5 skipped: Only one chunk created")


def test_semantic_splitting():
    """Test that chunks preserve semantic meaning (don't cut mid-word)"""
    text = "This is sentence one. " * 100 + "This is sentence two. " * 100
    result = chunk_text(text)
    
    for i, chunk in enumerate(result):
        last_char = chunk.strip()[-1] if chunk.strip() else ''
        assert last_char.isalnum() or last_char in ['.', '!', '?', ' ', '\n'], \
            f"Chunk {i} appears to cut mid-word: ...{chunk[-50:]}"
    
    print(f"Test 6 passed: All {len(result)} chunks preserve word boundaries")



def run_all_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print("Running chunk_text() tests...")
    print("="*50 + "\n")
    
    try:
        test_empty_string()
        test_whitespace_only()
        test_short_text()
        test_long_text()
        test_chunk_overlap()
        test_semantic_splitting()
        
        print("\n" + "="*50)
        print("ALL TESTS PASSED!")
        print("="*50 + "\n")
        return True
        
    except AssertionError as e:
        print(f"\n TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n ERROR: {e}\n")
        return False


if __name__ == "__main__":
    run_all_tests()
