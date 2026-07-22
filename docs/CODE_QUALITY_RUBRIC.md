# Code Quality Rubric

## Details

A four-dimension rubric—**readability**, **naming**, **structure**, and **error handling**—scored on a **1–5** scale (5 = best) by **≥ 2 team members** independently on a **sampled set** of **AI- and human-labeled** code regions. Report **inter-rater reliability (Cohen's κ)** per dimension. Scores reflect **subjective judgment**, not ground truth; this captures what **static tools miss** without pretending to be objective.

## How to score

- Score each dimension **independently** from 1 to 5.
- Pick the **lowest level whose description fully fits** the region; if signals are mixed, choose the lower score.
- Use **Observable signals** as evidence; cite file and line in calibration notes when possible.
- When unsure between **3 (Adequate)** and **4 (Good)**, ask: *Would I merge this without asking for changes?* Yes → 4 or higher; no → 3 or lower.

## Scoring scale

| Level | Label | Meaning |
|-------|-------|---------|
| **5** | **Excellent** | Exceeds expectations; no meaningful issues |
| **4** | **Good** | Meets expectations; minor polish only |
| **3** | **Adequate** | Acceptable baseline; meets minimum bar with clear room to improve |
| **2** | **Fair** | Partially meets expectations; noticeable issues |
| **1** | **Needs work** | Below expectations; revision required |

## Quick reference

| Category | Excellent (5) | Good (4) | Adequate (3) | Fair (2) | Needs work (1) |
|----------|---------------|----------|--------------|----------|----------------|
| **Readability** | Effortless to read; consistent formatting throughout | Clear and readable; tiny style nits only | Readable; minor inconsistencies or one dense block | Readable with effort; inconsistent spacing or long blocks | Hard to follow; messy or dense layout |
| **Naming** | Every name reveals intent and matches conventions | Names are clear; one or two could be sharper | Mostly clear; a few generic names that do not mislead | Several vague or inconsistent names | Names obscure behavior or ignore style |
| **Structure** | Focused modules; obvious flow and organization | Solid layout; minor duplication or nesting | Organization works; one extractable block or mild nesting | Hard to locate logic; weak separation of concerns | Tangled, duplicated, or misplaced code |
| **Error handling** | Failures visible and appropriate; edge cases handled thoughtfully | Main paths handle errors; minor edge-case gaps | Required paths covered; some vague messages or gaps | Errors swallowed, vague, or inconsistent | Silent failures, crashes on bad input, or misleading behavior |

---

## 1. Readability

How easy the code is for a reader to follow.

### Levels

**Excellent (5)** — Formatting is consistent (indentation, spacing, line breaks). Lines stay near ~88 characters unless a longer line reads naturally. Related code is grouped with blank lines between sections (imports → types/constants → helpers → main logic). Comments explain non-obvious *why*, not obvious *what*. TypeScript types and Python control flow are easy to trace.

**Good (4)** — Mostly consistent formatting with one or two minor style inconsistencies. Code is scannable without re-reading. Comments are helpful and not noisy. Exported TypeScript functions have readable types; Python control flow is straightforward.

**Adequate (3)** — Generally readable but with a few fixable issues: occasional long lines, one dense block, or a missing comment where logic is non-obvious. Formatting is mostly consistent; a reader can follow the code without stopping more than once or twice.

**Fair (2)** — Inconsistent indentation or spacing in places. Some long lines or dense blocks force re-reading. Comments are missing where logic is tricky, or restate the code without adding value.

**Needs work (1)** — Formatting varies widely. Large walls of code with little structure. Hard to see where one idea ends and another begins.

### Observable signals

- Consistent indent width (2 or 4 spaces); no mixed tabs and spaces.
- No trailing whitespace; stable quote and brace style within a file.
- Lines near ~88 characters; horizontal scrolling is rare.
- Blank lines separate imports, constants, helpers, and main logic.
- Comments explain *why* for non-obvious branches, workarounds, or invariants.
- TypeScript: explicit return types on exported functions; `any` avoided or justified in a comment.
- Python: loops and conditionals are straightforward; deeply nested comprehensions are absent or short.

### Red flags (score ≤ 2)

- Mixed tabs and spaces in the same file.
- Functions of 80+ lines with no internal sectioning or helper extraction.
- Large blocks of commented-out dead code left in place.
- Comments that only narrate what the next line already says (`// increment i`).

### Checklist

- [ ] Indentation is consistent (spaces or tabs—not mixed).
- [ ] Lines are reasonably short (~88 characters is a useful guide, not a pass/fail rule).
- [ ] Blank lines separate logical sections (imports, helpers, main logic).
- [ ] Comments explain intent where code alone is unclear—not redundant narration.
- [ ] TypeScript: types are readable on exports; `any` is rare and justified.
- [ ] Python: control flow (loops, conditionals) is straightforward to follow.
- [ ] No trailing whitespace or obviously inconsistent quote style within a file.
- [ ] Dense blocks are broken up or commented where a reader would pause.

---

## 2. Naming

Whether identifiers and files communicate purpose to a reader.

### Levels

**Excellent (5)** — Names are descriptive and match behavior. TypeScript uses `camelCase` for variables and functions; Python uses `snake_case`. Files and modules are named for what they contain. Booleans read as questions (`isValid`, `has_error`); functions read as verbs (`calculateTotal`, `parse_input`). Constants follow language norms (`SCREAMING_SNAKE` in TS/JS; module-level `snake_case` in Python).

**Good (4)** — Names are clear overall. One or two identifiers could be more specific but do not mislead. File and module names match their primary responsibility.

**Adequate (3)** — Most names are understandable; a few generic names (`data`, `result`) appear in narrow scope where meaning is clear from context. Style conventions are mostly followed.

**Fair (2)** — Several generic names (`data`, `temp`, `x`) or inconsistent style (mixing camelCase and snake_case in the wrong language). Reader must guess meaning from context.

**Needs work (1)** — Names hide behavior, duplicate meanings, or ignore language conventions. Files do not reflect their contents.

### Observable signals

- Variables use nouns or noun phrases (`userCount`, `chunk_path`).
- Functions and methods use verbs (`fetchUser`, `parse_input`).
- Booleans sound like yes/no questions (`canRetry`, `is_loaded`).
- No single-letter names except loop indices (`i`, `j`, `k`).
- File names match primary export or responsibility (`auth_service.py`, `useAuth.ts`).
- TypeScript: `camelCase` for variables, functions, and methods; `PascalCase` for types and components.
- Python: `snake_case` for variables, functions, and modules; `PascalCase` for classes.

### Red flags (score ≤ 2)

- Single-letter names outside loop indices in non-trivial logic.
- `camelCase` in Python or `snake_case` in TypeScript for ordinary identifiers.
- Misleading names (e.g. `getUser` that deletes, `isValid` that mutates state).
- Multiple unrelated concepts sharing the same generic name (`data`, `temp`) in one function.

### Checklist

- [ ] No single-letter names except loop indices (`i`, `j`, `k`).
- [ ] Variables and functions describe *what* they hold or *do*.
- [ ] TypeScript: `camelCase` for variables, functions, and methods.
- [ ] Python: `snake_case` for variables, functions, and modules.
- [ ] Boolean names sound like yes/no questions.
- [ ] File names match the module's purpose (e.g. `greet.ts`, `parse_data.py`).
- [ ] Constants follow language-appropriate conventions.
- [ ] Names remain accurate after behavior changes (no stale verbs or nouns).

---

## 3. Structure

How code is organized across files, functions, and modules.

### Levels

**Excellent (5)** — Each function has one clear job. Code lives in sensible files and folders. Nesting is shallow; early returns clarify logic where helpful. No dead or duplicated blocks. TypeScript exports are intentional; Python functions are grouped logically. Functions sit in a healthy ~15–40 line range unless the task naturally requires more with clear sectioning.

**Good (4)** — Organization is sound. A function may be slightly long or one block could be extracted, but flow is still clear. Imports are ordered; responsibilities are easy to locate.

**Adequate (3)** — Structure works for the task. One mildly long function, a small duplicated snippet, or nesting up to three levels is acceptable if the reader can still follow the flow without a map.

**Fair (2)** — Logic is hard to find or split across files without reason. Noticeable copy-paste or deep nesting. Imports or exports are disorganized.

**Needs work (1)** — Responsibilities are mixed; files are misplaced. Large duplicated sections or unclear entry points make changes risky.

### Observable signals

- Each function does one cohesive job (or one step in a clear pipeline).
- Files have a single dominant responsibility—not “god files” mixing unrelated domains.
- Nesting stays at three levels or less, or deeper blocks are extracted into helpers.
- Imports grouped: stdlib → third-party → local; no obvious unused imports.
- TypeScript: explicit exports; no accidental globals.
- Python: related helpers grouped; no unreachable code after `return`.
- Business logic is separated from wiring (routes/handlers delegate to services or helpers).

### Red flags (score ≤ 2)

- Copy-pasted logic that should be a shared helper.
- Business rules embedded entirely in route handlers with no extraction path.
- Dead code paths or unreachable blocks after `return`/`throw`.
- Circular import workarounds (lazy imports, import inside functions) without comment explaining why.

### Checklist

- [ ] Each function does one thing well (or one cohesive step in a pipeline).
- [ ] Source files are organized by purpose and location.
- [ ] No copy-pasted logic that should be a shared helper.
- [ ] Nesting is limited; early returns used where they improve clarity.
- [ ] Imports appear at the top and are organized (stdlib, third-party, local).
- [ ] TypeScript: exports are deliberate, not accidental globals.
- [ ] Python: related functions are grouped; no unreachable or dead code.
- [ ] Functions and files are a reasonable size for their responsibility.
- [ ] Entry points (main, handlers, exported API) are easy to identify.

---

## 4. Error handling

How the code deals with failure.

### Levels

**Excellent (5)** — Failures are visible, appropriate, and easy to reason about. Edge cases are handled thoughtfully. A reader can predict what happens when inputs go wrong. Error messages are actionable; resources are cleaned up (`with`, `try/finally`, effect cleanup).

**Good (4)** — Main paths handle errors correctly. Minor gaps in edge cases that do not undermine required behavior. Messages are mostly helpful.

**Adequate (3)** — Required failure paths are covered, but messages may be generic or one edge case is only partially handled. No silent success on failure; crashes on expected bad input are absent.

**Fair (2)** — Errors are swallowed, messages are vague, or handling is inconsistent across similar cases.

**Needs work (1)** — Silent failures, crashes on expected bad input, or behavior that misleads a reader about success vs failure.

### Observable signals

- Null, empty, and invalid inputs are handled where the API contract requires it.
- Errors are surfaced (return, throw, or log)—not silently ignored.
- Messages state what failed and give enough context to debug (`Invalid user id: 0`).
- Similar operations fail the same way across the module.
- Resources (files, connections, handles) are closed on failure paths.
- Empty collections, missing config, and timeouts are handled or explicitly documented as out of scope.

### Red flags (score ≤ 2)

- Bare `except:` or empty `catch` blocks that swallow errors.
- Success returned or reported when an operation failed.
- Crash (uncaught exception) on expected bad input (empty string, null, out-of-range index).
- Generic user-facing text with no diagnostic detail (`Something went wrong` only).

### Checklist

- [ ] Invalid or empty inputs are handled where the task requires it.
- [ ] Errors are surfaced or returned—not silently ignored.
- [ ] Error messages (if any) help a reader understand what went wrong.
- [ ] No obvious logic bugs in failure paths.
- [ ] Similar operations use consistent error patterns (throw vs return vs Result).
- [ ] Resources are released on failure (`with`, `try/finally`, cleanup callbacks).
- [ ] Edge cases (empty lists, missing files, network failure) are addressed or scoped out explicitly.
- [ ] Callers can distinguish failure from success without reading implementation details.
