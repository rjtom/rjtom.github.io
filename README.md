# 💫 Autonomous GitHub Bio-Page Deployer Agent

> **Experimental & Imaginative/Fictional Disclaimer**: This project is completely experimental. All features, data, and integrations are entirely imaginative/fictional and designed solely for demonstration, prototyping, and educational purposes.

A premium, fully autonomous AI Agent built on top of the **Google Antigravity SDK** that designs, commits, and deploys high-fidelity, responsive personal portfolio websites directly to **GitHub Pages** using GitHub REST APIs.

---

## 📸 Architecture & Workflow

1. **User Profile Ingestion**: Reads name, title, location, and social bio summary.
2. **Design Generation**: Automatically designs a luxury responsive HTML5 portfolio template complete with backdrop glows, custom typography, animations, and an embedded disclaimer banner.
3. **Repository Creation**: Interacts with the GitHub API to dynamically provision the target repository `<username>.github.io`.
4. **Code Publication**: Commits and pushes the generated `index.html` file into the main branch of the repository.
5. **Pages Provisioning**: Signals GitHub to enable static website hosting (GitHub Pages) on the repository.

---

## 🛠️ Getting Started

### Prerequisites

Ensure you have your **GEMINI_API_KEY** exported and have generated a **GitHub Personal Access Token (PAT)** with classic `repo` scope.

### Installation

Sync the workspace dependencies using `uv`:

```bash
uv sync
```

### Running the Agent

Launch the interactive bio deployer CLI:

```bash
python3 -m github_bio_agent.app
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
