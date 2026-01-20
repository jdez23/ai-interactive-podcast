"""
Manual test script for Q&A system with real podcasts.

Run this interactively to test the complete Q&A flow.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.question_answerer import answer_question, QuestionAnswererError


async def main():
    """Interactive Q&A testing."""
    print("\n" + "="*60)
    print("Q&A SYSTEM - MANUAL TEST")
    print("="*60)
    print("\nThis script lets you test the Q&A system with a real podcast.")
    print("You'll need a podcast_id from a completed podcast.\n")
    
    podcast_id = input("Enter podcast_id: ").strip()
    
    if not podcast_id:
        print("❌ No podcast_id provided. Exiting.")
        return
    
    print(f"\n✅ Testing with podcast: {podcast_id}")
    print("\nYou can now ask questions. Type 'quit' to exit.\n")
    
    while True:
        question = input("\n❓ Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not question:
            print("⚠️  Please enter a question")
            continue
        
        timestamp_input = input("⏱️  Timestamp (seconds, or press Enter for 100): ").strip()
        timestamp = float(timestamp_input) if timestamp_input else 100.0
        
        print(f"\n🔄 Generating answer...")
        
        try:
            answer = await answer_question(
                podcast_id=podcast_id,
                question=question,
                timestamp=timestamp
            )
            
            print(f"\n{'='*60}")
            print("📝 ANSWER:")
            print(f"{'='*60}")
            print(f"{answer['answer_text']}")
            print(f"\n📚 Sources: {', '.join(answer['sources'])}")
            print(f"📊 Context: {answer['context_used']['document_chunks']} chunks, "
                  f"{answer['context_used']['dialogue_exchanges']} dialogue exchanges")
            print(f"{'='*60}")
            
        except QuestionAnswererError as e:
            print(f"\n❌ Error: {str(e)}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")