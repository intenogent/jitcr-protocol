# JITCR Universal Commands
**Protocol Version:** 2.7
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

These seven rules apply to every project, every OS, every session:

1. Never delete files without explicit user permission
2. Never modify .env files without explicit user permission
3. Read existing files before overwriting — preserve content
4. Shell commands: always use forward slashes in paths
5. On `> start`: **READ TIER 2 FILE FIRST** (non-negotiable startup step)
6. **NEVER assume date/time — ALWAYS retrieve actual system time**
7. **NEVER assume project paths — ALWAYS read Tier 2 to get actual paths**

---

## Tier 2 File Reading (MANDATORY — NEW in v2.7)

⚠️ **CRITICAL**: The Tier 2 file (JITCR_[ProjectName].md) contains the ACTUAL project paths.
   ALWAYS read Tier 2 FIRST before doing anything else.
   This is how JITCR works across Windows, macOS, and Linux without hardcoded assumptions.

### Why Tier 2 First?

Different users have different paths:
- Windows user: `C:\Users\Alice\Documents\JITCR_Protocol\MyProject\`
- macOS user: `/Users/bob/Documents/JITCR_Protocol\MyProject/`
- Linux user: `/home/charlie/Documents/JITCR_Protocol/MyProject/`

These paths are set DURING INSTALLATION and stored IN TIER 2.
Tier 2 is the SOURCE OF TRUTH for project paths.
If you don't read Tier 2 first, you'll use hardcoded assumptions that are WRONG.

### How to Find and Read Tier 2

**On > start (STEP 1-2):**

1. Load MCP Tools:
   - `tool_search("filesystem read file windows")`
   - `tool_search("shell command execute")`

2. Read Project Instructions (from Claude Desktop)
   - Extract: {ProjectName}, {ProjectRoot}, {OS}
   - Note the "On > start: read JITCR_[ProjectName].md" line

3. Determine Tier 2 path:
   - **Most common:** `{ProjectRoot}/JITCR_{ProjectName}.md`
   - **Fallback:** Check parent directory of {ProjectRoot}

4. Read Tier 2:
   ```
   filesystem:read_text_file("{ProjectRoot}/JITCR_{ProjectName}.md")
   ```

5. Extract from Tier 2:
   - {HubRoot} — from "Session Logs" field parent directory
   - {ProjectRoot} — confirmed from "Project Root" field
   - Logs path: {HubRoot}/{ProjectName}/logs/
   - GitHub status: {GitHubRemote} and {GitHubPush}

6. Use these ACTUAL paths for rest of session

**After Reading Tier 2:**
- You now have ACTUAL project paths (not assumptions)
- You can read/write logs to correct location
- You can commit to git with correct paths
- You can push to correct GitHub remote (if enabled)

---

## System Date/Time Retrieval Protocol (MANDATORY — v2.6+)

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
Output: 2026-06-25 1703
Meaning: June 25, 2026 at 5:03 PM (17:03)
```

#### **macOS**
```bash
date +"%Y-%m-%d %H%M"
Output: 2026-06-25 1703
Meaning: June 25, 2026 at 5:03 PM (17:03)
```

#### **Linux**
```bash
date +"%Y-%m-%d %H%M"
Output: 2026-06-25 1703
Meaning: June 25, 2026 at 5:03 PM (17:03)
```

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

## `> start` — Initialize Session (UPDATED v2.7)

```
⚠️ CRITICAL: This sequence must be followed EXACTLY. Do not skip steps.

STEP 0: Load MCP Tools (CRITICAL)
        A. tool_search("filesystem read file windows")
        B. tool_search("shell command execute")
        C. Confirm: "MCP tools loaded"

STEP 1: Read Project Instructions from Claude Desktop
        Extract: {ProjectName}, {ProjectRoot}, {OS}
        Store as session variables

STEP 2: READ TIER 2 FILE FIRST (NON-NEGOTIABLE)
        ⚠️ This is the most important step. Do NOT skip.
        
        A. Determine Tier 2 path:
           Most common: {ProjectRoot}/JITCR_{ProjectName}.md
           Fallback: parent({ProjectRoot})/JITCR_{ProjectName}.md
        
        B. Read Tier 2 using filesystem MCP:
           filesystem:read_text_file("{ProjectRoot}/JITCR_{ProjectName}.md")
        
        C. IF file not found:
           → Ask user: "What is your {HubRoot} path? 
                       (Should be like C:\Users\...\Documents\JITCR_Protocol)"
           → Wait for answer
           → Use that path to locate Tier 2
           → Load Tier 2
        
        D. Extract from Tier 2 and store as session variables:
           - {HubRoot} (from "Session Logs" field parent)
           - {ProjectRoot} (confirmed)
           - {ProjectName} (confirmed)
           - {GitHubRemote} and {GitHubPush} status
        
        E. Confirm: "Tier 2 loaded → {ProjectRoot}/JITCR_{ProjectName}.md"

STEP 3: Verify Paths Work
        A. Try to list logs directory:
           filesystem:list_directory("{HubRoot}/{ProjectName}/logs/")
        
        B. IF path fails:
           → STOP
           → Ask user: "Logs directory not found. Can you confirm your paths?"
           → Help user locate correct paths
           → Do NOT proceed until paths are verified
        
        C. Confirm: "Paths verified ✓"

STEP 4: Retrieve System Time (from v2.6)
        Windows: shell-command("powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"")
        macOS/Linux: shell-command("date +"%Y-%m-%d %H%M"")
        Store as {session_time}
        Confirm: "Time retrieved: {session_time}"

STEP 5: OS Detection (silent)
        Windows → {runtime_os} = Windows
        macOS   → {runtime_os} = macOS
        Linux   → {runtime_os} = Linux

STEP 6: Git Status Check
        Run: git -C "{ProjectRoot}" status
        Result A — repo active → git commands enabled
        Result B — no repo → prompt user (initialize or skip)
        Result C — repo, no remote → note silently, local commits only

STEP 7: Load Tier 3 (Conditional)
        ALWAYS → read latest handoff from {HubRoot}/{ProjectName}/logs/
        CONDITIONALLY → if handoff status = BLOCKED,
                        also read last 3 journals from same folder
        CONDITIONALLY → if git active, run: git log -5 --oneline

STEP 8: Display Session Header
        ┌────────────────────────────────────┐
        │ Project  : {ProjectName}           │
        │ OS       : {runtime_os}            │
        │ Root     : {ProjectRoot}           │
        │ Started  : {session_time}          │
        │ Git      : {active | inactive}     │
        │ GitHub   : {push enabled | local}  │
        │ Loaded   : Tier 2 + Tier 3         │
        │ Commands : > journal, save, end... │
        └────────────────────────────────────┘

STEP 9: Begin Session
        Ready to help with user's task
```

---

## `> journal` — Write Session Journal Entry

```
1. Retrieve ACTUAL system time:
   Windows: powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"
   macOS/Linux: date +"%Y-%m-%d %H%M"

2. Create filename: journal_YYYY-MM-DD_HHMM.md (using actual time)
   Location: {HubRoot}/{ProjectName}/logs/

3. Create header: ## YYYY-MM-DD HH:MM | Session: [title]

4. Append entry content with actual timestamps

5. Confirm: "Journal updated → journal_YYYY-MM-DD_HHMM.md"
```

---

## `> handoff` — Create Session Handoff

```
1. Retrieve ACTUAL system time:
   Windows: powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"
   macOS/Linux: date +"%Y-%m-%d %H%M"

2. Create filename: handoff_YYYY-MM-DD_HHMM.md (using actual time)
   Location: {HubRoot}/{ProjectName}/logs/

3. Create header: # Session Handoff — YYYY-MM-DD HH:MM

4. Write handoff content with actual timestamps

5. Confirm: "Handoff saved → handoff_YYYY-MM-DD_HHMM.md"
```

---

## `> save` — Quick Save

```
1. Retrieve ACTUAL system time ONCE:
   Windows: powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"
   macOS/Linux: date +"%Y-%m-%d %H%M"

2. Run > journal using retrieved time

3. Run > handoff using same retrieved time

4. Confirm: "Session saved (YYYY-MM-DD HH:MM)"
```

---

## `> status` — Show Current State

```
1. Find and display last handoff filename + status line
2. Find and display last journal filename + status line
3. IF git active → run: git status --short
4. Display summary
```

---

## `> commit` — Git Commit (Local Only)

```
1. Retrieve actual system time for commit message
2. git -C "{ProjectRoot}" add -A
3. git -C "{ProjectRoot}" commit -m "{message}"
4. Confirm: "Committed locally → {hash}"
```

---

## `> end` — End Session

```
1. Retrieve ACTUAL system time at session END
2. Run > save using END time
3. Local commit with actual END timestamp:
   git -C "{ProjectRoot}" commit -m "Session end — YYYY-MM-DD HH:MM"
4. GitHub push (only if {GitHubPush} = yes):
   IF {push_enabled}: Prompt user, then push
   IF NOT {push_enabled}: Silent (local commit final step)
5. Display session summary with actual END timestamp
```

---

## `> backup` — Backup Project Folder

```
1. Retrieve actual system time
2. Create backup filename with actual timestamp
3. Windows: Compress-Archive with timestamp
4. macOS/Linux: zip with timestamp
5. Confirm with actual timestamp in output
```

---

## File Naming Conventions

| File Type | Format | Location |
|---|---|---|
| Tier 2 guide | `JITCR_[ProjectName].md` | `{HubRoot}/{ProjectName}/` |
| Journal | `journal_YYYY-MM-DD_HHMM.md` | `{HubRoot}/{ProjectName}/logs/` |
| Handoff | `handoff_YYYY-MM-DD_HHMM.md` | `{HubRoot}/{ProjectName}/logs/` |
| QA Results | `qa_YYYY-MM-DD_HHMM.md` | `{HubRoot}/{ProjectName}/logs/` |
| Backup | `{ProjectName}_backup_YYYY-MM-DD_HHMM.zip` | Project root |

---

## Execution Environment Rules

- ALL JITCR file operations use filesystem MCP or shell-command MCP only
- filesystem MCP → native OS paths (backslash on Windows, forward slash on macOS/Linux)
- shell-command MCP → forward slashes regardless of OS
- **ALWAYS retrieve actual system time via shell-command before creating ANY log file**
- **ALWAYS read Tier 2 first to get actual paths (not hardcoded assumptions)**

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-03-06 | Initial universal commands file |
| 2.1 | 2026-03-07 | Added > qa command |
| 2.2 | 2026-03-07 | Fixed OS detection |
| 2.3 | 2026-03-13 | Removed Sessions\ folder, logs now in JITCR_Protocol\{ProjectName}\logs\ |
| 2.4 | 2026-03-16 | GitHub push guardrail |
| 2.5 | 2026-06-25 | Added File Access Protocol — OS detection + MCP tool loading |
| 2.6 | 2026-06-25 | System Date/Time Retrieval Protocol (MANDATORY) |
| **2.7** | **2026-06-25** | **CRITICAL FIX: Tier 2 File Reading (MANDATORY first step). Added Guardrail #7: "NEVER assume project paths — ALWAYS read Tier 2 to get actual paths". Updated > start to explicitly require reading Tier 2 BEFORE anything else. This fixes path discovery issues across Windows/macOS/Linux. Agents must read Tier 2 to find actual {HubRoot} and {ProjectRoot} — no more hardcoded path assumptions.** |
