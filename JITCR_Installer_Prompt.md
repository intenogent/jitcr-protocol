────────────────────────────────────────────────────────────────────────────
JITCR Protocol Installer
────────────────────────────────────────────────────────────────────────────

This file contains the JITCR Protocol installation instructions.
Run each phase in order, starting with Phase 1 now.

────────────────────────────────────────────────────────────────────────────
WHAT IS JITCR?
────────────────────────────────────────────────────────────────────────────

JITCR (Just-In-Time Context Retrieval) is a token management protocol for
Claude Desktop. It splits project instructions across three tiers so Claude
only loads what it needs, when it needs it — reducing token usage
significantly across a session.

────────────────────────────────────────────────────────────────────────────
PHASE 1 — SILENT DETECTION (Run before saying anything to the user)
────────────────────────────────────────────────────────────────────────────

Run all checks silently. Do not greet the user. Do not explain what you are
doing. Just run the checks and then show the results block below.

CHECK 1 — Detect OS:
  Run: echo %OS%  (Windows returns "Windows_NT")
  Run: uname  (macOS returns "Darwin", Linux returns "Linux")
  Store as: {OS}  → Windows | macOS | Linux

CHECK 2 — filesystem MCP:
  Windows → try to read: C:\Windows\System32\drivers\etc\hosts
  macOS/Linux → try to read: /etc/hosts
  PASS → filesystem MCP is working
  FAIL → filesystem MCP is not responding

CHECK 3 — shell-command MCP:
  Run: echo "JITCR-TEST"
  PASS → shell-command MCP is working
  FAIL → shell-command MCP is not responding

CHECK 4 — Git:
  Run: git --version
  PASS → git is available
  FAIL → git not found (optional — only affects > commit and > end)

CHECK 5 — Detect username:
  Windows → run: powershell -Command "$env:USERNAME"
  macOS/Linux → run: echo $USER
  Store as: {Username}

────────────────────────────────────────────────────────────────────────────

After all checks, show the user this results block:

  ┌─────────────────────────────────────────────────────┐
  │  JITCR Protocol Installer — System Check Results    │
  ├─────────────────────────────────────────────────────┤
  │  OS detected      : {Windows | macOS | Linux}       │
  │  filesystem MCP   : [✅ OK | ❌ NOT FOUND]           │
  │  shell-command MCP: [✅ OK | ❌ NOT FOUND]           │
  │  Git              : [✅ OK | ⚠️  NOT FOUND]          │
  │  Username detected: {Username}                      │
  └─────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────
PHASE 1 — ERROR HANDLING
────────────────────────────────────────────────────────────────────────────

IF filesystem MCP FAILED:
  Show:

  "❌ INSTALLER CANNOT CONTINUE — filesystem MCP not responding.

  This installer requires the filesystem MCP to be configured and active
  in Claude Desktop. Without it, JITCR cannot read or write files on
  your computer.

  To fix this, open your Claude Desktop config file:

    Windows : %APPDATA%\Claude\claude_desktop_config.json
    macOS   : ~/Library/Application Support/Claude/claude_desktop_config.json
    Linux   : ~/.config/Claude/claude_desktop_config.json

  Make sure it includes a filesystem MCP entry with allowed_directories
  that includes your Documents folder (or wherever you want JITCR installed).

  Example (Windows):
  {
    \"mcpServers\": {
      \"filesystem\": {
        \"command\": \"npx\",
        \"args\": [\"-y\", \"@modelcontextprotocol/server-filesystem\",
                  \"C:\\\\Users\\\\{Username}\\\\Documents\"],
        \"type\": \"stdio\"
      }
    }
  }

  Example (macOS/Linux):
  {
    \"mcpServers\": {
      \"filesystem\": {
        \"command\": \"npx\",
        \"args\": [\"-y\", \"@modelcontextprotocol/server-filesystem\",
                  \"/Users/{Username}/Documents\"],
        \"type\": \"stdio\"
      }
    }
  }

  After updating the config:
  1. Save the file
  2. Fully quit and reopen Claude Desktop
  3. Start a new chat and attach this installer file again
  4. Say: see the attached

  Installation cancelled."

  STOP. Do not continue.

────────────────────────────────────────────────────────────────────────────

IF shell-command MCP FAILED:
  Show:

  "⚠️  shell-command MCP not detected.

  JITCR will still install but git commands (> commit, > end) will not
  work until shell-command MCP is configured.

  To fix this later, add to your Claude Desktop config file:

    Windows : %APPDATA%\Claude\claude_desktop_config.json
    macOS   : ~/Library/Application Support/Claude/claude_desktop_config.json
    Linux   : ~/.config/Claude/claude_desktop_config.json

  Add this entry to mcpServers:
    Windows : \"shell-command\": { \"command\": \"cmd\", \"args\": [\"/c\"], \"type\": \"stdio\" }
    macOS   : \"shell-command\": { \"command\": \"bash\", \"args\": [\"-c\"], \"type\": \"stdio\" }
    Linux   : \"shell-command\": { \"command\": \"bash\", \"args\": [\"-c\"], \"type\": \"stdio\" }

  Continue without shell-command MCP?

  [y] Yes, continue anyway    [n] No, I'll fix it first

  Your choice (type y or n):"

  Wait for user response.
  IF user types y → continue to human loop below
  IF user types n → "OK — fix the config, restart Claude Desktop, and attach this file again." STOP.

────────────────────────────────────────────────────────────────────────────

IF Git NOT FOUND:
  Note quietly in results block with ⚠️. Continue without stopping.
  Git is optional — only needed for > commit and > end commands.

────────────────────────────────────────────────────────────────────────────
PHASE 1 — HUMAN LOOP (after results block)
────────────────────────────────────────────────────────────────────────────

After showing results block (and resolving any MCP issues above), show:

  "Ready to set up JITCR Protocol on your computer.

  [y] Continue to setup    [n] Cancel

  Your choice (type y or n):"

  IF user types y → proceed to Phase 2
  IF user types n → "Installation cancelled. Goodbye!" STOP.

────────────────────────────────────────────────────────────────────────────
PHASE 2 — GATHER PROJECT INFO
Minimal typing. Numbers for choices, free text only where needed.
────────────────────────────────────────────────────────────────────────────

  ┌────────────────────────────────────────────────────┐
  │  Phase 2: Project Setup (5 questions)              │
  │  Progress: [1/5]                                   │
  └────────────────────────────────────────────────────┘

Q0: Where should JITCR store its files?

    Default path:
      Windows : C:\Users\{Username}\Documents\JITCR_Protocol\
      macOS   : /Users/{Username}/Documents/JITCR_Protocol/
      Linux   : /home/{Username}/Documents/JITCR_Protocol/

    [1] Use Default    [2] Custom Path

    Your choice (type 1 or 2):

    IF user types 1 → use OS default as {HubRoot}
    IF user types 2 → ask "Enter your custom path:"
    Store as: {HubRoot}
    Show: ✓ Confirmed: {HubRoot}

────────────────────────────────────────────────────────────────────────────

  ┌────────────────────────────────────────────────────┐
  │  Phase 2: Project Setup (5 questions)              │
  │  Progress: [2/5]                                   │
  └────────────────────────────────────────────────────┘

Q1: Project name?

    (No spaces. Example: MyPythonApp, my-app, MyTestProject)

    Your answer:

    Accept whatever the user types as-is. Do not ask for confirmation.
    IF user types → store as {ProjectName}
    Show: ✓ Confirmed: {ProjectName}

────────────────────────────────────────────────────────────────────────────

  ┌────────────────────────────────────────────────────┐
  │  Phase 2: Project Setup (5 questions)              │
  │  Progress: [3/5]                                   │
  └────────────────────────────────────────────────────┘

Q2: Project root folder?

    Default: {HubRoot}/{ProjectName}/

    [1] Use Default    [2] Custom Path

    Your choice (type 1 or 2):

    IF user types 1 → set {ProjectRoot} = {HubRoot}/{ProjectName}/
    IF user types 2 → ask "Enter custom path:"
    Store as: {ProjectRoot}
    Show: ✓ Confirmed: {ProjectRoot}

────────────────────────────────────────────────────────────────────────────

  ┌────────────────────────────────────────────────────┐
  │  Phase 2: Project Setup (5 questions)              │
  │  Progress: [4/5]                                   │
  └────────────────────────────────────────────────────┘

Q3: Role description (one sentence)?

    (Example: "Claude is the development assistant for MyApp, a Python web scraper.")

    Your answer:

    IF user types → store as {RoleDescription}
    Show: ✓ Confirmed: {RoleDescription}

────────────────────────────────────────────────────────────────────────────

  ┌────────────────────────────────────────────────────┐
  │  Phase 2: Project Setup (5 questions)              │
  │  Progress: [5/5]                                   │
  └────────────────────────────────────────────────────┘

Q4: Initialize git for this project?

    [1] Yes    [2] No    [3] Already exists

    Your choice (type 1, 2, or 3):

    IF user types 1 → {GitChoice} = yes
    IF user types 2 → {GitChoice} = no
    IF user types 3 → {GitChoice} = already
    Show: ✓ Confirmed: {GitChoice}

    IF GitChoice = yes OR already:

      Q4a: Push to GitHub?

           [y] Yes    [n] No

           Your choice (type y or n):

           IF user types y → {GitHubPush} = yes
           IF user types n → {GitHubPush} = no
           Show: ✓ Confirmed: {GitHubPush}

           IF GitHubPush = yes:

             Q4b: GitHub remote URL?

                  (Example: https://github.com/username/repo-name.git)

                  Your answer:

                  IF user types → store as {GitHubRemote}
                  Run: git -C "{ProjectRoot}" remote add origin "{GitHubRemote}"
                  Show: ✓ Confirmed: {GitHubRemote}

           IF GitHubPush = no:
             Store {GitHubRemote} = none
             Show: ✓ Local git only

    IF GitChoice = no:
      Store {GitHubPush} = no
      Store {GitHubRemote} = none
      Show: ✓ Git initialization skipped

────────────────────────────────────────────────────────────────────────────
PHASE 2 — FINAL CONFIRMATION BEFORE INSTALLATION
────────────────────────────────────────────────────────────────────────────

After all questions answered, show this confirmation screen:

  ┌────────────────────────────────────────────────────┐
  │  JITCR Protocol — Ready to Install                 │
  └────────────────────────────────────────────────────┘

  I now have everything I need and am ready to install the JITCR Protocol
  on your system. Here is exactly what will happen:

  📋 Project Summary:
     • Project name : {ProjectName}
     • Install path : {HubRoot}
     • Project root : {ProjectRoot}
     • Git          : {GitChoice}
     • GitHub push  : {GitHubPush}

  📁 Folders to create on your computer:
     • {HubRoot}/
     • {HubRoot}/{ProjectName}/
     • {HubRoot}/{ProjectName}/logs/
     • {HubRoot}/{ProjectName}/skills/

  📥 Files to download from GitHub:
     • JITCR_Universal_Commands.md  (if not already on your computer)
     • JITCR_Skills_Protocol.md     (if not already on your computer)
     • SKILL_TEMPLATE.md            (if not already on your computer)
     Source: https://github.com/intenogent/jitcr-protocol

  📄 Files to create on your computer:
     • JITCR_{ProjectName}.md  (your personal Tier 2 project guide)

  Nothing will be downloaded or created until you type y below.

  [y] Yes, install now    [n] Cancel

  Your choice (type y or n):

  IF user types y → proceed to Phase 3
  IF user types n → "Installation cancelled. Goodbye!" STOP.

────────────────────────────────────────────────────────────────────────────
PHASE 3 — CREATE EVERYTHING
Execute only after user confirms. Show progress at each step.
────────────────────────────────────────────────────────────────────────────

STEP 1 — Create folder structure:

  Show progress:
  ┌────────────────────────────────────────────────────┐
  │  Installing... (1/7)                               │
  └────────────────────────────────────────────────────┘

  Attempt to create:
    • {HubRoot}/
    • {HubRoot}/{ProjectName}/
    • {HubRoot}/{ProjectName}/logs/
    • {HubRoot}/{ProjectName}/skills/

  IF ANY FOLDER CREATION FAILS:
    Show:

    "⚠️  CANNOT CREATE FOLDERS — Installation stopped.

    Path that failed: {failed_path}

    Reason: The filesystem MCP does not have permission to access this location.

    To fix this, open your Claude Desktop config file:

      Windows : %APPDATA%\Claude\claude_desktop_config.json
      macOS   : ~/Library/Application Support/Claude/claude_desktop_config.json
      Linux   : ~/.config/Claude/claude_desktop_config.json

    Find the filesystem MCP entry and make sure allowed_directories includes
    the parent folder of the path that failed.

    Example (Windows) — to allow C:\Users\{Username}\Documents\JITCR_Protocol\:
      \"args\": [\"-y\", \"@modelcontextprotocol/server-filesystem\",
                \"C:\\\\Users\\\\{Username}\\\\Documents\"]

    Example (macOS/Linux) — to allow /Users/{Username}/Documents/JITCR_Protocol/:
      \"args\": [\"-y\", \"@modelcontextprotocol/server-filesystem\",
                \"/Users/{Username}/Documents\"]

    Steps to fix:
    1. Open the config file at the path shown above
    2. Update allowed_directories to include the required path
    3. Save the file
    4. Fully quit and reopen Claude Desktop
    5. Start a new chat, attach this installer file, and say: see the attached

    Installation cancelled."

    STOP. Do not continue.

  IF ALL FOLDERS CREATED SUCCESSFULLY:
    Show: "✓ Folders created"
    Continue to STEP 2.

────────────────────────────────────────────────────────────────────────────

STEP 2 — Download JITCR_Universal_Commands.md:

  Show progress:
  ┌────────────────────────────────────────────────────┐
  │  Installing... (2/7)                               │
  └────────────────────────────────────────────────────┘

  Check if {HubRoot}/JITCR_Universal_Commands.md exists.
  IF exists → skip, show "✓ Universal Commands already present"
  IF missing → download from:
    https://raw.githubusercontent.com/intenogent/jitcr-protocol/main/JITCR_Universal_Commands.md
    Save to: {HubRoot}/JITCR_Universal_Commands.md

  IF DOWNLOAD OR WRITE FAILS:
    Show:

    "⚠️  CANNOT WRITE FILE — Installation stopped.

    File that failed: {HubRoot}/JITCR_Universal_Commands.md

    Reason: The filesystem MCP cannot write to this location.

    To fix this, open your Claude Desktop config file:

      Windows : %APPDATA%\Claude\claude_desktop_config.json
      macOS   : ~/Library/Application Support/Claude/claude_desktop_config.json
      Linux   : ~/.config/Claude/claude_desktop_config.json

    Ensure allowed_directories includes: {HubRoot}

    Steps to fix:
    1. Open the config file
    2. Add {HubRoot} to allowed_directories
    3. Save and fully restart Claude Desktop
    4. Attach this installer file again and say: see the attached

    Installation cancelled."

    STOP.

  IF SUCCESS:
    Show: "✓ Universal Commands ready"
    Continue to STEP 3.

────────────────────────────────────────────────────────────────────────────

STEP 3 — Download JITCR_Skills_Protocol.md:

  Show progress:
  ┌────────────────────────────────────────────────────┐
  │  Installing... (3/7)                               │
  └────────────────────────────────────────────────────┘

  Check if {HubRoot}/JITCR_Skills_Protocol.md exists.
  IF exists → skip, show "✓ Skills Protocol already present"
  IF missing → download from:
    https://raw.githubusercontent.com/intenogent/jitcr-protocol/main/JITCR_Skills_Protocol.md
    Save to: {HubRoot}/JITCR_Skills_Protocol.md

  IF DOWNLOAD OR WRITE FAILS:
    Show same error pattern as STEP 2 with updated filename.
    STOP.

  IF SUCCESS:
    Show: "✓ Skills Protocol ready"
    Continue to STEP 4.

────────────────────────────────────────────────────────────────────────────

STEP 4 — Download SKILL_TEMPLATE.md:

  Show progress:
  ┌────────────────────────────────────────────────────┐
  │  Installing... (4/7)                               │
  └────────────────────────────────────────────────────┘

  Check if {HubRoot}/{ProjectName}/skills/SKILL_TEMPLATE.md exists.
  IF exists → skip, show "✓ Skill Template already present"
  IF missing → download from:
    https://raw.githubusercontent.com/intenogent/jitcr-protocol/main/SKILL_TEMPLATE.md
    Save to: {HubRoot}/{ProjectName}/skills/SKILL_TEMPLATE.md

  IF DOWNLOAD OR WRITE FAILS:
    Show same error pattern as STEP 2 with updated filename and path.
    STOP.

  IF SUCCESS:
    Show: "✓ Skill Template ready"
    Continue to STEP 5.

────────────────────────────────────────────────────────────────────────────

STEP 5 — Write JITCR_{ProjectName}.md (Tier 2):

  Show progress:
  ┌────────────────────────────────────────────────────┐
  │  Installing... (5/7)                               │
  └────────────────────────────────────────────────────┘

  File path: {HubRoot}/{ProjectName}/JITCR_{ProjectName}.md

  Write the following content with all {placeholders} substituted:

---
# JITCR_{ProjectName}
**Protocol Version:** 2.9 (Enhanced: OS-aware file access + MCP tool loading + System Time Retrieval + Tier 2 First + Skills Protocol + Git Flow Fix)
**Project:** {ProjectName}
**Created:** {today's date YYYY-MM-DD}
**Last Updated:** {today's date YYYY-MM-DD}
**Purpose:** Tier 2 project guide. Loaded once per session via > start.

> Edit this file as your project evolves. Do not delete it.
> For full command logic, see: JITCR_Universal_Commands.md

---

## Project Identity
| Field | Value |
|---|---|
| Project Name | {ProjectName} |
| **OS** | **{OS}** |
| Project Root | {ProjectRoot} |
| Session Logs | {HubRoot}/{ProjectName}/logs/ |
| Universal Commands | {HubRoot}/JITCR_Universal_Commands.md |
| Protocol Version | 2.9 (Multi-OS enhanced + System Time Retrieval + Tier 2 First + Skills + Git Flow Fix) |
| Git | {active / not initialized} |
| GitHub Remote | {GitHubRemote} |
| GitHub Push | {GitHubPush} |

> **Tier 2 Note (v2.7):** When > start runs, Claude agents MUST read this file FIRST to get actual project paths. This ensures agents don't use hardcoded path assumptions that fail on different systems or projects.
>
> **OS Note:** This project is configured for {OS}. When > start runs:
> - If runtime OS matches {OS} → normal operation
> - If runtime OS differs → protocol will warn, but file access will still work via filesystem MCPs
>
> **System Time Note (v2.6+):** All timestamps in filenames and log content are ACTUAL system time, retrieved via shell-command. Never assumed or hard-coded.

## Project Purpose
{RoleDescription}

## Key File Paths
| File | Path |
|---|---|
| This file (Tier 2) | {HubRoot}/{ProjectName}/JITCR_{ProjectName}.md |
| Universal Commands | {HubRoot}/JITCR_Universal_Commands.md |
| Session logs | {HubRoot}/{ProjectName}/logs/ |
| Project root | {ProjectRoot} |

## Project Skills

No skills created yet. Use `> skill add` to create project-specific skills.

| Skill | Description | Status |
|-------|-------------|--------|
| (none yet) | — | — |

**How to manage skills:**
- `> skill list` — Show all skills
- `> skill add` — Create new skill (interactive)
- `> skill use <name>` — Load skill into session
- `> skill remove <name>` — Delete skill

See: JITCR_Skills_Protocol.md (in {HubRoot}) for complete guide.

## Commands
| Command | Action |
|---|---|
| > start | Initialize session — load context, check git |
| > journal | Write journal entry |
| > handoff | Create handoff snapshot |
| > save | journal + handoff |
| > status | Show last handoff, journal, git status |
| > commit | Commit project files to local git |
| > end | save + commit locally + optional GitHub push |
| > backup | Zip project root |
| > skill | Manage project skills (see Skills section above) |
| > ? | Show all available commands |

Full command logic → JITCR_Universal_Commands.md

## Version History
| Version | Date | Notes |
|---|---|---|
| 1.0 | {today's date} | Created by JITCR Protocol Installer |
---

  IF WRITE FAILS:
    Show same error pattern as STEP 2 with updated filename and path.
    STOP.

  IF SUCCESS:
    Show: "✓ Tier 2 guide created"
    Continue to STEP 6.

────────────────────────────────────────────────────────────────────────────

STEP 6 — Git initialization:

  Show progress:
  ┌────────────────────────────────────────────────────┐
  │  Installing... (6/7)                               │
  └────────────────────────────────────────────────────┘

  IF GitChoice = yes:
    Run: git init "{ProjectRoot}"
    Run: git -C "{ProjectRoot}" config user.name "JITCR User"
    Run: git -C "{ProjectRoot}" config user.email "user@local"
    Show: "✓ Git initialized"

  IF GitChoice = already:
    Run: git -C "{ProjectRoot}" status
    Show: "✓ Git repo confirmed"

  IF GitChoice = no:
    Show: "✓ Git skipped"

  Continue to STEP 7.

────────────────────────────────────────────────────────────────────────────

STEP 7 — Final summary:

  Show progress:
  ┌────────────────────────────────────────────────────┐
  │  Installing... (7/7)                               │
  └────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────┐
  │  ✅ Installation Complete!                         │
  └────────────────────────────────────────────────────┘

  Created:
    ✓ {HubRoot}/
    ✓ {HubRoot}/{ProjectName}/
    ✓ {HubRoot}/{ProjectName}/logs/
    ✓ {HubRoot}/{ProjectName}/skills/
    ✓ JITCR_{ProjectName}.md
    ✓ JITCR_Universal_Commands.md
    ✓ JITCR_Skills_Protocol.md
    ✓ skills/SKILL_TEMPLATE.md
    ✓ Git: {GitChoice}
    ✓ GitHub: {GitHubPush}

────────────────────────────────────────────────────────────────────────────
PHASE 4 — HAND OFF TO USER
────────────────────────────────────────────────────────────────────────────

Tell the user:

"✅ JITCR Protocol setup is complete for {ProjectName}!

One final step — copy the text below and paste it into your Claude Desktop
Project Instructions for this project:

  Go to: Project → Settings → Project Instructions
  Replace everything there with this text:

════════════════════════════════════════════════════
## CRITICAL: Before anything else
⚠️ **NEW AGENTS: Read this section FIRST before any other action!**

1. Load MCP Tools:
   - tool_search("filesystem read file windows")
   - tool_search("shell command execute")

2. READ THIS TIER 2 FILE FIRST (MANDATORY):
   {HubRoot}/{ProjectName}/JITCR_{ProjectName}.md

   (This file contains your actual project paths. Do NOT use hardcoded paths.)

3. Extract paths from that file and then proceed with > start

## Role
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
- On > start: STEP 2 = READ TIER 2 FILE FIRST (see CRITICAL section above)

## Environment
{OS}

## Command Prefix
> = execute command — full reference in JITCR_{ProjectName}.md
════════════════════════════════════════════════════

After pasting, start a new chat in this project and type:

  > start

That's it — JITCR is running! 🚀"

────────────────────────────────────────────────────────────────────────────
PHASE 5 — AGENT STARTUP PROCEDURE (FOR CLAUDE AGENTS ONLY)
────────────────────────────────────────────────────────────────────────────

⚠️ THIS SECTION IS FOR CLAUDE AGENTS, NOT USERS.

When a new agent starts a session in a JITCR project, it MUST follow the
procedure outlined in JITCR_Universal_Commands.md v2.9+ section "> start".

Key startup sequence (abbreviated):

STEP 0:  Load MCP Tools
STEP 1:  Read Project Instructions
STEP 2:  READ TIER 2 FILE FIRST (non-negotiable)
STEP 3:  Verify paths work
STEP 4:  Retrieve actual system time
STEP 5:  OS detection
STEP 6:  Git status check
STEP 7:  Load Tier 3 (latest handoff + journals)
STEP 8:  Skills summary
STEP 9:  Display session header
STEP 10: Begin session

See JITCR_Universal_Commands.md for complete details.
