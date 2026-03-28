# Mimo Topic Plan

## Goal
Convert 3 origin topic files from `origin-messy-topics/` to new format in `dialogue-topics/`, following `SETTING-topic-template.md` and `DETAIL-topic-template.md`.

## Source Files
| File | Lines | Type | Has Detail? |
|------|-------|------|-------------|
| `origin-messy-topics/chatting-before-sleep.md` | 33 | None (simple) | No |
| `origin-messy-topics/learn-cuda.md` | 97 | Learning | Yes (code ~75 lines) |
| `origin-messy-topics/fanfiction.md` | 542 | Fanfiction | Yes (story ~520 lines) |

## Output Files
| Source | Output | Notes |
|--------|--------|-------|
| chatting-before-sleep.md | `SETTING-chatting-before-sleep.md` | No DETAIL needed |
| learn-cuda.md | `SETTING-learn-cuda.md` + `DETAIL-learn-cuda.md` | Code in DETAIL |
| fanfiction.md | `SETTING-fanfiction.md` + `DETAIL-fanfiction.md` | 4 stages in DETAIL |

## Tasks
- **Task 1**: Convert `chatting-before-sleep.md` → `SETTING-chatting-before-sleep.md`
- **Task 2**: Convert `learn-cuda.md` → `SETTING-learn-cuda.md` + `DETAIL-learn-cuda.md`
- **Task 3**: Convert `fanfiction.md` → `SETTING-fanfiction.md` + `DETAIL-fanfiction.md` (with 4 stages)

## Fanfiction Stage Split
| Stage | Content |
|-------|---------|
| Stage_1 | Hiro discovers someone approaching Emma, eavesdrops from hallway |
| Stage_2 | Lunch break — bento feeding, flustered cute interaction |
| Stage_3 | Afternoon — Hiro's internal monologue, realizes her feelings |
| Stage_4 | After school — crepe shop, Emma's confession, bittersweet ending |

## Rules
- Never edit existing files in `origin-messy-topics/`
- Git commit after every small edit
- Record to `time-action-record.md`
- Follow template format exactly from `SETTING-topic-template.md` and `DETAIL-topic-template.md`
