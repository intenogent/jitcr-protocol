# Just-In-Time Context Retrieval (JITCR) Framework

> **Version:** 1.3  
> **Author:** LaserWhiz  
> **Created:** 2026-02-12  
> **Purpose:** Optimize LLM token usage by strategically layering context across always-on instructions and on-demand retrieval.

---

## Quick Start: New Project Setup (5 Minutes)

### Step 1: Copy Tier 1 Template to Claude Desktop Project Instructions

In Claude Desktop: **Project Settings → Project Instructions** → Paste this:

```markdown
## Role
[One sentence: what Claude does for this project]

## Core Rules
- Act by default, be concise
- Never delete files or modify .env without explicit permission
- Read files before overwriting to preserve content
- Shell commands (git, python): use FORWARD SLASHES in paths
- `>` prefix = execute command
- On `> start`, read CLAUDE_GUIDELINES.md from: [PROJECT_ROOT_PATH]

## Environment
[OS] | [IDE] | [Language] | [Package Manager] | [venv name if applicable]
```

**Edit the bracketed items**, then save. (~200-300 tokens)

### Step 2: Create CLAUDE_GUIDELINES.md in Your Project

```
{your_project}/
├── CLAUDE_GUIDELINES.md   ← Create this file
└── logs/                   ← Create this folder
```

Copy the **Tier 2 Template** from the "Step 3: Create Tier 2" section below into `CLAUDE_GUIDELINES.md`, then customize for your project.

### Step 3: Test It

1. Open new chat in Claude Desktop
2. Type: `> start`
3. Claude should read CLAUDE_GUIDELINES.md and display session info
4. If it works, you're done!

### Step 4: Iterate

As you work, update CLAUDE_GUIDELINES.md with project-specific commands, paths, and workflows. Claude can edit this file directly.

---

## The Problem

LLM conversations have a **context window limit**. Everything sent to the model counts against this limit:

```
System Prompt + Project Instructions + Conversation History + Your Message = Total Tokens
```

**Common mistake:** Stuffing all instructions into Project Instructions, which loads on EVERY message.

**Consequences:**

- Faster context window exhaustion
- Earlier "Compacting conversation" errors
- Higher API costs (tokens × messages)
- Reduced space for actual conversation

---

## The Solution: JITCR

**Core Principle:** Load minimal context always, full context on-demand.

```
┌─────────────────────────────────────────────────────────────────┐
│                        JITCR ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   TIER 1: CORE INSTRUCTIONS (Always Loaded)                    │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ • Identity & role (1-2 sentences)                       │  │
│   │ • Non-negotiable rules (3-5 max)                        │  │
│   │ • Environment basics (OS, language, tools)              │  │
│   │ • Retrieval trigger (how to load Tier 2)                │  │
│   │ • ~200-400 tokens                                       │  │
│   └─────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼ Triggered by `> start` or request  │
│   TIER 2: PROJECT GUIDELINES (Loaded Once per Session)         │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ • Full CLI command reference                            │  │
│   │ • Templates (journal, handoff, commit)                  │  │
│   │ • Workflow protocols                                    │  │
│   │ • Project-specific paths & architecture                 │  │
│   │ • ~1,000-2,000 tokens                                   │  │
│   │ • File: CLAUDE_GUIDELINES.md in project root            │  │
│   └─────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼ Triggered by `> start` or request  │
│   TIER 3: SESSION CONTEXT (Loaded as Needed)                   │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ • Latest handoff document                               │  │
│   │ • Recent journal entries                                │  │
│   │ • Relevant code files                                   │  │
│   │ • Variable size                                         │  │
│   │ • Files: logs/handoff_*.md, logs/journal_*.md           │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Token Economics

### Before JITCR (Everything in Project Instructions)

```
1,500 tokens × 20 messages = 30,000 tokens per conversation
```

### After JITCR (Tiered Loading)

```
Tier 1: 300 tokens × 20 messages     =  6,000 tokens
Tier 2: 1,200 tokens × 1 load        =  1,200 tokens
Tier 3: ~500 tokens × 1 load         =    500 tokens
                                      ─────────────────
Total:                                  7,700 tokens
Savings:                               22,300 tokens (74% reduction)
```

---

## Implementation Guide

### Step 1: Audit Current Instructions

Review your existing Project Instructions and categorize each item:

| Item | Frequency Needed | Tier |
|------|------------------|------|
| "Act by default, be concise" | Every message | 1 |
| "Use forward slashes in shell commands" | Every message | 1 |
| "Don't delete files without permission" | Every message | 1 |
| Full CLI command list | Once per session | 2 |
| Journal template format | When writing journal | 2 |
| Git commit format | When committing | 2 |
| Last session's handoff | Start of session | 3 |

### Step 2: Create Tier 1 (Project Instructions)

**Template:**

```markdown
## Role
[One sentence defining Claude's role for this project]

## Core Rules
- [Rule 1: Most critical behavior]
- [Rule 2: Safety/permission rule]
- [Rule 3: File handling rule]
- Shell commands: use FORWARD SLASHES in paths
- On `> start`, read CLAUDE_GUIDELINES.md from project root

## Environment
[OS] | [IDE] | [Language/Version] | [Package Manager] | [Key Tools]

## Command Prefix
`>` = execute command (full reference in CLAUDE_GUIDELINES.md)
```

**Guidelines for Tier 1:**

- Maximum 400 tokens (~300 words)
- Only include what's needed for EVERY message
- Must include the retrieval trigger for Tier 2
- No templates, no detailed workflows

### Step 3: Create Tier 2 (CLAUDE_GUIDELINES.md)

**Location:** `{project_root}/CLAUDE_GUIDELINES.md`

**Template:**

```markdown
# Project Guidelines - [Project Name]

> **Last Updated:** YYYY-MM-DD
> **Project Root:** [Full path]

## Quick Reference

| Command | Action |
|---------|--------|
| `> start` | Initialize session, load context |
| `> save` | Write journal + handoff |
| `> commit` | Git commit with formatted message |
| [Add all commands] | |

---

## CLI Commands - Full Reference

### Session Management
| Command | Action | Details |
|---------|--------|---------|
| `> start` | Initialize session | Creates journal, reads last handoff, shows status |
| `> save` | Quick save | Runs `> journal` + `> handoff` |
| `> end` | End session | Runs `> save` + `> commit` + summary |

### Memory Commands
| Command | Action | Details |
|---------|--------|---------|
| `> journal` | Update session log | Appends to current session's journal file |
| `> handoff` | Create handoff | Snapshot for next session |
| `> status` | Show status | Git status, last journal, last handoff |

### Development Commands
| Command | Action | Details |
|---------|--------|---------|
| `> test` | Run tests | Executes test suite |
| `> run [file]` | Execute file | Runs specified Python file |
| `> tree` | Show structure | Directory tree of project |

[Add all project-specific commands]
```

---

## Templates

### Journal Entry Format

```markdown
---
## YYYY-MM-DD HH:MM | Session: [title]
**Status**: [IN PROGRESS | COMPLETED | BLOCKED]

### Completed
- [Items]

### Decisions
- [Decision]: [Reasoning]

### Next Steps
- [ ] [Items]

### Files Modified
- `path`: [changes]
---
```

### Handoff Document Format

```markdown
# Session Handoff — YYYY-MM-DD HH:MM

## Project Status
[Summary paragraph]

## Completed This Session
- [Items]

## Current File States
| File | Status | Notes |
|------|--------|-------|

## Open Issues
- [Issue]: [Details]

## Next Session Should
1. [Priority 1]
2. [Priority 2]
```

### Git Commit Format

```
[version]: [Short description]

- [File]: [Change]
- Decision: [If any]
- Next: [What follows]
```

---

## Project-Specific Details

### Directory Structure

```
{project_root}/
├── CLAUDE_GUIDELINES.md    ← This file
├── logs/
│   ├── journal_*.md        ← Session journals
│   └── handoff_*.md        ← Session handoffs
├── src/                    ← Source code
├── tests/                  ← Test files
└── .env                    ← Environment variables (parent or root)
```

### Key Paths

- **Project Root:** [Full Windows path]
- **Virtual Environment:** [Name and location]
- **Shared .env:** [Path]

### Architecture Notes

[Project-specific architecture decisions and patterns]

---

## Workflows

### Session Start Protocol

1. Fetch system timestamp
2. Create `logs/journal_YYYY-MM-DD_HHMM.md`
3. Read last handoff from `logs/`
4. Read last 3 journals for context
5. Run `git log -5` for recent commits
6. Display session header with status

### Pre-Compaction Warning

At 15+ exchanges or heavy tool usage, suggest `> save` proactively.

### Logging Best Practice

Log everything in natural language under Completed, Decisions, or Open. Avoid tagging systems (e.g., [FIX], [ISSUE], [ENHANCEMENT]) - they add overhead without proportional value. Natural descriptions like "Fixed shell command path format" or "Blocked on API credentials" are sufficient and searchable.

---

## Environment-Specific Notes

### Shell Command Paths

- **Filesystem MCP:** Windows paths (`C:\Users\...`)
- **shell-command MCP:** Forward slashes (`C:/Users/...`)

### Git Operations

```bash
git -C "C:/path/to/project" status
git -C "C:/path/to/project" add -A
git -C "C:/path/to/project" commit -m "message"
```

### Step 4: Create Tier 3 Structure (Logs Directory)

```
{project_root}/
└── logs/
    ├── journal_2026-02-10_0930.md
    ├── journal_2026-02-11_1400.md
    ├── journal_2026-02-12_0900.md
    ├── handoff_2026-02-10_1200.md
    ├── handoff_2026-02-11_1730.md
    └── handoff_2026-02-12_1100.md
```

**Naming Convention:** `{type}_YYYY-MM-DD_HHMM.md`

- **Always lowercase:** `handoff_`, `journal_` (never `HANDOFF_` or `JOURNAL_`)
- Sortable by filename
- One file per session
- Never modify previous sessions' files

---

## Retrieval Protocol

### On `> start` Command

1. READ: `{project_root}/CLAUDE_GUIDELINES.md` (Tier 2)
2. READ: Latest `handoff_*.md` from `logs/` (Tier 3)
3. READ: Last 3 `journal_*.md` from `logs/` (Tier 3)
4. RUN: `git log -5 --oneline` (recent commits)
5. DISPLAY: Session header with loaded context summary

### On Specific Commands

| Trigger | Load |
|---------|------|
| `> journal` | Journal template from CLAUDE_GUIDELINES.md |
| `> handoff` | Handoff template from CLAUDE_GUIDELINES.md |
| `> commit` | Commit format from CLAUDE_GUIDELINES.md |
| Any template need | Re-read relevant section if forgotten |

---

## Adaptation Guide

### For Different Project Types

**Python Development Project:**

```markdown
## Environment
Windows 11 | Cursor | Python 3.12 | UV | venv: [name]
```

**Node.js Project:**

```markdown
## Environment
Windows 11 | VS Code | Node 20 | pnpm |
```

**n8n Workflow Project:**

```markdown
## Environment
Windows 11 | n8n Cloud | MCP: n8n-mcp
```

### Scaling for Team Use

If sharing CLAUDE_GUIDELINES.md across team:

1. Keep Tier 1 (Project Instructions) personal/account-specific
2. Make CLAUDE_GUIDELINES.md repo-standard
3. Add `.claude/` directory for team conventions
4. Document in README.md that project uses JITCR

---

## Troubleshooting

### "Claude forgot the commands"

Session likely compacted. Run `> start` to reload Tier 2 & 3.

### "Context compacting" appears frequently

- Audit Tier 1 - may still be too large
- Reduce conversation length before saving
- Use `> save` proactively

### "Claude uses wrong path format"

Tier 1 must include: `Shell commands: use FORWARD SLASHES in paths`

### "Guidelines file not found"

- Verify CLAUDE_GUIDELINES.md exists in project root
- Check filesystem MCP has access to project directory
- Confirm path in Tier 1 retrieval instruction

---

## Checklist for New Projects

- [ ] Create slim Tier 1 Project Instructions (<400 tokens)
- [ ] Include retrieval trigger for CLAUDE_GUIDELINES.md
- [ ] Include shell command path format rule
- [ ] Create CLAUDE_GUIDELINES.md in project root
- [ ] Include all CLI commands with descriptions
- [ ] Include all templates (journal, handoff, commit)
- [ ] Document project-specific paths
- [ ] Create `logs/` directory
- [ ] Test `> start` command loads all tiers correctly
- [ ] Verify git operations work with forward slashes

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.3 | 2026-02-20 | Fixed markdown formatting (templates escaped in code fences); added explicit lowercase naming rule for handoff/journal files; standardized all file references to lowercase |
| 1.2 | 2026-02-12 | Added Logging Best Practice (natural language over tags) |
| 1.1 | 2026-02-12 | Added Quick Start section for new projects |
| 1.0 | 2026-02-12 | Initial framework |

---

## Credits

Framework developed through iterative optimization of Claude Desktop workflows.

**Key Insight:** The "Compacting conversation" problem is often caused by bloated always-on context, not conversation length alone.

**Inspiration:** JIT (Just-In-Time) manufacturing and compilation principles applied to LLM context management.
