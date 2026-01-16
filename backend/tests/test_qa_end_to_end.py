"""
End-to-end test for the complete Q&A system.

This test validates the entire Q&A flow from API request to answer generation.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.question_answerer import answer_question, QuestionAnswererError


async def test_question_answering():
    """
    Test the complete question answering flow.
    
    This test requires:
    - A completed podcast in the database
    - The podcast must have a script file
    - Source documents must be in the vector database
    """
    print("\n" + "="*60)
    print("Q&A END-TO-END TEST")
    print("="*60)
    
    podcast_id = input("\nEnter a podcast_id to test with (or press Enter to skip): ").strip()
    
    if not podcast_id:
        print("⚠️  Skipping test - no podcast_id provided")
        print("\nTo run this test:")
        print("1. Generate a podcast first")
        print("2. Note the podcast_id")
        print("3. Run this test again with that podcast_id")
        return
    
    test_cases = [
        {
            "question": "What is the main topic?",
            "timestamp": 30.0,
            "description": "General question at beginning"
        },
        {
            "question": "Can you explain that last part?",
            "timestamp": 120.0,
            "description": "Reference to recent dialogue"
        },
        {
            "question": "What are the key takeaways?",
            "timestamp": 200.0,
            "description": "Summary question"
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}: {test_case['description']}")
        print(f"{'='*60}")
        print(f"Question: {test_case['question']}")
        print(f"Timestamp: {test_case['timestamp']}s")
        
        try:
            answer = await answer_question(
                podcast_id=podcast_id,
                question=test_case['question'],
                timestamp=test_case['timestamp']
            )
            
            print(f"\n✅ Answer generated successfully!")
            print(f"\n📝 Answer:")
            print(f"   {answer['answer_text']}")
            print(f"\n📚 Sources: {', '.join(answer['sources'])}")
            print(f"\n📊 Context Used:")
            print(f"   - Document chunks: {answer['context_used']['document_chunks']}")
            print(f"   - Dialogue exchanges: {answer['context_used']['dialogue_exchanges']}")
            
            if len(answer['answer_text']) < 20:
                print(f"\n⚠️  Warning: Answer seems too short")
            
            if not answer['sources']:
                print(f"\n⚠️  Warning: No sources provided")
            
            passed += 1
            
        except QuestionAnswererError as e:
            print(f"\n❌ Test failed: {str(e)}")
            failed += 1
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            failed += 1
    
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")
    
    if passed == len(test_cases):
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


async def test_error_handling():
    """Test error handling in the Q&A system."""
    print("\n" + "="*60)
    print("ERROR HANDLING TEST")
    print("="*60)
    
    print("\n✓ Test 1: Non-existent podcast")
    try:
        await answer_question("pod_nonexistent_12345", "test question", 100.0)
        print("  ❌ FAILED - Should have raised QuestionAnswererError")
    except QuestionAnswererError as e:
        print(f"  ✅ PASSED - Correctly raised error: {str(e)}")
    
    print("\n✓ Test 2: Empty question")
    try:
        await answer_question("pod_123", "", 100.0)
        print("  ❌ FAILED - Should have raised QuestionAnswererError")
    except QuestionAnswererError as e:
        print(f"  ✅ PASSED - Correctly raised error: {str(e)}")
    
    print("\n✓ Test 3: Negative timestamp")
    try:
        await answer_question("pod_123", "test question", -10.0)
        print("  ❌ FAILED - Should have raised QuestionAnswererError")
    except QuestionAnswererError as e:
        print(f"  ✅ PASSED - Correctly raised error: {str(e)}")
    
    print("\n✅ Error handling tests complete")


async def run_all_tests():
    """Run all Q&A tests."""
    print("\n" + "="*60)
    print("Q&A SYSTEM - END-TO-END TEST SUITE")
    print("="*60)
    print("\nThis test suite validates the complete Q&A flow:")
    print("1. Context building (document chunks + recent dialogue)")
    print("2. Answer generation using OpenAI")
    print("3. Error handling")
    
    await test_error_handling()
    
    exit_code = await test_question_answering()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETE")
    print("="*60)
    
    return exit_code


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code or 0)