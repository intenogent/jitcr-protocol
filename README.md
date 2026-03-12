# JITCR Protocol
**Just-In-Time Context Retrieval for Claude Desktop**

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
  Lives in : Documents\Claude_Desktop\{ProjectName}\ on your machine
  Loads    : Once at > start via filesystem MCP
  Contains : Project purpose, architecture, key paths, commands, notes

TIER 3 — Session logs (loaded conditionally)
  Lives in : Documents\Claude_Desktop\Sessions\{ProjectName}\logs\
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
2. Checks that your session folder exists — creates it if not
3. Checks git status in your project root
4. Loads Tier 2 — reads `JITCR_{ProjectName}.md` from your machine via filesystem MCP
5. Loads Tier 3 — reads the latest handoff file; reads recent journals only if
   the last session was marked BLOCKED or had unresolved issues
6. Displays a session header confirming everything is loaded and ready

This means Claude enters every session already knowing your project, your last
session's state, and any open issues — without you typing a word of explanation.

---

## Before JITCR vs. After JITCR

The same project context, shown two ways. The content is identical — only
where it lives and when it loads is different.

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
- Sessions Hub: Documents\Claude_Desktop\Sessions\{ProjectName}\logs\
- Universal Commands: Documents\Claude_Desktop\JITCR_Universal_Commands.md
- Git: active

## Project Purpose
{RoleDescription}

## Key File Paths
- Tier 2 guide : Documents\Claude_Desktop\{ProjectName}\JITCR_{ProjectName}.md
- Session logs : Documents\Claude_Desktop\Sessions\{ProjectName}\logs\
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
> backup  Zip project root to local backup

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
  Documents\Claude_Desktop\{ProjectName}\

## Environment
{Environment}

## Command Prefix
> = execute command — full reference in JITCR_{ProjectName}.md
```

**Tier 2 — JITCR_{ProjectName}.md (~350 tokens, loaded once at `> start`)**

```markdown
## Project Identity
| Field          | Value                                                        |
|----------------|--------------------------------------------------------------|
| Project Name   | {ProjectName}                                                |
| OS             | {OS}                                                         |
| Project Root   | {ProjectRoot}                                                |
| Sessions Hub   | Documents\Claude_Desktop\Sessions\{ProjectName}\logs\        |
| Universal Cmds | Documents\Claude_Desktop\JITCR_Universal_Commands.md         |
| Git            | active                                                       |

## Project Purpose
{RoleDescription}

## Key File Paths
| File             | Path                                                         |
|------------------|--------------------------------------------------------------|
| This file (T2)   | Documents\Claude_Desktop\{ProjectName}\JITCR_{ProjectName}.md|
| Session logs     | Documents\Claude_Desktop\Sessions\{ProjectName}\logs\        |
| Project root     | {ProjectRoot}                                                |

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
| > backup  | Zip project root                              |

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
| `> journal` | Writes timestamped activity log entry to your Sessions folder |
| `> handoff` | Creates a structured snapshot of the current session state |
| `> save` | Runs journal + handoff together in one step |
| `> status` | Shows last handoff, last journal entry, and git status |
| `> commit` | Git commits all project files with a structured message |
| `> end` | save + optional commit + displays session summary |
| `> backup` | Zips your entire project root to a local backup file |
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
Allows Claude to run terminal commands. Needed for `> commit`, `> end`, and
`> backup`. JITCR works without it but git commands will be unavailable.

**4. Git — optional**
Only needed if you want version control via `> commit` and `> end`.
Download from [git-scm.com](https://git-scm.com) if needed.

---

### Installation — 3 Steps

**Step 1:** Create a new Claude Desktop Project for your project.
*(Claude Desktop → Projects → New Project)*

**Step 2:** Start a new chat inside that project. Copy the entire prompt
from [INSTALL_PROMPT.md](./INSTALL_PROMPT.md) and paste it as your first message.

**Step 3:** Claude runs the interactive setup — silently checks your MCPs,
asks a few questions about your project, creates all folders and files on your
machine, then outputs your Tier 1 text. Copy that text into your Project
Instructions *(Project → Settings → Project Instructions)*.

Start a new session and type `> start`. JITCR is running.

---

## Repo Contents

```
jitcr-protocol/
├── README.md                    ← You are here
├── INSTALL_PROMPT.md            ← Paste as your first chat message to install
└── JITCR_Universal_Commands.md  ← Full command logic for all > commands
```

---

## Requirements

- Claude Desktop with Project Instructions support
- filesystem MCP — required
- shell-command MCP — recommended
- Windows 11, macOS, or Linux
- Git — optional

---

## License

MIT — use it, fork it, adapt it freely.

---

## Author

Built by [@intenogent](https://github.com/intenogent)
Issues and contributions welcome — open a GitHub issue or PR.
