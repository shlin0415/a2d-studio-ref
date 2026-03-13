import os
import subprocess
from pathlib import Path

# --- CONFIGURATION ---
TARGET_DIR = r"./"  # Change this to your directory
REMOTE_URL = "git@github.com:yourusername/your-repo.git"
MAX_FILE_SIZE_MB = 5
SIZE_LIMIT_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def run_command(command, cwd=None):
    """Helper to run shell commands."""
    try:
        result = subprocess.run(
            command, cwd=cwd, shell=True, check=True, 
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def update_gitignore_for_large_files(root_dir):
    """Finds files > 5MB and appends them to .gitignore if not already there."""
    gitignore_path = Path(root_dir) / ".gitignore"
    
    # Read existing rules to avoid duplicates
    existing_rules = set()
    if gitignore_path.exists():
        existing_rules = set(gitignore_path.read_text().splitlines())

    new_ignores = []
    
    for file_path in Path(root_dir).rglob('*'):
        if file_path.is_file() and ".git" not in file_path.parts:
            # Check size
            if file_path.stat().st_size > SIZE_LIMIT_BYTES:
                # Get path relative to the root (Git style)
                rel_path = file_path.relative_to(root_dir).as_posix()
                if rel_path not in existing_rules:
                    new_ignores.append(rel_path)

    if new_ignores:
        print(f"Found {len(new_ignores)} new large files. Adding to .gitignore...")
        with open(gitignore_path, "a") as f:
            f.write("\n\n# --- AUTO-ADDED LARGE FILES (> 5MB) ---\n")
            for item in new_ignores:
                f.write(f"{item}\n")
        return True
    return False

def calculate_upload_size(root_dir):
    """Calculates total size of files NOT ignored by git."""
    # This command lists all files that git is currently tracking or about to track
    cmd = "git ls-files --others --cached --exclude-standard"
    files = run_command(cmd, cwd=root_dir)
    
    total_bytes = 0
    if files:
        for f in files.splitlines():
            file_path = Path(root_dir) / f
            if file_path.exists():
                total_bytes += file_path.stat().st_size
                
    return total_bytes / (1024 * 1024) # Return MB

def main():
    os.chdir(TARGET_DIR)
    
    # 1. Initialize Git if needed
    if not os.path.exists(".git"):
        print("Initializing Git...")
        run_command("git init")
        run_command(f"git remote add origin {REMOTE_URL}")

    # 2. Check for large files and update .gitignore
    # update_gitignore_for_large_files(TARGET_DIR)

    # 3. Calculate size before pushing
    total_size_mb = calculate_upload_size(TARGET_DIR)
    print(f"Current backup size (excluding ignored): {total_size_mb:.2f} MB")
    
    if total_size_mb > 1500: # Alert if > 1.5GB (GitHub likes repos < 2GB-5GB)
        print("!!! WARNING: Backup size is getting large for GitHub.")

    # # 4. Git Add, Commit, Push
    # print("Staging files...")
    # run_command("git add .")
    
    # status = run_command("git status --porcelain")
    # if status:
    #     print("Committing and Pushing...")
    #     run_command('git commit -m "Automated Backup"')
    #     run_command("git push -u origin main") # or master
    #     print("Success!")
    # else:
    #     print("No changes detected.")

if __name__ == "__main__":
    main()