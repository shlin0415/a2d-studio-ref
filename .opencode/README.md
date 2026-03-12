# OpenCode Intelligence Directory

This directory contains crystallized project intelligence.

## Structure

```
.opencode/
├── agents/           # Domain expertise and findings
├── command/          # Automation procedures
├── data/             # Risk mappings (if any)
└── skills/          # Standard operating procedures
```

## Contents

### agents/
- **gpt-sovits-expert.md**: GPT-SoVITS model switching bottleneck findings

### command/
- **run-tests-windows.md**: UTF-8 encoding fix for Windows test scripts

### skills/
- **dialogue-voice-pipeline.md**: End-to-end SOP for dialogue + voice generation

## Usage

These files are used by the AI agent to:
1. Avoid known pitfalls (Hidden Traps)
2. Follow established procedures
3. Apply domain expertise from past discoveries

## Updates

When new insights are gained:
1. Identify the category (agent/command/data/skill)
2. Update the relevant file using AReaL Gold Standard:
   - Imperative mood
   - Evidence-first
   - Short bullet points
3. Commit with "crystallize" message
