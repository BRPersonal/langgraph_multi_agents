"""
Writing Team Agents
"""
from typing import Dict, Any
from agents.base import BaseAgent
from utils.logger import logger

class WriterAgent(BaseAgent):
    """Agent specialized in creating final reports."""
    
    def __init__(self):
        super().__init__(
            name="Writer",
            model_name="llama-3.3-70b-versatile",
            temperature=0.7
        )
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create final report."""
        logger.info(f"{self.name}: Writing report")
        
        try:
            research_notes = state.get('research_notes', '')
            analysis_results = state.get('analysis_results', '')
            
            prompt = f"""Create an executive summary for tech professionals.

**Research Findings:**
{research_notes}

**Analysis:**
{analysis_results}

Format as:
# Weekly Tech Intelligence Report

## Executive Summary
(3-4 sentences highlighting the most important findings)

## Key Developments
(4-5 bullet points of major developments)

## Strategic Insights
(2-3 paragraphs discussing implications and opportunities)

## Recommendations
(3-4 actionable recommendations)

Keep it professional, concise, and focused on actionable insights."""
            
            report = self.invoke(prompt)
            
            logger.info(f"{self.name}: Report complete")
            return {
                "final_report": report,
                "next_agent": "END"
            }
        
        except Exception as e:
            logger.error(f"{self.name} error: {str(e)}")
            return {
                "final_report": f"Error generating report: {str(e)}",
                "next_agent": "END"
            }

class EditorAgent(BaseAgent):
    """Agent specialized in editing and refining content."""
    
    def __init__(self):
        super().__init__(
            name="Editor",
            temperature=0.3
        )
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Edit and refine the report."""
        logger.info(f"{self.name}: Editing report")
        
        try:
            draft = state.get('final_report', '')
            
            prompt = f"""Review and improve this report:

{draft}

Make it:
1. More concise (remove redundancy)
2. More professional (improve tone)
3. More actionable (strengthen recommendations)

Return the improved version."""
            
            edited_report = self.invoke(prompt)
            
            logger.info(f"{self.name}: Editing complete")
            return {
                "final_report": edited_report,
                "next_agent": "END"
            }
        
        except Exception as e:
            logger.error(f"{self.name} error: {str(e)}")
            return {"next_agent": "END"}

