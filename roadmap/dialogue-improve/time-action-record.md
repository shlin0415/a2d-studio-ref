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
