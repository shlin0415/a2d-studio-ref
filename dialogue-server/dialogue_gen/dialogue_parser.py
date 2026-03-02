"""
Dialogue Parser
Parses LLM-generated dialogue with emotion tags and actions
Based on LingChat's emotion parsing logic
"""

import re
import logging
from typing import Dict, List, Optional, Tuple

from .core.models import DialogueLine, STANDARD_EMOTIONS

logger = logging.getLogger(__name__)


class DialogueParser:
    """Parse dialogue with 【emotion】text（actions）<translation> format"""
    
    # Regex patterns
    EMOTION_PATTERN = re.compile(r'【([^】]+)】')
    ACTION_PATTERN = re.compile(r'（([^）]+)）')
    TRANSLATION_PATTERN = re.compile(r'<([^>]+)>')
    LINE_SPLITTER = re.compile(r'(?:【[^】]+】[^【]*?)(?=【|$)')
    
    @staticmethod
    def parse_raw_response(
        raw_text: str,
        character_name: str,
        valid_emotions: Optional[List[str]] = None,
    ) -> List[DialogueLine]:
        """
        Parse raw LLM response into structured dialogue lines
        
        Args:
            raw_text: Raw text from LLM with emotion tags
            character_name: Name of character speaking
            valid_emotions: List of valid emotions (uses standard 18 if None)
            
        Returns:
            List of DialogueLine objects
        """
        if not valid_emotions:
            valid_emotions = STANDARD_EMOTIONS
        
        lines = []
        
        # Split into individual dialogue units
        dialogue_units = DialogueParser._split_dialogue_units(raw_text)
        
        for unit in dialogue_units:
            try:
                line = DialogueParser.parse_dialogue_unit(
                    unit,
                    character_name=character_name,
                    valid_emotions=valid_emotions,
                )
                if line:
                    lines.append(line)
            except Exception as e:
                logger.warning(f"Failed to parse dialogue unit: {unit[:50]}... Error: {e}")
                continue
        
        return lines
    
    @staticmethod
    def parse_dialogue_unit(
        text: str,
        character_name: str,
        valid_emotions: Optional[List[str]] = None,
    ) -> Optional[DialogueLine]:
        """
        Parse a single dialogue unit with emotion tag
        
        Args:
            text: Single dialogue unit (e.g., "【高兴】你好！<Hello!>（挥手）")
            character_name: Character name
            valid_emotions: List of valid emotions
            
        Returns:
            DialogueLine object or None if parsing fails
        """
        if not valid_emotions:
            valid_emotions = STANDARD_EMOTIONS
        
        text = text.strip()
        if not text:
            return None
        
        # Extract emotion
        emotion_match = DialogueParser.EMOTION_PATTERN.search(text)
        if not emotion_match:
            logger.debug(f"No emotion tag found in: {text[:50]}")
            return None
        
        emotion = emotion_match.group(1).strip()
        
        # Validate emotion
        if emotion not in valid_emotions:
            logger.warning(f"Invalid emotion '{emotion}' not in valid emotions")
            # Still parse it, but mark as invalid
        
        # Remove emotion tag from text
        remaining_text = text[emotion_match.end():]
        
        # Extract translation (if present)
        translation_match = DialogueParser.TRANSLATION_PATTERN.search(remaining_text)
        translation = None
        if translation_match:
            translation = translation_match.group(1).strip()
            remaining_text = remaining_text[:translation_match.start()] + remaining_text[translation_match.end():]
        
        # Extract action (if present)
        action_match = DialogueParser.ACTION_PATTERN.search(remaining_text)
        action = ""
        if action_match:
            action = action_match.group(1).strip()
            remaining_text = remaining_text[:action_match.start()] + remaining_text[action_match.end():]
        
        # What's left is the dialogue text
        dialogue_text = remaining_text.strip()
        
        if not dialogue_text:
            logger.warning(f"No dialogue text found in unit: {text}")
            return None
        
        return DialogueLine(
            character=character_name,
            emotion=emotion,
            text=dialogue_text,
            action=action,
            text_jp=translation if translation else None,
        )
    
    @staticmethod
    def _split_dialogue_units(text: str) -> List[str]:
        """
        Split raw text into individual dialogue units
        Each unit should start with 【emotion】
        
        Args:
            text: Raw text with multiple dialogue units
            
        Returns:
            List of dialogue unit strings
        """
        # Find all emotion tag positions
        units = []
        current_pos = 0
        
        for match in DialogueParser.EMOTION_PATTERN.finditer(text):
            if match.start() > current_pos:
                # Add any text before this emotion as a separate unit
                prev_unit = text[current_pos:match.start()].strip()
                if prev_unit:
                    units.append(prev_unit)
            
            # Find the next emotion tag or end of text
            next_emotion = DialogueParser.EMOTION_PATTERN.search(text, match.end())
            if next_emotion:
                unit = text[match.start():next_emotion.start()]
                units.append(unit.strip())
                current_pos = next_emotion.start()
            else:
                # Last unit
                unit = text[match.start():]
                units.append(unit.strip())
                break
        
        # Filter empty units
        return [u for u in units if u]
    
    @staticmethod
    def parse_multi_character_dialogue(
        raw_text: str,
        characters: List[str],
        valid_emotions: Optional[List[str]] = None,
    ) -> List[DialogueLine]:
        """
        Parse multi-character dialogue
        Attempts to identify which character is speaking based on context
        
        Args:
            raw_text: Raw text with dialogue
            characters: List of character names
            valid_emotions: List of valid emotions
            
        Returns:
            List of DialogueLine objects
        """
        if not valid_emotions:
            valid_emotions = STANDARD_EMOTIONS
        
        lines = []
        
        # Split by emotion tags and try to assign speakers
        dialogue_units = DialogueParser._split_dialogue_units(raw_text)
        
        current_character_idx = 0
        
        for unit in dialogue_units:
            try:
                # Determine which character is speaking (round-robin)
                current_char = characters[current_character_idx % len(characters)]
                
                line = DialogueParser.parse_dialogue_unit(
                    unit,
                    character_name=current_char,
                    valid_emotions=valid_emotions,
                )
                
                if line:
                    lines.append(line)
                    current_character_idx += 1
                    
            except Exception as e:
                logger.warning(f"Failed to parse unit: {e}")
                continue
        
        return lines
    
    @staticmethod
    def validate_dialogue_format(dialogue_line: DialogueLine) -> Tuple[bool, str]:
        """
        Validate dialogue line format
        
        Args:
            dialogue_line: DialogueLine to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check emotion
        if not dialogue_line.emotion:
            return False, "Missing emotion tag"
        
        if dialogue_line.emotion not in STANDARD_EMOTIONS:
            return False, f"Invalid emotion: {dialogue_line.emotion}"
        
        # Check dialogue text
        if not dialogue_line.text:
            return False, "Missing dialogue text"
        
        # Check for emoticons (heuristic)
        emoticon_pattern = re.compile(r'[^\w\s\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff，。！？（）\(\)<>\-]')
        if emoticon_pattern.search(dialogue_line.text):
            return False, "Contains emoticons or invalid characters"
        
        return True, ""
    
    @staticmethod
    def extract_emotions(text: str) -> List[str]:
        """Extract all emotion tags from text"""
        matches = DialogueParser.EMOTION_PATTERN.findall(text)
        return list(set(matches))  # Remove duplicates
    
    @staticmethod
    def extract_actions(text: str) -> List[str]:
        """Extract all action descriptions from text"""
        matches = DialogueParser.ACTION_PATTERN.findall(text)
        return matches
