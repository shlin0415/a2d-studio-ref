# Task 3: Convert fanfiction.md

## Goal
Convert `origin-messy-topics/fanfiction.md` → `dialogue-topics/SETTING-fanfiction.md` + `dialogue-topics/DETAIL-fanfiction.md`

## Source Analysis
- 542 lines, fanfiction topic with long story
- Has `## Detail` section with ~520 lines of story text
- Type: Fanfiction
- Needs 4 stages in DETAIL

## Stage Split (by narrative arc)
| Stage | Lines (approx) | Content |
|-------|----------------|---------|
| Stage_1 | 12-108 | Hiro in hallway discovers someone approaching Emma, eavesdrops |
| Stage_2 | 108-268 | Lunch break — Snowy/Hannah tell about letter, bento feeding scene |
| Stage_3 | 270-362 | Afternoon — Hiro's internal monologue, realizes she likes Emma |
| Stage_4 | 364-537 | After school — crepe shop, Emma's confession, bittersweet ending |

## Mapping
| Old Section | New Location |
|-------------|-------------|
| `# Fanfiction` | `# Fanfiction` (in SETTING) |
| `Style: a little nsfw` | `Style='a little nsfw'` in Setting |
| `Location: See in ## Detail` | `Location='See in DETAIL'` |
| `Mood: ...` | `Mood='Mood for learning, comfortable, relaxed, lovely'` |
| `## Topic Description` | Topic Description section |
| `## Detail` content | DETAIL file with 4 stages |
| `## Character Interactions` | After `------` in Setting |

## Steps
1. Create `dialogue-topics/DETAIL-fanfiction.md` with 4 stages
2. Create `dialogue-topics/SETTING-fanfiction.md`
3. Git commit each
4. Record to time-action-record.md
