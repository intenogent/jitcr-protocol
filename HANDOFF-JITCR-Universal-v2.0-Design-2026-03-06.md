# JITCR Universal Architecture — Session Handoff
**Date:** 2026-03-06
**Session Type:** Design & Architecture Discussion
**Status:** DESIGN COMPLETE — Awaiting Implementation Approval
**Reference:** Earlier draft saved as `JITCR Universal Architecture — Session Handoff_03062026a.md`

---

## What Is JITCR?

JITCR (Just-In-Time Context Retrieval) is a token management **protocol** for Claude Desktop
that solves a fundamental problem: stuffing all instructions into Claude Desktop Project
Instructions means they load on every API call — wasting tokens, accelerating context
compaction, and burning budget unnecessarily.

### Naming Decision: Protocol
JITCR is formally a **Protocol** — not a framework or approach.
- Protocol implies a defined contract with specific rules and behaviors
- Predictable and implementable consistently across users, projects, and operating systems
- Positions alongside established protocol terminology (communication protocols, etc.)
- Abbreviation: **JITCR-P** if needed to distinguish spec from implementation

**Inspiration:** JIT (Just-In-Time) manufacturing and compilation principles —
load what you need, when you need it, not everything upfront.

---

## The Core Problem JITCR Solves

### Token Burn Without JITCR
When all instructions live in Claude Desktop Project Instructions, they load on every
single API call — multiplied across every message in a session:

```
Token cost = (All instruction tokens) × (number of messages in session)
```

As conversation length grows, this overhead compounds rapidly, exhausting the context
window faster and forcing compaction or new sessions.

### Token Savings With JITCR (Scalable Formula)
```
Tier 1 tokens  × (all messages)    = always-on cost (minimized)
Tier 2 tokens  × 1 load            = one-time session cost
Tier 3 tokens  × 1 conditional load = on-demand cost

Total = far less than (all tokens × all messages)
Savings scale with: instruction size × conversation length
```

> **Reference implementation:** The Cigar Band Identifier project (base implementation,
> preserved as-is) demonstrated ~74% token reduction in real usage. Benchmark script
> is planned but not yet built — exact API-verified numbers pending.

### Additional Problems JITCR Solves
- Claude Desktop compaction mid-session wipes all context →
  JITCR journals and handoffs preserve work across resets
- Starting new sessions means re-explaining everything →
  `> start` restores full context in one command
- No logging discipline across long coding/review sessions →
  Structured journal + handoff system captures decisions and state
- Manual per-project setup creates inconsistency →
  Universal command layer handles setup automatically

---

## Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      JITCR PROTOCOL LAYERS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 1 — PROJECT INSTRUCTIONS (Always-On / Compaction-Safe)   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • Project name — used for auto-folder creation          │   │
│  │ • OS declaration (Windows / macOS / Linux)              │   │
│  │ • Project root path                                     │   │
│  │ • Protocol guardrails (5 non-negotiable rules)          │   │
│  │ • Retrieval trigger: `> start`                          │   │
│  │ • Target: 200–300 tokens MAX                            │   │
│  │ • Lives in: Claude Desktop Project Instructions         │   │
│  │ • Survives: compaction, new sessions, restarts          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼ triggered by `> start`              │
│  TIER 2 — JITCR_[ProjectName].md (Loaded Once Per Session)     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • Full command reference (all > commands)               │   │
│  │ • Session workflow protocols                            │   │
│  │ • Templates: journal, handoff, commit                   │   │
│  │ • Project-specific paths and architecture               │   │
│  │ • Git configuration (if applicable)                     │   │
│  │ • Target: 600–1,500 tokens                              │   │
│  │ • Lives in: project root folder on host filesystem      │   │
│  │ • Loaded: Claude reads this file once at session start  │   │
│  │   via filesystem MCP — content stays in active context  │   │
│  │   memory for the session. File is never locked/modified │   │
│  │   by the load. User can edit manually at any time.      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼ conditional — see Tier 3 logic      │
│  TIER 3 — SESSION CONTEXT (On-Demand / Conditional)            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • Latest handoff_*.md — ALWAYS loaded at > start        │   │
│  │ • Last 3 journal_*.md — ONLY if handoff shows           │   │
│  │   BLOCKED status or open/unresolved issues              │   │
│  │ • Relevant code files — on explicit request only        │   │
│  │ • Git log (last 5 commits) — if git active              │   │
│  │ • Variable size — loaded selectively to save tokens     │   │
│  │ • Lives in: Sessions\{ProjectName}\logs\                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Tier 3 Conditional Loading Logic
```
> start always:      read latest handoff_*.md
> start conditional: IF handoff status = BLOCKED
                     OR handoff contains open/unresolved issues
                       THEN also read last 3 journal_*.md
                     ELSE skip journals — save tokens
```
This keeps Tier 3 truly just-in-time. Most sessions only pay for the handoff.

---

## Protocol Guardrails (Tier 1 — Non-Negotiable Rules)

These five rules must appear in every Tier 1 Project Instructions, for every project,
on every OS. They are the safety floor of the protocol:

1. Never delete files without explicit user permission
2. Never modify `.env` files without explicit user permission
3. Read existing files before overwriting — preserve content
4. Shell commands: always use forward slashes in paths
5. On `> start`: read `JITCR_[ProjectName].md` from project root

Everything else in Tier 1 is project-specific and customizable.
These five are not.

---

## File Naming Convention

### Tier 2 File
**Format:** `JITCR_[ProjectName].md`
**Examples:**
- `JITCR_CigarBandIdentifier.md`
- `JITCR_CDOpt.md`
- `JITCR_MyPythonApp.md`

**Why this naming:**
- Uppercase `JITCR_` prefix signals "protocol file — do not delete"
- Project name in filename makes purpose immediately clear when browsing filesystem
- User can and should edit this file manually as the project evolves
- Replaces the generic `CLAUDE_GUIDELINES.md` name used in v1.x (Cigar base)

### Session Log Files
**Format:** `{type}_YYYY-MM-DD_HHMM.md` (always lowercase type prefix)
**Examples:**
- `handoff_2026-03-06_1430.md`
- `journal_2026-03-06_0900.md`

---

## Universal Architecture (New — Designed This Session)

### Problem With v1.x (Cigar Project Base)
JITCR v1.x lives inside the Cigar Band Identifier project only. Every new project
requires manual setup. Session logs scatter across project folders. No consistent
hub. Commands must be re-created per project.

### Solution: Universal Command Layer + Per-Project Logs Hub

```
C:\Users\{name}\Documents\Claude_Desktop\          ← Windows
~/Documents/Claude_Desktop/                        ← macOS / Linux
│
├── JITCR_Universal_Commands.md    ← Shared command logic for ALL projects
│
├── JITCR Protocol\                ← Protocol documentation & specs
│   ├── HANDOFF-JITCR-Universal-v2.0-Design-2026-03-06.md  ← This file
│   ├── JITCR_Framework02202026b.md  (v1.3 base — preserved)
│   ├── benchmark\
│   │   └── jitcr_benchmark.py     ← Planned, not yet built
│   └── logs\
│
└── Sessions\                      ← Universal sessions hub
    ├── CigarBandIdentifier\       ← Auto-created on first > start
    │   └── logs\
    │       ├── journal_YYYY-MM-DD_HHMM.md
    │       └── handoff_YYYY-MM-DD_HHMM.md
    ├── CD_Opt\
    │   └── logs\
    ├── GeneralChats\              ← Fallback: no project name defined
    │   └── logs\
    └── {NewProject}\             ← Auto-created per project name in Tier 1
        └── logs\
```

Each project's `JITCR_[ProjectName].md` lives in the **project's own root folder**,
not in Sessions\. Sessions\ is only for logs (journals and handoffs).

---

## `> start` Command — Full Universal Protocol

```
STEP 1: OS Detection (silent, one-time)
  Windows → $env:OS returns "Windows_NT" → PowerShell syntax
  macOS   → uname returns "Darwin"        → bash syntax
  Linux   → uname returns "Linux"         → bash syntax
  Sets path separator and shell commands for entire session.

STEP 2: Project Folder Check
  Read project name from Tier 1.
  IF Sessions\{ProjectName}\ does not exist → create it + logs\ subfolder
  IF no project name defined in Tier 1     → route to Sessions\GeneralChats\

STEP 3: Git Status Check
  Run: git -C "{project_root}" status
  Result A — Active repo:    git commands enabled for session
  Result B — No repo found:  prompt user: "No git repo found. Initialize? (yes/no)"
             If yes → git init + git config (name + email)
  Result C — Repo, no remote: note it silently, local commits only

STEP 4: Load Tier 2
  Read JITCR_[ProjectName].md from project root via filesystem MCP.
  Confirm loaded. Display approximate token count.

STEP 5: Load Tier 3 (Conditional)
  Always: read latest handoff_*.md from Sessions\{ProjectName}\logs\
  Conditional: IF handoff status = BLOCKED or contains open issues
                 THEN read last 3 journal_*.md from same logs\ folder
  If git active: run git log -5 --oneline

STEP 6: Display Session Header
  Project name | OS detected | Timestamp
  Git: active / inactive / no-repo
  Files loaded: Tier 2 confirmed, Tier 3 files listed
  Available commands: quick reference
```

---

## Cross-Platform Compatibility

JITCR runs natively on all three OS. No containers, no Docker, no additional installs.

| Element | Windows | macOS | Linux |
|---|---|---|---|
| Sessions hub | `C:\Users\{name}\Documents\Claude_Desktop\Sessions\` | `~/Documents/Claude_Desktop/Sessions/` | `~/Documents/Claude_Desktop/Sessions/` |
| Shell | PowerShell | bash/zsh | bash |
| Filesystem MCP paths | Backslash `\` | Forward slash `/` | Forward slash `/` |
| Shell-command MCP paths | Forward slash `/` | Forward slash `/` | Forward slash `/` |
| Git commands | Identical | Identical | Identical |
| OS detection | `$env:OS` = Windows_NT | `uname` = Darwin | `uname` = Linux |

**User action required per project:** Declare OS and project root in Tier 1 once.
**Everything else:** Auto-detected and self-configuring at `> start`.

---

## Execution Environment — Critical Distinction

Claude Desktop contains two separate execution environments. JITCR must always
stay in Environment 1:

| | Environment 1: MCP Layer | Environment 2: Claude Code VM |
|---|---|---|
| What it is | filesystem + shell-command MCPs running as Node.js processes | Sandboxed Linux VM (claudevm.bundle) |
| Path style | Host OS native paths | Linux paths (/home/, /mnt/) |
| Files visible on host | ✅ Yes — immediately | ❌ No — trapped in VM |
| JITCR uses this | ✅ YES — always | ❌ NEVER |

**Warning sign:** If a response shows Linux-style paths (`/home/`, `/mnt/`) and you
are on Windows or macOS — the operation went into the Claude Code VM. Files written
there are not visible on your filesystem.

---

## Universal Command Reference

| Command | Action | Git Required? |
|---|---|---|
| `> start` | Detect OS, create folders, check git, load Tier 2 + Tier 3 | No |
| `> journal` | Write session journal entry to logs\ | No |
| `> handoff` | Create handoff snapshot for next session | No |
| `> save` | Runs `> journal` + `> handoff` | No |
| `> status` | Show git status, last journal, last handoff | Optional |
| `> commit` | Git commit with formatted message | YES |
| `> end` | Runs `> save` + optional `> commit` + session summary | Optional |
| `> backup` | Zip/copy project folder to backup location | No |

Git commands (`> commit`, `> end` with commit) silently skip if no git repo.
No errors, no noise — just skipped.

---

## Preserving the Base Implementation

**The Cigar Band Identifier project is the origin implementation and must not be changed.**

- All v1.x files stay exactly as-is under the Cigar project folder
- `CLAUDE_GUIDELINES.md` naming stays in that project (not renamed)
- That project serves as the before/after reference for benchmarking
- All universal v2.0 development happens in a new dedicated POC project

**POC project for v2.0 implementation:**
To be created as a separate Claude Desktop project.
Name suggestion: `JITCR-Protocol-POC`
Purpose: Build and test the universal architecture without touching the Cigar baseline.

---

## Publication Strategy

### Recommended Path: GitHub → Article → Community

**Stage 1 — GitHub Repository (foundation)**
Suggested repo name: `jitcr-protocol`

```
jitcr-protocol/
├── README.md                        ← What, why, 5-min quickstart
├── PROTOCOL_SPEC.md                 ← Formal v2.0 specification
├── templates/
│   ├── TIER1_template.md            ← Copy-paste Tier 1 starter
│   ├── JITCR_ProjectName_template.md ← Tier 2 template
│   └── JITCR_Universal_Commands.md  ← Universal commands file
├── examples/
│   ├── python-project/
│   ├── nodejs-project/
│   └── general-chat/
├── benchmark/
│   └── jitcr_benchmark.py           ← Verified token counts
└── CHANGELOG.md
```

**Stage 2 — Written Article (amplifier)**
Platform: Medium or Dev.to
Suggested title: *"How I Cut Claude Desktop Token Usage by ~74% With a Simple
Three-Tier Protocol"*
Lead with the problem → show before/after → link to GitHub repo.

**Stage 3 — Community Distribution**
- Anthropic Discord `#claude-desktop` channel
- Reddit r/ClaudeAI
- Reddit r/LocalLLaMA (broader AI audience)

**Pre-publication requirement:**
Do not publish until the benchmark script produces API-verified token counts.
Estimated numbers are not credible for publication. The benchmark is the
difference between an anecdote and a proof.

---

## Pending Feature: Dynamic MCP Loading

**Flagged for future discussion — not designed yet.**

Concept: Instead of all MCPs loading at Claude Desktop startup (always-on,
always consuming memory), load/unload them dynamically based on project context.

Known constraints from prior sessions:
- MCPs are Node.js processes spawned at CD startup
- Cannot be lazy-loaded mid-session in current CD architecture
- JITCR principles could apply to what MCPs *return* (response data)
  rather than MCP process lifecycle — this is the more viable direction

**Status:** Design discussion pending. Do not implement until fully scoped.

---

## Key Design Decisions Made This Session

| Decision | Rationale |
|---|---|
| JITCR = Protocol | Implies defined contract, predictable behavior, not just a suggestion |
| Universal via shared command file | Skills don't persist through compaction — wrong mechanism |
| OS detection in `> start` | No new dependencies, native execution on all three OS |
| No Docker | JITCR is a protocol not an app — nothing to containerize; would trap files in container |
| Auto-folder creation by project name | Zero manual setup per project after first `> start` |
| Git check + optional init in `> start` | Automation without assumption — never break on missing repo |
| Conditional Tier 3 loading | True JIT — only load journals when handoff shows unresolved state |
| GeneralChats fallback folder | JITCR works even with no project defined — universal by default |
| `JITCR_[ProjectName].md` naming | Protocol-branded, self-describing, safe from accidental deletion |
| Cigar project preserved as-is | Origin baseline for benchmarking — do not touch |
| New POC project for v2.0 | Clean implementation without risk to working baseline |
| GitHub as publication vehicle | Version-controlled, forkable, discoverable, permanent |

---

## Next Session Should

1. **Confirm this handoff** — any corrections or additions before building
2. **Create the POC project** in Claude Desktop named `JITCR-Protocol-POC`
3. **Implement in this order:**
   a. Create `Sessions\` hub folder structure
   b. Create `JITCR_Universal_Commands.md` with all universal commands
   c. Build Tier 1 template with OS + project name + 5 guardrail rules
   d. Build `> start` with OS detection + git check + conditional Tier 3
   e. Test on a simple general chat first (GeneralChats fallback path)
   f. Test on a real project (CD_Opt recommended — not Cigar)
4. **Build benchmark script** — highest priority for publication credibility
5. **Discuss Dynamic MCP Loading** — separate session after POC validated

---

## Session Reference
- Earlier draft: `JITCR Universal Architecture — Session Handoff_03062026a.md`
- Base implementation (preserved): Cigar Band Identifier project, `CLAUDE_GUIDELINES.md` v1.3
- This handoff represents: **JITCR Protocol v2.0 Universal Architecture Design**
