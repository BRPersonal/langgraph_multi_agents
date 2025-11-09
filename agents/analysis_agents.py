"""
Analysis Team Agents
"""
from typing import Dict, Any
from agents.base import BaseAgent
from tools.analysis_tools import analyze_sentiment, detect_patterns
from utils.logger import logger


class AnalystAgent(BaseAgent):
    """Agent specialized in analyzing trends and patterns."""
    
    def __init__(self):
        super().__init__(
            name="Analyst",
            temperature=0.5,
            use_google=False  # Using Groq instead
        )
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze research findings."""
        logger.info(f"{self.name}: Starting analysis")
        
        try:
            research_notes = state.get('research_notes', '')
            
            # Detect patterns
            topics = state.get('trending_topics', [])
            patterns = detect_patterns.invoke({"data": topics})
            
            # Perform analysis
            prompt = f"""Analyze these research findings:

{research_notes}

Common Patterns:
{chr(10).join(f'- {p}' for p in patterns)}

Provide:
1. Key Insights (3-4 bullet points)
2. Market Implications (2-3 sentences)
3. Emerging Trends (2-3 bullet points)

Keep it concise and actionable."""
            
            analysis = self.invoke(prompt)
            
            logger.info(f"{self.name}: Analysis complete")
            return {
                "analysis_results": analysis,
                "patterns": patterns,
                "next_agent": "writer"
            }
        
        except Exception as e:
            logger.error(f"{self.name} error: {str(e)}")
            return {
                "analysis_results": f"Analysis error: {str(e)}",
                "next_agent": "writer"
            }

class SentimentAnalyzer(BaseAgent):
    """Agent specialized in sentiment analysis."""
    
    def __init__(self):
        super().__init__(
            name="Sentiment Analyzer",
            temperature=0.2
        )
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sentiment of findings."""
        logger.info(f"{self.name}: Analyzing sentiment")
        
        try:
            research_notes = state.get('research_notes', '')
            sentiment_data = analyze_sentiment.invoke({"text": research_notes})
            
            logger.info(f"{self.name}: Sentiment is {sentiment_data['sentiment']}")
            return {
                "sentiment_analysis": sentiment_data
            }
        
        except Exception as e:
            logger.error(f"{self.name} error: {str(e)}")
            return {
                "sentiment_analysis": {"sentiment": "neutral", "score": 50}
            }

