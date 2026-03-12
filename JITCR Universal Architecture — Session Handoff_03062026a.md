# JITCR Universal Architecture — Session Handoff

**Date:** 2026-03-06
**Session Type:** Design & Architecture Discussion
**Status:** DESIGN COMPLETE — Awaiting Implementation Approval

---

## What Is JITCR?

JITCR (Just-In-Time Context Retrieval) is a token management **protocol** 
for Claude Desktop that solves a fundamental problem: LLM context windows 
are finite, and loading all instructions on every API call wastes tokens, 
accelerates compaction, and burns budget.

**Naming decision:** JITCR Protocol (not framework or approach)

- Protocol implies a defined contract with specific rules
- Predictable, implementable, consistent across users and projects
- Positions alongside established protocol terminology

**Inspiration:** JIT manufacturing and compilation — load what you need, 
when you need it, not everything upfront.

---

## The Core Problem JITCR Solves

```
WITHOUT JITCR:
System Prompt + ALL Instructions (1,500 tokens) × 20 messages = 30,000 tokens

WITH JITCR:
Tier 1 (300 tokens) × 20 messages    =  6,000 tokens
Tier 2 (1,200 tokens) × 1 load       =  1,200 tokens  
Tier 3 (~500 tokens) × 1 load        =    500 tokens
                                         ─────────────
Total:                                   7,700 tokens
Savings:                                74% reduction
```

Additional problems solved:

- Claude Desktop compaction mid-session loses all context → JITCR logs/handoffs 
  preserve it
- Starting new sessions means re-explaining everything → `> start` restores 
  full context in one command
- Files created in wrong environment (Claude Code VM vs MCP) → JITCR stays 
  100% in MCP layer (Node.js, Windows-native)
- No logging discipline → structured journal + handoff system per session

---

## Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    JITCR PROTOCOL LAYERS                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TIER 1 — PROJECT INSTRUCTIONS (Always-On, Compaction-Safe)│
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • Project name (used for auto-folder creation)      │   │
│  │ • OS declaration (Windows/macOS/Linux)              │   │
│  │ • Project root path                                 │   │
│  │ • 3-5 non-negotiable rules                          │   │
│  │ • Retrieval trigger: `> start`                      │   │
│  │ • Target: ~200-300 tokens MAX                       │   │
│  │ • Lives in: Claude Desktop Project Instructions     │   │
│  │ • Survives: compaction, new sessions                │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│                          ▼ triggered by `> start`           │
│  TIER 2 — CLAUDE_GUIDELINES.md (Loaded Once Per Session)   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • Full command reference (>, journal, handoff...)   │   │
│  │ • Session workflow protocols                        │   │
│  │ • Templates (journal, handoff, commit)              │   │
│  │ • Project-specific paths and architecture           │   │
│  │ • Git configuration (if applicable)                 │   │
│  │ • Target: 600-1,500 tokens                          │   │
│  │ • Lives in: project root folder on filesystem       │   │
│  │ • Loaded: once per session via filesystem MCP       │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│                          ▼ triggered by `> start` or demand │
│  TIER 3 — SESSION CONTEXT (On-Demand)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • Latest handoff document                           │   │
│  │ • Last 3 journal entries (conditional — see below)  │   │
│  │ • Relevant code files                               │   │
│  │ • Git log (last 5 commits)                          │   │
│  │ • Variable size — loaded selectively                │   │
│  │ • Lives in: Sessions\{ProjectName}\logs\            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Universal JITCR Architecture (New — Designed This Session)

### The Problem With Current JITCR

JITCR currently lives inside the Cigar Band Identifier project only.
Every new project requires manual setup: create CLAUDE_GUIDELINES.md,
set up logs/, wire Tier 1 trigger. Inconsistent across projects.

### The Solution: Universal Command Layer + Per-Project Logs

```
C:\Users\LaserMaster\Documents\Claude_Desktop\
│
├── JITCR_Universal_Commands.md        ← Shared command logic (all projects)
│
├── JITCR Framework\                   ← Framework documentation & specs
│   ├── JITCR_Framework.md
│   ├── JITCR_Framework02202026b.md    (v1.3 current)
│   ├── benchmark\
│   └── logs\
│
└── Sessions\                          ← Universal sessions hub
    ├── CigarBandIdentifier\           ← Auto-created on first > start
    │   └── logs\
    │       ├── journal_YYYY-MM-DD_HHMM.md
    │       └── handoff_YYYY-MM-DD_HHMM.md
    ├── CD_Opt\
    │   └── logs\
    ├── GeneralChats\                  ← Fallback for no-project sessions
    │   └── logs\
    └── {NewProject}\                  ← Auto-created per project name
        └── logs\
```

### How Auto-Folder Creation Works

`> start` reads project name from Tier 1, then:

```
1. Check if Sessions\{ProjectName}\ exists
2. If not → create it + logs\ subfolder automatically
3. All journals and handoffs route to that project's logs\
4. No manual folder creation ever needed
```

---

## `> start` Command — Full Universal Protocol

```
STEP 1: OS Detection (once, silent)
  → PowerShell: $env:OS → "Windows_NT"
  → bash: uname → "Darwin" (macOS) or "Linux"
  → Sets path separator and shell syntax for session

STEP 2: Project Folder Check
  → Read project name from Tier 1
  → If Sessions\{ProjectName}\ missing → create it
  → If no project name → route to Sessions\GeneralChats\

STEP 3: Git Status Check
  → Run: git -C "{project_root}" status
  → Result A: Active repo → git commands enabled
  → Result B: No repo → offer to initialize (yes/no prompt)
  → Result C: Repo exists, no remote → note it, local only

STEP 4: Load Tier 2
  → Read CLAUDE_GUIDELINES.md from project root
  → Confirm loaded, display token estimate

STEP 5: Load Tier 3 (Conditional)
  → Always: read latest handoff_*.md
  → Only if handoff shows BLOCKED or open issues:
    read last 3 journal_*.md
  → Run: git log -5 --oneline (if git active)

STEP 6: Display Session Header
  → Project name, OS, timestamp
  → Git status (active/inactive/no-repo)
  → Files loaded summary
  → Available commands reminder
```

---

## Cross-Platform Compatibility

JITCR runs natively on all three OS — no containers, no Docker needed.

| Element        | Windows                                              | macOS                                  | Linux                                  |
| -------------- | ---------------------------------------------------- | -------------------------------------- | -------------------------------------- |
| Sessions hub   | `C:\Users\{name}\Documents\Claude_Desktop\Sessions\` | `~/Documents/Claude_Desktop/Sessions/` | `~/Documents/Claude_Desktop/Sessions/` |
| Shell          | PowerShell                                           | bash/zsh                               | bash                                   |
| Path separator | `\` (filesystem MCP) / `/` (shell-command)           | `/`                                    | `/`                                    |
| Git            | Identical                                            | Identical                              | Identical                              |
| Detection      | `$env:OS` = Windows_NT                               | `uname` = Darwin                       | `uname` = Linux                        |

**User action required:** Declare OS and project root in Tier 1 once.
**Everything else:** Auto-detected and self-configuring at `> start`.

**Why NOT Docker:**

- JITCR is a protocol, not an application — nothing to containerize
- Docker would trap files inside a container = invisible on host filesystem
- Adds hard dependency (Docker Desktop) for zero functional gain
- OS detection in `> start` already solves cross-platform completely

---

## Execution Environment Clarity

**Critical distinction confirmed from system inspection:**

| Environment         | What It Is                           | Files Visible?            | JITCR Uses? |
| ------------------- | ------------------------------------ | ------------------------- | ----------- |
| MCP Layer (Node.js) | filesystem + shell-command MCPs      | ✅ Yes, Windows filesystem | ✅ YES       |
| Claude Code VM      | Sandboxed Linux VM (claudevm.bundle) | ❌ No, trapped in VM       | ❌ NEVER     |

**Rule:** Any JITCR operation that touches the filesystem must use the
filesystem MCP or shell-command MCP. Never Claude Code execution.
If you see Linux paths (/home/, /mnt/) in a response — you're in the VM.

---

## Git Integration — Universal Rules

**Git is project-specific, commands are universal:**

- `> commit` and `> end` commands live in JITCR_Universal_Commands.md
- Git repos initialize per-project under the project's filesystem path
- `> start` auto-checks git presence and offers initialization if missing
- git commands are silently skipped for GeneralChats (no repo = no error)

**Git initialization automation (built into `> start`):**

```
git init "{project_root}"
git config user.name "{name}"
git config user.email "{email}"
```

Runs only when `> start` detects no existing repo AND user confirms.

---

## Command Reference (Universal)

| Command     | Action                                       | Git Required? |
| ----------- | -------------------------------------------- | ------------- |
| `> start`   | Initialize session, detect OS, load Tier 2+3 | No            |
| `> journal` | Write session journal entry to logs\         | No            |
| `> handoff` | Create handoff snapshot for next session     | No            |
| `> save`    | Runs `> journal` + `> handoff`               | No            |
| `> status`  | Show git status, last journal, last handoff  | Optional      |
| `> commit`  | Git commit with formatted message            | YES           |
| `> end`     | Runs `> save` + `> commit` + session summary | Optional      |
| `> backup`  | Zip project folder to backup location        | No            |

---

## Logging: Conditional Tier 3 Loading (Optimization)

Current behavior: `> start` always loads last 3 journals (fixed token cost).
Improved behavior:

```
IF latest handoff status = COMPLETED/no open issues
  → Load handoff only (minimal Tier 3)
IF latest handoff status = BLOCKED or has open issues
  → Load handoff + last 3 journals (full Tier 3)
```

This makes Tier 3 truly on-demand — matches the original JITCR principle.

---

## Pending Feature: Dynamic MCP Loading

**Flagged for future discussion — not designed yet.**

Concept: Instead of all MCPs loading at Claude Desktop startup (always-on,
always consuming memory), explore whether MCPs can be loaded/unloaded
dynamically based on project context.

Known constraint from prior sessions:

- MCPs are Node.js processes spawned at CD startup
- They cannot be lazy-loaded mid-session currently
- JITCR principles could apply to MCP *response* data (what MCPs return)
  rather than MCP process lifecycle

**Status:** Design discussion pending. Do not implement until scoped.

---

## What JITCR Protocol Does NOT Do

- Does not containerize or use Docker
- Does not replace Claude Desktop Project Instructions (Tier 1 stays there)
- Does not lazy-load MCPs (separate future discussion)
- Does not require any software installation beyond existing MCPs
- Does not use the Claude Code VM — filesystem MCP only

---

## Current JITCR Version

Latest spec: `JITCR_Framework02202026b.md` (v1.3, 2026-02-20)
This handoff represents: **v2.0 Universal Architecture Design**
Implementation status: Design approved, not yet built

---

## Next Session Should

1. Review and approve this handoff document
2. Decide: implement universal structure now or continue design discussion
3. If approved → implement in this order:
   a. Create `Sessions\` hub folder structure
   b. Create `JITCR_Universal_Commands.md` with all universal commands
   c. Update Tier 1 template with OS + project name fields
   d. Build `> start` with OS detection + git check + conditional Tier 3
   e. Test on Cigar project first, then CD_Opt
4. Discuss Dynamic MCP Loading (separate session)
5. Build benchmark script (flagged since Feb 20, still pending)

---

## Key Decisions Made This Session

| Decision                                      | Rationale                                      |
| --------------------------------------------- | ---------------------------------------------- |
| JITCR = Protocol (not framework/approach)     | Implies defined contract, predictable behavior |
| Universal via shared command file, not Skills | Skills don't persist through compaction        |
| OS detection in `> start`, not Docker         | No new dependencies, native execution          |
| Auto-folder creation by project name          | Zero manual setup per project                  |
| Git check + optional init in `> start`        | Automation without assumption                  |
| Conditional Tier 3 loading                    | True JIT — load only what's needed             |
| GeneralChats fallback folder                  | JITCR works even without a project             |
| Claude Code VM = never for JITCR              | Files disappear — wrong environment            |
