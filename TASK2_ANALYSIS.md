# TASK2 Analysis: Voice Server Architecture for GPT-SoVITS Integration

## 0. Executive Summary

**Objective**: Build a voice server that converts Phase 2 dialogue text into audio using GPT-SoVITS API.

**GPT-SoVITS API**: Runs on local `http://127.0.0.1:9880` (or configurable port), provides:
- `/tts` endpoint: Convert text to speech with speaker/emotion via reference audio
- `/set_gpt_weights`: Load GPT model weights (.ckpt)
- `/set_sovits_weights`: Load SoVITS model weights (.pth)

**Character Voice Mapping**:
```
Character-voice-example/
├── 艾玛/ (Ema) → ema.character_key
│   └── GPT-SoVITS/
│       ├── good_ref/
│       │   ├── good_ref_audio.wav        # Prompt audio (2-3 sec)
│       │   └── good_ref_audio.txt        # Corresponding text
│       ├── manosaba_ema-e15.ckpt         # GPT model
│       ├── manosaba_ema_e8_s864.pth      # SoVITS model
│       └── voice_setting.txt             # Config metadata
└── 希罗/ (Hiro) → hiro.character_key
    └── GPT-SoVITS/
        ├── good_ref/
        │   ├── good_ref_audio.ogg        # Prompt audio
        │   └── good_ref_audio.txt        # Corresponding text
        ├── hiro-e15.ckpt                 # GPT model
        ├── hiro_e8_s2184.pth             # SoVITS model
        └── voice_setting.txt             # Config metadata
```

**Key Constraints**:
- GPT-SoVITS only (not vits-simple-api)
- One voice per character (no emotion-based voice switching)
- Use reference audio + reference text for voice cloning
- Return file paths (store audio in output/ folder)
- Don't stream audio directly (save to disk first)

---

## 1. GPT-SoVITS API Specification

### Endpoint: `/tts` (POST)

**Request Body** (JSON):
```json
{
    "text": "早上好，艾玛。",                # str.(required) text to synthesize
    "text_lang": "zh",                      # str.(required) zh/en/ja/yue/ko/auto
    "ref_audio_path": "path/to/ref.wav",   # str.(required) reference audio path (absolute or relative)
    "aux_ref_audio_paths": [],              # list.(optional) multi-speaker fusion refs
    "prompt_text": "早上好。",              # str.(optional) prompt text corresponding to ref audio
    "prompt_lang": "zh",                    # str.(required) language of prompt text
    "top_k": 5,                             # int. top k sampling (default: 5)
    "top_p": 1.0,                           # float. top p sampling (default: 1.0)
    "temperature": 1.0,                     # float. sampling temperature (default: 1.0)
    "text_split_method": "cut5",            # str. sentence segmentation method
    "batch_size": 1,                        # int. inference batch size (default: 1)
    "batch_threshold": 0.75,                # float. batch splitting threshold
    "split_bucket": true,                   # bool. split batch into buckets
    "speed_factor": 1.0,                    # float. speech speed (1.0=normal, 0.5=slow, 2.0=fast)
    "fragment_interval": 0.3,               # float. audio fragment interval
    "seed": -1,                             # int. reproducibility seed (-1=random)
    "media_type": "wav",                    # str. output format: wav/ogg/aac/raw
    "streaming_mode": false,                # bool. stream response (true=chunk by chunk)
    "parallel_infer": true,                 # bool. parallel inference (default: true)
    "repetition_penalty": 1.35,             # float. T2S model repetition penalty
    "sample_steps": 32,                     # int. VITS V3 sampling steps
    "super_sampling": false,                # bool. VITS V3 super-sampling
    "overlap_length": 2,                    # int. streaming mode token overlap
    "min_chunk_length": 16                  # int. streaming mode min chunk length
}
```

**Response**:
- **Success** (200): Binary audio stream (WAV/OGG/AAC/RAW bytes)
- **Failure** (400): JSON error message
  ```json
  {
      "detail": "Error message describing the issue"
  }
  ```

### Endpoint: `/set_gpt_weights` (GET or POST)

**GET**:
```
http://127.0.0.1:9880/set_gpt_weights?weights_path=/path/to/model.ckpt
```

**POST**:
```json
{
    "weights_path": "/path/to/model.ckpt"
}
```

**Response**:
- **Success** (200): `"success"` (plain text)
- **Failure** (400): JSON error message

**Notes**:
- Path can be absolute or relative to GPT-SoVITS root
- File must be .ckpt format
- This switches GPT model for future /tts calls

### Endpoint: `/set_sovits_weights` (GET or POST)

**GET**:
```
http://127.0.0.1:9880/set_sovits_weights?weights_path=/path/to/model.pth
```

**POST**:
```json
{
    "weights_path": "/path/to/model.pth"
}
```

**Response**:
- **Success** (200): `"success"` (plain text)
- **Failure** (400): JSON error message

**Notes**:
- Path can be absolute or relative to GPT-SoVITS root
- File must be .pth format
- This switches SoVITS model for future /tts calls

---

## 2. Phase 3 Architecture Design

### 2.1 Component Overview

```
dialogue-server/
├── voice_server/                          # NEW: Voice synthesis module
│   ├── __init__.py
│   ├── voice_loader.py                    # Load character voice configs
│   ├── voice_service.py                   # GPT-SoVITS API client
│   ├── voice_cache.py                     # Cache generated audio files
│   └── models.py                          # Voice-related data models
├── config.py                              # EXISTING: Environment config
├── dialogue_gen/                          # EXISTING: Phase 1-2
│   ├── character_loader.py
│   ├── prompt_builder.py
│   ├── dialogue_parser.py
│   ├── output_generator.py
│   └── topic_loader.py
├── output/                                # EXISTING: Output files
│   ├── dialogue.jsonl                     # Phase 2 output
│   ├── dialogue.json
│   ├── audio/                             # NEW: Voice cache folder
│   │   ├── ema_00000.wav
│   │   ├── ema_00001.wav
│   │   ├── hiro_00000.wav
│   │   └── ...
│   └── dialogue_with_voice.jsonl          # NEW: Phase 3 output with audio paths
├── demo_dialogue.py                       # EXISTING: Phase 1 demo
├── demo_real_llm.py                       # EXISTING: Phase 2 demo
├── demo_voice_generation.py               # NEW: Phase 3 demo
└── requirements.txt                       # EXISTING: Add httpx
```

### 2.2 Core Classes

#### 2.2.1 VoiceLoader (voice_loader.py)

**Purpose**: Load character voice configurations from Character-voice-example folder.

**Key Methods**:
```python
class VoiceLoader:
    async def load_character_voice(character: Character) -> VoiceConfig
        # Load GPT-SoVITS weights and reference audio for a character
        # Args:
        #   character: Character object from Phase 2
        # Returns:
        #   VoiceConfig with gpt_model_path, sovits_model_path, ref_audio_path, ref_text, prompt_lang
        # Raises:
        #   FileNotFoundError: If voice files not found
        #   ValueError: If voice_setting.txt is invalid
    
    def parse_voice_setting(setting_txt: str) -> dict
        # Parse voice_setting.txt file
        # Format: key=value lines with gsv_* prefix
        # Returns: dict with gsv_* keys
    
    def resolve_voice_path(character_key: str, relative_path: str) -> Path
        # Resolve paths in Character-voice-example/{character_key}/GPT-SoVITS/
```

**Data Model** (voice_server/models.py):
```python
class VoiceConfig(BaseModel):
    character_key: str              # ema, hiro, etc.
    gpt_model_path: str             # Absolute path to .ckpt file
    sovits_model_path: str          # Absolute path to .pth file
    ref_audio_path: str             # Absolute path to reference audio (wav/ogg)
    ref_text: str                   # Corresponding text for reference audio
    prompt_lang: str                # Language code (zh, en, ja, yue, ko)
    
class VoiceGenerationResult(BaseModel):
    character_key: str
    text: str
    audio_path: str                 # Relative path in output/audio/
    duration_seconds: float
    timestamp: datetime
```

#### 2.2.2 VoiceService (voice_service.py)

**Purpose**: Async HTTP client for GPT-SoVITS API.

**Key Methods**:
```python
class VoiceService:
    def __init__(gpt_sovits_url: str = "http://127.0.0.1:9880"):
        # Initialize HTTP client
    
    async def set_model(voice_config: VoiceConfig) -> bool
        # Load character's GPT and SoVITS models
        # 1. POST to /set_gpt_weights with gpt_model_path
        # 2. POST to /set_sovits_weights with sovits_model_path
        # Returns: True if both succeed, False otherwise
    
    async def generate_voice(
        text: str,
        voice_config: VoiceConfig,
        language: str = "auto",
        speed_factor: float = 1.0,
        media_type: str = "wav"
    ) -> bytes
        # Generate audio for text using pre-loaded models
        # Args:
        #   text: Text to synthesize (Chinese/Japanese/English/etc.)
        #   voice_config: Character voice configuration
        #   language: Target text language (auto-detect if "auto")
        #   speed_factor: Speech speed (0.5-2.0)
        #   media_type: Output format (wav, ogg, aac, raw)
        # Returns: Audio bytes
        # Raises:
        #   HTTPException: If API call fails
        #   TimeoutError: If request times out
    
    async def health_check() -> bool
        # Check if GPT-SoVITS API is running
        # GET to http://127.0.0.1:9880/docs (or try /tts with minimal request)
```

#### 2.2.3 VoiceCache (voice_cache.py)

**Purpose**: Manage audio file caching and deduplication.

**Key Methods**:
```python
class VoiceCache:
    def __init__(cache_dir: Path = Path("output/audio")):
        # Initialize cache directory
    
    async def save_audio(
        audio_bytes: bytes,
        character_key: str,
        text: str,
        media_type: str = "wav"
    ) -> str
        # Save audio to cache and return relative path
        # Naming: {character_key}_{sequence:05d}.{ext}
        # Example: ema_00000.wav, hiro_00001.wav
        # Returns: Relative path (audio/ema_00000.wav)
    
    def get_cached_audio(character_key: str, text: str) -> Optional[str]
        # Check if audio already exists for exact text
        # Returns: Relative path if found, None otherwise
    
    def clear_cache() -> int
        # Clear all cached audio files
        # Returns: Number of files deleted
    
    async def get_audio_duration(audio_path: Path) -> float
        # Get audio duration in seconds using soundfile or librosa
```

### 2.3 Integration Points

#### 2.3.1 With Phase 2 Output

**Input**: Phase 2 dialogue output (real_dialogue.jsonl)
```json
{
    "character_key": "ema",
    "emotion": "期待",
    "text": "这么晚来找我，是有什么事情吗？",
    "action": "高兴地看着hiro",
    "translation": "What brings you here so late?"
}
```

**Processing Flow**:
1. Read real_dialogue.jsonl from Phase 2
2. For each line:
   - Extract character_key and text
   - Call VoiceService.generate_voice(text, character_voice_config)
   - Call VoiceCache.save_audio(audio_bytes, character_key, text)
   - Append audio_path to output
3. Write dialogue_with_voice.jsonl

#### 2.3.2 Output Format

**Output**: dialogue_with_voice.jsonl
```json
{
    "character_key": "ema",
    "emotion": "期待",
    "text": "这么晚来找我，是有什么事情吗？",
    "action": "高兴地看着hiro",
    "translation": "What brings you here so late?",
    "audio_path": "audio/ema_00000.wav",
    "audio_duration": 2.45
}
```

**Output**: dialogue_with_voice.json (full format)
```json
{
    "metadata": {
        "topic": "chatting-before-sleep",
        "style": "sfw",
        "location": "bedroom",
        "mood": "intimate",
        "timestamp": "2024-12-19T10:30:00Z",
        "characters": ["ema", "hiro"],
        "total_duration": 45.67
    },
    "dialogue": [
        {
            "turn": 0,
            "character_key": "ema",
            "emotion": "期待",
            "text": "这么晚来找我，是有什么事情吗？",
            "action": "高兴地看着hiro",
            "audio_path": "audio/ema_00000.wav",
            "audio_duration": 2.45
        },
        {
            "turn": 1,
            "character_key": "hiro",
            "emotion": "开心",
            "text": "就想来陪你啊。",
            "action": "靠近ema",
            "audio_path": "audio/hiro_00000.wav",
            "audio_duration": 1.89
        }
    ]
}
```

### 2.4 Error Handling Strategy

| Scenario | Action |
|----------|--------|
| GPT-SoVITS not running | Raise clear error: "GPT-SoVITS API not available at http://127.0.0.1:9880" |
| Character voice files missing | Raise: "Voice files not found for character: ema" (list expected paths) |
| Invalid reference audio | Raise: "Reference audio format not supported: xyz.xyz" (list supported: wav, ogg) |
| Text too long | Split text using sentence boundaries, generate separately, concatenate audio |
| API timeout | Retry up to 3 times with exponential backoff (1s, 2s, 4s) |
| Out of disk space | Log warning, skip caching (stream from memory) |

---

## 3. Implementation Roadmap

### Phase 3.1: Foundation (Day 1)
- [ ] Create voice_server/ package structure
- [ ] Implement VoiceLoader with Character-voice-example parsing
- [ ] Add VoiceConfig to models.py
- [ ] Unit tests for VoiceLoader (test path resolution, voice_setting.txt parsing)

### Phase 3.2: API Client (Day 2)
- [ ] Implement VoiceService with httpx async client
- [ ] Add health_check() and test connectivity
- [ ] Implement set_model() for loading GPT/SoVITS weights
- [ ] Implement generate_voice() with proper error handling
- [ ] Unit tests for VoiceService (mock API responses)

### Phase 3.3: Caching & Integration (Day 3)
- [ ] Implement VoiceCache with file naming strategy
- [ ] Add duration detection (soundfile or librosa)
- [ ] Create demo_voice_generation.py (end-to-end test)
- [ ] Integrate with Phase 2 real_dialogue.jsonl
- [ ] Generate dialogue_with_voice.jsonl output

### Phase 3.4: Testing & Refinement (Day 4)
- [ ] Full end-to-end test with ema and hiro voices
- [ ] Performance profiling (latency per character)
- [ ] Audio quality check (auditory testing)
- [ ] Documentation and deployment notes

---

## 4. Dependencies

**New Requirements** (add to requirements.txt):
```
httpx>=0.25.0              # Async HTTP client for API calls
soundfile>=0.12.0          # Audio file duration detection (optional)
librosa>=0.10.0            # Alternative to soundfile
pydantic>=2.0.0            # Already in Phase 1-2
pyyaml>=6.0.0              # Already in Phase 1-2
```

**System Requirements**:
- GPT-SoVITS API running on http://127.0.0.1:9880
- FFmpeg (for AAC encoding if media_type="aac")

---

## 5. Voice Settings File Format

**Example**: Character-voice-example/艾玛/GPT-SoVITS/voice_setting.txt
```
gsv_gpt_model_name=manosaba_ema-e15.ckpt
gsv_sovits_model_name=manosaba_ema_e8_s864.pth
gsv_voice_filename=good_ref/0101Adv26_Ema012.wav
gsv_voice_text=早上好。
gsv_voice_lang=zh
```

**Parsing**:
1. Read file line by line
2. Split on first `=` character
3. Extract `gsv_*` key-value pairs
4. Resolve relative paths to absolute paths in Character-voice-example/{character_key}/GPT-SoVITS/

---

## 6. Language Detection Strategy

| Text | Auto-Detection | Expected Language |
|------|----------------|--------------------|
| "早上好，艾玛。" | zh | Chinese |
| "おはよう。" | ja | Japanese |
| "Good morning." | en | English |
| "早上好。おはようございます。" | auto | Use `prompt_lang` from voice_setting |

**Implementation**: Use textblob or chardet for language detection, fallback to voice_config.prompt_lang.

---

## 7. Comparative Reference: LingChat's VoiceMaker

**LingChat Architecture** (read-only reference from third_party/LingChat):
```python
# third_party/LingChat/ling_chat/core/ai_service/voice_maker.py
class VoiceMaker:
    def check_tts_availability(self) -> dict
        # Returns: {gsv: True/False, sbv2: True/False, ...}
    
    def set_tts_settings(tts_settings: VoiceModel, name: str)
        # Load TTS provider based on tts_type (gsv, sbv2, sva-vits, etc.)
        # Resolves reference audio paths relative to character folder
        # Initializes appropriate adapter (GSVAdapter, SBv2Adapter, etc.)

# third_party/LingChat/ling_chat/core/TTS/gsv_adapter.py
class GPTSoVITSAdapter(TTSBaseAdapter):
    async def generate_voice(text: str) -> bytes
        # POST to http://127.0.0.1:9880/tts with text and voice parameters
        # Returns audio bytes
    
    async def set_model(gpt_model_path: str, sovits_model_path: str) -> bool
        # POST to /set_gpt_weights and /set_sovits_weights
```

**Key Differences in Our Implementation**:
- LingChat: Generic multi-adapter architecture (supports many TTS backends)
- Our Task 2: Focused on GPT-SoVITS only, simpler interface
- LingChat: Real character loading from dialogue context
- Our Task 2: Pre-configured character voice mappings from Character-voice-example

---

## 8. Notes on Emotion and Voice

**Important Design Decision**: 
- GPT-SoVITS does NOT support emotion-based voice synthesis
- Reference audio + reference text define the speaker's voice characteristics
- Emotion is handled by:
  1. **Dialogue text variation** (LLM generates text with emotion context)
  2. **Visual representation** (emotion tag in output JSON, separate VFX rendering)
  3. **Optional**: Speed/pitch adjustment (speed_factor parameter)

**Example**: For character "ema" with emotion "期待" (expectation):
- **Text** (from Phase 2): "这么晚来找我，是有什么事情吗？" (already emotion-aware from LLM)
- **Voice** (Phase 3): Same reference audio regardless of emotion
- **Combined Effect**: LLM-generated text + base voice = emotion impression

This is intentional and matches LingChat's architecture (VoiceMaker uses ref_audio only, emotion is text-based).

---

## 9. API Protocol Summary

```
┌─────────────────────────────────────────────────────┐
│ Phase 2: Dialogue Generation (Real LLM)             │
│ Output: real_dialogue.jsonl                          │
│ {character_key, emotion, text, action, translation} │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│ Phase 3.1: VoiceLoader                           │
│ Load from: Character-voice-example/{char}/       │
│ Output: VoiceConfig (gpt_path, sovits_path,     │
│         ref_audio, ref_text, prompt_lang)        │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│ Phase 3.2: VoiceService                          │
│ 1. POST /set_gpt_weights (load GPT model)       │
│ 2. POST /set_sovits_weights (load SoVITS model) │
│ 3. POST /tts (generate audio from text)         │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│ Phase 3.3: VoiceCache                            │
│ Save: audio/{character_key}_{seq:05d}.wav        │
│ Return: audio_path (relative to output/)         │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│ Phase 3: Output: dialogue_with_voice.jsonl       │
│ {character_key, emotion, text, action,           │
│  translation, audio_path, audio_duration}        │
└──────────────────────────────────────────────────┘
```

---

## 10. Testing Strategy

### Unit Tests
- **VoiceLoader**: Mock Character-voice-example folder, test path resolution
- **VoiceService**: Mock httpx responses, test request formatting
- **VoiceCache**: Temp directory, verify file creation and naming

### Integration Tests
- **End-to-End**: Real GPT-SoVITS API (if available), generate sample audio for ema/hiro
- **Output Validation**: Verify dialogue_with_voice.jsonl format and paths

### Manual Testing
- Listen to generated audio (ema_00000.wav, hiro_00000.wav)
- Verify audio duration matches expected speech length
- Check language detection (should be zh for Chinese text)

---

## 11. Deployment Checklist

- [ ] GPT-SoVITS API running on http://127.0.0.1:9880
- [ ] Character-voice-example folder populated with ema and hiro voices
- [ ] Phase 2 output (real_dialogue.jsonl) available
- [ ] output/audio/ directory created
- [ ] requirements.txt updated with httpx, soundfile
- [ ] VoiceLoader tested with actual voice_setting.txt files
- [ ] VoiceService tested with health_check() before full run

---

## Next Steps

1. **Implement VoiceLoader** (priority: load character voice configs correctly)
2. **Implement VoiceService** (priority: API connectivity and error handling)
3. **Implement VoiceCache** (priority: file naming and deduplication)
4. **Create demo_voice_generation.py** (priority: end-to-end validation)
5. **Integration test** with Phase 2 real_dialogue.jsonl

---

*Last Updated: 2024-12-19*
*References: third_party/GPT-SoVITS-v2pro-20250604/api_v2.py, third_party/LingChat/ling_chat/core/TTS/gsv_adapter.py*
