# JITCR Universal Commands
**Protocol Version:** 2.0
**Author:** LaserWhiz
**Created:** 2026-03-06
**Purpose:** Shared command engine for all JITCR Protocol implementations.
           This file is referenced by every project's JITCR_[ProjectName].md.

> ⚠️ Do NOT delete this file.
> Edit ONLY when upgrading the JITCR Protocol itself.
> Individual projects are customized in their own JITCR_[ProjectName].md file.

---

## Protocol Guardrails (Non-Negotiable — All Projects)

These five rules apply to every project, every OS, every session:

1. Never delete files without explicit user permission
2. Never modify .env files without explicit user permission
3. Read existing files before overwriting — preserve content
4. Shell commands: always use forward slashes in paths
5. On `> start`: read JITCR_[ProjectName].md from project root

---

## OS Detection (Runs Silently at `> start`)

```
Windows → PowerShell: [System.Environment]::OSVersion.Platform returns "Win32NT"
macOS   → bash: uname returns "Darwin"
Linux   → bash: uname returns "Linux"
```

> ⚠️ Do NOT use $env:OS or $IsWindows for detection — both return blank/unreliable
>    results when invoked via shell-command MCP.
>    [System.Environment]::OSVersion.Platform is the confirmed reliable method.

Sets path separator and shell syntax for the entire session.
All subsequent path and shell operations use the detected OS context.

---

## Session Logs Location

Session logs (journals + handoffs) for every project are stored under:
`{HubRoot}\{ProjectName}\logs\`

The `{HubRoot}` path is defined by the user during install and stored in the
project's Tier 2 file (`JITCR_{ProjectName}.md`) under the Session Logs field.

Every project has its own `logs\` subfolder directly inside its project folder:
```
{HubRoot}\
├── JITCR_Universal_Commands.md        ← this file
├── {ProjectName-A}\
│   ├── JITCR_{ProjectName-A}.md          ← Tier 2 guide
│   └── logs\                             ← journals and handoffs
├── {ProjectName-B}\
│   ├── JITCR_{ProjectName-B}.md
│   └── logs\
└── {ProjectName-Z}\
    ├── JITCR_{ProjectName-Z}.md
    └── logs\

---

## `> start` — Initialize Session

```
STEP 1: OS Detection (silent)
        Windows → [System.Environment]::OSVersion.Platform = "Win32NT" → PowerShell syntax
        macOS   → uname = "Darwin"       → bash syntax
        Linux   → uname = "Linux"        → bash syntax

STEP 2: Read project name and {HubRoot} from Tier 1 Project Instructions
        Logs path: {HubRoot}\{ProjectName}\logs\

STEP 3: Check and create logs folder if missing
        IF {HubRoot}\{ProjectName}\logs\ does not exist
          → create {HubRoot}\{ProjectName}\
          → create {HubRoot}\{ProjectName}\logs\
          → confirm: "Created logs folder for {ProjectName}"

STEP 4: Git status check
        Run: git -C "{project_root}" status
        Result A — repo active     → git commands enabled for session
        Result B — no repo found   → prompt: "No git repo found.
                                     Initialize git here? (yes/no)"
                   If yes          → git init "{project_root}"
                                  → git config user.name + user.email
                   If no           → git commands disabled, no errors
        Result C — repo, no remote → note silently, local commits only

STEP 5: Load Tier 2
        Read JITCR_[ProjectName].md from project root via filesystem MCP
        Confirm loaded. Display approximate token count.

STEP 6: Load Tier 3 — Conditional
        ALWAYS   → read latest handoff_*.md from {HubRoot}\{ProjectName}\logs\
                   (if no handoff exists → note "First session for this project")
        ONLY IF  → handoff status = BLOCKED
                   OR handoff contains open/unresolved issues
                 → also read last 3 journal_*.md from same logs\ folder
        IF git active → run: git log -5 --oneline

STEP 7: Display session header
        ┌─────────────────────────────────────────┐
        │ Project  : {ProjectName}                │
        │ OS       : {detected OS}                │
        │ Started  : {YYYY-MM-DD HH:MM}           │
        │ Git      : {active | inactive | no repo}│
        │ Loaded   : Tier 2 + {Tier 3 files}      │
        │ Commands : > journal, save, handoff,    │
        │            status, commit, end, backup  │
        └─────────────────────────────────────────┘
```

---

## `> journal` — Write Session Journal Entry

```
1. Get current timestamp (YYYY-MM-DD HH:MM)
2. Determine journal file path:
   {HubRoot}\{ProjectName}\logs\journal_YYYY-MM-DD_HHMM.md
3. If file does not exist → create it with header
4. Append entry using template below
5. Confirm: "Journal updated → journal_YYYY-MM-DD_HHMM.md"
```

**Journal Entry Template:**
```markdown
---
## YYYY-MM-DD HH:MM | Session: [brief title]
**Status**: [IN PROGRESS | COMPLETED | BLOCKED]

### Completed
- [what was accomplished]

### Decisions
- [decision made]: [reasoning]

### Next Steps
- [ ] [item]

### Files Modified
- `path/to/file`: [what changed]
---
```

---

## `> handoff` — Create Session Handoff

```
1. Get current timestamp (YYYY-MM-DD HH:MM)
2. Create file:
   {HubRoot}\{ProjectName}\logs\handoff_YYYY-MM-DD_HHMM.md
3. Write handoff using template below
4. Confirm: "Handoff saved → handoff_YYYY-MM-DD_HHMM.md"
```

**Handoff Template:**
```markdown
# Session Handoff — YYYY-MM-DD HH:MM

## Project Status
[One paragraph summary of current state]

## Completed This Session
- [item]

## Current File States
| File | Status | Notes |
|------|--------|-------|
| | | |

## Open Issues
- [issue]: [details]

## Next Session Should
1. [priority 1]
2. [priority 2]
```

---

## `> save` — Quick Save

```
1. Run > journal
2. Run > handoff
3. Confirm: "Session saved — journal + handoff written."
```

---

## `> status` — Show Current State

```
1. Find and display last handoff filename + its status line
2. Find and display last journal filename + its status line
3. IF git active → run: git status --short
4. Display summary block
```

---

## `> commit` — Git Commit

```
IF no git repo active → skip silently
                        note: "Git not active for this project — skipped"
IF git active:
  1. git -C "{project_root}" add -A
  2. git -C "{project_root}" commit -m "{message}"
  3. Confirm: "Committed → {hash} : {message}"
```

**Commit Message Template:**
```
[version or date]: [short description]

- [file]: [what changed]
- Decision: [if applicable]
- Next: [what follows]
```

---

## `> end` — End Session

```
1. Run > save
2. IF git active → prompt: "Commit changes before ending? (yes/no)"
   If yes        → run > commit
3. Display session summary:
   ┌─────────────────────────────────────────┐
   │ Session Ended  : {YYYY-MM-DD HH:MM}     │
   │ Journal        : {filename}             │
   │ Handoff        : {filename}             │
   │ Git            : {committed | skipped}  │
   │ Next session   : {top priority from     │
   │                   handoff}              │
   └─────────────────────────────────────────┘
```

---

## `> backup` — Backup Project Folder

```
Windows:
  Compress-Archive -Path "{project_root}"
  -DestinationPath "{project_root}_backup_YYYY-MM-DD_HHMM.zip"

macOS / Linux:
  zip -r "{project_root}_backup_YYYY-MM-DD_HHMM.zip" "{project_root}"

Confirm: "Backup created → {project_root}_backup_YYYY-MM-DD_HHMM.zip"
```

---

## File Naming Conventions

| File Type | Format | Location |
|---|---|---|
| Tier 2 guide | `JITCR_[ProjectName].md` | `{HubRoot}\{ProjectName}\` |
| Journal | `journal_YYYY-MM-DD_HHMM.md` | `{HubRoot}\{ProjectName}\logs\` |
| Handoff | `handoff_YYYY-MM-DD_HHMM.md` | `{HubRoot}\{ProjectName}\logs\` |
| Backup | `{ProjectName}_backup_YYYY-MM-DD_HHMM.zip` | Project root or designated backup path |

> All type prefixes are always **lowercase**: `journal_`, `handoff_`

---

## Execution Environment Rules

- ALL JITCR file operations use filesystem MCP or shell-command MCP only
- filesystem MCP → accepts host OS native paths (backslash on Windows)
- shell-command MCP → always use forward slashes regardless of OS
- ⚠️ Warning sign: if Linux-style paths appear (`/home/`, `/mnt/`) on
  Windows or macOS — the operation is in the Claude Code VM, not MCP.
  Files written there are NOT visible on your filesystem.
- Never use Claude Code execution environment for any JITCR operations

---

## Tier 3 Conditional Loading Logic (Reference)

```
> start ALWAYS loads:
  → latest handoff_*.md

> start CONDITIONALLY loads:
  → IF handoff status = BLOCKED
    OR handoff contains open / unresolved issues
    THEN also load last 3 journal_*.md
    ELSE skip journals (save tokens)
```

This keeps Tier 3 truly just-in-time.
Most sessions only pay the token cost of the handoff file.

---

## `> ?` — Show Help

```
1. Display all available JITCR commands with one-line descriptions
2. Format as a clean command table
3. Add tip line at the bottom
```

**Output format:**
```
┌─────────────────────────────────────────────────────┐
│  JITCR Commands — {ProjectName}                     │
├─────────────────────────────────────────────────────┤
│  > start    Initialize session, load context        │
│  > journal  Write timestamped journal entry         │
│  > handoff  Create session handoff snapshot         │
│  > save     journal + handoff together              │
│  > status   Last handoff, journal, git status       │
│  > commit   Git commit all project files            │
│  > end      save + optional commit + summary        │
│  > backup   Zip project root to backup file         │
│  > ?        Show this help                          │
└─────────────────────────────────────────────────────┘
Tip: Commands accept natural extensions — e.g. > commit "my message"
     or > ? journal for details on a specific command.
```

---

## `> qa` — Run QA Test Suite

```
1. Read JITCR_QA.md from project root via filesystem MCP
2. Execute each test in sequence
3. Report PASS/FAIL per test inline as tests run
4. On completion, write results to:
   {HubRoot}\{ProjectName}\logs\qa_YYYY-MM-DD_HHMM.md
   using the QA Results Template in JITCR_QA.md
5. Display summary: X passed, Y failed, Z skipped

To run a single test:
  > qa QA-01   (replace QA-01 with any test ID)
```

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-03-06 | Initial universal commands file — JITCR Protocol v2.0 |
| 2.1 | 2026-03-07 | Added > qa command — QA test suite runner |
| 2.2 | 2026-03-07 | Fixed OS detection: $env:OS unreliable via shell-command MCP; use OSVersion.Platform |
| 2.3 | 2026-03-13 | Removed Sessions\ folder — logs now live inside each project subfolder; replaced hardcoded OS paths with {HubRoot} |
