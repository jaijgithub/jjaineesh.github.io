#!/usr/bin/env python3
"""
Setup script for PM Resume Agent
"""

import os
import shutil
import json
from pathlib import Path


def create_user_profile():
    """Create a personalized user profile from template."""
    template_path = "examples/user_profile_template.json"
    output_path = "my_profile.json"
    
    if os.path.exists(output_path):
        response = input(f"{output_path} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Skipping profile creation.")
            return
    
    # Copy template
    shutil.copy(template_path, output_path)
    print(f"✓ Created {output_path} from template")
    print(f"  Please edit {output_path} with your information")


def create_job_description_file():
    """Create a job description file."""
    output_path = "job_description.txt"
    
    if os.path.exists(output_path):
        response = input(f"{output_path} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Skipping job description creation.")
            return
    
    print("Enter the job description (paste the full text, then press Ctrl+D on a new line):")
    print("=" * 60)
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    job_description = '\n'.join(lines)
    
    with open(output_path, 'w') as f:
        f.write(job_description)
    
    print(f"\n✓ Created {output_path}")
    print(f"  Job description saved ({len(job_description)} characters)")


def run_example():
    """Run the agent with example data."""
    print("Running PM Resume Agent with example data...")
    
    cmd = (
        "python3 pm_resume_agent.py "
        "--profile examples/user_profile_template.json "
        "--job-description examples/sample_job_description.txt "
        "--output example_tailored_resume.md"
    )
    
    print(f"Command: {cmd}")
    os.system(cmd)


def main():
    """Main setup function."""
    print("🚀 PM Resume Agent Setup")
    print("=" * 40)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Create user profile from template")
        print("2. Create job description file")
        print("3. Run example with sample data")
        print("4. Show usage instructions")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            create_user_profile()
        elif choice == '2':
            create_job_description_file()
        elif choice == '3':
            run_example()
        elif choice == '4':
            show_usage()
        elif choice == '5':
            print("Setup complete! 🎉")
            break
        else:
            print("Invalid choice. Please enter 1-5.")


def show_usage():
    """Show usage instructions."""
    print("\n📖 Usage Instructions")
    print("=" * 40)
    print()
    print("1. Basic usage:")
    print("   python3 pm_resume_agent.py --profile my_profile.json --job-description job_description.txt")
    print()
    print("2. Specify output file:")
    print("   python3 pm_resume_agent.py --profile my_profile.json --job-description job_description.txt --output my_resume.md")
    print()
    print("3. JSON output format:")
    print("   python3 pm_resume_agent.py --profile my_profile.json --job-description job_description.txt --format json")
    print()
    print("4. Add focus areas:")
    print("   python3 pm_resume_agent.py --profile my_profile.json --job-description job_description.txt --focus \"agile\" \"data analysis\"")
    print()
    print("For more information, see README.md")


if __name__ == "__main__":
    main()