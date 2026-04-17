# Task 2: Convert learn-cuda.md

## Goal
Convert `origin-messy-topics/learn-cuda.md` → `dialogue-topics/SETTING-learn-cuda.md` + `dialogue-topics/DETAIL-learn-cuda.md`

## Source Analysis
- 97 lines, learning topic with code
- Has `## Detail` section with CUDA code
- Type: Learning
- No stage split needed (short code)

## Mapping
| Old Section | New Location |
|-------------|-------------|
| `# Learn CUDA` | `# Learn CUDA` (in SETTING) |
| `Style: a little nsfw` | `Style='a little nsfw'` in Setting |
| `Location: ...` | `Location='University, open learning space, no passersby'` |
| `Mood: ...` | `Mood='Mood for learning, comfortable, relaxed, lovely'` |
| `## Topic Description` | Topic Description section |
| `## Detail` content (code) | DETAIL file |
| `## Character Interactions` | After `------` in Setting |

## Steps
1. Create `dialogue-topics/DETAIL-learn-cuda.md`
2. Create `dialogue-topics/SETTING-learn-cuda.md`
3. Git commit each
4. Verify format
5. Record to time-action-record.md
