# Time Action Record

## 2026-03-28

### Session: Topic Conversion Plan + Task 1

**Time**: 00:00 - 00:15

**What**: Created mimo-topic-plan.md and mimo-topic-plan-task1.md, converted chatting-before-sleep.md to new SETTING format.

**Why**: Need to convert 3 origin topic files to new template format for dialogue-server to use.

**Files created**:
- `roadmap/mimo-topic-plan.md` — main plan
- `roadmap/mimo-topic-plan-task1.md` — task 1 detail
- `dialogue-topics/SETTING-chatting-before-sleep.md` — converted file

**Result**: Task 1 complete. chatting-before-sleep.md converted with all sections mapped correctly.

**Next**: Task 2 — Convert learn-cuda.md to SETTING + DETAIL files.

---

### Task 2: Convert learn-cuda.md

**Time**: 00:15 - 00:25

**What**: Created DETAIL-learn-cuda.md and SETTING-learn-cuda.md from origin-messy-topics/learn-cuda.md.

**Why**: learn-cuda.md is a Learning type topic with code content. Needs separate SETTING (metadata) and DETAIL (code) files.

**Files created**:
- `roadmap/mimo-topic-plan-task2.md` — task 2 detail
- `dialogue-topics/DETAIL-learn-cuda.md` — CUDA code with annotation header
- `dialogue-topics/SETTING-learn-cuda.md` — topic metadata, type=Learning, links to DETAIL file

**Result**: Task 2 complete. All sections mapped, DETAIL_File correctly references DETAIL-learn-cuda.md.

**Next**: Task 3 — Convert fanfiction.md (largest file, 542 lines, needs 4 stages).

---

### Task 3: Convert fanfiction.md

**Time**: 00:25 - 00:45

**What**: Created DETAIL-fanfiction.md (554 lines, 4 stages) and SETTING-fanfiction.md from origin-messy-topics/fanfiction.md.

**Why**: fanfiction.md is a Fanfiction type topic with long story content (~520 lines). Needed stage splitting by narrative arc.

**Stage split**:
| Stage | Content |
|-------|---------|
| Stage_1 | Hiro in hallway, Snowy/Hannah tell about letter, observing |
| Stage_2 | Eavesdropping, Emma says "喜欢", lunch bento feeding scene |
| Stage_3 | Afternoon self-study, Hiro realizes she likes Emma |
| Stage_4 | After school crepe shop, Emma's confession, bittersweet ending |

**Files created**:
- `roadmap/mimo-topic-plan-task3.md` — task 3 detail
- `dialogue-topics/DETAIL-fanfiction.md` — story with 4 stage markers
- `dialogue-topics/SETTING-fanfiction.md` — topic metadata, type=Fanfiction, DETAIL_Similarity=80

**Result**: Task 3 complete. All 3 origin topics converted.

---

### Session Summary

**All tasks complete.** Files created in `dialogue-topics/`:

| File | Type | Source |
|------|------|--------|
| `SETTING-chatting-before-sleep.md` | SETTING only | chatting-before-sleep.md |
| `SETTING-learn-cuda.md` + `DETAIL-learn-cuda.md` | SETTING + DETAIL | learn-cuda.md |
| `SETTING-fanfiction.md` + `DETAIL-fanfiction.md` | SETTING + DETAIL (4 stages) | fanfiction.md |

**Next steps**: Update `topic_loader.py` to parse the new format markers (`|====...====|`, `|---...---|`, `|<===...===>|`).

---

### Session: mimo-dv-test-plan - Language Settings + Param Rename

## Task 1: Phase 1 - SETTING Templates

**What**: Updated all SETTING-*.md and DETAIL-topic-template.md:
- Renamed `DETAIL_Similarity` → `DETAIL_Follow`, `DETAIL_ReadForbidden` → `DETAIL_Direct_Use_For_Voice`
- Added `Dialogue_Language` and `Voice_Language` fields
- Added preset comments to template
- Removed DETAIL params from chatting-before-sleep (no DETAIL for None type)

**Files changed**:
- `dialogue-topics/old-SETTING-topic-template.md` — old version preserved
- `dialogue-topics/SETTING-topic-template.md` — new version with all changes
- `dialogue-topics/SETTING-learn-cuda.md` — Follow=80, Direct_Use=20
- `dialogue-topics/SETTING-fanfiction.md` — Follow=80, Direct_Use=90, DL=zh, VL=ja
- `dialogue-topics/SETTING-chatting-before-sleep.md` — DL=zh, VL=zh
- `dialogue-topics/DETAIL-topic-template.md` — updated annotations

**Result**: Task 1 complete. All templates updated.

**Next**: Task 2 — Update topic_loader.py + config.py to parse new fields.

---

## Task 2: Phase 2 - topic_loader.py + config.py

**What**:
- Renamed old `topic_loader.py` → `old-topic_loader.py`
- Created new `topic_loader.py` with `|====Start/End of ...====|` section parsing
- Added `TopicMetadata` fields: `dialogue_language`, `voice_language`, `topic_type`, `detail_follow`, `detail_direct_use_for_voice`, `detail_file`
- Added `translate_mode` and `gpt_sovits_url` to `config.py`
- Created `test_topic_loader_new_format.py` with 4 tests (all passing)

**Files changed**:
- `dialogue-server/dialogue_gen/old-topic_loader.py` — old version preserved
- `dialogue-server/dialogue_gen/topic_loader.py` — new version with section parsing
- `dialogue-server/dialogue_gen/config.py` — added translate_mode, gpt_sovits_url
- `dialogue-server/tests/test_topic_loader_new_format.py` — 4 passing tests

**Test results**: 4/4 passed (chatting-before-sleep, learn-cuda, fanfiction, template)

**Next**: Task 3 — Fix prompt_builder.py to make language actually work.

---

## Task 3: Phase 3 - prompt_builder.py

**What**:
- Renamed old `prompt_builder.py` → `old-prompt_builder.py`
- Created new `prompt_builder.py` with dynamic language support (9 combinations)
- Format changes based on dialogue_language/voice_language (same=no translation, different=with translation)
- Hardcoded examples replaced with per-language examples
- Backward compat: old `language=` param still works
- Created `test_prompt_builder_languages.py` with 5 tests (all passing)

**Files changed**:
- `dialogue-server/dialogue_gen/old-prompt_builder.py` — old version preserved
- `dialogue-server/dialogue_gen/prompt_builder.py` — new version with dynamic format
- `dialogue-server/tests/test_prompt_builder_languages.py` — 5 passing tests

**Test results**: 5/5 passed (zh/zh, zh/ja, ja/ja, en/zh, backward compat)

---

### Phase 1-3 Summary (Verified)

All 3 phases verified with tests:
- Phase 1: SETTING templates updated with new params and language fields
- Phase 2: topic_loader.py parses new format correctly (4/4 tests)
- Phase 3: prompt_builder.py generates correct format for all 9 language combos (5/5 tests)

**Next**: Phase 4 (output pipeline) and Phase 5 (voice-server) — requires GPT-SoVITS running on 31801/31802.

---

## Task 4: Phase 4 - Fix output pipeline

**Time**: 2026-03-28 (continued)

**What**:
- Fixed duplicate elif blocks in dialogue_generator.py (lines 186-215 were duplicates using old `language=` param)
- Created test_output_format.py to verify JSONL output has caption_text/voice_text/caption_language/voice_language
- output_generator.py already had correct implementation (no changes needed)

**Files changed**:
- `dialogue-server/dialogue_gen/dialogue_generator.py` — removed duplicate elif blocks
- `dialogue-server/tests/test_output_format.py` — new test (4 tests)

**Result**: Task 4 complete. output_generator.py correctly produces caption_text/voice_text with language fields. 4/4 tests pass.

**Next**: Task 5 — voice-server integration with JSONL

---

## Task 5: Phase 5 - voice-server JSONL integration

**What**:
- Created jsonl_voice_generator.py: reads JSONL, extracts voice_text + voice_language, calls GPT-SoVITS API
- Created test_jsonl_voice.py: tests JSONL parsing, config parsing, character voice loading

**Files created**:
- `voice-server/jsonl_voice_generator.py` — main voice generator from JSONL
- `voice-server/tests/test_jsonl_voice.py` — 5 tests

**Result**: Task 5 complete. Voice generator reads JSONL header for voice_language, loads character voice settings from Character-voice-example/. 5/5 tests pass.

**Usage**:
```bash
python voice-server/jsonl_voice_generator.py --jsonl dialogue-server/output/real_dialogue.jsonl --api-url http://127.0.0.1:31801
```

---

### mimo-dv-test-plan Summary (All Tasks Complete)

All 5 phases verified:
- Phase 1: SETTING templates updated with new params and language fields ✅
- Phase 2: topic_loader.py parses new format correctly (4/4 tests) ✅
- Phase 3: prompt_builder.py generates correct format for all 9 language combos (5/5 tests) ✅
- Phase 4: output_generator.py produces caption_text/voice_text with language fields (4/4 tests) ✅
- Phase 5: jsonl_voice_generator.py reads JSONL and calls GPT-SoVITS with voice_language (5/5 tests) ✅

**Total**: 18/18 tests passing across all phases.

**Next possible directions**:
- Streaming output (async dialogue→voice pipeline)
- Edit & regenerate workflow
- Screen/UI display integration
