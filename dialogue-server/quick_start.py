"""
Quick Start Guide - Phase 1 MVP
Run this file to test all components
"""

import sys
from pathlib import Path

# Add dialogue-server to path
dialogue_server_path = Path(__file__).parent
sys.path.insert(0, str(dialogue_server_path))

from dialogue_gen.character_loader import CharacterLoader
from dialogue_gen.prompt_builder import PromptBuilder
from dialogue_gen.dialogue_parser import DialogueParser
from dialogue_gen.output_generator import OutputGenerator
from dialogue_gen.core.models import DialogueLine, CharacterSettings

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)


def demo_1_load_characters():
    """Demo 1: Load characters from Character-fig-setting-example"""
    print("\n" + "="*70)
    print("DEMO 1: Loading Characters")
    print("="*70)
    
    loader = CharacterLoader()
    ref_path = dialogue_server_path.parent / "Character-fig-setting-example"
    
    character_dirs = {
        "ema": ref_path / "ema",
        "hiro": ref_path / "hiro",
    }
    
    loaded_characters = {}
    
    for name, path in character_dirs.items():
        if path.exists():
            print(f"\nLoading '{name}' from {path}")
            char = loader.load_character(path)
            
            if char:
                loaded_characters[name] = char
                print(f"✓ Loaded: {char.ai_name}")
                print(f"  - Subtitle: {char.ai_subtitle}")
                print(f"  - System prompt: {(char.system_prompt or '')[:60]}...")
                
                # Show emotion figures
                emotions = loader.get_emotion_figures(path)
                print(f"  - Emotions ({len(emotions)}): {list(emotions.keys())[:5]}...")
            else:
                print(f"✗ Failed to load '{name}'")
        else:
            print(f"⚠ Path not found: {path}")
    
    return loaded_characters


def demo_2_build_prompts(characters):
    """Demo 2: Build system prompts"""
    print("\n" + "="*70)
    print("DEMO 2: Building System Prompts")
    print("="*70)
    
    if not characters:
        print("⚠ No characters loaded, skipping this demo")
        return
    
    builder = PromptBuilder()
    char_list = list(characters.values())
    
    print(f"\nBuilding prompt for {len(char_list)} characters")
    
    system_prompt = builder.build_system_prompt(
        user_name="Player",
        characters=char_list,
        topic="Two characters meet at a coffee shop and discuss their weekend plans",
        language="zh",
        enable_translation=False,
    )
    
    print(f"✓ Generated system prompt ({len(system_prompt)} characters)")
    print(f"\nPrompt preview (first 300 chars):\n")
    print(system_prompt[:300])
    print("...\n")
    
    return system_prompt


def demo_3_parse_dialogue():
    """Demo 3: Parse dialogue with emotion tags"""
    print("\n" + "="*70)
    print("DEMO 3: Parsing Dialogue Output")
    print("="*70)
    
    parser = DialogueParser()
    
    # Simulated LLM output
    sample_dialogue = """【高兴】今天天气真好呀！（高兴地伸了个懒腰）<The weather is wonderful today!>
【害羞】是啊，我也很开心（低下了头，脸有点红）<Me too, I'm happy...>
【开心】那我们一起去公园吧！（拉住对方的手）<Let's go to the park together!>"""
    
    print(f"\nSample LLM output:\n{sample_dialogue}\n")
    
    # Parse as multi-character dialogue
    char_names = ["Alice", "Bob"]
    
    dialogue_lines = parser.parse_multi_character_dialogue(
        raw_text=sample_dialogue,
        characters=char_names,
    )
    
    print(f"✓ Parsed {len(dialogue_lines)} dialogue lines\n")
    
    for idx, line in enumerate(dialogue_lines):
        print(f"Line {idx+1}:")
        print(f"  Character: {line.character}")
        print(f"  Emotion: 【{line.emotion}】")
        print(f"  Text: {line.text}")
        if line.action:
            print(f"  Action: （{line.action}）")
        if line.text_jp:
            print(f"  Translation: <{line.text_jp}>")
        print()
    
    return dialogue_lines


def demo_4_generate_output(dialogue_lines, characters):
    """Demo 4: Generate output files"""
    print("\n" + "="*70)
    print("DEMO 4: Generating Output Files")
    print("="*70)
    
    if not dialogue_lines:
        print("⚠ No dialogue lines to output, skipping this demo")
        return
    
    generator = OutputGenerator()
    
    # Convert character dict to list if needed
    if isinstance(characters, dict):
        char_list = list(characters.values())
    else:
        char_list = characters
    
    topic = "Two characters meet at a coffee shop"
    
    # Generate JSONL
    print(f"\nGenerating JSONL output...")
    jsonl_output = generator.generate_jsonl(
        dialogue_lines=dialogue_lines,
        characters=char_list,
        topic=topic,
        language="zh",
    )
    print(f"✓ Generated JSONL ({len(jsonl_output)} characters)")
    print(f"\nJSONL preview (first 300 chars):\n")
    print(jsonl_output[:300])
    print("...\n")
    
    # Generate JSON
    print(f"Generating JSON output...")
    json_output = generator.generate_json(
        dialogue_lines=dialogue_lines,
        characters=char_list,
        topic=topic,
        language="zh",
        pretty=True,
    )
    print(f"✓ Generated JSON ({len(json_output)} characters)")
    
    # Generate TXT
    print(f"\nGenerating TXT output...")
    txt_output = generator.generate_txt(
        dialogue_lines=dialogue_lines,
    )
    print(f"✓ Generated TXT ({len(txt_output)} characters)")
    print(f"\nTXT preview:\n")
    print(txt_output)


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("PHASE 1 MVP - QUICK START DEMO")
    print("="*70)
    print("\nThis demonstrates all 4 core components of the dialogue generation server:")
    print("1. Character Loading")
    print("2. Prompt Building")
    print("3. Dialogue Parsing")
    print("4. Output Generation")
    print("\nNote: To generate actual dialogue, you'll need OpenAI API key")
    
    # Run demos
    try:
        # Demo 1: Load characters
        characters = demo_1_load_characters()
        
        # Demo 2: Build prompts
        system_prompt = demo_2_build_prompts(characters)
        
        # Demo 3: Parse dialogue (using sample)
        dialogue_lines = demo_3_parse_dialogue()
        
        # Demo 4: Generate output
        demo_4_generate_output(dialogue_lines, characters)
        
        print("\n" + "="*70)
        print("✓ ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nNext steps:")
        print("1. Set CHAT_API_KEY environment variable")
        print("2. Run: python -m dialogue_gen.dialogue_generator")
        print("3. Or import DialogueGenerator for your own code")
        print("4. See README.md for detailed documentation")
        print()
        
    except Exception as e:
        print(f"\n✗ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
