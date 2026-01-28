---
description: Generate implementation tasks organized by technical layer with testable checkpoints
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Generate a `tasks.md` file with implementation tasks organized by **technical layer** (not by user story). Each layer has a **testable checkpoint** so progress can be validated incrementally.

## Operating Constraints

**TECH LEAD ROLE**: Act as a Tech Lead breaking down work into actionable tasks.

**LAYER-FIRST**: Organize by technical layer, not by user story. This prevents context switching between frontend/backend.

**TESTABLE CHECKPOINTS**: Each layer must end with a verification step.

**CONTEXT-AWARE**: Every implementation task should reference relevant skills/instructions.

## Pre-Flight Check: Plan Required

1. **Setup**: Run setup script to get paths:
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null || echo "ERROR: Run from git repository root")/.prd-kit/scripts" && python -m prd_scripts.setup_tasks --spec "[spec-identifier]" --json
   ```

2. Verify the JSON output:
   - `STATUS` should be `ready`
   - `HAS_PLAN` should be `true`

3. If status is `missing_plan`:
   ```
   ⚠️ Plan Not Generated
   
   Could not find plan.md for: [input]
   
   → Run @prd-plan first to generate the technical plan.
   ```

## Layer Structure

Tasks are organized into 6 layers:

| Layer | Purpose | Checkpoint |
|-------|---------|------------|
| **0** | Types & Interfaces | `npm run typecheck` passes |
| **1** | Backend / API | Endpoints return mock responses |
| **2** | Data Layer | Composables load real data |
| **3** | UI Components | Components render with mock data |
| **4** | Page Integration | Full flow works end-to-end |
| **5** | Polish & Validation | Production-ready, all ACs pass |

## Task Format

Each task follows this format:

```markdown
- [ ] T[NNN] [Tag] Description
  - Location: `path/to/file`
  - Pattern: Reference to existing file (if applicable)
  - Skill: `.github/skills/[name]/SKILL.md` (if applicable)
  - Details: Implementation specifics
```

### Tags

| Tag | Meaning |
|-----|---------|
| `[Context]` | Read files/skills before implementing |
| `[Scaffold]` | Create file structure with stubs |
| `[Implement]` | Write actual implementation |
| `[Test]` | Verify functionality |
| `[P]` | Can run in parallel with adjacent [P] tasks |

## Execution Steps

1. **Parse Input**: Extract spec directory from $ARGUMENTS

2. **Load Inputs**:
   - Read `specs/[XXX]/plan.md` - Layer breakdown, decisions
   - Read `specs/[XXX]/context.md` - Skills, patterns
   - Read `specs/[XXX]/deliverable.md` - Acceptance criteria
   - Read `.prd-kit/memory/tech-constitution.md` - Coding standards

3. **For Each Layer in Plan**:
   - Extract components/files to create
   - Generate scaffold task (create with stubs)
   - Generate implementation tasks
   - **Enforce Standards**: Ensure tasks include "Use [standard] naming" or "Follow [pattern] from Constitution"
   - Add checkpoint verification step

4. **Add Context Tasks**: For each layer that requires skills:
   - Add `[Context]` task to read relevant skills
   - Add `[Context]` task to analyze existing patterns

5. **Map Acceptance Criteria**: Ensure each AC from deliverable is covered by at least one task

6. **Generate tasks.md**: Create `specs/[XXX]/tasks.md`

## Output Format: tasks.md

```markdown
# Tasks: [Feature Name]

**Input**: plan.md, context.md, deliverable.md
**Generated**: [timestamp]

---

## Summary

| Layer | Tasks | Purpose |
|-------|-------|---------|
| 0 | [N] | Types & Interfaces |
| 1 | [N] | Backend / API |
| 2 | [N] | Data Layer |
| 3 | [N] | UI Components |
| 4 | [N] | Page Integration |
| 5 | [N] | Polish & Validation |
| **Total** | **[N]** | |

---

## Layer 0: Types & Interfaces ([N] tasks)

**Purpose**: Define all data contracts before implementation

- [ ] T000 [Context] Review existing type patterns
  - Read: `shared/types/` for naming conventions
  - Read: Existing similar types

- [ ] T001 [Scaffold] Create type file
  - Location: `shared/types/[feature].ts`
  - Content: Interface stubs with TODO comments

- [ ] T002 [Implement] Define [TypeName] interface
  - Details: [what fields, based on plan.md]

**Checkpoint**: `npm run typecheck` passes with new types

---

## Layer 1: Backend / API ([N] tasks)

**Purpose**: Create server endpoints (skip if no backend needed)

- [ ] T0XX [Context] Review API patterns
  - Read: `server/api/` structure
  - Read: Error handling conventions

- [ ] T0XX [Scaffold] Create endpoint files
  - Location: `server/api/[feature]/`
  - Content: Empty handlers with throw Error('Not implemented')

- [ ] T0XX [Implement] [Endpoint description]
  - Method: GET/POST/etc.
  - Details: [implementation specifics]

**Checkpoint**: Endpoints return expected response structure

---

## Layer 2: Data Layer ([N] tasks)

**Purpose**: Composables for data access and business logic

- [ ] T0XX [Context] Review composable patterns
  - Read: Existing composables in `composables/`
  - Focus: Return types, error handling

- [ ] T0XX [Scaffold] Create composable file
  - Location: `composables/use[Feature].ts`
  - Content: Empty functions returning stubs

- [ ] T0XX [Implement] [Composable function]
  - Details: [what it does]

**Checkpoint**: Composable successfully fetches/processes data

---

## Layer 3: UI Components ([N] tasks)

**Purpose**: Presentational components

- [ ] T0XX [Context] Review UI patterns and skills
  - Skill: `.github/skills/[relevant]/SKILL.md`
  - Pattern: `components/[Similar]/[Component].vue`

- [ ] T0XX [P] [Scaffold] Create [ComponentA].vue
  - Location: `components/[Feature]/[ComponentA].vue`
  - Content: Empty component with props/emits stubs

- [ ] T0XX [P] [Scaffold] Create [ComponentB].vue
  - Location: `components/[Feature]/[ComponentB].vue`
  - Content: Empty component with props/emits stubs

- [ ] T0XX [Implement] [ComponentA] functionality
  - Props: [list]
  - Emits: [list]
  - Details: [implementation]

**Checkpoint**: Components render correctly with mock data

---

## Layer 4: Page Integration ([N] tasks)

**Purpose**: Wire everything together in the page

- [ ] T0XX [Context] Review page coordinator pattern
  - Read: `.github/instructions/pages.*.md`
  - Pattern: Similar existing pages

- [ ] T0XX [Scaffold] Create page file
  - Location: `pages/[path].vue`
  - Content: Empty page with definePageMeta

- [ ] T0XX [Implement] Page state management
  - Details: Define refs, computed, watchers

- [ ] T0XX [Implement] Wire components
  - Details: Pass props, handle emits

- [ ] T0XX [Implement] Main workflow logic
  - Details: [the core feature flow]

**Checkpoint**: Full user flow works end-to-end

---

## Layer 5: Polish & Validation ([N] tasks)

**Purpose**: Edge cases, error handling, final verification

- [ ] T0XX [Implement] Error handling
  - Details: try/catch, error toasts, retry buttons

- [ ] T0XX [Implement] Loading states
  - Details: Skeletons, spinners, disabled states

- [ ] T0XX [Implement] Edge cases
  - Details: Empty states, validation, boundaries

- [ ] T0XX [Test] Validate Acceptance Criteria
  - AC1: [description] → [how to test]
  - AC2: [description] → [how to test]
  - ...

- [ ] T0XX [Test] Performance validation
  - Details: Test with realistic data volume

**Final Checkpoint**: All acceptance criteria pass, feature production-ready

---

## Acceptance Criteria Coverage

| AC | Description | Task(s) |
|----|-------------|---------|
| AC1 | [from deliverable] | T0XX, T0XX |
| AC2 | [from deliverable] | T0XX |
| ... | ... | ... |

---

## Parallel Opportunities

Tasks marked with [P] can be executed in parallel:
- Layer 3: Component scaffolding
- Layer 5: Independent polish items

---

## Notes

- [Any additional context]
- [Known constraints]
- [Dependencies on external systems]
```

## Command Output

```
📋 Tasks Generated

**Feature**: [XXX]-[feature-name]
**File**: specs/[XXX]-[feature-name]/tasks.md

**Summary**:
- [N] total tasks across 6 layers
- [N] context tasks (read before implement)
- [N] parallel opportunities
- All [N] acceptance criteria covered

**Estimated Effort**: [X-Y days]

**Ready for Implementation**: Start with Layer 0, proceed sequentially.
```

## Context

{ARGS}
