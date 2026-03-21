# Session: Roadmap Analysis - Task1 & Task2 Integration

## Date: 2026-03-21

## Participants
- User (Human)
- AI Assistant (opencode/minimax-m2.5-free)

---

## Session Summary

### Goal
Integrate Task1 (dialogue-server) and Task2 (voice-server) and create a roadmap for future improvements.

### Key Files Reviewed
- `tried-tasks-sessions-files/task1-human-chat.md`
- `tried-tasks-sessions-files/task2-human-chat.md`
- `tried-tasks-sessions-files/TASK1_ANALYSIS.md`
- `tried-tasks-sessions-files/TASK2_ANALYSIS.md`
- `tried-tasks-sessions-files/TASK1_QUICK_REFERENCE.md`
- `tried-tasks-sessions-files/TASK2_QUICK_REFERENCE.md`
- `roadmap/roadmap-after-task1-task2.md`
- `roadmap/what-have-been-down.md`
- `dialogue-server/` (source code)
- `voice-server/` (source code)
- `Character-fig-setting-example/`
- `Character-voice-example/`
- `dialogue-topics/`
- `origin-messy-topics/learn-cuda.md`
- `origin-messy-topics/fanfiction.md`
- `third_party/WebGAL/` (for reference)
- `third_party/Webgal_Dragonspring1.2/`

---

## Deliverables Created

### 1. `roadmap/what-have-been-down.md`
Comprehensive summary of Task1 and Task2 achievements:
- Task1: Dialogue Generation Server (6 components working)
- Task2: Voice Server (demo working, needs integration)

### 2. `roadmap/roadmap.md`
Integrated roadmap with:
- What has been done
- Recommended priority order
- Implementation plans for each task
- Testing criteria
- Questions for clarification

---

## Key Decisions Made

### Priority Order (Confirmed by User)
1. Topic Template System
2. Topic Types (4 types)
3. Streaming Output
4. Voice Integration
5. Edit & Regenerate
6. Screen/UI
7. Split & Resize

### Topic Type Behaviors (Confirmed by User)
- **Simple**: Free discussion (current state)
- **Learning**: Characters discuss concepts, NOT read code directly
- **Fanfiction**: Follow ## Detail with similarity% for dialogue only
- **Letter**: Read letter content, introduce correspondent

### Similarity Parameter
- Applies to **dialogue only** (what characters say)
- Not to plot/setting from ## Detail

### Fanfiction Splitting
- User requested splitting for long topics
- Split based on screen size calculation
- Stages help when screen is not big enough

### Screen/UI Approach
- Don't start full WebGAL
- Learn from WebGAL for reference
- Build simple screen display later

### Streaming
- Async dialogue→voice is important

---

## WebGAL Analysis (Reference)

### Scene Format
```
角色名:对话内容;
角色名:对话|对话;  (| = same character continues)
```

### Key Features
- Character name + colon + dialogue
- Multi-line with |
- Special commands: changeBg, changeFigure, setTransform, playEffect, addItem
- Single line = single display unit

### For Splitting Problem
- WebGAL doesn't have built-in screen-size-based text splitting
- Need our own calculator for text fitting

---

## Screen Calculator Design (Proposed)

```python
# dialogue-server/dialogue_gen/screen_calculator.py
def calculate_lines_per_screen(
    screen_width: int,
    screen_height: int,
    font_size: int,
    line_spacing: float,
    letter_spacing: float
) -> int:
    usable_height = screen_height * 0.7  # 30% for UI
    line_height = font_size * line_spacing
    return int(usable_height / line_height)
```

### Screen Presets (Proposed)
- PC: 1920x1080, font 20px
- Phone: 1080x2400, font 16px
- Tablet: 2048x1536, font 18px

---

## Open Questions (Discussed but Not Finalized)

1. **Screen presets**: Should include default PC/Phone/Tablet configs?
2. **Output format for stages**: Separate JSONL files or one file with `stage` field?
3. **Preview generation**: Output .txt preview for verification?
4. **Implementation approach**: Start Phase 1 after new session?

---

## Files Created in This Session

| File | Description |
|------|-------------|
| `roadmap/what-have-been-down.md` | Task1 + Task2 summary |
| `roadmap/roadmap.md` | Integrated roadmap document |
| `ACTION_LOG.md` | Action log entry |

---

## Session End Status

**Status**: Paused - New session to be started

**Reason**: User requested ending session and starting fresh

**Next Steps** (for next session):
1. Start Phase 1.1: Topic Template creation
2. Confirm screen calculator design
3. Begin implementation

---

## Git Commit Status

- All changes committed to git in previous sessions
- New files in this session: `roadmap/what-have-been-down.md`, `roadmap/roadmap.md`

---

*Session exported: 2026-03-21*
