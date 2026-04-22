# Task 2: Phase 2 - topic_loader.py + config.py

## Goal
1. Update `topic_loader.py` to parse new SETTING fields:
   - `Dialogue_Language`, `Voice_Language`
   - `DETAIL_Follow`, `DETAIL_Direct_Use_For_Voice`
   - `TOPIC_Type`
2. Update `config.py` to add `translate_mode`
3. Write test to verify parsing

## Approach
- Rename old topic_loader.py → old-topic_loader.py
- Create new topic_loader.py with new parsing logic
- Add new fields to TopicMetadata
- Write test file

## Files to change
| File | Action |
|------|--------|
| `dialogue_gen/topic_loader.py` | Rename to old-topic_loader.py, create new |
| `dialogue_gen/config.py` | Add translate_mode property |
| `tests/test_topic_loader_new_format.py` | New test file |

## TopicMetadata new fields
```python
dialogue_language: str = "zh"
voice_language: str = "zh"
topic_type: str = "None"
detail_follow: int = 80
detail_direct_use_for_voice: int = 0
detail_file: Optional[str] = None
```

## Test plan
- Load SETTING-chatting-before-sleep.md → verify DL=zh, VL=zh, type=None
- Load SETTING-learn-cuda.md → verify DL=zh, VL=zh, type=Learning, Follow=80, Direct=20
- Load SETTING-fanfiction.md → verify DL=zh, VL=ja, type=Fanfiction, Follow=80, Direct=90
