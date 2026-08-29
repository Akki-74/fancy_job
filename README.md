<p align="center">
  <img src="https://img.shields.io/badge/fancy__job-v0.1.0-blueviolet?style=for-the-badge" alt="Version">
</p>

<h1 align="center">🎰 Fancy Job</h1>

<p align="center">
  <strong>An automated daily number incrementer with intelligent cloud scheduling, Git automation, and optional AI-generated commit messages.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white&style=flat-square" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?logo=githubactions&logoColor=white&style=flat-square" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Package%20Manager-uv-DE5FE9?logo=astral&logoColor=white&style=flat-square" alt="uv">
  <img src="https://img.shields.io/badge/LLM-GPT--2%20(Optional)-FF6F00?logo=huggingface&logoColor=white&style=flat-square" alt="GPT-2">
  <img src="https://img.shields.io/badge/Scheduler-Stateful%20UTC%20Cron-4CAF50?style=flat-square" alt="Scheduler">
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
  <a href="#-intelligent-scheduler">Intelligent Scheduler</a> •
  <a href="#-llm-commit-messages">LLM Commit Messages</a> •
  <a href="#-github-actions-cicd">GitHub Actions</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-security">Security</a> •
  <a href="#-troubleshooting">Troubleshooting</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a>
</p>

---

## 📖 Overview

**Fancy Job** is a fully automated, cloud-native Python project that maintains a sequential counter in `number.txt`, creates Git commits, and pushes updates to GitHub without requiring any local machine to stay online.

The project demonstrates real-world software engineering practices wrapped in a playful concept:
- **Stateful Cloud Automation:** Uses GitHub Actions combined with a persistent JSON-based state machine (`schedule.json`) to trigger runs at randomized times each day.
- **Robust Git Automation:** Subprocess-based staging, committing, and pushing with automated identity management.
- **Optional AI Commit Synthesis:** Local LLM text generation using GPT-2 via Hugging Face Transformers to craft Conventional Commits.
- **Zero Base Dependencies:** Core execution relies purely on Python 3.12+ standard library modules (`json`, `random`, `subprocess`, `sys`, `datetime`, `pathlib`, `os`).

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔢 **Auto-Incrementing Counter** | Reads `number.txt`, increments the integer sequentially, and persists the new state |
| 📅 **Smart Cloud Scheduling** | Periodically polled via GitHub Actions cron, executing only when randomized UTC targets are met |
| 🎲 **Organic Timing Window** | Generates a new random execution timestamp between 08:00 and 23:00 UTC for each subsequent day |
| 📝 **Automated Git Workflow** | Automatically stages `number.txt`, creates a clean commit, and pushes to `origin` |
| 🧠 **Optional AI Commit Messages** | Generates Conventional Commit messages with GPT-2 when `FANCY_JOB_USE_LLM` is enabled |
| ☁️ **100% Serverless Execution** | Runs entirely within GitHub Actions runners with no dedicated hosting required |
| 🔒 **Concurrency & Race-Safe** | Configured with workflow concurrency grouping to prevent race conditions |
| 🐍 **Standard Library Core** | Base execution requires zero third-party packages |
| 📦 **Modern Tooling** | Managed with `uv` and `pyproject.toml` for blazing fast, reproducible dependency management |

---

## 🏗️ Architecture

```
                               GitHub Repository
  ┌────────────────────────────────────────────────────────────────────────┐
  │                                                                        │
  │  .github/workflows/daily-update.yml (Cron: every 30m / Manual dispatch)│
  │                                                                        │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
                        GitHub Actions Cloud Runner
  ┌────────────────────────────────────────────────────────────────────────┐
  │  1. Checkout repository with full history                              │
  │  2. Setup Python 3.12                                                  │
  │  3. Configure Git (github-actions[bot])                                │
  │  4. Run: python scheduler/scheduler.py                                 │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
                           scheduler/scheduler.py
  ┌────────────────────────────────────────────────────────────────────────┐
  │  • Reads schedule.json ("next_run" timestamp)                          │
  │  • Evaluates: Is current UTC time >= next_run?                         │
  └──────────────────────┬──────────────────────────┬──────────────────────┘
                         │                          │
                   NO (Not due)                 YES (Due)
                         │                          │
                         ▼                          ▼
                 Exit successfully           Execute update_number.py
                (No commit pushed)                  │
                                                    ├──────────────────────────┐
                                                    ▼                          ▼
                                            Read & Increment           Git Commit & Push
                                              number.txt                (Default / LLM)
                                                    │                          │
                                                    └────────────┬─────────────┘
                                                                 │
                                                                 ▼
                                                  Compute new random UTC target
                                                    (Tomorrow 08:00 - 23:00)
                                                                 │
                                                                 ▼
                                                    Update scheduler/schedule.json
                                                    & finish run
```

---

## ⚙️ How It Works

The architecture is cleanly separated into two distinct components: the **Execution Engine** (`update_number.py`) and the **Stateful Scheduler** (`scheduler/scheduler.py`).

### 1. The Execution Engine (`update_number.py`)

Responsible for manipulating the number file and publishing Git commits.

```python
# 1. Read the counter
def read_number():
    with open("number.txt", "r") as f:
        return int(f.read().strip())

# 2. Write the incremented value
def write_number(num):
    with open("number.txt", "w") as f:
        f.write(str(num))

# 3. Stage & Commit
def git_commit():
    subprocess.run(["git", "add", "number.txt"], check=True)
    if "FANCY_JOB_USE_LLM" in os.environ:
        commit_message = generate_random_commit_message()
    else:
        date = datetime.now().strftime("%Y-%m-%d")
        commit_message = f"Update number: {date}"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)

# 4. Push upstream
def git_push():
    subprocess.run(["git", "push"], check=True)
```

### 2. The Stateful Scheduler (`scheduler/scheduler.py`)

Coordinates when jobs run, ensuring the commit schedule looks organic and non-deterministic.

```python
START_HOUR = 8   # 08:00 UTC
END_HOUR = 23    # 22:59 UTC

def generate_random_time():
    tomorrow = datetime.now(timezone.utc).date() + timedelta(days=1)
    random_hour = random.randint(START_HOUR, END_HOUR - 1)
    random_minute = random.randint(0, 59)
    return datetime(
        tomorrow.year, tomorrow.month, tomorrow.day,
        random_hour, random_minute,
        tzinfo=timezone.utc,
    )
```

1. **GitHub Actions invokes `scheduler.py` every 30 minutes.**
2. `scheduler.py` loads `schedule.json`:
   - If `now < next_run`, it logs `Not due yet` and terminates immediately.
   - If `now >= next_run`, it triggers `update_number.py`.
3. Once the update succeeds, a new `next_run` timestamp is computed for tomorrow (between 08:00 and 22:59 UTC) and written back to `schedule.json`.

---

## 📁 Project Structure

```
fancy_job/
├── .github/
│   └── workflows/
│       └── daily-update.yml       # GitHub Actions workflow (runs every 30 mins)
├── .python-version                # Pins Python version to 3.12
├── CONTRIBUTING.md                # Project contribution guidelines
├── README.md                      # Detailed project documentation
├── number.txt                     # Plain text file containing the current number counter
├── pyproject.toml                 # Project metadata and optional LLM dependency definitions
├── scheduler/
│   ├── schedule.json              # State storage tracking the next scheduled UTC execution
│   └── scheduler.py               # Deterministic time-check scheduler
├── update_number.py               # Core script handling file I/O, Git commit, and push
└── uv.lock                        # Lockfile ensuring reproducible dependency resolution
```

---

## 🚀 Getting Started

### Prerequisites

- **Python:** `3.12+`
- **Git:** Installed and configured with your credentials
- **Package Manager:** `uv` (recommended) or `pip`

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/Akki-74/fancy_job.git
cd fancy_job
```

#### 2. Set Up Environment

**Using `uv` (Recommended):**
```bash
# Sync dependencies
uv sync
```

**Using Standard `pip`:**
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -e .
```

#### 3. (Optional) Install AI / LLM Dependencies

If you plan to use local GPT-2 commit message generation:

**Using `uv`:**
```bash
uv sync --extra llm
```

**Using `pip`:**
```bash
pip install -e ".[llm]"
```

---

## 💻 Usage

### Direct Manual Run
Increment the number, create a commit, and push immediately:

```bash
python update_number.py
```

### Running with AI Commit Messages
Enable the LLM generator by setting the `FANCY_JOB_USE_LLM` environment variable:

**PowerShell (Windows):**
```powershell
$env:FANCY_JOB_USE_LLM="1"
python update_number.py
```

**CMD (Windows):**
```cmd
set FANCY_JOB_USE_LLM=1
python update_number.py
```

**Bash / Zsh (Linux & macOS):**
```bash
FANCY_JOB_USE_LLM=1 python update_number.py
```

### Running the Scheduler
Test the scheduler evaluation locally:

```bash
python scheduler/scheduler.py
```

- If `schedule.json` has reached its timestamp, `update_number.py` will execute and schedule tomorrow's time.
- If not due, it displays current vs scheduled time.

---

## ⏱️ Intelligent Scheduler

The project avoids static cron patterns by pairing a frequent cloud poll with a local JSON state machine.

### Schedule State File (`scheduler/schedule.json`)

```json
{
  "next_run": "2026-08-29T14:32:00+00:00"
}
```

### Scheduler Logic Highlights

1. **Timezone Aware:** Always evaluates using UTC (`timezone.utc`) to prevent discrepancies across runners and locations.
2. **Success-Gated Rescheduling:** If `update_number.py` encounters a Git conflict or push error, `schedule.json` will not update, ensuring the run retries on the next workflow execution.
3. **Controllable Windows:** Default window is configured from `START_HOUR = 8` to `END_HOUR = 23` (8:00 AM – 11:00 PM UTC).

---

## 🧠 LLM Commit Messages

When `FANCY_JOB_USE_LLM` is set, `update_number.py` uses Hugging Face's `transformers` library to generate commit messages using the `openai-community/gpt2` model.

### Prompt & Sampling Strategy

The script prompts the model with standard Conventional Commit examples and samples with slight randomness:

```python
generated = generator(
    prompt,
    max_new_tokens=50,
    num_return_sequences=1,
    temperature=0.9,  # Sampling temperature for creative diversity
    top_k=50,         # Top-K filtering
    top_p=0.9,        # Nucleus (top-p) sampling
    truncation=True,
)
```

### Generated Message Format Examples

- `feat(auth): add user authentication module`
- `fix(api): resolve null pointer exception in user endpoint`
- `docs(readme): update installation instructions`
- `chore(deps): upgrade lodash to version 4.17.21`
- `refactor(utils): simplify date formatting logic`

---

## ☁️ GitHub Actions CI/CD

The workflow at [`.github/workflows/daily-update.yml`](.github/workflows/daily-update.yml) orchestrates cloud execution:

```yaml
name: Daily Number Update

on:
  schedule:
    - cron: "*/30 * * * *"  # Runs every 30 minutes
  workflow_dispatch:        # Allows manual run from GitHub UI

permissions:
  contents: write

concurrency:
  group: daily-number-update
  cancel-in-progress: false

jobs:
  update-number:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.12"

      - name: Configure Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Run Scheduler
        run: python scheduler/scheduler.py
```

### Key Workflow Features:
- **Write Permissions:** `permissions: contents: write` grants the runner permission to push commits back to the repository.
- **Concurrency Locking:** `concurrency` prevents multiple scheduled runs from stepping on each other during Git operations.
- **Manual Trigger:** Easily test the workflow using the `workflow_dispatch` button under GitHub Actions.

---

## 🔧 Configuration

### Environment Variables

| Variable | Type | Default | Description |
|---|---|---|---|
| `FANCY_JOB_USE_LLM` | String / Flag | *Unset* | Enables Hugging Face GPT-2 commit message generation |

### Dependencies Specification (`pyproject.toml`)

```toml
[project]
name = "fancy-job"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
llm = [
    "torch>=2.5.1",
    "transformers>=4.47.1"
]
```

---

## 🔐 Security

- **Authentication:** Relies exclusively on the built-in `GITHUB_TOKEN` provided by GitHub Actions — no Personal Access Tokens (PATs) or private keys required.
- **Zero Telemetry / Data Sharing:** When LLM mode is used, inference runs locally on the runner with no external API calls.
- **Deterministic Dependencies:** `uv.lock` ensures package integrity and protects against supply-chain tampering.

---

## 🐛 Troubleshooting

<details>
<summary><strong>❌ Git Push Fails in GitHub Actions (Permission Denied / 403)</strong></summary>

**Cause:** Workflow lacks write permissions to the repository.

**Fix:**
1. Navigate to **Settings** → **Actions** → **General** in your repository.
2. Under **Workflow permissions**, choose **Read and write permissions**.
3. Save changes.
</details>

<details>
<summary><strong>❌ Scheduler Prints "Not due yet" When Triggered Manually</strong></summary>

**Cause:** The current UTC time has not reached the `"next_run"` timestamp in `scheduler/schedule.json`.

**Fix:**
- To force an immediate update via the scheduler, edit `scheduler/schedule.json` and set `"next_run"` to a timestamp in the past (e.g., `"2000-01-01T00:00:00+00:00"`), or invoke `python update_number.py` directly.
</details>

<details>
<summary><strong>❌ `ModuleNotFoundError: No module named 'transformers'`</strong></summary>

**Cause:** `FANCY_JOB_USE_LLM` is set, but optional dependencies are not installed.

**Fix:**
```bash
uv sync --extra llm
# or
pip install -e ".[llm]"
```
</details>

<details>
<summary><strong>❌ Corrupted `number.txt`</strong></summary>

**Cause:** `number.txt` should contain only a single valid integer.

**Fix:**
```bash
echo 0 > number.txt
```
</details>

---

## 🤝 Contributing

This repository was originally created as an experimental project and is not actively seeking pull requests or feature additions. You are welcome to **fork** the project and customize it for your own needs.

Please refer to [`CONTRIBUTING.md`](CONTRIBUTING.md) for further information.

---

## 📜 License

This project is currently distributed without a formal open source license. All rights are retained by the repository owner. If you wish to use or modify it, please fork the repository.

---

<p align="center">
  Built with 🐍 Python, ⚙️ GitHub Actions, and ☕
</p>
