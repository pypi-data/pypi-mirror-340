import click
import os
import shutil
from pathlib import Path
import subprocess

# Define template structures (can be more sophisticated, maybe load from files)
TEMPLATES = {
    "standard-ml": {
        "dirs": [
            "config", "data/raw", "data/processed", "data/external",
            "notebooks", "src", "tests", "models"
        ],
        "files": {
            ".gitignore": "# Python\n__pycache__/\n*.py[cod]\n*$py.class\n\n# Environment\n.env\n.venv\nvenv/\nENV/\nenv/\n\n# Data & Models (often large/private - uncomment if needed)\n# data/\n# models/\n\n# Notebook Checkpoints\n.ipynb_checkpoints",
            "README.md": "# Project Title\n\nDescription...",
            "requirements.txt": "pandas\nnumpy\nscikit-learn\n# Add other core libraries",
            "config/config.yaml": "# Configuration settings\nparam1: value1",
            "notebooks/1.0-data-exploration.ipynb": '{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}', # Basic empty notebook
            "src/__init__.py": "",
            "src/data_loader.py": "# Data loading functions",
            "src/preprocessing.py": "# Data preprocessing functions",
            "src/model.py": "# Model definition",
            "src/train.py": "# Training script logic",
            "src/predict.py": "# Prediction script logic",
            "src/utils.py": "# Utility functions",
            "tests/__init__.py": "",
        }
    },
    "ai-agent": {
        "dirs": [
            "config", "data/knowledge_base", "notebooks",
            "src/agent", "src/tools", "src/prompts", "src/memory", "tests"
        ],
        "files": {
            ".gitignore": "# Python\n__pycache__/\n*.py[cod]\n*$py.class\n\n# Environment\n.env\n.venv\nvenv/\nENV/\nenv/\n\n# Sensitive Info\n*.log\n.env*\n!env.example\n\n# Notebook Checkpoints\n.ipynb_checkpoints",
            "README.md": "# AI Agent Project\n\nDescription...",
            "requirements.txt": "# langchain\n# openai\n# python-dotenv\n# Add other core libraries",
            ".env.example": "OPENAI_API_KEY='YOUR_API_KEY_HERE'",
            "config/agent_config.yaml": "model: 'gpt-4'\ntemperature: 0.7",
            "notebooks/agent_testing.ipynb": '{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}',
            "src/__init__.py": "",
            "src/agent/__init__.py": "",
            "src/agent/core.py": "# Core agent logic here",
            "src/tools/__init__.py": "",
            "src/tools/example_tool.py": "# Define agent tools here",
            "src/prompts/__init__.py": "",
            "src/prompts/system_prompt.txt": "You are a helpful AI assistant.",
            "src/prompts/user_template.txt": "User query: {query}",
            "src/memory/__init__.py": "",
            "src/utils.py": "# Utility functions",
            "src/main.py": "# Main entry point to run the agent",
            "tests/__init__.py": "",
        }
    }
    # Add more templates here
}

@click.command()
@click.argument('project_name')
@click.option('--template', '-t', default='standard-ml', type=click.Choice(TEMPLATES.keys()), help='Project template to use.')
@click.option('--git', is_flag=True, help='Initialize a git repository.')
def main(project_name, template, git):
    """Creates a standard ML/AI project structure."""
    base_path = Path(project_name)
    template_data = TEMPLATES.get(template)

    if not template_data:
        click.echo(f"Error: Template '{template}' not found.", err=True)
        return

    # Check if directory exists
    if base_path.exists():
        click.echo(f"Error: Directory '{project_name}' already exists.", err=True)
        return

    try:
        # Create root directory
        base_path.mkdir(parents=True)
        click.echo(f"Created project directory: {base_path}")

        # Create subdirectories
        for dir_path in template_data.get("dirs", []):
            (base_path / dir_path).mkdir(parents=True, exist_ok=True)
            click.echo(f"  Created dir:  {base_path / dir_path}")

        # Create files
        for file_path, content in template_data.get("files", {}).items():
            full_file_path = base_path / file_path
            # Ensure parent directory exists (important for nested files like src/...)
            full_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_file_path, 'w') as f:
                f.write(content)
            click.echo(f"  Created file: {full_file_path}")

        # Initialize git if requested
        if git:
            try:
                subprocess.run(['git', 'init'], cwd=str(base_path), check=True, capture_output=True)
                click.echo("Initialized git repository.")
                # Optional: Add and commit initial files
                # subprocess.run(['git', 'add', '.'], cwd=str(base_path), check=True)
                # subprocess.run(['git', 'commit', '-m', 'Initial commit from init-ml-app'], cwd=str(base_path), check=True)
                # click.echo("Added initial files to git.")
            except FileNotFoundError:
                click.echo("Warning: 'git' command not found. Could not initialize repository.", err=True)
            except subprocess.CalledProcessError as e:
                 click.echo(f"Warning: Git initialization failed: {e.stderr.decode()}", err=True)


        click.echo(f"\nSuccess! Project '{project_name}' created with template '{template}'.")
        click.echo("\nNext steps:")
        click.echo(f"  cd {project_name}")
        click.echo("  # Consider creating and activating a virtual environment:")
        click.echo("  # python -m venv .venv")
        click.echo("  # source .venv/bin/activate  (or .\\venv\\Scripts\\activate on Windows)")
        click.echo("  pip install -r requirements.txt")
        if template == "ai-agent":
             click.echo("  # Remember to create a .env file from .env.example and add your API keys!")


    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)
        # Optional: Clean up created directory on failure
        # shutil.rmtree(base_path)

if __name__ == '__main__':
    main()