# JITCR Universal Commands
**Protocol Version:** 2.5
**Author:** LaserWhiz
**Created:** 2026-03-06
**Last Enhanced:** 2026-06-25
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

## File Access Protocol — MCP Tool Selection (CRITICAL)

⚠️ **CRITICAL**: Claude has multiple file-access tools. Using the WRONG tool will fail silently.
   This section ensures correct tool selection on every OS, every session.

### Tool Capability Matrix

| Tool | OS Support | Purpose | Path Format | Activation | Use Case |
|---|---|---|---|---|---|
| `view` | Linux only | Read container mounts | `/mnt/...` | Always active | NOT for project work |
| `bash_tool` | Linux container | Run commands in VM | forward slashes | Always active | NOT for project work |
| **`filesystem:*`** | **Windows + macOS + Linux** | **Read/write native host files** | **Native OS paths** | **LOAD via tool_search** | ✅ **Project file R/W** |
| **`shell-command`** | **Windows + macOS + Linux** | **Run native OS commands** | **Forward slashes** | **LOAD via tool_search** | ✅ **Project commands** |

**KEY INSIGHT:**
- `view` and `bash_tool` run in Claude's Linux container environment
- `filesystem` and `shell-command` MCPs run on YOUR actual OS (Windows/macOS/Linux)
- Files written to `/mnt/` paths are NOT visible on your disk
- **ALWAYS use filesystem/shell-command MCPs for project work**

### Path Syntax Rules by OS

#### **IF Project OS = Windows**

**MCP Tools to Use:**
- Read files → `filesystem:read_text_file(path)`
- Write files → `filesystem:write_file(path, content)`
- List dirs → `filesystem:list_directory(path)`
- Run commands → `shell-command:execute_command(command)`

**Path Format Rules:**
| Operation | Format | Example |
|---|---|---|
| filesystem:read_text_file | Native backslash | `C:\Users\LaserMaster\Documents\file.md` |
| filesystem:write_file | Native backslash | `C:\project\output.txt` |
| filesystem:list_directory | Native backslash | `C:\project\logs` |
| shell-command | Forward slashes ALWAYS | `dir C:/Users/LaserMaster/Documents` |
| Git commands | Forward slashes ALWAYS | `git -C "C:/project" status` |

**If you accidentally use Linux paths:**
- ❌ `filesystem:read_text_file("/mnt/c/Users/...")` → FAIL
- ❌ `view("/mnt/c/Users/...")` → FAIL (reads container, not disk)
- ✅ `filesystem:read_text_file("C:\Users\...")` → SUCCESS

#### **IF Project OS = macOS**

**MCP Tools to Use:**
- Read files → `filesystem:read_text_file(path)`
- Write files → `filesystem:write_file(path, content)`
- List dirs → `filesystem:list_directory(path)`
- Run commands → `shell-command:execute_command(command)`

**Path Format Rules:**
| Operation | Format | Example |
|---|---|---|
| filesystem:read_text_file | Forward slash | `/Users/LaserMaster/Documents/file.md` |
| filesystem:write_file | Forward slash | `/Users/user/project/output.txt` |
| filesystem:list_directory | Forward slash | `/Users/user/project/logs` |
| shell-command | Forward slash | `ls /Users/LaserMaster/Documents` |
| Git commands | Forward slash | `git -C "/Users/user/project" status` |

#### **IF Project OS = Linux**

**MCP Tools to Use:**
- Read files → `filesystem:read_text_file(path)`
- Write files → `filesystem:write_file(path, content)`
- List dirs → `filesystem:list_directory(path)`
- Run commands → `shell-command:execute_command(command)`

**Path Format Rules:**
| Operation | Format | Example |
|---|---|---|
| filesystem:read_text_file | Forward slash | `/home/user/Documents/file.md` |
| filesystem:write_file | Forward slash | `/home/user/project/output.txt` |
| filesystem:list_directory | Forward slash | `/home/user/project/logs` |
| shell-command | Forward slash | `ls /home/user/Documents` |
| Git commands | Forward slash | `git -C "/home/user/project" status` |

### Decision Tree: Which Tool to Use

```
You need to READ a file on Windows/macOS/Linux?
  └─ Use: filesystem:read_text_file(native_path)
     Load first via: tool_search("filesystem")
     Path format: Determined by project OS (see above)
     Example (Windows): filesystem:read_text_file("C:\project\file.md")
     Example (macOS): filesystem:read_text_file("/Users/user/project/file.md")

You need to WRITE/CREATE a file?
  └─ Use: filesystem:write_file(native_path, content)
     Load first via: tool_search("filesystem")
     Path format: Determined by project OS

You need to RUN a command (git, dir, ls, etc.)?
  └─ Use: shell-command:execute_command(command)
     Load first via: tool_search("shell command")
     Path format: Forward slashes ALWAYS, regardless of OS
     Example (Windows): shell-command("dir C:/Users/...")
     Example (macOS): shell-command("git -C '/Users/user/project' status")

Do TEMPORARY work in Claude's Linux container (NOT recommended)?
  └─ Use: view() or bash_tool()
     ⚠️ Files NOT visible on your disk
     Use ONLY for temporary, non-project work
```

### Troubleshooting: File Access Errors

**Error: "Path not found" or "No such file or directory"**

Checklist:
1. ☐ Did you load MCP tools via `tool_search("filesystem")`?
   - If no → load now, then retry
2. ☐ Are you using the CORRECT tool?
   - File read? → use `filesystem:read_text_file`
   - Command run? → use `shell-command:execute_command`
   - Using container tools? → That's the problem
3. ☐ Is the path format correct for YOUR project OS?
   - Windows? → Backslash for filesystem:*, forward slash for shell-command
   - macOS/Linux? → Forward slashes for both
4. ☐ Does the file actually exist?
   - Run: `filesystem:list_directory("parent_folder")` to verify

**Error: "File was created but I can't see it on my disk"**

Diagnosis: You used `view()` or `bash_tool()` instead of filesystem MCPs.
- **Solution:** Use `filesystem:write_file()` with proper MCP loading

---

## Session Logs Location

Session logs (journals + handoffs) for every project are stored under:
`JITCR_Protocol\{ProjectName}\logs\`

`JITCR_Protocol\` is the fixed root folder created during install. Every project
gets its own subfolder inside it, with `logs\` for journals and handoffs.

Every project has its own `logs\` subfolder directly inside its project folder:
```
JITCR_Protocol\
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
```

---

## `> start` — Initialize Session

```
STEP 0: Load MCP Tools (NEW — CRITICAL)
        Before any file operations:
        A. tool_search("filesystem read file windows")
           → Loads: filesystem:read_text_file, filesystem:write_file, 
                    filesystem:list_directory, etc.
           → Confirm: "Filesystem MCPs loaded"
        B. tool_search("shell command execute")
           → Loads: shell-command:execute_command
           → Confirm: "Shell-command MCP loaded"
        C. These enable native file access on your OS
           (NOT in Claude's Linux container)

STEP 1: OS Detection (silent)
        Windows → [System.Environment]::OSVersion.Platform = "Win32NT"
                → {runtime_os} = Windows
                → {path_sep} = "\"
                → {shell} = PowerShell
        macOS   → uname = "Darwin"
                → {runtime_os} = macOS
                → {path_sep} = "/"
                → {shell} = bash
        Linux   → uname = "Linux"
                → {runtime_os} = Linux
                → {path_sep} = "/"
                → {shell} = bash

STEP 1b: Compare Runtime OS vs Project OS (NEW)
         Read "OS" field from Tier 2 if present
         IF {runtime_os} ≠ {project_os}:
           ⚠️  WARN: "Runtime OS differs from Project OS.
                      File paths may behave differently."
         ELSE:
           Silent confirmation: "OS detected: {runtime_os}"

STEP 2: Read project name from Tier 1 Project Instructions
        Logs path: JITCR_Protocol\{ProjectName}\logs\

STEP 3: Check and create logs folder if missing
        IF JITCR_Protocol\{ProjectName}\logs\ does not exist
          → create JITCR_Protocol\{ProjectName}\
          → create JITCR_Protocol\{ProjectName}\logs\
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

STEP 5: Load GitHub config from Tier 2
        Read {GitHub Remote} and {GitHub Push} fields from Tier 2 guide
        IF {GitHub Push} = yes AND {GitHub Remote} is set and not "none"
          → store as session variables: {github_remote}, {push_enabled} = true
          → confirm silently: GitHub push enabled for this session
        IF {GitHub Push} = no OR {GitHub Remote} is blank or "none"
          → store: {push_enabled} = false
          → GitHub push will never be prompted this session

STEP 6: Load Tier 2
        Read JITCR_[ProjectName].md from project root via filesystem MCP
        Confirm loaded. Display approximate token count.

STEP 7: Load Tier 3 — Conditional
        ALWAYS   → read latest handoff_*.md from JITCR_Protocol\{ProjectName}\logs\
                   (if no handoff exists → note "First session for this project")
        ONLY IF  → handoff status = BLOCKED
                   OR handoff contains open/unresolved issues
                 → also read last 3 journal_*.md from same logs\ folder
        IF git active → run: git log -5 --oneline

STEP 8: Display session header
        ┌─────────────────────────────────────────┐
        │ Project  : {ProjectName}                │
        │ OS       : {runtime_os}                 │
        │ Started  : {YYYY-MM-DD HH:MM}           │
        │ Git      : {active | inactive | no repo}│
        │ GitHub   : {push enabled | local only}  │
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
   JITCR_Protocol\{ProjectName}\logs\journal_YYYY-MM-DD_HHMM.md
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
   JITCR_Protocol\{ProjectName}\logs\handoff_YYYY-MM-DD_HHMM.md
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

## `> commit` — Git Commit (Local Only)

```
PURPOSE: Mid-session checkpoint — commits project root content to local git.
         What gets committed is controlled by {project_root}/.gitignore.
         Session logs (logs\) are never committed if excluded by .gitignore.
         This is a LOCAL commit only — nothing is pushed to GitHub.
         Push to GitHub only happens at > end, if configured.

IF no git repo active → skip silently
                        note: "Git not active for this project — skipped"
IF git active:
  1. git -C "{project_root}" add -A
  2. git -C "{project_root}" commit -m "{message}"
  3. Confirm: "Committed locally → {hash} : {message}"
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
PURPOSE: Saves session logs, always commits locally, then asks about
         GitHub push only if the project was configured for it at setup.

1. Run > save
   Confirm: "Journal + handoff written."

2. Local commit — always, no prompt:
   IF git active:
     Run: git -C "{project_root}" add -A
     Run: git -C "{project_root}" commit -m "Session end — {YYYY-MM-DD HH:MM}"
     Confirm: "Local commit done → {hash}"
   IF git not active:
     Note: "Git not active — local commit skipped."

3. GitHub push — only if configured:
   IF {push_enabled} = true:
     Prompt: "Push to GitHub now? (yes/no)"
     If yes → git -C "{project_root}" push {github_remote}
              Confirm: "Pushed to GitHub → {github_remote}"
     If no  → Confirm: "Changes committed locally. Push skipped for this session."
   IF {push_enabled} = false:
     No prompt — silent. Local commit is the final step.

4. Display session summary:
   ┌─────────────────────────────────────────┐
   │ Session Ended  : {YYYY-MM-DD HH:MM}     │
   │ Journal        : {filename}             │
   │ Handoff        : {filename}             │
   │ Local commit   : {hash | skipped}       │
   │ GitHub push    : {pushed | skipped |    │
   │                   not configured}       │
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
| Tier 2 guide | `JITCR_[ProjectName].md` | `JITCR_Protocol\{ProjectName}\` |
| Journal | `journal_YYYY-MM-DD_HHMM.md` | `JITCR_Protocol\{ProjectName}\logs\` |
| Handoff | `handoff_YYYY-MM-DD_HHMM.md` | `JITCR_Protocol\{ProjectName}\logs\` |
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
│  > commit   Commit project files to local git       │
│  > end      save + commit locally + optional push   │
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
   JITCR_Protocol\{ProjectName}\logs\qa_YYYY-MM-DD_HHMM.md
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
| 2.3 | 2026-03-13 | Removed Sessions\ folder — logs now live in JITCR_Protocol\{ProjectName}\logs\; all path references now use literal JITCR_Protocol\ root |
| 2.4 | 2026-03-16 | GitHub push guardrail: > end always commits locally (no prompt); push to GitHub only if configured at setup and confirmed at > end; > commit clarified as local-only; > start loads GitHub config from Tier 2; session header shows GitHub status |
| **2.5** | **2026-06-25** | **NEW: Added File Access Protocol section — explicit OS detection + MCP tool loading + OS-specific path rules. Added STEP 0 to > start for MCP tool loading. Added OS field comparison (runtime vs project). Multi-OS support enhanced for Windows/macOS/Linux users.** |
