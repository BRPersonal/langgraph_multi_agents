"""
Helper Utilities
"""
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from utils.config import settings
from utils.logger import logger


def format_messages(messages: List[Dict[str, str]]) -> str:
    """Format message list into readable string."""
    formatted = []
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        formatted.append(f"{role.upper()}: {content}")
    return "\n\n".join(formatted)

def extract_text(response: Any) -> str:
    """Extract text content from various response formats."""
    if isinstance(response, str):
        return response
    elif hasattr(response, 'content'):
        return response.content
    elif isinstance(response, dict):
        return response.get('content', str(response))
    else:
        return str(response)

def retry_with_backoff(max_attempts: int = None):
    """Decorator for retrying functions with exponential backoff."""
    if max_attempts is None:
        max_attempts = settings.max_retries
    
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )

def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def count_tokens_estimate(text: str) -> int:
    """Rough estimate of token count (4 chars ≈ 1 token)."""
    return len(text) // 4

