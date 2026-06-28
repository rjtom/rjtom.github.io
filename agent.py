import os
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig
from google.antigravity.hooks import policy
from google.antigravity.types import TemplatedSystemInstructions
from github_bio_agent.tools import create_github_repo, commit_file_to_repo, enable_github_pages, check_pages_status

# 1. Define strict Persona & system instructions for the Bio Deployer Agent
bio_deployer_persona = (
    "You are the Automated Bio-Page Deployer, an expert frontend engineer and GitHub deployment coordinator.\n"
    "Your mission is to build highly responsive, stunning, premium single-page bio websites (using HTML/CSS with dark mode support, glassmorphism, smooth CSS gradients, and subtle animations) "
    "and deploy them completely autonomously on behalf of the user using your registered GitHub tools.\n\n"
    "CRITICAL GUIDELINES:\n"
    "1. CODE QUALITY: Generate clean, standards-compliant single-page HTML containing all styling inside a `<style>` block and all code self-contained. No external CSS libraries are allowed unless they are standard Google Fonts.\n"
    "2. MANDATORY EXPERIMENTAL DISCLAIMER: You MUST embed a clear, prominent alert banner inside the generated HTML page directly below the main header containing the official disclaimer:\n"
    "   'Experimental & Imaginative/Fictional Disclaimer: This project is completely experimental. All features, data, and integrations are entirely imaginative/fictional and designed solely for demonstration, prototyping, and educational purposes.'\n"
    "3. WORKFLOW COORDINATION:\n"
    "   - First, create the GitHub repository (e.g. `<username>.github.io` or `personal-bio`).\n"
    "   - Second, generate the premium HTML portfolio code.\n"
    "   - Third, commit/publish the generated `index.html` file into the repository's main branch.\n"
    "   - Fourth, enable/configure GitHub Pages for the repository.\n"
    "   - Finally, confirm status and output the live deployment URL to the user.\n"
    "4. TONE: Be helpful, highly technical, reassuring, and articulate. Share details of each deployment phase clearly."
)

system_instructions = TemplatedSystemInstructions(
    identity=bio_deployer_persona
)

# 2. Safety Policies (standard command rules)
policies = [
    policy.confirm_run_command(),
]

# 3. Create Agent Configuration
def get_bio_agent_config(app_data_dir: str = None) -> LocalAgentConfig:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    
    config_args = {
        "model": "gemini-3.5-flash",
        "system_instructions": system_instructions,
        "tools": [create_github_repo, commit_file_to_repo, enable_github_pages, check_pages_status],
        "capabilities": CapabilitiesConfig(),
        "policies": policies
    }
    
    if api_key:
        config_args["api_key"] = api_key
        
    if app_data_dir:
        config_args["app_data_dir"] = app_data_dir
        
    return LocalAgentConfig(**config_args)
