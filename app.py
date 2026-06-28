import asyncio
import os
import sys
from google.antigravity import Agent
from github_bio_agent.agent import get_bio_agent_config

# Elegant Terminal Formatting Helpers
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

async def main():
    print(f"{Colors.HEADER}{Colors.BOLD}==================================================")
    print(" 💫 Google Antigravity - Autonomous Bio Deployer")
    print(f"=================================================={Colors.ENDC}\n")
    
    print(f"{Colors.OKCYAN}This agent automates the creation and deployment of your personal portfolio website.")
    print("It uses your GitHub Personal Access Token (PAT) to create a repo, commit code, and enable Pages.")
    print(f"No code is written by you. Everything is fully agentic.{Colors.ENDC}\n")
    
    # 1. Ask for credentials and info
    github_username = input(f"{Colors.BOLD}Enter your GitHub Username: {Colors.ENDC}").strip()
    if not github_username:
        print(f"{Colors.FAIL}Error: GitHub Username is required.{Colors.ENDC}")
        return
        
    github_pat = input(f"{Colors.BOLD}Enter your GitHub PAT (repo scope): {Colors.ENDC}").strip()
    if not github_pat:
        print(f"{Colors.FAIL}Error: GitHub Personal Access Token (PAT) is required.{Colors.ENDC}")
        return
        
    print(f"\n{Colors.OKBLUE}--- Profile Information ---{Colors.ENDC}")
    full_name = input(f"{Colors.BOLD}Enter your Full Name (for the bio): {Colors.ENDC}").strip()
    title = input(f"{Colors.BOLD}Enter your Professional Title (e.g. AI Engineer): {Colors.ENDC}").strip()
    location = input(f"{Colors.BOLD}Enter your Location (e.g. New York, NY): {Colors.ENDC}").strip()
    bio_summary = input(f"{Colors.BOLD}Enter a short bio / tagline: {Colors.ENDC}").strip()
    
    # Check for GEMINI_API_KEY
    gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
    if not gemini_api_key:
        print(f"\n{Colors.WARNING}⚠️ Warning: GEMINI_API_KEY environment variable not found.")
        print(f"Please obtain an API key from Google AI Studio (https://aistudio.google.com/app/api-keys){Colors.ENDC}")
        gemini_api_key = input(f"{Colors.BOLD}Or paste your Gemini API Key here (optional): {Colors.ENDC}").strip()
        if gemini_api_key:
            os.environ["GEMINI_API_KEY"] = gemini_api_key
        else:
            print(f"{Colors.FAIL}Error: Gemini API Key is required to run the agent.{Colors.ENDC}")
            return

    # Compose the prompt
    prompt = (
        f"Deploy a beautiful, modern personal bio website for me on GitHub Pages. Here are my details:\n"
        f"- Name: {full_name}\n"
        f"- Title: {title}\n"
        f"- Location: {location}\n"
        f"- Bio Tagline: {bio_summary}\n"
        f"- GitHub Username: {github_username}\n"
        f"- GitHub PAT: {github_pat}\n"
        f"- Target Repository Name: {github_username}.github.io\n\n"
        f"Please run through the full sequence: create the repo, generate index.html (including the experimental disclaimer banner), commit index.html to the repo, and activate GitHub Pages."
    )

    print(f"\n{Colors.HEADER}{Colors.BOLD}==================================================")
    print(" 🚀 Initializing Antigravity Deployment Agent...")
    print(f"=================================================={Colors.ENDC}\n")

    config = get_bio_agent_config()
    
    async with Agent(config) as agent:
        print(f"{Colors.OKBLUE}[Agent] Thinking and planning deployment sequence...{Colors.ENDC}")
        response = await agent.chat(prompt)
        
        # Stream thoughts
        print(f"\n{Colors.OKBLUE}🧠 [Agent Reasoning/Thoughts]{Colors.ENDC}")
        async for thought in response.thoughts:
            print(f"{Colors.OKCYAN}{thought}{Colors.ENDC}", end="", flush=True)
        print()

        # Stream final response
        print(f"\n{Colors.OKGREEN}📢 [Agent Response]{Colors.ENDC}")
        async for chunk in response:
            print(chunk, end="", flush=True)
        print()

    print(f"\n{Colors.OKGREEN}{Colors.BOLD}==================================================")
    print(" 🎉 Deployment Process Finished!")
    print(f" Your website will be available shortly at:")
    print(f" 👉 https://{github_username}.github.io/")
    print(f"=================================================={Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}Process cancelled by user.{Colors.ENDC}")
