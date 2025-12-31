# API Reference for HF Dataset Storage

This reference provides detailed documentation for all the APIs and configuration options related to Hugging Face dataset storage.

## Table of Contents

1. [CommitScheduler](#commitscheduler)
2. [HfApi Upload Methods](#hfapi-upload-methods)
3. [Commit Operations](#commit-operations)
4. [Authentication](#authentication)
5. [Configuration](#configuration)
6. [Error Handling](#error-handling)

---

## CommitScheduler

The `CommitScheduler` class automatically uploads files to a dataset repository at regular intervals.

### Constructor

```python
from huggingface_hub import CommitScheduler

scheduler = CommitScheduler(
    repo_id: str,
    folder_path: str | Path,
    *,
    repo_type: str = "dataset",
    revision: str = "main",
    path_in_repo: str = ".",
    every: int | float = 5,
    token: str | None = None,
    allow_patterns: str | List[str] | None = None,
    ignore_patterns: str | List[str] | None = None,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `repo_id` | `str` | Required | Repository ID (e.g., "username/dataset-name") |
| `folder_path` | `str | Path` | Required | Local folder to monitor and upload |
| `repo_type` | `str` | `"dataset"` | Type of repo: "dataset", "model", or "space" |
| `revision` | `str` | `"main"` | Git revision/branch to commit to |
| `path_in_repo` | `str` | `"."` | Path in the repo where files will be uploaded |
| `every` | `int | float` | `5` | Minutes between uploads (minimum 5 recommended) |
| `token` | `str | None` | `None` | HuggingFace token (uses cached token if None) |
| `allow_patterns` | `str | List[str] | None` | `None` | Glob patterns for files to include |
| `ignore_patterns` | `str | List[str] | None` | `None` | Glob patterns for files to exclude |

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `lock` | `threading.Lock` | Thread lock for safe concurrent writes |
| `api` | `HfApi` | HuggingFace API client instance |
| `repo_id` | `str` | The repository ID |
| `folder_path` | `Path` | The monitored folder path |

### Methods

#### `push_to_hub()`

Manually trigger an upload. Called automatically by the scheduler.

```python
scheduler.push_to_hub()
```

**Note:** You can override this method in a subclass for custom behavior.

### Example: Basic Usage

```python
from pathlib import Path
from huggingface_hub import CommitScheduler

# Create scheduler
scheduler = CommitScheduler(
    repo_id="username/my-dataset",
    folder_path=Path("./data"),
    every=10,
)

# Files in ./data will be uploaded every 10 minutes
# Use scheduler.lock when writing to ensure thread safety
```

### Example: Custom Upload Logic

```python
from huggingface_hub import CommitScheduler
import zipfile
from pathlib import Path

class CustomScheduler(CommitScheduler):
    def push_to_hub(self):
        """Custom logic to zip files before upload."""
        files = list(self.folder_path.glob("*.txt"))
        if not files:
            return None

        # Create archive
        archive_path = self.folder_path / "archive.zip"
        with zipfile.ZipFile(archive_path, "w") as zf:
            for file in files:
                zf.write(file, file.name)

        # Upload using parent's API
        self.api.upload_file(
            path_or_fileobj=str(archive_path),
            path_in_repo="archives/archive.zip",
            repo_id=self.repo_id,
            repo_type=self.repo_type,
        )

        # Cleanup
        archive_path.unlink()
        for file in files:
            file.unlink()
```

---

## HfApi Upload Methods

The `HfApi` class provides methods for uploading files and folders.

### upload_file()

Upload a single file to a repository.

```python
from huggingface_hub import HfApi

api = HfApi()

api.upload_file(
    path_or_fileobj: str | Path | bytes | BinaryIO,
    path_in_repo: str,
    repo_id: str,
    *,
    repo_type: str = "model",
    revision: str = "main",
    commit_message: str | None = None,
    commit_description: str | None = None,
    token: str | None = None,
    run_as_future: bool = False,
)
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `path_or_fileobj` | `str | Path | bytes | BinaryIO` | File path or file-like object to upload |
| `path_in_repo` | `str` | Destination path in the repository |
| `repo_id` | `str` | Repository ID |
| `repo_type` | `str` | "model", "dataset", or "space" |
| `revision` | `str` | Branch/tag to commit to |
| `commit_message` | `str | None` | Custom commit message |
| `commit_description` | `str | None` | Extended commit description |
| `token` | `str | None` | Authentication token |
| `run_as_future` | `bool` | Run upload in background (returns Future) |

#### Returns

- `str`: Commit hash (URL to the commit)
- `concurrent.futures.Future`: If `run_as_future=True`

#### Example

```python
# Upload file from path
api.upload_file(
    path_or_fileobj="/path/to/file.json",
    path_in_repo="data/file.json",
    repo_id="username/my-dataset",
    repo_type="dataset",
    commit_message="Add new data file"
)

# Upload bytes
data = b'{"key": "value"}'
api.upload_file(
    path_or_fileobj=data,
    path_in_repo="config.json",
    repo_id="username/my-dataset",
    repo_type="dataset",
)

# Background upload
future = api.upload_file(
    path_or_fileobj="large_file.bin",
    path_in_repo="large_file.bin",
    repo_id="username/my-dataset",
    repo_type="dataset",
    run_as_future=True,
)
# Do other work...
future.result()  # Wait for completion
```

---

### upload_folder()

Upload an entire folder to a repository.

```python
api.upload_folder(
    folder_path: str | Path,
    repo_id: str,
    *,
    repo_type: str = "model",
    revision: str = "main",
    path_in_repo: str = ".",
    commit_message: str | None = None,
    commit_description: str | None = None,
    token: str | None = None,
    allow_patterns: str | List[str] | None = None,
    ignore_patterns: str | List[str] | None = None,
    delete_patterns: str | List[str] | None = None,
    run_as_future: bool = False,
)
```

#### Additional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `folder_path` | `str | Path` | Local folder to upload |
| `allow_patterns` | `str | List[str] | None` | Glob patterns to include |
| `ignore_patterns` | `str | List[str] | None` | Glob patterns to exclude |
| `delete_patterns` | `str | List[str] | None` | Patterns to delete from repo before upload |

#### Example

```python
# Upload entire folder
api.upload_folder(
    folder_path="./my_dataset",
    repo_id="username/my-dataset",
    repo_type="dataset",
)

# Upload only CSV files
api.upload_folder(
    folder_path="./data",
    repo_id="username/my-dataset",
    repo_type="dataset",
    allow_patterns="*.csv",
)

# Upload and delete old files
api.upload_folder(
    folder_path="./new_data",
    path_in_repo="data",
    repo_id="username/my-dataset",
    repo_type="dataset",
    delete_patterns="*.old",  # Delete .old files first
)
```

---

### upload_large_folder()

Upload very large folders with resume capability.

```python
api.upload_large_folder(
    repo_id: str,
    folder_path: str | Path,
    *,
    repo_type: str = "model",
    revision: str = "main",
    private: bool = False,
    token: str | None = None,
    allow_patterns: str | List[str] | None = None,
    ignore_patterns: str | List[str] | None = None,
    num_workers: int = 1,
)
```

#### Key Features

- **Resumable**: Caches progress locally, can resume after interruption
- **Multi-threaded**: Parallel uploads with `num_workers`
- **Resilient**: Automatic retries on errors

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `num_workers` | `int` | Number of parallel upload threads |

#### Limitations

- Cannot set custom `path_in_repo` (upload to root)
- Cannot set custom commit message
- Cannot delete files while uploading
- Cannot create PR directly

#### Example

```python
# Upload huge dataset
api.upload_large_folder(
    repo_id="username/huge-dataset",
    folder_path="/data/massive_dataset",
    repo_type="dataset",
    num_workers=4,  # Use 4 parallel threads
)

# If interrupted, re-run the same command to resume
```

---

## Commit Operations

For fine-grained control over commits, use `create_commit()` with operation objects.

### create_commit()

Create a commit with multiple operations (add/delete/copy files).

```python
api.create_commit(
    repo_id: str,
    operations: List[CommitOperation],
    *,
    commit_message: str,
    commit_description: str | None = None,
    repo_type: str = "model",
    revision: str = "main",
    token: str | None = None,
    create_pr: bool = False,
)
```

### Operation Types

#### CommitOperationAdd

Add or update a file.

```python
from huggingface_hub import CommitOperationAdd

op = CommitOperationAdd(
    path_in_repo="path/to/file.txt",
    path_or_fileobj="/local/path/file.txt"  # or bytes or file object
)
```

#### CommitOperationDelete

Delete a file or folder.

```python
from huggingface_hub import CommitOperationDelete

op = CommitOperationDelete(
    path_in_repo="path/to/delete.txt"  # or "folder/" for directories
)
```

#### CommitOperationCopy

Copy a file within the repository.

```python
from huggingface_hub import CommitOperationCopy

op = CommitOperationCopy(
    src_path_in_repo="original.txt",
    path_in_repo="copy.txt",
    src_revision="main"  # optional: copy from different branch
)
```

### Example: Multi-operation Commit

```python
from huggingface_hub import HfApi, CommitOperationAdd, CommitOperationDelete

api = HfApi()

operations = [
    CommitOperationAdd(
        path_in_repo="data/new_file.json",
        path_or_fileobj="/local/new_file.json"
    ),
    CommitOperationAdd(
        path_in_repo="config.yaml",
        path_or_fileobj=b"key: value"
    ),
    CommitOperationDelete(
        path_in_repo="old_data/"  # Delete entire folder
    ),
]

api.create_commit(
    repo_id="username/my-dataset",
    operations=operations,
    commit_message="Update dataset files",
    commit_description="Added new data and removed old files",
    repo_type="dataset",
)
```

---

## Authentication

### Method 1: CLI Login (Recommended)

```bash
huggingface-cli login
```

This caches your token locally. All subsequent API calls use this token automatically.

### Method 2: Environment Variable

```bash
export HF_TOKEN="hf_..."
```

```python
import os
from huggingface_hub import HfApi

api = HfApi(token=os.environ["HF_TOKEN"])
```

### Method 3: Programmatic Token

```python
from huggingface_hub import HfApi

api = HfApi(token="hf_your_token_here")
```

### For Hugging Face Spaces

1. Go to Space Settings → Repository secrets
2. Add secret: `HF_TOKEN` = your token value
3. Access in code:

```python
import os
token = os.environ.get("HF_TOKEN")
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HF_TOKEN` | Authentication token | None |
| `HF_HOME` | Cache directory | `~/.cache/huggingface` |
| `HF_HUB_CACHE` | Hub cache directory | `$HF_HOME/hub` |
| `HF_ENDPOINT` | Hub endpoint URL | `https://huggingface.co` |
| `HF_XET_CACHE` | Xet cache directory | `$HF_HOME/xet` |
| `HF_XET_HIGH_PERFORMANCE` | Enable high-performance mode | `0` |

### Example: Custom Cache Location

```python
import os

# Set cache to local SSD for better performance
os.environ["HF_HOME"] = "/mnt/local-ssd/.cache/huggingface"

from huggingface_hub import HfApi
api = HfApi()
```

---

## Error Handling

### Common Errors and Solutions

#### 1. Authentication Error

```python
from huggingface_hub import HfApi
from huggingface_hub.utils import HfHubHTTPError

api = HfApi()

try:
    api.upload_file(
        path_or_fileobj="file.txt",
        path_in_repo="file.txt",
        repo_id="username/dataset",
        repo_type="dataset",
    )
except HfHubHTTPError as e:
    if e.response.status_code == 401:
        print("❌ Authentication failed. Run: huggingface-cli login")
    else:
        raise
```

#### 2. Repository Not Found

```python
from huggingface_hub import HfApi
from huggingface_hub.utils import RepositoryNotFoundError

api = HfApi()

try:
    api.upload_file(...)
except RepositoryNotFoundError:
    print("❌ Repository not found. Creating...")
    api.create_repo(repo_id="username/dataset", repo_type="dataset")
    api.upload_file(...)  # Retry
```

#### 3. File Too Large

```python
from huggingface_hub import HfApi

api = HfApi()

file_size = os.path.getsize("huge_file.bin")

if file_size > 5 * 1024**3:  # > 5GB
    print("⚠️ Large file detected, using upload_large_folder")
    # Move file to folder and use upload_large_folder
else:
    api.upload_file(
        path_or_fileobj="huge_file.bin",
        path_in_repo="huge_file.bin",
        repo_id="username/dataset",
        repo_type="dataset",
    )
```

#### 4. Network Interruption

```python
from huggingface_hub import HfApi
import time

api = HfApi()

max_retries = 3
for attempt in range(max_retries):
    try:
        api.upload_folder(
            folder_path="./data",
            repo_id="username/dataset",
            repo_type="dataset",
        )
        break
    except Exception as e:
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"⚠️ Upload failed, retrying in {wait_time}s...")
            time.sleep(wait_time)
        else:
            print("❌ Upload failed after all retries")
            raise
```

---

## Advanced Patterns

### Pattern 1: Atomic Updates

Ensure all files are updated together or not at all.

```python
from huggingface_hub import HfApi, CommitOperationAdd

api = HfApi()

# Prepare all operations
operations = [
    CommitOperationAdd("file1.json", path_or_fileobj=data1),
    CommitOperationAdd("file2.json", path_or_fileobj=data2),
    CommitOperationAdd("file3.json", path_or_fileobj=data3),
]

# Single atomic commit
api.create_commit(
    repo_id="username/dataset",
    operations=operations,
    commit_message="Atomic update of all files",
    repo_type="dataset",
)
```

### Pattern 2: Concurrent Uploads

Upload multiple files in parallel.

```python
from huggingface_hub import HfApi
from concurrent.futures import ThreadPoolExecutor

api = HfApi()
files = ["file1.txt", "file2.txt", "file3.txt"]

def upload_file(filename):
    api.upload_file(
        path_or_fileobj=filename,
        path_in_repo=filename,
        repo_id="username/dataset",
        repo_type="dataset",
    )

with ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(upload_file, files)
```

### Pattern 3: Progressive Dataset Building

Build dataset incrementally with versioning.

```python
from huggingface_hub import HfApi

api = HfApi()

for version in range(1, 11):
    # Generate data for this version
    data = generate_data(version)

    # Upload to versioned path
    api.upload_file(
        path_or_fileobj=data,
        path_in_repo=f"versions/v{version}/data.json",
        repo_id="username/dataset",
        repo_type="dataset",
        commit_message=f"Add version {version}",
    )
```

---

## Performance Tips

### 1. Use High-Performance Mode

For maximum upload speed (uses all CPU cores and bandwidth):

```bash
export HF_XET_HIGH_PERFORMANCE=1
```

### 2. Local Cache for Cluster Uploads

When uploading from distributed filesystems:

```bash
# Point cache to local SSD, not network filesystem
export HF_XET_CACHE=/local-ssd/.cache/xet
```

### 3. Batch Small Files

Instead of uploading thousands of small files individually:

```python
import zipfile
from huggingface_hub import HfApi

# Zip small files
with zipfile.ZipFile("archive.zip", "w") as zf:
    for file in small_files:
        zf.write(file)

# Upload single archive
api.upload_file(
    path_or_fileobj="archive.zip",
    path_in_repo="data/archive.zip",
    repo_id="username/dataset",
    repo_type="dataset",
)
```

### 4. Use Background Uploads

Don't block your main thread:

```python
from huggingface_hub import HfApi

api = HfApi()

# Start upload in background
future = api.upload_folder(
    folder_path="./data",
    repo_id="username/dataset",
    repo_type="dataset",
    run_as_future=True,
)

# Do other work
process_more_data()

# Wait for completion when ready
future.result()
```

---

## Comparison Table

| Feature | CommitScheduler | upload_folder() | upload_large_folder() |
|---------|----------------|-----------------|----------------------|
| Automatic uploads | ✅ Yes | ❌ No | ❌ No |
| Resumable | ❌ No | ❌ No | ✅ Yes |
| Custom commit message | ❌ No | ✅ Yes | ❌ No |
| Background operation | ✅ Yes | ✅ Yes (with flag) | ❌ No |
| Path in repo | ✅ Yes | ✅ Yes | ❌ No (root only) |
| Multi-threaded | ❌ No | ❌ No | ✅ Yes |
| Best for | Continuous logging | One-time uploads | Huge datasets |

---

## Quick Reference

### Upload Single File
```python
api.upload_file(path_or_fileobj="file.txt", path_in_repo="file.txt",
                repo_id="user/dataset", repo_type="dataset")
```

### Upload Folder
```python
api.upload_folder(folder_path="./data", repo_id="user/dataset",
                  repo_type="dataset")
```

### Scheduled Uploads
```python
scheduler = CommitScheduler(repo_id="user/dataset", folder_path="./data",
                            every=10, repo_type="dataset")
```

### Background Upload
```python
future = api.upload_folder(..., run_as_future=True)
future.result()  # Wait for completion
```

### Large Folder
```python
api.upload_large_folder(repo_id="user/dataset", folder_path="./big_data",
                        repo_type="dataset", num_workers=4)
```
