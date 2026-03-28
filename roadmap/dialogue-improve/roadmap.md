# Dialogue Improve Plan

## Goal
Test the three types of topic.md in `dialogue-topics/` with the new dialogue server,
using real LLM API calls. Fix output format to remove hardcoded `text_jp` and use
proper `caption_text`/`voice_text` with dynamic language from SETTING metadata.

## Part A: Output Format Cleanup

### A1: Rename old v1.0 output files
- `dialogue-server/output/demo_dialogue.*` → `old-demo_dialogue.*`
- `dialogue-server/output/real_dialogue.*` → `old-real_dialogue.*`
- These are v1.0 format with hardcoded `"language": "zh"`, no longer match new server

### A2: Clean DialogueLine model (`models.py`)
- Remove `text_jp: Optional[str]` field
- Add `translation_text: Optional[str] = None` field

### A3: Update Dialogue Parser (`dialogue_parser.py`)
- Line 131: `text_jp=translation` → `translation_text=translation`

### A4: Update Output Generator (`output_generator.py`)
- Remove `text_jp` from output dict in `_dialogue_line_to_dict()`
- voice_text logic: same-lang → `line.text`, diff-lang → `line.translation_text`
- Add `topic_type` to header

### A5: Update Voice Server Parser (`jsonl_voice_generator.py`)
- Remove `text_jp` from `DialogueLine` dataclass
- Update fallback: `voice_text=d.get("voice_text", d.get("text", ""))`

### A6: Fix all tests
- Update any `text_jp` references to `translation_text`

## Part B: Pipeline Integration

### B1: Update Topic Loader (`topic_loader.py`)
- `_load_detail_file()`: Read DETAIL content into `metadata.detail_content`
- Add `_parse_stages()` → `metadata.stages: Dict[str, str]`

### B2: Update Prompt Builder (`prompt_builder.py`)
- Add `build_system_prompt_from_metadata()` method
- Topic-type instructions: None (free), Learning (discuss concepts), Fanfiction (follow story)
- Include DETAIL content in prompt
- Remove hardcoded max_sentences constraint

### B3: Update Dialogue Generator (`dialogue_generator.py`)
- Add `generate_from_topic_file()` method
- Connect TopicLoader → PromptBuilder → LLM → Parser → OutputGenerator

## Part C: Testing

### C1: Create `test_three_topics.py`
- Test 1: SETTING-chatting-before-sleep.md (None, zh→zh)
- Test 2: SETTING-learn-cuda.md (Learning, zh→zh)
- Test 3: SETTING-fanfiction.md Stage_1 (Fanfiction, zh→ja)

## Execution Order
```
A1 → A2 → A3 → A4 → A5 → A6 → B1 → B2 → B3 → C1
```
