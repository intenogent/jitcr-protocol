# SKILL_TEMPLATE.md

**Use this template as a reference when creating new skills via `> skill add`**

---

## What Is This Template?

This is a reference template showing the structure and format that JITCR skills should follow.

When you run `> skill add`, Claude will:
1. Ask you for skill details (name, description, content)
2. Create a folder: `skills/{skill-name}/`
3. Create a `SKILL.md` file in that folder (using the structure below)
4. Auto-create skill-metadata.json
5. Update your Tier 2 file automatically

**You can create skills in three ways:**

**PATH 1:** Paste skill content directly  
**PATH 2:** Describe what you need (Claude generates)  
**PATH 3:** Explore if it's a skill (Claude validates)

This template shows the FORMAT your skill should have.

---

## Template Structure

Use this format for SKILL.md in `{ProjectName}/skills/{skill-name}/SKILL.md`:

```markdown
# Skill: [Skill Name]

**Purpose:** [One-line description of what this skill does]

**Scope:** [Choose one: single-task | multi-step-workflow | utility]

**When to use:** [Brief explanation of when/how to invoke this skill]

---

## Overview

[1-2 paragraph explanation of the skill's purpose and main capability]

---

## Key Instructions / Knowledge / Process

[This is the core content of your skill. Format depends on type:]

### For Process Skills:
```
Step 1: [First step]
Step 2: [Second step]
Step 3: [Third step]
```

### For Knowledge Skills:
```
**Topic 1:**
[Detailed explanation]

**Topic 2:**
[Detailed explanation]
```

### For Analysis Skills:
```
**Criteria:**
- Point 1
- Point 2
- Point 3
```

---

## Usage Examples

[Show 2-3 concrete examples of how to use this skill]

---

## Best Practices

- [Practice 1]
- [Practice 2]
- [Practice 3]

---

## Notes

[Any additional notes or context]
```

---

## Creating Your Own Skill

When you're ready to create a skill:

1. Run: `> skill add`
2. Choose your path (content, description, or explore)
3. Provide the skill details
4. Claude will create the folder and SKILL.md
5. Use this template as a reference for SKILL.md format
6. Edit anytime with: `> skill edit {skill-name}`

**Remember:** Skills are reusable, focused knowledge that loads on-demand.

For complete guidance, see: `JITCR_Universal_Skills_Protocol.md`
