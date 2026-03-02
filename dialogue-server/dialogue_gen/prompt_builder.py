"""
Prompt Builder
Constructs LLM prompts with dialogue format rules
Based on LingChat's sys_prompt_builder logic
"""

import os
import logging
from typing import List, Dict, Optional

from .core.models import CharacterSettings, STANDARD_EMOTIONS

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Build LLM system prompts with dialogue format rules"""
    
    # Standard 18 emotions from LingChat
    EMOTIONS = STANDARD_EMOTIONS
    
    @staticmethod
    def build_system_prompt(
        user_name: str,
        characters: List[CharacterSettings],
        topic: str,
        language: str = "zh",
        enable_translation: bool = False,
    ) -> str:
        """
        Build system prompt for multi-character dialogue generation
        
        Args:
            user_name: Name of the user/player
            characters: List of characters participating
            topic: Context/topic for the dialogue
            language: Target language (zh, en, jp)
            enable_translation: Whether to enable ZH->JP translation
            
        Returns:
            System prompt string
        """
        
        # Build character descriptions
        char_descriptions = "\n".join([
            PromptBuilder._format_character_description(char, user_name)
            for char in characters
        ])
        
        # Build dialogue format instructions
        dialogue_format = PromptBuilder._build_dialogue_format_instructions(
            language=language,
            enable_translation=enable_translation
        )
        
        # Build conversation rules
        conversation_rules = PromptBuilder._build_conversation_rules(
            num_characters=len(characters),
            language=language
        )
        
        # Assemble complete system prompt
        system_prompt = f"""You are a professional dialogue writer creating natural, engaging conversations.

## Characters
{char_descriptions}

## Dialogue Format
{dialogue_format}

## Conversation Rules
{conversation_rules}

## Topic/Context
{topic}

Now, generate the dialogue. Remember to strictly follow the format rules."""
        
        return system_prompt
    
    @staticmethod
    def _format_character_description(character: CharacterSettings, user_name: str) -> str:
        """Format a single character description for the prompt"""
        
        base_desc = f"""### {character.ai_name}
User interacting with: {user_name}"""
        
        if character.ai_subtitle:
            base_desc += f"\nRole: {character.ai_subtitle}"
        
        if character.system_prompt:
            # Extract core personality/behavior from system prompt
            # Skip dialogue format instructions
            lines = character.system_prompt.split('\n')
            core_prompt = '\n'.join([
                line for line in lines 
                if not any(x in line for x in ['【', '】', '格式', 'format'])
            ])
            if core_prompt.strip():
                base_desc += f"\nCharacter Profile:\n{core_prompt.strip()}"
        
        return base_desc
    
    @staticmethod
    def _build_dialogue_format_instructions(
        language: str = "zh",
        enable_translation: bool = False
    ) -> str:
        """Build dialogue format instructions based on language"""
        
        format_base = f"""Each character's response must follow this strict format:
【emotion】dialogue text（optional actions）"""
        
        if enable_translation and language != "zh":
            format_base += """<translation>"""
        
        format_base += f"""

### Valid Emotions ({len(PromptBuilder.EMOTIONS)} total)
{', '.join(PromptBuilder.EMOTIONS)}

### Format Rules
- Emotion tags must be enclosed in 【】
- No emoticons (颜文字) allowed
- Actions are optional, enclosed in （）
- Each sentence must be complete (no connecting with ~)
- One character speaks per turn"""
        
        if enable_translation and language == "jp":
            format_base += "\n- Include Japanese translation in <> after each sentence"
        elif enable_translation and language == "en":
            format_base += "\n- Include English translation in <> after each sentence"
        
        format_base += """

### Example Format
【高兴】今天天气真好呀！<Today's weather is wonderful!>
【害羞】我...我觉得有点不好意思呢（低下了头）<I... feel a bit embarrassed...>"""
        
        return format_base
    
    @staticmethod
    def _build_conversation_rules(
        num_characters: int,
        language: str = "zh"
    ) -> str:
        """Build conversation rules"""
        
        rules = f"""1. Generate a natural dialogue with {num_characters} characters
2. Each character should speak 2-3 times minimum
3. Responses should reflect character personality
4. Maintain conversation flow and context
5. Use appropriate emotions for each statement
6. Actions should enhance the scene (optional)
7. Dialogue should be engaging and natural
8. Total dialogue should be between 300-500 words
9. Each turn must use valid emotions from the emotion list
10. Do not break the dialogue format under any circumstances"""
        
        return rules
    
    @staticmethod
    def build_single_character_prompt(
        user_name: str,
        character: CharacterSettings,
        topic: str,
        language: str = "zh",
        enable_translation: bool = False,
        dialogue_history: Optional[List[Dict]] = None,
    ) -> str:
        """
        Build system prompt for single character dialogue
        
        Args:
            user_name: Name of the user
            character: Character for dialogue
            topic: Conversation topic/context
            language: Target language
            enable_translation: Whether to enable translation
            dialogue_history: Previous dialogue lines (for context)
            
        Returns:
            System prompt string
        """
        return PromptBuilder.build_system_prompt(
            user_name=user_name,
            characters=[character],
            topic=topic,
            language=language,
            enable_translation=enable_translation,
        )
    
    @staticmethod
    def get_emotion_list() -> List[str]:
        """Get the standard emotion list"""
        return PromptBuilder.EMOTIONS.copy()
    
    @staticmethod
    def validate_emotion(emotion: str) -> bool:
        """Check if emotion is in standard list"""
        return emotion in PromptBuilder.EMOTIONS
