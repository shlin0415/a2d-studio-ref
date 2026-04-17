# TASK2 Quick Reference: Voice Server Implementation Guide

## TL;DR - GPT-SoVITS API

**Running**: http://127.0.0.1:9880 (local service)

**Three Endpoints**:
1. **POST /tts** → Send text + ref_audio → Get audio bytes
2. **GET /set_gpt_weights?weights_path=...** → Load GPT model
3. **GET /set_sovits_weights?weights_path=...** → Load SoVITS model

---

## Voice Data Structure

**Character Voice Config** (from voice_setting.txt):
```
Character-voice-example/
├── 艾玛/ (ema)
│   ├── GPT-SoVITS/
│   │   ├── good_ref/
│   │   │   ├── good_ref_audio.wav  ← Reference voice sample (2-3 sec)
│   │   │   └── good_ref_audio.txt  ← Text of reference: "早上好。"
│   │   ├── manosaba_ema-e15.ckpt   ← GPT weights
│   │   ├── manosaba_ema_e8_s864.pth ← SoVITS weights
│   │   └── voice_setting.txt       ← Config file
│   └── setting.txt                 (from Phase 2)
└── 希罗/ (hiro)
    ├── GPT-SoVITS/
    │   ├── good_ref/
    │   │   ├── good_ref_audio.ogg
    │   │   └── good_ref_audio.txt
    │   ├── hiro-e15.ckpt
    │   ├── hiro_e8_s2184.pth
    │   └── voice_setting.txt
    └── setting.txt
```

**voice_setting.txt Format**:
```
gsv_gpt_model_name=manosaba_ema-e15.ckpt
gsv_sovits_model_name=manosaba_ema_e8_s864.pth
gsv_voice_filename=good_ref/0101Adv26_Ema012.wav
gsv_voice_text=早上好。
gsv_voice_lang=zh
```

---

## 3-Class Architecture

### 1️⃣ VoiceLoader
**Job**: Read Character-voice-example → Extract voice configs

```python
# Usage
loader = VoiceLoader(base_path="Character-voice-example")
voice_config = await loader.load_character_voice(character)
# Returns: VoiceConfig(
#   character_key="ema",
#   gpt_model_path="/full/path/manosaba_ema-e15.ckpt",
#   sovits_model_path="/full/path/manosaba_ema_e8_s864.pth",
#   ref_audio_path="/full/path/good_ref/0101Adv26_Ema012.wav",
#   ref_text="早上好。",
#   prompt_lang="zh"
# )
```

### 2️⃣ VoiceService
**Job**: Call GPT-SoVITS API (set models, generate audio)

```python
# Usage
service = VoiceService(url="http://127.0.0.1:9880")

# Step 1: Load character models
await service.set_model(voice_config)

# Step 2: Generate audio
audio_bytes = await service.generate_voice(
    text="这么晚来找我，是有什么事情吗？",
    voice_config=voice_config,
    language="zh",
    speed_factor=1.0,
    media_type="wav"
)
# Returns: b'\x52\x49\x46\x46...' (WAV file bytes)
```

### 3️⃣ VoiceCache
**Job**: Save audio files, manage disk storage

```python
# Usage
cache = VoiceCache(cache_dir=Path("output/audio"))

# Save audio
audio_path = await cache.save_audio(
    audio_bytes=audio_bytes,
    character_key="ema",
    text="这么晚来找我，是有什么事情吗？"
)
# Returns: "audio/ema_00000.wav"

# Get duration
duration = await cache.get_audio_duration(Path("output/audio/ema_00000.wav"))
# Returns: 2.45 (seconds)
```

---

## Integration with Phase 2

**Input**: `dialogue_gen/output/real_dialogue.jsonl`
```json
{"character_key": "ema", "emotion": "期待", "text": "这么晚来找我..."}
{"character_key": "hiro", "emotion": "开心", "text": "就想来陪你啊。"}
```

**Output**: `dialogue_gen/output/dialogue_with_voice.jsonl`
```json
{"character_key": "ema", "emotion": "期待", "text": "这么晚来找我...", "audio_path": "audio/ema_00000.wav", "audio_duration": 2.45}
{"character_key": "hiro", "emotion": "开心", "text": "就想来陪你啊。", "audio_path": "audio/hiro_00000.wav", "audio_duration": 1.89}
```

---

## API Request/Response Examples

### POST /tts
**Request**:
```json
{
    "text": "早上好，艾玛。",
    "text_lang": "zh",
    "ref_audio_path": "/path/to/good_ref.wav",
    "prompt_text": "早上好。",
    "prompt_lang": "zh",
    "speed_factor": 1.0,
    "media_type": "wav"
}
```

**Response**: 
- Success (200): Binary WAV data
- Failure (400): `{"detail": "Error message"}`

### GET /set_gpt_weights
**Request**:
```
http://127.0.0.1:9880/set_gpt_weights?weights_path=/full/path/manosaba_ema-e15.ckpt
```

**Response**:
- Success (200): `"success"`
- Failure (400): `{"detail": "Model not found"}`

---

## File Naming Convention

Audio files in `output/audio/`:
```
{character_key}_{sequence:05d}.{ext}

Examples:
ema_00000.wav    (first ema line)
ema_00001.wav    (second ema line)
hiro_00000.wav   (first hiro line)
hiro_00001.wav   (second hiro line)
```

**Why this?**: Easy to match back to dialogue line using sequence number.

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| One voice per character | GPT-SoVITS voice cloning uses reference audio, not emotion-based switching |
| Don't cache duplicates | If same text occurs twice, generate separately (small perf hit, no complexity) |
| Return file paths | Caller can stream/download/process; not GPT-SoVITS's job |
| Speed factor 1.0 default | Natural speech; can override per line if needed |
| Language auto-detect | GPT-SoVITS handles "auto" well; fallback to voice_config.prompt_lang |
| Retry 3x on timeout | Transient network issues are common |

---

## Error Scenarios

| Error | Handling |
|-------|----------|
| GPT-SoVITS not running | `ConnectionError("API not available at http://127.0.0.1:9880")` |
| voice_setting.txt missing | `FileNotFoundError("Voice settings not found for ema")` |
| Reference audio format wrong | `ValueError("Expected .wav or .ogg, got .mp3")` |
| API timeout (>30s) | Retry 3x with exponential backoff (1s, 2s, 4s), then fail |
| Disk full | Log warning, continue without caching |

---

## Dependencies to Add

```bash
pip install httpx>=0.25.0 soundfile>=0.12.0
```

**What they do**:
- `httpx`: Async HTTP client (replaces requests)
- `soundfile`: Get audio duration without loading full file into memory

---

## Implementation Checklist

- [ ] Create `dialogue_gen/voice_server/` folder
- [ ] Add `VoiceConfig`, `VoiceGenerationResult` to models
- [ ] Implement `VoiceLoader` → test with ema/hiro folders
- [ ] Implement `VoiceService` → test health_check(), set_model(), generate_voice()
- [ ] Implement `VoiceCache` → test file creation and deduplication
- [ ] Create `demo_voice_generation.py` → end-to-end test
- [ ] Update `requirements.txt` with httpx, soundfile
- [ ] Run demo on Phase 2 output (real_dialogue.jsonl)
- [ ] Generate `dialogue_with_voice.jsonl`
- [ ] Listen to audio samples (ema_00000.wav, hiro_00000.wav)
- [ ] Git commit Phase 3 code

---

## Quick Start Command

```bash
# 1. Start GPT-SoVITS API (in separate terminal)
cd third_party/GPT-SoVITS-v2pro-20250604
python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml

# 2. Run Phase 3 demo
cd dialogue-server
python demo_voice_generation.py
```

---

## LingChat Reference

If you need to check LingChat's implementation for reference:
- VoiceMaker: `third_party/LingChat/ling_chat/core/ai_service/voice_maker.py`
- GPT-SoVITS Adapter: `third_party/LingChat/ling_chat/core/TTS/gsv_adapter.py`

(Read-only reference only - don't modify third_party/)

---

*Quick reference for Phase 3 voice server implementation*
*Full details in TASK2_ANALYSIS.md*
