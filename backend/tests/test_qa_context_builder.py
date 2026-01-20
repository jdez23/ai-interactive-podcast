"""
Tests for Q&A Context Builder Service.

This test file verifies the build_qa_context function works correctly
with different scenarios including error cases.
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.qa_context_builder import (
    build_qa_context,
    QAContextError,
    validate_context
)


async def test_basic_context_building():
    """
    Test 1: Basic Context Building
    
    Tests that the function can successfully build context for a valid podcast.
    """
    print("\n" + "="*60)
    print("TEST 1: Basic Context Building")
    print("="*60)
    
    try:
        podcast_id = input("Enter a valid podcast_id (or press Enter to skip): ").strip()
        
        if not podcast_id:
            print("⚠️  Skipping test - no podcast_id provided")
            return
        
        question = "What is backpropagation?"
        timestamp = 165.5
        
        print(f"\nBuilding context for:")
        print(f"  Podcast ID: {podcast_id}")
        print(f"  Question: {question}")
        print(f"  Timestamp: {timestamp}s")
        
        context = await build_qa_context(
            podcast_id=podcast_id,
            question=question,
            timestamp=timestamp
        )
        
        print("\n✅ Context built successfully!")
        print(f"\nContext structure:")
        print(f"  Question: {context['question']}")
        print(f"  Timestamp: {context['timestamp']}")
        print(f"  Document chunks: {len(context['document_chunks'])} chunks")
        print(f"  Recent dialogue: {len(context['recent_dialogue'])} exchanges")
        print(f"  Podcast metadata: {context['podcast_metadata']['podcast_id']}")
        
        if context['document_chunks']:
            print(f"\n📄 Sample document chunk:")
            chunk = context['document_chunks'][0]
            print(f"  Source: {chunk['source']}")
            print(f"  Relevance: {chunk['relevance_score']:.2f}")
            print(f"  Text preview: {chunk['text'][:100]}...")
        
        if context['recent_dialogue']:
            print(f"\n💬 Sample recent dialogue:")
            for exchange in context['recent_dialogue'][-2:]:
                print(f"  [{exchange['timestamp']}s] {exchange['speaker'].upper()}: {exchange['text'][:80]}...")
        
        is_valid = validate_context(context)
        print(f"\n✅ Context validation: {'PASSED' if is_valid else 'FAILED'}")
        
    except QAContextError as e:
        print(f"\n❌ QAContextError: {str(e)}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")


async def test_error_handling():
    """
    Test 2: Error Handling
    
    Tests that the function properly handles various error cases.
    """
    print("\n" + "="*60)
    print("TEST 2: Error Handling")
    print("="*60)
    
    print("\n📋 Test 2a: Empty podcast_id")
    try:
        await build_qa_context("", "test question", 100.0)
        print("❌ Should have raised QAContextError")
    except QAContextError as e:
        print(f"✅ Correctly raised error: {str(e)}")
    
    print("\n📋 Test 2b: Empty question")
    try:
        await build_qa_context("pod_123", "", 100.0)
        print("❌ Should have raised QAContextError")
    except QAContextError as e:
        print(f"✅ Correctly raised error: {str(e)}")
    
    print("\n📋 Test 2c: Negative timestamp")
    try:
        await build_qa_context("pod_123", "test question", -10.0)
        print("❌ Should have raised QAContextError")
    except QAContextError as e:
        print(f"✅ Correctly raised error: {str(e)}")
    
    print("\n📋 Test 2d: Non-existent podcast")
    try:
        await build_qa_context("pod_nonexistent_12345", "test question", 100.0)
        print("❌ Should have raised QAContextError")
    except QAContextError as e:
        print(f"✅ Correctly raised error: {str(e)}")


async def test_timestamp_edge_cases():
    """
    Test 3: Timestamp Edge Cases
    
    Tests dialogue extraction at different timestamps.
    """
    print("\n" + "="*60)
    print("TEST 3: Timestamp Edge Cases")
    print("="*60)
    
    podcast_id = input("\nEnter a valid podcast_id (or press Enter to skip): ").strip()
    
    if not podcast_id:
        print("⚠️  Skipping test - no podcast_id provided")
        return
    
    test_cases = [
        ("Beginning", 5.0),
        ("Middle", 150.0),
        ("Near end", 500.0),
        ("Beyond end", 10000.0)
    ]
    
    for label, timestamp in test_cases:
        print(f"\n📋 Testing {label} (timestamp: {timestamp}s)")
        try:
            context = await build_qa_context(
                podcast_id=podcast_id,
                question="Test question",
                timestamp=timestamp
            )
            
            dialogue_count = len(context['recent_dialogue'])
            print(f"✅ Retrieved {dialogue_count} recent exchanges")
            
            if context['recent_dialogue']:
                first_ts = context['recent_dialogue'][0]['timestamp']
                last_ts = context['recent_dialogue'][-1]['timestamp']
                print(f"   Timestamp range: {first_ts}s - {last_ts}s")
            
        except QAContextError as e:
            print(f"❌ Error: {str(e)}")


async def test_different_questions():
    """
    Test 4: Different Question Types
    
    Tests semantic search with various question types.
    """
    print("\n" + "="*60)
    print("TEST 4: Different Question Types")
    print("="*60)
    
    podcast_id = input("\nEnter a valid podcast_id (or press Enter to skip): ").strip()
    
    if not podcast_id:
        print("⚠️  Skipping test - no podcast_id provided")
        return
    
    questions = [
        "What is the main topic?",
        "Can you explain that last part?",
        "How does this work?",
        "What are the key takeaways?",
        "Why is this important?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n📋 Question {i}: {question}")
        try:
            context = await build_qa_context(
                podcast_id=podcast_id,
                question=question,
                timestamp=100.0
            )
            
            chunk_count = len(context['document_chunks'])
            print(f"✅ Found {chunk_count} relevant chunks")
            
            if context['document_chunks']:
                top_chunk = context['document_chunks'][0]
                print(f"   Top relevance: {top_chunk['relevance_score']:.2f}")
                print(f"   Preview: {top_chunk['text'][:80]}...")
            
        except QAContextError as e:
            print(f"❌ Error: {str(e)}")


async def run_all_tests():
    """Run all test scenarios."""
    print("\n" + "="*60)
    print("Q&A CONTEXT BUILDER - TEST SUITE")
    print("="*60)
    print("\nThis test suite will verify the build_qa_context function")
    print("works correctly with different scenarios.")
    print("\nNote: You'll need at least one completed podcast in your")
    print("database to run the full test suite.")
    
    await test_basic_context_building()
    await test_error_handling()
    await test_timestamp_edge_cases()
    await test_different_questions()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETE")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())