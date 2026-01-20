"""
Automated tests for Q&A system (no user input required).

Tests the question answerer service with mock/error scenarios.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.question_answerer import (
    answer_question,
    QuestionAnswererError,
    validate_answer
)


async def test_error_handling():
    """Test error handling in the Q&A system."""
    print("\n" + "="*60)
    print("TEST: Error Handling")
    print("="*60)
    
    tests_passed = 0
    tests_failed = 0
    
    print("\n✓ Test 1: Non-existent podcast")
    try:
        await answer_question("pod_nonexistent_12345", "test question", 100.0)
        print("  ❌ FAILED - Should have raised QuestionAnswererError")
        tests_failed += 1
    except QuestionAnswererError as e:
        if "not found" in str(e).lower():
            print(f"  ✅ PASSED - Correctly raised error: {str(e)}")
            tests_passed += 1
        else:
            print(f"  ❌ FAILED - Wrong error message: {str(e)}")
            tests_failed += 1
    
    print("\n✓ Test 2: Empty question")
    try:
        await answer_question("pod_123", "", 100.0)
        print("  ❌ FAILED - Should have raised QuestionAnswererError")
        tests_failed += 1
    except QuestionAnswererError as e:
        if "empty" in str(e).lower():
            print(f"  ✅ PASSED - Correctly raised error: {str(e)}")
            tests_passed += 1
        else:
            print(f"  ❌ FAILED - Wrong error message: {str(e)}")
            tests_failed += 1
    
    print("\n✓ Test 3: Negative timestamp")
    try:
        await answer_question("pod_123", "test question", -10.0)
        print("  ❌ FAILED - Should have raised QuestionAnswererError")
        tests_failed += 1
    except QuestionAnswererError as e:
        if "negative" in str(e).lower():
            print(f"  ✅ PASSED - Correctly raised error: {str(e)}")
            tests_passed += 1
        else:
            print(f"  ❌ FAILED - Wrong error message: {str(e)}")
            tests_failed += 1
    
    return tests_passed, tests_failed


def test_answer_validation():
    """Test answer validation logic."""
    print("\n" + "="*60)
    print("TEST: Answer Validation")
    print("="*60)
    
    tests_passed = 0
    tests_failed = 0
    
    print("\n✓ Test 1: Valid answer")
    valid_answer = {
        "answer_text": "This is a valid answer with sufficient length.",
        "sources": ["doc1.pdf", "doc2.pdf"],
        "context_used": {
            "document_chunks": 5,
            "dialogue_exchanges": 3
        },
        "timestamp": 100.0
    }
    if validate_answer(valid_answer):
        print("  ✅ PASSED - Valid answer accepted")
        tests_passed += 1
    else:
        print("  ❌ FAILED - Valid answer rejected")
        tests_failed += 1
    
    print("\n✓ Test 2: Missing required field")
    invalid_answer = {
        "answer_text": "Answer text",
        "sources": [],
    }
    if not validate_answer(invalid_answer):
        print("  ✅ PASSED - Invalid answer rejected")
        tests_passed += 1
    else:
        print("  ❌ FAILED - Invalid answer accepted")
        tests_failed += 1
    
    print("\n✓ Test 3: Answer too short")
    short_answer = {
        "answer_text": "Short",
        "sources": [],
        "context_used": {"document_chunks": 0, "dialogue_exchanges": 0},
        "timestamp": 100.0
    }
    if not validate_answer(short_answer):
        print("  ✅ PASSED - Short answer rejected")
        tests_passed += 1
    else:
        print("  ❌ FAILED - Short answer accepted")
        tests_failed += 1
    
    print("\n✓ Test 4: Wrong type for sources")
    wrong_type_answer = {
        "answer_text": "This is a valid answer.",
        "sources": "not a list",  # Should be list
        "context_used": {"document_chunks": 0, "dialogue_exchanges": 0},
        "timestamp": 100.0
    }
    if not validate_answer(wrong_type_answer):
        print("  ✅ PASSED - Wrong type rejected")
        tests_passed += 1
    else:
        print("  ❌ FAILED - Wrong type accepted")
        tests_failed += 1
    
    return tests_passed, tests_failed


async def run_all_tests():
    """Run all automated Q&A tests."""
    print("\n" + "="*60)
    print("Q&A SYSTEM - AUTOMATED TEST SUITE")
    print("="*60)
    print("\nThese tests validate Q&A functionality without requiring")
    print("a real podcast. They test error handling and validation logic.")
    
    total_passed = 0
    total_failed = 0
    
    passed, failed = await test_error_handling()
    total_passed += passed
    total_failed += failed
    
    passed, failed = test_answer_validation()
    total_passed += passed
    total_failed += failed
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total Passed: {total_passed}")
    print(f"Total Failed: {total_failed}")
    
    if total_failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_failed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)