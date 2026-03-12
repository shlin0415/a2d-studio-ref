# Dialogue-Voice Pipeline SOP

## Overview

End-to-end pipeline for generating character dialogue with voice synthesis.

## Pipeline Stages

### Stage 1: Dialogue Generation (Phase 1-2)
**Location:** `dialogue-server/`

1. **Load Characters**
   - Read from `Character-fig-setting-example/{character}/`
   - Parse `setting.txt` for character config
   - Extract available emotions from `fig/` folder

2. **Load Topic**
   - Read from `dialogue-topics/{topic}.md`
   - Extract metadata: style, location, mood

3. **Build Prompt**
   - Construct system prompt with dialogue format rules
   - Include character names and valid emotions

4. **Call LLM API**
   - Use DeepSeek or OpenAI API
   - Generate dialogue in format: `【emotion】text（action）<translation>`

5. **Parse & Output**
   - Extract emotion, text, action, translation
   - Save to `output/real_dialogue.jsonl`

**Command:**
```bash
cd dialogue-server
python demo_real_llm.py
```

---

### Stage 2: Voice Synthesis (Task 2)
**Location:** `voice-server/`

1. **Load Voice Config**
   - Read from `Character-voice-example/{character}/GPT-SoVITS/voice_setting.txt`
   - Get model paths: GPT (.ckpt), SoVITS (.pth)
   - Get reference audio path and text

2. **Pre-load Models (Dual Port Strategy)**
   - Port 31801: Load Ema models
   - Port 31802: Load Hiro models
   - **Critical:** Never switch models on single port

3. **Generate Voice**
   - For each dialogue line:
     - Select character port
     - Call `/tts` API
     - Save audio to `output/`

4. **Output**
   - Save audio files: `{character}_{index}.wav`
   - Save timing results to JSON

**Commands:**
```bash
# Test single port bottleneck
python test_single_port_bottleneck.py

# Test dual port performance  
python test_dual_port_performance.py

# Compare results
python compare_results.py
```

---

## Critical Rules

1. **Never use single port for multi-character** - Always use dedicated ports
2. **Always pre-load models** - Load once at startup, not per line
3. **Validate emotions against fig folder** - Only use emotions with corresponding images
4. **Save audio files** - Enable debugging and verification

---

## Test Results Summary

| Metric | Single Port | Dual Ports | Improvement |
|--------|-------------|------------|-------------|
| Total Time | 36.53s | 24.07s | 34% faster |
| Model Load | 16.58s | 3.27s | 80% reduction |

---

## File Structure

```
ref/
├── dialogue-server/
│   ├── dialogue_gen/
│   │   ├── character_loader.py
│   │   ├── prompt_builder.py
│   │   ├── dialogue_parser.py
│   │   ├── output_generator.py
│   │   └── llm_service.py
│   ├── output/
│   │   └── real_dialogue.jsonl
│   └── demo_real_llm.py
│
├── voice-server/
│   ├── test_single_port_bottleneck.py
│   ├── test_dual_port_performance.py
│   ├── compare_results.py
│   └── output/
│       ├── single_port_test_audio/
│       └── dual_port_test_audio/
│
├── Character-fig-setting-example/
│   ├── 艾玛/
│   └── 希罗/
│
├── Character-voice-example/
│   ├── 艾玛/GPT-SoVITS/
│   └── 希罗/GPT-SoVITS/
│
└── dialogue-topics/
    └── chatting-before-sleep.md
```

---

## Reference

- Template: `voice-server/test_dual_port_performance.py`
- GPT-SoVITS API: `.opencode/agents/gpt-sovits-expert.md`
