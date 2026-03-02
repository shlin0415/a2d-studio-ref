"""
Data models for dialogue generation system
Based on LingChat's CharacterSettings and SillyTavern's character format
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict


class VoiceModel(BaseModel):
    """Voice synthesis configuration"""
    sva_speaker_id: Optional[str] = None
    sbv2_name: Optional[str] = None
    sbv2_speaker_id: Optional[str] = None
    bv2_speaker_id: Optional[str] = None


class CharacterSettings(BaseModel):
    """
    Character configuration model
    Mirrors LingChat's structure with additions for dialogue generation
    """

    model_config = ConfigDict(extra="allow")

    # Basic Info
    ai_name: str = Field(default="character_name")
    character_key: Optional[str] = None  # Folder name (ema, hiro, etc.)
    ai_subtitle: Optional[str] = ""
    user_name: str = Field(default="player")
    user_subtitle: Optional[str] = ""

    # Prompts (CRITICAL)
    system_prompt: Optional[str] = None
    system_prompt_example: Optional[str] = None
    system_prompt_example_old: Optional[str] = None

    # Voice
    voice_models: Optional[VoiceModel] = None
    tts_type: Optional[str] = None

    # Visual
    body_part: Optional[Dict[str, Any]] = None
    scale: float = 1.0
    clothes_name: Optional[str] = None
    available_emotions: Optional[List[str]] = None  # Emotions from fig/ folder
    
    # Available Emotions (dynamically loaded from fig/ folder)
    available_emotions: List[str] = Field(default_factory=list)
    clothes: Optional[List[Dict[str, str]]] = None

    # Metadata
    resource_path: Optional[str] = None
    character_id: Optional[int] = None


class DialogueLine(BaseModel):
    """Single line of dialogue with emotion and metadata"""
    
    character: str
    emotion: str
    text: str
    action: str = ""
    text_jp: Optional[str] = None
    emotion_jp: Optional[str] = None
    timestamp: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "character": "Alice",
                "emotion": "平静",
                "text": "今天天气真好啊",
                "action": "",
                "text_jp": "今日はいい天気ですね",
            }
        }


class DialoguePlaybook(BaseModel):
    """Complete dialogue playbook"""
    
    header: Dict[str, Any]
    lines: List[DialogueLine]
    
    class Config:
        json_schema_extra = {
            "example": {
                "header": {
                    "characters": ["Alice", "Bob"],
                    "topic": "Weather",
                    "language": "zh",
                    "emotion_count": 18,
                },
                "lines": [
                    {
                        "character": "Alice",
                        "emotion": "平静",
                        "text": "今天天气真好",
                    }
                ]
            }
        }


# Standard emotions expanded to include more variations
STANDARD_EMOTIONS = [
    "慌张",
    "担心", 
    "尴尬",
    "紧张",
    "高兴",
    "自信",
    "害怕",
    "害羞",
    "认真",
    "生气",
    "无语",
    "厌恶",
    "疑惑",
    "难为情",
    "惊讶",
    "情动",
    "哭泣",
    "调皮",
    # Additional emotions for late-night chatting scenarios
    "温柔",  # Gentle/tender
    "期待",  # Expecting/looking forward to
    "开心",  # Happy/cheerful
    "平静",  # Calm/peaceful
    "困惑",  # Confused
    "失望",  # Disappointed
    "感动",  # Moved/touched
]
