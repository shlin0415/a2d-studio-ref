import os
import argparse
import sys
from pathlib import Path

# Try to import pathspec for gitignore support
try:
    import pathspec
except ImportError:
    print("Error: 'pathspec' library is required.")
    print("Please install it using: pip install pathspec")
    sys.exit(1)

# Patterns based on your provided list
IGNORE_PATTERNS = """
# Dependencies
node_modules/
.pnpm-store/
vendor/
venv/
env/
.venv/
third_party/

# Build Artifacts
dist/
build/
out/
*.exe
*.dll
*.so
*.dylib
*.app

# IDE & Editor
.vscode/
.idea/
*.swp
*.swo
*.sublime-*

# OS Files
.DS_Store
Thumbs.db
desktop.ini
$RECYCLE.BIN/

# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
.eggs/

# Large Model Files
*.pth
*.ckpt
*.safetensors
*.gguf
*.bin
models/
checkpoints/
vae/
loras/
embeddings/

# Assets & Media
*.ogg
*.wav
*.mp3
*.png
*.jpg
*.jpeg
*.gif
*runtime*
*assets*
*resource*
*background*
*/fig/*
*/third_party/*
*/third-party/*

# Temporary / Logs
.cache/
temp/
tmp/
*.tmp
outputs/
logs/
*.log

# Negations (Exceptions to keep)
!dialogue-server/**/*.orig
"""

SOURCE_EXTENSIONS = {
    '.py', '.js', '.ts', '.c', '.cpp', '.h', '.hpp', '.java', 
    '.go', '.rs', '.sh', '.rb', '.php', '.cs', '.html', '.css', 
    '.sql', '.yaml', '.yml', '.json', '.md', '.txt'
}

# SOURCE_EXTENSIONS = {
#     '.py', '.js', '.ts', '.c', '.cpp', '.h', '.hpp', '.java', 
#     '.go', '.rs', '.sh', '.rb', '.php', '.cs', '.html', '.css'
# }


def get_spec(root_path):
    lines = IGNORE_PATTERNS.splitlines()
    gitignore_file = Path(root_path) / ".gitignore"
    if gitignore_file.exists():
        with open(gitignore_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines.extend(f.readlines())
    return pathspec.PathSpec.from_lines('gitwildmatch', lines)

def is_ignored(path, spec, root_path):
    rel_path = os.path.relpath(path, root_path)
    if rel_path == ".": return False
    return spec.match_file(rel_path.replace(os.sep, '/'))

def print_tree(directory, spec, root_path, file_handle, prefix=""):
    try:
        items = sorted(os.listdir(directory))
    except PermissionError:
        return

    filtered_items = [i for i in items if not is_ignored(os.path.join(directory, i), spec, root_path)]

    for i, item in enumerate(filtered_items):
        path = os.path.join(directory, item)
        is_last = (i == len(filtered_items) - 1)
        connector = "└── " if is_last else "├── "
        
        file_handle.write(f"{prefix}{connector}{item}\n")
        
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(path, spec, root_path, file_handle, new_prefix)

def collect_sources(directory, spec, root_path, file_handle):
    for root, dirs, files in os.walk(directory):
        # Prune ignored directories
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), spec, root_path)]
        
        for file in sorted(files):
            file_path = os.path.join(root, file)
            if is_ignored(file_path, spec, root_path):
                continue
                
            if Path(file).suffix.lower() in SOURCE_EXTENSIONS:
                rel_path = os.path.relpath(file_path, root_path)
                file_handle.write("\n" + "="*8 + "\n")
                file_handle.write(f"FILE: {rel_path}\n")
                file_handle.write("="*8 + "\n\n")
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        file_handle.write(f.read())
                        file_handle.write("\n")
                except Exception as e:
                    file_handle.write(f"[Could not read file {file}: {e}]\n")

def main():
    parser = argparse.ArgumentParser(description="Collect source code and tree structure.")
    parser.add_argument("--path", type=str, required=True, help="Folder path to scan.")
    parser.add_argument("--output", type=str, help="Output file path (optional).")
    args = parser.parse_args()

    root_path = os.path.abspath(args.path)
    if not os.path.exists(root_path):
        print(f"Error: Path '{root_path}' does not exist.")
        return

    spec = get_spec(root_path)

    # Determine where to send output
    if args.output:
        out_f = open(args.output, 'w', encoding='utf-8')
        print(f"Processing... results will be saved to {args.output}")
    else:
        out_f = sys.stdout

    try:
        out_f.write(f"\n# PROJECT STRUCTURE: {os.path.basename(root_path)}/\n")
        print_tree(root_path, spec, root_path, out_f)
        
        out_f.write("\n" + "#"*8 + "\n")
        out_f.write("# SOURCE CODE COLLECTION\n")
        out_f.write("#"*8 + "\n")
        collect_sources(root_path, spec, root_path, out_f)
        
        if args.output:
            print("Done!")
    finally:
        if args.output:
            out_f.close()

if __name__ == "__main__":
    main()

    