"""
Test script for podcast storage and retrieval system.

This script tests the podcast storage functionality including:
- Saving and retrieving podcasts
- Status progression
- Failed generation cleanup
- Listing all podcasts

Note: This test only tests the database storage layer, not actual file generation.
"""

import sys
import os
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database.podcast_storage import (
    save_podcast,
    get_podcast,
    get_all_podcasts,
    update_podcast_status,
    delete_podcast,
    init_database
)
from datetime import datetime
import json


def test_save_and_retrieve():
    """Test 1: Save and retrieve podcast."""
    print("\n=== Test 1: Save and Retrieve Podcast ===")
    
    podcast_data = {
        "podcast_id": "test_pod_001",
        "document_ids": ["doc_test_123"],
        "status": "processing",
        "stage": "initializing",
        "target_duration": "medium",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    save_podcast(podcast_data)
    print(f"✓ Saved podcast: {podcast_data['podcast_id']}")
    
    retrieved = get_podcast("test_pod_001")
    assert retrieved is not None, "Podcast not found"
    assert retrieved["podcast_id"] == "test_pod_001"
    assert retrieved["status"] == "processing"
    assert retrieved["document_ids"] == ["doc_test_123"]
    print(f"✓ Retrieved podcast: {retrieved['podcast_id']}")
    print(f"  Status: {retrieved['status']}")
    print(f"  Document IDs: {retrieved['document_ids']}")
    print("✅ Test 1 PASSED")


def test_status_progression():
    """Test 2: Status progression from processing to complete."""
    print("\n=== Test 2: Status Progression ===")
    
    podcast_id = "test_pod_002"
    
    podcast_data = {
        "podcast_id": podcast_id,
        "document_ids": ["doc_test_456"],
        "status": "processing",
        "stage": "generating_script",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    save_podcast(podcast_data)
    print(f"✓ Created podcast with status: processing")
    
    update_podcast_status(
        podcast_id,
        "complete",
        stage="complete",
        audio_url="/generated/podcasts/test_pod_002.mp3",
        duration_seconds=180.5
    )
    print(f"✓ Updated status to: complete")
    
    retrieved = get_podcast(podcast_id)
    assert retrieved["status"] == "complete"
    assert retrieved["audio_url"] == "/generated/podcasts/test_pod_002.mp3"
    assert retrieved["duration_seconds"] == 180.5
    assert retrieved["completed_at"] is not None
    print(f"  Status: {retrieved['status']}")
    print(f"  Audio URL: {retrieved['audio_url']}")
    print(f"  Duration: {retrieved['duration_seconds']}s")
    print(f"  Completed at: {retrieved['completed_at']}")
    print("✅ Test 2 PASSED")


def test_failed_generation():
    """Test 3: Failed generation with error message."""
    print("\n=== Test 3: Failed Generation ===")
    
    podcast_id = "test_pod_003"
    
    podcast_data = {
        "podcast_id": podcast_id,
        "document_ids": ["doc_test_789"],
        "status": "processing",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    save_podcast(podcast_data)
    print(f"✓ Created podcast: {podcast_id}")
    
    error_msg = "ElevenLabs API error: Rate limit exceeded"
    update_podcast_status(
        podcast_id,
        "failed",
        stage="failed",
        error_message=error_msg
    )
    print(f"✓ Marked as failed with error")
    
    retrieved = get_podcast(podcast_id)
    assert retrieved["status"] == "failed"
    assert retrieved["error_message"] == error_msg
    assert retrieved["failed_at"] is not None
    print(f"  Status: {retrieved['status']}")
    print(f"  Error: {retrieved['error_message']}")
    print(f"  Failed at: {retrieved['failed_at']}")
    print("✅ Test 3 PASSED")


def test_list_all_podcasts():
    """Test 4: List all podcasts."""
    print("\n=== Test 4: List All Podcasts ===")
    
    for i in range(3):
        podcast_data = {
            "podcast_id": f"test_pod_list_{i}",
            "document_ids": [f"doc_test_{i}"],
            "status": "complete" if i % 2 == 0 else "processing",
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        save_podcast(podcast_data)
    
    print(f"✓ Created 3 test podcasts")
    
    all_podcasts = get_all_podcasts()
    print(f"✓ Retrieved {len(all_podcasts)} total podcasts")
    
    test_podcasts = [p for p in all_podcasts if p["podcast_id"].startswith("test_pod_list_")]
    assert len(test_podcasts) >= 3, "Not all test podcasts found"
    
    print(f"  Test podcasts found: {len(test_podcasts)}")
    for podcast in test_podcasts[:3]:
        print(f"    - {podcast['podcast_id']}: {podcast['status']}")
    
    print("✅ Test 4 PASSED")


def test_podcast_not_found():
    """Test 5: Podcast not found."""
    print("\n=== Test 5: Podcast Not Found ===")
    
    result = get_podcast("nonexistent_podcast_id")
    assert result is None, "Should return None for nonexistent podcast"
    print("✓ Correctly returned None for nonexistent podcast")
    print("✅ Test 5 PASSED")


def test_update_with_multiple_fields():
    """Test 6: Update multiple fields at once."""
    print("\n=== Test 6: Update Multiple Fields ===")
    
    podcast_id = "test_pod_multi"
    
    podcast_data = {
        "podcast_id": podcast_id,
        "document_ids": ["doc_multi"],
        "status": "processing",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    save_podcast(podcast_data)
    print(f"✓ Created podcast: {podcast_id}")
    
    update_podcast_status(
        podcast_id,
        "complete",
        stage="complete",
        audio_url="/generated/podcasts/test_pod_multi.mp3",
        script_url="/generated/podcasts/test_pod_multi_script.json",
        duration_seconds=240.0
    )
    print(f"✓ Updated multiple fields")
    
    retrieved = get_podcast(podcast_id)
    assert retrieved["status"] == "complete"
    assert retrieved["audio_url"] == "/generated/podcasts/test_pod_multi.mp3"
    assert retrieved["script_url"] == "/generated/podcasts/test_pod_multi_script.json"
    assert retrieved["duration_seconds"] == 240.0
    
    print(f"  Status: {retrieved['status']}")
    print(f"  Audio URL: {retrieved['audio_url']}")
    print(f"  Script URL: {retrieved['script_url']}")
    print(f"  Duration: {retrieved['duration_seconds']}s")
    print("✅ Test 6 PASSED")


def cleanup_test_data():
    """Clean up test data."""
    print("\n=== Cleaning Up Test Data ===")
    
    test_ids = [
        "test_pod_001",
        "test_pod_002",
        "test_pod_003",
        "test_pod_list_0",
        "test_pod_list_1",
        "test_pod_list_2",
        "test_pod_multi"
    ]
    
    for podcast_id in test_ids:
        try:
            delete_podcast(podcast_id)
            print(f"✓ Deleted: {podcast_id}")
        except Exception as e:
            print(f"  (Skipped {podcast_id}: {str(e)})")
    
    print("✅ Cleanup complete")


def main():
    """Run all tests."""
    print("=" * 60)
    print("PODCAST STORAGE TEST SUITE")
    print("=" * 60)
    print("\nNote: This test only validates the database storage layer.")
    print("No actual audio files are generated or required.\n")
    
    try:
        init_database()
        print("✓ Database initialized")
        
        test_save_and_retrieve()
        test_status_progression()
        test_failed_generation()
        test_list_all_podcasts()
        test_podcast_not_found()
        test_update_with_multiple_fields()
        
        cleanup_test_data()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())