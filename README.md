<p align="center">
  <img src="https://img.shields.io/badge/fancy__job-v0.1.0-blueviolet?style=for-the-badge" alt="Version">
</p>

<h1 align="center">🎰 Fancy Job</h1>

<p align="center">
  <strong>An automated daily number incrementer that commits &amp; pushes to GitHub — powered by GitHub Actions, Python, and optional AI-generated commit messages.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white&style=flat-square" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?logo=githubactions&logoColor=white&style=flat-square" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Package%20Manager-uv-DE5FE9?logo=astral&logoColor=white&style=flat-square" alt="uv">
  <img src="https://img.shields.io/badge/LLM-GPT--2%20(Optional)-FF6F00?logo=huggingface&logoColor=white&style=flat-square" alt="GPT-2">
  <img src="https://img.shields.io/badge/License-Unlicensed-lightgrey?style=flat-square" alt="License">
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-features">Features</a> •
  <a href="#%EF%B8%8F-architecture">Architecture</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-project-structure">Project Structure</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-llm-commit-messages">LLM Commit Messages</a> •
  <a href="#-scheduling--automation">Scheduling</a> •
  <a href="#-security">Security</a> •
  <a href="#-troubleshooting">Troubleshooting</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-license">License</a>
</p>

---

## 📖 Overview

**Fancy Job** is a lightweight, fully automated Python project that increments a number stored in a plain text file (`number.txt`), commits the change to Git, and pushes it to GitHub — all without human intervention.

It was born as a fun experiment and has grown into a neat showcase of:

- **GitHub Actions CI/CD** — cloud-based cron automation
- **Python scripting** — file I/O, subprocess management, scheduling
- **AI/ML integration** — optional GPT-2-powered commit messages via Hugging Face Transformers
- **Windows Task Scheduler** — local randomized scheduling

The entire pipeline runs in GitHub's cloud infrastructure, meaning **your computer doesn't need to be on**. You can also run it locally for testing, development, or just for fun.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔢 **Auto-Increment** | Reads the current number from `number.txt`, increments it by 1, and writes it back |
| 📝 **Auto-Commit** | Stages and commits the updated file with a timestamped message |
| 🚀 **Auto-Push** | Pushes the commit to the remote GitHub repository |
| ☁️ **Cloud Automation** | Runs entirely via GitHub Actions — no local machine needed |
| ⏰ **Daily Cron Schedule** | Configurable GitHub Actions cron trigger for daily execution |
| 🎲 **Randomized Local Scheduling** | On Windows, reschedules itself via Task Scheduler at a random time each day |
| 🧠 **AI Commit Messages** | Optionally generates creative commit messages using GPT-2 (Hugging Face Transformers) |
| 🐍 **Pure Python** | Core logic uses only the Python standard library (`os`, `subprocess`, `random`, `datetime`) |
| 🔐 **Secure by Default** | Uses GitHub Actions' built-in `GITHUB_TOKEN` — no personal tokens required |
| 🛠️ **Manual Trigger** | Supports `workflow_dispatch` for on-demand execution from the GitHub Actions UI |
| 📦 **Modern Tooling** | Managed with `uv` and `pyproject.toml` for fast, reproducible dependency resolution |

---

## 🏗️ Architecture

The project follows a simple linear pipeline:

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Repository                    │
│                                                         │
│   .github/workflows/daily-update.yml                    │
│         │                                               │
│         │  (cron schedule / manual trigger)              │
│         ▼                                               │
│   ┌───────────────────┐                                 │
│   │  GitHub Actions   │  Cloud Runner (ubuntu-latest)   │
│   │  Workflow Runner  │                                 │
│   └────────┬──────────┘                                 │
│            │                                            │
│            │  1. Checkout repo                          │
│            │  2. Set up Python 3.12                     │
│            │  3. Configure Git identity                 │
│            │  4. Run update_number.py                   │
│            ▼                                            │
│   ┌───────────────────┐                                 │
│   │  update_number.py │                                 │
│   └────────┬──────────┘                                 │
│            │                                            │
│     ┌──────┴──────────────────┐                         │
│     ▼                         ▼                         │
│  ┌──────────────┐    ┌─────────────────┐                │
│  │  number.txt  │    │   Git Engine    │                │
│  │  Read → +1   │    │  add → commit   │                │
│  │  → Write     │    │  → push         │                │
│  └──────────────┘    └─────────────────┘                │
│                               │                         │
│                               ▼                         │
│                      Repository Updated                 │
│                      (new commit pushed)                │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

```
number.txt (read) → Python (increment) → number.txt (write)
                                        ↓
                                   git add number.txt
                                        ↓
                                   git commit -m "..."
                                        ↓
                                   git push origin
```

---

## ⚙️ How It Works

The core logic lives in [`update_number.py`](update_number.py). Here is a step-by-step breakdown of what happens on every execution:

### Step 1 — Read the Current Number

```python
def read_number():
    with open("number.txt", "r") as f:
        return int(f.read().strip())
```

Opens `number.txt`, reads the contents, strips whitespace, and parses it as an integer.

### Step 2 — Increment and Write

```python
def write_number(num):
    with open("number.txt", "w") as f:
        f.write(str(num))
```

Overwrites `number.txt` with the new value (`current + 1`).

### Step 3 — Git Commit

```python
def git_commit():
    subprocess.run(["git", "add", "number.txt"])
    if "FANCY_JOB_USE_LLM" in os.environ:
        commit_message = generate_random_commit_message()
    else:
        date = datetime.now().strftime("%Y-%m-%d")
        commit_message = f"Update number: {date}"
    subprocess.run(["git", "commit", "-m", commit_message])
```

- Stages `number.txt`
- Checks if the `FANCY_JOB_USE_LLM` environment variable is set:
  - **If set:** generates a creative commit message using GPT-2
  - **If not set:** uses the default format `Update number: YYYY-MM-DD`
- Commits the staged change

### Step 4 — Git Push

```python
def git_push():
    result = subprocess.run(["git", "push"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Changes pushed to GitHub successfully.")
    else:
        print("Error pushing to GitHub:")
        print(result.stderr)
```

Pushes the commit to the remote repository. Captures and reports any errors.

### Step 5 — Reschedule (Local Only)

```python
def update_cron_with_random_time():
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    # Creates a Windows Task Scheduler entry for tomorrow at a random time
```

When running locally on Windows, the script uses `schtasks` to schedule itself for the next day at a randomly chosen hour and minute. This ensures each execution happens at a different time.

### Orchestration

```python
def main():
    current_number = read_number()
    new_number = current_number + 1
    write_number(new_number)
    git_commit()
    git_push()
    update_cron_with_random_time()
```

The `main()` function ties everything together in order, wrapped in a try/except that exits with code 1 on failure.

---

## 📁 Project Structure

```
fancy_job/
├── .github/
│   └── workflows/
│       └── daily-update.yml      # GitHub Actions workflow (cron + manual trigger)
├── .python-version               # Pins Python to 3.12 (used by uv/pyenv)
├── CONTRIBUTING.md               # Contribution guidelines
├── README.md                     # This file
├── number.txt                    # The auto-incremented number (currently: 9)
├── pyproject.toml                # Project metadata & dependencies
├── update_number.py              # Core Python script (all logic lives here)
└── uv.lock                       # Lockfile for reproducible dependency resolution
```

### Key Files Explained

| File | Purpose |
|---|---|
| `update_number.py` | The heart of the project — reads, increments, writes, commits, pushes, and reschedules |
| `number.txt` | A single-line text file holding the current number |
| `pyproject.toml` | Declares the project name (`fancy-job`), version (`0.1.0`), Python requirement (`>=3.12`), and optional LLM dependencies |
| `daily-update.yml` | GitHub Actions workflow that checks out the repo, configures Git, and runs the script on a schedule |
| `uv.lock` | Auto-generated lockfile created by `uv` for deterministic installs |
| `.python-version` | Specifies `3.12` for tools like `uv` and `pyenv` |

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Minimum Version | Notes |
|---|---|---|
| **Python** | 3.12+ | Required |
| **Git** | Any modern version | Must be installed and configured |
| **uv** | Latest | Recommended package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/)) |
| **pip** | Latest | Alternative to `uv` |

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/Akki-74/fancy_job.git
cd fancy_job
```

#### 2. Set Up Python Environment

**Using `uv` (recommended):**

```bash
uv sync
```

This creates a virtual environment and installs all dependencies from the lockfile.

**Using `pip`:**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -e .
```

#### 3. (Optional) Install LLM Dependencies

If you want AI-generated commit messages:

**Using `uv`:**

```bash
uv sync --extra llm
```

**Using `pip`:**

```bash
pip install -e ".[llm]"
```

This installs:
- `torch >= 2.5.1` — PyTorch deep learning framework
- `transformers >= 4.47.1` — Hugging Face Transformers library

> **Note:** The LLM dependencies are large (~2 GB+). The base project runs perfectly without them.

---

## 💻 Usage

### Local Execution

Run the script directly:

```bash
python update_number.py
```

**What happens:**
1. Reads the number from `number.txt`
2. Increments it by 1
3. Commits the change to Git
4. Pushes to GitHub
5. Schedules the next run via Windows Task Scheduler at a random time tomorrow

### With LLM Commit Messages

Set the `FANCY_JOB_USE_LLM` environment variable before running:

**Windows (PowerShell):**
```powershell
$env:FANCY_JOB_USE_LLM = "1"
python update_number.py
```

**Windows (CMD):**
```cmd
set FANCY_JOB_USE_LLM=1
python update_number.py
```

**macOS / Linux:**
```bash
FANCY_JOB_USE_LLM=1 python update_number.py
```

### GitHub Actions (Automated)

The workflow at `.github/workflows/daily-update.yml` runs automatically. You can also trigger it manually:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select the **Daily Number Update** workflow
4. Click **Run workflow**
5. Select the branch and click **Run workflow**

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `FANCY_JOB_USE_LLM` | No | *(unset)* | Set to any value to enable GPT-2 commit message generation |
| `GITHUB_TOKEN` | Auto (CI) | *(provided by Actions)* | Used by GitHub Actions for authenticated pushes |

### `pyproject.toml` Settings

```toml
[project]
name = "fancy-job"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []                    # No base dependencies

[project.optional-dependencies]
llm = [
    "torch>=2.5.1",
    "transformers>=4.47.1"
]
```

- **Base mode:** Zero external dependencies — only the Python standard library
- **LLM mode:** Adds PyTorch + Transformers for AI-generated commit messages

### Git Configuration

The script automatically changes its working directory to the script's location:

```python
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
```

This ensures Git commands always run in the correct repository root, regardless of where the script is invoked from.

For GitHub Actions, Git identity is configured in the workflow:
```yaml
git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"
```

---

## 🧠 LLM Commit Messages

When the `FANCY_JOB_USE_LLM` environment variable is set, the script generates commit messages using **OpenAI's GPT-2** model via Hugging Face's `transformers` library.

### How It Works

```python
def generate_random_commit_message():
    from transformers import pipeline

    generator = pipeline("text-generation", model="openai-community/gpt2")
    prompt = """
        Generate a Git commit message following the Conventional Commits standard...
    """
    generated = generator(
        prompt,
        max_new_tokens=50,
        num_return_sequences=1,
        temperature=0.9,
        top_k=50,
        top_p=0.9,
        truncation=True,
    )
```

### Generation Parameters

| Parameter | Value | Purpose |
|---|---|---|
| `model` | `openai-community/gpt2` | Lightweight, no API key required |
| `max_new_tokens` | `50` | Keeps messages concise |
| `temperature` | `0.9` | Higher creativity in outputs |
| `top_k` | `50` | Limits sampling to top 50 tokens |
| `top_p` | `0.9` | Nucleus sampling for diversity |
| `truncation` | `True` | Prevents exceeding model context |

### Example Generated Messages

```
feat(auth): add user authentication module
fix(api): resolve null pointer exception in user endpoint
docs(readme): update installation instructions
chore(deps): upgrade lodash to version 4.17.21
refactor(utils): simplify date formatting logic
```

> **Note:** GPT-2 is a general-purpose language model. Generated messages follow the Conventional Commits pattern from the prompt but may occasionally produce unexpected results.

---

## 📅 Scheduling & Automation

### GitHub Actions (Cloud)

The workflow is configured in [`.github/workflows/daily-update.yml`](.github/workflows/daily-update.yml).

**Trigger types:**
- `schedule` — Cron-based daily execution
- `workflow_dispatch` — Manual trigger from the GitHub Actions UI

**Workflow permissions:**
- The workflow uses GitHub's built-in `GITHUB_TOKEN` for authentication
- Requires **Read and write permissions** under repository Settings → Actions → General → Workflow permissions

### Windows Task Scheduler (Local)

When run locally, the script creates a one-time Windows Task Scheduler entry:

```
Task Name:   DailyNumberIncrementer
Schedule:    Once, tomorrow at a random HH:MM
Command:     "<python_exe>" "<script_path>"
```

Each execution **deletes the previous task** and creates a new one with a freshly randomized time, so the script runs at a different time every day.

**Why random times?**  
Randomizing the execution time avoids predictable patterns, making the commit history look more organic and natural.

### How Scheduling Works Internally

```python
def update_cron_with_random_time():
    random_hour = random.randint(0, 23)      # 0-23
    random_minute = random.randint(0, 59)     # 0-59
    tomorrow = date.today() + timedelta(days=1)

    # Delete existing task
    subprocess.run(["schtasks", "/delete", "/tn", "DailyNumberIncrementer", "/f"])

    # Create new task for tomorrow at the random time
    subprocess.run([
        "schtasks", "/create",
        "/tn", "DailyNumberIncrementer",
        "/tr", f'"{python_exe}" "{script_path}"',
        "/sc", "once",
        "/st", f"{random_hour:02d}:{random_minute:02d}",
        "/sd", tomorrow.strftime("%m/%d/%Y"),
        "/f",
    ])
```

---

## 🔐 Security

| Concern | Mitigation |
|---|---|
| **Authentication** | Uses GitHub Actions' built-in `GITHUB_TOKEN` — no personal access tokens or secrets stored |
| **Permissions** | The `GITHUB_TOKEN` is scoped to the repository and the workflow run |
| **No Secrets in Code** | No API keys, passwords, or tokens are hardcoded |
| **LLM Model** | GPT-2 runs locally (no external API calls, no data sent to third parties) |
| **Dependencies** | Locked via `uv.lock` for reproducible, tamper-resistant installs |

---

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><strong>❌ "Error pushing to GitHub"</strong></summary>

**Possible causes:**
- Git remote not configured — run `git remote -v` to verify
- Authentication failure — ensure `GITHUB_TOKEN` has write permissions (in Actions) or your local Git credentials are configured
- Branch protection rules blocking pushes

**Fix:**
```bash
# Verify remote
git remote -v

# For local usage, ensure credentials are cached
git config credential.helper store
```
</details>

<details>
<summary><strong>❌ "Error updating Windows Task Scheduler"</strong></summary>

**Possible causes:**
- Script not running with administrator privileges
- `schtasks` not available (non-Windows system)

**Fix:**
- Run the terminal/script as **Administrator**
- This feature is **Windows-only** — on macOS/Linux, use `cron` instead
</details>

<details>
<summary><strong>❌ "ModuleNotFoundError: No module named 'transformers'"</strong></summary>

**Cause:** LLM dependencies not installed.

**Fix:**
```bash
uv sync --extra llm
# or
pip install -e ".[llm]"
```
</details>

<details>
<summary><strong>❌ GitHub Actions workflow not running</strong></summary>

**Possible causes:**
- Workflow file is empty or has syntax errors
- GitHub disables scheduled workflows on repos with no recent activity (after 60 days)

**Fix:**
- Verify `.github/workflows/daily-update.yml` has valid YAML content
- Push a commit or manually trigger the workflow to re-enable it
- Check the **Actions** tab for error messages
</details>

<details>
<summary><strong>❌ number.txt contains unexpected content</strong></summary>

**Cause:** The file must contain a single integer with no extra whitespace or characters.

**Fix:**
```bash
echo 0 > number.txt
```
</details>

---

## 🤝 Contributing

This project was originally intended as a joke/experiment. While the interest is appreciated, **pull requests and issues are generally not accepted**. Feel free to **fork** the repository and modify it for your own use.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for more details.

---

## 🗺️ Roadmap

Potential future enhancements (community forks welcome):

- [ ] 🐧 **Cross-platform scheduling** — Add `cron` support for macOS/Linux alongside Windows Task Scheduler
- [ ] 🔄 **Configurable increment** — Allow custom step sizes (e.g., +2, +5, +10)
- [ ] 📊 **Statistics dashboard** — Track and visualize the number growth over time
- [ ] 🤖 **Better LLM models** — Swap GPT-2 for more capable local models (e.g., Phi, Gemma)
- [ ] 🧪 **Unit tests** — Add pytest-based test suite for all functions
- [ ] 🔔 **Notifications** — Send alerts on failure (email, Discord, Slack)
- [ ] 📋 **Changelog generation** — Auto-generate a `CHANGELOG.md` from commit history
- [ ] 🌍 **Multi-branch support** — Run on multiple branches simultaneously
- [ ] 🐳 **Docker support** — Containerized execution for CI/CD portability

---

## 📜 License

This project does not currently include a license file. All rights are reserved by the author by default.

If you wish to use this project, please contact the author or fork the repository.

---

<p align="center">
  Made with ❤️ and a touch of absurdity
</p>

<p align="center">
  <a href="https://github.com/Akki-74/fancy_job">⭐ Star this repo</a> if it made you smile!
</p>
