# JITCR Protocol

[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Any%20AI%20Assistant-green)](#platform-compatibility)
[![Protocol](https://img.shields.io/badge/Protocol-v2.9-orange)](JITCR_Universal_Commands.md)

**Just-In-Time Context Retrieval -- AI session management for any platform.**

Every AI session starts from zero. Projects lose context. Tokens burn. Models degrade. JITCR fixes all of it.

---

## The Philosophy

Close the chat. Hit a token limit. Switch models. Come back three days later.

JITCR remembers -- because you told it to.

```
  > end      (Tuesday, 5:42 PM)
             Saves journal + handoff. Commits locally.
             Asks to push to GitHub if configured.

             ...three days pass...

  > start    (Friday, 9:15 AM)
             Reads the handoff. Restores full project context.
             No re-explaining. No "let me catch you up."
```

The AI reads exactly what you left behind -- what was done, what was decided, what's still open, what comes next -- and picks up mid-thought. If one handoff isn't enough, `> start` reaches further back through your journals automatically. You decide how much history matters. JITCR makes sure it gets read.

That same principle runs through everything else in JITCR. This is not a fixed tool with a fixed feature set -- it is a customizable framework. You bring your own knowledge, your own skills, your own validation rules, your own guardrails. A skill is not a built-in feature. It is domain expertise, a repeated process, an industry-specific rule, an output format your team requires -- whatever *you* define -- sitting on your machine, invisible, costing nothing until the moment you call it.

Nothing is hard-coded except the protocol itself. The protocol is the chassis. You build the agent.

---

## The Problem

AI assistants forget everything between sessions, degrade as context grows, and lock your work to a single model and platform. Research confirms it: every frontier model tested shows accuracy drops as context length increases -- up to 85% degradation, no exceptions. Meanwhile, your project instructions reload on every single message whether the AI needs them or not.

JITCR solves the full range: token waste, context degradation, lost session state, no reusable knowledge, no portable continuity, no domain validation, no real safety controls, no version discipline, and no path toward a shared ecosystem of AI capabilities.

---

## What You Get

| Theme | Capabilities |
|---|---|
| **Context Retrieval** | Just-in-time loading, multi-layer architecture, OS-aware operation |
| **Session Continuity** | Cross-session persistence, cross-model portability, actual timestamps, automatic path discovery |
| **Skills and Knowledge** | On-demand skills, fully user-defined and extensible, project-local RAG, custom input/output/interaction templates -- bring any knowledge, any rules, any workflow |
| **Validation** | Structural checks, conceptual validation, configurable multi-mode validation |
| **Guardrails** | Protocol-level rules, project-level custom rules, skill-level scoped rules, defense-in-depth safety |
| **Version Control** | Local git, optional GitHub push, timestamped project backup |
| **Commands** | 9 core commands, 10 skill-family commands, extensible framework |
| **Installer** | Automated setup, MCP error handling, automatic file downloads |
| **Ecosystem** | Marketplace-ready architecture, shared skills ecosystem |

---

## How It Works

JITCR organizes project context across layers. Each layer loads at the right time -- not all at once.

```
LAYER 1 -- Project Instructions (~200-300 tokens, every message)
  Lives in : AI platform persistent instructions
             (Claude Desktop Project Instructions, ChatGPT custom
              instructions, Gemini Gems, Copilot notebooks, or any
              equivalent your platform provides)
  Loads    : Every message
  Contains : Role, project name, root path, guardrails, > start trigger

LAYER 2 -- JITCR_{ProjectName}.md (~350 tokens, once per session)
  Lives in : JITCR_Protocol/{ProjectName}/ on your machine
  Loads    : Once at > start via file access tools
  Contains : Project purpose, key paths, GitHub config,
             project guardrails, skills registry, commands

LAYER 3 -- Session logs (~150 tokens, once per session)
  Lives in : JITCR_Protocol/{ProjectName}/logs/
  Loads    : Latest handoff always + recent journals if needed
  Contains : What was done, decisions made, open issues, next steps
```

Type `> start` and the AI reads all three layers automatically, checks git, detects your OS, retrieves real system time, and enters the session already knowing your project. Here is what that actually looks like on screen:

```
+--------------------------------------+
| Project  : BlogRewrite               |
| OS       : Windows                   |
| Root     : C:\Users\You\Documents\   |
|            BlogRewrite               |
| Started  : 2026-07-02 08:30          |
| Git      : active                    |
| GitHub   : local only                |
| Loaded   : Tier 2 + Tier 3          |
| Skills   : none                      |
| Commands : > journal, save, end...   |
+--------------------------------------+

Picking up from handoff 2026-06-29_1742. Last session
you finished the outline draft and were about to start
the introduction. Ready to continue, or something else?
```

No screen-sharing. No re-explaining. The AI already knows.

This is also where JITCR differs from approaches like a persistent chat thread, a synced notes app, or a folder of saved prompts: those keep a record, but they still rely on you to re-read it and re-explain what matters. JITCR's layers are read by the AI itself, every session, automatically — the record becomes context, not homework.

> See [HOWTO.md](HOWTO.md) for the full architecture deep dive, the complete first-session walkthrough, and step-by-step `> start` explanation.

---

## Quick Start

**Three things before you begin, then the installer takes over.**

1. Install Claude Desktop and add the filesystem MCP to your config file
2. Create a project and paste the installer agent block into Project Instructions
3. Download `JITCR_Installer_Prompt.md` from this repo, attach it to a chat, and type `see the attached`

The installer runs five guided questions, shows you a full summary before creating anything, and outputs your permanent Layer 1 Project Instructions at the end.

> Full installation guide with all config details, MCP setup, and step-by-step walkthrough: [How to Install](#how-to-install)

---

## Features

### Theme A: Context Retrieval Architecture

**Just-In-Time Context Retrieval** is the core philosophy. Context is not preloaded. It is retrieved on demand -- at the exact moment the session needs it, in the exact amount the session needs. Nothing loads that is not needed. Nothing that is not loaded costs tokens.

**Multi-layer selective context loading** organizes AI instructions across any number of priority layers. Only the minimum loads on every message. The rest loads once at session start -- or on demand when you call it.

**OS-aware, platform-agnostic operation** means JITCR detects your operating system at session start and adjusts its behavior accordingly. Windows, macOS, Linux -- the protocol adapts to the environment. You do not adapt to the protocol.

---

### Theme B: Session Continuity

**Cross-session context persistence** means no more re-explaining. Every session writes a structured handoff and journal to your local machine. Start a new session after a token limit, a model switch, or a week away -- type `> start` and full context is restored from your own files. Instantly.

**Cross-model portability** means session files are plain text. Any AI model that can read files can pick up where the last session left off. Hand a JITCR handoff to a different model and continue without losing a thing.

**Actual system time retrieval** means JITCR never assumes or hard-codes timestamps. Every session retrieves the real system time before writing any log. Every filename, every journal entry, every handoff reflects when it actually happened.

**Automatic path discovery** means JITCR always reads your project configuration first to get real paths. No hard-coded assumptions. No failures when paths differ across machines or team members.

> See [HOWTO.md -- Session Continuity Workflow](HOWTO.md#7-session-continuity--workflow-guide) for the full workflow and model-switching guide.

---

### Theme C: Skills and Knowledge

**On-demand skills** are reusable instruction sets that live in your project and load only when you call them. Zero tokens until invoked. Automatic unload when the session ends.

**User-defined, fully customizable skills** are yours to build. A skill is not a preset. It is whatever you need it to be -- domain knowledge, a process, a reference, a workflow. You own it. It lives on your machine.

**Project-local RAG** is a local, file-based knowledge retrieval system. No vector database. No cloud. No external service. Your knowledge files live in your project, under your control, and load only when the session needs them.

**Custom input templates** define exactly how you give information to the AI for a specific workflow. Package a structured input format as a skill. Load it when needed. The AI follows your format every time.

**Custom output layout templates** define exactly how the AI structures its response. Package it as a skill, load on demand. Consistent output every time, across every session.

**Custom interaction templates** combine input and output into a single, complete framework for a specific workflow. One skill loads the whole interaction contract -- how you provide information and how the AI responds.

**Three-path intelligent skill creation** meets you where you are. Have content ready? Paste it in. Have an idea? Describe it and the AI generates the skill. Exploring? Describe the problem and get guidance on whether a skill is the right approach.

**Smart skill suggestions** analyze the current session context and suggest skills that would help -- based on what you are actually doing, not a static menu.

**Automatic Layer 2 updates** keep your project configuration current whenever you add, modify, or remove a skill. The skills registry stays accurate without manual maintenance.

> See [HOWTO.md -- Skills System](HOWTO.md#3-skills-system--complete-guide) for the full skills guide, folder structure, and creation walkthrough.
> See [HOWTO.md -- Custom Templates](HOWTO.md#4-custom-templates--complete-guide) for input, output, and interaction template walkthroughs.

---

### Theme D: Validation

**Structural skill validation** checks every skill for the required folder structure, SKILL.md presence, metadata file, and size constraints before the skill is admitted to the project.

**Conceptual skill validation** goes further. The AI reasons against a set of protocol-defined disqualifier rules -- checking whether the proposed skill is appropriate, coherent, and protocol-compliant as a matter of logic, not just structure.

**Configurable multi-mode validation** is JITCR's most novel capability. Any feature can implement any combination of validation behaviors in any configuration:

- **Protocol-governed** -- built-in JITCR structural and conceptual checks
- **No-validation** -- bypass entirely for workflows where speed matters
- **User-defined rule-based** -- you write your own domain-specific rules; the AI validates against them and returns specific failure reports identifying exactly which rule was violated and how
- **Agent-assisted intelligent** -- AI reasoning applied to your rules, catching violations that pattern matching would miss

Any combination. Any configuration. No equivalent exists in any AI protocol or tool as of this writing.

> See [HOWTO.md -- Configurable Multi-Mode Validation](HOWTO.md#5-configurable-multi-mode-validation--reference) for full configuration reference and examples.

---

### Theme E: Guardrails and Safety

**Protocol-level guardrails** are seven universal rules built into JITCR. They apply to every project, every session, every platform. They cannot be disabled:

1. Never delete files without explicit user permission
2. Never modify .env files without explicit user permission
3. Read existing files before overwriting -- preserve content
4. Shell commands always use forward slashes in paths
5. Always read the project guide first at session start
6. Never assume or hard-code timestamps -- always retrieve actual time
7. Never assume project paths -- always read from the project guide

What this looks like in practice: if the AI is about to overwrite a file, it reads the existing content first and tells you what's there before making any change -- it never silently replaces something it hasn't looked at. If you ask it to delete a file, it states what it's about to delete and waits for your explicit "yes," every time, no exceptions.

**Project-level custom guardrails** are defined in your Layer 2 project guide and loaded at `> start`. Active for the entire session. Encode compliance requirements, approval workflows, access controls, domain-specific safety rules -- whatever your project needs.

**Skill-level guardrails** are embedded inside individual skills. They activate only when that skill loads and unload automatically when the session ends. Rules that cost nothing until they are needed.

**Defense-in-depth safety** means all three guardrail layers operate simultaneously and independently. No single layer depends on another.

**Human-in-the-loop approval workflows** mean critical operations require your explicit confirmation before the AI acts. GitHub push at `> end`. Skill deletion at `> skill remove`. No autonomous action on high-stakes operations.

**Full transparency and observability** means you always know what is loaded, what happened, and what is coming next. Session header at `> start`. Handoffs track all decisions and open issues. All logs are plain markdown on your local machine. No hidden state. No cloud.

> See [HOWTO.md -- Guardrails Configuration](HOWTO.md#6-guardrails--configuration-guide) for the full configuration guide across all three levels.

---

### Theme F: Version Control and Backup

**Local git version control** via `> commit` -- always local, never pushes automatically. Use it as a mid-session checkpoint or end-of-session save.

**GitHub push** is opt-in, configured once at install. The AI asks before pushing at `> end`. Every session. No exceptions.

**Project backup** via `> backup` creates a timestamped zip of your project root, on demand, on your machine.

---

### Theme G: Extensibility and Commands

**An extensible self-configuring command framework** means new capabilities automatically generate their own command interfaces. As JITCR grows, new commands appear without manual registration.

**A full session command set** covers everything from session initialization to git operations to skill management. Nine core commands. Ten skill-family commands. All extensible.

---

### Theme H: Installer and Setup

**Automated installation** via a single attached file. Silent system checks first. Five questions. A full confirmation summary before anything is created. Everything is shown before you commit.

**Clear MCP error handling** means if a required tool is missing, the installer tells you exactly what failed, exactly why, and the exact fix for your OS -- including the precise config file path and what to add to it.

**Automatic file downloads** pull the shared protocol files from GitHub during install. You download one file. The installer handles the rest.

**Two-path project structure** keeps JITCR management files completely separate from your project root. Session logs, skills, and configuration stay private. Your project root stays clean.

---

### Theme I: Ecosystem and Future

**Marketplace and ecosystem readiness** means the skills and templates infrastructure is designed to support a future ecosystem of shared, distributable capabilities. The architecture is already in place.

---

## Token Savings and Real Costs

The savings come from when content loads — not just how much there is.

### Token Math

```
WITHOUT JITCR -- full block on every message:
  ~725 tokens x 20 messages = 14,500 tokens

WITH JITCR -- only Layer 1 repeats:
  Layer 1 (~225 tokens) x 20 messages =  4,500 tokens  (every message)
  Layer 2 (~350 tokens) x 1           =    350 tokens  (once at > start)
  Layer 3 (~150 tokens) x 1           =    150 tokens  (once at > start)
  Total                               =  5,000 tokens

SAVED: ~9,500 tokens (~65%) across a 20-message session
```

Layers 2 and 3 are paid once at `> start`. Layer 1 is the only repeating cost. Breakeven is typically after 3-5 messages. After that, every message saves tokens.

> **Note:** These figures are estimates based on generic JITCR templates. Actual savings depend on your project instruction size and session length. Savings grow with session length -- every additional message widens the gap.

### Dollar Cost -- Verified June 2026 Rates

Using Claude Sonnet 4.6 at Anthropic's published rate of **$3.00 per million input tokens**:

```
WITHOUT JITCR:
  14,500 tokens x $3.00 / 1,000,000 = $0.0435 per session

WITH JITCR:
  5,000 tokens x $3.00 / 1,000,000  = $0.015 per session

SAVED PER SESSION: ~$0.029 (~65%)

At 10 sessions/week, 50 weeks/year:
  WITHOUT JITCR: $21.75/year per project
  WITH JITCR:    $7.50/year per project
  ANNUAL SAVING: ~$14.25 per project

At 50 sessions/week (active team, multiple projects):
  WITHOUT JITCR: $108.75/year
  WITH JITCR:    $37.50/year
  ANNUAL SAVING: ~$71.25/year
```

> **Source:** Anthropic API Pricing, June 2026. Claude Sonnet 4.6: $3.00/1M input tokens, $15.00/1M output tokens.
> Verify current rates at https://platform.claude.com/docs/en/about-claude/pricing

### Why Token Savings Also Mean Better Quality

Keeping Layer 1 under 300 tokens keeps every message well inside the range where models perform at their best. The project detail that would have bloated every message is now loaded once, cleanly, at session start.

Research confirms the quality impact. Chroma (2025) tested 18 frontier models and found every one degrades as context grows -- no exceptions. Liu et al. (Stanford/TACL, 2024) documented 30%+ accuracy drops for information buried in the middle of long contexts -- the volume itself impairs reasoning regardless of total context size.

> **Sources:**
> - Chroma Research (2025): Context Rot -- 18 frontier models tested, all degrade: https://www.morphllm.com/context-rot
> - Liu et al. (Stanford / TACL, 2024): Lost in the Middle -- 30%+ accuracy drops on middle-context information

---

## Commands

### Core Commands

| Command | What It Does |
|---|---|
| `> start` | Initialize session: load all layers, check git, display header |
| `> journal` | Write timestamped activity log to `logs/` |
| `> handoff` | Create structured session state snapshot in `logs/` |
| `> save` | Run journal + handoff together |
| `> status` | Show last handoff, last journal, git status |
| `> commit` | Commit project files to local git (never pushes automatically) |
| `> end` | Save + commit locally + optional GitHub push if configured |
| `> backup` | Zip project root with actual timestamp in filename |
| `> ?` | Show all available commands |

### Skills Commands

| Command | What It Does |
|---|---|
| `> skill list` | Show all skills for this project |
| `> skill add` | Create a new skill: interactive, three paths |
| `> skill use <name>` | Load a skill into the current session |
| `> skill info <name>` | Show skill details |
| `> skill enable <name>` | Set skill to auto-load at `> start` |
| `> skill disable <name>` | Return to manual-load only |
| `> skill edit <name>` | Edit skill content or metadata |
| `> skill remove <name>` | Delete a skill (requires confirmation) |
| `> skill validate` | Check all skills for structural and conceptual compliance |
| `> skill suggest` | Smart recommendations based on session context |
| `> ? skill` | Show full skills help |

### `> commit` vs `> end`

| | `> commit` | `> end` |
|---|---|---|
| Saves journal + handoff | No | Yes, always |
| Commits to local git | Yes, always | Yes, always |
| Pushes to GitHub | Optional — asks if configured | Optional — asks if configured |
| When to use | Mid-session checkpoint | End of session |

---

## Platform Compatibility

JITCR works on any AI platform that meets two conditions:

**Condition 1 -- Persistent instructions:** A place to store your project context so the AI knows its role, rules, and configuration across sessions. Claude Desktop Project Instructions, ChatGPT custom instructions, Gemini Gems, Microsoft Copilot notebooks, a system prompt in a locally hosted model, or any equivalent your platform provides.

**Condition 2 -- File access:** The ability to read and write files on your computer or a shared location. This is how JITCR loads Layer 2, writes session logs, manages skills, and restores context at `> start`.

Platforms that meet both conditions today include Claude Desktop, ChatGPT with file tools, Gemini, Microsoft Copilot, locally hosted models via Ollama or Open WebUI, and enterprise AI systems with system prompt and file access support.

**The automated installer is built for Claude Desktop.** It is the reference implementation because Claude Desktop has the most complete file access tooling available today.

**On other platforms,** the protocol, commands, session files, and skills are identical. The setup process differs only in how persistent instructions and file access are configured on that platform. A JITCR project transfers to any compatible platform without changing a single protocol file.

For setup assistance on platforms other than Claude Desktop: https://github.com/intenogent

> See [HOWTO.md -- Platform-Specific Setup](HOWTO.md#10-platform-specific-setup--non-claude-desktop) for step-by-step setup on ChatGPT, Gemini, Copilot, and local models.

---

## How to Install

### What You Need

**1. Claude Desktop**
Download from https://claude.ai/download

**2. filesystem MCP (required)**
Gives Claude Desktop read and write access to your local files. Without this, JITCR cannot function.

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "C:\\Users\\{YourUsername}\\Documents"],
      "type": "stdio"
    }
  }
}
```

Config file location:
- Windows : `%APPDATA%\Claude\claude_desktop_config.json`
- macOS   : `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux   : `~/.config/Claude/claude_desktop_config.json`

After editing, fully quit and reopen Claude Desktop.

**3. shell-command MCP (recommended)**
Allows Claude to run terminal commands. Needed for `> commit`, `> end`, and `> backup`. JITCR installs and runs without it, but git commands will not be available.

Add to `mcpServers` in your config:
- Windows : `"shell-command": { "command": "cmd", "args": ["/c"], "type": "stdio" }`
- macOS   : `"shell-command": { "command": "bash", "args": ["-c"], "type": "stdio" }`
- Linux   : `"shell-command": { "command": "bash", "args": ["-c"], "type": "stdio" }`

**4. Git (optional)**
Only needed if you want version control via `> commit` and `> end`.
Download from https://git-scm.com

---

### How JITCR Organizes Your Files

Every JITCR project has two independent paths:

**Path A: JITCR management** `JITCR_Protocol/{ProjectName}/`
Where JITCR stores its operational files: your Layer 2 project guide, session logs, and skills. Private by design. Never committed to git.

**Path B: Project root** `{ProjectRoot}` -- anywhere on your machine
Where your actual work lives. What git tracks. What `> commit` commits and `> end` can push.

```
JITCR_Protocol/                             <- your local JITCR hub
|
+-- JITCR_Universal_Commands.md             <- shared command engine
+-- JITCR_Skills_Protocol.md               <- skills guide
|
+-- {ProjectName}/
    +-- JITCR_{ProjectName}.md             <- Layer 2 project guide
    +-- logs/
    |   +-- journal_YYYY-MM-DD_HHMM.md
    |   +-- handoff_YYYY-MM-DD_HHMM.md
    +-- skills/
        +-- SKILL_TEMPLATE.md
        +-- {skill-name}/
            +-- SKILL.md
            +-- skill-metadata.json
```

The installer creates all folders and downloads all shared files automatically. Your Layer 2 guide is generated locally from your answers during setup.

---

### Installation: 5 Steps

**Step 1: Create a new project in Claude Desktop.**

Claude Desktop --> Projects --> New Project. Name it the same as your JITCR project name.

---

**Step 2: Paste the installer agent block into Project Instructions.**

Go to Project --> Settings --> Project Instructions. Paste this exactly:

```
## Role
You are the JITCR Protocol Installer agent for this project.

## Your Job
When the user attaches JITCR_Installer_Prompt.md and says see the attached:
- Read the file immediately
- Execute it phase by phase exactly as written
- Start with Phase 1 silently -- no greeting, no questions first
- Do not summarize the file. Do not ask what to do with it. Just run it.

## MCP Tools
Load these at the start:
- tool_search("filesystem read file windows")
- tool_search("shell command execute")
```

---

**Step 3: Download the installer and run it.**

Download `JITCR_Installer_Prompt.md` from this repo. Click the file, click Raw, save the page.

Start a new chat in your project, attach the file, and say:

```
see the attached
```

The installer runs automatically. Silent system check first, then five questions.

> **Note:** Claude may display a brief transparency message before starting — this is normal. It means Claude is confirming you authorized the installation. Just continue when prompted.

---

**Step 4: Follow the five questions.**

- Where to store JITCR files (default or custom path)
- Your project name
- Your project root folder
- One sentence describing what this project is for
- Whether to use git (and optionally GitHub)

Review the Ready to Install summary, type `y`. The installer creates all folders, downloads shared files, and generates your Layer 2 project guide. At the end it outputs your permanent Layer 1 Project Instructions.

---

**Step 5: Replace Project Instructions and test.**

Copy the Layer 1 text from the installer output. Go to Project --> Settings --> Project Instructions. Replace the installer block with the new text.

Start a new chat and type:

```
> start
```

JITCR is running. For a complete walkthrough of what to do next -- including exactly what the session header looks like and how to checkpoint your first session -- see [HOWTO.md -- Your First Session](HOWTO.md#2-your-first-session).

---

### Git and GitHub

`> commit` and `> end` operate on your project root only. Keep JITCR session logs out of git -- they are private operational files.

Recommended `.gitignore` for projects where JITCR files share the project folder:

```
# Whitelist approach for clean public repo
*
!.gitignore
!README.md
!LICENSE
!CONTRIBUTING.md

# JITCR operational files -- never commit
logs/
skills/
JITCR_*.md
```

> See [HOWTO.md -- Git and GitHub Integration](HOWTO.md#8-git-and-github-integration) for the full git workflow guide.

---

## Repo Contents

```
jitcr-protocol/
+-- README.md                   <- You are here
+-- HOWTO.md                    <- Deep reference documentation
+-- JITCR_Installer_Prompt.md   <- Installer -- download manually (Step 3)
+-- JITCR_Universal_Commands.md <- Downloaded automatically by installer
+-- JITCR_Skills_Protocol.md    <- Downloaded automatically by installer
+-- SKILL_TEMPLATE.md           <- Downloaded automatically by installer
+-- CONTRIBUTING.md             <- Contribution guidelines and sign-off process
+-- LICENSE                     <- Apache License 2.0
```

Download manually: `JITCR_Installer_Prompt.md` (Step 3 above)

Downloaded automatically by the installer: `JITCR_Universal_Commands.md`, `JITCR_Skills_Protocol.md`, `SKILL_TEMPLATE.md`

Generated locally by the installer (not downloaded): `JITCR_{ProjectName}.md` -- your personal Layer 2 project guide, built from your answers at setup

---

## Contributing

Contributions are open and welcome -- feedback, bug reports, documentation fixes, skills, and pull requests. Under Apache 2.0 there's no separate agreement to sign, just a `Signed-off-by` line on your commits. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full process including how the sign-off works.

---

## License

Copyright (c) 2026 Arshia (intenogent).

JITCR Protocol is published under the **Apache License 2.0** -- free to use, modify, and distribute, for personal and commercial use alike, with no revenue thresholds and no separate enterprise tier.

See [LICENSE](LICENSE) for full terms.

For questions: https://github.com/intenogent

---

## Author

Built by [@intenogent](https://github.com/intenogent)

For setup assistance on platforms other than Claude Desktop, licensing inquiries, or anything else: https://github.com/intenogent
