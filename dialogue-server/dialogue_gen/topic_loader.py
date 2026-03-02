"""
Topic Loader
Reads topic descriptions and metadata from .md files
"""

import logging
import re
from pathlib import Path
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


class TopicMetadata:
    """Metadata extracted from topic .md file"""
    
    def __init__(self):
        self.title: str = "Dialogue"
        self.description: str = ""
        self.style: str = "a little nsfw"  # sfw, a little nsfw, nsfw
        self.location: Optional[str] = None
        self.mood: Optional[str] = None
        self.context: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "title": self.title,
            "style": self.style,
            "location": self.location,
            "mood": self.mood,
        }


class TopicLoader:
    """Load and parse topic metadata from markdown files"""
    
    @staticmethod
    def load_topic(topic_path: Path | str) -> tuple[str, TopicMetadata]:
        """
        Load topic from markdown file
        
        Args:
            topic_path: Path to topic.md file
            
        Returns:
            Tuple of (full_topic_text, metadata)
        """
        topic_path = Path(topic_path)
        metadata = TopicMetadata()
        
        if not topic_path.exists():
            logger.warning(f"Topic file not found: {topic_path}")
            return "", metadata
        
        try:
            with open(topic_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title (first # line)
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if title_match:
                metadata.title = title_match.group(1).strip()
            
            # Extract YAML-like metadata blocks or key: value patterns
            style_match = re.search(r'^[#\s]*[Ss]tyle[:\s]+(.+)$', content, re.MULTILINE)
            if style_match:
                style_val = style_match.group(1).strip().lower()
                if style_val in ('sfw', 'a little nsfw', 'nsfw'):
                    metadata.style = style_val
            
            location_match = re.search(r'^[#\s]*[Ll]ocation[:\s]+(.+)$', content, re.MULTILINE)
            if location_match:
                metadata.location = location_match.group(1).strip()
            
            mood_match = re.search(r'^[#\s]*[Mm]ood[:\s]+(.+)$', content, re.MULTILINE)
            if mood_match:
                metadata.mood = mood_match.group(1).strip()
            
            # Extract description (everything after title up to the next ## section)
            desc_match = re.search(r'^# .+\n\n(.+?)(?=\n##|\Z)', content, re.MULTILINE | re.DOTALL)
            if desc_match:
                metadata.description = desc_match.group(1).strip()
            
            logger.info(f"Loaded topic: {metadata.title}")
            logger.info(f"  Style: {metadata.style}, Location: {metadata.location}")
            
            return content, metadata
            
        except Exception as e:
            logger.error(f"Error loading topic: {e}")
            return "", metadata
