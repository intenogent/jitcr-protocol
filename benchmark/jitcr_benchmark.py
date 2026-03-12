"""
JITCR Framework Token Benchmark
================================
Measures token savings from Just-In-Time Context Retrieval (JITCR) framework
using Anthropic's official count_tokens API for exact, publication-grade numbers.

Usage:
  python jitcr_benchmark.py                    # Full benchmark with API
  python jitcr_benchmark.py --offline          # Offline estimation only
  python jitcr_benchmark.py --messages 30      # Custom message count

Output:
  - Console report
  - benchmark_results.json (machine-readable)

Requirements:
  - anthropic SDK (pip install anthropic)
  - python-dotenv (pip install python-dotenv)
  - ANTHROPIC_API_KEY in .env or environment
"""

import os
import sys
import json
import glob
import argparse
from datetime import datetime
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

# .env location
ENV_PATH = "C:/Users/LaserMaster/Documents/udemy/AIEngineerAgenticTrackTheCompleteAgentnMCPCourse/agents/.env"

# Reference project paths (read-only, for token counting only)
CIGAR_PROJECT = "C:/Users/LaserMaster/Documents/udemy/AIEngineerAgenticTrackTheCompleteAgentnMCPCourse/agents/3_crew/cigar_band_identifier_v5"
BEFORE_JITCR_FILE = f"{CIGAR_PROJECT}/b4_jitcr/prj_inst_b4JITCR_approach.md"
TIER2_FILE = f"{CIGAR_PROJECT}/CLAUDE_GUIDELINES.md"
LOGS_DIR = f"{CIGAR_PROJECT}/logs"

# Current Tier 1 content (exact text from Claude Desktop Project Instructions)
TIER1_CONTENT = """# TIER 1 - Cigar Project Instructions (Copy to Claude Desktop)
## Role
Advanced Agentic AI developer. Expertise: multi-agent systems, Python on Windows 11, API integrations.
You are running in the Claude Desktop with full access to the system through:
- Filesystem mcp connector
- Shell-command mcp connector
- Make sure to use the right syntax for accessing Windows 11
## Core Rules
- Act by default, be concise
- Never delete files or modify .env without explicit permission
- Read files before overwriting to preserve content
- Shell commands (git, python): use FORWARD SLASHES in paths
## CLI Commands (`>` = execute)
| Command | Action |
|---------|--------|
| `> start` | Initialize session, load full context |
| `> save` | Write journal + handoff |
| `> commit` | Git commit |
| `> end` | Save + commit + summary |
| `> ?` | Show full command reference |
Templates and full details → read CLAUDE_GUIDELINES.md from:
`C:\\Users\\LaserMaster\\Documents\\udemy\\AIEngineerAgenticTrackTheCompleteAgentnMCPCourse\\agents\\3_crew\\cigar_band_identifier_v5`
## Requires Explicit `>` Command
- Modifying `.env`
- Writing to journal or handoff files
- Making git commits
## Environment
Windows 11 | Cursor | Python 3.12 | UV | venv: agents
## Git Commit
 You do have full access. The key is to use forward slashes (/) in PowerShell instead of backslashes, which are consumed as escape characters.
## Pause and Check With Me
- Deleting existing files
- Architecture changes beyond current task
- Requirements genuinely contradictory or missing critical info
- Blocked by missing credentials or permissions"""

# Defaults
DEFAULT_MESSAGES = 20
GIT_LOG_TOKENS_ESTIMATE = 150  # ~5 commits oneline
JOURNALS_TO_LOAD = 3
MODEL = "claude-sonnet-4-5-20250929"
CONTEXT_WINDOW = 200_000  # Claude's context window

# Pricing (per 1M input tokens, as of Feb 2026)
PRICING = {
    "sonnet_4.5": {"input": 3.00, "output": 15.00},
    "opus_4.5":   {"input": 15.00, "output": 75.00},
}

# Parameterized project profiles for generalization
PROJECT_PROFILES = {
    "small": {
        "description": "Simple script or utility project",
        "before_chars": 1500,
        "tier1_chars": 300,
        "tier2_chars": 3000,
        "tier3_chars": 2000,
    },
    "medium": {
        "description": "Multi-file application (similar to reference project)",
        "before_chars": 6300,
        "tier1_chars": 1200,
        "tier2_chars": 7200,
        "tier3_chars": 8000,
    },
    "large": {
        "description": "Enterprise workflow or multi-agent system",
        "before_chars": 15000,
        "tier1_chars": 800,
        "tier2_chars": 12000,
        "tier3_chars": 15000,
    },
}


# ─────────────────────────────────────────────
# Token Counting
# ─────────────────────────────────────────────

def init_api_client():
    """Initialize Anthropic client with API key from .env."""
    try:
        from dotenv import load_dotenv
        load_dotenv(ENV_PATH, override=True)
    except ImportError:
        pass  # Fall back to environment variable

    try:
        import anthropic
        return anthropic.Anthropic()
    except Exception as e:
        print(f"ERROR: Could not initialize Anthropic client: {e}")
        return None


def count_tokens_api(client, text: str) -> int:
    """Exact token count via Anthropic's count_tokens API (free endpoint)."""
    if not text.strip():
        return 0
    response = client.messages.count_tokens(
        model=MODEL,
        messages=[{"role": "user", "content": text}]
    )
    return response.input_tokens


def count_tokens_offline(text: str) -> int:
    """Offline estimation: 3.8 chars/token for mixed markdown/prose."""
    if not text.strip():
        return 0
    return max(1, int(len(text) / 3.8))


# ─────────────────────────────────────────────
# File Discovery (reads content only, exposes only sizes/counts)
# ─────────────────────────────────────────────

def read_file(path: str) -> str:
    """Read file, return empty string if missing."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"  WARNING: Not found: {path}")
        return ""


def get_latest_handoff(logs_dir: str) -> tuple:
    """Find most recent handoff (case-insensitive, deduplicated)."""
    patterns = [
        os.path.join(logs_dir, "handoff_*.md"),
        os.path.join(logs_dir, "HANDOFF_*.md"),
    ]
    all_files = []
    for p in patterns:
        all_files.extend(glob.glob(p))
    # Deduplicate by normalizing to lowercase for comparison
    seen = {}
    for f in all_files:
        key = os.path.basename(f).lower()
        seen[key] = f  # Last wins (preserves actual path)
    unique = list(seen.values())
    if not unique:
        return "", "(none)", 0
    # Sort by lowercase basename for consistent ordering
    latest = sorted(unique, key=lambda f: os.path.basename(f).lower())[-1]
    content = read_file(latest)
    return content, os.path.basename(latest), len(content)


def get_latest_journals(logs_dir: str, count: int = 3) -> list:
    """Find N most recent journals (case-insensitive, deduplicated)."""
    patterns = [
        os.path.join(logs_dir, "journal_*.md"),
        os.path.join(logs_dir, "JOURNAL_*.md"),
    ]
    all_files = []
    for p in patterns:
        all_files.extend(glob.glob(p))
    # Filter to dated files only
    dated = [f for f in all_files if any(c.isdigit() for c in os.path.basename(f))]
    # Deduplicate by lowercase basename
    seen = {}
    for f in dated:
        key = os.path.basename(f).lower()
        seen[key] = f
    unique = list(seen.values())
    # Sort by lowercase basename
    sorted_files = sorted(unique, key=lambda f: os.path.basename(f).lower())
    latest = sorted_files[-count:] if len(sorted_files) >= count else sorted_files
    return [(read_file(f), os.path.basename(f), os.path.getsize(f)) for f in latest]


# ─────────────────────────────────────────────
# Benchmark Core
# ─────────────────────────────────────────────

def run_benchmark(count_fn, messages: int, method: str):
    """Run all 4 benchmarks and return structured results."""

    print(f"\n{'='*72}")
    print(f"  JITCR FRAMEWORK TOKEN BENCHMARK")
    print(f"  Method: {method}")
    print(f"  Model: {MODEL}")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}")
    print(f"{'='*72}")

    # ── Read files ──
    print(f"\n  Reading project files (content not displayed)...")
    before_content = read_file(BEFORE_JITCR_FILE)
    tier2_content = read_file(TIER2_FILE)
    handoff_content, handoff_name, handoff_bytes = get_latest_handoff(LOGS_DIR)
    journals = get_latest_journals(LOGS_DIR, JOURNALS_TO_LOAD)

    if not before_content:
        print("  ERROR: Could not read before-JITCR file.")
        sys.exit(1)
    if not tier2_content:
        print("  ERROR: Could not read CLAUDE_GUIDELINES.md.")
        sys.exit(1)

    # ── Count tokens ──
    print(f"  Counting tokens via {method}...\n")

    before_tokens = count_fn(before_content)
    tier1_tokens = count_fn(TIER1_CONTENT)
    tier2_tokens = count_fn(tier2_content)
    handoff_tokens = count_fn(handoff_content) if handoff_content else 0

    journal_data = []
    total_journal_tokens = 0
    for content, name, size in journals:
        t = count_fn(content)
        journal_data.append({"name": name, "bytes": size, "tokens": t})
        total_journal_tokens += t

    git_tokens = GIT_LOG_TOKENS_ESTIMATE
    tier3_total = handoff_tokens + total_journal_tokens + git_tokens

    # ════════════════════════════════════════════
    # BENCHMARK 1: Token Count Comparison
    # ════════════════════════════════════════════
    print(f"{'─'*72}")
    print(f"  BENCHMARK 1: TOKEN COUNT COMPARISON")
    print(f"{'─'*72}")
    print(f"\n  Component Inventory:")
    print(f"  {'Component':<40} {'Bytes':>7} {'Tokens':>8} {'Loaded':>12}")
    print(f"  {'─'*40} {'─'*7} {'─'*8} {'─'*12}")
    print(f"  {'Before JITCR (full instructions)':<40} {len(before_content):>7} {before_tokens:>8} {'every msg':>12}")
    print(f"  {'After — Tier 1 (Project Instructions)':<40} {len(TIER1_CONTENT):>7} {tier1_tokens:>8} {'every msg':>12}")
    print(f"  {'After — Tier 2 (CLAUDE_GUIDELINES.md)':<40} {len(tier2_content):>7} {tier2_tokens:>8} {'once':>12}")
    print(f"  {'After — Tier 3: Handoff':<40} {len(handoff_content):>7} {handoff_tokens:>8} {'once':>12}")
    for j in journal_data:
        print(f"  {'After — Tier 3: ' + j['name']:<40} {j['bytes']:>7} {j['tokens']:>8} {'once':>12}")
    print(f"  {'After — Tier 3: Git log (est.)':<40} {'~600':>7} {git_tokens:>8} {'once':>12}")

    print(f"\n  Session Simulation ({messages} messages):")
    print(f"  {'Scenario':<25} {'Formula':<35} {'Total Tokens':>13}")
    print(f"  {'─'*25} {'─'*35} {'─'*13}")

    before_total = before_tokens * messages
    after_total = (tier1_tokens * messages) + tier2_tokens + tier3_total
    savings = before_total - after_total
    pct = (savings / before_total * 100) if before_total > 0 else 0

    print(f"  {'Without JITCR':<25} {f'{before_tokens} × {messages} msgs':<35} {before_total:>13,}")
    print(f"  {'With JITCR':<25} {f'{tier1_tokens}×{messages} + {tier2_tokens} + {tier3_total}':<35} {after_total:>13,}")
    print(f"  {'SAVINGS':<25} {'':35} {savings:>13,} ({pct:.1f}%)")

    print(f"\n  Scaling Analysis:")
    print(f"  {'Messages':>8} {'Without':>10} {'With':>10} {'Saved':>10} {'Reduction':>10}")
    print(f"  {'─'*8} {'─'*10} {'─'*10} {'─'*10} {'─'*10}")
    scaling = []
    for n in [5, 10, 15, 20, 25, 30, 50]:
        b = before_tokens * n
        a = (tier1_tokens * n) + tier2_tokens + tier3_total
        s = b - a
        p = (s / b * 100) if b > 0 else 0
        scaling.append({"messages": n, "before": b, "after": a, "saved": s, "percent": round(p, 1)})
        print(f"  {n:>8} {b:>10,} {a:>10,} {s:>10,} {p:>9.1f}%")

    # ════════════════════════════════════════════
    # BENCHMARK 2: COST IMPACT
    # ════════════════════════════════════════════
    print(f"\n{'─'*72}")
    print(f"  BENCHMARK 2: COST IMPACT")
    print(f"{'─'*72}")

    sessions_per_day = 5  # Conservative estimate
    days_per_month = 22   # Working days

    for model_name, prices in PRICING.items():
        cost_per_token = prices["input"] / 1_000_000
        before_cost_session = before_total * cost_per_token
        after_cost_session = after_total * cost_per_token
        saved_session = before_cost_session - after_cost_session

        before_cost_month = before_cost_session * sessions_per_day * days_per_month
        after_cost_month = after_cost_session * sessions_per_day * days_per_month
        saved_month = before_cost_month - after_cost_month

        print(f"\n  {model_name} (${prices['input']}/M input tokens):")
        print(f"    Per session ({messages} msgs):  Before ${before_cost_session:.4f}  After ${after_cost_session:.4f}  Saved ${saved_session:.4f}")
        print(f"    Monthly ({sessions_per_day} sessions/day × {days_per_month} days):")
        print(f"      Before: ${before_cost_month:.2f}   After: ${after_cost_month:.2f}   Saved: ${saved_month:.2f}")

    # ════════════════════════════════════════════
    # BENCHMARK 3: SESSION LONGEVITY
    # ════════════════════════════════════════════
    print(f"\n{'─'*72}")
    print(f"  BENCHMARK 3: SESSION LONGEVITY (estimated exchanges before compaction)")
    print(f"{'─'*72}")

    # Assumptions (conservative)
    avg_user_msg = 150      # tokens per user message
    avg_response = 1500     # tokens per Claude response
    avg_tool_overhead = 300 # MCP tool call + result per exchange
    conversation_per_exchange = avg_user_msg + avg_response + avg_tool_overhead

    print(f"\n  Assumptions:")
    print(f"    Context window:           {CONTEXT_WINDOW:>10,} tokens")
    print(f"    Avg user message:         {avg_user_msg:>10} tokens")
    print(f"    Avg Claude response:      {avg_response:>10,} tokens")
    print(f"    Avg tool overhead:        {avg_tool_overhead:>10} tokens")
    print(f"    Per exchange (conv only): {conversation_per_exchange:>10,} tokens")

    # MODEL: Claude Desktop sends Project Instructions with EVERY API call.
    # The context window fills with:
    #   Project Instructions (fixed, every call)
    #   + Cumulative conversation history (grows each exchange)
    #   + Current user message
    #
    # Context at exchange N:
    #   Without JITCR: before_tokens + N * conversation_per_exchange
    #   With JITCR:    tier1_tokens + tier2_and_3_once + N * conversation_per_exchange
    #
    # The JITCR Tier 2+3 content appears once in conversation history
    # (from the > start exchange) and stays there as history grows.

    # Without JITCR: Project Instructions take space every call
    available_without = CONTEXT_WINDOW - before_tokens
    exchanges_without = available_without // conversation_per_exchange

    # With JITCR: Smaller Tier 1 in system prompt, but Tier 2+3 in conversation history
    available_with = CONTEXT_WINDOW - tier1_tokens - tier2_tokens - tier3_total
    exchanges_with = available_with // conversation_per_exchange

    gained = exchanges_with - exchanges_without
    gained_pct = (gained / exchanges_without * 100) if exchanges_without > 0 else 0

    print(f"\n  Context Fill Model:")
    print(f"    Project Instructions are sent with EVERY API call from Claude Desktop.")
    print(f"    Conversation history accumulates and counts against the context window.")
    print(f"    JITCR Tier 2+3 appears once in history (from '> start' exchange).")

    print(f"\n  Results:")
    print(f"    Without JITCR:")
    print(f"      System prompt (every call):  {before_tokens:>8,} tokens")
    print(f"      Available for conversation:  {available_without:>8,} tokens")
    print(f"      Estimated exchanges:         {exchanges_without:>8,}")
    print(f"    With JITCR:")
    print(f"      System prompt (every call):  {tier1_tokens:>8,} tokens")
    print(f"      Tier 2+3 in history (once):  {tier2_tokens + tier3_total:>8,} tokens")
    print(f"      Available for conversation:  {available_with:>8,} tokens")
    print(f"      Estimated exchanges:         {exchanges_with:>8,}")
    print(f"    Extra exchanges gained:        {gained:>8,} ({gained_pct:.1f}% more)")
    print(f"\n  Note: With a 200K context window, the longevity gain from JITCR is")
    print(f"  modest (~{gained_pct:.0f}%). The primary value is token COST savings,")
    print(f"  not session length. Longevity gains are larger on smaller context")
    print(f"  windows or projects with bigger instruction sets.")

    # ════════════════════════════════════════════
    # BENCHMARK 4: BETWEEN-SESSION EFFICIENCY
    # ════════════════════════════════════════════
    print(f"\n{'─'*72}")
    print(f"  BENCHMARK 4: BETWEEN-SESSION CONTEXT RESTORATION")
    print(f"{'─'*72}")

    start_load = tier2_tokens + tier3_total
    # Manual re-explanation estimate: conversational text is ~30-50% more verbose
    # than structured handoff. Plus you'd need to re-explain project setup, commands, etc.
    manual_estimate = int(tier3_total * 1.4) + tier2_tokens  # You'd still need to convey Tier 2 info somehow

    print(f"\n  JITCR '> start' context load:")
    print(f"    Tier 2 (guidelines):    {tier2_tokens:>6} tokens")
    print(f"    Tier 3 (handoff+journals+git): {tier3_total:>6} tokens")
    print(f"    Total one-time cost:    {start_load:>6} tokens")
    print(f"\n  Without JITCR (estimated manual re-explanation):")
    print(f"    Re-explain project context: {manual_estimate:>6} tokens (est.)")
    print(f"    Note: This assumes conversational re-explanation is ~40% more")
    print(f"    verbose than structured handoff documents, and you'd still need")
    print(f"    to convey the equivalent of Tier 2 information somehow.")
    print(f"\n  Key advantage: JITCR handoffs are machine-generated and structured,")
    print(f"  requiring zero user effort to restore context between sessions.")

    # ════════════════════════════════════════════
    # MATHEMATICAL PROOF
    # ════════════════════════════════════════════
    print(f"\n{'─'*72}")
    print(f"  MATHEMATICAL PROOF: UNIVERSAL SAVINGS FORMULA")
    print(f"{'─'*72}")
    print(f"""
  Let:
    B = Before JITCR instruction tokens (loaded every message)
    T1 = Tier 1 tokens (loaded every message)
    T2 = Tier 2 tokens (loaded once)
    T3 = Tier 3 tokens (loaded once)
    N = Number of messages in session

  Without JITCR:  Cost_before = B × N
  With JITCR:     Cost_after  = (T1 × N) + T2 + T3

  Savings = B×N - (T1×N + T2 + T3)
          = N×(B - T1) - (T2 + T3)

  Since JITCR moves content from always-on (B) to on-demand (T2+T3):
    B ≈ T1 + T2  (before = Tier 1 + what became Tier 2)

  Therefore:
    Savings ≈ N×T2 - (T2 + T3)
            = T2×(N - 1) - T3

  Breakeven: N > 1 + (T3 / T2)

  With reference data: T2 = {tier2_tokens}, T3 = {tier3_total}
    Breakeven: N > 1 + ({tier3_total} / {tier2_tokens}) = {1 + tier3_total/tier2_tokens:.1f} messages

  After {1 + tier3_total/tier2_tokens:.1f} messages, JITCR saves tokens on EVERY
  additional message. Savings grow linearly and are unbounded.

  At N = {messages}: Savings = {tier2_tokens}×({messages}-1) - {tier3_total} = {tier2_tokens*(messages-1) - tier3_total:,} tokens
  Actual measured:  {savings:,} tokens ({pct:.1f}% reduction)
""")

    # ════════════════════════════════════════════
    # PARAMETERIZED PROFILES
    # ════════════════════════════════════════════
    print(f"{'─'*72}")
    print(f"  GENERALIZATION: PARAMETERIZED PROJECT PROFILES")
    print(f"{'─'*72}")
    print(f"\n  Using offline estimation (3.8 chars/token) for synthetic profiles.\n")

    for profile_name, profile in PROJECT_PROFILES.items():
        b_tok = count_tokens_offline(profile["before_chars"] * "x")
        t1_tok = count_tokens_offline(profile["tier1_chars"] * "x")
        t2_tok = count_tokens_offline(profile["tier2_chars"] * "x")
        t3_tok = count_tokens_offline(profile["tier3_chars"] * "x")

        b_total = b_tok * messages
        a_total = (t1_tok * messages) + t2_tok + t3_tok
        s = b_total - a_total
        p = (s / b_total * 100) if b_total > 0 else 0
        breakeven = 1 + (t3_tok / t2_tok) if t2_tok > 0 else 999

        marker = " ← reference" if profile_name == "medium" else ""
        print(f"  {profile_name.upper()} ({profile['description']}){marker}")
        print(f"    Before: {b_tok} tok/msg × {messages} = {b_total:,}")
        print(f"    After:  T1({t1_tok})×{messages} + T2({t2_tok}) + T3({t3_tok}) = {a_total:,}")
        print(f"    Savings: {s:,} tokens ({p:.1f}%) | Breakeven: {breakeven:.1f} msgs\n")

    # ════════════════════════════════════════════
    # METHODOLOGY
    # ════════════════════════════════════════════
    print(f"{'─'*72}")
    print(f"  METHODOLOGY")
    print(f"{'─'*72}")
    print(f"  Token counting: {method}")
    print(f"  Model: {MODEL}")
    print(f"  Reference project: cigar_band_identifier_v5 (file sizes only, no content exposed)")
    print(f"  Before JITCR: Actual pre-JITCR Project Instructions file ({len(before_content):,} bytes)")
    print(f"  After JITCR:  Actual current Tier 1/2/3 files from active project")
    print(f"  Tier 3 git log: Estimated at {git_tokens} tokens (5 oneline commits)")
    print(f"  Session longevity: Conservative estimates for avg message sizes")
    print(f"  Parameterized profiles: Offline estimation (3.8 chars/token)")
    print(f"  Cost pricing: As of Feb 2026, Anthropic published rates")
    print()

    # ── Build results dict ──
    results = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "method": method,
            "model": MODEL,
            "messages_per_session": messages,
            "framework_version": "1.3",
        },
        "benchmark_1_token_counts": {
            "before_jitcr": {"bytes": len(before_content), "tokens": before_tokens},
            "after_tier1": {"bytes": len(TIER1_CONTENT), "tokens": tier1_tokens},
            "after_tier2": {"bytes": len(tier2_content), "tokens": tier2_tokens},
            "after_tier3_handoff": {"bytes": len(handoff_content), "tokens": handoff_tokens, "file": handoff_name},
            "after_tier3_journals": journal_data,
            "after_tier3_git": {"tokens": git_tokens, "note": "estimated"},
            "after_tier3_total": tier3_total,
            "session_before_total": before_total,
            "session_after_total": after_total,
            "savings_tokens": savings,
            "savings_percent": round(pct, 1),
            "scaling": scaling,
        },
        "benchmark_2_cost": {
            "sessions_per_day": sessions_per_day,
            "working_days_per_month": days_per_month,
            "models": {}
        },
        "benchmark_3_longevity": {
            "context_window": CONTEXT_WINDOW,
            "avg_user_msg_tokens": avg_user_msg,
            "avg_response_tokens": avg_response,
            "avg_tool_overhead_tokens": avg_tool_overhead,
            "per_exchange_tokens": conversation_per_exchange,
            "exchanges_without_jitcr": exchanges_without,
            "exchanges_with_jitcr": exchanges_with,
            "extra_exchanges": gained,
            "extra_exchanges_percent": round(gained_pct, 1),
        },
        "benchmark_4_session_restore": {
            "jitcr_start_load_tokens": start_load,
            "manual_estimate_tokens": manual_estimate,
        },
        "mathematical_proof": {
            "breakeven_messages": round(1 + tier3_total / tier2_tokens, 1) if tier2_tokens > 0 else None,
            "formula": "Savings = T2 × (N - 1) - T3",
        },
    }

    # Add cost data
    for model_name, prices in PRICING.items():
        cpt = prices["input"] / 1_000_000
        results["benchmark_2_cost"]["models"][model_name] = {
            "price_per_m_input": prices["input"],
            "before_per_session": round(before_total * cpt, 6),
            "after_per_session": round(after_total * cpt, 6),
            "saved_per_session": round((before_total - after_total) * cpt, 6),
            "before_monthly": round(before_total * cpt * sessions_per_day * days_per_month, 4),
            "after_monthly": round(after_total * cpt * sessions_per_day * days_per_month, 4),
            "saved_monthly": round((before_total - after_total) * cpt * sessions_per_day * days_per_month, 4),
        }

    return results


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="JITCR Framework Token Benchmark")
    parser.add_argument("--offline", action="store_true", help="Use offline estimation instead of API")
    parser.add_argument("--messages", type=int, default=DEFAULT_MESSAGES, help=f"Messages per session (default: {DEFAULT_MESSAGES})")
    args = parser.parse_args()

    if args.offline:
        count_fn = count_tokens_offline
        method = "Offline estimation (3.8 chars/token, ±15-20%)"
    else:
        client = init_api_client()
        if client is None:
            print("Falling back to offline estimation.")
            count_fn = count_tokens_offline
            method = "Offline estimation (3.8 chars/token, ±15-20%)"
        else:
            count_fn = lambda text: count_tokens_api(client, text)
            method = "Anthropic count_tokens API (exact)"

    results = run_benchmark(count_fn, args.messages, method)

    # Save results
    output_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(output_dir, "benchmark_results.json")
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved to: {json_path}")


if __name__ == "__main__":
    main()
