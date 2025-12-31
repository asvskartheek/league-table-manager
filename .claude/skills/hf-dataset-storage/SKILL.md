---
name: hf-dataset-storage
description: Implement persistent storage for Hugging Face Spaces using dataset storage. Use when working with HF Spaces persistence, saving space data to datasets, scheduled uploads to HuggingFace Hub, or when the user mentions dataset storage, space persistence, CommitScheduler, or backing up space data.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Hugging Face Dataset Storage for Spaces

This skill helps you implement persistent storage for Hugging Face Spaces using dataset repositories as a data store.

## When to Use Dataset Storage

Use dataset storage for Hugging Face Spaces when:
- You need data to persist beyond the Space's lifecycle
- You want to collect user feedback or logs from a Space
- You need append-only storage for analytics or training data
- You want to avoid paying for persistent storage upgrades
- You need to version your data over time

## Quick Start

### 1. Install Required Package

```bash
uv add huggingface_hub
```

### 2. Basic Setup with CommitScheduler (Recommended)

For append-only data that should be uploaded periodically (e.g., logs, user feedback):

```python
import json
import uuid
from pathlib import Path
from huggingface_hub import CommitScheduler

# Create a unique file to avoid conflicts across restarts
feedback_file = Path("user_feedback/") / f"data_{uuid.uuid4()}.json"
feedback_folder = feedback_file.parent

# Schedule uploads every 10 minutes (minimum recommended: 5 minutes)
scheduler = CommitScheduler(
    repo_id="username/my-dataset",  # Will be created if doesn't exist
    repo_type="dataset",
    folder_path=feedback_folder,
    path_in_repo="data",  # Upload to /data folder in the dataset
    every=10,  # Upload every 10 minutes
)

# Append data with thread safety
def save_data(data_dict):
    """Save data to file with thread lock for concurrent writes."""
    with scheduler.lock:
        with feedback_file.open("a") as f:
            f.write(json.dumps(data_dict))
            f.write("\n")
```

### 3. Manual Upload Methods

For one-time or controlled uploads:

```python
from huggingface_hub import HfApi

api = HfApi()

# Upload a single file
api.upload_file(
    path_or_fileobj="/path/to/local/file.json",
    path_in_repo="data/file.json",
    repo_id="username/my-dataset",
    repo_type="dataset",
)

# Upload an entire folder
api.upload_folder(
    folder_path="/path/to/local/folder",
    path_in_repo="data",
    repo_id="username/my-dataset",
    repo_type="dataset",
)
```

## Authentication

Before uploading, you need to authenticate with Hugging Face:

### Option 1: Login via CLI
```bash
huggingface-cli login
```

### Option 2: Use Token Programmatically
```python
from huggingface_hub import HfApi

api = HfApi(token="hf_...")
```

### Option 3: Set Environment Variable
```bash
export HF_TOKEN="hf_..."
```

For Spaces, add `HF_TOKEN` as a secret in Space settings.

## Advanced Patterns

### Pattern 1: Gradio Space with User Feedback

```python
import json
import uuid
from pathlib import Path
import gradio as gr
from huggingface_hub import CommitScheduler

# Setup
feedback_file = Path("user_feedback/") / f"data_{uuid.uuid4()}.json"
feedback_folder = feedback_file.parent

scheduler = CommitScheduler(
    repo_id="username/user-feedback-dataset",
    repo_type="dataset",
    folder_path=feedback_folder,
    path_in_repo="feedback",
    every=10,
)

def save_feedback(input_text, output_text, rating):
    """Save user feedback with thread safety."""
    with scheduler.lock:
        with feedback_file.open("a") as f:
            f.write(json.dumps({
                "input": input_text,
                "output": output_text,
                "rating": rating,
                "timestamp": str(uuid.uuid4())
            }))
            f.write("\n")

# Use in Gradio interface
with gr.Blocks() as demo:
    # ... define your Gradio UI
    submit_btn.click(save_feedback, inputs=[input_box, output_box, rating])

demo.launch()
```

### Pattern 2: Training Logs with Progress Tracking

```python
import json
from pathlib import Path
from huggingface_hub import CommitScheduler
from tqdm import tqdm

# Setup
log_file = Path("training_logs/") / "metrics.jsonl"
log_folder = log_file.parent
log_folder.mkdir(exist_ok=True)

scheduler = CommitScheduler(
    repo_id="username/training-logs",
    repo_type="dataset",
    folder_path=log_folder,
    path_in_repo="logs",
    every=5,  # Upload every 5 minutes
)

# Training loop
for epoch in tqdm(range(num_epochs), desc="Training"):
    # ... training code ...

    # Log metrics
    with scheduler.lock:
        with log_file.open("a") as f:
            f.write(json.dumps({
                "epoch": epoch,
                "loss": loss,
                "accuracy": accuracy
            }))
            f.write("\n")
```

### Pattern 3: Large File Upload with Background Processing

```python
from huggingface_hub import HfApi

api = HfApi()

# Upload large files in the background (non-blocking)
future = api.upload_folder(
    repo_id="username/large-dataset",
    folder_path="./data",
    repo_type="dataset",
    run_as_future=True,  # Non-blocking upload
)

# Continue working while upload happens
# ... do other work ...

# Wait for upload to complete when needed
future.result()  # This blocks until upload finishes
```

### Pattern 4: Scheduled Uploads with Multiple File Types

```python
import zipfile
import tempfile
from pathlib import Path
from huggingface_hub import CommitScheduler

class ImageArchiveScheduler(CommitScheduler):
    """Custom scheduler that zips images before uploading."""

    def push_to_hub(self):
        # Find all PNG files
        png_files = list(self.folder_path.glob("*.png"))
        if len(png_files) == 0:
            return None  # Skip if nothing to commit

        # Zip files
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = Path(tmpdir) / "images.zip"
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for png_file in png_files:
                    zip_file.write(filename=png_file, arcname=png_file.name)

            # Upload archive
            self.api.upload_file(
                path_or_fileobj=archive_path,
                path_in_repo=f"{self.path_in_repo}/images.zip",
                repo_id=self.repo_id,
                repo_type=self.repo_type,
            )

        # Clean up local files
        for png_file in png_files:
            png_file.unlink()

# Usage
scheduler = ImageArchiveScheduler(
    repo_id="username/image-dataset",
    repo_type="dataset",
    folder_path=Path("./images"),
    path_in_repo="archives",
    every=15,
)
```

## Best Practices

### 1. File Naming for Concurrent Access
Always use UUIDs or timestamps to avoid filename conflicts:
```python
import uuid
filename = f"data_{uuid.uuid4()}.json"
```

### 2. Thread Safety
Always use the scheduler lock when writing:
```python
with scheduler.lock:
    with file.open("a") as f:
        f.write(data)
```

### 3. Append-Only Data
CommitScheduler assumes append-only operations. Only:
- Create new files
- Append to existing files
- Never delete or overwrite files (this can corrupt the repo)

### 4. Upload Frequency
- Minimum recommended: 5 minutes
- For user-facing apps: 10-15 minutes
- For training logs: 5-10 minutes

### 5. Data Format
Use formats readable by the Datasets library:
- JSON Lines (`.jsonl`) for structured data
- CSV for tabular data
- Parquet for large datasets
- ZIP for grouped files

### 6. Error Handling
The scheduler silently handles errors and retries. For critical data:
```python
import logging

logging.basicConfig(level=logging.INFO)
# Scheduler will log errors automatically
```

### 7. Large Files
For very large datasets (>1GB), consider:
```python
from huggingface_hub import HfApi

api = HfApi()

# Upload large folders with automatic chunking
api.upload_large_folder(
    repo_id="username/huge-dataset",
    folder_path="./data",
    repo_type="dataset",
)
```

## Common Use Cases

### Use Case 1: A/B Testing Results
```python
# Save A/B test results from a Gradio Space
def log_ab_test(user_id, variant, conversion):
    with scheduler.lock:
        with ab_test_file.open("a") as f:
            f.write(json.dumps({
                "user_id": user_id,
                "variant": variant,
                "conversion": conversion,
                "timestamp": datetime.now().isoformat()
            }))
            f.write("\n")
```

### Use Case 2: Model Predictions Storage
```python
# Store model predictions for analysis
def save_prediction(input_data, prediction, confidence):
    with scheduler.lock:
        with predictions_file.open("a") as f:
            f.write(json.dumps({
                "input": input_data,
                "prediction": prediction,
                "confidence": confidence,
                "model_version": "v1.0"
            }))
            f.write("\n")
```

### Use Case 3: Dataset Versioning
```python
# Create versioned snapshots of data
api = HfApi()

api.upload_folder(
    folder_path="./current_data",
    path_in_repo=f"snapshots/{datetime.now().strftime('%Y%m%d')}",
    repo_id="username/versioned-dataset",
    repo_type="dataset",
    commit_message=f"Snapshot for {datetime.now().date()}"
)
```

## Troubleshooting

### Issue: Upload fails with authentication error
**Solution:** Ensure you're logged in or have set the `HF_TOKEN` environment variable.

### Issue: Empty commits being created
**Solution:** The scheduler automatically skips empty commits. If you see them, check if files are being created correctly.

### Issue: Files not appearing in dataset
**Solution:** Wait for the next scheduled upload (check the `every` parameter) or the scheduler may be encountering errors.

### Issue: Out of memory errors
**Solution:** Use `upload_large_folder()` for very large datasets or upload files one at a time.

### Issue: Concurrent write conflicts
**Solution:** Always use `scheduler.lock` when writing to files that the scheduler is monitoring.

## References

- [HF Hub Dataset Storage Documentation](https://huggingface.co/docs/hub/spaces-storage#dataset-storage)
- [CommitScheduler API Reference](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api#huggingface_hub.CommitScheduler)
- [Upload Guide](https://huggingface.co/docs/huggingface_hub/main/en/guides/upload)
- [Space to Dataset Saver Example](https://huggingface.co/spaces/Wauplin/space_to_dataset_saver)

## Example: Complete Gradio App with Dataset Storage

See [examples.md](examples.md) for a complete working example of a Gradio Space with dataset storage.
