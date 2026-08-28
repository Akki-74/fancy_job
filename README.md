# Daily Number Incrementer

<p align="center">
  <strong>Automated daily number increments, Git commits, and GitHub pushes — running entirely in the cloud.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GitHub%20Actions-Automation-2088FF?logo=githubactions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Dependencies-Standard%20Library-4CAF50" alt="Dependencies">
</p>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Local Usage](#local-usage)
- [GitHub Actions](#github-actions)
- [Scheduling](#scheduling)
- [GitHub Actions Permissions](#github-actions-permissions)
- [Manual Workflow Execution](#manual-workflow-execution)
- [LLM Commit Messages](#llm-commit-messages)
- [Configuration](#configuration)
- [Git Configuration](#git-configuration)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Development](#development)
- [Contributing](#contributing)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [License](#license)

---

# Overview

**Daily Number Incrementer** is a lightweight Python automation project that increments a sequential number stored in a text file, creates a Git commit, and pushes the change to GitHub.

The project is designed to run automatically using **GitHub Actions**, allowing the entire process to run in GitHub's cloud infrastructure without requiring the user's local computer to be turned on.

The project can also be executed manually from a local machine for testing or development.

---

# Features

- 🔢 Automatically increments a sequential number
- 📄 Stores the number in `number.txt`
- 📝 Automatically creates Git commits
- 🚀 Automatically pushes changes to GitHub
- ☁️ Runs automated jobs using GitHub Actions
- ⏰ Daily automated execution
- 🎲 Selects a different execution time slot each day
- 🧠 Optional LLM-generated commit messages
- 🐍 Written in Python
- 📦 Uses the Python standard library for basic operation
- 🔐 Uses GitHub Actions' built-in `GITHUB_TOKEN`
- 💻 Supports local execution
- 🛠️ Can be manually triggered from GitHub Actions

---

# Architecture

The project consists of a Python script and a GitHub Actions workflow.

```text
┌──────────────────────────────────────────────┐
│              GitHub Repository               │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │ .github/workflows/daily-update.yml    │  │
│  └───────────────────┬────────────────────┘  │
│                      │                       │
└──────────────────────┼───────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  GitHub Actions │
              │  Cloud Runner   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ update_number.py│
              └────────┬────────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
      ┌──────────────┐    ┌──────────────┐
      │ Read number  │    │ Git commands │
      │ Increment    │    │ Commit       │
      │ Write number │    │ Push         │
      └──────┬───────┘    └──────┬───────┘
             │                   │
             ▼                   │
      ┌──────────────┐            │
      │  number.txt  │────────────┘
      └──────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ GitHub Repository│
              │   Updated file  │
              └─────────────────┘
