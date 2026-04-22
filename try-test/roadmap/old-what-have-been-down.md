# What Have Been Done: Task1 and Task2 Summary

## Overview

This document summarizes the work completed in **Task 1 (Dialogue Server)** and **Task 2 (Voice Server)** for the a2d-studio project.

---

## Task 1: Dialogue Generation Server

### Objective
Build a multi-character dialogue generation server that generates structured dialogue scripts from character settings and topics using LLM.

### Key Components Implemented

#### 1. Character Loader (`dialogue-server/dialogue_gen/character_loader.py`)
- Reads `setting.txt` from character folders in `Character-fig-setting-example/`
- Parses YAML format with fallback to regex
- Dynamically discovers emotion figures from `fig/` directories
- Returns structured `CharacterSettings` objects

#### 2. Prompt Builder (`dialogue-server/dialogue_gen/prompt_builder.py`)
- Constructs system prompts with dialogue format rules
- Implements LingChat-style format: `【emotion】text（actions）<translation>`
- Supports 18 standard emotions
- Multi-language support (Chinese, English, Japanese)

#### 3. LLM Service (`dialogue-server/dialogue_gen/llm_service.py`)
- OpenAI API wrapper with streaming support
- Configurable model and parameters
- Async/await support
- Error handling and logging

#### 4. Dialogue Parser (`dialogue-server/dialogue_gen/dialogue_parser.py`)
- Parses emotion tags from LLM output
- Extracts dialogue, actions, translations
- Validates emotions against character figure sets
- Multi-character assignment (round-robin)

#### 5. Output Generator (`dialogue-server/dialogue_gen/output_generator.py`)
- JSONL format (primary, like SillyTavern)
- Alternative formats: JSON, CSV, TXT
- Metadata headers with character info

#### 6. Main Orchestrator (`dialogue-server/dialogue_gen/dialogue_generator.py`)
- Coordinates all components
- `generate_multi_character_dialogue()` for multi-character
- `generate_single_character_dialogue()` for single character

### Data Models (`dialogue-server/dialogue_gen/core/models.py`)
- `CharacterSettings` - Character configuration
- `DialogueLine` - Single dialogue unit
- `DialoguePlaybook` - Complete dialogue output
- `STANDARD_EMOTIONS` - 18-emotion list

### Character Format
Characters stored in `Character-fig-setting-example/`:
```
character_name/
├── fig/
│   ├── 平静.png
│   ├── 害羞.png
│   ├── 生气.png
│   └── ... (emotion figures)
├── setting.txt
└── 头像.png
```

### Example Characters
- **艾玛 (Ema)**: `Character-fig-setting-example/艾玛/`
- **希罗 (Hiro)**: `Character-fig-setting-example/希罗/`

### Topic Format
Topics stored in `dialogue-topics/`:
```markdown
# Chatting Before Sleep

Style: a little nsfw
Location: Bedroom
Mood: Intimate, comfortable, relaxed
```

### Output Format (JSONL)
```json
{"index": 0, "character": "艾玛", "emotion": "期待", "text": "这么晚来找我，是有什么事情吗？", "action": "高兴地看着希罗", "text_jp": "んな遅くに私を訪ねてくるなんて、何か用事があるの？"}
{"index": 1, "character": "希罗", "emotion": "开心", "text": "就想来陪你啊。", "action": "靠近艾玛", "text_jp": "単純にだよ"}
```

### Key Features
- Emotion validation against actual character figure files
- Multi-language output (Chinese + Japanese translation)
- Action parsing in parentheses
- Configurable sentence limits per character
- Style and location settings from topic markdown

---

## Task 2: Voice Server

### Objective
Build a voice server that converts dialogue text into audio using GPT-SoVITS API.

### Key Components Implemented

#### 1. Voice Demo (`voice-server/demo_gpt_sovits_voice.py`)
- Basic GPT-SoVITS API client
- Loads character voice settings from `Character-voice-example/`
- Generates audio for dialogue text
- Saves to output folder

#### 2. Performance Testing
- `test_single_port_bottleneck.py` - Tests single port (9880) performance
- `test_dual_port_performance.py` - Tests dual port (31801, 31802) performance
- Compares model switching overhead

### Character Voice Format
Characters stored in `Character-voice-example/`:
```
character_name/
├── GPT-SoVITS/
│   ├── good_ref/
│   │   ├── 0101Adv26_Ema012.wav    # Reference audio
│   │   └── 0101Adv26_Ema012.txt    # Reference text
│   ├── manosaba_ema-e15.ckpt       # GPT model
│   ├── manosaba_ema_e8_s864.pth   # SoVITS model
│   └── voice_setting.txt           # Config
```

### Example Voice Characters
- **艾玛 (Ema)**: `Character-voice-example/艾玛/GPT-SoVITS/`
  - GPT model: `manosaba_ema-e15.ckpt`
  - SoVITS model: `manosaba_ema_e8_s864.pth`
  - Type: v2
  
- **希罗 (Hiro)**: `Character-voice-example/希罗/GPT-SoVITS/`
  - GPT model: `hiro-e15.ckpt`
  - SoVITS model: `hiro_e8_s2184.pth`
  - Type: v2ProPlus

### GPT-SoVITS API
- **Endpoint**: `http://127.0.0.1:9880`
- **Main endpoints**:
  - `POST /tts` - Generate speech
  - `GET /set_gpt_weights?weights_path=...` - Load GPT model
  - `GET /set_sovits_weights?weights_path=...` - Load SoVITS model

### Audio Output
Generated audio stored in `voice-server/output/`:
```
output/
├── demo_voice/
│   ├── 艾玛/
│   │   ├── zh_艾玛.wav
│   │   ├── en_艾玛.wav
│   │   └── ja_艾玛.wav
│   └── 希罗/
│       ├── zh_希罗.wav
│       ├── en_希罗.wav
│       └── ja_希罗.wav
├── single_port_test_audio/
└── dual_port_test_audio/
```

---

## File Structure Summary

```
ref/
├── dialogue-server/                    # Task 1: Dialogue Generation
│   ├── dialogue_gen/
│   │   ├── character_loader.py
│   │   ├── prompt_builder.py
│   │   ├── llm_service.py
│   │   ├── dialogue_parser.py
│   │   ├── output_generator.py
│   │   ├── dialogue_generator.py
│   │   ├── topic_loader.py
│   │   └── core/
│   │       └── models.py
│   ├── tests/
│   │   └── test_components.py
│   ├── output/
│   │   ├── real_dialogue.json
│   │   └── real_dialogue.jsonl
│   ├── quick_start.py
│   ├── README.md
│   └── requirements.txt
│
├── voice-server/                      # Task 2: Voice Generation
│   ├── demo_gpt_sovits_voice.py
│   ├── test_single_port_bottleneck.py
│   ├── test_dual_port_performance.py
│   ├── output/
│   │   ├── demo_voice/
│   │   ├── single_port_test_audio/
│   │   └── dual_port_test_audio/
│   └── compare_results.py
│
├── Character-fig-setting-example/    # Character Visual Settings
│   ├── 艾玛/
│   │   ├── setting.txt
│   │   ├── fig/
│   │   │   ├── 平静.png
│   │   │   ├── 开心.png
│   │   │   └── ... (18 emotions)
│   │   └── 头像.png
│   └── 希罗/
│       ├── setting.txt
│       ├── fig/
│       │   └── ... (13 emotions)
│       └── 头像.png
│
├── Character-voice-example/           # Character Voice Settings
│   ├── 艾玛/
│   │   └── GPT-SoVITS/
│   │       ├── voice_setting.txt
│   │       ├── good_ref/
│   │       └── models
│   └── 希罗/
│       └── GPT-SoVITS/
│           ├── voice_setting.txt
│           ├── good_ref/
│           └── models
│
├── dialogue-topics/                   # Dialogue Topics
│   └── chatting-before-sleep.md
│
└── tried-tasks-sessions-files/       # Task Documentation
    ├── task1-human-chat.md
    ├── task2-human-chat.md
    ├── TASK1_ANALYSIS.md
    ├── TASK2_ANALYSIS.md
    └── ...
```

---

## Technical Highlights

### Dialogue Format (from LingChat)
```
【emotion】dialogue text（optional actions）<optional translation>

Example:
【期待】这么晚来找我，是有什么事情吗？（高兴地伸了个懒腰）<こんなに遅くに私を訪ねてくるなんて、何か用事があるの？>
```

### 18 Standard Emotions
慌张、担心、尴尬、紧张、高兴、自信、害怕、害羞、认真、生气、无语、厌恶、疑惑、难为情、惊讶、情动、哭泣、调皮

### Multi-Language Support
- **Caption text**: Chinese (default), can be English or Japanese
- **Voice text**: Japanese (default), can be Chinese or English
- Translation via LLM

### Voice Generation Pipeline
1. Load character voice config from `voice_setting.txt`
2. Set GPT model weights (`/set_gpt_weights`)
3. Set SoVITS model weights (`/set_sovits_weights`)
4. Generate audio with reference audio (`/tts`)
5. Save audio to output folder

---

## Next Steps (Future Tasks)

### Task 3: Integration
- Connect dialogue-server output to voice-server input
- Implement caption_text vs voice_text separation
- Handle action text removal for voice generation

### Task 4: Enhanced Features
- Token management for long conversations
- Memory bank system
- Animation/sprite control integration

---

*Last Updated: 2026-03-15*
