"""
Integration test script for podcast API endpoints.

This script tests the full API workflow:
1. Upload a document
2. Generate a podcast
3. Check podcast status
4. List all podcasts
5. Retrieve completed podcast

Prerequisites:
- Backend server must be running (python main.py)
- A test PDF file should be available in backend/uploads/
"""

import requests
import time
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"
TEST_PDF = Path(__file__).parent.parent / "uploads" / "test.pdf"


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_health_check():
    """Test 1: Health check."""
    print_section("Test 1: Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200, f"Health check failed: {response.status_code}"
    
    data = response.json()
    print(f"✓ Server is healthy")
    print(f"  Status: {data['status']}")
    print("✅ Test 1 PASSED")


def test_upload_document():
    """Test 2: Upload a document."""
    print_section("Test 2: Upload Document")
    
    if not TEST_PDF.exists():
        print(f"⚠️  Test PDF not found at {TEST_PDF}")
        print("   Skipping document upload test")
        return None
    
    with open(TEST_PDF, "rb") as f:
        files = {"file": (TEST_PDF.name, f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/api/documents/upload", files=files)
    
    assert response.status_code == 200, f"Upload failed: {response.status_code}"
    
    data = response.json()
    document_id = data["document_id"]
    
    print(f"✓ Document uploaded successfully")
    print(f"  Document ID: {document_id}")
    print(f"  Filename: {data['filename']}")
    print(f"  Chunks: {data['chunks_stored']}")
    print("✅ Test 2 PASSED")
    
    return document_id


def test_generate_podcast(document_id):
    """Test 3: Generate a podcast."""
    print_section("Test 3: Generate Podcast")
    
    if document_id is None:
        print("⚠️  No document ID available, skipping podcast generation")
        return None
    
    payload = {
        "document_id": document_id,
        "options": {
            "target_duration": "short"
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/podcasts/generate", json=payload)
    assert response.status_code == 202, f"Generation failed: {response.status_code}"
    
    data = response.json()
    podcast_id = data["podcast_id"]
    
    print(f"✓ Podcast generation started")
    print(f"  Podcast ID: {podcast_id}")
    print(f"  Status: {data['status']}")
    print(f"  Message: {data['message']}")
    print("✅ Test 3 PASSED")
    
    return podcast_id


def test_check_podcast_status(podcast_id):
    """Test 4: Check podcast status."""
    print_section("Test 4: Check Podcast Status")
    
    if podcast_id is None:
        print("⚠️  No podcast ID available, skipping status check")
        return
    
    response = requests.get(f"{BASE_URL}/api/podcasts/{podcast_id}")
    assert response.status_code == 200, f"Status check failed: {response.status_code}"
    
    data = response.json()
    
    print(f"✓ Retrieved podcast status")
    print(f"  Podcast ID: {data['podcast_id']}")
    print(f"  Status: {data['status']}")
    print(f"  Created at: {data['created_at']}")
    
    if data['status'] == 'processing':
        print(f"\n  ⏳ Podcast is still processing...")
        print(f"     You can check status again with:")
        print(f"     curl {BASE_URL}/api/podcasts/{podcast_id}")
    elif data['status'] == 'complete':
        print(f"  Audio URL: {data.get('audio_url')}")
        print(f"  Duration: {data.get('duration_seconds')}s")
    elif data['status'] == 'failed':
        print(f"  ❌ Error: {data.get('error')}")
    
    print("✅ Test 4 PASSED")


def test_list_all_podcasts():
    """Test 5: List all podcasts."""
    print_section("Test 5: List All Podcasts")
    
    response = requests.get(f"{BASE_URL}/api/podcasts/")
    assert response.status_code == 200, f"List failed: {response.status_code}"
    
    data = response.json()
    
    print(f"✓ Retrieved podcast list")
    print(f"  Total podcasts: {data['total']}")
    
    if data['total'] > 0:
        print(f"\n  Recent podcasts:")
        for podcast in data['podcasts'][:3]:
            print(f"    - {podcast['podcast_id']}: {podcast['status']}")
    
    print("✅ Test 5 PASSED")


def test_podcast_not_found():
    """Test 6: Podcast not found."""
    print_section("Test 6: Podcast Not Found")
    
    response = requests.get(f"{BASE_URL}/api/podcasts/nonexistent_id_12345")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    print(f"✓ Correctly returned 404 for nonexistent podcast")
    print("✅ Test 6 PASSED")


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("PODCAST API INTEGRATION TEST SUITE")
    print("=" * 60)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Test PDF: {TEST_PDF}")
    
    try:
        test_health_check()
        
        document_id = test_upload_document()
        
        podcast_id = test_generate_podcast(document_id)
        
        test_check_podcast_status(podcast_id)
        
        test_list_all_podcasts()
        
        test_podcast_not_found()
        
        print("\n" + "=" * 60)
        print("✅ ALL INTEGRATION TESTS PASSED!")
        print("=" * 60)
        
        if podcast_id:
            print(f"\n💡 TIP: Monitor your podcast generation:")
            print(f"   curl {BASE_URL}/api/podcasts/{podcast_id}")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return 1
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERROR: Could not connect to {BASE_URL}")
        print("   Make sure the backend server is running:")
        print("   cd backend && python main.py")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())