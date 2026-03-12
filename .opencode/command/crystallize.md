---
description: Harvest breakthroughs and "Hidden Traps" from the current session to update project intelligence.
---

# Intelligence Crystallization

This command performs a retrospective on the current development session. It identifies architectural breakthroughs and "Hidden Traps" and encodes them into the project's permanent intelligence directory (`.opencode/`).

## Session Context

Current branch: 
!`git branch --show-current`

Recent activity:
!`git log -n 5 --oneline`

Files modified in this session:
!`git status --short`

Change volume:
!`git diff origin/main...HEAD --stat`

## Usage

```
/crystallize
```

## Workflow

### Step 1: Complexity Triage
Analyze the session history and the diff summary above to determine the **Reflection Depth**:

1. **Category LOW:** Local logic changes, documentation, or unit tests.
   - *Action:* Proceed to **Step 2: Direct Implementation**.
2. **Category HIGH:** Architectural shifts, complex debugging (e.g., resolving hangs, leaks, or race conditions), or multi-file refactors.
   - *Action:* Proceed to **Step 3: Expert Consultation**.

### Step 2: Direct Implementation (Path A)
*Use this path for straightforward improvements.*

1. Read the `crystallize-gold-experience` skill.
2. Examine the full diff: `git diff origin/main...HEAD`.
3. Identify the **Hidden Trap** (the non-obvious root cause) and the **Breakthrough** (the solution pattern).
4. Perform edits directly on the relevant `.opencode/` files (`agents/`, `skills/`, `data/`, or `command/`).

### Step 3: Expert Consultation (Path B)
*Use this path for deep architectural extraction.*

Execute a background task to consult the `crystallize-expert`.
**Note:** The expert is Read-Only. It will propose the content; you (the Main Agent) should take ref of the suggestions and help edit. Do not edit old existing files in .opencode/ in common cases. You can suggest the user to do.

```javascript
task(
  category="deep",
  load_skills=["crystallize-gold-experience"],
  run_in_background=false,
  description="Deep Intelligence Extraction",
  prompt="""
    High-complexity changes detected. 
    1. Analyze the session history and diffs to identify the root cause of 'Hidden Traps'.
    2. Identify architectural breakthroughs.
    3. PROPOSE precise updates for relevant .opencode/ files (Agents, Skills, Data).
    4. OUTPUT: Provide the exact content/bullet points to be added to each file using the AReaL Gold Standard (Imperative mood, Evidence-first).
  """
)
```

### Step 4: Standards & Finalization
Regardless of the path, all updates must adhere to the **AReaL Gold Standard**:
- **Tone:** Imperative mood ("Always," "Never," "Ensure").
- **Evidence:** Include the diagnostic CLI commands (e.g., `py-spy`, `logs`, `nvidia-smi`) used to verify the fix if exist.
- **Format:** Precise bullet points; lists over paragraphs.
- **Reference:** Link to the best implementation in the current repo as a "Template" if exists.

## Termination & Commit
1. Summarize the captured intelligence for the user.
2. **Commit:** Execute a "Crystallization Commit" describing the intelligence captured (e.g., `chore(agents): crystallize async deadlock resolution logic`).
3. **Stop:** Ask the user to stop or continue when take too long time to prevent logic looping.

______________________________________________________________________

<!--
================================================================================
                            MAINTAINER GUIDE
================================================================================

Location: .opencode/command/crystallize.md
Invocation: /crystallize

## Design Philosophy
This command mirrors the AReaL /create-pr strategy. It uses shell injection (!) 
to provide a snapshot of the session. It strictly separates the "Expert Brain" 
from the "Main Agent Hand" to maintain safety and consistency.

## How to Update
Update the triage criteria in Step 1 if the project's risk profile changes.
================================================================================
-->
