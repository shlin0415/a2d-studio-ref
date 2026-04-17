# Task 4: Phase 4 - Update output pipeline

## Goal
1. Update `output_generator.py` to add `caption_text`, `voice_text`, `caption_language`, `voice_language` to JSONL output
2. Update `dialogue_generator.py` to pass language from TopicMetadata to prompt_builder and output_generator
3. Write test to verify output format

## JSONL output format change
Old per line:
```json
{"index": 0, "character": "艾玛", "text": "这么晚来找我", "text_jp": "こんな遅くに"}
```

New per line:
```json
{"index": 0, "character": "艾玛", "text": "这么晚来找我", "caption_text": "这么晚来找我", "voice_text": "こんな遅くに", "caption_language": "zh", "voice_language": "ja"}
```

Header change:
```json
{"header": {"dialogue_language": "zh", "voice_language": "ja", ...}}
```

## Approach
- Rename old output_generator.py → old-output_generator.py, create new
- Edit dialogue_generator.py to pass language params
- Write test

## Files
| File | Action |
|------|--------|
| `dialogue_gen/output_generator.py` | Rename to old, create new |
| `dialogue_gen/dialogue_generator.py` | Edit to pass language |
| `tests/test_output_format.py` | New test |
