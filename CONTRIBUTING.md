# Contributing to JITCR Protocol

Thanks for your interest in helping with JITCR! We genuinely appreciate it.

## The Short Version

JITCR is currently maintained by @intenogent as a solo project, so I review contributions personally. I'm committed to responding within a few days (not hours) — I do my best to keep things moving.

I actively review and merge contributions that follow these guidelines. You won't wait months — I respond within a few days and take your work seriously.


**You can help in these ways:**

1. **Report bugs** — Open an Issue (no discussion needed)
2. **Fix documentation** — Submit a PR directly for typos, clarity, or missing examples
3. **Suggest ideas** — Start a Discussion before writing code
4. **Test and give feedback** — Try JITCR on your OS and tell us what works/breaks

---

## 1. Report a Bug ✅

Found something that doesn't work?

**Open an Issue with:**
- Your OS (Windows 11, macOS 14, Linux distro)
- JITCR version or installation date
- What you were trying to do
- What happened instead
- Steps to reproduce (so we can test it)
- Any error messages (copy & paste the full text)

That's it. We'll investigate and fix it.

**Why not a PR?** Bug fixes touch the core protocol. We want to make sure the fix works and doesn't break something else.

---

## 2. Improve Documentation ✅

Spot a typo, unclear explanation, or missing example?

**Submit a PR directly:**
- Keep it focused (one fix per PR)
- Clear commit message: `docs: fix typo in README section X` or `docs: clarify installation step 3`
- Documentation PRs are quick to review — go ahead!

---

## 3. Suggest an Idea or Improvement 💡

Have a thought about a new command, better workflow, or feature?

**Start a Discussion first** (not a PR):
- Go to **Discussions → Ideas (Feature Requests)**
- Describe what you'd like to see and why
- We'll talk it through together

**Why discuss first?** Discussing saves everyone time:
- Some ideas are great and we'll say "yes, please submit a PR"
- Some need refinement before code
- Some don't fit JITCR's design — that's okay, we'll explain why

This way you know your PR will be welcomed before you write it.

---

## 4. Test & Give Feedback ✅

Try JITCR on your OS with your setup and tell us what works and what doesn't.

**Open an Issue with your experience:**
- Include what worked smoothly
- Include what was confusing or broke
- This helps us improve

---

## The PR Workflow (Once We've Agreed)

Once we've discussed and agreed a change is good:

1. **Fork the repo**
2. **Create a branch** from `main`:
   - `docs/fix-typo-section-x`
   - `docs/clarify-installation`
   - `installer/improve-error-message`
3. **Make your changes**
4. **Test it** (especially for installer changes — try the install on your OS)
5. **Write a clear commit message:**
   ```
   docs: fix typo in token savi formula
   
   Changed "~725 tokens × 20 me" to match the actual formula
   ```
6. **Submit the PR** with a description of what you changed and why

We'll review and merge (or ask for adjustments).

---

## Important Ground Rules

These protect JITCR's stability:

**Protocol changes need discussion first.** The protocol is JITCR's foundation. A change that looks good in isolation might break session continuity, token math, or workflow logic. That's why we discuss before coding.

**One focused change per PR.** Don't fix a bug, improve docs, and refactor the installer all in one PR. Easier to review, easier to merge, easier to revert if needed.

---

## What We Value in Contributions

- **Solves a real problem** — You hit a bug or found an inefficiency, and you're fixing it
- **Comes with context** — You explain what, why, and how
- **Is tested** — You've verified the fix/improvement actually works
- **Is respectful** — You understand JITCR's design philosophy and work within it
- **Helps others** — You're thinking about the next person who uses JITCR

---

## Questions?

- **How do I use JITCR?** → Read the [README.md](README.md)
- **Found a bug?** → Open an [Issue](../../issues)
- **Have an idea?** → Post in [Discussions → Ideas](../../discussions)
- **General question?** → Use [Discussions → Q&A](../../discussions)

---

## Thank You

Whether you're reporting a bug, fixing a typo, or suggesting an idea — thank you. JITCR is better because people like you care enough to engage.

Let's build something solid together. 🚀
