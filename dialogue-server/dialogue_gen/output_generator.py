"""
Output Generator
Generates JSONL playbook output from parsed dialogue
Supports caption_text/voice_text with language fields
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

from .core.models import DialogueLine, DialoguePlaybook, CharacterSettings

logger = logging.getLogger(__name__)


class OutputGenerator:
    """Generate structured dialogue output in JSONL format"""

    @staticmethod
    def generate_jsonl(
        dialogue_lines: List[DialogueLine],
        characters: List[CharacterSettings],
        topic: str,
        dialogue_language: str = "zh",
        voice_language: str = "zh",
        output_path: Optional[Path] = None,
        # Backward compat
        language: Optional[str] = None,
    ) -> str:
        """
        Generate JSONL output from dialogue lines

        Args:
            dialogue_lines: List of DialogueLine objects
            characters: List of CharacterSettings
            topic: Dialogue topic
            dialogue_language: Language for caption text
            voice_language: Language for voice/TTS text
            output_path: Optional file path to write output
            language: Deprecated, use dialogue_language instead

        Returns:
            JSONL string (newline-separated JSON objects)
        """

        if language is not None:
            dialogue_language = language

        # Build header
        header = OutputGenerator._build_header(
            characters=characters,
            topic=topic,
            dialogue_language=dialogue_language,
            voice_language=voice_language,
            num_lines=len(dialogue_lines),
        )

        # Build output lines
        jsonl_lines = [json.dumps(header, ensure_ascii=False)]

        for idx, line in enumerate(dialogue_lines):
            line_dict = OutputGenerator._dialogue_line_to_dict(
                line,
                idx,
                dialogue_language=dialogue_language,
                voice_language=voice_language,
            )
            jsonl_lines.append(json.dumps(line_dict, ensure_ascii=False))

        jsonl_output = "\n".join(jsonl_lines)

        # Write to file if path provided
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(jsonl_output)
            logger.info(f"Wrote output to: {output_path}")

        return jsonl_output

    @staticmethod
    def _build_header(
        characters: List[CharacterSettings],
        topic: str,
        dialogue_language: str = "zh",
        voice_language: str = "zh",
        num_lines: int = 0,
    ) -> Dict[str, Any]:
        """Build JSONL header with metadata"""

        # Use character_key if available, otherwise fall back to ai_name
        char_names = [(char.character_key or char.ai_name) for char in characters]

        return {
            "header": {
                "characters": char_names,
                "character_count": len(characters),
                "topic": topic,
                "dialogue_language": dialogue_language,
                "voice_language": voice_language,
                "emotion_count": 18,
                "line_count": num_lines,
                "timestamp": datetime.now().isoformat(),
                "format_version": "2.0",
                "format_description": "Multi-character dialogue with caption/voice language support",
            }
        }

    @staticmethod
    def _dialogue_line_to_dict(
        line: DialogueLine,
        index: int,
        dialogue_language: str = "zh",
        voice_language: str = "zh",
    ) -> Dict[str, Any]:
        """Convert DialogueLine to dictionary for JSON serialization"""

        # Determine caption_text and voice_text
        caption_text = line.text  # Primary text is always caption

        if dialogue_language == voice_language:
            # Same language: voice_text = caption_text
            voice_text = line.text
        else:
            # Different languages: voice_text = translation (text_jp or explicit)
            voice_text = line.text_jp if line.text_jp else line.text

        result = {
            "index": index,
            "character": line.character,
            "emotion": line.emotion,
            "text": line.text,
            "action": line.action,
            "text_jp": line.text_jp,
            "caption_text": caption_text,
            "voice_text": voice_text,
            "caption_language": dialogue_language,
            "voice_language": voice_language,
            "emotion_jp": line.emotion_jp,
            "timestamp": line.timestamp,
        }

        return result

    @staticmethod
    def generate_json(
        dialogue_lines: List[DialogueLine],
        characters: List[CharacterSettings],
        topic: str,
        dialogue_language: str = "zh",
        voice_language: str = "zh",
        output_path: Optional[Path] = None,
        pretty: bool = True,
        language: Optional[str] = None,
    ) -> str:
        """Generate single JSON output (alternative to JSONL)"""

        if language is not None:
            dialogue_language = language

        header = OutputGenerator._build_header(
            characters=characters,
            topic=topic,
            dialogue_language=dialogue_language,
            voice_language=voice_language,
            num_lines=len(dialogue_lines),
        )

        lines_list = [
            OutputGenerator._dialogue_line_to_dict(
                line,
                idx,
                dialogue_language=dialogue_language,
                voice_language=voice_language,
            )
            for idx, line in enumerate(dialogue_lines)
        ]

        playbook_dict = {
            **header,
            "lines": lines_list,
        }

        if pretty:
            json_output = json.dumps(playbook_dict, ensure_ascii=False, indent=2)
        else:
            json_output = json.dumps(playbook_dict, ensure_ascii=False)

        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(json_output)
            logger.info(f"Wrote JSON output to: {output_path}")

        return json_output

    @staticmethod
    def generate_csv(
        dialogue_lines: List[DialogueLine],
        output_path: Optional[Path] = None,
    ) -> str:
        """Generate CSV output for spreadsheet applications"""
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                "Character",
                "Emotion",
                "Dialogue",
                "Action",
                "Translation",
                "Emotion (JP)",
            ]
        )

        for line in dialogue_lines:
            writer.writerow(
                [
                    line.character,
                    line.emotion,
                    line.text,
                    line.action,
                    line.text_jp or "",
                    line.emotion_jp or "",
                ]
            )

        csv_output = output.getvalue()

        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8", newline="") as f:
                f.write(csv_output)
            logger.info(f"Wrote CSV to: {output_path}")

        return csv_output

    @staticmethod
    def generate_txt(
        dialogue_lines: List[DialogueLine],
        output_path: Optional[Path] = None,
    ) -> str:
        """Generate human-readable TXT output"""

        lines = []

        for line in dialogue_lines:
            line_text = f"{line.character}: 【{line.emotion}】{line.text}"

            if line.action:
                line_text += f"（{line.action}）"

            if line.text_jp:
                line_text += f"\n  -> {line.text_jp}"

            lines.append(line_text)

        txt_output = "\n\n".join(lines)

        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(txt_output)
            logger.info(f"Wrote TXT to: {output_path}")

        return txt_output
