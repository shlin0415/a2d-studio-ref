---
name: crystallize-gold-experience
description: Guide for capturing breakthroughs, lessons learned, and hidden traps from the current session and exporting them into the .opencode/ folder. Use when a task is finished or a hard bug is resolved.
---

# Crystallize Gold Experience

Capture architectural intelligence and "Hidden Traps" discovered during development and convert them into permanent system knowledge.

## When to Use

This skill is triggered when:
- A major feature or stage is successfully completed.
- A difficult bug (especially distributed hangs or logic errors) is resolved.
- You realize the current `.opencode/` instructions were incomplete or led to a mistake.
- **Mandatory:** If a single issue took more than 3 turns to debug.

## Reference Examples (AReaL Gold Standard)
**Format first!!! Especially for the special head, the special tail, and the name match!!!**
**If the format is wrong, the whole file will be totally useless!!!**
| Component | AReaL Crystallized Lesson | File Reference |
| :--- | :--- | :--- |
| **Agent** | "Experts must use `dp_shard_mod_ep` mesh, not `dp_shard`, to avoid OOM." | `agents/archon-expert-example-AReaL.md` |
| **Command** | "Allocate `task(model='opus')` for engine code but `haiku` for docs." | `command/review-pr-example-AReaL.md` |
| **Data** | "Map `parallel_dims.py` to **CRITICAL** risk level." | `data/review-pr-change-types-example-AReaL.md` |
| **Skill** | "Verify StateDict on a **Meta Device** before consuming real GPU time." | `skills/add-archon-model-example-AReaL/SKILL.md` |

## Step-by-Step Guide

### Step 1: Perform Root Cause Reflection
Analyze the delta between the initial failure and the final solution.
- **The Hidden Trap:** What was the non-obvious cause? (e.g., NCCL timeouts, async blocking in a hot path, DTensor mesh mismatch).
- **The Breakthrough:** What specific evidence (`py-spy`, `nvidia-smi`) or code pattern fixed it?

### Step 2: Determine Component Routing
Map the discovery to the correct `.opencode/` category:

| Category | Destination | When to Update |
| :--- | :--- | :--- |
| **Domain Intuition** | `agents/` | New sharding rules, hardware constraints, or framework behaviors. |
| **Automation** | `command/` | Repetitive Git, Bash, or Review workflows found during the session. |
| **Risk Mapping** | `data/` | New correlations between "File Paths" and "Risk Levels/Severities." |
| **Procedures** | `skills/` | Standard Operating Procedures (SOPs) for repeating the task. |

### Step 3: Draft Precise Updates
Follow the **AReaL Formatting Standard**:
- **Imperative Mood:** Use "Always," "Never," "Ensure." (e.g., "Never use `print()` in hot paths").
- **Evidence-First:** Include the specific `bash` command used to verify the state.
- **Short & Precise:** Use bullet points. No introductory fluff.

### Step 4: Update and Commit
1.  Read the relevant `.opencode/` file.
2.  Inject the new intelligence into the "Common Issues," "Key Requirements," or "Debugging" sections.
3.  Perform a "Crystallization Commit" to save the system state.

## Key Requirements

1.  **Never delete existing knowledge:** Only append or refine unless a rule is proven wrong.
2.  **Externalize everything:** If you "figured it out" in your reasoning, it must be written in the `.opencode/` folder.
3.  **Machine-Readable:** Keep checklists structured so future agents can parse them as tasks.
4.  **Reference the Gold Standard:** When adding a skill, link to the best implementation in the current repo as the "Template."

## Common Mistakes
- ❌ Format error (the file head, the file tail, the name match).
- ❌ Writing long paragraphs (AI context is more efficient with lists).
- ❌ Keeping lessons "in-head" across session restarts (leads to regression).
- ❌ Documenting the "What" (Code) instead of the "Why" (Architecture/Trap).
- ❌ Forgetting to include the `bash` commands used for verification.

______________________________________________________________________

<!--
================================================================================
                            MAINTAINER GUIDE
================================================================================

Location: .opencode/skills/crystallize-gold-experience/SKILL.md
Invocation: /crystallize-gold-experience

## Purpose
This is the meta-learning skill. It ensures that the agent's "Expertise" 
is not static but grows with every code change.

## How to Update
Update this skill if the directory structure of .opencode/ changes 
or if new model-specific "Harvesting" rules are discovered.
================================================================================
-->
