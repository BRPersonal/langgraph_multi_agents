"""
Data Processing Tools
"""
from typing import List, Dict, Any
from langchain_core.tools import tool
from utils.logger import logger
import json


@tool
def process_data(data: List[Dict[str, Any]], operation: str = "filter") -> List[Dict[str, Any]]:
    """
    Process and transform data.
    
    Args:
        data: List of data dictionaries
        operation: Operation to perform (filter, sort, group)
    
    Returns:
        Processed data
    """
    logger.info(f"Processing data with operation: {operation}")
    
    if operation == "filter":
        # Filter out low-quality items
        processed = [item for item in data if len(str(item)) > 50]
    elif operation == "sort":
        # Sort by relevance (simplified)
        processed = sorted(data, key=lambda x: len(str(x)), reverse=True)
    else:
        processed = data
    
    logger.info(f"Processed {len(processed)} items")
    return processed

@tool
def summarize_text(text: str, max_length: int = 200) -> str:
    """
    Summarize long text content.
    
    Args:
        text: Text to summarize
        max_length: Maximum length of summary
    
    Returns:
        Summarized text
    """
    logger.info(f"Summarizing text of length: {len(text)}")
    
    if len(text) <= max_length:
        return text
    
    # Simple extractive summarization (in production, use LLM)
    sentences = text.split(". ")
    summary = ". ".join(sentences[:3]) + "."
    
    if len(summary) > max_length:
        summary = summary[:max_length-3] + "..."
    
    logger.info(f"Generated summary of length: {len(summary)}")
    return summary

