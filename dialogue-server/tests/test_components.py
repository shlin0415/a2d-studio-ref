"""
Test script for Phase 1 MVP
Tests all components with Character-fig-setting-example
"""

import sys
import asyncio
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dialogue_gen.character_loader import CharacterLoader
from dialogue_gen.prompt_builder import PromptBuilder
from dialogue_gen.dialogue_parser import DialogueParser
from dialogue_gen.output_generator import OutputGenerator

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_character_loader():
    """Test character loading"""
    print("\n" + "="*60)
    print("TEST 1: Character Loader")
    print("="*60)
    
    loader = CharacterLoader()
    
    # Test with example characters
    char_paths = [
        Path(__file__).parent.parent / "Character-fig-setting-example" / "ema",
        Path(__file__).parent.parent / "Character-fig-setting-example" / "hiro",
    ]
    
    for char_path in char_paths:
        if char_path.exists():
            print(f"\nLoading character from: {char_path}")
            character = loader.load_character(char_path)
            
            if character:
                print(f"✓ Successfully loaded: {character.ai_name}")
                print(f"  Subtitle: {character.ai_subtitle}")
                print(f"  Prompt preview: {(character.system_prompt or '')[:100]}...")
                
                # Get emotion figures
                emotions = loader.get_emotion_figures(char_path)
                print(f"  Found {len(emotions)} emotion figures: {', '.join(list(emotions.keys())[:5])}...")
            else:
                print(f"✗ Failed to load character")
        else:
            print(f"✗ Character path not found: {char_path}")


def test_prompt_builder():
    """Test prompt building"""
    print("\n" + "="*60)
    print("TEST 2: Prompt Builder")
    print("="*60)
    
    builder = PromptBuilder()
    
    # Load characters first
    loader = CharacterLoader()
    char_paths = [
        Path(__file__).parent.parent / "Character-fig-setting-example" / "ema",
        Path(__file__).parent.parent / "Character-fig-setting-example" / "hiro",
    ]
    
    characters = []
    for path in char_paths:
        if path.exists():
            char = loader.load_character(path)
            if char:
                characters.append(char)
    
    if characters:
        print(f"\nBuilding prompt for {len(characters)} characters")
        
        system_prompt = builder.build_system_prompt(
            user_name="Alice",
            characters=characters,
            topic="Two characters meet at a bookstore and discuss their favorite books",
            language="zh",
            enable_translation=False,
        )
        
        print(f"✓ Generated system prompt ({len(system_prompt)} chars)")
        print(f"\nPrompt preview:\n{system_prompt[:300]}...\n")
        
        # Test emotion validation
        emotions = builder.get_emotion_list()
        print(f"✓ Standard emotions ({len(emotions)}): {emotions[:5]}...")
        
        is_valid = builder.validate_emotion("高兴")
        print(f"✓ Emotion validation - '高兴' is valid: {is_valid}")
        
        is_valid = builder.validate_emotion("invalid_emotion")
        print(f"✓ Emotion validation - 'invalid_emotion' is valid: {is_valid}")


def test_dialogue_parser():
    """Test dialogue parsing"""
    print("\n" + "="*60)
    print("TEST 3: Dialogue Parser")
    print("="*60)
    
    parser = DialogueParser()
    
    # Test single unit parsing
    test_cases = [
        "【高兴】今天天气真好！<Today's weather is wonderful!>",
        "【害羞】我...我觉得有点不好意思呢（低下了头）<I feel a bit embarrassed...>",
        "【生气】你为什么这样做！（愤怒地指向对方）",
        "【无语】这就是你的理由吗？（摇了摇头）",
    ]
    
    print("\nParsing individual dialogue units:")
    
    for test_case in test_cases:
        print(f"\nInput: {test_case}")
        
        line = parser.parse_dialogue_unit(
            text=test_case,
            character_name="TestChar",
            valid_emotions=parser.EMOTIONS,
        )
        
        if line:
            print(f"✓ Parsed successfully")
            print(f"  Emotion: {line.emotion}")
            print(f"  Text: {line.text}")
            print(f"  Action: {line.action}")
            print(f"  Translation: {line.text_jp}")
        else:
            print(f"✗ Failed to parse")
    
    # Test raw response parsing
    raw_dialogue = """【高兴】今天天气真好！
【害羞】我...我也觉得（低下了头）<I think so too...>
【开心】我们一起出去走走吧！"""
    
    print(f"\n\nParsing multi-line dialogue:")
    print(f"Input (raw):\n{raw_dialogue}\n")
    
    lines = parser.parse_raw_response(
        raw_text=raw_dialogue,
        character_name="Alice",
    )
    
    print(f"✓ Parsed {len(lines)} lines")
    for idx, line in enumerate(lines):
        print(f"  Line {idx+1}: [{line.emotion}] {line.text}")


def test_output_generator():
    """Test output generation"""
    print("\n" + "="*60)
    print("TEST 4: Output Generator")
    print("="*60)
    
    from dialogue_gen.core.models import DialogueLine, CharacterSettings
    
    # Create sample dialogue
    dialogue_lines = [
        DialogueLine(
            character="Alice",
            emotion="高兴",
            text="今天天气真好啊！",
            action="",
            text_jp="今日はいい天気ですね！",
        ),
        DialogueLine(
            character="Bob",
            emotion="害羞",
            text="是啊，我们一起出去走走吧（拉住Alice的手）",
            action="拉住Alice的手",
            text_jp="そうですね、一緒に歩きませんか",
        ),
    ]
    
    characters = [
        CharacterSettings(ai_name="Alice"),
        CharacterSettings(ai_name="Bob"),
    ]
    
    topic = "Two friends meet and plan their weekend"
    
    print(f"\nGenerating JSONL output...")
    jsonl_output = OutputGenerator.generate_jsonl(
        dialogue_lines=dialogue_lines,
        characters=characters,
        topic=topic,
        language="zh",
    )
    print(f"✓ Generated JSONL ({len(jsonl_output)} chars)")
    print(f"\nJSONL preview:\n{jsonl_output[:300]}...\n")
    
    print(f"\nGenerating JSON output...")
    json_output = OutputGenerator.generate_json(
        dialogue_lines=dialogue_lines,
        characters=characters,
        topic=topic,
        language="zh",
        pretty=True,
    )
    print(f"✓ Generated JSON ({len(json_output)} chars)")
    
    print(f"\nGenerating TXT output...")
    txt_output = OutputGenerator.generate_txt(
        dialogue_lines=dialogue_lines,
    )
    print(f"✓ Generated TXT ({len(txt_output)} chars)")
    print(f"\nTXT preview:\n{txt_output}\n")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*80)
    print("PHASE 1 MVP: Component Testing")
    print("="*80)
    
    try:
        test_character_loader()
        test_prompt_builder()
        test_dialogue_parser()
        test_output_generator()
        
        print("\n" + "="*80)
        print("✓ All tests completed successfully!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
