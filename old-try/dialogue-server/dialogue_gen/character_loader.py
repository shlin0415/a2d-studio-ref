"""
Character Loader
Reads character configuration from setting.txt files
Based on LingChat's Function.load_character_settings and parse_enhanced_txt
"""

import re
import ast
from pathlib import Path
from typing import Dict, Optional, List
import yaml
import logging

from .core.models import CharacterSettings

logger = logging.getLogger(__name__)


class CharacterLoader:
    """Load and validate character settings from folder structure"""
    
    # Fields that should be None if empty in settings file
    HIDE_NONE_FIELDS = {
        "system_prompt_example",
        "system_prompt_example_old",
        "ai_subtitle",
        "user_subtitle",
    }
    
    @staticmethod
    def load_character(character_path: str | Path, character_key: Optional[str] = None) -> Optional[CharacterSettings]:
        """
        Load character from folder containing setting.txt
        
        Args:
            character_path: Path to character folder (e.g., Character-fig-setting-example/ema/)
            character_key: Optional identifier for character (e.g., 'ema', 'hiro'). Defaults to folder name.
            
        Returns:
            CharacterSettings object or None if loading fails
        """
        character_path = Path(character_path)
        
        # Auto-detect character_key from folder name if not provided
        if not character_key:
            character_key = character_path.name
        
        if not character_path.exists() or not character_path.is_dir():
            logger.error(f"Character path does not exist: {character_path}")
            return None
        
        # Try multiple setting file names
        setting_files = [
            character_path / "setting.txt",
            character_path / "setting-calm-version.txt",
            character_path / "setting-straightforward-version.txt",
        ]
        
        settings_dict = None
        for setting_file in setting_files:
            if setting_file.exists():
                try:
                    settings_dict = CharacterLoader.parse_enhanced_txt(setting_file)
                    logger.info(f"Loaded character settings from: {setting_file}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to parse {setting_file}: {e}")
                    continue
        
        if not settings_dict:
            logger.error(f"No valid setting file found in {character_path}")
            return None
        
        # Set character key and resource path
        settings_dict["character_key"] = character_key
        settings_dict["resource_path"] = str(character_path)
        
        # Load available emotions from fig/ folder
        emotion_figures = CharacterLoader.get_emotion_figures(character_path)
        settings_dict["available_emotions"] = sorted(list(emotion_figures.keys()))
        
        logger.info(f"Found {len(emotion_figures)} emotions: {', '.join(settings_dict['available_emotions'][:5])}...")
        
        # Try to create CharacterSettings object
        try:
            settings = CharacterSettings(**settings_dict)
            logger.info(f"Successfully loaded character: {settings.ai_name}")
            return settings
        except Exception as e:
            logger.error(f"Failed to create CharacterSettings: {e}")
            return None
    
    @staticmethod
    def parse_enhanced_txt(file_path: Path) -> Dict[str, any]:
        """
        Parse setting.txt file with support for multiple formats
        Based on LingChat's parse_enhanced_txt
        
        Supports:
        - Single line values: key = value
        - Quoted values: key = "value"
        - Multiline strings: key = \"\"\"value\"\"\"
        - Dictionary values: key = {dict_content}
        
        Args:
            file_path: Path to setting.txt file
            
        Returns:
            Dictionary of parsed settings
        """
        settings = {}
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Try YAML parsing first (most common format)
        try:
            yaml_data = yaml.safe_load(content)
            if isinstance(yaml_data, dict):
                settings.update(yaml_data)
                logger.debug(f"Successfully parsed {file_path.name} as YAML")
                return settings
        except yaml.YAMLError as e:
            logger.debug(f"YAML parsing failed for {file_path.name}: {e}, trying regex parsing")
        
        # Fallback to regex-based parsing (for custom formats)
        # Handle multiline strings: key = """value"""
        multi_line_pattern = re.compile(r'^(\w+)\s*=\s*"""(.*?)"""\s*$', re.MULTILINE | re.DOTALL)
        for match in multi_line_pattern.finditer(content):
            key = match.group(1)
            value = match.group(2).strip()
            settings[key] = value
        
        # Handle dictionary values: key = {...}
        dict_pattern = re.compile(r'^(\w+)\s*=\s*({.*?})\s*$', re.MULTILINE | re.DOTALL)
        for match in dict_pattern.finditer(content):
            key = match.group(1)
            if key not in settings:
                value = match.group(2).strip()
                try:
                    settings[key] = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    settings[key] = value
        
        # Handle single line values: key = value
        single_line_pattern = re.compile(r'^(\w+)\s*=\s*(.*?)\s*$', re.MULTILINE)
        for match in single_line_pattern.finditer(content):
            key = match.group(1)
            if key not in settings:
                value = match.group(2).strip()
                
                # Remove quotes if present
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                
                # Convert empty string to None for specific fields
                if value == '' and key in CharacterLoader.HIDE_NONE_FIELDS:
                    value = None
                
                settings[key] = value
        
        return settings
    
    @staticmethod
    def get_emotion_figures(character_path: str | Path) -> Dict[str, Path]:
        """
        Discover emotion figure files in character folder
        
        Args:
            character_path: Path to character folder
            
        Returns:
            Dictionary mapping emotion names to image file paths
        """
        character_path = Path(character_path)
        fig_path = character_path / "fig"
        
        emotion_figures = {}
        
        if not fig_path.exists():
            logger.warning(f"Figure folder not found: {fig_path}")
            return emotion_figures
        
        # Find all image files (PNG, JPG)
        for img_file in fig_path.glob("*.png"):
            emotion_name = img_file.stem  # Filename without extension
            emotion_figures[emotion_name] = img_file
            logger.debug(f"Found emotion figure: {emotion_name} -> {img_file.name}")
        
        for img_file in fig_path.glob("*.jpg"):
            emotion_name = img_file.stem
            emotion_figures[emotion_name] = img_file
        
        for img_file in fig_path.glob("*.jpeg"):
            emotion_name = img_file.stem
            emotion_figures[emotion_name] = img_file
        
        return emotion_figures
    
    @staticmethod
    def validate_character_emotions(
        character: CharacterSettings,
        character_path: str | Path
    ) -> bool:
        """
        Validate that character's emotions have corresponding figure files
        
        Args:
            character: CharacterSettings object
            character_path: Path to character folder
            
        Returns:
            True if all emotions have figures, False otherwise
        """
        emotion_figures = CharacterLoader.get_emotion_figures(character_path)
        
        # If system_prompt mentions emotions, validate them
        if character.system_prompt:
            # Extract emotion names from system prompt
            # Looking for 【emotion】 patterns
            emotion_pattern = re.compile(r'【([^】]+)】')
            mentioned_emotions = set(emotion_pattern.findall(character.system_prompt))
            
            missing_emotions = []
            for emotion in mentioned_emotions:
                if emotion not in emotion_figures:
                    missing_emotions.append(emotion)
            
            if missing_emotions:
                logger.warning(
                    f"Character {character.ai_name} has emotions without figures: "
                    f"{', '.join(missing_emotions)}"
                )
                return False
        
        logger.info(f"Character {character.ai_name} validated successfully")
        return True
