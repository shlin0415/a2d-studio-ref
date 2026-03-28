# Time Action Record - Dialogue Improve

## Task A1: Rename old v1.0 output files

**Time**: 2026-03-29, start ~current

**What**: Renamed 6 old output files in `dialogue-server/output/` to `old-*` prefix.

**Files renamed**:
- `demo_dialogue.jsonl` → `old-demo_dialogue.jsonl`
- `demo_dialogue.json` → `old-demo_dialogue.json`
- `demo_dialogue.txt` → `old-demo_dialogue.txt`
- `real_dialogue.jsonl` → `old-real_dialogue.jsonl`
- `real_dialogue.json` → `old-real_dialogue.json`
- `real_dialogue.txt` → `old-real_dialogue.txt`

**Why**: Old files are v1.0 format with hardcoded `"language": "zh"` (singular), missing `dialogue_language`, `voice_language`, `caption_text`, `voice_text`. Incompatible with new v2.0 pipeline.

**Result**: All 6 files renamed successfully. `dialogue-server/output/` now contains only `old-*` files and `voice/` directory.

**Next**: Task A2 — Clean DialogueLine model (remove `text_jp`, add `translation_text`)

---

## Tasks A2-A6: Output Format Cleanup

**Time**: 2026-03-29, continued

**What**: Removed `text_jp` from the entire codebase and replaced with `translation_text`.

**Files modified**:
- `dialogue-server/dialogue_gen/core/models.py` — `text_jp` → `translation_text` in DialogueLine
- `dialogue-server/dialogue_gen/dialogue_parser.py` — parser writes to `translation_text`
- `dialogue-server/dialogue_gen/output_generator.py` — removed `text_jp` from output dict, added `topic_type` to header, voice_text uses `translation_text`
- `voice-server/jsonl_voice_generator.py` — removed `text_jp` from dataclass and parser
- `dialogue-server/demo_real_llm.py` — updated to use `translation_text`
- `dialogue-server/quick_start.py` — updated to use `translation_text`
- `dialogue-server/tests/test_output_format.py` — updated test data
- `dialogue-server/tests/test_components.py` — updated test data
- `voice-server/tests/test_jsonl_voice.py` — removed `text_jp` from test JSON

**Why**: `text_jp` was hardcoded to assume Japanese. The new `translation_text` field is generic — it holds whatever the LLM translated, regardless of target language. The output generator maps it to `voice_text` based on the configured `voice_language`.

**Test results**: All tests pass:
- test_topic_loader_new_format.py: 4/4 ✅
- test_output_format.py: 4/4 ✅
- test_prompt_builder_languages.py: 5/5 ✅
- test_jsonl_voice.py: 5/5 ✅

**Next**: Part B — Pipeline Integration (topic_loader, prompt_builder, dialogue_generator)

---

## Part B: Pipeline Integration

### Task B1: Update topic_loader.py — Load DETAIL content + stages
