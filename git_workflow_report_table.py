import subprocess
import sys
from tabulate import tabulate

# --------- CONFIG ---------
REPO_PATH = "/"  # change to your repo folder
BRANCH = "main"                   # change if your default branch is master
# --------------------------

# ANSI Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
CYAN = "\033[96m"

def run_cmd(cmd):
    """Run a shell command and return output"""
    result = subprocess.run(cmd, cwd=REPO_PATH, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{RED}Error running: {cmd}\n{result.stderr}{RESET}")
        sys.exit(1)
    return result.stdout.strip()

def show_change_report():
    """Show a table of file changes"""
    status = run_cmd("git status --porcelain")
    if not status:
        print(f"{CYAN}No changes detected.{RESET}")
        return

    table_data = []
    for line in status.splitlines():
        code, file_path = line[:2], line[3:]
        if code == "A " or code == "??":
            table_data.append([f"{GREEN}Added{RESET}", file_path])
        elif code == " M":
            table_data.append([f"{YELLOW}Modified{RESET}", file_path])
        elif code == " D":
            table_data.append([f"{RED}Deleted{RESET}", file_path])

    print("\n📋 Change Report:")
    print(tabulate(table_data, headers=["Status", "File"], tablefmt="fancy_grid"))

def main():
    print(f"{CYAN}🔹 Pulling latest changes from GitHub...{RESET}")
    print(run_cmd(f"git pull origin {BRANCH}"))

    show_change_report()

    commit_msg = input("\nEnter commit message (leave empty to skip commit): ").strip()
    if commit_msg:
        print(f"\n{CYAN}🔹 Staging all changes...{RESET}")
        print(run_cmd("git add ."))

        print(f"\n{CYAN}🔹 Committing changes...{RESET}")
        print(run_cmd(f'git commit -m "{commit_msg}"'))

        print(f"\n{CYAN}🔹 Pushing to GitHub...{RESET}")
        print(run_cmd(f"git push origin {BRANCH}"))
    else:
        print(f"\n{YELLOW}No commit message entered. Skipping commit and push.{RESET}")

    print(f"\n{GREEN}✅ Workflow complete!{RESET}")

if __name__ == "__main__":
    main()
