# Dialogue Generation Server - Phase 1 MVP

## Overview

A Python-based server for generating multi-character dialogues using LLM APIs. Implements the architecture designed in **TASK1_ANALYSIS.md**.

## Phase 1 Components (Complete ✓)

### ✅ Core Modules

1. **Character Loader** (`character_loader.py`)
   - Reads character settings from `setting.txt` (YAML format)
   - Discovers emotion figure files in `fig/` folders
   - Validates character configuration
   - Returns `CharacterSettings` objects

2. **Prompt Builder** (`prompt_builder.py`)
   - Constructs system prompts with dialogue format rules
   - Enforces 【emotion】text（actions）<translation> format
   - Supports 18 standard emotions
   - Multi-language support (ZH, EN, JP)

3. **LLM Service** (`llm_service.py`)
   - Wrapper around LLM APIs (OpenAI support included)
   - Streaming and non-streaming generation
   - Configurable model and parameters

4. **Dialogue Parser** (`dialogue_parser.py`)
   - Parses LLM output with emotion tags
   - Extracts emotion, dialogue, action, and translation
   - Validates emotion format
   - Supports multi-character dialogue assignment

5. **Output Generator** (`output_generator.py`)
   - Generates JSONL playbooks (primary format)
   - Alternative formats: JSON, CSV, TXT
   - Structured metadata and headers
   - File I/O support

6. **Main Orchestrator** (`dialogue_generator.py`)
   - `DialogueGenerator` class coordinates all components
   - `generate_multi_character_dialogue()` - Main API
   - `generate_single_character_dialogue()` - Single character
   - Full async/await support

### ✅ Data Models (`core/models.py`)

- `CharacterSettings` - Character configuration (based on LingChat)
- `DialogueLine` - Single dialogue unit
- `DialoguePlaybook` - Complete dialogue output
- `STANDARD_EMOTIONS` - 18-emotion list

### ✅ Testing (`tests/test_components.py`)

Complete test suite for all components:
- Character loading from Character-fig-setting-example
- Prompt building with multiple characters
- Dialogue unit parsing
- Multi-line dialogue parsing
- Output generation (JSONL, JSON, TXT)

## Project Structure

```
dialogue-server/
├── dialogue_gen/
│   ├── __init__.py
│   ├── character_loader.py        # Load character settings
│   ├── prompt_builder.py          # Build system prompts
│   ├── dialogue_parser.py         # Parse dialogue output
│   ├── output_generator.py        # Generate JSONL/JSON/CSV/TXT
│   ├── llm_service.py             # LLM API wrapper
│   ├── dialogue_generator.py      # Main orchestrator
│   └── core/
│       ├── __init__.py
│       └── models.py              # Data models
├── tests/
│   └── test_components.py         # Component tests
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or manually install
pip install pydantic pyyaml aiohttp openai python-dotenv
```

## Quick Start

### 1. Set Environment Variables

```bash
export CHAT_API_KEY="sk-..."  # OpenAI API key
```

Or create a `.env` file in the `dialogue-server` directory:

```env
CHAT_API_KEY=sk-...
```

### 2. Run Tests

```bash
cd dialogue-server
python tests/test_components.py
```

Expected output:
```
================================================================================
PHASE 1 MVP: Component Testing
================================================================================

============================================================
TEST 1: Character Loader
============================================================

Loading character from: .../Character-fig-setting-example/ema
✓ Successfully loaded: ema
  Subtitle: Female character with calm demeanor
  Prompt preview: ...
  Found 18 emotion figures: 平静, 害羞, 生气, ...
```

### 3. Generate Dialogue (Example)

```python
import asyncio
from pathlib import Path
from dialogue_gen.dialogue_generator import DialogueGenerator

async def main():
    generator = DialogueGenerator()
    
    result = await generator.generate_multi_character_dialogue(
        character_paths=[
            "Character-fig-setting-example/ema",
            "Character-fig-setting-example/hiro",
        ],
        topic="Two friends meet at a bookstore discussing their favorite books",
        user_name="player",
        language="zh",
        output_path=Path("output/dialogue.jsonl"),
        output_format="jsonl",
    )
    
    print(f"Generated {result['num_lines']} dialogue lines")

asyncio.run(main())
```

## Output Format

### JSONL Format (Recommended)

```jsonl
{"header": {"characters": ["Alice", "Bob"], "topic": "...", "language": "zh", "emotion_count": 18, "line_count": 5, "timestamp": "...", "format_version": "1.0"}}
{"index": 0, "character": "Alice", "emotion": "高兴", "text": "今天天气真好！", "action": "", "text_jp": "今日はいい天気ですね", "emotion_jp": null, "timestamp": null}
{"index": 1, "character": "Bob", "emotion": "害羞", "text": "是啊，我们一起出去走走吧（拉住Alice的手）", "action": "拉住Alice的手", "text_jp": "そうですね、一緒に歩きませんか", "emotion_jp": null, "timestamp": null}
```

### JSON Format

```json
{
  "header": {
    "characters": ["Alice", "Bob"],
    "character_count": 2,
    "topic": "...",
    "language": "zh",
    "emotion_count": 18,
    "line_count": 5
  },
  "lines": [
    {
      "index": 0,
      "character": "Alice",
      "emotion": "高兴",
      "text": "今天天气真好！",
      "action": "",
      "text_jp": "今日はいい天気ですね"
    },
    ...
  ]
}
```

### TXT Format

```
Alice: 【高兴】今天天气真好！
  → 今日はいい天気ですね

Bob: 【害羞】是啊，我们一起出去走走吧（拉住Alice的手）
  → そうですね、一緒に歩きませんか
```

## API Reference

### DialogueGenerator Class

```python
class DialogueGenerator:
    async def generate_multi_character_dialogue(
        character_paths: List[str | Path],
        topic: str,
        user_name: str = "player",
        language: str = "zh",
        enable_translation: bool = False,
        output_path: Optional[Path] = None,
        output_format: str = "jsonl",
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> Dict[str, Any]
```

**Returns:**
```python
{
    "success": bool,
    "characters": List[str],
    "num_lines": int,
    "output_format": str,
    "output_path": Optional[str],
    "dialogue_lines": List[DialogueLine],
    "raw_output": str,  # First 500 chars of output
}
```

## Character Format

Characters must follow the structure from **Character-fig-setting-example**:

```
character_name/
├── setting.txt              # YAML configuration
├── fig/
│   ├── 平静.png             # Emotion figures
│   ├── 害羞.png
│   ├── 生气.png
│   └── ... (up to 18 emotions)
└── 头像.png                 # Avatar image
```

## Configuration

### System Prompt Structure

The prompt builder automatically:
- Includes character descriptions from `system_prompt` field
- Specifies dialogue format rules (【emotion】text）
- Lists valid emotions
- Provides format examples
- Defines conversation rules

### Supported Emotions (18 Standard)

```
慌张、担心、尴尬、紧张、高兴、自信、害怕、害羞、
认真、生气、无语、厌恶、疑惑、难为情、惊讶、情动、
哭泣、调皮
```

## Known Limitations & TODO

### Phase 1 Limitations
- Single LLM provider (OpenAI) - others can be added
- No translation integration yet (framework ready for Phase 3)
- No voice synthesis (Phase 3)
- No persistent memory banks (Phase 3)
- No emotion figure linking (Phase 3+)

### Phase 2 TODO
- [ ] Multi-character context refinement
- [ ] Character alternation validation
- [ ] Long conversation handling (token counting)
- [ ] Better emotion assignment logic

### Phase 3 TODO
- [ ] Translation service (ZH ↔ JP, EN)
- [ ] Long context compression
- [ ] Voice synthesis integration
- [ ] Memory bank system
- [ ] Emotion figure annotation

## Logging

Set logging level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Log messages include:
- Character loading status
- Prompt construction details
- Dialogue parsing results
- Output generation confirmation

## Testing Component by Component

### Test Character Loader Only

```python
from dialogue_gen.character_loader import CharacterLoader

loader = CharacterLoader()
character = loader.load_character("Character-fig-setting-example/ema")
print(character.ai_name)  # Output: ema
```

### Test Prompt Builder Only

```python
from dialogue_gen.prompt_builder import PromptBuilder

builder = PromptBuilder()
prompt = builder.build_system_prompt(
    user_name="Alice",
    characters=[character1, character2],
    topic="Two friends meeting",
)
print(prompt[:200])
```

### Test Dialogue Parser Only

```python
from dialogue_gen.dialogue_parser import DialogueParser

parser = DialogueParser()
line = parser.parse_dialogue_unit(
    text="【高兴】今天真开心！（拍了拍chest）",
    character_name="Alice",
)
print(line.emotion)  # Output: 高兴
print(line.text)     # Output: 今天真开心！
print(line.action)   # Output: 拍了拍chest
```

## Troubleshooting

### Issue: "No API key found"
**Solution:** Set `CHAT_API_KEY` environment variable
```bash
export CHAT_API_KEY="sk-..."
```

### Issue: Character not loading
**Solution:** Ensure `setting.txt` exists and is valid YAML
```bash
ls -la Character-fig-setting-example/ema/setting.txt
```

### Issue: Emotion parsing failing
**Solution:** Check emotion tags are wrapped with 【】 (not regular brackets)
```
✗ Wrong: [emotion]text
✓ Right: 【emotion】text
```

## Next Steps (Phase 2+)

1. **Integration Testing** - Test with actual OpenAI API
2. **Multi-Character Refinement** - Better character context handling
3. **Translation Pipeline** - Add ZH→JP translation
4. **Token Management** - Handle 1000+ word conversations
5. **Animation Integration** - Link dialogue to character figures
6. **Performance** - Caching, streaming optimization

## Contributing

When extending the system:
1. Follow the async/await pattern used in `DialogueGenerator`
2. Add logging at key points
3. Update data models in `core/models.py` as needed
4. Add tests to `tests/test_components.py`
5. Update this README

## References

- [Full Analysis](../TASK1_ANALYSIS.md)
- [Character Format Example](../Character-fig-setting-example/)
- [LingChat Source](../LingChat/)
- [SillyTavern Source](../SillyTavern/)

