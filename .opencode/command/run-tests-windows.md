# Run Tests on Windows

## Problem
Windows console uses GBK encoding by default, causing `UnicodeEncodeError` when printing emojis (✓, ❌, 📋, etc.).

## Solution: UTF-8 Encoding Fix

### Option 1: Python Script Fix (Recommended)

Add UTF-8 encoding setup at the top of each Python script:

```python
# Force UTF-8 encoding for Windows
import sys
import os
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
```

### Option 2: Replace Unicode Characters

Replace Unicode symbols with ASCII alternatives:
- `✓` → `[OK]`
- `❌` → `[ERROR]`
- `📋` → `[INFO]`
- `⚠️` → `[WARN]`
- `🔍` → `[CHECK]`

### Option 3: Batch File with Encoding

Create `.bat` file with UTF-8 codepage:
```batch
@echo off
chcp 65001 >nul
set PYTHONUTF8=1
call conda activate a2d-studio
cd /d "%~dp0"
python your_script.py
```

---

## Commands Used

### Run Single Port Test
```bash
cd voice-server
conda activate a2d-studio
python test_single_port_bottleneck.py
```

### Run Dual Port Test
```bash
cd voice-server
conda activate a2d-studio
python test_dual_port_performance.py
```

### Compare Results
```bash
cd voice-server
python compare_results.py
```

---

## Verification

Check output encoding:
```python
import sys
print(sys.stdout.encoding)  # Should be 'utf-8'
```

---

## Files Updated

- `voice-server/test_single_port_bottleneck.py`
- `voice-server/test_dual_port_performance.py`
- `voice-server/compare_results.py`
