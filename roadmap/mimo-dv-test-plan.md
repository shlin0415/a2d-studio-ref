# mimo-dv-test-plan: Dialogue/Voice Language Settings + Parameter Rename

## Goal
1. Rename `DETAIL_Similarity` → `DETAIL_Follow`, `DETAIL_ReadForbidden` → `DETAIL_Direct_Use_For_Voice`
2. Add `Dialogue_Language` and `Voice_Language` settings (3x3 = 9 combinations: zh, en, ja)
3. Fix code so language actually works (prompt_builder.py currently hardcoded)
4. Update output format with `caption_text` and `voice_text`
5. Update voice-server to use `Voice_Language`

## Approach
Option 2: Phase 1-3 first, verify, then Phase 4-5.

## Tasks

### Task 1: Phase 1 - SETTING Templates (.md files)
- Rename params in all SETTING-*.md and DETAIL-topic-template.md
- Add `Dialogue_Language`, `Voice_Language` fields
- Add preset comments
- No code changes, no risk

### Task 2: Phase 2 - topic_loader.py + config.py
- Parse new fields from SETTING files
- Add `TopicMetadata` fields
- Add `Translate_Mode` to config.py
- Rename old files to old-*, create new files
- Write test to verify parsing

### Task 3: Phase 3 - prompt_builder.py
- Make language dynamic (currently hardcoded Chinese+Japanese)
- 9 format combinations
- Write test to verify prompts change with language

### Task 4: Phase 4 - output_generator.py + dialogue_generator.py
- Add `caption_text`, `voice_text`, `caption_language`, `voice_language` to output
- Pass language from TopicMetadata through pipeline

### Task 5: Phase 5 - voice-server
- Read `voice_language` from JSONL header
- Remove hardcoded `text_language="zh"` in test files
- Test with GPT-SoVITS on port 31801/31802

## Rules
- Prefer rename old files to old-*, create new files
- Git commit every small edit
- Record to time-action-record.md
- Each task independently testable
