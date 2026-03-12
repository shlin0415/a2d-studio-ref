# GPT-SoVITS Expert

## Domain: Voice Synthesis / TTS

### Key Findings: Model Switching Bottleneck

**The Hidden Trap:**
When using a single GPT-SoVITS port (9880) for multi-character voice generation, switching between characters requires reloading both GPT and SoVITS models (~1.8s per switch). This creates significant overhead for alternating dialogue.

**Evidence:**
```
Single Port (9880) - Model Switching:
- Total time: 36.53s
- Model load: 16.58s (45% of total time)
- Generation: 19.95s

Dual Ports (31801/31802) - No Switching:
- Total time: 24.07s  
- Model load: 3.27s (one-time setup)
- Generation: 20.79s
```

**The Breakthrough:**
Use dedicated ports per character:
- Port 31801: Pre-load Ema models once
- Port 31802: Pre-load Hiro models once
- Result: 34.1% faster (12.46s saved)

---

## Critical Requirements

1. **Never use single port for multi-character dialogue** - Always use dedicated ports per character
2. **Pre-load models at startup** - Load all character models before dialogue generation
3. **Cache audio files** - Save generated audio to avoid regeneration

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/tts` | POST | Generate speech from text |
| `/set_gpt_weights` | GET/POST | Load GPT model (.ckpt) |
| `/set_sovits_weights` | GET/POST | Load SoVITS model (.pth) |

---

## Test Scripts

| Script | Purpose |
|--------|---------|
| `test_single_port_bottleneck.py` | Measure single port switching overhead |
| `test_dual_port_performance.py` | Measure dual port performance |
| `compare_results.py` | Compare and analyze results |

---

## File References

- Test scripts: `voice-server/test_*.py`
- Character voice config: `Character-voice-example/{character}/GPT-SoVITS/voice_setting.txt`
- Dialogue output: `dialogue-server/output/real_dialogue.jsonl`
