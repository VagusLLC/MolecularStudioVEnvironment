#!/usr/bin/env python3
"""
Script to populate Jinja2 templates with user-provided values.
This script checks for a .env file first, then prompts the user for any missing variables.
"""

import os
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_vars = {}
    env_file = Path('.env')
    
    if env_file.exists():
        print("📁 Found .env file, loading environment variables...")
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        env_vars[key] = value
            print(f"✓ Loaded {len(env_vars)} variable(s) from .env file")
        except Exception as e:
            print(f"⚠️  Warning: Could not read .env file: {e}")
            env_vars = {}
    else:
        print("📁 No .env file found")
    
    return env_vars


def get_user_input(env_vars):
    """Prompt the user for any missing required variables."""
    print("🔧 Checking for required variables...")
    print()
    
    # Check if MongoURI is already loaded from .env
    if 'MONGO_URI' in env_vars:
        print("✓ MONGO_URI found in .env file")
        mongo_uri = env_vars['MONGO_URI']
    else:
        # Prompt for MongoURI if not in .env
        print("❓ MONGO_URI not found in .env file, please enter it:")
        while True:
            mongo_uri = input("Please enter your MongoDB URI: ").strip()
            if mongo_uri:
                # Basic validation - check if it looks like a MongoDB URI
                if mongo_uri.startswith(('mongodb://', 'mongodb+srv://')):
                    break
                else:
                    print("⚠️  Warning: This doesn't look like a standard MongoDB URI.")
                    confirm = input("Continue anyway? (y/N): ").strip().lower()
                    if confirm in ['y', 'yes']:
                        break
            else:
                print("❌ MongoURI cannot be empty. Please try again.")
        
        # Add to env_vars dictionary
        env_vars['MONGO_URI'] = mongo_uri
        print(f"✓ MongoURI loaded successfully")
    if 'MONGO_DOCS_COLLECTION' in env_vars:
        print("✓ MONGO_DOCS_COLLECTION found in .env file")
        mongo_docs_collection = env_vars['MONGO_DOCS_COLLECTION']
    else:
        print("❓ MONGO_DOCS_COLLECTION not found in .env file, please enter it:")
        mongo_docs_collection = input("Please enter your MongoDB collection name: ").strip()
        env_vars['MONGO_DOCS_COLLECTION'] = mongo_docs_collection
        print(f"✓ MONGO_DOCS_COLLECTION loaded successfully")
    return env_vars


def render_template(template_path, output_path, env_vars):
    """Render a Jinja2 template with environment variables."""
    try:
        # Set up Jinja2 environment
        template_dir = Path(template_path).parent
        template_name = Path(template_path).name
        
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        template = env.get_template(template_name)
        
        # Render template with environment variables
        rendered_content = template.render(**env_vars)
        
        # Write rendered content to output file
        with open(output_path, 'w') as f:
            f.write(rendered_content)
        
        print(f"✓ Successfully rendered {template_path} -> {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error rendering {template_path}: {e}")
        return False


def main():
    """Main function to populate all templates."""
    # Load environment variables from .env file
    env_vars = load_env_file()
    
    # Get any missing user input
    env_vars = get_user_input(env_vars)
    
    print(f"\nLoaded {len(env_vars)} value(s) total")
    
    # Define template mappings
    templates = [
        ("my_launchpad.yaml.j2", "my_launchpad.yaml"),
        ("jobflow.yaml.j2", "jobflow.yaml")
    ]
    
    # Render each template
    success_count = 0
    for template_path, output_path in templates:
        if os.path.exists(template_path):
            if render_template(template_path, output_path, env_vars):
                success_count += 1
        else:
            print(f"⚠️  Template {template_path} not found, skipping...")
    
    print(f"\n🎉 Completed! Successfully rendered {success_count}/{len(templates)} templates.")
    
    # Show which values were used
    print("\n📋 Values used:")
    for key, value in env_vars.items():
        # Mask sensitive values
        if any(sensitive in key.lower() for sensitive in ['password', 'secret', 'key', 'token', 'uri']):
            masked_value = '*' * min(len(value), 8) if value else 'None'
            print(f"  {key}: {masked_value}")
        else:
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()

