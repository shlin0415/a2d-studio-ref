"""
Main Dialogue Generator Orchestrator
Coordinates all components for dialogue generation
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

from .character_loader import CharacterLoader
from .prompt_builder import PromptBuilder
from .dialogue_parser import DialogueParser
from .output_generator import OutputGenerator
from .llm_service import LLMService
from .core.models import CharacterSettings, DialogueLine

logger = logging.getLogger(__name__)


class DialogueGenerator:
    """Main orchestrator for dialogue generation"""

    def __init__(
        self,
        llm_provider: str = "openai",
        llm_model: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
    ):
        """
        Initialize dialogue generator

        Args:
            llm_provider: LLM provider name
            llm_model: Model to use
            api_key: API key (defaults to env var)
        """
        self.character_loader = CharacterLoader()
        self.prompt_builder = PromptBuilder()
        self.dialogue_parser = DialogueParser()
        self.output_generator = OutputGenerator()
        self.llm_service = LLMService(
            provider=llm_provider,
            model=llm_model,
            api_key=api_key,
        )

    async def generate_multi_character_dialogue(
        self,
        character_paths: List[str | Path],
        topic: str,
        user_name: str = "player",
        dialogue_language: str = "zh",
        voice_language: str = "zh",
        enable_translation: bool = False,
        output_path: Optional[Path] = None,
        output_format: str = "jsonl",
        max_tokens: int = 1024,
        temperature: float = 0.7,
        # Backward compat
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate multi-character dialogue

        Args:
            character_paths: List of paths to character folders
            topic: Dialogue topic/context
            user_name: Name of user/player
            dialogue_language: Language for caption/dialogue text (zh, en, ja)
            voice_language: Language for TTS voice text (zh, en, ja)
            enable_translation: Whether to enable translation
            output_path: Path to save output
            output_format: Output format (jsonl, json, csv, txt)
            max_tokens: Max tokens for LLM
            temperature: LLM temperature
            language: Deprecated, use dialogue_language instead

        Returns:
            Dictionary with status and results
        """

        if language is not None:
            dialogue_language = language

        logger.info(
            f"Starting multi-character dialogue generation ({len(character_paths)} characters)"
        )

        # Step 1: Load characters
        characters = []
        for char_path in character_paths:
            char = self.character_loader.load_character(char_path)
            if char:
                characters.append(char)
            else:
                logger.warning(f"Failed to load character from: {char_path}")

        if not characters:
            return {
                "success": False,
                "error": "No valid characters loaded",
            }

        logger.info(
            f"Loaded {len(characters)} characters: {[c.ai_name for c in characters]}"
        )

        # Step 2: Build system prompt
        system_prompt = self.prompt_builder.build_system_prompt(
            user_name=user_name,
            characters=characters,
            topic=topic,
            dialogue_language=dialogue_language,
            voice_language=voice_language,
            enable_translation=enable_translation,
        )

        logger.debug(f"System prompt length: {len(system_prompt)} chars")

        # Step 3: Generate dialogue via LLM
        try:
            raw_dialogue = await self.llm_service.generate_dialogue(
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            logger.info(f"Generated raw dialogue: {len(raw_dialogue)} chars")
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
            }

        # Step 4: Parse dialogue
        char_names = [c.ai_name for c in characters]
        dialogue_lines = self.dialogue_parser.parse_multi_character_dialogue(
            raw_text=raw_dialogue,
            characters=char_names,
            valid_emotions=self.prompt_builder.get_emotion_list(),
        )

        logger.info(f"Parsed {len(dialogue_lines)} dialogue lines")

        # Step 5: Generate output
        if output_format == "jsonl":
            output = self.output_generator.generate_jsonl(
                dialogue_lines=dialogue_lines,
                characters=characters,
                topic=topic,
                dialogue_language=dialogue_language,
                voice_language=voice_language,
                output_path=output_path,
            )
        elif output_format == "json":
            output = self.output_generator.generate_json(
                dialogue_lines=dialogue_lines,
                characters=characters,
                topic=topic,
                dialogue_language=dialogue_language,
                voice_language=voice_language,
                output_path=output_path,
                pretty=True,
            )
        elif output_format == "csv":
            output = self.output_generator.generate_csv(
                dialogue_lines=dialogue_lines,
                output_path=output_path,
            )
        elif output_format == "txt":
            output = self.output_generator.generate_txt(
                dialogue_lines=dialogue_lines,
                output_path=output_path,
            )
        else:
            logger.warning(
                f"Unknown output format: {output_format}, defaulting to jsonl"
            )
            output = self.output_generator.generate_jsonl(
                dialogue_lines=dialogue_lines,
                characters=characters,
                topic=topic,
                dialogue_language=dialogue_language,
                voice_language=voice_language,
                output_path=output_path,
            )

        return {
            "success": True,
            "characters": char_names,
            "num_lines": len(dialogue_lines),
            "output_format": output_format,
            "output_path": str(output_path) if output_path else None,
            "dialogue_lines": dialogue_lines,
            "raw_output": output[:500] + "..." if len(output) > 500 else output,
        }

    async def generate_single_character_dialogue(
        self,
        character_path: str | Path,
        topic: str,
        user_name: str = "player",
        language: str = "zh",
        enable_translation: bool = False,
        output_path: Optional[Path] = None,
        output_format: str = "jsonl",
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Generate single character dialogue

        Args:
            character_path: Path to character folder
            topic: Dialogue topic
            user_name: User/player name
            language: Target language
            enable_translation: Whether to enable translation
            output_path: Path to save output
            output_format: Output format
            max_tokens: Max tokens for LLM
            temperature: LLM temperature

        Returns:
            Dictionary with status and results
        """

        logger.info(f"Starting single-character dialogue generation")

        # Load character
        character = self.character_loader.load_character(character_path)
        if not character:
            return {
                "success": False,
                "error": f"Failed to load character from: {character_path}",
            }

        logger.info(f"Loaded character: {character.ai_name}")

        # Generate (delegate to multi-character with single character)
        return await self.generate_multi_character_dialogue(
            character_paths=[character_path],
            topic=topic,
            user_name=user_name,
            language=language,
            enable_translation=enable_translation,
            output_path=output_path,
            output_format=output_format,
            max_tokens=max_tokens,
            temperature=temperature,
        )


async def main():
    """Example usage"""

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Initialize generator
    generator = DialogueGenerator(
        llm_provider="openai",
        llm_model="gpt-3.5-turbo",
    )

    # Example: Generate with character-fig-setting-example
    character_paths = [
        "Character-fig-setting-example/ema",
        "Character-fig-setting-example/hiro",
    ]

    topic = "Two friends meet in a coffee shop and discuss their weekend plans."

    result = await generator.generate_multi_character_dialogue(
        character_paths=character_paths,
        topic=topic,
        user_name="player",
        language="zh",
        output_format="jsonl",
        output_path=Path("output/dialogue.jsonl"),
    )

    print(f"\nGeneration result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
