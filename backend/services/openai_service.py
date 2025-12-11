"""
OpenAI service for generating podcast scripts and handling LLM interactions.

This service provides:
- OpenAI client configuration
- Prompt template management
- Error handling and retry logic
- Token usage tracking
"""

import logging
import time
from typing import Dict, List, Optional
from openai import OpenAI, OpenAIError, APIError, RateLimitError, APIConnectionError, APITimeoutError
from config.settings import OPENAI_API_KEY, DEFAULT_MODEL, DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=30.0
)


class OpenAIServiceError(Exception):
    """Custom exception for OpenAI service errors."""
    pass


def exponential_backoff_retry(func):
    """
    Decorator for exponential backoff retry logic.
    
    Retries the function up to 3 times with exponential backoff:
    - 1st retry: wait 1 second
    - 2nd retry: wait 2 seconds
    - 3rd retry: wait 4 seconds
    """
    def wrapper(*args, **kwargs):
        max_retries = 3
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except RateLimitError as e:
                if attempt == max_retries - 1:
                    logger.error(f"Rate limit exceeded after {max_retries} attempts")
                    raise OpenAIServiceError(f"Rate limit exceeded: {str(e)}")
                
                delay = base_delay * (2 ** attempt)
                logger.warning(f"Rate limit hit, retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                
            except (APIConnectionError, APITimeoutError) as e:
                if attempt == max_retries - 1:
                    logger.error(f"Network error after {max_retries} attempts: {str(e)}")
                    raise OpenAIServiceError(f"Network error: {str(e)}")
                
                delay = base_delay * (2 ** attempt)
                logger.warning(f"Network error, retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                
            except APIError as e:
                # Don't retry on API errors (invalid request, etc.)
                logger.error(f"OpenAI API error: {str(e)}")
                raise OpenAIServiceError(f"API error: {str(e)}")
                
            except OpenAIError as e:
                logger.error(f"OpenAI error: {str(e)}")
                raise OpenAIServiceError(f"OpenAI error: {str(e)}")
                
    return wrapper


def create_podcast_dialogue_prompt(
    topic: str,
    document_chunks: str,
    duration_minutes: int = 5
) -> str:
    """
    Create a prompt for generating podcast dialogue.
    
    Args:
        topic: The topic of the podcast
        document_chunks: Relevant text content from documents
        duration_minutes: Target duration in minutes (default: 5)
        
    Returns:
        Formatted prompt string
    """
    word_count = duration_minutes * 150
    
    prompt = f"""You are creating a natural, engaging podcast discussion between two hosts about a specific topic.

**Hosts:**
- Host A (Alex): Curious, asks insightful questions, represents the learner
- Host B (Jordan): Knowledgeable, explains clearly, makes complex topics accessible

**Topic:** {topic}

**Source Material:**
{document_chunks}

**Instructions:**
1. Create a {duration_minutes}-minute podcast script (approximately {word_count} words)
2. Start with a warm, engaging introduction
3. Discuss 3-4 key points from the source material
4. Use natural conversation - including reactions like "wow," "interesting," "that's fascinating"
5. Alex should ask follow-up questions that a learner would ask
6. Jordan should explain concepts clearly with examples or analogies
7. End with a brief, memorable conclusion
8. Stay true to the source material - don't make up facts

**CRITICAL: Format your response EXACTLY like this:**
Host A: [Line of dialogue]
Host B: [Response]
Host A: [Follow-up]
Host B: [Explanation]
...

Do not include any text outside of the script format. Do not use markdown code blocks. Begin now:
"""
    return prompt


@exponential_backoff_retry
def generate_completion(
    prompt: str,
    model: str = "gpt-4o-mini",
    max_tokens: Optional[int] = None,
    temperature: float = 0.7
) -> Dict:
    """
    Generate a completion using OpenAI API with error handling and retry logic.
    
    Args:
        prompt: The prompt to send to the model
        model: Model to use (default: gpt-4o-mini for cost-effectiveness)
        max_tokens: Maximum tokens to generate (default: None for no limit)
        temperature: Sampling temperature 0-2 (default: 0.7)
        
    Returns:
        Dictionary containing:
        - content: The generated text
        - usage: Token usage statistics
        - model: Model used
        
    Raises:
        OpenAIServiceError: If the API call fails after retries
    """
    try:
        logger.info(f"Generating completion with model: {model}")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates engaging podcast scripts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        content = response.choices[0].message.content
        usage = response.usage
        
        logger.info(f"Token usage - Prompt: {usage.prompt_tokens}, "
                   f"Completion: {usage.completion_tokens}, "
                   f"Total: {usage.total_tokens}")
        
        return {
            "content": content,
            "usage": {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            },
            "model": model
        }
        
    except Exception as e:
        raise


def generate_podcast_dialogue(
    topic: str,
    document_chunks: str,
    duration_minutes: int = 5,
    model: str = "gpt-4o-mini"
) -> Dict:
    """
    Generate podcast dialogue from document chunks.
    
    This is a high-level function that combines prompt creation and completion.
    
    Args:
        topic: The topic of the podcast
        document_chunks: Relevant text content from documents
        duration_minutes: Target duration in minutes (default: 5)
        model: Model to use (default: gpt-4o-mini)
        
    Returns:
        Dictionary containing:
        - dialogue: The generated host/guest conversation
        - usage: Token usage statistics
        - model: Model used
        
    Example:
        result = generate_podcast_dialogue(
            topic="The American Revolution",
            document_chunks="The American Revolution began in 1775...",
            duration_minutes=3
        )
        print(result["dialogue"])
        # Output:
        # Host A: Welcome to today's discussion about the American Revolution!
        # Host B: Thanks for having me! This is such a fascinating period...
    """
    prompt = create_podcast_dialogue_prompt(topic, document_chunks, duration_minutes)
    
    result = generate_completion(
        prompt=prompt,
        model=model,
        temperature=0.7
    )
    
    return {
        "dialogue": result["content"],
        "usage": result["usage"],
        "model": result["model"]
    }


def validate_api_key() -> bool:
    """
    Validate that the OpenAI API key is configured and working.
    
    Returns:
        True if API key is valid, False otherwise
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY not found in environment variables")
        return False
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        logger.info("OpenAI API key validated successfully")
        return True
    except Exception as e:
        logger.error(f"API key validation failed: {str(e)}")
        return False


def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a text string.
    
    This is a rough estimate: ~4 characters per token for English text.
    For precise counting, use tiktoken library.
    
    Args:
        text: The text to estimate tokens for
        
    Returns:
        Estimated token count
    """
    return len(text) // 4