# Task 3: Phase 3 - Fix prompt_builder.py

## Goal
Make language actually control the output format. Currently hardcoded to Chinese+Japanese.

## Current problem
`prompt_builder.py` accepts `language` param but format is always:
```
【emotion】Chinese dialogue（action）<Japanese translation>
```

## Fix
New signature with `dialogue_language` + `voice_language`. Format becomes dynamic.

## Format table
| DL | VL | Prompt Format |
|----|----|---------------|
| zh | zh | `【emotion】Chinese dialogue（action）` |
| zh | ja | `【emotion】Chinese dialogue（action）<Japanese translation>` |
| zh | en | `【emotion】Chinese dialogue（action）<English translation>` |
| ja | ja | `【emotion】Japanese dialogue（action）` |
| ja | zh | `【emotion】Japanese dialogue（action）<Chinese translation>` |
| ja | en | `【emotion】Japanese dialogue（action）<English translation>` |
| en | en | `【emotion】English dialogue（action）` |
| en | zh | `【emotion】English dialogue（action）<Chinese translation>` |
| en | ja | `【emotion】English dialogue（action）<Japanese translation>` |

## Approach
- Rename old prompt_builder.py → old-prompt_builder.py
- Create new prompt_builder.py with dynamic format
- Write test to verify prompts change with language

## Files to change
| File | Action |
|------|--------|
| `dialogue_gen/prompt_builder.py` | Rename to old, create new |
| `tests/test_prompt_builder_languages.py` | New test file |
