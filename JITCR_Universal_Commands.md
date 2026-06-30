# JITCR Universal Commands
**Protocol Version:** 2.8
**Author:** LaserWhiz
**Created:** 2026-03-06
**Last Enhanced:** 2026-06-26
**Purpose:** Shared command engine for all JITCR Protocol implementations.
           This file is referenced by every project's JITCR_[ProjectName].md.

> ⚠️ Do NOT delete this file.
> Edit ONLY when upgrading the JITCR Protocol itself.
> Individual projects are customized in their own JITCR_[ProjectName].md file.

---

## Protocol Guardrails — All Projects

These seven rules apply to every project, every OS, every session:

1. Never delete files without explicit user permission
2. Never modify .env files without explicit user permission
3. Read existing files before overwriting — preserve content
4. Shell commands: always use forward slashes in paths
5. On `> start`: read Tier 2 file first — it contains actual project paths
6. Never assume date/time — always retrieve actual system time
7. Never assume project paths — always read Tier 2 to get actual paths

---

## Tier 2 File Reading (v2.7+)

The Tier 2 file (JITCR_[ProjectName].md) contains the actual project paths for this specific install.
Read Tier 2 first at session start — this is how JITCR works correctly across Windows, macOS,
and Linux without hardcoded path assumptions.

See JITCR_Universal_Commands.md v2.7+ section for details.

---

## System Date/Time Retrieval Protocol (v2.6+)

Never assume or hard-code timestamps — always retrieve actual system date/time.
This applies to all logging commands and file operations.

See JITCR_Universal_Commands.md v2.6+ section for details.

---

## `> start` — Initialize Session (UPDATED v2.7)

```
Follow this sequence in order — each step depends on the previous one.

STEP 0: Load MCP Tools
        A. tool_search("filesystem read file windows")
        B. tool_search("shell command execute")
        C. Confirm: "MCP tools loaded"

STEP 1: Read Project Instructions from Claude Desktop
        Extract: {ProjectName}, {ProjectRoot}, {OS}
        Store as session variables

STEP 2: Read Tier 2 file first — actual project paths live here
        A. Read Tier 2 file
        B. Extract all paths and configuration
        C. Confirm: "Tier 2 loaded"

STEP 3: Verify Paths Work
        A. List logs directory
        B. Confirm paths are correct
        C. Confirm: "Paths verified ✓"

STEP 4: Retrieve System Time
        Get actual system time (not assumed)
        Store as {session_time}
        Confirm: "Time retrieved: {session_time}"

STEP 5: OS Detection (silent)
        Detect Windows, macOS, or Linux

STEP 6: Git Status Check
        Check if repo is active
        Enable/prompt for git as needed

STEP 7: Load Tier 3 (Conditional)
        Load latest handoff + journals if BLOCKED status
        Load recent git log if active

STEP 8: Skills Summary (NEW v2.8)
        Check if skills folder exists
        List enabled skills
        Show: "X enabled skills available"

STEP 9: Display Session Header
        ┌────────────────────────────────────┐
        │ Project  : {ProjectName}           │
        │ OS       : {runtime_os}            │
        │ Root     : {ProjectRoot}           │
        │ Started  : {session_time}          │
        │ Git      : {active | inactive}     │
        │ GitHub   : {push enabled | local}  │
        │ Skills   : {X enabled | ready}     │
        │ Loaded   : Tier 2 + Tier 3         │
        │ Commands : > journal, save, end... │
        └────────────────────────────────────┘

STEP 10: Begin Session
        Ready to help with user's task
```

---

## SKILLS COMMANDS (NEW in v2.8)

All skills commands are available via the `> skill` family. Skills are project-scoped, reusable
instructions that load on-demand. See JITCR_Skills_Protocol.md for complete documentation.

### Discovery Commands

#### `> skill list`
**Purpose:** List all skills in this project

**Output format:**
```
Enabled skills (will load on > start or via > skill use):
  • skill-name-1 — One-line description
  • skill-name-2 — One-line description

Disabled skills (available on-demand):
  • skill-name-3 — One-line description

Use: > skill use <name>  or  > skill info <name>
```

#### `> skill info <name>`
**Purpose:** Show details about a specific skill

**Output format:**
```
Skill: skill-name

Description:  One-line description
Scope:        Single-task / Multi-step / Utility
Status:       Enabled / Disabled
Created:      YYYY-MM-DD
Path:         {ProjectName}\skills\skill-name\SKILL.md

To use: > skill use skill-name
To edit: > skill edit skill-name
To disable: > skill disable skill-name
```

### Creation Commands

#### `> skill add` (Interactive, Three-Path)
**Purpose:** Create a new skill

**Flow:**
```
Detects user intent:
  
  PATH 1: User provides skill content
    Q: Skill name?
    Q: One-line description?
    Q: Paste skill content?
    → Claude validates → Creates skill
  
  PATH 2: User provides description only
    Q: Skill name?
    Q: What should this skill do? (detailed)
    → Claude generates from best practices
    → User reviews → Creates skill
  
  PATH 3: User exploring
    Q: What problem are you solving?
    → Claude validates if it's skill-material
    → If yes: generates draft
    → If no: explains why and suggests alternative

Final Q: Load automatically on > start? (yes/no)
         Default: yes (can change with > skill disable)

Result: Skill created in {ProjectName}\skills\{skill-name}\
        SKILL.md + skill-metadata.json created
        Tier 2 updated automatically
```

### Usage Commands

#### `> skill use <name>`
**Purpose:** Load a skill into current session

**Effect:**
- Loads skill content into context window
- Available for all remaining messages in this session
- Can load multiple skills in one session
- Skills auto-unload at session end

**Example output:**
```
✓ Skill loaded: github-automation
  Available for this session
  Use: I'll reference the skill content as needed
```

### Management Commands

#### `> skill enable <name>`
**Purpose:** Allow a skill to auto-load on > start

**Effect:**
- Skill will load automatically next session
- Appears in skill summary at > start

#### `> skill disable <name>`
**Purpose:** Prevent a skill from auto-loading

**Effect:**
- Skill won't load at > start
- Can still be loaded manually with > skill use

#### `> skill edit <name>`
**Purpose:** Edit skill content or metadata

**Available edits:**
- Edit SKILL.md content
- Update description
- Change auto-load setting
- Update other metadata

#### `> skill remove <name>`
**Purpose:** Delete a skill

**Confirmation required before deletion:**
```
Delete skill "skill-name"? (yes/no)

This will:
  • Delete folder: {ProjectName}\skills\skill-name\
  • Remove from Tier 2
  • Cannot be undone (but recoverable from git if committed)

Confirm? (yes/no)
```

### Validation Commands

#### `> skill validate`
**Purpose:** Check all skills for JITCR compliance

**Checks:**
- Folder structure valid
- SKILL.md present and readable
- skill-metadata.json valid JSON
- Metadata has all required fields

**Output:**
```
Validating all skills...

skill-name-1    ✓ PASS
skill-name-2    ✓ PASS
skill-name-3    ⚠ WARNING (metadata issue)

Results: 2 passed, 1 warning, 0 failed
```

#### `> skill validate <name>`
**Purpose:** Check a specific skill

**Output:**
```
Validating: skill-name

Structure    ✓ Valid
SKILL.md     ✓ Readable
Metadata     ✓ Valid JSON
Size         ✓ Reasonable

Result: ✓ PASS — Ready for use
```

### Suggestion Command

#### `> skill suggest` (NEW v2.8)
**Purpose:** Smart suggestion based on session context

**Intelligence:**
- Analyzes last journal entries
- Analyzes current session context
- Recommends relevant enabled skills
- User confirms before loading

**Example output:**
```
Based on your work (code review), you might want:
  • code-review skill
  • documentation skill

Load them? (yes/no)
```

### Help Command

#### `> ? skill`
**Purpose:** Show all skills commands

**Output:**
```
┌──────────────────────────────────┐
│  JITCR Skills Commands           │
├──────────────────────────────────┤
│  > skill list        List all    │
│  > skill add         Create new  │
│  > skill use <name>  Load skill  │
│  > skill info <name> Show details│
│  > skill enable <name> Activate  │
│  > skill disable <name> Deactivate
│  > skill edit <name> Edit skill  │
│  > skill remove <name> Delete    │
│  > skill validate    Check all   │
│  > skill suggest     Smart hint  │
│  > ? skill           This help   │
└──────────────────────────────────┘

Tip: Skills load on-demand. Use > skill list to discover skills.
```

---

## `> journal` — Write Session Journal Entry

```
1. Retrieve ACTUAL system time
2. Create filename: journal_YYYY-MM-DD_HHMM.md (using actual time)
   Location: {HubRoot}/{ProjectName}/logs/
3. Create header: ## YYYY-MM-DD HH:MM | Session: [title]
4. Append entry content with actual timestamps
5. Confirm: "Journal updated → journal_YYYY-MM-DD_HHMM.md"
```

---

## `> handoff` — Create Session Handoff

```
1. Retrieve ACTUAL system time
2. Create filename: handoff_YYYY-MM-DD_HHMM.md (using actual time)
   Location: {HubRoot}/{ProjectName}/logs/
3. Create header: # Session Handoff — YYYY-MM-DD HH:MM
4. Write handoff content with actual timestamps
5. Confirm: "Handoff saved → handoff_YYYY-MM-DD_HHMM.md"
```

---

## `> save` — Quick Save

```
1. Retrieve ACTUAL system time ONCE
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

## `> commit` — Git Commit

```
1. Retrieve actual system time

2. Show what will be committed:
   git -C "{ProjectRoot}" status --short
   Show: "Ready to commit the above changes. Proceed? (yes/no)"
   IF no: "Commit cancelled." STOP.

3. Stage and commit:
   git -C "{ProjectRoot}" add -A
   git -C "{ProjectRoot}" commit -m "{user message if provided | 'Checkpoint — YYYY-MM-DD HH:MM'}"
   Confirm: "Committed locally → {hash}"

4. GitHub push (only if {GitHubPush} = yes):
   IF {push_enabled}:
     Show: "Push to GitHub now? (yes/no)"
     IF yes:
       Detect branch: git -C "{ProjectRoot}" rev-parse --abbrev-ref HEAD
       Run: git -C "{ProjectRoot}" push origin {branch}
       Confirm: "Pushed → {GitHubRemote} ({branch})"
       IF push fails: "Push failed — check GitHub authentication
                       (SSH key or HTTPS credentials must be pre-configured)"
     IF no:
       Show: "Committed locally only."
   IF NOT {push_enabled}: Silent (local commit is final step)
```

---

## `> end` — End Session

```
1. Retrieve ACTUAL system time at session END

2. Run > save using END time

3. Local commit:
   git -C "{ProjectRoot}" add -A
   git -C "{ProjectRoot}" commit -m "Session end — YYYY-MM-DD HH:MM"
   Confirm: "Committed locally → {hash}"

4. GitHub push (only if {GitHubPush} = yes):
   IF {push_enabled}:
     Show: "Push to GitHub now? (yes/no)"
     IF yes:
       Detect branch: git -C "{ProjectRoot}" rev-parse --abbrev-ref HEAD
       Run: git -C "{ProjectRoot}" push origin {branch}
       Confirm: "Pushed → {GitHubRemote} ({branch})"
       IF push fails: "Push failed — check GitHub authentication
                       (SSH key or HTTPS credentials must be pre-configured)"
     IF no:
       Show: "Skipped — committed locally only."
   IF NOT {push_enabled}: Silent (local commit is final step)

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

## `> ?` — Show Help (UPDATED v2.8)

```
Display all available commands:

┌──────────────────────────────────────┐
│  JITCR Commands — {ProjectName}       │
├──────────────────────────────────────┤
│  > start    Initialize session        │
│  > journal  Write timestamped entry   │
│  > handoff  Create session snapshot   │
│  > save     journal + handoff         │
│  > status   Last handoff, journal,... │
│  > commit   Commit to local git       │
│  > end      save + commit + push      │
│  > backup   Zip project root          │
│  > skill    Manage project skills     │
│  > ?        Show this help            │
└──────────────────────────────────────┘

Sub-help available:
  > ? skill     Show all skills commands
  > ? journal   Show journal details
  > ? commit    Show commit options

Tip: Use natural extensions:
  > journal "topic"    Journal with title
  > commit "message"   Commit with message
  > end yes            End + auto-push
```

---

## File Naming Conventions

| File Type | Format | Location |
|---|---|---|
| Tier 2 guide | `JITCR_[ProjectName].md` | `{HubRoot}/{ProjectName}/` |
| Journal | `journal_YYYY-MM-DD_HHMM.md` | `{HubRoot}/{ProjectName}/logs/` |
| Handoff | `handoff_YYYY-MM-DD_HHMM.md` | `{HubRoot}/{ProjectName}/logs/` |
| Backup | `{ProjectName}_backup_YYYY-MM-DD_HHMM.zip` | Project root |
| Skill | `SKILL.md` | `{HubRoot}/{ProjectName}/skills/{skill-name}/` |
| Skill Metadata | `skill-metadata.json` | `{HubRoot}/{ProjectName}/skills/{skill-name}/` |

---

## Execution Environment Rules

- ALL JITCR file operations use filesystem MCP or shell-command MCP only
- filesystem MCP → native OS paths (backslash on Windows, forward slash on macOS/Linux)
- shell-command MCP → forward slashes regardless of OS
- Always retrieve actual system time via shell-command before creating any log file
- Always read Tier 2 first to get actual paths — never use hardcoded assumptions
- **Skills folder is auto-created at installation, ready for user skill creation**

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
| 2.6 | 2026-06-25 | System Date/Time Retrieval Protocol |
| 2.7 | 2026-06-25 | Tier 2 File Reading (mandatory first step) |
| 2.8 | 2026-06-26 | Skills Protocol v1.0 — complete skills command family |
| **2.9** | **2026-06-30** | **Fixed > commit and > end git flows: added git add -A to > end commit step (was missing); added human-in-the-loop confirmation + git status preview before committing in > commit; added optional GitHub push to > commit (was local-only); made > end push flow explicit with real git commands, branch detection, and auth failure guidance. Both commands now show git status before committing and ask before pushing.** |

---
