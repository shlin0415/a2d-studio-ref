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
        max_sentences_per_character: int = 5,
    ) -> str:
        """
        Build system prompt for multi-character dialogue generation
        
        Args:
            user_name: Name of the user/player
            characters: List of characters participating
            topic: Context/topic for the dialogue
            language: Target language (zh, en, jp)
            enable_translation: Whether to enable ZH->JP translation
            max_sentences_per_character: Max sentences per character turn
            
        Returns:
            System prompt string
        """
        
        # Build character descriptions and get character names
        char_descriptions = []
        char_names = []
        for char in characters:
            char_descriptions.append(PromptBuilder._format_character_description(char, user_name))
            char_names.append(char.character_key or char.ai_name)
        
        char_descriptions_str = "\n".join(char_descriptions)
        
        # Collect all available emotions from characters
        all_emotions = set()
        for char in characters:
            if char.available_emotions:
                all_emotions.update(char.available_emotions)
        
        # Build dialogue format instructions with character-specific emotions
        dialogue_format = PromptBuilder._build_dialogue_format_instructions(
            language=language,
            enable_translation=enable_translation,
            max_sentences=max_sentences_per_character,
            valid_emotions=list(all_emotions) if all_emotions else None,
            character_names=char_names
        )
        
        # Build conversation rules
        conversation_rules = PromptBuilder._build_conversation_rules(
            num_characters=len(characters),
            language=language,
            max_sentences=max_sentences_per_character,
            character_names=char_names
        )
        
        # Assemble complete system prompt
        system_prompt = f"""You are a professional dialogue writer creating natural, engaging conversations.

## Characters
{char_descriptions_str}

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
        enable_translation: bool = False,
        max_sentences: int = 5,
        valid_emotions: Optional[List[str]] = None,
        character_names: Optional[List[str]] = None
    ) -> str:
        """Build dialogue format instructions based on language"""
        
        # Use character-specific emotions if provided, otherwise use standard
        emotions = valid_emotions if valid_emotions else PromptBuilder.EMOTIONS
        emotions = sorted(emotions)
        
        # Default to Chinese + Japanese translation
        format_base = f"""Each character's response must follow this STRICT format:
【emotion】Chinese dialogue（action with CHARACTER NAMES）<Japanese translation>

### Example Format:
【期待】这么晚来找我，是有什么事情吗？（高兴地看着ema）<こんな遅くに私を訪ねてくるなんて、何か用事があるの？>
【害羞】我...我觉得有点不好意思呢（低下了头，走近hiro）<私は...ちょっと恥ずかしいです...>

### Character Names in Actions
When writing actions, use the actual character names:"""
        
        if character_names and len(character_names) > 0:
            format_base += f"\n- Character 1: {character_names[0]}"
            if len(character_names) > 1:
                format_base += f"\n- Character 2: {character_names[1]}"
            if len(character_names) > 2:
                for i, name in enumerate(character_names[2:], 3):
                    format_base += f"\n- Character {i}: {name}"
            format_base += "\n- DO NOT use generic terms like '对方', '他', '她' in actions"
        
        format_base += f"""

### Constraints:
- MUST use 【】 for emotions (NOT English)
- MUST include <> Japanese translation for EACH line
- Maximum {max_sentences} sentences per character turn
- Actions use （）and should be creative and descriptive
- Use specific character names in actions, not '对方'
- Each sentence must be complete and natural

### Valid Emotions ({len(emotions)} total - These are the ONLY emotions you can use)
{', '.join(emotions)}"""
        
        return format_base
    
    @staticmethod
    def _build_conversation_rules(
        num_characters: int,
        language: str = "zh",
        max_sentences: int = 5,
        character_names: Optional[List[str]] = None
    ) -> str:
        """Build conversation rules"""
        
        char_list = ""
        if character_names:
            char_list = f"\nCharacters: {', '.join(character_names)}\n"
        
        rules = f"""1. Generate a natural dialogue with {num_characters} characters
{char_list}2. Characters alternate speaking turns naturally
3. Each character speaks 2-3 times minimum
4. Each turn: {max_sentences} sentences maximum
5. Responses reflect character personality and the setting
6. Maintain conversation flow and emotional continuity
7. Use appropriate emotions for each statement
8. Actions should enhance the scene and feel natural
9. Dialogue should be engaging, warm, and natural
10. Total dialogue should be 300-500 words
11. CRITICAL: Do not break the format 【emotion】text（action）<Japanese> under any circumstances
12. All emotions must be valid Chinese emotion names from the list"""
        
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
