JITCR Protocol
Context management protocol for Claude Desktop. 3-tier architecture: 65% token savings, session continuity across LLMs, defense-in-depth safety controls.
What This Is
JITCR Protocol is a specification and setup guide — not a downloadable tool or software you run.
This repository contains:
📋 The JITCR Protocol specification (how context management works)
📖 Setup instructions for your Claude Desktop project
🗂️ Directory structure guidelines
⚙️ Command templates and workflows
You don't clone this to run it. Instead, you read it and implement it in your own Claude Desktop projects.
How to Use This Repository
Read the specification sections to understand how JITCR works
Copy the setup instructions from JITCR_Installer_Prompt.md
Paste those instructions into your Claude Desktop project settings
Follow the directory structure guide to organize your context
Use the commands and workflows from JITCR_Universal_Commands.md
That's it. You're now using JITCR.
Why JITCR?
Without proper context management in Claude Desktop, you run into:
📈 Token bloat — unnecessary repetition wastes tokens and costs
🔄 Lost context — sessions don't maintain continuity across conversations
⚠️ No safety guardrails — unstructured context can lead to errors
JITCR solves this by organizing your context into three safety layers with built-in efficiency checks.
Quick Start
Want to see if JITCR is right for you?
Check out the "The Problem" section in the README
Skim the "What JITCR Does" section
Review "The Three Tiers" to understand the approach
If interested, jump to "How to Install" to get started


# JITCR Protocol
**Just-In-Time Context Retrieval for Claude Desktop**

---

## Table of Contents

- [The Problem](#the-problem)
- [What JITCR Does](#what-jitcr-does)
- [Control Layers — Safety Architecture](#control-layers--safety-architecture)
- [What Are MCPs?](#what-are-mcps)
- [The Three Tiers](#the-three-tiers)
- [How > start Works](#how--start-works)
- [Before & After JITCR](#before-jitcr-vs-after-jitcr)
- [Token Savings](#token-savings--the-formula)
- [Session Continuity & Commands](#feature-2--session-continuity)
- [How to Install](#how-to-install)
  - [Pre-requisites](#pre-requisites)
  - [How JITCR Organizes Your Files](#how-jitcr-organizes-your-files)
    - [Where JITCR_Protocol/ Is Created](#where-jitcr_protocol-is-created)
    - [Two Paths: JITCR Management vs. Your Project](#two-paths-jitcr-management-vs-your-project)
    - [What Gets Committed and Pushed](#what-gets-committed-and-pushed)
  - [Installation — 3 Steps](#installation--3-steps)
- [Repo Contents](#repo-contents)
- [Requirements](#requirements)
- [License](#license)
- [Author](#author)

---

## The Problem

If you use Claude Desktop for real projects, you have likely hit three walls:

**1. Token burn.**
Your Project Instructions load on *every single message* — whether Claude needs
that context or not. Everything in one block, repeated on every API call, burning
tokens and accelerating context compaction.

**2. Lost context between sessions.**
When a session ends — token limit hit, starting fresh, or switching to a different
LLM — you lose everything. Back to re-explaining your project from scratch every time.

**3. Risk and safety in AI workflows.**
As AI assistants gain more capabilities (file access, git commands, external operations),
how do you ensure they operate safely? Default constraints are needed, plus approval
workflows for critical operations, and full transparency about what's happening.

JITCR Protocol solves all three.

---

## What JITCR Does

JITCR (Just-In-Time Context Retrieval) is a protocol for Claude Desktop with three features:

**Feature 1 — Token Management**
Split project instructions across three tiers. Each tier loads only when needed —
not on every API call. The same context costs far fewer tokens across a session.

**Feature 2 — Session Continuity**
Every session gets a running activity log, a structured handoff document, and an
optional local git backup. Start any new session — even on a different LLM — type
`> start` and full context is restored instantly from your own files.

**Feature 3 — Control Layers (Safety Architecture)**
A multi-layered approach to safety combining preventive guardrails, human-in-the-loop 
approvals, and full transparency. Default controls protect every project; both 
prevention and approval can be customized per project's specific needs.

---

## Control Layers — Safety Architecture

JITCR implements a defense-in-depth approach to AI safety:

### Layer 1: Preventive Guardrails (Defaults)

Default constraints that stop harmful actions before they occur:

- Never delete files without explicit user permission
- Never modify .env without explicit user permission
- Read existing files before overwriting — preserve content
- Shell commands: always use forward slashes in paths
- On > start: read from explicit, verified paths only

These guardrails are automatically included in every project's Tier 1 instructions.

### Layer 2: Human-in-the-Loop Approval (Defaults)

Critical operations require explicit user confirmation:

- **GitHub push approval** — User confirms before pushing to GitHub at `> end`
- **Git initialization approval** — User chooses whether to initialize git during setup
- **GitHub configuration approval** — User selects push behavior at setup time (yes/no/local-only)

### Layer 3: Transparency & Observability

Users know exactly what's enabled and what's happening:

- **Session headers** display git status and GitHub configuration at session start
- **Handoff files** track completions, decisions, and open issues
- **All logs stored locally** as readable markdown files — no cloud, full control

### Customizable Per Project

These defaults apply to all JITCR projects. Both prevention guardrails and approval 
workflows can be customized to match your project's specific requirements, sensitivity 
levels, and team workflows.

See your project's Tier 2 guide (`JITCR_[ProjectName].md`) to extend or modify controls 
for your specific needs. Examples include:

- Adding approval workflows for risky operations
- Defining rules for sensitive data handling (API keys, credentials)
- Customizing path verification rules
- Requiring additional confirmations before git operations
- Implementing compliance or audit requirements

**Why Layered Controls Matter**

Default controls provide immediate safety for any JITCR project. Customizable layers 
let teams implement controls matching their specific risk profiles — sensitive data 
handling, compliance requirements, team workflows, and project sensitivity levels.

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
  Contains : Role, project name, root path, guardrails, > start trigger

TIER 2 — JITCR_{ProjectName}.md (loaded once per session)
  Lives in : JITCR_Protocol/{ProjectName}/ on your machine
  Loads    : Once at > start via filesystem MCP
  Contains : Project purpose, architecture, key paths, GitHub config, commands, notes

TIER 3 — Session logs (loaded conditionally)
  Lives in : JITCR_Protocol/{ProjectName}/logs/
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
4. Loads GitHub config from Tier 2 — reads `GitHub Remote` and `GitHub Push` fields
   and stores them for the session (silently)
5. Loads Tier 2 — reads `JITCR_{ProjectName}.md` from your machine via filesystem MCP
6. Loads Tier 3 — reads the latest handoff file from `JITCR_Protocol/{ProjectName}/logs/`;
   reads recent journals only if the last session was marked BLOCKED or had unresolved issues
7. Displays a session header confirming everything is loaded and ready, including
   whether GitHub push is enabled or local-only for this project

This means Claude enters every session already knowing your project, your last
session's state, open issues, and whether GitHub push is configured — without you
typing a word of explanation.

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
- Session logs : JITCR_Protocol/{ProjectName}/logs/
- Universal Commands: JITCR_Protocol/JITCR_Universal_Commands.md
- Git: active

## Project Purpose
{RoleDescription}

## Key File Paths
- Tier 2 guide : JITCR_Protocol/{ProjectName}/JITCR_{ProjectName}.md
- Session logs : JITCR_Protocol/{ProjectName}/logs/
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
> commit  Git commit all project files locally
> end     save + commit locally + optional GitHub push

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
  JITCR_Protocol/{ProjectName}/

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
| Session Logs   | JITCR_Protocol/{ProjectName}/logs/                      |
| Universal Cmds | JITCR_Protocol/JITCR_Universal_Commands.md              |
| Git            | active                                                  |
| GitHub Remote  | {https://github.com/username/repo.git or none}          |
| GitHub Push    | {yes / no}                                              |

## Project Purpose
{RoleDescription}

## Key File Paths
| File           | Path                                                    |
|----------------|---------------------------------------------------------|
| This file (T2) | JITCR_Protocol/{ProjectName}/JITCR_{ProjectName}.md     |
| Session logs   | JITCR_Protocol/{ProjectName}/logs/                      |
| Project root   | {ProjectRoot}                                           |

## Quick Command Reference
| Command   | Action                                              |
|-----------|-----------------------------------------------------|
| > start   | Initialize session — load context, check git        |
| > journal | Write journal entry                                 |
| > handoff | Create handoff snapshot                             |
| > save    | journal + handoff (no git)                          |
| > status  | Show last handoff, journal, git status              |
| > commit  | Commit project files to local git only              |
| > end     | save + commit locally + optional GitHub push        |

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
| `> start` | Loads Tier 2 + Tier 3, checks git, loads GitHub config, displays session header |
| `> journal` | Writes timestamped activity log entry to `{ProjectName}/logs/` |
| `> handoff` | Creates a structured snapshot of the current session state |
| `> save` | Runs journal + handoff together — no git involved |
| `> status` | Shows last handoff, last journal entry, and git status |
| `> commit` | Commits project files to **local git only** — never pushes to GitHub |
| `> end` | Runs save + always commits locally + asks about GitHub push if configured |
| `> ?` | Display all available commands |

> Commands accept natural extensions — e.g. `> commit "my message"` or
> `> ? journal` for details on a specific command.

### How `> commit` and `> end` differ

| | `> commit` | `> end` |
|---|---|---|
| Saves journal + handoff | ❌ | ✅ always |
| Commits to local git | ✅ always | ✅ always |
| Pushes to GitHub | ❌ never | ✅ asks — only if configured |
| When to use | Mid-session checkpoint | End of session |

**The rule is simple:**
- Use `> commit` often during a session to checkpoint your work locally
- Use `> end` when you are done — it saves everything, commits locally, and
  asks whether to push to GitHub if your project is configured for it
- If your project has no GitHub remote configured, `> end` never asks about push —
  local commit is always the final step

### GitHub push is opt-in — configured at setup

During the JITCR installer, you are asked whether this project will push to GitHub
and what the remote URL is. This is stored in your Tier 2 guide (`GitHub Remote`
and `GitHub Push` fields). From then on:

- If `GitHub Push = yes` — `> end` will ask "Push to GitHub now? (yes/no)" every session
- If `GitHub Push = no` — push is never mentioned, local commit is always final

This means local-only projects are never prompted about GitHub, and GitHub-connected
projects are always reminded at the right moment — end of session.

All logs and handoffs are saved as plain markdown files on your own machine —
no cloud, no external service, fully under your control.

**What this enables:**

- **Token limit reached** — start a fresh session, type `> start` — Tier 2 and
  the latest handoff restore full context instantly, no re-explaining needed
- **Switching LLMs** — hand the structured handoff to GPT, Gemini, or any other
  model and continue without losing any context
- **Returning after days** — the handoff tells you exactly where you left off,
  what decisions were made, and what comes next
- **Protecting work** — local git commit at every `> end` means your work is always
  versioned locally, even if you never push to GitHub
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

#### Where `JITCR_Protocol/` Is Created

The first thing the installer asks (Q0) is where to create the `JITCR_Protocol/`
folder — the central hub for all your JITCR-managed projects on this machine.
**You are in full control of this location.** The installer suggests OS-based defaults:

| OS | Default location |
|---|---|
| Windows | `C:\Users\{YourUsername}\Documents\JITCR_Protocol/` |
| macOS | `~/Documents/JITCR_Protocol/` |
| Linux | `~/Documents/JITCR_Protocol/` |

Press Enter to accept the default, or type any custom path. This folder is created
once and shared across all your JITCR projects on this machine.

> **Important:** `JITCR_Protocol/` is the JITCR management hub only — it stores
> Tier 2 guides and session logs. Your actual project files stay wherever they
> already are. See [Two Paths](#two-paths-jitcr-management-vs-your-project) below.

---

#### Two Paths: JITCR Management vs. Your Project

This is the most important concept to understand before installing JITCR.
Every JITCR project has **two distinct paths** that serve completely different purposes:

**Path A — JITCR Management Path**
`JITCR_Protocol/{ProjectName}/`

This is where JITCR stores its own operational files:
- `JITCR_{ProjectName}.md` — the Tier 2 guide (project context, paths, GitHub config)
- `logs/` — all journals and handoffs (session memory)

These files are **private by design**. They are never committed to git and never
pushed to GitHub. They exist only to give Claude context across sessions.

**Path B — Project Root**
`{ProjectRoot}` — anywhere on your machine

This is where your actual work lives — code, writing, presentations, protocol
files, or any content Claude is helping you build. This is what git tracks.
This is what gets committed by `> commit` and pushed by `> end`.

**These two paths are intentionally separate** and the installer asks you to
define them independently at Q2.

---

**Three common setups:**

```
SETUP 1 — Separate paths (recommended for most projects)

  JITCR_Protocol/MyApp\                  ← Path A: JITCR management only
    ├── JITCR_MyApp.md                   ← Tier 2 guide
    └── logs/                            ← journals + handoffs (never committed)

  C:\Dev\MyApp\                          ← Path B: your actual project
    ├── src\
    ├── README.md
    └── .gitignore                       ← controls what git tracks here

  → JITCR management and project files are cleanly separated.
    Git only sees C:\Dev\MyApp\ — logs never at risk of being committed.


SETUP 2 — Same path (press Enter at Q2 — simplest setup)

  JITCR_Protocol/MyApp\                  ← Path A AND Path B in one folder
    ├── JITCR_MyApp.md                   ← Tier 2 guide
    ├── logs/                            ← journals + handoffs
    └── [your project files here]        ← also here

  → Works fine, but your .gitignore MUST exclude logs/ and JITCR_MyApp.md
    to prevent session memory from being committed to git.


SETUP 3 — Linking an existing project (type path at Q2)

  JITCR_Protocol/MyApp\                  ← Path A: JITCR management only
    ├── JITCR_MyApp.md
    └── logs/

  C:\Users\Me\Documents\Existing-Work\   ← Path B: pre-existing folder linked at Q2
    ├── [existing files]
    └── .gitignore

  → Ideal when your project already exists somewhere else on your machine.
    Just point JITCR at it — nothing moves, nothing changes in your project folder.
```

> **Recommendation — Project naming:** Use the same name for your JITCR project
> (Q1) as your Claude Desktop project name. This keeps `JITCR_Protocol/{ProjectName}/`
> clearly linked to the right Claude Desktop project, especially when managing multiple projects.

---

#### What Gets Committed and Pushed

> ⚠️ **Read this before using git with JITCR.**

`> commit` and `> end` operate on **Path B (Project Root)** only — not on the
JITCR management path. What gets committed and what gets pushed is controlled
entirely by the `.gitignore` file in your Project Root.

**Key rules:**

- **JITCR session logs are private** — journals and handoffs in `logs/` should
  always be excluded from git, whether they live in the same folder as your
  project or not. Add `logs/` to your `.gitignore` if they share a folder.

- **Public repos need a whitelist** — if your project root is a public GitHub
  repo, use a whitelist `.gitignore` (like this protocol does) that explicitly
  names only the files you want published. Everything else is excluded by default.

- **Private/local projects** — git tracks everything not excluded by `.gitignore`.
  Make sure your `.gitignore` is correct before running `> end` with GitHub push enabled.

- **`> commit` is always local** — it never touches GitHub regardless of your
  `.gitignore`. Only `> end` can push, and only after you confirm.

- **If in doubt, use Setup 1** — keeping Path A and Path B separate eliminates
  any risk of accidentally committing JITCR management files.

**Example `.gitignore` for a public repo (whitelist approach):**
```
# Exclude everything by default
*

# Explicitly allow only what should be published
!.gitignore
!README.md
!src/
!src/**
```

**Example `.gitignore` for a private project with JITCR in the same folder:**
```
# Exclude JITCR management files
logs/
JITCR_*.md
```

---

**The `JITCR_Protocol/` folder on your machine (created by the installer):**

```
JITCR_Protocol/                               ← your local JITCR hub (Path A for all projects)
│
├── JITCR_Universal_Commands.md               ← shared command engine (all projects)
│
├── {ProjectName-A}\                          ← one subfolder per project
│   ├── JITCR_{ProjectName-A}.md              ← Tier 2 guide for this project
│   └── logs/                                 ← all session logs for this project
│       ├── journal_YYYY-MM-DD_HHMM.md        ← activity log
│       └── handoff_YYYY-MM-DD_HHMM.md        ← session handoff
│
├── {ProjectName-B}\
│   ├── JITCR_{ProjectName-B}.md
│   └── logs/
│
└── {ProjectName-Z}\
    ├── JITCR_{ProjectName-Z}.md
    └── logs/
```

> Each project's JITCR management files live under `JITCR_Protocol/{ProjectName}/`.
> The actual project files live at `{ProjectRoot}` — wherever you defined it at Q2.
> The `JITCR_Universal_Commands.md` file is shared — one copy at the hub root,
> used by all projects.

**What the `logs/` folder contains:**
Every time you run `> save`, JITCR writes two files into `{ProjectName}/logs/`:

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

**Step 1:** Create a new Claude Desktop Project.
*(Claude Desktop → Projects → New Project)*

> **Recommendation:** Name your Claude Desktop project the same as your JITCR
> project name (Q1 in the installer). This keeps your `JITCR_Protocol/{ProjectName}/`
> folder clearly linked to the right Claude Desktop project when managing multiple projects.

**Step 2:** Download `JITCR_Installer_Prompt.md` from this repo (click the file →
click the download icon), then attach it to a new chat message in your project
along with this trigger prompt:

```
You are running inside Claude Desktop with filesystem MCP and shell-command MCP
available. Please use the attached file to set up the JITCR Protocol for this
project. Follow its instructions exactly, starting with Phase 1.
```

When Claude asks for confirmation to proceed, type `yes`. The installer runs
interactively — checking your MCPs, asking a few questions, and creating all
files and folders automatically.

> **Note on Q0 — Hub location:** The installer asks where to create
> `JITCR_Protocol/`. Press Enter to accept the OS default or type a custom path.
> See [Where JITCR_Protocol/ Is Created](#where-jitcr_protocol-is-created) above.

> **Note on Q2 — Project folder:** The installer asks whether you have an existing
> folder to link as your Project Root. If this is a new project, press Enter —
> your project folder defaults to `JITCR_Protocol/{ProjectName}/` (same as the
> JITCR management path). If your project already exists elsewhere on your machine,
> type that path. See [Two Paths](#two-paths-jitcr-management-vs-your-project)
> above for implications of each choice.

> **Note on Q5 — Git and GitHub:** The installer asks whether you want git
> initialized and whether you plan to push to GitHub. If you provide a GitHub
> remote URL, it is stored in your Tier 2 guide and used by `> end` to offer
> a push at the end of every session. If you choose local-only, GitHub push
> is never mentioned again for that project. See
> [What Gets Committed and Pushed](#what-gets-committed-and-pushed) above.

**Step 3:** When the installer finishes, it outputs your **Tier 1 text**. Copy it and
paste it into **Project → Settings → Project Instructions**. Start a new chat and
type `> start`. JITCR is running. 🚀

---

## Repo Contents

```
jitcr-protocol/
├── README.md                      ← You are here — full documentation
├── JITCR_Installer_Prompt.md      ← Installer prompt — fetched automatically at install time
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


