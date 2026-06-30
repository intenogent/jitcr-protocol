# JITCR Skills Protocol
**Protocol Version:** 1.0
**Author:** LaserWhiz
**Created:** 2026-06-26
**Purpose:** Comprehensive guide for project-scoped skills in JITCR Protocol.
           Defines skill architecture, creation, loading, and management.

> ⚠️ This is a CORE JITCR capability. Individual projects reference this guide.
> Edit ONLY when upgrading the Skills Protocol itself.

---

## What Are JITCR Skills?

**Skills** are **project-scoped, reusable AI instructions** that live in your project and load on-demand.

A skill:
- ✅ Contains structured knowledge or repeatable process
- ✅ Can be invoked by name within a session
- ✅ Is reusable across multiple sessions
- ✅ Loads only when needed (saves tokens)
- ✅ Is packaged independently from project code
- ✅ Has standard structure (folder + SKILL.md + metadata)

**NOT a skill:**
- ❌ One-time solution for specific session
- ❌ Code that belongs in your project files
- ❌ Session-specific context or workaround
- ❌ Content too project-specific to reuse

---

## Skills Architecture

### Folder Structure

```
{ProjectName}\
├── JITCR_{ProjectName}.md                (Tier 2 guide)
├── logs\                                  (Session logs)
└── skills\                                (NEW: Project skills)
    ├── SKILL_TEMPLATE.md                  (Reference template)
    ├── skill-name-1\                      (User-created skill)
    │   ├── SKILL.md                       (Skill definition)
    │   ├── skill-metadata.json            (Auto-managed metadata)
    │   └── [supporting files - optional]
    ├── skill-name-2\
    │   ├── SKILL.md
    │   ├── skill-metadata.json
    │   └── [supporting files - optional]
    └── skill-name-3\
        ├── SKILL.md
        ├── skill-metadata.json
        └── [supporting files - optional]
```

### Skill File Structure

Every skill folder must contain:

#### **SKILL.md** (Required)
The main skill definition file containing:
- Skill name and description
- Purpose and scope
- Usage instructions
- Skill content (instructions, process, knowledge base, etc.)

```markdown
# Skill: [Skill Name]

**Purpose:** [One-line description]

**Scope:** [single-task / multi-step-workflow / utility]

**Usage:** 
[How to invoke this skill in a session]

---

## Skill Content

[The actual skill instructions/knowledge/process goes here]
```

#### **skill-metadata.json** (Auto-managed)
Created and managed automatically by JITCR. Contains:
```json
{
  "name": "skill-name",
  "description": "One-line description",
  "scope": "single-task | multi-step | utility",
  "created": "2026-06-26",
  "enabled": true,
  "auto_load": true,
  "version": "1.0",
  "last_modified": "2026-06-26",
  "size_tokens": 500,
  "dependencies": []
}
```

#### **Supporting Files** (Optional)
- Code files (if skill includes code examples)
- Data files (if skill needs reference data)
- Templates (if skill includes templates)
- Examples (if skill needs usage examples)

---

## Skills Commands

All skills commands are available via the `> skill` family of commands:

### Discovery Commands

#### `> skill list`
**Purpose:** Show all skills in this project

**Output:**
```
Project Skills — {ProjectName}

Enabled (will load on > start):
  ✓ github-automation  — Automate GitHub workflows
  ✓ code-review        — Code quality analysis  
  ✓ documentation      — Generate documentation

Disabled (available on-demand):
  ✗ research-tools     — Research and analysis
  ✗ testing-framework  — QA and testing

3 enabled, 2 disabled, 5 total
Use: > skill use <name>    or    > skill info <name>
```

#### `> skill info <name>`
**Purpose:** Show details about a specific skill

**Output:**
```
Skill: github-automation

Description:    Automate GitHub workflows
Scope:         Multi-step workflow
Status:        Enabled
Auto-load:     Yes
Created:       2026-06-20
Last modified: 2026-06-25
Size:          ~2,500 tokens
Path:          skills\github-automation\SKILL.md

Usage: > skill use github-automation
       (loads into this session only)

To edit: > skill edit github-automation
To disable: > skill disable github-automation
```

### Creation Commands

#### `> skill add`
**Purpose:** Create a new skill (interactive, three-path system)

**Flow:**
```
User types: > skill add

Detects user intent:
  PATH 1: "I have skill content to paste"
  PATH 2: "I have an idea but no content"
  PATH 3: "I'm not sure if this is a skill"

PATH 1 — Content Provided:
  Q: Skill name? (e.g., github-automation)
  Q: One-line description?
  Q: Paste your skill content?
  
  → Claude validates structure
  → Creates skill folder + SKILL.md
  → Updates Tier 2 automatically

PATH 2 — Description Only:
  Q: Skill name?
  Q: What should this skill do? (detailed)
  Q: Any reference files/links?
  
  → Claude generates skill from description
  → User reviews generated content
  → Confirms or requests changes
  → Creates skill folder + SKILL.md

PATH 3 — Exploring:
  Q: What problem are you trying to solve?
  Q: Describe in 2-3 sentences
  
  → Claude validates: "Is this a skill or something else?"
  
  IF skill-appropriate:
    → Offers to generate draft
    → User confirms
  
  IF not skill-appropriate:
    → Explains why (context, code, process, etc.)
    → Suggests alternative

Result: Skill created in {ProjectName}\skills\{skill-name}\
```

#### Auto-loading Question
After skill creation:
```
Q: Load this skill automatically on > start? (yes/no)
   Default: yes
   Note: Can be changed anytime with > skill disable
```

### Usage Commands

#### `> skill use <name>`
**Purpose:** Load a skill into current session context

**Effect:**
- Loads skill content into context window
- Skill available for all remaining session messages
- Can load multiple skills in one session
- Skills automatically unload at session end

**Example:**
```
You: > skill use github-automation

Claude: ✓ Skill loaded: github-automation
        Available for this session
        Use normally — I'll reference the skill content
```

### Management Commands

#### `> skill enable <name>`
**Purpose:** Allow a skill to auto-load on > start

**Before:**
```
Skill status: disabled (manual load only via > skill use)
```

**After:**
```
Skill status: enabled (will load automatically on > start)
```

#### `> skill disable <name>`
**Purpose:** Prevent a skill from auto-loading

**Before:**
```
Skill status: enabled (loads automatically on > start)
```

**After:**
```
Skill status: disabled (manual load only via > skill use)
```

#### `> skill edit <name>`
**Purpose:** Edit skill content or metadata

**Available edits:**
- Edit SKILL.md content
- Update description
- Change auto-load setting
- Update metadata
- Add supporting files

#### `> skill remove <name>`
**Purpose:** Delete a skill from project

**Confirmation Required:**
```
Delete skill "github-automation"? (yes/no)

This will:
  ✓ Delete folder: skills\github-automation\
  ✓ Remove from Tier 2
  ✓ Cannot be undone (but skill file can be recovered from git if committed)

Confirm? (yes/no)
```

### Validation Commands

#### `> skill validate`
**Purpose:** Check all skills for compliance with JITCR standards

**Output:**
```
Validating all skills...

github-automation      ✓ PASS
  ├─ Structure: valid
  ├─ SKILL.md: present and readable
  ├─ Metadata: valid JSON
  └─ Size: 2,500 tokens (OK)

code-review           ✓ PASS
  ├─ Structure: valid
  ├─ SKILL.md: present and readable
  └─ Metadata: valid JSON

documentation         ⚠ WARNING
  ├─ Structure: valid
  ├─ SKILL.md: present and readable
  ├─ Metadata: INVALID JSON (missing "scope" field)
  └─ Fix: > skill edit documentation

Results: 2 passed, 1 warning, 0 failed
All skills are usable.
```

#### `> skill validate <name>`
**Purpose:** Check a specific skill

**Output:**
```
Validating: github-automation

Structure    ✓ Valid (folder + SKILL.md + metadata)
SKILL.md     ✓ Readable and non-empty
Metadata     ✓ Valid JSON with all required fields
Size         ✓ ~2,500 tokens (reasonable)
Dependencies ✓ None (OK)

Result: ✓ PASS
Status: Ready for use
```

---

## Skill Validation — Complete Reference

JITCR skill validation operates at two independent levels. Both run automatically
during `> skill add` and on demand via `> skill validate`. Understanding both levels
is essential for agents assisting users with skill creation.

---

### Level 1 — Structural Validation

Checks that the skill's files and folders meet the required physical structure.
These checks are deterministic — pass or fail, no judgment required.

| Check | Pass Condition | Fail Action |
|---|---|---|
| Folder exists | `skills/{skill-name}/` folder present | Create it or report missing |
| SKILL.md present | File exists and is non-empty | Report missing, block skill |
| skill-metadata.json present | File exists and is valid JSON | Regenerate via `> skill edit` |
| Required metadata fields | name, description, scope, created, enabled, auto_load, version | Report missing fields |
| Size within limits | SKILL.md under 10,000 tokens | Warn at 5,000+, block at 10,000+ |

Structural validation runs first, always. If it fails, conceptual validation does
not run — fix the structure first.

---

### Level 2 — Conceptual Validation

Checks that the skill's *content* is appropriate, coherent, and protocol-compliant.
This is a reasoning check, not a structural one. An agent applies these rules against
the actual text of SKILL.md and returns a specific failure report if any rule is violated.

#### The Conceptual Disqualifier Rules

A skill FAILS conceptual validation if ANY of the following rules are triggered.
Each rule includes a test the agent applies and a suggested fix for the user.

---

**Rule 1 — Conflicts with Level 1 Protocol Guardrails**

Triggers if: The skill instructs the AI to perform an action that a protocol-level
guardrail explicitly prohibits — for example, deleting files without user permission,
modifying .env files, assuming timestamps, or bypassing the Tier 2 read at session start.

Why: Protocol guardrails are non-negotiable. A skill cannot override them regardless
of the stated justification.

Fix: Rephrase the conflicting instruction to work within guardrail constraints.
Example: "delete the old version before saving" → "ask user to confirm deletion before saving."

---

**Rule 2 — Attempts to Redefine Core Protocol Behavior**

Triggers if: The skill redefines what a core JITCR command does (`> start`, `> end`,
`> journal`, `> handoff`, `> save`, `> commit`, `> backup`) rather than extending it
with project-specific behavior.

Why: Skills extend the protocol. They do not replace it. A skill that rewrites `> start`
from scratch would conflict with the Universal Commands spec and break session continuity.

Fix: Narrow the skill to the specific additional behavior needed. Add a project-level
step, not a replacement for the whole command.

---

**Rule 3 — Scope Too Broad**

Triggers if: The skill attempts to cover the entire project's purpose rather than one
cohesive, reusable capability. Signal phrases: "handles all aspects of," "complete guide
to," "everything related to," or a skill that would only ever make sense as the single
skill in a project.

Why: A skill that is too broad cannot be loaded selectively. It defeats just-in-time
loading and is hard to maintain as the project evolves.

Fix: Split into focused sub-skills, each covering one capability. Name them clearly.

---

**Rule 4 — Session-Specific, Not Reusable**

Triggers if: The skill encodes context that is specific to one session or one moment
in time — for example, "the file we are currently refactoring," "the bug we found
today," or a hardcoded reference to a specific piece of work that will not recur.

Why: Skills are reusable across sessions. If the content only makes sense today,
it belongs in a journal or handoff entry, not a skill.

Fix: Generalize the skill to the repeatable pattern (e.g., "how to refactor any
function in this codebase" rather than "how to refactor utils.py today").

---

**Rule 5 — Contains Harmful or Safety-Bypassing Instructions**

Triggers if: The skill instructs the AI to ignore confirmation prompts for
destructive operations, bypass guardrails under specific conditions, suppress
warnings, proceed without user approval on high-stakes actions, or take any
action that removes human oversight.

Why: No stated justification makes safety-bypassing acceptable. This is a hard
disqualifier, not a matter of degree.

Fix: Remove the bypass instruction entirely. If speed is the concern, design the
workflow to minimize confirmation steps rather than eliminate them.

---

**Rule 6 — Duplicates an Existing Skill**

Triggers if: The proposed skill's purpose substantially overlaps with an existing
skill in the project's skills registry. "Substantially overlaps" means a user
invoking either skill for the same task would get equivalent results.

Why: Duplicate skills waste tokens, cause confusion about which to load, and
diverge over time as one is maintained and the other is not.

Fix: Edit the existing skill to incorporate the new capability, or differentiate
the scopes so both are clearly needed for different situations.

---

**Rule 7 — Instruction Quality Too Low to Be Useful**

Triggers if: The skill content is so vague, incomplete, or contradictory that
an agent loading it would not know what to do differently than without it.
Examples: a skill that says only "be helpful with code reviews" with no criteria,
checklist, format, or process defined; or a skill whose instructions contradict
each other.

Why: A skill that does not meaningfully change agent behavior wastes tokens every
time it loads and creates false confidence that a capability is defined when it is not.

Fix: Revise to include specific, actionable instructions — criteria, steps, formats,
or rules that unambiguously change how the agent responds when the skill is active.

---

#### Reporting Conceptual Validation Results

When a conceptual validation check fails, the agent returns a structured failure report:

```
Conceptual Validation — FAILED

Skill: {skill-name}
Rule violated: Rule {N} — {Rule Name}

What triggered it:
  "{exact quote or paraphrase of the violating content from SKILL.md}"

Why it fails:
  {explanation of how the content conflicts with the rule}

Suggested fix:
  {specific, actionable guidance for how to revise the skill}

Next step: Run > skill edit {skill-name} to revise, then re-validate.
```

If multiple rules are violated, list each one separately. Do not combine into a
single generic failure — the user needs to know exactly which rules were triggered
and in what order to fix them.

---

### Configurable Multi-Mode Validation

Any skill can implement any combination of validation behaviors beyond the two
default levels above. This is configured in SKILL.md using a `## Validation
Configuration` section.

#### The Four Modes

**Mode 1 — Protocol-Governed (default)**
The standard two-level check: structural + conceptual disqualifiers.
This mode runs automatically on all skills. No configuration required.

**Mode 2 — No-Validation**
Structural and conceptual checks are bypassed entirely.
Use for rapid iteration, exploratory skills, or content already verified externally.

```markdown
## Validation Configuration
Mode: no-validation
Reason: [optional — explain why validation is bypassed]
```

**Mode 3 — User-Defined Rule-Based**
You write domain-specific validation rules. The agent validates inputs against
them and returns a structured failure report identifying exactly which rule was
violated, what the violating content is, and what would need to change to pass.

```markdown
## Validation Configuration
Mode: user-defined

Rules:
1. [Rule statement — specific, binary, scoped]
2. [Rule statement]
3. [Rule statement]

On failure:
- Return structured failure report
- List each violated rule by number
- Quote the specific violating content
- Do not auto-correct — present for human review
```

**Mode 4 — Agent-Assisted Intelligent**
AI reasoning is applied to your rules, catching violations that pattern matching
would miss: logical inconsistencies, implicit contradictions, contextual violations.

Combine with Mode 3 for the most powerful validation available:

```markdown
## Validation Configuration
Mode: user-defined + agent-assisted

Rules:
1. [Rule statement]
2. [Rule statement]

On failure:
- Return structured failure report
- Reason about meaning, not just text matching
- Flag implicit violations (e.g., a conclusion claim not supported by the body)
- Do not auto-correct — present for human review
```

#### Mode Selection Guide

Use this table to decide which mode to recommend when helping a user configure validation:

| Skill Type | Recommended Mode | Why |
|---|---|---|
| Knowledge / reference skill | Mode 1 (default) | Standard quality check is sufficient |
| Exploratory / draft skill | Mode 2 (no-validation) | User is still figuring out the shape |
| Process / workflow skill | Mode 1 + Mode 3 | Add domain rules for the specific process |
| Output template skill | Mode 3 + Mode 4 | Reasoning catches format violations text matching misses |
| Compliance / legal / regulated content | Mode 3 + Mode 4 | High stakes — intelligent validation justified |
| Skills for other people's use | Mode 3 + Mode 4 | External users need consistent, reliable behavior |
| Utility / helper skill | Mode 1 (default) | Low complexity, standard check sufficient |

When in doubt, start with Mode 1. Suggest adding Mode 3 rules once the user has
used the skill enough to know what kinds of failures actually occur in practice.

---

### Validation-Integrated Creation Flow

Validation should not be a separate afterthought step — it happens during skill
creation, as the agent builds the skill alongside the user.

**Path 1 — Content Provided (validate on receipt)**

```
Step 1: Receive content
Step 2: Run structural pre-check (can the folder/file structure be created?)
Step 3: Run Level 1 structural validation on the pasted content
Step 4: Run Level 2 conceptual validation against all 7 disqualifier rules
Step 5: IF any rule violated → return failure report, ask user to revise before creating
Step 6: IF all rules pass → confirm: "Validation passed. Ready to create {skill-name}?"
Step 7: User confirms → create files, update Tier 2
Step 8: Confirm creation, suggest mode configuration if skill type warrants it
```

The agent does NOT create the skill first and validate later. Validate before creating.

**Path 2 — Description Only (validate the draft)**

```
Step 1: Gather: skill name, description, what it should do (detailed)
Step 2: Generate SKILL.md draft
Step 3: Run Level 2 conceptual validation on the generated draft internally
         (before showing to user — fix disqualifier issues in generation, not after)
Step 4: Show draft to user with plain-language summary:
         "Here's what I've drafted. Validation: passed / [issue found]."
Step 5: User reviews and either:
         (a) Approves → go to Step 6
         (b) Requests changes → revise, re-validate internally, show updated draft
Step 6: Confirm: "Ready to create {skill-name}?"
Step 7: User confirms → create files, update Tier 2
Step 8: Ask: "Do you want to add custom validation rules for this skill? (y/n)"
         IF yes → walk through Mode 3 / Mode 3+4 configuration
         IF no → done
```

The agent self-validates the draft before showing it to the user.

**Path 3 — Exploring (validate the concept first)**

```
Step 1: Listen to the problem description
Step 2: Apply disqualifier rules as a concept-level check:
         - Would this be Rule 3 (too broad)?
         - Would this be Rule 4 (session-specific, not reusable)?
         - Is this a repeatable process, or a one-time thing?
Step 3: Decision:
         IF skill-appropriate → "This is a good fit for a skill. Here's why: [reason].
                                  Want me to draft it? (y/n)"
         IF not skill-appropriate → "This isn't quite a skill because [specific reason].
                                      What might work better is [alternative]."
Step 4: IF proceeding → switch to Path 2 flow from Step 1
```

The agent's judgment on "is this a skill?" is grounded in the disqualifier rules,
not a vague sense of appropriateness. Always name the rule and explain why.

---

### Agent Quick-Reference — Validation in Practice

```
BEFORE creating any skill:
  ✓ Run structural pre-check
  ✓ Run conceptual check against all 7 disqualifier rules
  ✓ Only create after both pass

WHEN validation fails:
  ✓ Return structured failure report (rule number, quote, why, fix)
  ✓ Never silently proceed past a failed rule
  ✓ Never auto-correct without showing the user what changed

DURING > skill add Path 1 (content provided):
  ✓ Validate before creating, not after

DURING > skill add Path 2 (description → draft):
  ✓ Self-validate the draft before showing it to the user
  ✓ After approval, ask about custom validation mode configuration

DURING > skill add Path 3 (exploring):
  ✓ Ground the judgment in specific disqualifier rules
  ✓ Name the rule that would be triggered if not a skill

FOR mode selection:
  ✓ Default: Mode 1 (structural + conceptual)
  ✓ Rapid iteration / exploratory: Mode 2
  ✓ Process / output / compliance: Mode 3 + Mode 4
  ✓ Suggest upgrading to Mode 3 once user knows what failures occur in practice

ALWAYS:
  ✓ A validation failure is a fix request, not a rejection.
    Guide toward the fix, not away from the skill.
```

---

### Suggestion Command

#### `> skill suggest`
**Purpose:** Smart suggestion based on session context

**Intelligence Levels:**

**Level 1: Passive (shown at > start)**
```
You have 3 enabled skills available:
  • github-automation
  • code-review  
  • documentation

Use: > skill use <name>  or  > skill list
```

**Level 2: Active (based on handoff patterns)**
```
> start (session begins)
  ↓
System suggests: "Based on last session (code review work), 
                  you might want: > skill use code-review (y/n)?"
```

**Level 3: Interactive (this command)**
```
You: > skill suggest

Claude analyzes:
  - Last 3 journal entries
  - Current session context
  - Your available skills

Claude: "Your work looks like you need code-review and documentation.
         Load them? (yes/no)

         > skill use code-review
         > skill use documentation"
```

### Help Command

#### `> ? skill`
**Purpose:** Show all skills commands

**Output:**
```
┌──────────────────────────────────────┐
│  JITCR Skills Commands — Help        │
├──────────────────────────────────────┤
│  > skill list          List all      │
│  > skill add           Create new    │
│  > skill use <name>    Load skill    │
│  > skill info <name>   Show details  │
│  > skill enable <name>  Activate    │
│  > skill disable <name> Deactivate  │
│  > skill edit <name>   Edit skill   │
│  > skill remove <name> Delete skill │
│  > skill validate      Check all    │
│  > skill suggest       Smart hint   │
│  > ? skill             This help    │
└──────────────────────────────────────┘

Tip: Each skill loads only when needed. Skills unload at session end.
     Use > skill list to see all available skills.
     Use > skill suggest for intelligent recommendations.
```

---

## Loading Strategy

### On `> start` (Session Initialization)

```
> start runs
  ↓
Loads Tier 2 (project context)
  ↓
Shows Skill Summary:
  "3 enabled skills available:
   • github-automation
   • code-review
   • documentation
   
   Use: > skill use <name>  or  > skill suggest"
  ↓
Session continues (skills NOT auto-loaded yet)
  ↓
Optional: User types > skill suggest
  ↓
User needs skill: > skill use github-automation
  ↓
Skill loads into context (THIS session only)
  ↓
User continues work with skill active
```

### During Session

```
At any point during a session:

User: > skill use code-review
  ↓
Claude: ✓ Skill loaded: code-review
        Available for rest of this session
  ↓
User continues with skill context available
  ↓
User can load multiple skills: > skill use documentation
  ↓
Both skills stay loaded until session ends
```

### Session End

```
> end (or session ends)
  ↓
All loaded skills automatically unload
  ↓
Skills metadata updated with last-used timestamp
  ↓
Session ends
```

---

## Tier 2 Integration

Every project's Tier 2 file (JITCR_{ProjectName}.md) includes a "Project Skills" section:

```markdown
## Project Skills

| Skill | Description | Status | Auto-load |
|-------|-------------|--------|-----------|
| github-automation | Automate GitHub workflows | enabled | yes |
| code-review | Code quality analysis | enabled | yes |
| documentation | Generate documentation | enabled | no |
| research-tools | Research and analysis | disabled | - |

**Total:** 4 skills (3 enabled, 1 disabled)

**How to manage:**
- `> skill list` — Show all skills
- `> skill use <name>` — Load a skill
- `> skill add` — Create new skill
- `> skill remove <name>` — Delete skill

See JITCR_Skills_Protocol.md for complete guide.
```

Tier 2 is automatically updated when skills are added/removed/enabled/disabled.

---

## Best Practices

### 1. Keep Skills Focused
- ✅ One skill = one cohesive capability
- ❌ Don't combine unrelated knowledge into one skill
- **Example:** `github-automation` should contain GitHub-specific instructions, not also Python tips

### 2. Make Skills Reusable
- ✅ Skills work across multiple sessions
- ✅ Skills don't depend on session context
- ❌ Don't make a skill that only makes sense in one project session
- **Example:** `code-review` process should work on any code, not just "this specific file"

### 3. Use Clear Names
- ✅ Describe what the skill does: `github-automation`, `code-review`, `documentation`
- ❌ Vague names: `tool1`, `helper`, `stuff`
- ❌ Too long: `my-comprehensive-github-workflow-and-automation-system`

### 4. Document the Skill
- ✅ Clear description in SKILL.md
- ✅ Usage examples in SKILL.md
- ✅ Scope clearly stated
- ❌ Unclear instructions
- ❌ Missing examples

### 5. Load Only When Needed
- ✅ Most sessions won't need all skills
- ✅ Use `> skill use` when you need it
- ❌ Don't keep all skills loaded all the time (wastes tokens)
- **Philosophy:** Just-in-time loading, not preload

### 6. Keep Sizes Reasonable
- ✅ Skills under 5,000 tokens are ideal
- ⚠️ 5,000-10,000 tokens is acceptable
- ❌ Anything over 10,000 tokens should be split into multiple skills
- **Reason:** Smaller skills load faster and waste fewer tokens when not used

---

## Skill Examples

### Example 1: github-automation (Multi-step Workflow)
```
Scope: Multi-step workflow
Purpose: Automate GitHub operations (create branches, PRs, commits)
Size: ~2,500 tokens
Auto-load: Yes

Content:
- Step 1: Create feature branch from main
- Step 2: Make commits following convention
- Step 3: Create pull request with template
- Step 4: Add labels and assign reviewers
- Step 5: Merge once approved
```

### Example 2: code-review (Single-task Utility)
```
Scope: Single-task
Purpose: Analyze code for quality issues
Size: ~1,500 tokens
Auto-load: No (load when needed)

Content:
- Checklist for code review
- Common issues to look for
- Performance considerations
- Security considerations
- Test coverage expectations
```

### Example 3: documentation (Multi-step Workflow)
```
Scope: Multi-step workflow
Purpose: Generate and maintain project documentation
Size: ~3,000 tokens
Auto-load: Yes

Content:
- README structure and template
- API documentation format
- Code comment best practices
- CONTRIBUTING guide format
- Architecture documentation outline
```

---

## Troubleshooting

### Problem: "Skill not loading"
**Cause:** Skill might not be enabled or path is wrong
**Solution:** 
1. `> skill list` (check if enabled)
2. `> skill enable <name>` (if disabled)
3. `> skill use <name>` (manual load)
4. `> skill validate <name>` (check structure)

### Problem: "Skill content seems outdated"
**Solution:**
1. `> skill info <name>` (check last modified date)
2. `> skill edit <name>` (update content)
3. `> skill validate <name>` (verify changes)

### Problem: "Too many skills slowing session"
**Solution:**
1. `> skill list` (see what's enabled)
2. `> skill disable <name>` (disable unused skills)
3. Load only needed skills with `> skill use <name>`

### Problem: "Skill structure validation fails"
**Solution:**
1. `> skill validate <name>` (see specific error)
2. `> skill edit <name>` (fix the issue)
3. Ensure SKILL.md exists and skill-metadata.json is valid JSON

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-06-26 | Initial JITCR Skills Protocol — complete spec |
| 1.1 | 2026-06-30 | Added: Skill Validation Complete Reference — Level 1 structural validation table, Level 2 conceptual validation with 7 disqualifier rules + structured failure report format, Configurable Multi-Mode Validation (4 modes + mode-selection guide), Validation-Integrated Creation Flow (Paths 1/2/3), Agent Quick-Reference card |

---
