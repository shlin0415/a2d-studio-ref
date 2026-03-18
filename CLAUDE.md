# AI Safety & Logging Protocol

## 0. Always ask before do something dangerous and use git
- before use dangerous 'rm' or other similar commands, ask the user.
- before install, check if the specific conda env is activated, if not, ask the user.
- please always use git to make sure safe rollback. 

## 1. Minimalist Logging (Token-Efficient)
- Before and after every action, append a single-line summary to `ACTION_LOG.md`.
- FORMAT: [Timestamp] | [Action Type] | [Target] | [Result Summary]
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

## 6. always remember to check the running env and run commands in the proper env
example:
```
(base) PS D:\aaa-new\setups\a2d-studio\ref> conda activate a2d-studio
(a2d-studio) PS D:\aaa-new\setups\a2d-studio\ref> 
```

## 7. please do not edit files in the third_party folder and things recorded in .gitignore in normal situation
If needed, ask the user first.

## 8. NEVER use rm or delete or similar things before asking the user
If needed, use git and move useless things to ./trash/ (if not exist should create first).

