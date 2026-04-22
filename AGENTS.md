## 0000. From andrej-karpathy

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```
Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.


## 000. First Principles
Please think using the first principles approach. 
You should not always assume that we are very clear about what we want and how to achieve it. 
Please be cautious and start from the original needs and problems. 
If the motives and goals are not clear, stop and discuss with us.

## 00. Specification for Solutions
When you are required to provide modifications or reconfiguration solutions, the following specifications must be followed: No compatibility or patch solutions are allowed.
No over-design is permitted. Maintain the shortest path implementation and must not violate the first requirement.
No solutions beyond the requirements provided by us are allowed, such as some fallback and downgrade solutions.
This may lead to issues with business logic deviation.
It is necessary to ensure the correctness of the solution logic and must undergo full-chain logic verification.

## 0. Always ask before do something dangerous and use git add commit after every small edit
- before use dangerous 'rm' or other similar commands, ask the user.
- before install, check if the specific conda env is activated, if not, ask the user.
- please always use git to make sure safe rollback. 

## 1. Minimalist Logging (Token-Efficient)
- Before and after every action, append a single-line summary to `time-action-record.md`.
- What you do, why, brief results, next, and the timeline (the time you start and end).
- Do NOT record full terminal stdout unless an error occurs. 

## 2. Smart Backup Policy (Original + 2)
- Before the first-ever modification of a file, create `filename.orig`. Never delete or overwrite `.orig`.
- For subsequent edits, maintain exactly two rotating backups: `filename.bak1` and `filename.bak2`.
- Always overwrite the oldest `.bak` file so that you only ever have: [Original], [Previous], and [Current].

## 3. Strict Safety
- Use of `rm` or `shred` is strictly forbidden. 
- To "delete" content, move it to a `.trash/` directory or comment it out.

## 4. Internal Tooling Awareness
- Use your internal `write_file` and `list_dir` tools to verify states before/after actions. 
- When recording logs, prioritize using your internal memory; only write to the markdown log to provide a "hard copy" for the human user.

## 5. the example way to get tail of run on windows:
```
# 1. Force PowerShell to use UTF-8 for everything
$OutputEncoding = [Console]::InputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
# 2. Force Python to use UTF-8 mode
$env:PYTHONUTF8 = 1
# 3. Run your command (using Select-Object to get the tail)
python .\quick_start.py 2>&1 | Select-Object -Last 50
```

## 6. always remember to check the running env (uv/pip/conda/...) and run commands in the proper env
example:
```win
(base) PS D:\aaa-new\setups\a2d-studio\ref> conda activate a2d-studio
(a2d-studio) PS D:\aaa-new\setups\a2d-studio\ref> 
```
```linux
conda info --envs 
```
you may alread in the correct conda env.
If not, you need to find the .bat or .sh or similar things in anaconda or miniconda folder.

## 7. please do not edit files in the third_party folder and things recorded in .gitignore in normal situation
If needed, ask the user first.

## 8. NEVER use rm or delete or similar things before asking the user
If needed, use git and move useless things to ./trash/ (if not exist should create first).

## 9. other things
please make sure your actions can be totally rollback.
please ALWAYS check the system is safe, and your action will not break the system.
please make sure your log files, other output files and commands are under curr dir, 
or the system will seem stop you and ask for permission.

## 10. end questions
at the end, you can list 10 questions, and A. B. C., and your answers and recommandations to help things be clear.
