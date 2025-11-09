"""
Base Agent Class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import settings
from utils.logger import logger


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(
        self,
        name: str,
        model_name: str = None,
        temperature: float = 0.7,
        use_google: bool = False
    ):
        self.name = name
        self.model_name = model_name or settings.DEFAULT_MODEL
        self.temperature = temperature
        
        logger.info(f"Initializing agent: {name}")
        
        # Initialize model
        if use_google:
            self.model = ChatGoogleGenerativeAI(
                model=settings.FAST_MODEL,
                temperature=temperature,
                google_api_key=settings.GOOGLE_API_KEY
            )
        else:
            self.model = ChatGroq(
                model=self.model_name,
                temperature=temperature,
                groq_api_key=settings.GROQ_API_KEY
            )
    
    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent's main task."""
        pass
    
    def invoke(self, prompt: str) -> str:
        """Invoke the model with a prompt."""
        try:
            response = self.model.invoke(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Error in {self.name}: {str(e)}")
            raise

