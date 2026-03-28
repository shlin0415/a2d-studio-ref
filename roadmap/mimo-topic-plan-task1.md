# Task 1: Convert chatting-before-sleep.md

## Goal
Convert `origin-messy-topics/chatting-before-sleep.md` → `dialogue-topics/SETTING-chatting-before-sleep.md`

## Source Analysis
- 33 lines, simple topic
- Sections: Title, metadata (Style/Location/Mood), Topic Description, Setting, Key Points, Expected Tone, Character Interactions
- No `## Detail` section → `TOPIC_Type='None'`
- Only SETTING file needed

## Mapping
| Old Section | New Location |
|-------------|-------------|
| `# Chatting Before Sleep` | `# Chatting Before Sleep` |
| `Style: a little nsfw` | `Style='a little nsfw'` in Setting |
| `Location: Bedroom` | `Location='Bedroom'` in Setting |
| `Mood: Intimate, comfortable, relaxed` | `Mood='Intimate, comfortable, relaxed'` in Setting |
| `## Topic Description` text | Inside `|====Start of Topic Description====|` |
| `## Setting` bullets | Inside Setting section |
| `## Key Points` | After `------` in Setting |
| `## Expected Tone` | After `------` in Setting |
| `## Character Interactions` | After `------` in Setting |

## Steps
1. Create `dialogue-topics/SETTING-chatting-before-sleep.md`
2. Git commit
3. Verify format matches template
4. Record to time-action-record.md
