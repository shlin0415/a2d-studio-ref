# GPT-SoVITS Integration Investigation Summary

## Investigation Scope
**Goal**: Understand how LingChat and SillyTavern integrate with GPT-SoVITS for voice synthesis.
**Duration**: Cross-referenced third_party/ sources and existing character-voice-example structure
**Findings**: Complete API specification, architecture patterns, character voice mapping system

---

## Key Findings

### 1. GPT-SoVITS API Architecture

**Service**: Local HTTP API
- **URL**: http://127.0.0.1:9880 (configurable)
- **Type**: RESTful JSON API with binary audio response
- **Framework**: FastAPI with Uvicorn

**Three Core Endpoints**:

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/tts` | POST | Generate speech from text | ✅ Primary |
| `/set_gpt_weights` | GET/POST | Load GPT model weights | ✅ Required |
| `/set_sovits_weights` | GET/POST | Load SoVITS model weights | ✅ Required |

### 2. TTS Request Structure

**Mandatory Fields**:
```json
{
    "text": "早上好，艾玛。",          # Text to synthesize
    "text_lang": "zh",              # Target language (zh/en/ja/yue/ko/auto)
    "ref_audio_path": "/path.wav",  # Reference audio for voice cloning
    "prompt_lang": "zh"             # Reference text language
}
```

**Optional Parameters** (for fine-tuning):
- `speed_factor` (float): 0.5 = slow, 2.0 = fast (default: 1.0)
- `temperature` (float): Sampling randomness (default: 1.0)
- `top_k`, `top_p` (int/float): Sampling parameters
- `media_type` (str): Output format - "wav", "ogg", "aac", "raw" (default: "wav")
- `streaming_mode` (bool): Chunk-by-chunk response (default: false)

### 3. Character Voice Mapping System

**Structure** (from Character-voice-example):
```
Character-voice-example/
├── 艾玛 (Ema) → Character.character_key = "ema"
│   └── GPT-SoVITS/
│       ├── good_ref/
│       │   ├── 0101Adv26_Ema012.wav
│       │   └── 0101Adv26_Ema012.txt
│       ├── manosaba_ema-e15.ckpt
│       ├── manosaba_ema_e8_s864.pth
│       └── voice_setting.txt
└── 希罗 (Hiro) → Character.character_key = "hiro"
    └── GPT-SoVITS/
        ├── good_ref/
        │   ├── 0204Adv10_Hiro006.ogg
        │   └── 0204Adv10_Hiro006.txt
        ├── hiro-e15.ckpt
        ├── hiro_e8_s2184.pth
        └── voice_setting.txt
```

**Key Pattern**: 
- Chinese folder names (艾玛, 希罗) map to character_key (ema, hiro)
- Voice settings are per-character, not per-emotion
- Reference audio + text = voice fingerprint for cloning

### 4. Voice Setting File Format

**File**: Character-voice-example/{character}/GPT-SoVITS/voice_setting.txt

**Content** (key=value format):
```
gsv_gpt_model_name=manosaba_ema-e15.ckpt
gsv_sovits_model_name=manosaba_ema_e8_s864.pth
gsv_voice_filename=good_ref/0101Adv26_Ema012.wav
gsv_voice_text=早上好。
gsv_voice_lang=zh
```

**Parsing**:
- Line-by-line: key=value
- Prefix: `gsv_` (GPT-SoVITS)
- Paths are relative to Character-voice-example/{character}/GPT-SoVITS/
- Paths must be resolved to absolute paths for API calls

### 5. LingChat Reference Architecture

**VoiceMaker** (ling_chat/core/ai_service/voice_maker.py):
- Manages TTS provider selection and initialization
- Supports multiple backends: gsv, sbv2, sva-vits, sbv2api, aivis, bv2
- Checks availability: `check_tts_availability()` → dict of bool
- Loads settings: `set_tts_settings(tts_settings: VoiceModel, name: str)`
- Initializes adapter based on tts_type field

**GPTSoVITSAdapter** (ling_chat/core/TTS/gsv_adapter.py):
- Class: `GPTSoVITSAdapter(TTSBaseAdapter)`
- Uses `httpx` for async HTTP client
- Two key methods:
  1. `async set_model(gpt_model_path: str, sovits_model_path: str) → bool`
  2. `async generate_voice(text: str) → bytes`
- Inherits from `TTSBaseAdapter` (base interface pattern)

### 6. Model File Types

| File Type | Purpose | Example | Load Endpoint |
|-----------|---------|---------|----------------|
| `.ckpt` | GPT weights | manosaba_ema-e15.ckpt | /set_gpt_weights |
| `.pth` | SoVITS weights | manosaba_ema_e8_s864.pth | /set_sovits_weights |
| `.wav` | Reference audio | good_ref/0101Adv26_Ema012.wav | /tts (ref_audio_path) |
| `.ogg` | Reference audio | good_ref/0204Adv10_Hiro006.ogg | /tts (ref_audio_path) |
| `.txt` | Reference text | good_ref/0101Adv26_Ema012.txt | /tts (prompt_text) |

### 7. Supported Languages

**GPT-SoVITS Language Codes**:
- `zh` - Chinese (Simplified/Traditional)
- `en` - English
- `ja` - Japanese
- `yue` - Cantonese
- `ko` - Korean
- `auto` - Auto-detect from input text

**Detection Strategy**:
- Primary: Use `text_lang` parameter with specific code
- Fallback: Use `auto` for language auto-detection
- Reference language: `prompt_lang` (from voice_setting.txt usually "zh")

### 8. Error Response Format

**Success (HTTP 200)**:
```
Binary audio stream (WAV/OGG/AAC/RAW)
```

**Failure (HTTP 400)**:
```json
{
    "detail": "Error message describing the issue"
}
```

**Common Errors**:
- Model not found: "weights_path not found"
- Invalid text: "text is empty"
- Audio format not supported: "ref_audio_path format not supported"
- API timeout: (httpx TimeoutError)

### 9. Audio Output Formats

**Supported by media_type parameter**:

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| `wav` | Default | Uncompressed, widely supported | Large file size |
| `ogg` | Web/streaming | Small file size, good quality | Requires OGG decoder |
| `aac` | Mobile | Small file size, widely supported | Requires FFmpeg |
| `raw` | Internal | Minimal overhead | No container, just PCM data |

**Recommendation**: Use `wav` for local caching (simplest), `ogg` for streaming.

### 10. Performance Characteristics

**From test logs** (third_party/GPT-SoVITS-v2pro-20250604-run.md):

| Metric | Value | Notes |
|--------|-------|-------|
| Model load time | 2-5 sec | One-time cost per model |
| Short text (早上好。) | 0.3-0.5 sec | 2-3 word phrase |
| Medium text | 1-3 sec | Normal dialogue line |
| Long text | 5-10 sec | Paragraph-length text |
| Batch inference | 2x faster | Parallel_infer=true (default) |

**Optimization**:
- Load models once per character, not per line
- Keep models in memory during multi-line generation
- Use `parallel_infer=true` (default) for multi-line batching

### 11. Integration Points

**Phase 2 → Phase 3 Data Flow**:
```
Phase 2: real_dialogue.jsonl
├── character_key: "ema" | "hiro"
├── text: "这么晚来找我，是有什么事情吗？"
├── emotion: "期待" (for visual FX, not voice)
└── ...

Phase 3 Processing:
├── VoiceLoader: Load character voice config
├── VoiceService: Call GPT-SoVITS API
├── VoiceCache: Save audio file
└── Output: dialogue_with_voice.jsonl
    ├── audio_path: "audio/ema_00000.wav"
    ├── audio_duration: 2.45
    └── ... (all Phase 2 fields)
```

### 12. Deployment Requirements

**Software**:
- Python 3.8+ (for async/await)
- HTTPx library (async HTTP)
- soundfile or librosa (audio duration detection)
- FFmpeg (optional, for AAC format)

**Hardware**:
- GPU recommended (NVIDIA CUDA)
- Disk: ~2GB for model weights per character
- Memory: ~2GB RAM minimum

**Network**:
- Local API communication (low latency)
- No internet required (fully local)

---

## Investigation Sources

| Source | Type | Key Content |
|--------|------|-------------|
| third_party/GPT-SoVITS-v2pro-20250604/api_v2.py | API Code | Complete endpoint documentation, request/response models, error handling |
| third_party/GPT-SoVITS-v2pro-20250604-run.md | Log | Real execution example showing model loading and inference |
| Character-voice-example/ | Data | Actual character voice structure and file organization |
| third_party/LingChat/ling_chat/core/TTS/gsv_adapter.py | Reference | Async HTTP client pattern for GPT-SoVITS API |
| third_party/LingChat/ling_chat/core/ai_service/voice_maker.py | Reference | TTS provider management and initialization |

---

## Design Patterns Identified

### Pattern 1: Adapter Pattern (TTS)
```python
class TTSBaseAdapter:
    async def generate_voice(text: str) -> bytes
    async def set_model(...) -> bool

class GPTSoVITSAdapter(TTSBaseAdapter):
    # Implements GPT-SoVITS-specific logic

class SBv2Adapter(TTSBaseAdapter):
    # Implements SoftVITS-v2-specific logic
```

**Implication**: Multiple TTS backends can be swapped without changing interface.

### Pattern 2: Configuration via Voice Settings
```
Character folder structure → voice_setting.txt → VoiceConfig
```

**Benefit**: Easy to switch voice models, add new characters, or tweak parameters.

### Pattern 3: Reference Audio Cloning
```
ref_audio + ref_text → voice fingerprint → apply to new text
```

**Benefit**: Don't need to train models per character; use existing voices.

---

## Constraints & Limitations

| Constraint | Impact | Workaround |
|-----------|--------|-----------|
| One model pair per character | Must load new models for each character | Pre-load all characters' models on startup |
| No real-time emotion control | Emotion conveyed via LLM text only | Generate text variations for emotions |
| Reference audio length (2-3 sec) | Too short affects voice quality | Use high-quality recordings |
| API runs locally only | No cloud inference | Deploy GPT-SoVITS service on same/nearby server |
| Model size (~1GB per character) | Disk and memory overhead | Use smaller models if available |

---

## Investigation Conclusions

1. **✅ API is mature**: FastAPI-based, well-documented, production-ready
2. **✅ Character voice mapping is clear**: voice_setting.txt provides standardized config
3. **✅ Integration is straightforward**: Three endpoints cover all needs (set models, generate)
4. **✅ Performance is acceptable**: 0.3-3 sec per line, cacheable
5. **✅ Architecture is extensible**: LingChat's adapter pattern can be reused
6. **⚠️ Local-only deployment**: Requires GPT-SoVITS API running on same machine
7. **⚠️ No emotion-based synthesis**: Voice is character-level, not emotion-level

---

## Next Steps (Phase 3 Implementation)

1. **VoiceLoader**: Parse voice_setting.txt and resolve paths
2. **VoiceService**: Build async HTTPx client for API calls
3. **VoiceCache**: Manage output/audio/ file storage
4. **Integration**: Connect to Phase 2 dialogue output
5. **Testing**: Generate dialogue_with_voice.jsonl with real audio

---

*Investigation completed: 2024-12-19*
*Status: Ready for Phase 3 implementation*
*Reference: TASK2_ANALYSIS.md, TASK2_QUICK_REFERENCE.md*
