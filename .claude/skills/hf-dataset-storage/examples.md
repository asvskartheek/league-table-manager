# Complete Examples for HF Dataset Storage

This file contains complete, working examples for implementing dataset storage in Hugging Face Spaces.

## Example 1: Complete Gradio App with User Feedback Storage

This example shows a complete Gradio application that collects user feedback and saves it to a dataset.

```python
# app.py
import json
import uuid
from pathlib import Path
from datetime import datetime
import gradio as gr
from huggingface_hub import CommitScheduler

# ============================================================================
# Setup Dataset Storage
# ============================================================================

# Create unique feedback file using UUID to avoid conflicts
feedback_file = Path("user_feedback") / f"feedback_{uuid.uuid4()}.jsonl"
feedback_folder = feedback_file.parent

# Create folder if it doesn't exist
feedback_folder.mkdir(parents=True, exist_ok=True)

# Initialize CommitScheduler
# This will automatically upload data every 10 minutes
scheduler = CommitScheduler(
    repo_id="your-username/app-feedback-dataset",  # Replace with your repo
    repo_type="dataset",
    folder_path=feedback_folder,
    path_in_repo="feedback",
    every=10,  # Upload every 10 minutes
)

print(f"✅ Dataset storage initialized. Data will be saved to: {scheduler.repo_id}")

# ============================================================================
# Application Logic
# ============================================================================

def translate_text(text, target_language):
    """
    Mock translation function. Replace with your actual model/API.
    """
    # Simulated translations
    translations = {
        "French": f"[FR] {text}",
        "Spanish": f"[ES] {text}",
        "German": f"[DE] {text}",
    }
    return translations.get(target_language, text)

def save_feedback(input_text, translation, language, rating, comments):
    """
    Save user feedback to the dataset with thread safety.
    """
    if not input_text or not translation:
        return "⚠️ No data to save"

    feedback_data = {
        "timestamp": datetime.now().isoformat(),
        "input_text": input_text,
        "translation": translation,
        "target_language": language,
        "rating": rating,
        "comments": comments,
        "session_id": str(uuid.uuid4())
    }

    # Use scheduler lock for thread-safe writes
    with scheduler.lock:
        with feedback_file.open("a") as f:
            f.write(json.dumps(feedback_data))
            f.write("\n")

    return "✅ Feedback saved! Thank you!"

# ============================================================================
# Gradio Interface
# ============================================================================

with gr.Blocks(title="Translation App with Feedback") as demo:
    gr.Markdown("# Translation App")
    gr.Markdown("Translate text and provide feedback to help us improve!")

    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(
                label="Enter text to translate",
                placeholder="Type something...",
                lines=3
            )
            language = gr.Dropdown(
                choices=["French", "Spanish", "German"],
                label="Target Language",
                value="French"
            )
            translate_btn = gr.Button("Translate", variant="primary")

        with gr.Column():
            output_text = gr.Textbox(
                label="Translation",
                lines=3,
                interactive=False
            )

    gr.Markdown("### How was the translation?")

    with gr.Row():
        rating = gr.Slider(
            minimum=1,
            maximum=5,
            step=1,
            label="Rating (1-5 stars)",
            value=3
        )
        comments = gr.Textbox(
            label="Additional comments (optional)",
            placeholder="Any suggestions?",
            lines=2
        )

    feedback_status = gr.Textbox(label="Status", interactive=False)
    submit_feedback_btn = gr.Button("Submit Feedback", variant="secondary")

    # Connect the functions
    translate_btn.click(
        fn=translate_text,
        inputs=[input_text, language],
        outputs=output_text
    )

    submit_feedback_btn.click(
        fn=save_feedback,
        inputs=[input_text, output_text, language, rating, comments],
        outputs=feedback_status
    )

    gr.Markdown("---")
    gr.Markdown(
        f"💾 Feedback is automatically saved to the dataset: "
        f"[{scheduler.repo_id}](https://huggingface.co/datasets/{scheduler.repo_id})"
    )

if __name__ == "__main__":
    demo.launch()
```

### Requirements for Example 1

```toml
# pyproject.toml or requirements.txt
[project]
dependencies = [
    "gradio>=4.0.0",
    "huggingface_hub>=0.20.0",
]
```

---

## Example 2: Training Logger with Dataset Storage

This example shows how to log training metrics to a dataset during model training.

```python
# train.py
import json
import time
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
from huggingface_hub import CommitScheduler

# ============================================================================
# Setup Dataset Storage for Training Logs
# ============================================================================

log_folder = Path("training_logs")
log_folder.mkdir(exist_ok=True)

# Create separate files for different log types
metrics_file = log_folder / "metrics.jsonl"
checkpoints_file = log_folder / "checkpoints.jsonl"

# Initialize scheduler - uploads every 5 minutes during training
scheduler = CommitScheduler(
    repo_id="your-username/training-logs",
    repo_type="dataset",
    folder_path=log_folder,
    path_in_repo="runs",
    every=5,
)

print(f"📊 Training logs will be saved to: {scheduler.repo_id}")

# ============================================================================
# Training Configuration
# ============================================================================

config = {
    "model": "my-model-v1",
    "learning_rate": 0.001,
    "batch_size": 32,
    "num_epochs": 10,
    "dataset": "training-data-v1"
}

# Save configuration
with scheduler.lock:
    config_file = log_folder / "config.json"
    with config_file.open("w") as f:
        json.dump(config, f, indent=2)

# ============================================================================
# Training Functions
# ============================================================================

def log_metrics(epoch, step, loss, accuracy, learning_rate):
    """Log training metrics."""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "epoch": epoch,
        "step": step,
        "loss": float(loss),
        "accuracy": float(accuracy),
        "learning_rate": learning_rate
    }

    with scheduler.lock:
        with metrics_file.open("a") as f:
            f.write(json.dumps(metrics))
            f.write("\n")

def log_checkpoint(epoch, model_path, metrics):
    """Log checkpoint information."""
    checkpoint_info = {
        "timestamp": datetime.now().isoformat(),
        "epoch": epoch,
        "model_path": model_path,
        "metrics": metrics
    }

    with scheduler.lock:
        with checkpoints_file.open("a") as f:
            f.write(json.dumps(checkpoint_info))
            f.write("\n")

def train_epoch(epoch, num_steps=100):
    """Mock training epoch."""
    epoch_loss = 0
    pbar = tqdm(range(num_steps), desc=f"Epoch {epoch}")

    for step in pbar:
        # Simulate training
        time.sleep(0.1)

        # Mock metrics
        loss = 1.0 / (step + 1 + epoch * 10)
        accuracy = min(0.95, 0.5 + step * 0.005 + epoch * 0.05)

        epoch_loss += loss

        # Log every 10 steps
        if step % 10 == 0:
            log_metrics(
                epoch=epoch,
                step=step,
                loss=loss,
                accuracy=accuracy,
                learning_rate=config["learning_rate"]
            )

        pbar.set_postfix({"loss": f"{loss:.4f}", "acc": f"{accuracy:.4f}"})

    return epoch_loss / num_steps, accuracy

# ============================================================================
# Main Training Loop
# ============================================================================

def main():
    print("🚀 Starting training...")

    for epoch in range(config["num_epochs"]):
        print(f"\n📍 Epoch {epoch + 1}/{config['num_epochs']}")

        # Train for one epoch
        avg_loss, final_accuracy = train_epoch(epoch)

        # Log checkpoint
        checkpoint_path = f"checkpoints/model_epoch_{epoch}.pt"
        log_checkpoint(
            epoch=epoch,
            model_path=checkpoint_path,
            metrics={"loss": avg_loss, "accuracy": final_accuracy}
        )

        print(f"✅ Epoch {epoch + 1} complete - Loss: {avg_loss:.4f}, Acc: {final_accuracy:.4f}")

    print(f"\n🎉 Training complete! Logs saved to: {scheduler.repo_id}")

    # Force final upload
    # Note: scheduler will upload automatically, but we can trigger it manually if needed
    print("📤 Uploading final logs...")
    time.sleep(2)  # Give scheduler time to complete

if __name__ == "__main__":
    main()
```

---

## Example 3: Dataset Snapshot Saver

This example shows how to create versioned snapshots of data.

```python
# snapshot_saver.py
import json
from pathlib import Path
from datetime import datetime
from huggingface_hub import HfApi
from tqdm import tqdm

class DatasetSnapshotSaver:
    """Save versioned snapshots of data to HuggingFace datasets."""

    def __init__(self, repo_id, repo_type="dataset"):
        self.api = HfApi()
        self.repo_id = repo_id
        self.repo_type = repo_type

        # Create repo if it doesn't exist
        try:
            self.api.create_repo(
                repo_id=repo_id,
                repo_type=repo_type,
                exist_ok=True
            )
            print(f"✅ Repository ready: {repo_id}")
        except Exception as e:
            print(f"❌ Error creating repo: {e}")

    def save_snapshot(self, data_folder, snapshot_name=None):
        """
        Save a snapshot of the data folder to the dataset.

        Args:
            data_folder: Path to local folder containing data
            snapshot_name: Optional custom name, defaults to timestamp
        """
        if snapshot_name is None:
            snapshot_name = datetime.now().strftime("%Y%m%d_%H%M%S")

        data_path = Path(data_folder)
        if not data_path.exists():
            raise ValueError(f"Data folder not found: {data_folder}")

        print(f"📸 Creating snapshot: {snapshot_name}")

        # Upload folder
        self.api.upload_folder(
            folder_path=str(data_path),
            path_in_repo=f"snapshots/{snapshot_name}",
            repo_id=self.repo_id,
            repo_type=self.repo_type,
            commit_message=f"Snapshot: {snapshot_name}"
        )

        print(f"✅ Snapshot saved: snapshots/{snapshot_name}")
        return snapshot_name

    def save_metadata(self, snapshot_name, metadata):
        """Save metadata for a snapshot."""
        metadata_content = json.dumps(metadata, indent=2)

        self.api.upload_file(
            path_or_fileobj=metadata_content.encode(),
            path_in_repo=f"snapshots/{snapshot_name}/metadata.json",
            repo_id=self.repo_id,
            repo_type=self.repo_type,
            commit_message=f"Add metadata for {snapshot_name}"
        )

        print(f"✅ Metadata saved for snapshot: {snapshot_name}")

# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    # Initialize saver
    saver = DatasetSnapshotSaver(
        repo_id="your-username/data-snapshots"
    )

    # Create sample data
    data_folder = Path("./sample_data")
    data_folder.mkdir(exist_ok=True)

    # Generate some sample files
    print("📝 Generating sample data...")
    for i in tqdm(range(10)):
        sample_file = data_folder / f"data_{i}.json"
        with sample_file.open("w") as f:
            json.dump({"id": i, "value": i * 10}, f)

    # Save snapshot
    snapshot_name = saver.save_snapshot(
        data_folder=data_folder,
        snapshot_name="initial_snapshot"
    )

    # Save metadata
    saver.save_metadata(
        snapshot_name=snapshot_name,
        metadata={
            "created_at": datetime.now().isoformat(),
            "num_files": 10,
            "description": "Initial data snapshot",
            "version": "1.0"
        }
    )

    print(f"\n🎉 Complete! View at: https://huggingface.co/datasets/{saver.repo_id}")
```

---

## Example 4: Image Collection Archiver

This example shows how to collect images and periodically archive them to a dataset.

```python
# image_archiver.py
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
from huggingface_hub import CommitScheduler

class ImageArchiveScheduler(CommitScheduler):
    """
    Custom scheduler that collects images and uploads them as ZIP archives.
    """

    def push_to_hub(self):
        """Override to zip images before uploading."""

        # Find all image files
        image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.gif"]
        image_files = []
        for ext in image_extensions:
            image_files.extend(list(self.folder_path.glob(ext)))

        if len(image_files) == 0:
            print("No images to archive")
            return None

        print(f"📦 Archiving {len(image_files)} images...")

        # Create ZIP archive
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"images_{timestamp}.zip"

        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = Path(tmpdir) / archive_name

            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for img_file in image_files:
                    zip_file.write(
                        filename=img_file,
                        arcname=f"{timestamp}/{img_file.name}"
                    )

            # Upload archive
            self.api.upload_file(
                path_or_fileobj=str(archive_path),
                path_in_repo=f"{self.path_in_repo}/{archive_name}",
                repo_id=self.repo_id,
                repo_type=self.repo_type,
                commit_message=f"Archive {len(image_files)} images from {timestamp}"
            )

        # Delete local images after successful upload
        for img_file in image_files:
            img_file.unlink()

        print(f"✅ Archived and uploaded {len(image_files)} images")

# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    import time
    from PIL import Image
    import numpy as np

    # Setup image folder
    image_folder = Path("./collected_images")
    image_folder.mkdir(exist_ok=True)

    # Initialize custom scheduler
    scheduler = ImageArchiveScheduler(
        repo_id="your-username/image-archives",
        repo_type="dataset",
        folder_path=image_folder,
        path_in_repo="archives",
        every=5,  # Archive every 5 minutes
    )

    print(f"📸 Image archiver started. Saving to: {scheduler.repo_id}")

    # Simulate image collection
    print("Generating sample images...")
    for i in range(5):
        # Create a random image
        img_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)

        # Save image
        img_path = image_folder / f"image_{i}_{datetime.now().strftime('%H%M%S')}.png"
        img.save(img_path)
        print(f"  Generated: {img_path.name}")

        time.sleep(2)

    print("\n⏳ Waiting for scheduler to archive images...")
    print("   (In production, your app would continue running)")

    # In a real application, the scheduler runs in the background
    # and you can continue processing
```

---

## Example 5: A/B Testing Results Collector

This example shows how to collect A/B testing results from a Gradio Space.

```python
# ab_testing_app.py
import json
import uuid
import random
from pathlib import Path
from datetime import datetime
import gradio as gr
from huggingface_hub import CommitScheduler

# ============================================================================
# Setup Dataset Storage for A/B Testing
# ============================================================================

results_folder = Path("ab_test_results")
results_folder.mkdir(exist_ok=True)

results_file = results_folder / f"results_{uuid.uuid4()}.jsonl"

scheduler = CommitScheduler(
    repo_id="your-username/ab-test-results",
    repo_type="dataset",
    folder_path=results_folder,
    path_in_repo="experiments",
    every=10,
)

print(f"📊 A/B test results will be saved to: {scheduler.repo_id}")

# ============================================================================
# A/B Testing Logic
# ============================================================================

def assign_variant():
    """Randomly assign user to variant A or B."""
    return random.choice(["A", "B"])

def get_recommendation(user_input, variant):
    """
    Generate recommendation based on variant.
    Variant A: Conservative recommendations
    Variant B: Aggressive recommendations
    """
    if variant == "A":
        return f"Conservative recommendation for: {user_input}"
    else:
        return f"Aggressive recommendation for: {user_input}"

def log_interaction(session_id, variant, user_input, recommendation, user_clicked):
    """Log A/B test interaction."""
    result = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "variant": variant,
        "user_input": user_input,
        "recommendation": recommendation,
        "user_clicked": user_clicked,
        "conversion": user_clicked
    }

    with scheduler.lock:
        with results_file.open("a") as f:
            f.write(json.dumps(result))
            f.write("\n")

# ============================================================================
# Gradio Interface
# ============================================================================

def process_request(user_input, session_state):
    """Process user request and assign variant."""
    if session_state is None:
        session_state = {
            "session_id": str(uuid.uuid4()),
            "variant": assign_variant()
        }

    recommendation = get_recommendation(user_input, session_state["variant"])

    return (
        recommendation,
        f"You are in variant: {session_state['variant']}",
        session_state,
        session_state["session_id"],
        session_state["variant"],
        user_input,
        recommendation
    )

def log_click(session_id, variant, user_input, recommendation):
    """Log when user clicks the recommendation."""
    if session_id:
        log_interaction(session_id, variant, user_input, recommendation, True)
        return "✅ Click logged!"
    return "⚠️ No session data"

with gr.Blocks(title="A/B Testing Demo") as demo:
    gr.Markdown("# A/B Testing Demo")
    gr.Markdown("Test two different recommendation strategies")

    # Session state
    session_state = gr.State(None)
    session_id_state = gr.State(None)
    variant_state = gr.State(None)
    input_state = gr.State(None)
    recommendation_state = gr.State(None)

    with gr.Row():
        user_input = gr.Textbox(
            label="What are you looking for?",
            placeholder="Enter your query..."
        )
        submit_btn = gr.Button("Get Recommendation", variant="primary")

    recommendation_output = gr.Textbox(
        label="Recommendation",
        interactive=False
    )

    variant_display = gr.Textbox(
        label="Your Test Variant",
        interactive=False
    )

    click_btn = gr.Button("I like this recommendation!", variant="secondary")
    click_status = gr.Textbox(label="Status", interactive=False)

    # Connect functions
    submit_btn.click(
        fn=process_request,
        inputs=[user_input, session_state],
        outputs=[
            recommendation_output,
            variant_display,
            session_state,
            session_id_state,
            variant_state,
            input_state,
            recommendation_state
        ]
    )

    click_btn.click(
        fn=log_click,
        inputs=[session_id_state, variant_state, input_state, recommendation_state],
        outputs=click_status
    )

    gr.Markdown("---")
    gr.Markdown(f"📊 Results are saved to: [{scheduler.repo_id}](https://huggingface.co/datasets/{scheduler.repo_id})")

if __name__ == "__main__":
    demo.launch()
```

---

## Running the Examples

For any of these examples:

1. **Install dependencies:**
   ```bash
   uv add gradio huggingface_hub
   # For image example: uv add pillow numpy
   ```

2. **Login to Hugging Face:**
   ```bash
   huggingface-cli login
   ```

3. **Update repo_id:**
   Replace `"your-username/repo-name"` with your actual HuggingFace username and desired dataset name.

4. **Run the script:**
   ```bash
   uv run app.py
   ```

5. **View results:**
   Visit `https://huggingface.co/datasets/your-username/repo-name` to see your data!
