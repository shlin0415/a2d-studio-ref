"""
Prompt Builder
Constructs LLM prompts with dialogue format rules
Supports dynamic language combinations: (zh, en, ja) x (zh, en, ja)
Based on LingChat's sys_prompt_builder logic
"""

import os
import logging
from typing import List, Dict, Optional, TYPE_CHECKING

from .core.models import CharacterSettings, STANDARD_EMOTIONS

if TYPE_CHECKING:
    from .topic_loader import TopicMetadata

logger = logging.getLogger(__name__)

# Language display names
LANG_NAMES = {
    "zh": "Chinese",
    "ja": "Japanese",
    "en": "English",
}

# Format examples for each language combination
LANG_EXAMPLES = {
    ("zh", "zh"): {
        "line1": "【期待】这么晚来找我，是有什么事情吗？（高兴地看着对方）",
        "line2": "【害羞】我...我有点睡不着呢（低下了头）",
    },
    ("zh", "ja"): {
        "line1": "【期待】这么晚来找我，是有什么事情吗？（高兴地看着对方）<こんな遅くに私を訪ねてくるなんて、何か用事があるの？>",
        "line2": "【害羞】我...我有点睡不着呢（低下了头）<私...ちょっと眠れないんです...>",
    },
    ("zh", "en"): {
        "line1": "【期待】这么晚来找我，是有什么事情吗？（高兴地看着对方）<Why are you coming to see me so late?>",
        "line2": "【害羞】我...我有点睡不着呢（低下了头）<I... I can't really fall asleep...>",
    },
    ("ja", "ja"): {
        "line1": "【嬉しい】こんな遅くに会いに来てくれたの？（嬉しそうに相手を見つめる）",
        "line2": "【恥ずかしい】私...ちょっと眠れないんです...（うつむく）",
    },
    ("ja", "zh"): {
        "line1": "【嬉しい】こんな遅くに会いに来てくれたの？（嬉しそうに相手を見つめる）<这么晚来找我吗？>",
        "line2": "【恥ずかしい】私...ちょっと眠れないんです...（うつむく）<我...有点睡不着...>",
    },
    ("ja", "en"): {
        "line1": "【嬉しい】こんな遅くに会いに来てくれたの？（嬉しそうに相手を見つめる）<You came to see me so late?>",
        "line2": "【恥ずかしい】私...ちょっと眠れないんです...（うつむく）<I... I can't really fall asleep...>",
    },
    ("en", "en"): {
        "line1": "【Happy】Why did you come to see me so late?（looks at the other happily）",
        "line2": "【Shy】I... I can't really fall asleep...（looks down）",
    },
    ("en", "zh"): {
        "line1": "【Happy】Why did you come to see me so late?（looks at the other happily）<这么晚来找我吗？>",
        "line2": "【Shy】I... I can't really fall asleep...（looks down）<我...有点睡不着...>",
    },
    ("en", "ja"): {
        "line1": "【Happy】Why did you come to see me so late?（looks at the other happily）<こんな遅くに会いに来てくれたの？>",
        "line2": "【Shy】I... I can't really fall asleep...（looks down）<私...ちょっと眠れないんです...>",
    },
}


class PromptBuilder:
    """Build LLM system prompts with dialogue format rules"""

    # Standard 18 emotions from LingChat
    EMOTIONS = STANDARD_EMOTIONS

    @staticmethod
    def build_system_prompt(
        user_name: str,
        characters: List[CharacterSettings],
        topic: str,
        dialogue_language: str = "zh",
        voice_language: str = "zh",
        enable_translation: bool = False,
        max_sentences_per_character: int = 5,
        # Backward compat
        language: Optional[str] = None,
    ) -> str:
        """
        Build system prompt for multi-character dialogue generation

        Args:
            user_name: Name of the user/player
            characters: List of characters participating
            topic: Context/topic for the dialogue
            dialogue_language: Language for caption/dialogue text (zh, en, ja)
            voice_language: Language for TTS voice text (zh, en, ja)
            enable_translation: Whether to enable translation (kept for compat)
            max_sentences_per_character: Max sentences per character turn
            language: Deprecated, use dialogue_language instead

        Returns:
            System prompt string
        """

        # Backward compat: if language is passed, use it as dialogue_language
        if language is not None:
            dialogue_language = language

        # Build character descriptions and get character names
        char_descriptions = []
        char_names = []
        for char in characters:
            char_descriptions.append(
                PromptBuilder._format_character_description(char, user_name)
            )
            char_names.append(char.character_key or char.ai_name)

        char_descriptions_str = "\n".join(char_descriptions)

        # Collect all available emotions from characters
        all_emotions = set()
        for char in characters:
            if char.available_emotions:
                all_emotions.update(char.available_emotions)

        # Build dialogue format instructions with language support
        dialogue_format = PromptBuilder._build_dialogue_format_instructions(
            dialogue_language=dialogue_language,
            voice_language=voice_language,
            max_sentences=max_sentences_per_character,
            valid_emotions=list(all_emotions) if all_emotions else None,
            character_names=char_names,
        )

        # Build conversation rules
        conversation_rules = PromptBuilder._build_conversation_rules(
            num_characters=len(characters),
            dialogue_language=dialogue_language,
            max_sentences=max_sentences_per_character,
            character_names=char_names,
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
    def build_system_prompt_from_metadata(
        user_name: str,
        characters: List[CharacterSettings],
        metadata: "TopicMetadata",
    ) -> str:
        """
        Build system prompt using TopicMetadata from SETTING file.

        This is the main method for the new pipeline. It:
        - Reads dialogue_language and voice_language from metadata
        - Adds topic-type-specific instructions (None/Learning/Fanfiction)
        - Includes DETAIL content when present
        - Allows flexible dialogue length

        Args:
            user_name: Name of the user/player
            characters: List of characters participating
            metadata: TopicMetadata from TopicLoader.load_topic()

        Returns:
            System prompt string
        """
        # Build character descriptions
        char_descriptions = []
        char_names = []
        for char in characters:
            char_descriptions.append(
                PromptBuilder._format_character_description(char, user_name)
            )
            char_names.append(char.character_key or char.ai_name)

        char_descriptions_str = "\n".join(char_descriptions)

        # Collect all available emotions
        all_emotions = set()
        for char in characters:
            if char.available_emotions:
                all_emotions.update(char.available_emotions)

        # Build dialogue format instructions
        dialogue_format = PromptBuilder._build_dialogue_format_instructions(
            dialogue_language=metadata.dialogue_language,
            voice_language=metadata.voice_language,
            max_sentences=5,
            valid_emotions=list(all_emotions) if all_emotions else None,
            character_names=char_names,
        )

        # Build conversation rules (flexible length)
        conversation_rules = PromptBuilder._build_flexible_conversation_rules(
            num_characters=len(characters),
            dialogue_language=metadata.dialogue_language,
            character_names=char_names,
        )

        # Build topic-type-specific instructions
        topic_type_instructions = PromptBuilder._build_topic_type_instructions(
            metadata=metadata,
        )

        # Build DETAIL content section (if present)
        detail_section = PromptBuilder._build_detail_section(metadata)

        # Build topic section
        extra_notes = ""
        if metadata.extra_setting:
            extra_notes = f"Additional setting notes:\n{metadata.extra_setting}"

        topic_section = f"""## Topic/Context
Title: {metadata.title}
Type: {metadata.topic_type}
Style: {metadata.style}
Time: {metadata.time}
Mood: {metadata.mood}
Context: {metadata.context}
Location: {metadata.location}
{metadata.description if metadata.description else ""}
{extra_notes}"""

        # Assemble complete system prompt
        system_prompt = f"""You are a professional dialogue writer creating natural, engaging conversations.

## Characters
{char_descriptions_str}

## Dialogue Format
{dialogue_format}

## Conversation Rules
{conversation_rules}
{topic_type_instructions}

{topic_section}
{detail_section}

Now, generate the dialogue. Remember to strictly follow the format rules."""

        return system_prompt

    @staticmethod
    def _build_topic_type_instructions(metadata: "TopicMetadata") -> str:
        """Build topic-type-specific instructions based on TOPIC_Type"""
        topic_type = metadata.topic_type.lower()

        if topic_type == "none" or topic_type == "":
            return ""

        instructions = "\n## Topic Type Instructions\n"

        if topic_type == "learning":
            instructions += f"""This is a LEARNING topic. Characters are studying/discussing material together.
- Discuss key concepts, insights, and difficulties from the material below
- Characters should express understanding, confusion, or breakthroughs naturally
- DO NOT read code or technical content verbatim for voice output
- You may reference function names, variable names, or key ideas briefly
- DETAIL_Follow={metadata.detail_follow}: Discuss with this level of depth
- DETAIL_Direct_Use_For_Voice={metadata.detail_direct_use_for_voice}: Keep direct quotes low for voice
"""
        elif topic_type == "fanfiction":
            instructions += f"""This is a FANFICTION topic. Characters are re-enacting a story.
- Follow the story in the DETAIL content below with {metadata.detail_follow}% similarity
- Characters should act out the scenes naturally as dialogue
- When the source has dialogue lines, you may copy them directly
- DETAIL_Direct_Use_For_Voice={metadata.detail_direct_use_for_voice}%: This controls how much source text goes directly into voice
- At high values (80-100), copy dialogue lines verbatim when possible
- At lower values, paraphrase while keeping the plot points
"""
        elif topic_type == "story":
            instructions += f"""This is a STORY topic. Characters discuss or react to a story.
- Use the story as loose inspiration ({metadata.detail_follow}% follow)
- Create original dialogue inspired by the mood and themes
- DETAIL_Direct_Use_For_Voice={metadata.detail_direct_use_for_voice}: Minimal direct quoting
"""
        elif topic_type == "asmr":
            instructions += f"""This is an ASMR topic. Soft, intimate delivery.
- Use gentle, whispered tone appropriate for ASMR
- Follow the DETAIL loosely ({metadata.detail_follow}%)
- DETAIL_Direct_Use_For_Voice={metadata.detail_direct_use_for_voice}: Minimal direct quoting
"""
        else:
            instructions += f"""Topic type: {metadata.topic_type}
- DETAIL_Follow={metadata.detail_follow}
- DETAIL_Direct_Use_For_Voice={metadata.detail_direct_use_for_voice}
"""

        return instructions

    @staticmethod
    def _build_detail_section(metadata: "TopicMetadata") -> str:
        """Build the DETAIL content section for the prompt"""
        if not metadata.detail_content:
            return ""

        # If stages exist and are relevant, include them
        if metadata.stages:
            # For staged content, include Stage_1 by default
            stage_content = metadata.stages.get("Stage_1", "")
            if stage_content:
                # Truncate if too long (keep within reasonable prompt size)
                if len(stage_content) > 4000:
                    stage_content = stage_content[:4000] + "\n... [content truncated]"
                return f"""
## DETAIL Content (Stage_1)
{stage_content}"""

        # No stages — include full DETAIL (truncated if needed)
        content = metadata.detail_content
        if len(content) > 4000:
            content = content[:4000] + "\n... [content truncated]"

        return f"""
## DETAIL Content
{content}"""

    @staticmethod
    def _build_flexible_conversation_rules(
        num_characters: int,
        dialogue_language: str = "zh",
        character_names: Optional[List[str]] = None,
    ) -> str:
        """Build conversation rules with flexible length (no hard max_sentences cap)"""
        char_list = ""
        if character_names:
            char_list = f"\nCharacters: {', '.join(character_names)}\n"

        caption_lang = LANG_NAMES.get(dialogue_language, "Chinese")

        rules = f"""1. Generate a natural dialogue with {num_characters} characters
{char_list}2. Characters alternate speaking turns naturally
3. Each character speaks multiple times
4. Each turn: keep it natural (1-3 sentences usually, but can be longer when appropriate)
5. Responses reflect character personality and the setting
6. Maintain conversation flow and emotional continuity
7. Use appropriate emotions for each statement
8. Actions should enhance the scene and feel natural
9. Dialogue should be engaging, warm, and natural
10. Let the dialogue length feel natural — not too short, not too long
11. CRITICAL: All dialogue text must be in {caption_lang}
12. Do not break the format 【emotion】text（action）under any circumstances
13. All emotions must be valid Chinese emotion names from the list"""

        return rules

    def _format_character_description(
        character: CharacterSettings, user_name: str
    ) -> str:
        """Format a single character description for the prompt"""

        base_desc = f"""### {character.ai_name}
User interacting with: {user_name}"""

        if character.ai_subtitle:
            base_desc += f"\nRole: {character.ai_subtitle}"

        if character.system_prompt:
            # Extract core personality/behavior from system prompt
            lines = character.system_prompt.split("\n")
            core_prompt = "\n".join(
                [
                    line
                    for line in lines
                    if not any(x in line for x in ["【", "】", "格式", "format"])
                ]
            )
            if core_prompt.strip():
                base_desc += f"\nCharacter Profile:\n{core_prompt.strip()}"

        return base_desc

    @staticmethod
    def _build_dialogue_format_instructions(
        dialogue_language: str = "zh",
        voice_language: str = "zh",
        max_sentences: int = 5,
        valid_emotions: Optional[List[str]] = None,
        character_names: Optional[List[str]] = None,
    ) -> str:
        """Build dialogue format instructions based on language combination"""

        # Use character-specific emotions if provided, otherwise use standard
        emotions = valid_emotions if valid_emotions else PromptBuilder.EMOTIONS
        emotions = sorted(emotions)

        caption_lang = LANG_NAMES.get(dialogue_language, "Chinese")
        voice_lang = LANG_NAMES.get(voice_language, "Chinese")

        # Determine format based on whether languages differ
        if dialogue_language == voice_language:
            # Same language: no translation needed
            format_base = f"""Each character's response must follow this STRICT format:
【emotion】{caption_lang} dialogue（action with CHARACTER NAMES）

### Example Format:
"""
        else:
            # Different languages: include translation
            format_base = f"""Each character's response must follow this STRICT format:
【emotion】{caption_lang} dialogue（action with CHARACTER NAMES）<{voice_lang} translation>

### Example Format:
"""

        # Get examples for this language combination
        examples = LANG_EXAMPLES.get(
            (dialogue_language, voice_language), LANG_EXAMPLES[("zh", "zh")]
        )
        format_base += f"{examples['line1']}\n{examples['line2']}\n"

        # Character names in actions
        format_base += "\n### Character Names in Actions\nWhen writing actions, use the actual character names:"

        if character_names and len(character_names) > 0:
            format_base += f"\n- Character 1: {character_names[0]}"
            if len(character_names) > 1:
                format_base += f"\n- Character 2: {character_names[1]}"
            if len(character_names) > 2:
                for i, name in enumerate(character_names[2:], 3):
                    format_base += f"\n- Character {i}: {name}"
            format_base += (
                "\n- DO NOT use generic terms like '对方', '他', '她' in actions"
            )

        # Constraints
        format_base += f"""

### Constraints:
- MUST use 【】 for emotions (NOT English brackets)
- Maximum {max_sentences} sentences per character turn
- Actions use （）and should be creative and descriptive
- Use specific character names in actions, not '对方'
- Each sentence must be complete and natural
- Dialogue language: {caption_lang}"""

        if dialogue_language != voice_language:
            format_base += f"\n- MUST include <{voice_lang}> translation for EACH line"

        format_base += f"""

### Valid Emotions ({len(emotions)} total - These are the ONLY emotions you can use)
{", ".join(emotions)}"""

        return format_base

    @staticmethod
    def _build_conversation_rules(
        num_characters: int,
        dialogue_language: str = "zh",
        max_sentences: int = 5,
        character_names: Optional[List[str]] = None,
    ) -> str:
        """Build conversation rules"""

        char_list = ""
        if character_names:
            char_list = f"\nCharacters: {', '.join(character_names)}\n"

        caption_lang = LANG_NAMES.get(dialogue_language, "Chinese")

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
11. CRITICAL: All dialogue text must be in {caption_lang}
12. Do not break the format 【emotion】text（action）under any circumstances
13. All emotions must be valid Chinese emotion names from the list"""

        return rules

    @staticmethod
    def build_single_character_prompt(
        user_name: str,
        character: CharacterSettings,
        topic: str,
        dialogue_language: str = "zh",
        voice_language: str = "zh",
        enable_translation: bool = False,
        dialogue_history: Optional[List[Dict]] = None,
        # Backward compat
        language: Optional[str] = None,
    ) -> str:
        """Build system prompt for single character dialogue"""

        if language is not None:
            dialogue_language = language

        return PromptBuilder.build_system_prompt(
            user_name=user_name,
            characters=[character],
            topic=topic,
            dialogue_language=dialogue_language,
            voice_language=voice_language,
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
