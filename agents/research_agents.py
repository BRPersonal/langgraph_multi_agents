"""
Research Team Agents
"""
from typing import Dict, Any, List
from agents.base import BaseAgent
from tools.search_tools import fetch_trending_topics, search_articles
from utils.logger import logger

class ResearchAgent(BaseAgent):
    """Agent specialized in gathering trending information."""
    
    def __init__(self):
        super().__init__(
            name="Researcher",
            temperature=0.3,
            use_google=False  # Using Groq instead
        )
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gather trending topics."""
        logger.info(f"{self.name}: Starting research")
        
        try:
            # Fetch trending topics
            topics = fetch_trending_topics.invoke({"timeframe": "week", "limit": 5})
            
            # Format research notes
            prompt = f"""You are a research specialist.
            
Task: {state.get('current_task', 'Research trending topics')}

I've found these trending topics:
{chr(10).join(f'{i+1}. {topic}' for i, topic in enumerate(topics))}

Create a brief overview of why these topics are trending (2-3 sentences total)."""
            
            overview = self.invoke(prompt)
            
            research_notes = f"""## Trending Topics

{chr(10).join(f'{i+1}. {topic}' for i, topic in enumerate(topics))}

## Overview
{overview}"""
            
            logger.info(f"{self.name}: Research complete")
            return {
                "research_notes": research_notes,
                "trending_topics": topics,
                "next_agent": "collector"
            }
        
        except Exception as e:
            logger.error(f"{self.name} error: {str(e)}")
            return {
                "research_notes": f"Error in research: {str(e)}",
                "next_agent": "analyst"
            }

class DataCollectorAgent(BaseAgent):
    """Agent specialized in gathering detailed information."""
    
    def __init__(self):
        super().__init__(
            name="Data Collector",
            temperature=0.3,
            use_google=False  # Using Groq instead
        )
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Collect detailed data about topics."""
        logger.info(f"{self.name}: Collecting data")
        
        try:
            topics = state.get('trending_topics', [])
            all_articles = []
            
            # Gather articles for each topic
            for topic in topics[:3]:  # Limit to 3 topics for speed
                articles = search_articles.invoke({
                    "topic": topic,
                    "max_results": 2
                })
                all_articles.extend(articles)
            
            # Format detailed data
            articles_text = "\n\n".join([
                f"**{article['title']}**\n{article['summary']}\nSource: {article['source']}"
                for article in all_articles
            ])
            
            detailed_data = f"""## Detailed Research Data

{articles_text}"""
            
            # Combine with existing research
            updated_notes = state.get('research_notes', '') + "\n\n" + detailed_data
            
            logger.info(f"{self.name}: Data collection complete")
            return {
                "research_notes": updated_notes,
                "articles": all_articles,
                "next_agent": "analyst"
            }
        
        except Exception as e:
            logger.error(f"{self.name} error: {str(e)}")
            return {"next_agent": "analyst"}

