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

---
