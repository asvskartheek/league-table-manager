#!/usr/bin/env python3
"""
Demo script showing HuggingFace Dataset Storage patterns.
This demonstrates the skill's capabilities without requiring actual HF authentication.
"""

import json
from pathlib import Path
from datetime import datetime


def demo_file_structure():
    """Show how to structure files for dataset storage."""
    print("=" * 60)
    print("📁 File Structure Demo")
    print("=" * 60)

    # Example 1: JSON Lines format (recommended for append-only data)
    demo_folder = Path("demo_data")
    demo_folder.mkdir(exist_ok=True)

    # Create sample JSONL file
    sample_file = demo_folder / "sample_data.jsonl"
    sample_data = [
        {"id": 1, "timestamp": datetime.now().isoformat(), "value": "first entry"},
        {"id": 2, "timestamp": datetime.now().isoformat(), "value": "second entry"},
        {"id": 3, "timestamp": datetime.now().isoformat(), "value": "third entry"},
    ]

    with sample_file.open("w") as f:
        for entry in sample_data:
            f.write(json.dumps(entry))
            f.write("\n")

    print(f"✅ Created sample JSONL file: {sample_file}")
    print(f"   Contains {len(sample_data)} entries\n")

    # Show the content
    print("📄 File contents:")
    print(sample_file.read_text())
    print()


def demo_scheduler_pattern():
    """Show the CommitScheduler pattern (without actual upload)."""
    print("=" * 60)
    print("🔄 CommitScheduler Pattern")
    print("=" * 60)

    code_example = '''
from pathlib import Path
from huggingface_hub import CommitScheduler

# Setup
feedback_folder = Path("user_feedback")
feedback_file = feedback_folder / "data.jsonl"

# Create scheduler (uploads every 10 minutes)
scheduler = CommitScheduler(
    repo_id="username/my-dataset",
    repo_type="dataset",
    folder_path=feedback_folder,
    path_in_repo="feedback",
    every=10,
)

# Save data with thread safety
def save_feedback(data):
    with scheduler.lock:
        with feedback_file.open("a") as f:
            f.write(json.dumps(data))
            f.write("\\n")
'''

    print("💡 Recommended Pattern for Continuous Data Collection:")
    print(code_example)
    print()


def demo_manual_upload_pattern():
    """Show manual upload patterns."""
    print("=" * 60)
    print("📤 Manual Upload Pattern")
    print("=" * 60)

    code_example = '''
from huggingface_hub import HfApi

api = HfApi()

# Method 1: Upload single file
api.upload_file(
    path_or_fileobj="data.json",
    path_in_repo="data/data.json",
    repo_id="username/my-dataset",
    repo_type="dataset",
)

# Method 2: Upload entire folder
api.upload_folder(
    folder_path="./my_data",
    repo_id="username/my-dataset",
    repo_type="dataset",
)

# Method 3: Large folder (resumable)
api.upload_large_folder(
    repo_id="username/huge-dataset",
    folder_path="/path/to/huge/folder",
    repo_type="dataset",
    num_workers=4,
)
'''

    print("💡 Manual Upload Options:")
    print(code_example)
    print()


def demo_use_cases():
    """Show common use cases."""
    print("=" * 60)
    print("🎯 Common Use Cases")
    print("=" * 60)

    use_cases = {
        "1. Gradio Space User Feedback": {
            "description": "Collect and store user interactions",
            "pattern": "CommitScheduler",
            "frequency": "Every 10-15 minutes",
            "format": "JSON Lines (.jsonl)",
        },
        "2. Training Logs": {
            "description": "Store model training metrics over time",
            "pattern": "CommitScheduler",
            "frequency": "Every 5 minutes",
            "format": "JSON Lines (.jsonl) or CSV",
        },
        "3. A/B Testing Results": {
            "description": "Track experiment variants and conversions",
            "pattern": "CommitScheduler",
            "frequency": "Every 10 minutes",
            "format": "JSON Lines (.jsonl)",
        },
        "4. Dataset Versioning": {
            "description": "Create snapshots of evolving datasets",
            "pattern": "Manual upload_folder()",
            "frequency": "On-demand",
            "format": "Any format (Parquet recommended)",
        },
        "5. Image Collection": {
            "description": "Archive images periodically",
            "pattern": "Custom Scheduler (zip files)",
            "frequency": "Every 15 minutes",
            "format": "ZIP archives",
        },
    }

    for use_case, details in use_cases.items():
        print(f"\n{use_case}")
        print(f"  📝 {details['description']}")
        print(f"  🔧 Pattern: {details['pattern']}")
        print(f"  ⏱️  Frequency: {details['frequency']}")
        print(f"  📄 Format: {details['format']}")

    print()


def demo_best_practices():
    """Show best practices."""
    print("=" * 60)
    print("⭐ Best Practices")
    print("=" * 60)

    practices = [
        "✅ Use UUID filenames to avoid conflicts across restarts",
        "✅ Always use scheduler.lock for thread-safe writes",
        "✅ Use JSON Lines (.jsonl) for structured append-only data",
        "✅ Set minimum upload frequency to 5 minutes",
        "✅ Never delete or overwrite files with CommitScheduler",
        "✅ Use upload_large_folder() for datasets > 1GB",
        "✅ Store HF_TOKEN as environment variable or Space secret",
        "✅ Use Parquet format for very large tabular datasets",
    ]

    for practice in practices:
        print(f"  {practice}")

    print()


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 60)
    print("🚀 HuggingFace Dataset Storage Skill Demo")
    print("=" * 60)
    print()

    demo_file_structure()
    demo_scheduler_pattern()
    demo_manual_upload_pattern()
    demo_use_cases()
    demo_best_practices()

    print("=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)
    print()
    print("📚 For more information, see:")
    print("   - examples.md: Complete working examples")
    print("   - reference.md: Detailed API documentation")
    print("   - SKILL.md: Quick start guide")
    print()


if __name__ == "__main__":
    main()
