"""
LLM Service Wrapper
Handles communication with LLM APIs for dialogue generation
Supports OpenAI, DeepSeek, and other compatible APIs
"""

import os
import logging
from typing import List, Dict, Optional, AsyncGenerator
import asyncio

logger = logging.getLogger(__name__)


class LLMService:
    """Wrapper for LLM API calls"""
    
    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        """
        Initialize LLM service
        
        Args:
            provider: LLM provider (openai, deepseek, etc.)
            model: Model name
            api_key: API key (defaults to env var)
            base_url: API base URL (for non-OpenAI providers)
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key or os.environ.get("DIALOGUE_API_KEY") or os.environ.get("CHAT_API_KEY")
        self.base_url = base_url or os.environ.get("DIALOGUE_BASE_URL")
        
        if not self.api_key:
            logger.warning("No API key found for LLM service")
        
        self._init_client()
    
    def _init_client(self):
        """Initialize LLM client based on provider"""
        
        try:
            from openai import AsyncOpenAI
            
            # Build OpenAI client with optional base_url for DeepSeek
            client_kwargs = {"api_key": self.api_key}
            if self.base_url:
                client_kwargs["base_url"] = self.base_url
            
            self.client = AsyncOpenAI(**client_kwargs)
            logger.info(f"Initialized {self.provider} client with model: {self.model}")
            if self.base_url:
                logger.info(f"Using custom base URL: {self.base_url}")
        except ImportError:
            logger.error("OpenAI package not installed: pip install openai")
            self.client = None
    
    async def generate_dialogue(
        self,
        system_prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate dialogue from system prompt
        
        Args:
            system_prompt: System prompt for LLM
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation
            
        Returns:
            Generated dialogue text
        """
        
        if not self.client:
            raise RuntimeError("LLM client not initialized")
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            dialogue = response.choices[0].message.content
            logger.info(f"Generated dialogue ({len(dialogue)} chars)")
            return dialogue
            
        except Exception as e:
            logger.error(f"Error generating dialogue: {e}")
            raise
    
    async def generate_dialogue_stream(
        self,
        system_prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        """
        Generate dialogue with streaming
        
        Args:
            system_prompt: System prompt for LLM
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation
            
        Yields:
            Chunks of dialogue text
        """
        
        if not self.client:
            raise RuntimeError("LLM client not initialized")
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True,
            )
            
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error in streaming dialogue: {e}")
            raise
    
    @staticmethod
    def test_connection(api_key: Optional[str] = None) -> bool:
        """Test LLM connection"""
        
        api_key = api_key or os.environ.get("CHAT_API_KEY")
        
        if not api_key:
            logger.error("No API key available for testing")
            return False
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            # Simple test
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say hello"}],
                max_tokens=10,
            )
            
            logger.info("LLM connection test successful")
            return True
            
        except Exception as e:
            logger.error(f"LLM connection test failed: {e}")
            return False
