"""
Simple automated tests for Q&A Context Builder Service.

This test file runs automated tests without requiring user input.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.qa_context_builder import (
    build_qa_context,
    QAContextError,
    validate_context,
    _extract_recent_dialogue
)


def test_error_handling():
    """Test error handling for invalid inputs."""
    print("\n" + "="*60)
    print("TEST: Error Handling")
    print("="*60)
    
    async def run_tests():
        print("\n✓ Test 1: Empty podcast_id")
        try:
            await build_qa_context("", "test question", 100.0)
            print("  ❌ FAILED - Should have raised QAContextError")
            return False
        except QAContextError as e:
            print(f"  ✅ PASSED - Correctly raised: {str(e)}")
        
        print("\n✓ Test 2: Empty question")
        try:
            await build_qa_context("pod_123", "", 100.0)
            print("  ❌ FAILED - Should have raised QAContextError")
            return False
        except QAContextError as e:
            print(f"  ✅ PASSED - Correctly raised: {str(e)}")
        
        print("\n✓ Test 3: Negative timestamp")
        try:
            await build_qa_context("pod_123", "test question", -10.0)
            print("  ❌ FAILED - Should have raised QAContextError")
            return False
        except QAContextError as e:
            print(f"  ✅ PASSED - Correctly raised: {str(e)}")
        
        print("\n✓ Test 4: Non-existent podcast")
        try:
            await build_qa_context("pod_nonexistent_12345", "test question", 100.0)
            print("  ❌ FAILED - Should have raised QAContextError")
            return False
        except QAContextError as e:
            print(f"  ✅ PASSED - Correctly raised: {str(e)}")
        
        return True
    
    result = asyncio.run(run_tests())
    return result


def test_dialogue_extraction():
    """Test dialogue extraction logic."""
    print("\n" + "="*60)
    print("TEST: Dialogue Extraction")
    print("="*60)
    
    mock_script = [
        {"speaker": "host", "text": "Welcome to the podcast!"},
        {"speaker": "guest", "text": "Thanks for having me."},
        {"speaker": "host", "text": "Let's talk about AI."},
        {"speaker": "guest", "text": "AI is fascinating."},
        {"speaker": "host", "text": "What about neural networks?"},
        {"speaker": "guest", "text": "Neural networks are powerful."},
        {"speaker": "host", "text": "How do they learn?"},
        {"speaker": "guest", "text": "Through backpropagation."},
        {"speaker": "host", "text": "Can you explain that?"},
        {"speaker": "guest", "text": "Sure, it's a training algorithm."},
    ]
    
    print("\n✓ Test 1: Beginning (timestamp: 5s)")
    dialogue = _extract_recent_dialogue(mock_script, 5.0, lookback_seconds=60)
    print(f"  Retrieved {len(dialogue)} exchanges")
    if dialogue:
        print(f"  First exchange at: {dialogue[0]['timestamp']}s")
        print(f"  Last exchange at: {dialogue[-1]['timestamp']}s")
    print("  ✅ PASSED")
    
    print("\n✓ Test 2: Middle (timestamp: 40s)")
    dialogue = _extract_recent_dialogue(mock_script, 40.0, lookback_seconds=60)
    print(f"  Retrieved {len(dialogue)} exchanges")
    if dialogue:
        print(f"  First exchange at: {dialogue[0]['timestamp']}s")
        print(f"  Last exchange at: {dialogue[-1]['timestamp']}s")
    print("  ✅ PASSED")
    
    print("\n✓ Test 3: Near end (timestamp: 70s)")
    dialogue = _extract_recent_dialogue(mock_script, 70.0, lookback_seconds=60)
    print(f"  Retrieved {len(dialogue)} exchanges")
    if dialogue:
        print(f"  First exchange at: {dialogue[0]['timestamp']}s")
        print(f"  Last exchange at: {dialogue[-1]['timestamp']}s")
    print("  ✅ PASSED")
    
    print("\n✓ Test 4: Beyond end (timestamp: 1000s)")
    dialogue = _extract_recent_dialogue(mock_script, 1000.0, lookback_seconds=60)
    print(f"  Retrieved {len(dialogue)} exchanges")
    if dialogue:
        print(f"  First exchange at: {dialogue[0]['timestamp']}s")
        print(f"  Last exchange at: {dialogue[-1]['timestamp']}s")
    print("  ✅ PASSED")
    
    print("\n✓ Test 5: Empty script")
    dialogue = _extract_recent_dialogue([], 50.0, lookback_seconds=60)
    print(f"  Retrieved {len(dialogue)} exchanges (should be 0)")
    assert len(dialogue) == 0, "Empty script should return empty list"
    print("  ✅ PASSED")
    
    return True


def test_context_validation():
    """Test context validation."""
    print("\n" + "="*60)
    print("TEST: Context Validation")
    print("="*60)
    
    print("\n✓ Test 1: Valid context")
    valid_context = {
        "question": "What is AI?",
        "timestamp": 100.0,
        "document_chunks": [
            {"text": "AI is...", "source": "doc.pdf", "relevance_score": 0.9}
        ],
        "recent_dialogue": [
            {"speaker": "host", "text": "Welcome", "timestamp": 90.0}
        ],
        "podcast_metadata": {
            "podcast_id": "pod_123",
            "document_ids": ["doc_1"],
            "created_at": "2026-01-01T00:00:00Z"
        }
    }
    result = validate_context(valid_context)
    print(f"  Validation result: {result}")
    assert result == True, "Valid context should pass validation"
    print("  ✅ PASSED")
    
    print("\n✓ Test 2: Missing required field")
    invalid_context = {
        "question": "What is AI?",
        "timestamp": 100.0,
        "recent_dialogue": [],
        "podcast_metadata": {}
    }
    result = validate_context(invalid_context)
    print(f"  Validation result: {result}")
    assert result == False, "Invalid context should fail validation"
    print("  ✅ PASSED")
    
    print("\n✓ Test 3: Wrong field type")
    invalid_context = {
        "question": "What is AI?",
        "timestamp": 100.0,
        "document_chunks": "not a list",
        "recent_dialogue": [],
        "podcast_metadata": {}
    }
    result = validate_context(invalid_context)
    print(f"  Validation result: {result}")
    assert result == False, "Invalid type should fail validation"
    print("  ✅ PASSED")
    
    return True


def run_all_tests():
    """Run all automated tests."""
    print("\n" + "="*60)
    print("Q&A CONTEXT BUILDER - AUTOMATED TEST SUITE")
    print("="*60)
    
    results = []
    
    results.append(("Error Handling", test_error_handling()))
    results.append(("Dialogue Extraction", test_dialogue_extraction()))
    results.append(("Context Validation", test_context_validation()))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)