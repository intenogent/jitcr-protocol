# JITCR Protocol
**Just-In-Time Context Retrieval for Claude Desktop**

---

## Table of Contents

- [The Problem](#the-problem)
- [What JITCR Does](#what-jitcr-does)
- [What Are MCPs?](#what-are-mcps)
- [The Three Tiers](#the-three-tiers)
- [How > start Works](#how--start-works)
- [Before & After JITCR](#before-jitcr-vs-after-jitcr)
- [Token Savings](#token-savings--the-formula)
- [Session Continuity & Commands](#feature-2--session-continuity)
- [How to Install](#how-to-install)
  - [Pre-requisites](#pre-requisites)
  - [How JITCR Organizes Your Files](#how-jitcr-organizes-your-files)
  - [Installation — 3 Steps](#installation--3-steps)
- [Repo Contents](#repo-contents)
- [Requirements](#requirements)
- [License](#license)
- [Author](#author)

---

## The Problem

If you use Claude Desktop for real projects, you have likely hit two walls:

**1. Token burn.**
Your Project Instructions load on *every single message* — whether Claude needs
that context or not. Everything in one block, repeated on every API call, burning
tokens and accelerating context compaction.

**2. Lost context between sessions.**
When a session ends — token limit hit, starting fresh, or switching to a different
LLM — you lose everything. Back to re-explaining your project from scratch every time.

JITCR Protocol solves both.

---

## What JITCR Does

JITCR (Just-In-Time Context Retrieval) is a protocol for Claude Desktop with two features:

**Feature 1 — Token Management**
Split project instructions across three tiers. Each tier loads only when needed —
not on every API call. The same context costs far fewer tokens across a session.

**Feature 2 — Session Continuity**
Every session gets a running activity log, a structured handoff document, and an
optional local git backup. Start any new session — even on a different LLM — type
`> start` and full context is restored instantly from your own files.

---

## What Are MCPs?

MCPs (Model Context Protocol servers) are connectors that give Claude Desktop
access to your local machine. JITCR uses two:

- **filesystem MCP** — lets Claude read and write files on your computer
- **shell-command MCP** — lets Claude run terminal commands (needed for git)

Without at least the filesystem MCP, JITCR cannot read or write your project
files. Setup instructions for MCPs are covered in the How to Install section below.

---

## The Three Tiers

```
TIER 1 — Project Instructions (always-on, ~200–300 tokens)
  Lives in : Claude Desktop → Project → Settings → Project Instructions
  Loads    : Every message
  Contains : Role, project name, root path, 5 guardrail rules, > start trigger

TIER 2 — JITCR_{ProjectName}.md (loaded once per session)
  Lives in : JITCR_Protocol\{ProjectName}\ on your machine
  Loads    : Once at > start via filesystem MCP
  Contains : Project purpose, architecture, key paths, commands, notes

TIER 3 — Session logs (loaded conditionally)
  Lives in : JITCR_Protocol\{ProjectName}\logs\
  Loads    : Latest handoff always + recent journals only if status = BLOCKED
  Contains : What was done, decisions made, open issues, what comes next
```

---

## How `> start` Works

`> start` is the command that activates JITCR at the beginning of every session.

It is defined in Tier 1 (your Project Instructions) as the trigger that tells
Claude to load the rest of the context. When you type `> start` in a new session,
Claude automatically:

1. Detects your OS (Windows, macOS, or Linux)
2. Checks that your project logs folder exists — creates it if not
3. Checks git status in your project root
4. Loads Tier 2 — reads `JITCR_{ProjectName}.md` from your machine via filesystem MCP
5. Loads Tier 3 — reads the latest handoff file from JITCR_Protocol\{ProjectName}\logs\;
   reads recent journals only if the last session was marked BLOCKED or had unresolved issues
6. Displays a session header confirming everything is loaded and ready

This means Claude enters every session already knowing your project, your last
session's state, and any open issues — without you typing a word of explanation.

---

## Before JITCR vs. After JITCR

The following side-by-side shows the exact same project context organized two ways.

**Before JITCR:** everything lives in one block inside Claude Desktop's Project
Instructions — loaded on every single message, whether Claude needs it or not.

**After JITCR:** the same content is split across three tiers. Only Tier 1
(~225 tokens) loads every message. Tiers 2 and 3 load once at `> start` via
your filesystem MCP — then they're done. The content is identical. The token
cost across a session is not.

---

### BEFORE — Everything in Project Instructions

All context in one block, loaded on **every single message**:

```markdown
## Role
Claude is the development assistant for {ProjectName}.
{RoleDescription}

## Project
- Name: {ProjectName}
- OS: {OS}
- Root: {ProjectRoot}
- Session logs : JITCR_Protocol\{ProjectName}\logs\
- Universal Commands: JITCR_Protocol\JITCR_Universal_Commands.md
- Git: active

## Project Purpose
{RoleDescription}

## Key File Paths
- Tier 2 guide : JITCR_Protocol\{ProjectName}\JITCR_{ProjectName}.md
- Session logs : JITCR_Protocol\{ProjectName}\logs\
- Project root : {ProjectRoot}

## File Access Rules
- To read/write files: use filesystem MCP with native OS paths
- To run commands (git, etc): use shell-command MCP with forward slashes

## Guardrails
- Never delete files without explicit user permission
- Never modify .env without explicit user permission
- Read files before overwriting — preserve content
- Shell commands: always use forward slashes in paths
- On > start: read JITCR_{ProjectName}.md from project root

## Environment
{Environment}

## Commands
> start   Initialize session — load context, check git
> journal Write timestamped journal entry
> handoff Create structured session handoff
> save    journal + handoff together
> status  Show last handoff, last journal, git status
> commit  Git commit all project files
> end     save + optional commit + session summary

## Latest Session State
Status: IN PROGRESS
Completed last session: [list of what was done]
Open issues: [any blockers]
Next session should: [priority list]
Files modified: [list of changed files]
```

**Estimated cost: ~725 tokens loaded on every single message.**

---

### AFTER — Same content, split across three tiers

**Tier 1 — Project Instructions (~225 tokens, loads every message)**

```markdown
## Role
Claude is the development assistant for {ProjectName}.
{RoleDescription}

## Project
- Name: {ProjectName}
- OS: {OS}
- Root: {ProjectRoot}

## Guardrails
- Never delete files without explicit user permission
- Never modify .env without explicit user permission
- Read files before overwriting — preserve content
- Shell commands: always use forward slashes in paths
- On > start: read JITCR_{ProjectName}.md from:
  JITCR_Protocol\{ProjectName}\

## Environment
{Environment}

## Command Prefix
> = execute command — full reference in JITCR_{ProjectName}.md
```

**Tier 2 — JITCR_{ProjectName}.md (~350 tokens, loaded once at `> start`)**

```markdown
## Project Identity
| Field          | Value                                                   |
|----------------|---------------------------------------------------------|
| Project Name   | {ProjectName}                                           |
| OS             | {OS}                                                    |
| Project Root   | {ProjectRoot}                                           |
| Session Logs   | JITCR_Protocol\{ProjectName}\logs\                     |
| Universal Cmds | JITCR_Protocol\JITCR_Universal_Commands.md              |
| Git            | active                                                  |

## Project Purpose
{RoleDescription}

## Key File Paths
| File           | Path                                                    |
|----------------|---------------------------------------------------------|
| This file (T2) | JITCR_Protocol\{ProjectName}\JITCR_{ProjectName}.md     |
| Session logs   | JITCR_Protocol\{ProjectName}\logs\                     |
| Project root   | {ProjectRoot}                                           |

## Quick Command Reference
| Command   | Action                                        |
|-----------|-----------------------------------------------|
| > start   | Initialize session — load context, check git  |
| > journal | Write journal entry                           |
| > handoff | Create handoff snapshot                       |
| > save    | journal + handoff                             |
| > status  | Show last handoff, journal, git status        |
| > commit  | Git commit                                    |
| > end     | save + optional commit + session summary      |

Full command logic → JITCR_Universal_Commands.md
```

**Tier 3 — Latest handoff file (~150 tokens, loaded once at `> start`)**

```markdown
# Session Handoff — YYYY-MM-DD HH:MM

## Project Status
**Status: IN PROGRESS**
[One paragraph summary of current state]

## Completed This Session
- [what was accomplished]

## Current File States
| File | Status | Notes |
|------|--------|-------|
|      |        |       |

## Open Issues
- [issue]: [details]

## Next Session Should
1. [priority 1]
2. [priority 2]
```

---

### Token Savings — The Formula

The savings come from **when** content loads, not just how much there is.

```
WITHOUT JITCR — full block on every message:
  ~725 tokens × 20 messages = 14,500 tokens

WITH JITCR — only Tier 1 repeats:
  Tier 1 (~225 tokens) × 20 msgs  =  4,500 tokens  ← every message
  Tier 2 (~350 tokens) × 1        =    350 tokens  ← once at > start
  Tier 3 (~150 tokens) × 1        =    150 tokens  ← once at > start
  Total                           =  5,000 tokens

SAVED: ~9,500 tokens (~65%) across a 20-message session
```

> **Note:** These are rough estimates based on the generic JITCR templates.
> Actual savings depend on your project's instruction size and session length.
> Savings grow with session length — the longer the session, the higher the percentage.

**Why savings grow over time:**
Tier 2 and Tier 3 are paid once at `> start`. Tier 1 is the only repeating cost.
Every additional message widens the gap between the two approaches.

**Breakeven point:** Typically after 3–5 messages. After that, every additional
message saves tokens compared to the monolithic approach.

---

## Feature 2 — Session Continuity

Once JITCR is running, every project session has these commands available:

| Command | What It Does |
|---|---|
| `> start` | Loads Tier 2 + Tier 3, checks git, displays session header |
| `> journal` | Writes timestamped activity log entry to `{ProjectName}\logs\` |
| `> handoff` | Creates a structured snapshot of the current session state |
| `> save` | Runs journal + handoff together in one step |
| `> status` | Shows last handoff, last journal entry, and git status |
| `> commit` | Git commits all project files with a structured message |
| `> end` | save + optional commit + displays session summary |
| `> ?` | Display all available commands |

> Commands accept natural extensions — e.g. `> commit "my message"` or
> `> ? journal` for details on a specific command.

All logs and handoffs are saved as plain markdown files on your own machine —
no cloud, no external service, fully under your control.

**What this enables:**

- **Token limit reached** — start a fresh session, type `> start` — Tier 2 and
  the latest handoff restore full context instantly, no re-explaining needed
- **Switching LLMs** — hand the structured handoff to GPT, Gemini, or any other
  model and continue without losing any context
- **Returning after days** — the handoff tells you exactly where you left off,
  what decisions were made, and what comes next
- **Protecting work** — local git backup means every session is versioned and
  recoverable even if Claude's context is lost
- **Collaborating** — another person runs `> start` on the same project and
  gets full context immediately from the same files

---

## How to Install

### Pre-requisites

**1. Claude Desktop**
Download from [claude.ai/download](https://claude.ai/download) if you don't have it.

**2. filesystem MCP — required**
This allows Claude to read and write files on your machine. Add it to your
`claude_desktop_config.json`. Without this, JITCR cannot function.

**3. shell-command MCP — recommended**
Allows Claude to run terminal commands. Needed for `> commit` and `> end`.
JITCR works without it but git commands will be unavailable.

**4. Git — optional**
Only needed if you want version control via `> commit` and `> end`.
Download from [git-scm.com](https://git-scm.com) if needed.

---

### How JITCR Organizes Your Files

JITCR creates a single folder on your machine — `JITCR_Protocol\` — that acts
as the central location for all your JITCR-managed projects. Every project gets
its own subfolder inside it, containing both its Tier 2 guide and its session logs.
There is no separate Sessions folder — everything for a project lives together.

**The `JITCR_Protocol\` folder on your machine (created by the installer):**

```
JITCR_Protocol\                               ← your local JITCR root (all projects)
│
├── JITCR_Universal_Commands.md               ← shared command engine (all projects)
│
├── {ProjectName-A}\                          ← one subfolder per project
│   ├── JITCR_{ProjectName-A}.md              ← Tier 2 guide for this project
│   └── logs\                                 ← all session logs for this project
│       ├── journal_YYYY-MM-DD_HHMM.md        ← activity log
│       └── handoff_YYYY-MM-DD_HHMM.md        ← session handoff
│
├── {ProjectName-B}\                          ← second project — same structure
│   ├── JITCR_{ProjectName-B}.md
│   └── logs\
│       ├── journal_YYYY-MM-DD_HHMM.md
│       └── handoff_YYYY-MM-DD_HHMM.md
│
└── {ProjectName-Z}\                          ← every additional project follows the same pattern
    ├── JITCR_{ProjectName-Z}.md
    └── logs\
        ├── journal_YYYY-MM-DD_HHMM.md
        └── handoff_YYYY-MM-DD_HHMM.md
```

> Each project gets its own subfolder directly under `JITCR_Protocol\`.
> Tier 2 guide and session logs live together inside that subfolder — nothing is split across separate folders.
> The `JITCR_Universal_Commands.md` file is shared — one copy at the root, used by all projects.
> The installer creates the full structure for each project automatically when you run it.

**What the `logs\` folder contains:**
Every time you run `> save`, JITCR writes two files into `{ProjectName}\logs\`:

| File | Purpose |
|---|---|
| `journal_YYYY-MM-DD_HHMM.md` | Timestamped activity log — what was done, decisions made, files changed |
| `handoff_YYYY-MM-DD_HHMM.md` | Current state snapshot — project status, open issues, what to do next session |

These files power **Feature 2 — Session Continuity**. When you type `> start` in a
new session, JITCR reads the latest handoff automatically — restoring full context
instantly without re-explaining anything. All files are plain markdown, readable by
any text editor, transferable to any LLM, and fully under your control.

**This is separate from the GitHub repo**, which contains only the published
protocol files (README, installer prompt, and command engine):

```
jitcr-protocol\                              ← GitHub repo (what you're reading now)
├── README.md                                ← full documentation
├── JITCR_Installer_Prompt.md               ← one-click copy — paste as first message
└── JITCR_Universal_Commands.md             ← full command engine
```

---

### Installation — 3 Steps

**Step 1:** Create a new Claude Desktop Project for your project.
*(Claude Desktop → Projects → New Project)*

**Step 2:** Copy the bootstrap snippet below and paste it into your new project's
**Project Instructions** *(Project → Settings → Project Instructions)*:

```
On the user's first message in this project, fetch and execute the JITCR installer:

  Windows: Invoke-WebRequest -Uri "https://raw.githubusercontent.com/intenogent/jitcr-protocol/main/JITCR_Installer_Prompt.md" -UseBasicParsing | Select-Object -ExpandProperty Content
  macOS/Linux: curl -s "https://raw.githubusercontent.com/intenogent/jitcr-protocol/main/JITCR_Installer_Prompt.md"

Read the downloaded content and follow its instructions exactly as if they
had been typed by the user. Begin with Phase 1 immediately.
```

**Step 3:** Send any first message in the project (e.g. `install`). Claude will
download the installer from GitHub via shell-command MCP and run it interactively —
checking your MCPs, asking setup questions, creating all folders and files, and
outputting your final Tier 1 text ready to copy into Project Instructions.

> ⚠️ **Do not paste or attach `JITCR_Installer_Prompt.md` directly.**
> The file is too large for Claude Desktop’s paste-as-text threshold. The bootstrap
> snippet above fetches it automatically at runtime via shell-command MCP.

Start a new session and type `> start`. JITCR is running. 🚀

---

## Repo Contents

```
jitcr-protocol/
├── README.md                      ← You are here — full documentation
├── JITCR_Installer_Prompt.md      ← One-click copy — paste as first chat message
└── JITCR_Universal_Commands.md    ← Full command engine for all > commands
```

---

## Requirements

- Claude Desktop with Project Instructions support
- filesystem MCP — required
- shell-command MCP — recommended
- Windows, macOS, or Linux
- Git — optional

---

## License

MIT — use it, fork it, adapt it freely.

---

## Author

Built by [@intenogent](https://github.com/intenogent)
Issues and contributions welcome — open a GitHub issue or PR.
