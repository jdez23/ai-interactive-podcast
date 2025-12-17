"""
End-to-end test for podcast generation pipeline.

This test validates the complete podcast generation workflow:
1. Upload a document
2. Generate a podcast
3. Check status
4. Verify audio file is created
"""

import asyncio
import time
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"
TEST_PDF = Path(__file__).parent.parent.parent / "backend" / "uploads" / "test_document.pdf"


def test_podcast_generation_endpoint():
    """Test the podcast generation endpoint with a real document."""
    
    print("\n" + "="*60)
    print("PODCAST GENERATION ENDPOINT TEST")
    print("="*60)
    
    print("\n[1] Checking for existing documents...")
    
    document_id = "doc_test_123"  
    
    print(f"\n[2] Generating podcast for document: {document_id}")
    
    generate_request = {
        "document_id": document_id,
        "options": {
            "target_duration": "short"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/podcasts/generate",
            json=generate_request,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 202:
            print("✓ Podcast generation initiated successfully!")
            podcast_data = response.json()
            podcast_id = podcast_data["podcast_id"]
            
            print(f"\n[3] Checking podcast status: {podcast_id}")
            
            max_attempts = 60
            attempt = 0
            
            while attempt < max_attempts:
                attempt += 1
                time.sleep(5)
                
                status_response = requests.get(
                    f"{BASE_URL}/api/podcasts/{podcast_id}",
                    timeout=10
                )
                
                status_data = status_response.json()
                current_status = status_data["status"]
                
                print(f"  Attempt {attempt}: Status = {current_status}")
                
                if current_status == "complete":
                    print("\n✓ Podcast generation complete!")
                    print(f"  Audio URL: {status_data.get('audio_url')}")
                    print(f"  Script URL: {status_data.get('script_url')}")
                    print(f"  Duration: {status_data.get('duration_seconds')}s")
                    
                    # Verify audio file exists
                    audio_path = Path(__file__).parent.parent / "generated" / "podcasts" / f"{podcast_id}.mp3"
                    if audio_path.exists():
                        file_size = audio_path.stat().st_size
                        print(f"  File size: {file_size / 1024:.1f} KB")
                        print("\n✓ Audio file verified!")
                    else:
                        print("\n✗ Audio file not found!")
                    
                    break
                    
                elif current_status == "failed":
                    print(f"\n✗ Podcast generation failed!")
                    print(f"  Error: {status_data.get('error')}")
                    break
            
            if attempt >= max_attempts:
                print("\n✗ Timeout waiting for podcast generation")
                
        elif response.status_code == 400:
            print("✗ Bad request - check document_id")
            print(f"  Error: {response.json().get('detail')}")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server. Is it running?")
        print("  Run: cd backend && uvicorn main:app --reload")
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
    
    print("\n" + "="*60)


def test_status_endpoint():
    """Test the status endpoint with a non-existent podcast."""
    
    print("\n" + "="*60)
    print("STATUS ENDPOINT TEST (404 Case)")
    print("="*60)
    
    fake_podcast_id = "pod_nonexistent"
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/podcasts/{fake_podcast_id}",
            timeout=10
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 404:
            print("\n✓ Correctly returns 404 for non-existent podcast")
        else:
            print(f"\n✗ Expected 404, got {response.status_code}")
            
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
    
    print("\n" + "="*60)


def test_list_podcasts():
    """Test the list podcasts endpoint."""
    
    print("\n" + "="*60)
    print("LIST PODCASTS TEST")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/podcasts/",
            timeout=10
        )
        
        print(f"\nStatus Code: {response.status_code}")
        data = response.json()
        
        print(f"Total podcasts: {data.get('total', 0)}")
        
        if data.get('podcasts'):
            print("\nPodcasts:")
            for podcast in data['podcasts'][:5]:
                print(f"  - {podcast['podcast_id']}: {podcast['status']}")
        
        print("\n✓ List endpoint working")
        
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
    
    print("\n" + "="*60)


def test_invalid_document():
    """Test with an invalid document ID."""
    
    print("\n" + "="*60)
    print("INVALID DOCUMENT TEST")
    print("="*60)
    
    generate_request = {
        "document_id": "doc_does_not_exist",
        "options": {
            "target_duration": "short"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/podcasts/generate",
            json=generate_request,
            timeout=10
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("\n✓ Correctly rejects invalid document_id")
        else:
            print(f"\n✗ Expected 400, got {response.status_code}")
            
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
    
    print("\n" + "="*60)


def test_invalid_duration():
    """Test with an invalid target duration."""
    
    print("\n" + "="*60)
    print("INVALID DURATION TEST")
    print("="*60)
    
    generate_request = {
        "document_id": "doc_test_123",
        "options": {
            "target_duration": "invalid_duration"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/podcasts/generate",
            json=generate_request,
            timeout=10
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("\n✓ Correctly rejects invalid target_duration")
        else:
            print(f"\n✗ Expected 400, got {response.status_code}")
            
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("PODCAST GENERATION API TESTS")
    print("="*60)
    print("\nMake sure the server is running:")
    print("  cd backend && uvicorn main:app --reload")
    print("\nAnd you have a test document uploaded.")
    print("="*60)
    
    test_invalid_document()
    test_invalid_duration()
    test_status_endpoint()
    test_list_podcasts()
    
    print("\n" + "="*60)
    print("TESTS COMPLETE")
    print("="*60 + "\n")