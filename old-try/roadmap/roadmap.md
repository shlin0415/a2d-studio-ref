# a2d-studio Roadmap

## Part 1: What Have Been Done (Task1 + Task2)

### Template Update (2026-03-25) 🆕
**New Topic Template Format**: We have finalized the special symbol design for topic templates.

| Symbol Type | Start | End |
|-------------|-------|-----|
| Metadata | `|---Field: value---|` | - |
| Section | `|====Start of Name====|` | `|====End of Name====|` |
| Stage | `|<===Start of Stage_N===>|` | `|<===End of Stage_N===>|` |

**Files Created**:
- [`dialogue-topics/template.md`](dialogue-topics/template.md) - New standard template with examples
- [`dialogue-topics/format-chatting-before-sleep.md`](dialogue-topics/format-chatting-before-sleep.md) - Converted from old format
- [`dialogue-topics/format-fanfiction.md`](dialogue-topics/format-fanfiction.md) - Converted with 4 stages
- [`dialogue-topics/format-learn-cuda.md`](dialogue-topics/format-learn-cuda.md) - Converted with ReadForbidden

---

### Task 1: Dialogue Generation Server ✅
**Location**: `dialogue-server/`

**Core Components**:
| Component | File | Status |
|-----------|------|--------|
| Character Loader | `dialogue_gen/character_loader.py` | ✅ Working |
| Prompt Builder | `dialogue_gen/prompt_builder.py` | ✅ Working |
| LLM Service | `dialogue_gen/llm_service.py` | ✅ Working |
| Dialogue Parser | `dialogue_gen/dialogue_parser.py` | ✅ Working |
| Output Generator | `dialogue_gen/output_generator.py` | ✅ Working |
| Main Orchestrator | `dialogue_gen/dialogue_generator.py` | ✅ Working |

**Output**: `dialogue-server/output/real_dialogue.jsonl`
```json
{"index": 0, "character": "艾玛", "emotion": "期待", "text": "这么晚来找我，是有什么事情吗？", "action": "高兴地看着希罗", "text_jp": "...")
```

### Task 2: Voice Generation Server ⚠️
**Location**: `voice-server/`

**Demo Working**: `demo_gpt_sovits_voice.py` can generate audio for:
- Character: 艾玛 (Ema), 希罗 (Hiro)
- Languages: Chinese, English, Japanese

**Issue**: Not integrated with dialogue-server output yet.

---

## Part 2: Proposed Improvements Analysis

From `roadmap-after-task1-task2.md`:

| # | Improvement | Description | Priority |
|---|-------------|-------------|----------|
| 1 | Topic Template | Standardize topic format | **HIGH** |
| 2 | Topic Types | Support 4 types of topics | **HIGH** |
| 3 | Streaming Output | Async dialogue→voice pipeline | **HIGH** |
| 4 | Edit & Regenerate | User editing + voice regeneration | MEDIUM |
| 5 | Screen/UI | Display characters on screen | MEDIUM |
| 6 | Split & Resize | Page splitting for screen | LOW |

---

## Part 3: Recommended Order & Implementation Plans

### Phase 1: Foundation (Weeks 1-2) - Must Do First

#### 1.1 Topic Template System 🔴 FIRST PRIORITY

**Why first**: Everything depends on having a clear topic format.

**Current state**: Topics in `dialogue-topics/` have no standard structure.

**New Template Format** (from `dialogue-topics/template.md`):

The new template uses special markers for parsing:

| Section | Start Symbol | End Symbol |
|---------|--------------|-------------|
| Metadata | `|---Field: value---|` | N/A |
| Sections | `|====Start of Name====|` | `|====End of Name====|` |
| Stages | `|<===Start of Stage_N===>|` | `|<===End of Stage_N===>|` |

**Example**:
```markdown
|---Style: a little nsfw---|
|---Location: Bedroom---|
|---Mood: Intimate, comfortable---|

# Topic Name

## Topic Description
|====Start of Topic Description====|
Description content
|====End of Topic Description====|

## Detail
|====Start of Detail====|
Main content here
|<===Start of Stage_1===>|
First part
|<===End of Stage_1===>|
|====End of Detail====|

|---Similarity: 80---|
|---ReadForbidden: ```[\s\S]*?``` ---|
```

**Plan**:
```
dialogue-topics/
├── template.md              # NEW: Topic template with markers
├── format-chatting-before-sleep.md  # Converted from chatting-before-sleep.md
├── format-fanfiction.md     # Converted from fanfiction.md
├── format-learn-cuda.md    # Converted from learn-cuda.md
├── chatting-before-sleep.md # Old format (keep for compatibility)
├── learn-cuda.md           # Old format (keep for compatibility)
└── fanfiction.md           # Old format (keep for compatibility)
```

**Testing**:
- Run `python dialogue-server/quick_start.py` with new template
- Verify LLM respects `similarity` and `read_forbidden` parameters
- Verify stage markers work correctly for long content

---

#### 1.2 Topic Type Support 🔴 SECOND PRIORITY

**Why second**: Depends on template, enables all topic types.

**4 Types**:
| Type | Behavior | Current State |
|------|----------|----------------|
| Simple | Free discussion | Working |
| Learning | Don't read ## Detail directly, discuss key points | ⚠️ Partial (new format supports `ReadForbidden`) |
| Fanfiction | Follow ## Detail with similarity % | ✅ New format supports `Similarity` |
| Letter | Read letter content, introduce correspondent | ❌ Not supported |

**Topic Parsing**: The new template format requires updates to:
```
dialogue-server/dialogue_gen/
├── topic_loader.py      # MODIFY: Parse new symbol markers
├── prompt_builder.py    # MODIFY: Add type-specific prompts
└── parser.py            # MODIFY: Handle stage markers
```

**Plan**:
```
dialogue-server/dialogue_gen/
├── topic_loader.py      # MODIFY: Add type detection
├── prompt_builder.py    # MODIFY: Add type-specific prompts
└── topic_types.py      # NEW: Type definitions
```

**Implementation for each type**:

**Simple** (current - no changes needed):
- Use existing prompt builder

**Learning**:
```python
# In prompt_builder.py, add:
LEARNING_PROMPT = """
## Instructions for learning topic:
- Do NOT read the code/content in ## Detail directly
- Discuss key points, insights, or "踩坑" (trap experiences)
- Feel free to express difficulty, confusion, or breakthroughs
"""
```

**Fanfiction**:
```python
# In prompt_builder.py, add:
FANFICTION_PROMPT = """
## Instructions for fanfiction topic:
- Follow the story in ## Detail with {similarity}% accuracy
- At 100%: Copy/paste key lines as dialogue
- At 50%: Paraphrase while keeping plot points
- At 0%: Create original dialogue that matches mood
"""
```

**Letter**:
```python
# In prompt_builder.py, add:
LETTER_PROMPT = """
## Instructions for letter topic:
- Introduce the letter and the correspondent
- Read specific content from letter when appropriate
- React to the letter content naturally
"""
```

**Testing**:
- Create test topics for each type in `dialogue-topics/`
- Run dialogue-server and verify output matches expected behavior

---

### Phase 2: Integration (Weeks 3-4)

#### 2.1 Streaming Output Pipeline 🔴 THIRD PRIORITY

**Why third**: Critical for long topics, enables async processing.

**Current issue**: dialogue-server waits for ALL dialogue before voice-server can start.

**Plan**:
```
dialogue-server/          voice-server/
     |                        |
  [dialogue unit 1] ───────► [generate voice]
     |                        |
  [dialogue unit 2] ───────► [generate voice]
     |                        |
  [dialogue unit 3] ───────► [generate voice]
```

**Implementation**:
```
dialogue-server/dialogue_gen/
├── streaming_output.py   # NEW: Async output with callbacks
└── output_generator.py   # MODIFY: Add streaming mode

voice-server/
├── streaming_client.py   # NEW: Listen for dialogue units
└── voice_service.py      # MODIFY: Add queue processing
```

**Key design**:
```python
# streaming_output.py
class StreamingDialogueGenerator:
    def __init__(self, on_dialogue_unit_callback):
        self.callback = on_dialogue_unit_callback
    
    async def generate(self, characters, topic):
        for dialogue_unit in self.llm.stream():
            # Parse immediately
            parsed = self.parser.parse(dialogue_unit)
            # Send to voice server
            await self.callback(parsed)
            # Save to file incrementally
            await self.output.save_incremental(parsed)
```

**Testing**:
- Run with long topic (fanfiction.md)
- Verify voice generation starts before dialogue completes

**Existing solutions in third_party**:
- LingChat: Uses WebSocket streaming (`message_system/`)
- GPT-SoVITS API: Already supports streaming mode

---

#### 2.2 Dialogue-Voice Integration ⚠️ FOURTH PRIORITY

**Why fourth**: Currently voice-server is separate from dialogue-server.

**Current state**:
- dialogue-server outputs: `real_dialogue.jsonl`
- voice-server needs: manual input

**Plan**:
```
dialogue-server/output/real_dialogue.jsonl
         │
         ▼
[caption_text] vs [voice_text] separation
         │
         ▼
voice-server/input/ (auto-detect)
         │
         ▼
voice-server/output/audio/
```

**Key fix needed**:
```python
# In dialogue-server output, ensure:
{
    "character": "艾玛",
    "text": "这么晚来找我，是有什么事情吗？",  # Caption (Chinese)
    "text_jp": "んな遅くに...",               # Voice (Japanese)
    "action": "高兴地看着希罗",               # Not for voice
    "voice_text": "んな遅くに私を訪ね...",   # NEW: extracted for voice
    "caption_text": "这么晚来找我，是有什么事情吗？"  # NEW: for display
}
```

**Implementation**:
```python
# dialogue-server/dialogue_gen/output_generator.py
def separate_caption_and_voice(dialogue_line):
    # Remove action text in parentheses for voice
    voice_text = remove_parentheses(dialogue_line.text_jp)
    # Keep full text for caption
    caption_text = dialogue_line.text_jp
    return caption_text, voice_text
```

**Testing**:
- Run dialogue-server → verify voice_text extracted correctly
- Run voice-server with extracted text → verify audio quality

---

### Phase 3: User Experience (Weeks 5-8)

#### 3.1 Edit & Regenerate 🔴 FIFTH PRIORITY

**Why fifth**: Users need to tweak dialogue before final output.

**Features needed**:
1. Load `real_dialogue.jsonl` into editable UI
2. User edits text in one language
3. Detect changes → mark for voice regeneration
4. Re-generate voice for changed entries only

**Plan**:
```
processing-topic-folders/
└── {topic-name}/
    ├── dialogue.jsonl          # Original (git tracked)
    ├── dialogue_edited.jsonl   # User edits
    ├── voice/                  # Generated audio
    │   ├── ema_00000.wav
    │   └── hiro_00000.wav
    └── metadata.json           # Which entries need regeneration
```

**Implementation**:
```python
# Simple approach: JSON diff
def detect_changes(original_path, edited_path):
    original = load_jsonl(original_path)
    edited = load_jsonl(edited_path)
    changed_indices = []
    for i, (orig, edit) in enumerate(zip(original, edited)):
        if orig['text_jp'] != edit['text_jp']:
            changed_indices.append(i)
    return changed_indices
```

**Testing**:
- Edit one line in dialogue.jsonl
- Run regenerate → verify only changed line gets new voice

---

#### 3.2 Screen/UI Display 🔴 SIXTH PRIORITY

**Why sixth**: End-to-end visualization.

**Features**:
- Character figures display
- Subtitle text
- Voice playback
- Timeline controls (play, pause, next, prev)
- Settings panel

**Plan**:
```
screen-server/
├── index.html              # Basic player
├── player.js               # Audio/text synchronization
├── style.css               # Layout (16:9 for pc, 9:20 for phone, responsive, etc)
└── config.json             # Screen settings
```

**Integration with WebGAL** (third_party):
- WebGAL has: character sprites, backgrounds, text boxes
- We can use WebGAL's rendering for our dialogue playback
- Location: `third_party/WebGAL/`

**Testing**:
- Load processed topic folder
- Play through all dialogue
- Verify timing matches audio duration

---

#### 3.3 Split & Resize (Page System) 🟢 LAST PRIORITY

**Why last**: Nice to have, complex to implement.

**Features**:
- Split long topics into pages
- Support multiple screen sizes (PC, phone)
- Configurable font size, line spacing
- Stage-by-stage output

**Implementation approach**:
```python
# dialogue-server/dialogue_gen/page_splitter.py
def split_into_pages(dialogue_jsonl, screen_config):
    # Calculate max characters per page based on:
    # - Screen resolution
    # - Font size
    # - Line spacing
    # Split dialogue into N pages
    # Return: [{"page": 1, "start_line": 0, "end_line": 5}, ...]
```

**Testing**:
- Test with different screen configs
- Verify text fits within bounds

---

## Part 4: Implementation Summary Table

| Priority | Task | Dependencies | Est. Time | Existing Solution |
|----------|------|--------------|-----------|-------------------|
| 1 | Topic Template | None | 1 day | LingChat prompts |
| 2 | Topic Types | Template | 2 days | None |
| 3 | Streaming Output | Types | 3 days | LingChat WS |
| 4 | Voice Integration | Streaming | 1 day | None |
| 5 | Edit & Regenerate | Voice Integration | 3 days | None |
| 6 | Screen/UI | All above | 5 days | WebGAL |
| 7 | Split & Resize | Screen/UI | 3 days | None |

**Total estimated**: ~18 days (9 weeks at 2 days/week)

---

## Part 5: Quick Start Recommendations

### If you want to test NOW:

1. **Test current dialogue-server**:
   ```bash
   cd dialogue-server
   conda activate a2d-studio
   python quick_start.py
   ```

2. **Test voice-server demo**:
   ```bash
   # First tell user to start GPT-SoVITS API
   # cd third_party/GPT-SoVITS-v2pro-20250604
   # python api_v2.py -a 127.0.0.1 -p 9880
   
   # Then run voice demo
   cd voice-server
   conda activate a2d-studio
   python demo_gpt_sovits_voice.py
   ```

### If you want to extend:

**Recommended next step**: Create topic template (`dialogue-topics/template.md`)

This is the smallest, most foundational change that enables everything else.

---

## Part 6: Questions to Clarify

Before proceeding, please confirm:

1. **Priority order**: Does this order make sense? Any task should be higher/lower priority?

2. **Topic types**: Are the 4 types correct? Should any be added/removed?

3. **Streaming**: Is async dialogue→voice important for your use case, or is batch processing acceptable?

4. **Screen/UI**: Should we build from scratch or extend WebGAL? WebGAL has more features but may be complex.

5. **Scope**: Is there a specific topic you want to finish first? That could guide prioritization.

---

*Last Updated: 2026-03-15*
*Based on: roadmap-after-task1-task2.md + what-have-been-down.md*
