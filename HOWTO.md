# HOWTO -- JITCR Protocol Deep Reference

**Protocol Version:** 3.0
**Companion to:** [README.md](README.md)
**Purpose:** Complete operational reference for building, configuring, and running JITCR Protocol projects.

This document is for users who are already running JITCR and want to go deeper. If you are new to JITCR, start with [README.md](README.md).

---

## Table of Contents

1. [Architecture Deep Dive](#1-architecture-deep-dive)
2. [Your First Session](#2-your-first-session)
3. [Skills System: Complete Guide](#3-skills-system-complete-guide)
4. [Custom Templates: Complete Guide](#4-custom-templates-complete-guide)
5. [Configurable Multi-Mode Validation: Reference](#5-configurable-multi-mode-validation-reference)
6. [Guardrails: Configuration Guide](#6-guardrails-configuration-guide)
7. [Session Continuity: Workflow Guide](#7-session-continuity-workflow-guide)
8. [Git and GitHub Integration](#8-git-and-github-integration)
9. [Multi-Project Setup](#9-multi-project-setup)
10. [Platform-Specific Setup: Non-Claude Desktop](#10-platform-specific-setup-non-claude-desktop)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Architecture Deep Dive

### The Three Tiers

JITCR's architecture answers one question: what does the AI actually need right now, and what can stay on disk until it is needed?

The answer is three tiers, each with a different load time.

**Tier 1 -- Project Instructions (every message)**

This is the always-on tier. It lives in your AI platform's persistent instructions -- Claude Desktop Project Instructions, ChatGPT custom instructions, Gemini Gems, or any equivalent. It loads on every single message.

Because it loads every message, it must be minimal. Target: under 300 tokens. What belongs here: the AI's role, the project name, the root path, the seven protocol guardrails, and the `> start` trigger that tells the AI how to initialize.

Nothing that changes session to session belongs in Tier 1. That is what Tiers 2 and 3 are for.

**Tier 2 -- JITCR_{ProjectName}.md (once per session)**

This is the project configuration tier. It lives at `JITCR_Protocol/{ProjectName}/JITCR_{ProjectName}.md` on your machine. It loads once at `> start` via the filesystem MCP.

What belongs here: project purpose, all key file paths, GitHub configuration, project-level custom guardrails, the skills registry, and the command reference. Everything that is stable across sessions but specific to this project.

The AI reads this file once at session start and holds it in context for the rest of the session. It does not reload on every message.

**Tier 3 -- Session logs (conditionally, at session start)**

This is the continuity tier. It lives in `JITCR_Protocol/{ProjectName}/logs/` on your machine. At `> start`, the AI reads the latest handoff file automatically, checks it against actual git history for drift, and flags its age if it's more than 3 days old. If the handoff's Status line says BLOCKED, the AI also reads the 3 journals immediately prior to it for background. Separately, if any journals exist dated after the latest handoff -- meaning `> journal` ran without a matching `> handoff` -- the AI reads those too, so nothing written gets silently skipped.

What belongs here: what was completed last session, what is in progress, what decisions were made, what comes next. The AI enters every session already knowing where you left off.

---

### The Two-Path Structure

Every JITCR project has two independent paths that must never be confused.

**JITCR management folder** -- `JITCR_Protocol/` (private, never committed)

This is where JITCR stores everything it manages: your Tier 2 project guides, session logs, skills, and the shared protocol files (Universal Commands, Skills Protocol). This path is private by design. It never goes into git.

**Project Root** -- `{ProjectRoot}` (your work, version-controlled)

This is where your actual project files live. What git tracks. What `> commit` commits and `> end` can push. This path is entirely separate from the JITCR management folder.

The separation matters because your session logs, skill definitions, and project configuration contain operational detail that does not belong in a public repository. Keep them separate.

---

### What `> start` Does -- Step by Step

When you type `> start`, the AI executes this sequence:

**Step 0 -- Load MCP tools**
The AI loads the filesystem and shell-command MCPs. Without these, no file access or shell commands are possible.

**Step 1 -- Read Tier 1**
The AI already has Tier 1 -- it was in the persistent instructions. It extracts your project name, OS, root path, and the path to your Tier 2 file.

**Step 2 -- Read Tier 2 file (non-negotiable)**
The AI reads `JITCR_{ProjectName}.md` from your JITCR management folder. This is the most important step. Everything else -- paths, guardrails, skills, GitHub config -- comes from this file. The AI never assumes paths. It always reads Tier 2 first.

**Step 3 -- Verify paths**
The AI attempts to list your logs directory to confirm paths are working. If the path fails, it stops and asks you to confirm before proceeding.

**Step 4 -- Retrieve actual system time**
The AI runs a shell command to get the real system time.
- Windows: `powershell -Command "Get-Date -Format 'yyyy-MM-dd HHmm'"`
- macOS/Linux: `date +"%Y-%m-%d %H%M"`

This time is used for all filenames and log headers in the session. It is never assumed or hard-coded.

**Step 5 -- OS detection**
The AI detects whether it is running on Windows, macOS, or Linux and adjusts file path conventions accordingly.

**Step 6 -- Git status check**
The AI runs `git status` on your project root. If git is active, git commands are enabled for the session. If no remote is configured, local commits only. If git is not initialized, the AI notes this silently.

**Step 7 -- Load session context (Tier 3) and verify it**
The AI reads the latest handoff from your logs folder. If git is active, it checks the handoff's claims against `git log -5 --oneline` and `git status --short` and flags any mismatch rather than trusting the file blindly. It also checks the handoff's age against the current time and flags it if more than 3 days old. If the handoff's Status line says BLOCKED, the AI also reads the 3 journals immediately before it for background. Separately -- regardless of Status -- if any journals exist dated after the latest handoff, the AI reads those too, since `> journal` can still run without a matching `> handoff`. Both checks are summarized in one line in the session header (Step 9).

**Step 8 -- Skills summary**
The AI checks the skills registry in your Tier 2 file and notes any available skills for the session.

**Step 9 -- Display session header**
```
+--------------------------------------+
| Project  : {ProjectName}             |
| OS       : {runtime_os}              |
| Root     : {ProjectRoot}             |
| Started  : {actual_system_time}      |
| Git      : {active | inactive}       |
| GitHub   : {push enabled | local}    |
| Loaded   : Tier 2 + Tier 3          |
| Handoff  : {match|DRIFT} · {age}     |
| Skills   : {skill count or none}     |
| Commands : > journal, save, end...   |
+--------------------------------------+
```

**Step 10 -- Begin session**
The AI is ready. Full project context loaded. No re-explaining required.

---

## 2. Your First Session

This section walks through a complete first session from the moment the installer finishes to the moment you close the chat -- one continuous example, with the actual commands and the actual output you will see.

### The Scenario

You just finished the installer for a project called `BlogRewrite`. Your Tier 1 Project Instructions have been replaced with the permanent version. You start a new chat.

---

### Step 1 -- Type `> start`

```
> start
```

This is the very first message in the chat. JITCR has no prior session to read yet, so the handoff and journal lookups will come back empty -- that is expected and normal for a first run.

You will see something close to this:

```
+--------------------------------------+
| Project  : BlogRewrite               |
| OS       : Windows                   |
| Root     : C:/Users/You/Documents/   |
|            BlogRewrite               |
| Started  : 2026-06-29 09:15          |
| Git      : active                    |
| GitHub   : local only                |
| Loaded   : Tier 2 (no Tier 3 yet --  |
|            first session)            |
| Skills   : none                      |
| Commands : > journal, save, end...   |
+--------------------------------------+

This is your first session for BlogRewrite. No prior
handoff exists yet -- that's expected. What would you
like to work on?
```

Notice: no re-explaining required, because there is nothing to re-explain yet. This is the only session where that is true.

---

### Step 2 -- Do the actual work

You ask the AI to do whatever the project is for -- draft an outline, review a file, refactor a script, whatever `BlogRewrite` exists to do. This part is just normal conversation. JITCR is not in the way of your work; it is operating quietly underneath it.

---

### Step 3 -- Checkpoint with `> save` partway through

Forty minutes in, you have made real progress and do not want to lose it if the session ends unexpectedly.

```
> save
```

The AI writes both a journal and a handoff to `logs/`, and confirms:

```
Saved.
journal_2026-06-29_0955.md
handoff_2026-06-29_0955.md
```

You keep working. Nothing about the conversation changes -- `> save` is a quiet background action, not an interruption.

---

### Step 4 -- End the session with `> end`

You are done for the day.

```
> end
```

The AI writes a fresh journal and handoff (capturing everything since your last `> save`), commits the project root to local git, and -- because this project has no GitHub remote configured -- stops there.

```
Session ended.
journal_2026-06-29_1742.md
handoff_2026-06-29_1742.md
Committed to local git: "Session end -- 2026-06-29 17:42"
No GitHub remote configured -- skipping push.
```

If GitHub push had been configured at install, the AI would ask before pushing -- every time, no exceptions.

---

### Step 5 -- Three days later, type `> start` again

New chat, same project.

```
> start
```

This time, Tier 3 has something to read:

```
+--------------------------------------+
| Project  : BlogRewrite               |
| OS       : Windows                   |
| Root     : C:/Users/You/Documents/   |
|            BlogRewrite               |
| Started  : 2026-07-02 08:30          |
| Git      : active                    |
| GitHub   : local only                |
| Loaded   : Tier 2 + Tier 3          |
| Handoff  : match · 3 days old        |
| Skills   : none                      |
| Commands : > journal, save, end...   |
+--------------------------------------+

Picking up from handoff 2026-06-29_1742. Last session
you finished the outline draft and were about to start
the introduction. Ready to continue with the intro, or
is there something else first?
```

That is the entire point of the protocol, demonstrated end to end: one `> start`, no re-explaining, the AI already knows where you left off.

---

### Choosing Between `> journal`, `> save`, and `> end`

| When | Use |
|---|---|
| You want a record of what just happened, but you're continuing the session | `> journal` |
| You want a safety checkpoint before something risky, or before a long break | `> save` |
| You are done for the day | `> end` |

A simple rule: if you are not sure, `> save` is always safe to run. It costs you nothing and protects you from losing progress to a token limit, a crash, or simply forgetting to run `> end` before closing the tab.

---

### When the Handoff Itself Goes Wrong

Everything above assumes the handoff is accurate. Occasionally it will not be -- a session ended mid-thought without `> end`, two sessions overlapped, or you manually edited a log file and introduced a contradiction. JITCR's continuity promise depends on trusting the handoff, so it is worth knowing what happens when that trust is misplaced.

**The handoff contradicts the actual project state.** Example: the handoff says "outline complete, starting the introduction," but the outline file in your project root does not exist, or looks unfinished. The AI does not blindly trust the handoff over what it can observe -- if it reads project files as part of the session and finds something that conflicts with what the handoff claims, it will flag the discrepancy and ask you which is correct rather than silently proceeding on stale information. You can also proactively run `> status` at any point to compare the last handoff against current git history and surface mismatches before they cause confusion.

**Two handoffs exist with conflicting information** (for example, after two people worked on the same project without coordinating, or a session crashed and was manually restarted without `> end` being run first). `> start` reads only the single most recent handoff by filename timestamp -- it does not attempt to merge or reconcile multiple handoffs. If you suspect the most recent one is incomplete or wrong, say so at the start of the session and ask the AI to also read the prior handoff and the journals in between; it will use that additional context instead of relying on the single most recent file alone.

**The handoff looks suspiciously thin or generic** (for example, it does not mention specific files, decisions, or next steps you remember discussing). This usually means `> end` or `> save` was run too early, before the meaningful work of the session happened, or a session ended due to a token limit without a save beforehand. There is no automatic recovery from missing information that was never written down -- this is exactly why frequent `> save` matters (see "Recovering from a Token Limit" below). If you find a handoff is thin, the practical fix is simply to tell the AI what actually happened; it will treat that as authoritative for the rest of the session and the next `> save` or `> end` will capture it correctly going forward.

**General principle:** JITCR's session files are plain text, not a database with referential integrity. The protocol does not silently auto-correct conflicting information on your behalf -- by design, per the guardrail that the AI never assumes when something is unclear. If something in a handoff looks wrong, say so. The AI will treat your correction as more authoritative than a stale file.

---

## 3. Skills System: Complete Guide

### What a Skill Is

A skill is a self-contained instruction set that lives in your project's skills folder and loads into the session only when you call it. It costs zero tokens when not active. It unloads automatically when the session ends.

A skill can contain anything you want the AI to know or do for a specific capability:

- Domain knowledge specific to your project
- Process definitions -- step-by-step workflows the AI follows
- Input formats -- how you structure information when giving it to the AI
- Output templates -- how the AI structures its responses
- Validation rules -- criteria the AI checks before acting
- Behavioral guardrails scoped to that capability

Skills are project-scoped. They belong to one project, reflect what that project actually needs, and live on your machine. You own them.

---

### Skill Folder Structure

```
JITCR_Protocol/{ProjectName}/skills/
  SKILL_TEMPLATE.md              <- reference template, downloaded at install
  {skill-name}/
    SKILL.md                     <- skill definition, instructions, knowledge
    skill-metadata.json          <- auto-managed metadata
```

**SKILL.md** contains the actual skill content -- the instructions, knowledge, or process the AI uses when this skill is active.

**skill-metadata.json** is managed automatically by JITCR. It stores the skill name, description, creation date, version, and auto-load preference. You do not need to edit this manually.

---

### Creating a Skill -- Three Paths

Run `> skill add` and the AI detects which path fits your situation.

**Path 1 -- You have content ready**

You have the skill content written or pasted. The AI validates it against structural and conceptual criteria, then creates the skill folder and files. You review the validation result and confirm.

Best for: domain knowledge documents, process definitions you have already written, reference material you want to make callable on demand.

**Path 2 -- You have an idea but no content**

You describe what you need. The AI drafts the skill content from your description, shows you a preview, and waits for your approval before creating anything. You can request revisions before confirming.

Best for: workflows you understand but have not documented, output formats you want to standardize, interaction patterns you want to formalize.

**Path 3 -- You are exploring**

You describe a problem you are trying to solve. The AI assesses whether a skill is the right approach and, if not, suggests alternatives. If a skill is appropriate, it walks you through Path 2.

Best for: when you know something is not working but are not sure if a skill is the solution.

Example:

```
You:  Every time I ask for a competitive analysis, I get a different
      structure and I have to keep telling you what sections I want.

AI:   That's a good fit for a skill -- specifically an output template.
      Rather than re-explaining the structure each time, we can define
      it once and load it whenever you need a competitive analysis.

      What sections do you want every analysis to include?

You:  Market position, pricing comparison, feature gaps, and a
      recommendation.

AI:   Got it. Here's a draft SKILL.md for a "competitive-analysis-output"
      skill with those four sections in that order. Want me to create
      it, or adjust anything first?
```

If the problem described is not actually a good fit for a skill -- for example, something that changes every single time and has no repeatable shape -- the AI says so directly and suggests handling it as regular conversation instead of creating a skill that would not get reused.

---

### Skill Lifecycle

**Create** -- `> skill add` (one of three paths above)

**Validate** -- happens automatically during creation. Also available on demand:
- `> skill validate` -- checks all project skills
- Structural check: folder present, SKILL.md present, metadata present, size within limits
- Conceptual check: AI reasons against protocol disqualifier rules

**Load** -- `> skill use <name>` -- makes the skill active for the current session

**Auto-load** -- `> skill enable <name>` -- skill loads automatically at every `> start`

**Inspect** -- `> skill info <name>` -- shows skill content, metadata, and status

**Edit** -- `> skill edit <name>` -- modify content or metadata; triggers re-validation

**Disable auto-load** -- `> skill disable <name>` -- returns to manual-load only

**Remove** -- `> skill remove <name>` -- deletes the skill; requires explicit confirmation

---

### Skills Commands Reference

| Command | What It Does |
|---|---|
| `> skill list` | Show all skills -- name, description, status, auto-load setting |
| `> skill add` | Create a new skill -- interactive, detects which path applies |
| `> skill use <name>` | Load a skill into the current session |
| `> skill info <name>` | Show full skill details: content, metadata, validation status |
| `> skill enable <name>` | Set skill to auto-load at every `> start` |
| `> skill disable <name>` | Return skill to manual-load only |
| `> skill edit <name>` | Edit skill content or metadata; triggers re-validation |
| `> skill remove <name>` | Delete a skill permanently -- requires explicit confirmation |
| `> skill validate` | Run structural and conceptual validation on all project skills |
| `> skill suggest` | Analyze current session and suggest relevant skills |
| `> ? skill` | Show full skills help |

---

### Smart Skill Suggestions

`> skill suggest` analyzes the current session -- what you have been working on, what tools you have used, what patterns are emerging -- and recommends skills that would help. It does not show a static menu. It reasons about what your current work actually needs.

Run it when: you sense you are doing something repetitive, when output formats are inconsistent, or when you want to know if an existing skill covers what you are trying to do.

---

### Automatic Tier 2 Updates

When you create, edit, enable, disable, or remove a skill, JITCR automatically updates the skills registry in your Tier 2 file (`JITCR_{ProjectName}.md`). The registry stays accurate without manual maintenance. The next `> start` reflects the current state of your skills.

---

## 4. Custom Templates: Complete Guide

### What Templates Are

Templates are skills that define the shape of an interaction rather than domain knowledge. Where a knowledge skill tells the AI what to know, a template skill tells the AI how to receive information and how to respond.

There are three types:

**Custom input templates** -- define how you give information to the AI for a specific workflow. You define the structure. The AI follows it every time that skill is active.

**Custom output layout templates** -- define how the AI structures its responses. Consistent headings, sections, formats -- every session, every model.

**Custom interaction templates** -- combine both into one skill. One load covers the full input-output contract for a specific workflow.

All three are created with `> skill add`, live in your skills folder, and load on demand.

---

### Building a Custom Input Template

An input template is a SKILL.md that tells the AI: when this skill is active, expect information in this format, and here is what each field means.

Example: you consistently provide bug reports to the AI. Instead of re-explaining the format every session, you build an input template:

```
# Bug Report Input Template

When this skill is active, the user will provide bug reports in this format:

  ENVIRONMENT: [OS, model, version]
  STEPS: [numbered reproduction steps]
  EXPECTED: [what should happen]
  ACTUAL: [what happened instead]
  SEVERITY: [critical / high / medium / low]

Parse each field explicitly before responding. If any field is missing,
ask for it before proceeding. Do not infer missing fields.
```

Load it with `> skill use bug-report-input`. Every bug report you provide that session follows the contract. No re-explaining.

---

### Building a Custom Output Layout Template

An output template is a SKILL.md that tells the AI: when this skill is active, structure every response in this format.

Example: you want every code review response to follow a consistent structure:

```
# Code Review Output Template

When this skill is active, structure every code review response as follows:

  ## Summary
  One paragraph. What the code does and overall assessment.

  ## Issues
  Numbered list. Each issue: [severity] description + specific line reference.

  ## Suggestions
  Numbered list. Each suggestion: what to change and why.

  ## Verdict
  One line: APPROVED / NEEDS CHANGES / MAJOR REVISION REQUIRED

Do not add sections not listed above. Do not omit sections even if empty.
```

Load it with `> skill use code-review-output`. Every code review that session follows the same structure.

---

### Building a Custom Interaction Template

An interaction template combines input and output into one skill. Use this when a workflow has both a specific way you provide information and a specific way you expect the AI to respond.

Example: weekly status updates -- you provide information in a specific format and want a specific report back:

```
# Weekly Status Interaction Template

## Input Format
When this skill is active, the user provides status updates as:

  COMPLETED: [bullet list of what was done]
  IN PROGRESS: [bullet list with % complete]
  BLOCKED: [item -- reason -- what is needed to unblock]
  NEXT WEEK: [planned items]

## Output Format
Respond with:

  ## Status Report -- [date]

  ### Completed
  [formatted list from COMPLETED field]

  ### In Progress
  [formatted list with completion percentages]

  ### Blockers
  [table: Item | Reason | Unblock Requirement]

  ### Next Week
  [formatted list from NEXT WEEK field]

  ### Health
  [one-line assessment: GREEN / YELLOW / RED + one sentence why]
```

One skill. One load. Full interaction contract.

---

### When to Use Each Type

| Use | Type |
|---|---|
| You provide structured information repeatedly | Input template |
| You want consistent AI response format | Output template |
| Both apply to the same workflow | Interaction template |
| The workflow is one-sided (you ask, AI answers freely) | Neither -- use a knowledge skill |

---

### When NOT to Create a Template

A template earns its keep when the same shape repeats across many sessions. It is not worth building when:

- You only need the format once. Just describe what you want in the conversation -- a template you will use a single time costs more setup effort than it saves.
- The output genuinely needs to vary every time. If no two responses should look alike, a rigid template will fight against what you actually need.
- You are still figuring out what the right format even is. Iterate in plain conversation first. Turn it into a template once the shape has stabilized, not before.

A good signal that a template is worth building: you have caught yourself typing the same formatting instructions for the third time.

---

## 5. Configurable Multi-Mode Validation: Reference

### What It Is

Most AI tools have one approach to validation: a fixed set of structural checks. Pass or fail. No user control.

JITCR's configurable multi-mode validation lets any feature implement any combination of validation behaviors in any configuration. This is JITCR's most novel architectural element -- no equivalent exists in any competing AI protocol or tool as of this writing.

---

### The Four Modes

**Mode 1 -- Protocol-governed validation**

The built-in JITCR validation rules apply. For skills, this means:
- Structural check: skill folder present, SKILL.md present, skill-metadata.json present, file sizes within limits
- Conceptual check: AI reasons against protocol-defined disqualifier rules to assess whether the skill is appropriate, coherent, and protocol-compliant

This mode is always available. It is what `> skill validate` runs by default.

**Mode 2 -- No-validation execution**

Validation is bypassed entirely. The feature executes without checks. Use this for workflows where speed matters more than compliance checking -- rapid iteration, exploratory work, or situations where the content is already verified by other means.

**Mode 3 -- User-defined rule-based validation**

This is where JITCR becomes uniquely powerful. You write your own domain-specific validation rules. The AI validates inputs against them and returns structured failure reports.

A failure report identifies:
- Which specific rule was violated
- What the violating content is
- Why it fails the rule
- What would need to change for it to pass

This is not a generic pass/fail. It is a specific, actionable diagnostic against your own rules.

**Mode 4 -- Agent-assisted intelligent validation**

The AI applies reasoning -- not just pattern matching -- to validate against your rules. It catches violations that string matching or structural checks would miss: logical inconsistencies, implicit contradictions, contextual rule violations.

Concrete example of the difference: suppose one of your rules is "every claim in the conclusion must already appear in the body." A pattern-matching check can only catch this if the conclusion repeats the exact wording from the body -- it has no way to know that "revenue grew significantly" in the conclusion and "Q3 revenue increased 4% over Q2" in the body are or are not the same claim. Mode 4 reasons about the actual meaning: it recognizes that "grew significantly" may not be supported by a 4% increase, flags the mismatch, and explains why -- something no string or structure check could ever catch, because the violation is in the logic, not the text.

Combine with Mode 3 for the most powerful validation available: your rules, reasoned against by the AI, with structured failure reports.

---

### How to Configure Validation in Your Project

Validation mode is configured per-feature in your Tier 2 project guide or in a skill's SKILL.md. You specify which modes apply and in what order.

Example: a skill that validates client deliverables against your firm's style guide

```
## Validation Configuration

Mode: user-defined + agent-assisted (Modes 3 + 4)

Rules:
1. No passive voice in executive summary sections
2. All numerical claims must include a source citation
3. Section headings must match the approved template exactly
4. Conclusions must not introduce new information not present in the body
5. Client name must appear in its approved form: [Client Legal Name]

On validation failure:
- Return a structured failure report
- List each violated rule by number
- Quote the specific violating text
- Explain why it fails
- Do not auto-correct -- present for human review
```

Load the skill. Run validation. Get a specific, actionable report against your rules.

---

### Writing Effective Validation Rules

Rules work best when they are:

**Specific** -- "No passive voice in executive summary sections" is enforceable. "Good writing style" is not.

**Binary** -- the rule either passes or fails for a given input. Avoid rules with gradations (poor/acceptable/good) -- use separate rules for each threshold instead.

**Scoped** -- state where the rule applies. A rule that applies to the whole document is harder to enforce than one scoped to a specific section or element type.

**Independent** -- each rule should stand alone. Avoid rules that require other rules to be evaluated first.

---

## 6. Guardrails: Configuration Guide

### The Three Guardrail Layers

JITCR implements guardrails as three independent layers. Each layer operates regardless of whether the others are present. Together they give you defense-in-depth safety without any single point of failure.

---

### Protocol-Level Guardrails (Non-Negotiable)

Seven universal rules built into JITCR. They apply to every project, every session, every platform. They cannot be disabled by any project configuration, any skill, or any user instruction.

| Rule | What It Prevents |
|---|---|
| Never delete files without explicit user permission | Accidental or AI-initiated file deletion |
| Never modify .env files without explicit user permission | Accidental credential or config corruption |
| Read existing files before overwriting -- preserve content | Silent data loss during file writes |
| Shell commands always use forward slashes in paths | Path failures on Windows from backslash issues |
| Always read the project guide first at session start | AI using hardcoded path assumptions that fail |
| Never assume or hard-code timestamps -- always retrieve actual time | Log files with wrong timestamps, debugging confusion |
| Never assume project paths -- always read from the project guide | Path failures across machines, users, or OS environments |

These are the baseline safety floor. Every JITCR project gets them automatically.

**Why the forward-slash guardrail matters:** on Windows, the `filesystem` tool accepts both `\` and `/`, but the `shell-command` tool does not reliably accept `\` -- some implementations strip single backslashes during their own internal parsing, before the path ever reaches PowerShell or cmd. A path like `C:\Users\You\Project` can silently become `C:UsersYouProject` and get written to the wrong location with a mangled name, instead of raising an error. Forward slash works correctly in both tools, on every OS, with no exceptions found in testing. This is why JITCR stores and uses `{ProjectRoot}` and `{HubRoot}` as forward-slash from the moment they're captured (at install, or whenever you provide a custom path) -- not as a style choice, but because it's the one format both tools can be trusted with.

---

### Project-Level Guardrails (Per-Project, Fully Customizable)

Defined in your Tier 2 file (`JITCR_{ProjectName}.md`) under a `## Project Guardrails` section. Loaded at `> start`. Active for the entire session.

This is where you encode your project's specific rules.

**How to add project guardrails:**

Open your `JITCR_{ProjectName}.md` file and add or edit the `## Project Guardrails` section:

```
## Project Guardrails
- Never commit files in the /client-data/ folder to git
- Always request confirmation before running any database migration
- Do not generate or suggest SQL DELETE statements without explicit instruction
- Output files must follow the naming convention: YYYY-MM-DD_{type}_{version}.ext
- API keys found in any file must be flagged immediately and not logged
```

The AI reads these at `> start` and applies them for the entire session. Edit them as your project's requirements evolve.

**What belongs in project guardrails:**

- Data handling and compliance requirements (what data can go where)
- Approval workflows (what requires your confirmation before the AI acts)
- Access controls (which files, folders, systems are off-limits)
- Output constraints (format requirements, naming conventions, disclosure rules)
- Domain-specific safety rules (what the AI may and may not do for this project)

---

### Skill-Level Guardrails (On-Demand, Scoped)

Behavioral rules embedded directly in a skill's SKILL.md. They activate only when that skill is loaded and unload automatically when the session ends.

Use skill guardrails for rules that only apply when a specific capability is active. They cost zero tokens when the skill is not loaded.

Example -- a skill for working with production database schemas:

```
## Skill Guardrails

When this skill is active:
- Never suggest DROP, DELETE, or TRUNCATE statements without explicit user request
- Always present schema changes as a dry-run preview before suggesting execution
- Flag any change that would affect more than 1,000 rows
- Do not proceed with any destructive operation until the user types CONFIRM
```

These rules are tightly scoped to the specific capability. They do not pollute the session with rules that do not apply when you are doing other work.

---

### Defense-in-Depth -- How the Layers Work Together

All three layers are active simultaneously. No layer depends on another.

If a project-level guardrail is absent, protocol-level guardrails still run. If a skill with skill-level guardrails is not loaded, the session still has protocol-level and project-level guardrails. If someone bypasses a skill, the project-level rules still apply.

The layers are additive. More layers active means more specific protection, not more dependency.

---

### Human-in-the-Loop Approval Points

Beyond the guardrail layers, JITCR builds explicit approval gates into high-stakes operations:

| Operation | What Triggers the Gate |
|---|---|
| `> end` -- GitHub push | AI asks before every push, even if GitHub is configured |
| `> skill remove` | AI requires explicit confirmation before deleting a skill |
| Git initialization | Your choice at install time -- AI never initializes without being asked |
| File overwrites | Protocol-level guardrail: AI reads existing file before overwriting |

These gates are built into the command logic. They do not depend on project or skill guardrails being configured.

---

## 7. Session Continuity: Workflow Guide

### The Two Session Files

Every JITCR session writes two files to your local machine under `JITCR_Protocol/{ProjectName}/logs/`.

**Journal** -- `journal_YYYY-MM-DD_HHMM.md`

What happened this session. Work log, decisions made, files created or modified, issues encountered, approaches tried -- including a required Failed Approaches note (what was tried and abandoned, so a future session doesn't repeat it; "None this session" if nothing applies). Written with `> journal` or `> save`. Provides the detailed record for future sessions to reference. Journal is the only place session detail lives -- handoff never repeats it.

**Handoff** -- `handoff_YYYY-MM-DD_HHMM.md`

Current state snapshot only -- a required Status line, open issues, what comes next, blockers, and any critical context the next session needs immediately. Written with `> handoff` or `> save`. This is what `> start` reads automatically -- and now verifies automatically too: `> start` checks the handoff against real git history for drift and flags its age if stale, rather than trusting it blindly.

The handoff is the most important file. Write it carefully at the end of every session. A good handoff means the next session -- or the next model -- picks up without re-explaining anything.

---

### The Command Workflow

| Situation | Command | What It Does |
|---|---|---|
| Mid-session checkpoint | `> journal` | Writes current activity log only |
| Snapshot current project state | `> handoff` | Writes structured state snapshot only |
| Quick save before a risky operation | `> save` | Writes journal + handoff |
| End of session | `> end` | Writes journal + handoff + commits + optional push |
| Check where things stand | `> status` | Shows last handoff status, last journal, git status |
| Version control checkpoint | `> commit` | Commits to local git, with optional GitHub push |

**Use `> save` frequently.** Token limits hit without warning. A recent `> save` means the next session starts from a current handoff, not a stale one from two hours ago.

---

### Recovering from a Token Limit

Token limit hits mid-session:

1. Start a new chat in the same project
2. Type `> start`
3. The AI reads the latest handoff automatically
4. Session context is restored

If you did not `> save` before the token limit hit, the handoff reflects the state at your last save. Work done after the last save may need to be re-explained. This is why frequent `> save` matters.

---

### Switching Models Mid-Project

JITCR session files are plain text markdown. Any model that can read files can use them.

To hand off to a different model:

1. End the current session with `> end` (or at minimum `> save`)
2. Set up the new model with JITCR Tier 1 instructions for this project
3. Ensure the new model has filesystem access to your JITCR management folder
4. Start a new session and type `> start`

The new model reads the same handoff, the same Tier 2 guide, and the same session logs. It enters the session with full context. No re-explaining required.

---

### Working Across Machines

Session files are plain markdown files on your machine. To continue work on a different machine:

1. Copy your `JITCR_Protocol/` folder to the new machine (or sync via a tool of your choice)
2. Ensure JITCR is configured on the new machine (MCP tools, project instructions)
3. Type `> start` -- the AI reads the handoff and Tier 2 from the new location

The session continues from where you left off.

---

### Collaborating with Another Person

A teammate can pick up your JITCR project by:

1. Getting access to your `JITCR_Protocol/{ProjectName}/` folder (share the folder, or copy it)
2. Having their own JITCR setup (MCP tools configured, project instructions set)
3. Typing `> start` in their own session

They enter with full context from your latest handoff. They can continue independently and their session writes its own handoff files. Merge decisions are yours -- JITCR does not enforce a single-writer model.

---

## 8. Git and GitHub Integration

### How Git Works in JITCR

JITCR's git integration is intentionally conservative. The AI never pushes automatically. It never commits without being asked. It asks before pushing to GitHub every time.

**`> commit`** -- commits your project root to local git, with optional GitHub push. Does not touch the JITCR management folder. Use it as a mid-session checkpoint.

**`> end`** -- runs `> save` first (journal + handoff), then commits to local git, then -- and only if GitHub push is configured and you type yes -- pushes to the remote.

The commit message can be customized: `> commit your message here`.

---

### What Gets Committed

`> commit` and `> end` operate on your **project root** (`{ProjectRoot}`), not on the JITCR management folder. What gets included in the commit is controlled by the `.gitignore` in your project root.

JITCR management folder files (session logs, skills, Tier 2 guide) should never be committed. They are private operational files.

If your JITCR management folder is inside your project root (not recommended but supported), your `.gitignore` must explicitly exclude JITCR files:

```
# Exclude JITCR operational files
JITCR_Protocol/
JITCR_*.md
logs/
skills/
```

If your project root and JITCR management folder are fully separate paths (recommended), no `.gitignore` entry is needed for JITCR files -- they are not in the git tree at all.

---

### Recommended .gitignore for Public Repos

For projects where you want fine control over what goes public, use a whitelist approach:

```
# Whitelist -- only explicitly named files are committed
*

# Files to include
!.gitignore
!README.md
!LICENSE
!CONTRIBUTING.md
!HOWTO.md
!JITCR_Installer_Prompt.md
!JITCR_Universal_Commands.md
!JITCR_Universal_Skills_Protocol.md
!SKILL_TEMPLATE.md
!.github/
!.github/**

# Add your project-specific files here
# !src/
# !docs/
```

This approach means nothing goes to GitHub by accident. You explicitly opt files in.

---

### Setting Up GitHub Push

GitHub push is configured at install time (Question 4 in the installer). If you skipped it at install and want to add it later:

1. Open your `JITCR_{ProjectName}.md` file
2. Update the `GitHub Push` field to `yes`
3. Update the `GitHub Remote` field to your repo URL
4. Run: `git -C "{ProjectRoot}" remote add origin {your-repo-url}`

At the next `> end`, the AI will ask whether to push.

---

### `> backup` -- Local Project Backup

`> backup` creates a timestamped zip of your entire project root on your local machine. It does not touch the JITCR management folder. It does not push anywhere.

Filename format: `{ProjectName}_backup_YYYY-MM-DD_HHMM.zip`

The timestamp is actual system time retrieved at the moment you run the command. Use `> backup` before major changes, before a risky refactor, or any time you want a local snapshot independent of git.

---

### New to Git?

JITCR's git integration assumes basic familiarity with git concepts (commits, remotes, `.gitignore`). If you are new to git, the official documentation at https://git-scm.com/doc covers the fundamentals well -- start with "what is a commit" and "what is a remote" before configuring GitHub push. JITCR's commands wrap standard git operations; nothing here requires anything beyond what that documentation covers.

---

## 9. Multi-Project Setup

### How Multiple Projects Share One JITCR Management Folder

Your JITCR management folder (`JITCR_Protocol/`) holds all your projects. Each project gets its own subfolder:

```
JITCR_Protocol/
|
+-- JITCR_Universal_Commands.md            <- shared across all projects
+-- JITCR_Universal_Skills_Protocol.md     <- shared across all projects
|
+-- ProjectAlpha/
|   +-- JITCR_ProjectAlpha.md
|   +-- logs/
|   +-- skills/
|
+-- ProjectBeta/
|   +-- JITCR_ProjectBeta.md
|   +-- logs/
|   +-- skills/
|
+-- ClientWork/
    +-- JITCR_ClientWork.md
    +-- logs/
    +-- skills/
```

The shared protocol files (`JITCR_Universal_Commands.md`, `JITCR_Universal_Skills_Protocol.md`) are downloaded once at first install and shared across all projects. You do not need multiple copies.

---

### Creating a Second Project

Run the installer again in a new Claude Desktop project:

1. Claude Desktop --> Projects --> New Project
2. Download `JITCR_Installer_Prompt.md` from the repo. On GitHub, click the file name, then click the Download button in the top right of the file view.
3. Open a new chat in the project, attach the file, and paste this into the chat box — then submit:

```
I want to install JITCR Protocol on my computer.
The installer file JITCR_Installer_Prompt.md is attached.

Please read it and run the installation exactly as written.
I explicitly authorize you to:
- Run silent system checks (OS, MCP tools, git)
- Ask me questions to gather my project details
- Create folders and files on my computer at paths I confirm
- Download the required JITCR files from GitHub

Load these MCP tools first:
- tool_search("filesystem read file windows")
- tool_search("shell command execute")

Then begin Phase 1 system checks now.
```
4. At Question 0, choose the same JITCR management root you used before
5. At Question 1, give the new project a different name
6. The installer creates the new project subfolder without touching existing projects

Each project gets its own Tier 2 guide, its own logs folder, and its own skills folder. They share the protocol files.

---

### Managing Skills Across Projects

Skills are project-scoped. A skill created in `ProjectAlpha` does not appear in `ProjectBeta`.

If you want to reuse a skill across projects, copy the skill folder manually:

1. Locate the skill at `JITCR_Protocol/ProjectAlpha/skills/{skill-name}/`
2. Copy the entire folder to `JITCR_Protocol/ProjectBeta/skills/{skill-name}/`
3. Run `> skill validate` in the new project to confirm the skill is valid
4. JITCR will detect the new skill and update the Tier 2 skills registry automatically

---

### Naming Conventions for Multiple Projects

Use project names that are unambiguous and filesystem-safe:

- No spaces (use hyphens or CamelCase)
- Descriptive enough to identify at a glance
- Consistent with how you name the corresponding Claude Desktop project

Examples: `ClientABC-Web`, `InternalTools`, `ResearchQ3`, `PersonalSite`

---

## 10. Platform-Specific Setup: Non-Claude Desktop

JITCR's protocol, commands, session files, and skills are identical across all platforms. What changes is how you configure persistent instructions and file access on each platform.

The automated installer is built for Claude Desktop. On other platforms, follow the manual setup below.

**A note on these steps:** the guidance below is best-effort, based on each platform's general capabilities -- it has not been verified through hands-on use of ChatGPT, Gemini, Copilot, or local model tooling. If you have direct experience with any of these platforms and can confirm, correct, or improve these steps, a pull request is very welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

### ChatGPT (with file tools)

**Persistent instructions:** ChatGPT custom instructions (Settings --> Personalization --> Custom Instructions). Paste your Tier 1 JITCR Project Instructions there.

**File access:** ChatGPT's file upload and code interpreter tools provide file access. For full JITCR functionality, you need a GPT or workflow that can read and write files on your machine. The web interface's file upload is read-only and session-scoped -- not sufficient for full JITCR session continuity. A ChatGPT Desktop integration with local file access (where available) or a custom GPT with file tool access is required.

**Manual Tier 2 loading:** Without filesystem MCP equivalents, you may need to manually paste your `JITCR_{ProjectName}.md` content at the start of each session rather than having the AI read it from disk.

---

### Gemini (Gems)

**Persistent instructions:** Create a Gem (Gemini Advanced --> Gems --> New Gem). Paste your Tier 1 Project Instructions as the Gem's instructions.

**File access:** Gemini's file access capabilities vary by interface. Gemini Advanced with Google Drive integration can read Drive files. For full JITCR functionality, your session logs and Tier 2 guide need to be accessible via Drive or another file mechanism the Gem can reach.

**Recommended approach:** Store your `JITCR_{ProjectName}.md` and session logs in a Google Drive folder. Configure the Gem to read from that folder at session start.

---

### Microsoft Copilot (Notebooks)

**Persistent instructions:** Copilot Notebooks provide persistent context. Paste your Tier 1 Project Instructions into the notebook context.

**File access:** Microsoft Copilot with SharePoint or OneDrive integration can access files. Store your JITCR management folder in OneDrive and configure Copilot to read from it.

---

### Local Models (Ollama, Open WebUI, LM Studio)

**Persistent instructions:** Most local model interfaces support a system prompt. Paste your Tier 1 Project Instructions as the system prompt for your session.

**File access:** Local models typically require a tool layer (LangChain, LlamaIndex, a custom script, or Open WebUI's document feature) to provide file read/write access. Configure your tool layer to allow reading from your JITCR management folder path and writing to your logs folder.

**Session continuity:** With file access configured, `> start` can read your Tier 2 guide and session logs exactly as it does on Claude Desktop. Without file access, you need to manually provide the handoff content at session start.

---

### Any Other Platform

JITCR works on any platform that provides:

1. A place to store persistent instructions across sessions
2. A way for the AI to read and write files on your machine or a shared location

If both conditions are met, the JITCR protocol runs without modification. Adapt the file access method to whatever your platform provides.

For setup assistance on any platform: https://github.com/intenogent

---

## 11. Troubleshooting

### filesystem MCP not loading

**Symptom:** `> start` fails to read Tier 2. AI reports it cannot access files.

**Cause:** The filesystem MCP is not configured, not active, or does not have permission to access your JITCR management folder path.

**Fix:**

1. Open your Claude Desktop config file:
   - Windows : `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS   : `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux   : `~/.config/Claude/claude_desktop_config.json`

2. Confirm the filesystem MCP entry is present and the `args` path includes your Documents folder (or wherever your JITCR management folder lives).

3. Fully quit Claude Desktop (not just close the window -- quit from the menu or system tray) and reopen it.

4. Start a new chat and type `> start` again.

---

### shell-command MCP not available -- git commands failing

**Symptom:** `> commit` or `> end` fails. AI reports shell-command MCP is not available.

**Fix:**

Add the shell-command MCP to your Claude Desktop config:

```json
"shell-command": {
  "command": "cmd",
  "args": ["/c"],
  "type": "stdio"
}
```

(Replace `cmd` with `bash` and `/c` with `-c` on macOS/Linux.)

Fully quit and reopen Claude Desktop. Git commands will be available in the next session.

JITCR runs without shell-command MCP -- you just lose `> commit`, `> end` git operations, `> backup`, and actual system time retrieval.

---

### Paths failing on a different machine

**Symptom:** `> start` cannot find Tier 2 or logs. AI reports path not found.

**Cause:** The paths in Tier 1 Project Instructions or in the Tier 2 file point to a location that does not exist on this machine.

**Fix:**

1. Confirm the JITCR management folder exists on this machine at the expected path.
2. If the JITCR management folder is in a different location, update the Tier 2 path in Tier 1 Project Instructions to point to the correct location on this machine.
3. Alternatively, copy the JITCR management folder to the same path as the original machine.

If you are moving between machines regularly, consider storing your JITCR management folder in a location that syncs (cloud storage, network drive) and ensure the sync path is consistent across machines.

---

### `> start` not finding session logs

**Symptom:** `> start` completes but reports no handoff found or shows no session history.

**Cause:** The logs folder is empty (first session), or the AI is looking in the wrong path.

**Fix:**

1. If this is the first session, the empty logs folder is expected. Proceed normally.
2. If logs exist but are not found, confirm the `Session Logs` path in your Tier 2 file points to the correct folder.
3. Run `> status` -- it will attempt to find and display the latest handoff. If it also fails, the path in Tier 2 needs correction.

---

### Handoff seems wrong, stale, or contradicts the project

**Symptom:** `> start` reads a handoff, but what it describes does not match the actual state of your files -- or two sessions seem to have overlapping, contradictory histories.

**Cause:** A previous session ended without `> end` or `> save` (so no handoff was written for that work), two people or two parallel sessions worked on the project without coordinating, or a log file was manually edited and introduced an inconsistency.

**Fix:**

1. Run `> status` to compare the latest handoff against current git history -- this often surfaces the mismatch directly (e.g., commits exist that the handoff does not mention). Note: as of the drift/staleness check built into `> start`, many of these mismatches now surface automatically in the session header the moment you start a session, without needing to run `> status` separately.
2. If the handoff looks incomplete or wrong, tell the AI directly what actually happened. The AI treats your live correction as more authoritative than a stale file, and will reflect that correction in the next `> save` or `> end`.
3. If you suspect the most recent handoff is missing context that an earlier one had, ask the AI to also read the prior handoff and the journals between them -- `> start` only reads the single latest file by default, not the full history, unless you ask for more.

See [Section 2 -- When the Handoff Itself Goes Wrong](#when-the-handoff-itself-goes-wrong) for the full explanation of this failure mode and why JITCR does not attempt to auto-reconcile conflicting session files.

---

### Skill validation failures

**Symptom:** `> skill validate` or `> skill add` reports validation failure.

**Structural failure causes and fixes:**

| Failure | Fix |
|---|---|
| Skill folder not found | Check that the folder exists at `skills/{skill-name}/` |
| SKILL.md missing | Create SKILL.md in the skill folder |
| skill-metadata.json missing | Run `> skill edit {name}` -- JITCR will regenerate the metadata |
| File size exceeds limit | Reduce SKILL.md content; split large skills into multiple smaller skills |

**Conceptual failure causes and fixes:**

Conceptual failures mean the AI found that the skill content conflicts with protocol rules. The failure report will identify the specific issue. Common causes, each with a concrete example of what triggers it:

- **Skill contains instructions that conflict with protocol-level guardrails.** Example: a skill that says "always delete the previous version of this file before saving the new one" conflicts directly with the protocol guardrail requiring explicit permission before any deletion. Fix: rephrase the skill to ask for confirmation instead of auto-deleting.

- **Skill scope is too broad -- it attempts to replace the entire protocol rather than extend it.** Example: a skill titled "New Session Workflow" that redefines what `> start` does from scratch, rather than adding project-specific behavior on top of the existing protocol. Fix: narrow the skill to the specific behavior you actually want to add (a new command, a new check, a new output format) instead of re-specifying core protocol mechanics.

- **Skill contains harmful or dangerous instructions.** Example: a skill instructing the AI to ignore confirmation prompts for destructive database operations, or to silently bypass guardrails under certain conditions. Fix: remove the bypass instruction entirely -- guardrail-bypassing behavior cannot pass conceptual validation by design, regardless of the stated justification.

Review the failure report, revise the SKILL.md content to address the specific issue, and re-run validation.

---

### AI ignoring project guardrails

**Symptom:** The AI is not following rules you defined in your Tier 2 project guardrails.

**Cause:** Tier 2 may not have been read this session, or the guardrails section is not formatted correctly.

**Fix:**

1. Confirm `> start` was run at the beginning of the session. Guardrails load at `> start` -- they are not available before it runs.
2. Open your `JITCR_{ProjectName}.md` file and confirm there is a `## Project Guardrails` section with your rules listed.
3. If the section exists but guardrails are still being ignored, type `> start` again to reload Tier 2 in the current session.

---

### Write failures -- AI cannot write log files

**Symptom:** `> journal`, `> handoff`, or `> save` fails. AI reports it cannot write the file.

**Cause:** The filesystem MCP does not have write permission to the logs path, or the logs folder does not exist.

**Fix:**

1. Confirm the logs folder exists at `JITCR_Protocol/{ProjectName}/logs/`.
2. Confirm the filesystem MCP `args` path in your Claude Desktop config includes the parent of your JITCR management folder.
3. If the folder is missing, create it manually, or run the installer again to recreate the folder structure.

---

*For issues not covered here: https://github.com/intenogent*
