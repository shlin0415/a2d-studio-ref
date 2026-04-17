# Task 1: Phase 1 - SETTING Templates (.md files)

## Goal
Update all SETTING-*.md and DETAIL-topic-template.md:
1. Rename `DETAIL_Similarity` → `DETAIL_Follow` with preset comments
2. Rename `DETAIL_ReadForbidden` → `DETAIL_Direct_Use_For_Voice` with preset comments
3. Add `Dialogue_Language='zh'` and `Voice_Language='zh'` fields

## Files to change
| File | Changes |
|------|---------|
| `SETTING-topic-template.md` | Rename params, add language fields, add preset comments |
| `SETTING-learn-cuda.md` | Change values: Follow=80, Direct_Use=20, add language |
| `SETTING-fanfiction.md` | Change values: Follow=80, Direct_Use=90, add language |
| `SETTING-chatting-before-sleep.md` | Add language fields only (no DETAIL params) |
| `DETAIL-topic-template.md` | Update annotation references |

## Preset table for comments
```
DETAIL_Follow=80 // 常见预设: Learning=80, Fanfiction=80, Story=60, ASMR=60
DETAIL_Direct_Use_For_Voice=0 // 常见预设: Learning=20, Fanfiction=90, Story=20, ASMR=20
```

## Steps
1. Rename old SETTING-topic-template.md → old-SETTING-topic-template.md
2. Create new SETTING-topic-template.md with all changes
3. Repeat for other SETTING files
4. Update DETAIL-topic-template.md annotations
5. Git commit each
6. Record to time-action-record.md
