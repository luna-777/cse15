# Codebook: Specific vs. Vague Prompts

**Unit of analysis:** one user prompt (single turn), typically one `user_prompt` row from `ai_usage_csv` / `data/user_prompts.csv`.  
**Codes:** mutually exclusive — assign exactly one primary code per prompt.  
**Optional:** add a secondary flag for edge cases (see §4).

---

## 1. Definitions

### SPECIFIC

A prompt that gives the model enough constraints that two competent readers would expect a **similar kind of answer**. It names or clearly implies at least two of:

| Dimension | What “clear” looks like |
|-----------|-------------------------|
| **Task** | What to do (write, explain, compare, fix, generate, summarize, explore…) |
| **Object** | What it’s about (topic, file, path, concept, feature, error…) |
| **Output form** | Format, length, structure, or genre (list, paragraph, code, table, report…) |
| **Constraints** | Audience, tone, scope, must-include / must-avoid, success criteria |

**Rule of thumb:** You could rewrite it as a short checklist of requirements without inventing major missing pieces.

### VAGUE

A prompt that leaves **central decisions open**, so competent readers could reasonably expect **very different** answers. Typical signals:

- Missing or unclear task (“help,” “thoughts,” “something about…”)
- Topic only, no ask (“climate change,” “my code”)
- Open-ended with no bounds (“tell me everything,” “make it better”)
- Pronouns / deixis with no recoverable referent (“fix this,” “continue,” “the usual,” “this tab”)
- Multiple incompatible reads with no preference stated

**Rule of thumb:** You would need to invent major requirements (what to produce, for whom, how long, about what) before answering.

---

## 2. Decision procedure (apply in order)

1. Is this a real user ask? If it is system noise, a local-command caveat, a single character, or a context-continuation dump with **no** new ask → **EXCLUDE** (not SPECIFIC/VAGUE).
2. Can you state the **task** in one verb phrase without guessing?  
   - No → **VAGUE**
3. Can you state the **object/topic** without guessing?  
   - No → **VAGUE**
4. Is at least one of **output form** or **constraints** present *or* strongly implied by genre (e.g. “write a Python function that…”)?  
   - Yes → **SPECIFIC**  
   - No, but task + object are clear and the expected answer type is narrow by convention → **SPECIFIC** (e.g. “What year did the Berlin Wall fall?”)  
   - No, and many answer shapes remain plausible → **VAGUE**

**Tie-break:** If unsure between SPECIFIC and VAGUE, code **VAGUE** (prefer under-claiming specificity).

---

## 3. Anchors (examples)

### SPECIFIC

| Prompt | Why |
|--------|-----|
| “Explain recursion to a first-year CS student in under 150 words, with one short Python example.” | Task + audience + length + form |
| “List 5 pros and 3 cons of using Redis for session storage in a Django app.” | Task + counts + domain |
| “Review the AI Usage tab CSV upload flow. Identify where `analyzeAiUsageCsv` is called, list required columns, and propose one minimal fix.” | Task + object + deliverables |
| “Explore `packages/engine/src/collect/`: list files, read `gitMetricsApi.ts`, summarize how commits are fetched.” | Task + paths + numbered form |
| “What year did the Berlin Wall fall?” | Closed factual ask; little room for divergent form |

### VAGUE

| Prompt | Why |
|--------|-----|
| “Help with my essay.” | Task weak; topic/output missing |
| “Make this better.” | No criteria or referent |
| “AI and education.” | Topic only |
| “Thoughts?” | No object or task |
| “Write something interesting.” | Task present; object/form/constraints absent |
| “lets work on testing. How high can we reasonably get in code coverage?” | Directional but no target files, threshold, or method |
| “by analyzing the logs will we be able to support this tap entirely?” | Referent (“this tap”) and criteria unclear |

### Borderline → resolve with procedure

| Prompt | Code | Note |
|--------|------|------|
| “Summarize photosynthesis.” | **SPECIFIC** | Task + object; short summary is conventional |
| “Tell me about photosynthesis.” | **VAGUE** | Open length/depth/angle |
| “Write a poem about the ocean.” | **SPECIFIC** | Task + object + form |
| “Write about the ocean.” | **VAGUE** | Form/angle open |
| “Debug my code” + full traceback + snippet attached | **SPECIFIC** | Object recoverable from context |
| “Debug my code” alone | **VAGUE** | Object not recoverable |
| “So i can merge this PR even when my other partner didn't merge her stuff yet right” | **SPECIFIC** | Clear closed workflow question |

### EXCLUDE (do not code SPECIFIC/VAGUE)

| Prompt pattern | Why |
|----------------|-----|
| `<local-command-caveat>…` only | Not a user ask |
| Single character / empty (`C`) | Not a prompt |
| Pure “session continued from previous conversation” summary with no new instruction | Continuation dump |
| Huge pasted model/tool output with no ask | Dump, not a prompt |

---

## 4. Optional secondary flags

Use only if useful for analysis (primary code remains SPECIFIC, VAGUE, or EXCLUDE):

| Flag | Meaning |
|------|---------|
| `CONTEXT_DEPENDENT` | Specificity relies on attached prior turn, `@path`, selection, or file contents |
| `PARTIAL` | Clear task *or* object, but not both (usually still **VAGUE** as primary) |
| `OVERSPECIFIED` | Specific but packed with conflicting constraints (still **SPECIFIC**) |

---

## 5. Coding sheet fields (suggested)

| Field | Values |
|-------|--------|
| `prompt_id` | string (stable id) |
| `primary_code` | `SPECIFIC` \| `VAGUE` \| `EXCLUDE` |
| `has_task` | Y/N |
| `has_object` | Y/N |
| `has_form` | Y/N |
| `has_constraints` | Y/N |
| `context_dependent` | Y/N |
| `exclude_reason` | short free text if EXCLUDE |
| `notes` | short free text |
| `coder_id` | string |

Source columns from `data/user_prompts.csv` often include: `result_id`, `repo_url`, `timestamp`, `session_id`, `message_text`.

---

## 6. Reliability tips

- Code from the **prompt text + available attachments in that row** only; don’t use the model’s later reply to decide specificity.
- Train on 20–50 pilot anchors before full coding; discuss disagreements.
- Report **% agreement** and preferably **Cohen’s κ** on an overlapping subset.
- Document project-specific overrides here when the team agrees on them.

---

## 7. Pilot tagging workflow

1. Sample ~30–50 prompts from `data/user_prompts.csv` (varied repos and lengths).
2. Apply this codebook independently (ideally two coders).
3. Resolve disagreements; update anchors or rules in this doc.
4. Then tag the full set.
