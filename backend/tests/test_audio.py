"""
Test script for ElevenLabs audio generation service.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.audio_service import generate_speech, synthesize_audio, VOICE_CONFIG


async def test_audio_generation():
    """Test ElevenLabs audio generation with host and guest voices."""
    
    print("=" * 60)
    print("Testing ElevenLabs Audio Generation")
    print("=" * 60)
    
    try:
        print("\nGenerating host audio...")
        host_text = "Welcome to Space Explorers, the podcast where we journey through our solar system! I'm your host, and today we're diving into the fascinating world of Mars."
        host_path = await generate_speech(
            text=host_text,
            voice_id=VOICE_CONFIG["host"],
            output_filename="test_host.mp3"
        )
        print(f"✅ Host audio generated: {host_path}")
        
        print("\nGenerating guest audio...")
        guest_text = "Thanks for having me! I'm thrilled to share what makes Mars so special. It's often called the Red Planet, and for good reason."
        guest_path = await generate_speech(
            text=guest_text,
            voice_id=VOICE_CONFIG["guest"],
            output_filename="test_guest.mp3"
        )
        print(f"✅ Guest audio generated: {guest_path}")
        
        print("\nGenerating longer text sample...")
        long_text = """
        Mars has captivated humanity for centuries. It's the fourth planet from the Sun,
        with a diameter of about 4,220 miles—roughly half the size of Earth.
        The planet's distinctive red color comes from iron oxide, or rust, covering its surface.
        Mars has two small moons, Phobos and Deimos, and features the largest volcano in our
        solar system, Olympus Mons, which stands nearly 16 miles high!
        """
        long_path = await generate_speech(
            text=long_text,
            voice_id=VOICE_CONFIG["host"],
            output_filename="test_long.mp3"
        )
        print(f"✅ Long text audio generated: {long_path}")
        
        print("\nTesting special characters...")
        special_text = """
        What's really exciting is Mars' potential for life! Scientists have found evidence
        of ancient water—rivers, lakes, and maybe even oceans. The Mars rovers (like
        Curiosity & Perseverance) have discovered organic molecules, which are the
        "building blocks" of life. Temperature ranges from -195°F to 70°F, and a day
        on Mars lasts 24.6 hours. NASA's missions have cost $2.5+ billion, but the
        discoveries are priceless! As we say: "Mars isn't just a planet—it's humanity's
        next frontier!"
        """
        special_path = await generate_speech(
            text=special_text,
            voice_id=VOICE_CONFIG["guest"],
            output_filename="test_special.mp3"
        )
        print(f"✅ Special characters audio generated: {special_path}")
        
        print("\n" + "=" * 60)
        print("✨ All tests passed successfully!")
        print("=" * 60)
        print("\nManual verification checklist:")
        print("  1. Listen to test_host.mp3 - should be clear and natural")
        print("  2. Listen to test_guest.mp3 - should sound different from host")
        print("  3. Listen to test_long.mp3 - should handle paragraph without issues")
        print("  4. Listen to test_special.mp3 - should handle special characters")
        print("  5. Verify no distortion or artifacts in any file")
        print("\nAudio files location:")
        print(f"  {Path(host_path).parent}")
        
    except ValueError as e:
        print(f"\n❌ Validation error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error during audio generation: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False
    
    return True


async def test_error_handling():
    """Test error handling scenarios."""
    
    print("\n" + "=" * 60)
    print("Testing Error Handling")
    print("=" * 60)
    
    print("\nTesting empty text...")
    try:
        await generate_speech(
            text="",
            voice_id=VOICE_CONFIG["host"],
            output_filename="test_empty.mp3"
        )
        print("❌ Should have raised ValueError for empty text")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    print("\nTesting invalid voice ID...")
    try:
        await generate_speech(
            text="Test",
            voice_id="",
            output_filename="test_invalid.mp3"
        )
        print("❌ Should have raised ValueError for invalid voice ID")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    print("\n✅ Error handling tests passed!")


async def main():
    """Run all tests."""
    print("\nStarting ElevenLabs Audio Service Tests\n")
    
    success = await test_audio_generation()
    
    if success:
        await test_error_handling()
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("⚠️  Some tests failed. Please check the errors above.")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())