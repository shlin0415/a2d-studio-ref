"""
Topic Loader
Reads topic descriptions and metadata from SETTING-*.md files
Parses new format with |====Start of ...====| markers
"""

import logging
import re
from pathlib import Path
from typing import Dict, Optional, Any, List

logger = logging.getLogger(__name__)


class TopicMetadata:
    """Metadata extracted from SETTING-*.md file"""

    def __init__(self):
        self.title: str = "Dialogue"
        self.topic_type: str = "None"  # None, Learning, Story, Fanfiction, ASMR
        self.description: str = ""

        # Setting fields
        self.style: str = "sfw"
        self.time: str = "Multiple times"
        self.mood: str = "Multiple reasonable mood"
        self.context: str = "Characters are spending time together"
        self.location: str = "Multiple places"

        # Language fields
        self.dialogue_language: str = "zh"
        self.voice_language: str = "zh"

        # DETAIL fields
        self.detail_follow: int = 80
        self.detail_direct_use_for_voice: int = 0
        self.detail_file: Optional[str] = None
        self.detail_content: str = ""  # Full DETAIL file content
        self.stages: Dict[str, str] = {}  # Stage name -> content (if staged)

        # Extra setting content (after ------)
        self.extra_setting: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "title": self.title,
            "topic_type": self.topic_type,
            "style": self.style,
            "time": self.time,
            "mood": self.mood,
            "context": self.context,
            "location": self.location,
            "dialogue_language": self.dialogue_language,
            "voice_language": self.voice_language,
            "detail_follow": self.detail_follow,
            "detail_direct_use_for_voice": self.detail_direct_use_for_voice,
            "detail_file": self.detail_file,
            "detail_content_length": len(self.detail_content),
            "stage_names": list(self.stages.keys()),
        }


class TopicLoader:
    """Load and parse topic metadata from SETTING-*.md files in new format"""

    # Section markers
    SECTION_START = re.compile(r"\|====Start of (.+?)====\|")
    SECTION_END = re.compile(r"\|====End of (.+?)====\|")

    # Field patterns: Field='value' or Field=value
    STRING_FIELD = re.compile(r"^(\w+)\s*=\s*'([^']*)'")
    INT_FIELD = re.compile(r"^(\w+)\s*=\s*(\d+)")

    @staticmethod
    def load_topic(topic_path: Path | str) -> tuple[str, TopicMetadata]:
        """
        Load topic from SETTING-*.md file in new format

        Args:
            topic_path: Path to SETTING-*.md file

        Returns:
            Tuple of (full_topic_text, metadata)
        """
        topic_path = Path(topic_path)
        metadata = TopicMetadata()

        if not topic_path.exists():
            logger.warning(f"Topic file not found: {topic_path}")
            return "", metadata

        try:
            with open(topic_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract title (first # line)
            title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
            if title_match:
                metadata.title = title_match.group(1).strip()

            # Parse sections
            sections = TopicLoader._parse_sections(content)

            # Parse Topic Description section
            if "Topic Description" in sections:
                TopicLoader._parse_topic_description(
                    sections["Topic Description"], metadata
                )

            # Parse Setting section
            if "Setting" in sections:
                TopicLoader._parse_setting_section(sections["Setting"], metadata)

            # Parse Detail section
            if "Detail" in sections:
                TopicLoader._parse_detail_section(sections["Detail"], metadata)
                TopicLoader._load_detail_file(metadata, topic_path.parent)

            logger.info(f"Loaded topic: {metadata.title}")
            logger.info(f"  Type: {metadata.topic_type}")
            logger.info(
                f"  Languages: {metadata.dialogue_language} -> {metadata.voice_language}"
            )
            logger.info(
                f"  DETAIL: Follow={metadata.detail_follow}, DirectUse={metadata.detail_direct_use_for_voice}"
            )

            return content, metadata

        except Exception as e:
            logger.error(f"Error loading topic: {e}")
            import traceback

            traceback.print_exc()
            return "", metadata

    @staticmethod
    def _parse_sections(content: str) -> Dict[str, str]:
        """Parse content into sections delimited by |====Start/End of ...====|"""
        sections = {}
        lines = content.split("\n")
        current_section = None
        current_content = []

        for line in lines:
            start_match = TopicLoader.SECTION_START.match(line.strip())
            end_match = TopicLoader.SECTION_END.match(line.strip())

            if start_match:
                current_section = start_match.group(1)
                current_content = []
            elif end_match:
                if current_section:
                    sections[current_section] = "\n".join(current_content)
                    current_section = None
                    current_content = []
            elif current_section is not None:
                current_content.append(line)

        return sections

    @staticmethod
    def _parse_topic_description(section_content: str, metadata: TopicMetadata):
        """Parse Topic Description section for TOPIC_Type and description"""
        for line in section_content.split("\n"):
            line = line.strip()
            if not line or line.startswith("------"):
                continue

            # Check for TOPIC_Type
            match = TopicLoader.STRING_FIELD.match(line)
            if match and match.group(1) == "TOPIC_Type":
                metadata.topic_type = match.group(2)
                continue

            # Non-field lines are description
            if not TopicLoader.STRING_FIELD.match(
                line
            ) and not TopicLoader.INT_FIELD.match(line):
                if line and not line.startswith("//"):
                    if metadata.description:
                        metadata.description += " " + line
                    else:
                        metadata.description = line

    @staticmethod
    def _parse_setting_section(section_content: str, metadata: TopicMetadata):
        """Parse Setting section for all fields"""
        before_divider = True

        for line in section_content.split("\n"):
            line = line.strip()
            if not line:
                continue

            if line.startswith("------"):
                before_divider = False
                continue

            # Try string field: Field='value'
            str_match = TopicLoader.STRING_FIELD.match(line)
            if str_match:
                key = str_match.group(1)
                value = str_match.group(2)

                field_map = {
                    "Style": "style",
                    "Time": "time",
                    "Mood": "mood",
                    "Context": "context",
                    "Location": "location",
                    "Dialogue_Language": "dialogue_language",
                    "Voice_Language": "voice_language",
                }

                if key in field_map:
                    setattr(metadata, field_map[key], value)
                continue

            # Try int field: Field=value
            int_match = TopicLoader.INT_FIELD.match(line)
            if int_match:
                key = int_match.group(1)
                value = int_match.group(2)

                int_field_map = {
                    "DETAIL_Follow": "detail_follow",
                    "DETAIL_Direct_Use_For_Voice": "detail_direct_use_for_voice",
                }

                if key in int_field_map:
                    setattr(metadata, int_field_map[key], int(value))
                continue

            # After divider, collect extra content
            if not before_divider and line and not line.startswith("//"):
                if metadata.extra_setting:
                    metadata.extra_setting += "\n" + line
                else:
                    metadata.extra_setting = line

    @staticmethod
    def _parse_detail_section(section_content: str, metadata: TopicMetadata):
        """Parse Detail section for DETAIL_File"""
        for line in section_content.split("\n"):
            line = line.strip()
            match = TopicLoader.STRING_FIELD.match(line)
            if match and match.group(1) == "DETAIL_File":
                metadata.detail_file = match.group(2)
                break

    @staticmethod
    def _load_detail_file(metadata: TopicMetadata, topic_dir: Path):
        """Load DETAIL file content and parse stages if present"""
        if metadata.detail_file:
            detail_path = topic_dir / metadata.detail_file
            if detail_path.exists():
                try:
                    with open(detail_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    metadata.detail_content = content
                    # Parse stages if present
                    metadata.stages = TopicLoader._parse_stages(content)
                    if metadata.stages:
                        logger.info(
                            f"  DETAIL file loaded with {len(metadata.stages)} stages: {detail_path}"
                        )
                    else:
                        logger.info(f"  DETAIL file loaded (no stages): {detail_path}")
                except Exception as e:
                    logger.error(f"  Error reading DETAIL file: {e}")
            else:
                logger.warning(f"  DETAIL file not found: {detail_path}")

    @staticmethod
    def _parse_stages(content: str) -> Dict[str, str]:
        """Parse stage markers from DETAIL content.

        Stage markers: |<===Start of Stage_N===>| ... |<===End of Stage_N==>|
        Returns dict of stage_name -> stage_content.
        """
        stages = {}
        stage_pattern = re.compile(
            r"\|<===Start of (Stage_\d+)===>\|(.*?)\|<===End of \1===>\|",
            re.DOTALL,
        )
        for match in stage_pattern.finditer(content):
            stage_name = match.group(1)
            stage_content = match.group(2).strip()
            stages[stage_name] = stage_content
        return stages
