"""
Analysis and Pattern Detection Tools
"""
from typing import Dict, List, Any
from langchain_core.tools import tool
from utils.logger import logger
import re


@tool
def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of text content.
    
    Args:
        text: Text to analyze
    
    Returns:
        Sentiment analysis results
    """
    logger.info("Analyzing sentiment")
    
    # Simple keyword-based sentiment (in production, use LLM or dedicated service)
    positive_keywords = ['good', 'great', 'excellent', 'amazing', 'love', 'best', 'innovative']
    negative_keywords = ['bad', 'terrible', 'awful', 'hate', 'worst', 'poor', 'broken']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_keywords if word in text_lower)
    negative_count = sum(1 for word in negative_keywords if word in text_lower)
    
    total = positive_count + negative_count
    if total == 0:
        sentiment = "neutral"
        score = 50
    else:
        score = int((positive_count / total) * 100)
        if score > 60:
            sentiment = "positive"
        elif score < 40:
            sentiment = "negative"
        else:
            sentiment = "mixed"
    
    result = {
        "sentiment": sentiment,
        "score": score,
        "confidence": min(total * 10, 100),
        "positive_signals": positive_count,
        "negative_signals": negative_count
    }
    
    logger.info(f"Sentiment: {sentiment} (score: {score})")
    return result

@tool
def detect_patterns(data: List[str]) -> List[str]:
    """
    Detect common patterns in text data.
    
    Args:
        data: List of text items
    
    Returns:
        List of detected patterns
    """
    logger.info(f"Detecting patterns in {len(data)} items")
    
    # Find common keywords
    word_freq = {}
    for item in data:
        words = re.findall(r'\b[a-z]{4,}\b', item.lower())
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get top patterns
    patterns = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    result = [f"{word} (appears {count} times)" for word, count in patterns]
    
    logger.info(f"Detected {len(result)} patterns")
    return result

