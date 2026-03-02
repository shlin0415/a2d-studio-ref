"""
Real LLM Integration Test
Uses actual ema and hiro characters with LLM API
Topic: Chatting before sleep
"""

import sys
import asyncio
from pathlib import Path

# Add dialogue-server to path
dialogue_server_path = Path(__file__).parent
sys.path.insert(0, str(dialogue_server_path))

from dialogue_gen.character_loader import CharacterLoader
from dialogue_gen.prompt_builder import PromptBuilder
from dialogue_gen.dialogue_parser import DialogueParser
from dialogue_gen.output_generator import OutputGenerator
from dialogue_gen.llm_service import LLMService
from dialogue_gen.topic_loader import TopicLoader
from dialogue_gen.config import Config

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)


async def main():
    """Run real LLM dialogue generation"""
    
    print("\n" + "="*70)
    print("REAL LLM DIALOGUE GENERATION")
    print("="*70)
    print("Characters: ema, hiro")
    print("Topic: Chatting before sleep")
    print("Languages: Chinese → Japanese")
    
    # Load config from .env
    config = Config()
    
    print(f"\nConfig loaded:")
    print(f"  API Key: {config.api_key[:20]}...")
    print(f"  Model: {config.model}")
    print(f"  Base URL: {config.base_url}")
    print(f"  Max sentences: {config.max_sentences}")
    print(f"  Languages: {config.languages}")
    
    # Step 1: Load characters
    print("\n" + "="*70)
    print("STEP 1: Loading Characters")
    print("="*70)
    
    loader = CharacterLoader()
    ref_path = dialogue_server_path.parent / "Character-fig-setting-example"
    
    try:
        ema = loader.load_character(ref_path / "ema")
        hiro = loader.load_character(ref_path / "hiro")
        
        if not ema or not hiro:
            print("✗ Failed to load characters")
            return
        
        print(f"✓ Loaded ema: {ema.ai_name}")
        print(f"✓ Loaded hiro: {hiro.ai_name}")
        
        characters = [ema, hiro]
    except Exception as e:
        print(f"✗ Error loading characters: {e}")
        return
    
    # Step 2: Load topic
    print("\n" + "="*70)
    print("STEP 2: Loading Topic")
    print("="*70)
    
    topic_path = dialogue_server_path.parent / "dialogue-topics" / "chatting-before-sleep.md"
    
    try:
        if topic_path.exists():
            topic_text, topic_metadata = TopicLoader.load_topic(topic_path)
            print(f"✓ Loaded topic: {topic_metadata.title}")
            print(f"  Style: {topic_metadata.style}")
            if topic_metadata.location:
                print(f"  Location: {topic_metadata.location}")
            if topic_metadata.mood:
                print(f"  Mood: {topic_metadata.mood}")
            topic = f"""Topic: {topic_metadata.title}
Style: {topic_metadata.style}
{f"Location: {topic_metadata.location}" if topic_metadata.location else ""}

{topic_metadata.description}"""
        else:
            topic = "Characters are chatting before going to sleep."
            print(f"✓ Using default topic")
    except Exception as e:
        print(f"✗ Error loading topic: {e}")
        topic = "Characters are chatting before going to sleep."
    
    # Step 3: Build system prompt
    print("\n" + "="*70)
    print("STEP 3: Building System Prompt")
    print("="*70)
    
    builder = PromptBuilder()
    system_prompt = builder.build_system_prompt(
        user_name="player",
        characters=characters,
        topic=topic,
        language="zh",
        enable_translation=True,
        max_sentences_per_character=config.max_sentences,
    )
    
    print(f"✓ Generated system prompt ({len(system_prompt)} chars)")
    print(f"\nPrompt preview (first 400 chars):\n")
    print(system_prompt[:400])
    print("...\n")
    
    # Step 4: Call LLM API
    print("="*70)
    print("STEP 4: Calling LLM API")
    print("="*70)
    
    llm_service = LLMService(
        provider="deepseek",
        model=config.model,
        api_key=config.api_key,
        base_url=config.base_url,
    )
    
    try:
        print(f"Calling {config.model} API...")
        llm_response = await llm_service.generate_dialogue(
            system_prompt=system_prompt,
            max_tokens=2048,
            temperature=0.8,
        )
        
        print(f"✓ Received response ({len(llm_response)} chars)")
        print(f"\nLLM Response:\n")
        print(llm_response)
        
    except Exception as e:
        print(f"✗ Error calling LLM: {e}")
        print("\nUsing sample dialogue for demonstration...")
        llm_response = """【期待】这么晚来找我，是有什么事情吗？（好奇地看着对方）<こんな遅くに訪ねてくるなんて、何か用事があるの？>
【害羞】没...没什么啦（挠了挠头）<そう...何もないんだけど...>
【温柔】只是想和你聊聊天呢（坐在床边）<ただあなたと話したかったから...>
【期待】是吗？那我们聊聊今天的事吧（靠在枕头上）<そう？それなら今日のことについて話そうか>
【开心】好啊！（笑着开始聊天）<いいね！>"""
        print(llm_response)
    
    # Step 5: Parse dialogue
    print("\n" + "="*70)
    print("STEP 5: Parsing Dialogue")
    print("="*70)
    
    parser = DialogueParser()
    
    # Collect all valid emotions from characters
    all_emotions = set()
    for char in characters:
        all_emotions.update(char.available_emotions)
    
    print(f"Using character-specific emotions ({len(all_emotions)} total):")
    print(f"  {', '.join(sorted(all_emotions)[:10])}...")
    
    try:
        dialogue_lines = parser.parse_multi_character_dialogue(
            llm_response,
            [ema.character_key or ema.ai_name, hiro.character_key or hiro.ai_name],
            valid_emotions=list(all_emotions) if all_emotions else None,
        )
        
        print(f"✓ Parsed {len(dialogue_lines)} dialogue lines")
        
        for i, line in enumerate(dialogue_lines[:3]):
            print(f"\nLine {i+1}:")
            print(f"  Character: {line.character}")
            print(f"  Emotion: 【{line.emotion}】")
            print(f"  Text: {line.text}")
            if line.action:
                print(f"  Action: （{line.action}）")
            if line.text_jp:
                print(f"  JP: <{line.text_jp}>")
        
        if len(dialogue_lines) > 3:
            print(f"\n... and {len(dialogue_lines) - 3} more lines")
        
    except Exception as e:
        print(f"✗ Error parsing dialogue: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 6: Generate output
    print("\n" + "="*70)
    print("STEP 6: Generating Output Files")
    print("="*70)
    
    output_dir = dialogue_server_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generator = OutputGenerator()
    
    try:
        # Generate JSONL
        jsonl_path = output_dir / "real_dialogue.jsonl"
        generator.generate_jsonl(
            dialogue_lines=dialogue_lines,
            characters=characters,
            topic="Chatting before sleep",
            language="zh",
            output_path=jsonl_path,
        )
        print(f"✓ Generated JSONL: {jsonl_path}")
        
        # Generate JSON
        json_path = output_dir / "real_dialogue.json"
        generator.generate_json(
            dialogue_lines=dialogue_lines,
            characters=characters,
            topic="Chatting before sleep",
            language="zh",
            output_path=json_path,
        )
        print(f"✓ Generated JSON: {json_path}")
        
        # Generate TXT
        txt_path = output_dir / "real_dialogue.txt"
        generator.generate_txt(
            dialogue_lines=dialogue_lines,
            output_path=txt_path,
        )
        print(f"✓ Generated TXT: {txt_path}")
        
    except Exception as e:
        print(f"✗ Error generating output: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "="*70)
    print("✓ DIALOGUE GENERATION COMPLETE!")
    print("="*70)
    print(f"\nOutput files saved to: {output_dir}")


if __name__ == "__main__":
    asyncio.run(main())
