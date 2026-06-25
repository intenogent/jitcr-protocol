# JITCR Universal Commands
**Protocol Version:** 2.6
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

These six rules apply to every project, every OS, every session:

1. Never delete files without explicit user permission
2. Never modify .env files without explicit user permission
3. Read existing files before overwriting — preserve content
4. Shell commands: always use forward slashes in paths
5. On `> start`: read JITCR_[ProjectName].md from project root
6. **NEVER assume date/time — ALWAYS retrieve actual system time**

---

## System Date/Time Retrieval Protocol (MANDATORY — NEW in v2.6)

⚠️ **CRITICAL**: NEVER assume or hard-code timestamps. ALWAYS retrieve actual system date/time.
   This applies to ALL logging commands and file operations.

### When to Use System Time (All Cases)

**File names:**
- `journal_YYYY-MM-DD_HHMM.md` — must use ACTUAL system time (not assumed)
- `handoff_YYYY-MM-DD_HHMM.md` — must use ACTUAL system time (not assumed)
- `qa_YYYY-MM-DD_HHMM.md` — must use ACTUAL system time (not assumed)
- `{ProjectName}_backup_YYYY-MM-DD_HHMM.zip` — must use ACTUAL system time (not assumed)

**File content:**
- Journal headers: `## YYYY-MM-DD HH:MM | Session: [title]` — must use ACTUAL time
- Handoff headers: `# Session Handoff — YYYY-MM-DD HH:MM` — must use ACTUAL time
- QA result headers: `# QA Results — YYYY-MM-DD HH:MM` — must use ACTUAL time

**Commit messages:**
- Session end commits should include actual timestamp

### How to Retrieve System Date/Time by OS

#### **Windows**
```powershell
powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"
Output: 2026-06-25 1635
Meaning: June 25, 2026 at 4:35 PM (16:35)
```

#### **macOS**
```bash
date +"%Y-%m-%d %H%M"
Output: 2026-06-25 1635
Meaning: June 25, 2026 at 4:35 PM (16:35)
```

#### **Linux**
```bash
date +"%Y-%m-%d %H%M"
Output: 2026-06-25 1635
Meaning: June 25, 2026 at 4:35 PM (16:35)
```

### Implementation in Commands

**> start:**
```
STEP 1c: Retrieve System Time (NEW)
  Windows: shell-command("powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"")
  macOS/Linux: shell-command("date +"%Y-%m-%d %H%M"")
  Store as {session_time} = YYYY-MM-DD HHMM
  Use in session header: "Started : {session_time}"
```

**> journal:**
```
1. Retrieve actual system time (never assume)
2. Create filename with ACTUAL time: journal_YYYY-MM-DD_HHMM.md
3. Create header with ACTUAL time: ## YYYY-MM-DD HH:MM | Session: [title]
```

**> handoff:**
```
1. Retrieve actual system time (never assume)
2. Create filename with ACTUAL time: handoff_YYYY-MM-DD_HHMM.md
3. Create header with ACTUAL time: # Session Handoff — YYYY-MM-DD HH:MM
```

**> save:**
```
1. Retrieve actual system time ONCE (use for both journal + handoff)
2. Run > journal using retrieved time
3. Run > handoff using same retrieved time
```

**> end:**
```
1. Retrieve actual system time at session END
2. Run > save using END time
3. Final commit with actual END timestamp
```

### Validation Rules

✅ **ALWAYS:**
- Retrieve system time from shell-command BEFORE creating any log file
- Use retrieved time in both filename AND file content
- For > save: retrieve time once, use for both journal + handoff
- For > end: retrieve time at session END, not start

❌ **NEVER:**
- Assume time based on previous session or logic
- Hard-code timestamps
- Use approximate times
- Skip system time retrieval

---

## OS Detection (Runs Silently at `> start`)

```
Windows → PowerShell: [System.Environment]::OSVersion.Platform returns "Win32NT"
macOS   → bash: uname returns "Darwin"
Linux   → bash: uname returns "Linux"
```

---

## File Access Protocol — MCP Tool Selection (CRITICAL)

⚠️ **CRITICAL**: Claude has multiple file-access tools. Using the WRONG tool will fail silently.

### Tool Capability Matrix

| Tool | OS Support | Purpose | Activation | Use Case |
|---|---|---|---|---|
| `view` | Linux only | Read container mounts | Always active | NOT for project work |
| `bash_tool` | Linux container | Run commands in VM | Always active | NOT for project work |
| **`filesystem:*`** | **Windows + macOS + Linux** | **Read/write native host files** | **LOAD via tool_search** | ✅ **Project file R/W** |
| **`shell-command`** | **Windows + macOS + Linux** | **Run native OS commands** | **LOAD via tool_search** | ✅ **Project commands** |

**ALWAYS use filesystem/shell-command MCPs for project work**

---

## Session Logs Location

Session logs are stored under: `JITCR_Protocol\{ProjectName}\logs\`

---

## `> start` — Initialize Session

```
STEP 0: Load MCP Tools
        A. tool_search("filesystem read file windows")
        B. tool_search("shell command execute")

STEP 1: OS Detection

STEP 1c: Retrieve System Time (NEW in v2.6)
        Windows: shell-command("powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"")
        macOS/Linux: shell-command("date +"%Y-%m-%d %H%M"")
        Store {session_time} for use in headers

STEP 2-8: Continue with existing steps
```

---

## `> journal` — Write Session Journal Entry

```
1. Retrieve ACTUAL system time (not assumed):
   Windows: powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"
   macOS/Linux: date +"%Y-%m-%d %H%M"
2. Create filename: journal_YYYY-MM-DD_HHMM.md (using actual time)
3. Create header: ## YYYY-MM-DD HH:MM | Session: [title]
4. Confirm: "Journal updated → journal_YYYY-MM-DD_HHMM.md"
```

---

## `> handoff` — Create Session Handoff

```
1. Retrieve ACTUAL system time (not assumed):
   Windows: powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"
   macOS/Linux: date +"%Y-%m-%d %H%M"
2. Create filename: handoff_YYYY-MM-DD_HHMM.md (using actual time)
3. Create header: # Session Handoff — YYYY-MM-DD HH:MM
4. Confirm: "Handoff saved → handoff_YYYY-MM-DD_HHMM.md"
```

---

## `> save` — Quick Save

```
1. Retrieve ACTUAL system time ONCE:
   Windows: powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"
   macOS/Linux: date +"%Y-%m-%d %H%M"
2. Run > journal using retrieved time
3. Run > handoff using same retrieved time
4. Confirm: "Session saved — journal + handoff written (YYYY-MM-DD HH:MM)"
```

---

## `> status` — Show Current State

```
1. Find and display last handoff + status line
2. Find and display last journal + status line
3. IF git active → git status --short
4. Display summary
```

---

## `> commit` — Git Commit (Local Only)

```
1. (Optional) Retrieve actual system time for commit message
2. git -C "{project_root}" add -A
3. git -C "{project_root}" commit -m "{message}"
4. Confirm: "Committed locally → {hash} : {message}"
```

---

## `> end` — End Session

```
1. Retrieve ACTUAL system time at session END:
   Windows: powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"
   macOS/Linux: date +"%Y-%m-%d %H%M"
2. Run > save using END time
3. Local commit with actual END timestamp
4. GitHub push — only if configured
5. Display session summary with actual END timestamp
```

---

## `> backup` — Backup Project Folder

```
1. Retrieve actual system time:
   Windows: powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"
   macOS/Linux: date +"%Y-%m-%d %H%M"
2. Windows: Compress-Archive with timestamp YYYY-MM-DD_HHMM
3. macOS/Linux: zip with timestamp YYYY-MM-DD_HHMM
4. Confirm with actual timestamp in output
```

---

## File Naming Conventions

| File Type | Format | Location |
|---|---|---|
| Tier 2 guide | `JITCR_[ProjectName].md` | `JITCR_Protocol\{ProjectName}\` |
| Journal | `journal_YYYY-MM-DD_HHMM.md` | `JITCR_Protocol\{ProjectName}\logs\` |
| Handoff | `handoff_YYYY-MM-DD_HHMM.md` | `JITCR_Protocol\{ProjectName}\logs\` |
| QA Results | `qa_YYYY-MM-DD_HHMM.md` | `JITCR_Protocol\{ProjectName}\logs\` |
| Backup | `{ProjectName}_backup_YYYY-MM-DD_HHMM.zip` | Project root |

> All timestamps must be ACTUAL system time (not assumed)

---

## Execution Environment Rules

- ALL JITCR file operations use filesystem MCP or shell-command MCP only
- filesystem MCP → native OS paths (backslash on Windows)
- shell-command MCP → forward slashes regardless of OS
- **ALWAYS retrieve actual system time via shell-command before creating ANY log file**
- Never use Claude Code execution environment for JITCR operations

---

## `> ?` — Show Help

Display all available JITCR commands with one-line descriptions.

---

## `> qa` — Run QA Test Suite

```
1. Retrieve actual system time
2. Read JITCR_QA.md from project root
3. Execute each test in sequence
4. Write results to: qa_YYYY-MM-DD_HHMM.md (with actual time)
5. Display summary: X passed, Y failed, Z skipped
```

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-03-06 | Initial universal commands file |
| 2.1 | 2026-03-07 | Added > qa command |
| 2.2 | 2026-03-07 | Fixed OS detection |
| 2.3 | 2026-03-13 | Removed Sessions\ folder |
| 2.4 | 2026-03-16 | GitHub push guardrail |
| 2.5 | 2026-06-25 | Added File Access Protocol |
| **2.6** | **2026-06-25** | **NEW: System Date/Time Retrieval Protocol (MANDATORY). NEVER assume timestamps — ALWAYS retrieve actual system time. Added Guardrail #6. System time retrieval commands for Windows/macOS/Linux. Applied to all commands: > journal, > handoff, > save, > end, > qa, > backup, > commit.** |
