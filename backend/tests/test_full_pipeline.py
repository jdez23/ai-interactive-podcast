"""
Complete end-to-end test for the full podcast generation pipeline.

This test:
1. Uploads a real PDF document
2. Generates a podcast from it
3. Verifies the complete workflow
"""

import asyncio
import time
import requests
import json
from pathlib import Path
import sys

BASE_URL = "http://localhost:8000"


def upload_document(pdf_path: Path) -> str:
    """
    Upload a PDF document and return the document_id.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        document_id from the upload response
    """
    print(f"\n[1] Uploading document: {pdf_path.name}")
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    with open(pdf_path, "rb") as f:
        files = {"file": (pdf_path.name, f, "application/pdf")}
        response = requests.post(
            f"{BASE_URL}/api/documents/upload",
            files=files,
            timeout=30
        )
    
    if response.status_code != 200:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")
    
    data = response.json()
    document_id = data["document_id"]
    chunks_count = data["chunks_count"]
    
    print(f"    ✓ Document uploaded successfully")
    print(f"    ✓ Document ID: {document_id}")
    print(f"    ✓ Chunks created: {chunks_count}")
    
    return document_id


def generate_podcast(document_id: str, target_duration: str = "short") -> str:
    """
    Generate a podcast from a document.
    
    Args:
        document_id: Document ID to generate podcast from
        target_duration: short, medium, or long
        
    Returns:
        podcast_id from the generation response
    """
    print(f"\n[2] Generating podcast (duration: {target_duration})")
    
    response = requests.post(
        f"{BASE_URL}/api/podcasts/generate",
        json={
            "document_id": document_id,
            "options": {
                "target_duration": target_duration
            }
        },
        timeout=300
    )
    
    if response.status_code != 202:
        raise Exception(f"Generation failed: {response.status_code} - {response.text}")
    
    data = response.json()
    podcast_id = data["podcast_id"]
    
    print(f"    ✓ Podcast generation started")
    print(f"    ✓ Podcast ID: {podcast_id}")
    print(f"    ✓ Status: {data['status']}")
    
    return podcast_id


def wait_for_completion(podcast_id: str, max_wait_seconds: int = 300) -> dict:
    """
    Poll for podcast completion.
    
    Args:
        podcast_id: Podcast ID to check
        max_wait_seconds: Maximum time to wait
        
    Returns:
        Final podcast status data
    """
    print(f"\n[3] Waiting for podcast generation to complete...")
    print(f"    (Max wait time: {max_wait_seconds} seconds)")
    
    start_time = time.time()
    attempt = 0
    
    while time.time() - start_time < max_wait_seconds:
        attempt += 1
        time.sleep(5)
        
        response = requests.get(
            f"{BASE_URL}/api/podcasts/{podcast_id}",
            timeout=10
        )
        
        if response.status_code != 200:
            raise Exception(f"Status check failed: {response.status_code}")
        
        data = response.json()
        status = data["status"]
        
        elapsed = int(time.time() - start_time)
        print(f"    [{attempt}] {elapsed}s - Status: {status}", end="")
        
        if "stage" in data:
            print(f" (Stage: {data.get('stage')})")
        else:
            print()
        
        if status == "complete":
            return data
        elif status == "failed":
            raise Exception(f"Podcast generation failed: {data.get('error')}")
    
    raise TimeoutError(f"Podcast generation timed out after {max_wait_seconds}s")


def verify_podcast(podcast_data: dict) -> bool:
    """
    Verify the generated podcast.
    
    Args:
        podcast_data: Podcast status data
        
    Returns:
        True if verification passes
    """
    print(f"\n[4] Verifying generated podcast...")
    
    required_fields = ["podcast_id", "audio_url", "duration_seconds"]
    for field in required_fields:
        if field not in podcast_data or podcast_data[field] is None:
            print(f"    ✗ Missing field: {field}")
            return False
    
    print(f"    ✓ All required fields present")
    
    podcast_id = podcast_data["podcast_id"]
    audio_path = Path(__file__).parent.parent / "generated" / "podcasts" / f"{podcast_id}.mp3"
    
    if not audio_path.exists():
        print(f"    ✗ Audio file not found: {audio_path}")
        return False
    
    file_size = audio_path.stat().st_size
    print(f"    ✓ Audio file exists: {file_size / 1024:.1f} KB")
    
    script_path = Path(__file__).parent.parent / "generated" / "podcasts" / f"{podcast_id}_script.json"
    
    if not script_path.exists():
        print(f"    ✗ Script file not found: {script_path}")
        return False
    
    print(f"    ✓ Script file exists")
    
    with open(script_path, "r") as f:
        script = json.load(f)
    
    if not isinstance(script, list) or len(script) == 0:
        print(f"    ✗ Invalid script structure")
        return False
    
    print(f"    ✓ Script has {len(script)} exchanges")
    
    duration = podcast_data["duration_seconds"]
    if duration < 10 or duration > 1800:
        print(f"    ✗ Unusual duration: {duration}s")
        return False
    
    print(f"    ✓ Duration is reasonable: {duration:.1f}s ({duration/60:.1f} minutes)")
    
    return True


def main():
    """Run the complete end-to-end test."""
    
    print("\n" + "="*70)
    print("COMPLETE PODCAST GENERATION PIPELINE TEST")
    print("="*70)
    
    if len(sys.argv) > 1:
        pdf_path = Path(sys.argv[1])
    else:
        pdf_input = input("\nEnter path to PDF file: ").strip()
        pdf_path = Path(pdf_input)
    
    if len(sys.argv) > 2:
        target_duration = sys.argv[2]
    else:
        target_duration = input("Enter target duration (short/medium/long) [short]: ").strip() or "short"
    
    try:
        document_id = upload_document(pdf_path)
        
        podcast_id = generate_podcast(document_id, target_duration)
        
        podcast_data = wait_for_completion(podcast_id)
        
        success = verify_podcast(podcast_data)
        
        print("\n" + "="*70)
        if success:
            print("✓ COMPLETE PIPELINE TEST PASSED!")
        else:
            print("✗ VERIFICATION FAILED")
        print("="*70)
        
        print(f"\nPodcast Details:")
        print(f"  Podcast ID: {podcast_data['podcast_id']}")
        print(f"  Audio URL: {podcast_data['audio_url']}")
        print(f"  Script URL: {podcast_data.get('script_url')}")
        print(f"  Duration: {podcast_data['duration_seconds']:.1f}s")
        print(f"  Created: {podcast_data['created_at']}")
        
        print(f"\nAccess your podcast at:")
        print(f"  {BASE_URL}{podcast_data['audio_url']}")
        
        print("\n" + "="*70 + "\n")
        
        return 0 if success else 1
        
    except FileNotFoundError as e:
        print(f"\n✗ ERROR: {e}")
        return 1
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to server")
        print("  Make sure the server is running:")
        print("  cd backend && uvicorn main:app --reload")
        return 1
    except TimeoutError as e:
        print(f"\n✗ ERROR: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)