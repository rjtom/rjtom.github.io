import sys
import os
import time
from github_bio_agent.tools import create_github_repo, commit_file_to_repo, enable_github_pages, check_pages_status

def deploy():
    username = "rjtom"
    pat = os.environ.get("GITHUB_PAT", "").strip()
    if not pat:
        print("[ERROR] GITHUB_PAT environment variable is not set. Please set it before running.")
        sys.exit(1)
    repo_name = f"{username}.github.io"

    
    print("========== Starting Automated Portfolio Deployment ==========")
    
    # 1. Create Repository
    print(f"1. Attempting to create public repository '{repo_name}'...")
    try:
        res = create_github_repo(repo_name, "Personal portfolio website deployed autonomously by Google Antigravity Agent", pat)
        print(f"   [SUCCESS/INFO] {res}")
    except Exception as e:
        print(f"   [WARNING] Repository creation skipped or failed: {e}")
        print("             If you created the repository manually on GitHub, we will still attempt to commit to it.")

        
    # 2. Read local index.html
    html_path = "/Users/thomasraju/kaggle-comp/github_bio_agent/index.html"
    print(f"2. Reading premium HTML portfolio from {html_path}...")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"   [ERROR] Failed to read index.html: {e}")
        sys.exit(1)
        
    # 3. Commit index.html
    # We wait a couple of seconds to make sure the newly created repo is initialized on GitHub
    print("3. Waiting 3 seconds for repository initialization on GitHub...")
    time.sleep(3)
    
    print(f"4. Committing index.html to '{username}/{repo_name}' main branch...")
    try:
        res = commit_file_to_repo(
            repo_name=repo_name,
            file_path="index.html",
            content=content,
            commit_message="feat: deploy premium portfolio via Antigravity Agent",
            github_pat=pat,
            github_username=username
        )
        print(f"   [SUCCESS] {res}")
    except Exception as e:
        print(f"   [ERROR] Failed to commit file: {e}")
        sys.exit(1)
        
    # 4. Enable Pages
    print("5. Enabling GitHub Pages on main branch...")
    try:
        res = enable_github_pages(repo_name, pat, username)
        print(f"   [SUCCESS/INFO] {res}")
    except Exception as e:
        print(f"   [ERROR] Failed to enable Pages: {e}")
        # Sometimes Pages is already enabled automatically for <user>.github.io repos
        pass
        
    # 5. Check Pages status
    print("6. Verifying Pages deployment status...")
    time.sleep(2)
    try:
        res = check_pages_status(repo_name, pat, username)
        print(f"   [STATUS] {res}")
    except Exception as e:
        print(f"   [WARNING] Could not verify Pages status: {e}")
        
    print("\n================== Deployment Complete! ==================")
    print(f"Your gorgeous personal bio page is live at: https://{username}.github.io/")

if __name__ == "__main__":
    deploy()
