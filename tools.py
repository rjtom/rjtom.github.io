import urllib.request
import json
import base64
from typing import Dict, Any, Optional

def _github_request(url: str, method: str, pat: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Helper utility to perform authenticated requests to the GitHub REST API."""
    req = urllib.request.Request(
        url,
        method=method,
        headers={
            "Authorization": f"Bearer {pat}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "google-antigravity-bio-deployer",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )
    
    if data is not None:
        req.add_header("Content-Type", "application/json")
        json_data = json.dumps(data).encode("utf-8")
    else:
        json_data = None
        
    try:
        with urllib.request.urlopen(req, data=json_data) as response:
            res_body = response.read().decode("utf-8")
            return json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            err_json = json.loads(err_body)
            err_msg = err_json.get("message", err_body)
        except Exception:
            err_msg = err_body
        raise Exception(f"GitHub API Error [{e.code}]: {err_msg}")
    except Exception as e:
        raise Exception(f"Connection error: {str(e)}")

def create_github_repo(repo_name: str, description: str, github_pat: str) -> str:
    """Creates a new public GitHub repository for the authenticated user.

    Args:
        repo_name: The name of the repository to create.
        description: A brief description of the repository.
        github_pat: The GitHub Personal Access Token (PAT) with repo scope.
    """
    url = "https://api.github.com/user/repos"
    payload = {
        "name": repo_name,
        "description": description,
        "private": False,
        "auto_init": True  # Crucial to create main branch with a README so we can commit files to it immediately
    }
    
    # Check if repo already exists, if so return success message instead of failing
    try:
        _github_request(url, "POST", github_pat, payload)
        return f"Successfully created new public repository '{repo_name}' with auto-initialization."
    except Exception as e:
        if "already exists" in str(e).lower() or "442" in str(e) or "422" in str(e):
            return f"Repository '{repo_name}' already exists. Proceeding with update."
        raise e

def commit_file_to_repo(
    repo_name: str,
    file_path: str,
    content: str,
    commit_message: str,
    github_pat: str,
    github_username: str
) -> str:
    """Commits or updates a file in the main branch of a specified GitHub repository.

    Args:
        repo_name: Name of the target repository.
        file_path: The workspace file path, e.g. "index.html".
        content: The raw string content of the file.
        commit_message: Message to associate with the commit.
        github_pat: The GitHub Personal Access Token.
        github_username: The GitHub username of the repository owner.
    """
    url = f"https://api.github.com/repos/{github_username}/{repo_name}/contents/{file_path}"
    
    # Step 1: Check if file already exists to get its SHA hash (required for updates)
    sha = None
    try:
        file_info = _github_request(url, "GET", github_pat)
        sha = file_info.get("sha")
    except Exception:
        # File doesn't exist yet, which is fine
        pass
        
    # Base64 encode the string content
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha
        
    _github_request(url, "PUT", github_pat, payload)
    return f"Successfully committed '{file_path}' to repository '{github_username}/{repo_name}' on branch 'main'."

def enable_github_pages(repo_name: str, github_pat: str, github_username: str) -> str:
    """Enables and configures GitHub Pages hosting for the main branch of a repository.

    Args:
        repo_name: Name of the repository to enable Pages for.
        github_pat: The GitHub Personal Access Token.
        github_username: The GitHub username.
    """
    url = f"https://api.github.com/repos/{github_username}/{repo_name}/pages"
    payload = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }
    
    try:
        _github_request(url, "POST", github_pat, payload)
        return f"Successfully enabled GitHub Pages hosting on the 'main' branch (root path) for '{github_username}/{repo_name}'."
    except Exception as e:
        if "already exists" in str(e).lower() or "already enabled" in str(e).lower() or "409" in str(e):
            return f"GitHub Pages is already configured/enabled for '{github_username}/{repo_name}'."
        raise e

def check_pages_status(repo_name: str, github_pat: str, github_username: str) -> str:
    """Retrieves the deployment status of GitHub Pages for a given repository.

    Args:
        repo_name: Name of the repository.
        github_pat: The GitHub Personal Access Token.
        github_username: The GitHub username.
    """
    url = f"https://api.github.com/repos/{github_username}/{repo_name}/pages"
    try:
        res = _github_request(url, "GET", github_pat)
        html_url = res.get("html_url", f"https://{github_username}.github.io/{repo_name}/")
        status = res.get("status", "active")
        return f"GitHub Pages status: {status}. Live URL: {html_url}"
    except Exception as e:
        return f"Could not fetch Pages status (Pages might still be provisioning): {str(e)}"
