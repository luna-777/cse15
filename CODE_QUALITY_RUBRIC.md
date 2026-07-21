# Code Quality Rubric

## Details

A short 4-item rubric—**readability**, **naming**, **structure**, and **error handling**—scored by **≥ 2 team members** independently on a **sampled set** of **AI- and human-labeled** code regions. Report **inter-rater reliability (Cohen's κ)** per dimension. Scores reflect **subjective judgment**, not ground truth; this captures what **static tools miss** without pretending to be objective.

## Scoring scale

| Level | Label | Meaning |
|-------|-------|---------|
| 4 | **Excellent** | Exceeds expectations; no meaningful issues |
| 3 | **Good** | Meets expectations; minor polish only |
| 2 | **Fair** | Partially meets expectations; noticeable issues |
| 1 | **Needs work** | Below expectations; revision required |

## Quick reference

| Category | Excellent (4) | Good (3) | Fair (2) | Needs work (1) |
|----------|---------------|----------|----------|----------------|
| **Readability** | Effortless to read; consistent formatting throughout | Clear and readable; tiny style nits only | Readable with effort; inconsistent spacing or long blocks | Hard to follow; messy or dense layout |
| **Naming** | Every name reveals intent and matches conventions | Names are clear; one or two could be sharper | Several vague or inconsistent names | Names obscure behavior or ignore style |
| **Structure** | Focused modules; obvious flow and organization | Solid layout; minor duplication or nesting | Hard to locate logic; weak separation of concerns | Tangled, duplicated, or misplaced code |
| **Error handling** | Failures visible and appropriate; edge cases handled thoughtfully | Main paths handle errors; minor edge-case gaps | Errors swallowed, vague, or inconsistent | Silent failures, crashes on bad input, or misleading behavior |

---

## 1. Readability

How easy the code is for a reader to follow.

### Levels

**Excellent (4)** — Formatting is consistent (indentation, spacing, line breaks). Lines are reasonably short. Related code is grouped with blank lines between sections. Comments explain non-obvious *why*, not obvious *what*. TypeScript types and Python control flow are easy to trace.

**Good (3)** — Mostly consistent formatting with one or two minor style inconsistencies. Code is scannable without re-reading. Comments are helpful and not noisy.

**Fair (2)** — Inconsistent indentation or spacing in places. Some long lines or dense blocks. Comments are missing where logic is tricky, or restate the code without adding value.

**Needs work (1)** — Formatting varies widely. Large walls of code with little structure. Hard to see where one idea ends and another begins.

### Checklist

- [ ] Indentation is consistent (spaces or tabs—not mixed).
- [ ] Lines are reasonably short (~88 characters is a useful guide, not a pass/fail rule).
- [ ] Blank lines separate logical sections (imports, helpers, main logic).
- [ ] Comments explain intent where code alone is unclear—not redundant narration.
- [ ] TypeScript: types are readable, not overly clever.
- [ ] Python: control flow (loops, conditionals) is straightforward to follow.

---

## 2. Naming

Whether identifiers and files communicate purpose to a reader.

### Levels

**Excellent (4)** — Names are descriptive and match behavior. TypeScript uses `camelCase` for variables and functions; Python uses `snake_case`. Files and modules are named for what they contain. Booleans read as questions (`isValid`, `has_error`); functions read as verbs (`calculateTotal`, `parse_input`).

**Good (3)** — Names are clear overall. One or two identifiers could be more specific but do not mislead.

**Fair (2)** — Several generic names (`data`, `temp`, `x`) or inconsistent style (mixing camelCase and snake_case in the wrong language). Reader must guess meaning from context.

**Needs work (1)** — Names hide behavior, duplicate meanings, or ignore language conventions. Files do not reflect their contents.

### Checklist

- [ ] No single-letter names except loop indices (`i`, `j`, `k`).
- [ ] Variables and functions describe *what* they hold or *do*.
- [ ] TypeScript: `camelCase` for variables, functions, and methods.
- [ ] Python: `snake_case` for variables, functions, and modules.
- [ ] Boolean names sound like yes/no questions.
- [ ] File names match the module's purpose (e.g. `greet.ts`, `parse_data.py`).

---

## 3. Structure

How code is organized across files, functions, and modules.

### Levels

**Excellent (4)** — Each function has one clear job. Code lives in sensible files and folders. Nesting is shallow; early returns clarify logic where helpful. No dead or duplicated blocks. TypeScript exports are intentional; Python functions are grouped logically.

**Good (3)** — Organization is sound. A function may be slightly long or one block could be extracted, but flow is still clear.

**Fair (2)** — Logic is hard to find or split across files without reason. Noticeable copy-paste or deep nesting. Imports or exports are disorganized.

**Needs work (1)** — Responsibilities are mixed; files are misplaced. Large duplicated sections or unclear entry points make changes risky.

### Checklist

- [ ] Each function does one thing well (or one cohesive step in a pipeline).
- [ ] Source files are organized by purpose and location.
- [ ] No copy-pasted logic that should be a shared helper.
- [ ] Nesting is limited; early returns used where they improve clarity.
- [ ] Imports appear at the top and are organized (stdlib, third-party, local).
- [ ] TypeScript: exports are deliberate, not accidental globals.
- [ ] Python: related functions are grouped; no unreachable or dead code.

---

## 4. Error handling

How the code deals with failure.

### Levels

**Excellent (4)** — Failures are visible, appropriate, and easy to reason about. Edge cases are handled thoughtfully. A reader can predict what happens when inputs go wrong.

**Good (3)** — Main paths handle errors correctly. Minor gaps in edge cases that do not undermine required behavior.

**Fair (2)** — Errors are swallowed, messages are vague, or handling is inconsistent across similar cases.

**Needs work (1)** — Silent failures, crashes on expected bad input, or behavior that misleads a reader about success vs failure.

### Checklist

- [ ] Invalid or empty inputs are handled where the task requires it.
- [ ] Errors are surfaced or returned—not silently ignored.
- [ ] Error messages (if any) help a reader understand what went wrong.
- [ ] No obvious logic bugs in failure paths.
