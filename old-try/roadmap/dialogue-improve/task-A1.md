# Task A1: Rename old v1.0 output files

## Goal
Rename old output files to `old-*` prefix to preserve them as reference while
clearing the way for new v2.0 format outputs.

## Files to rename
- `dialogue-server/output/demo_dialogue.jsonl` → `old-demo_dialogue.jsonl`
- `dialogue-server/output/demo_dialogue.json` → `old-demo_dialogue.json`
- `dialogue-server/output/demo_dialogue.txt` → `old-demo_dialogue.txt`
- `dialogue-server/output/real_dialogue.jsonl` → `old-real_dialogue.jsonl`
- `dialogue-server/output/real_dialogue.json` → `old-real_dialogue.json`
- `dialogue-server/output/real_dialogue.txt` → `old-real_dialogue.txt`

## Why
- Old files use v1.0 format with hardcoded `"language": "zh"` (singular)
- Missing `dialogue_language`, `voice_language`, `caption_text`, `voice_text`
- Incompatible with voice-server parser and new pipeline
