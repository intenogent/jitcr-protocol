# Contributing to JITCR Protocol

Thanks for your interest in helping with JITCR! We genuinely appreciate it.

---

## A Quick Note

JITCR is currently maintained by **@intenogent** as a solo project. I'm committed to responding to contributions, but with limited availability — expect a response within a few days, not hours. I'll do my best to keep things moving.

---

## How You Can Help

### **1. Report a Bug** ✅
Found something that doesn't work?

- **Open an Issue** with:
  - Your OS (Windows 11, macOS 14, Linux distro)
  - JITCR version or installation date
  - What you were trying to do
  - What happened instead
  - Steps to reproduce (so we can test it)
  - Any error messages (copy & paste the full text)

That's it. We'll investigate and fix it.

**Why not a PR?** Bug fixes touch the core protocol. We want to make sure the fix is tested and won't break something else.

### **2. Suggest an Idea or Improvement** 💡
Have a thought about a new `>` command, better workflow, or feature?

- **Go to Discussions → Ideas (Feature Requests)**
- Describe what you'd like to see and why
- We'll discuss it together

This lets us think it through before anyone writes code. Some ideas are great, some need refinement, some don't fit JITCR's design — discussing first saves everyone time.

**Why not a PR?** We need to agree on the direction first. Submitting code for an idea that doesn't align with JITCR's goals creates extra work for everyone.

### **3. Improve Documentation** ✅
Spot a typo, unclear explanation, or missing example?

- **Submit a PR** for documentation fixes
- Keep it focused (one fix per PR)
- Clear commit message: `docs: fix typo in README section X` or `docs: clarify installation step 3`

Documentation PRs are quick to review. Go ahead!

### **4. Improve the Installer Experience** ✅
Found a way to make the `JITCR_Installer_Prompt.md` clearer or more robust?

- **Open an Issue first** to discuss the improvement
- Once we agree it's good, submit a PR

The installer is critical — we want to vet changes before merging.

### **5. Test & Feedback** ✅
Try JITCR on your OS, with your setup, and tell us what works and what doesn't.

- **Open an Issue** with your experience
- Include what worked smoothly
- Include what was confusing or broke
- This helps us improve

---

## How NOT to Contribute (And Why)

### ❌ Don't submit a PR for protocol changes without discussing first

**This happens:** You find what you think is a better way to handle Tier 2 loading, or a new `>` command, and submit a PR.

**Why we can't merge it:** The protocol is the foundation of JITCR. A change that looks good in isolation might break session continuity, token math, or workflow logic. We need to discuss the implications first.

**What to do instead:** Open an Issue describing the change and why it matters. Let's talk it through. If it's solid, we'll say "yes, please submit a PR" and you'll know it'll be welcomed.

### ❌ Don't change multiple systems in one PR

**This happens:** You fix a bug, improve docs, and refactor the installer all in one PR.

**Why we can't review it:** Too many changes mean too much to vet at once. Also hard to understand the intent.

**What to do instead:** One PR = one focused change. Easier to review, easier to merge, easier to revert if needed.

### ❌ Don't assume we want a feature even if it's cool

**This happens:** You add a feature you think is awesome — maybe a new `> config` command or a plugin system.

**Why we can't just merge it:** JITCR is intentionally minimal. Every addition increases complexity and maintenance burden. We need to align on whether it's worth it.

**What to do instead:** Open an Issue: "I think we should add X because Y." Let's discuss if it fits JITCR's design.

---

## The PR Workflow (If We've Agreed)

Once we've agreed to a PR (documentation fix, installer improvement, etc.):

1. **Fork** the repo
2. **Create a branch** from `main`:
   - `docs/fix-typo-section-x`
   - `docs/clarify-installation`
   - `installer/improve-error-message`
3. **Make your changes**
4. **Test it** (especially for installer changes — try the install on your OS)
5. **Write a clear commit message:**
   ```
   docs: fix typo in token savings section

   Changed "~725 tokens × 20 messages" calculation example
   to match the actual formula in the docs.
   ```
6. **Submit the PR** with a description of what you changed and why

That's it. We'll review and merge (or ask for adjustments).

---

## Questions?

- **How do I use JITCR?** → Read the [README.md](README.md)
- **I found a bug** → Open an [Issue](https://github.com/intenogent/jitcr-protocol/issues)
- **I have an idea** → Post in [Discussions → Ideas](https://github.com/intenogent/jitcr-protocol/discussions/categories/ideas-feature-requests)
- **I want to ask something** → Use [Discussions → Q&A](https://github.com/intenogent/jitcr-protocol/discussions/categories/q-a)

---

## What We're Looking For

We especially value contributions that:

✅ **Solve real problems** — You hit a bug or inefficiency, and you're reporting it or fixing it  
✅ **Come with context** — You explain what, why, and how  
✅ **Are tested** — You've verified the fix/improvement actually works  
✅ **Are respectful** — You understand JITCR's design philosophy and work within it  
✅ **Help others** — You're thinking about the next person who uses JITCR  

---

## Thank You

Whether you're reporting a bug, suggesting an idea, or fixing a typo — thank you. JITCR is better because of people like you who care enough to engage.

Let's build something solid together. 🚀

---

**@intenogent**
