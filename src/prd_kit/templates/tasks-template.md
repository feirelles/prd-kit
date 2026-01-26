# Tasks: [FEATURE_NAME]

**Input**: plan.md, context.md, deliverable.md
**Generated**: [TIMESTAMP]

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
  - Read: `[TYPES_PATH]`

- [ ] T001 [Scaffold] Create type file
  - Location: `[FILE_PATH]`

- [ ] T002 [Implement] Define types
  - Details: [SPECIFICS]

**Checkpoint**: `npm run typecheck` passes

---

## Layer 1: Backend / API ([N] tasks)

**Purpose**: Create server endpoints

- [ ] T0XX [Context] Review API patterns
  - Read: `[API_PATH]`

- [ ] T0XX [Implement] [ENDPOINT_DESCRIPTION]
  - Location: `[FILE_PATH]`

**Checkpoint**: Endpoints return expected responses

---

## Layer 2: Data Layer ([N] tasks)

**Purpose**: Composables for data access

- [ ] T0XX [Context] Review composable patterns
  - Read: `[COMPOSABLES_PATH]`

- [ ] T0XX [Implement] [COMPOSABLE_NAME]
  - Location: `[FILE_PATH]`

**Checkpoint**: Data loads successfully

---

## Layer 3: UI Components ([N] tasks)

**Purpose**: Presentational components

- [ ] T0XX [Context] Review UI patterns
  - Skill: `[SKILL_PATH]`

- [ ] T0XX [P] [Scaffold] Create components
  - Location: `[COMPONENTS_PATH]`

- [ ] T0XX [Implement] [COMPONENT_NAME]
  - Details: [SPECIFICS]

**Checkpoint**: Components render with mock data

---

## Layer 4: Page Integration ([N] tasks)

**Purpose**: Wire everything together

- [ ] T0XX [Scaffold] Create page
  - Location: `[PAGE_PATH]`

- [ ] T0XX [Implement] State management
  - Details: [SPECIFICS]

- [ ] T0XX [Implement] Wire components
  - Details: [SPECIFICS]

**Checkpoint**: Full flow works end-to-end

---

## Layer 5: Polish & Validation ([N] tasks)

**Purpose**: Production readiness

- [ ] T0XX [Implement] Error handling

- [ ] T0XX [Implement] Loading states

- [ ] T0XX [Test] Validate acceptance criteria
  - [AC_LIST]

**Final Checkpoint**: All ACs pass, production-ready

---

## AC Coverage

| AC | Task(s) |
|----|---------|
| [AC_ID] | [TASK_IDS] |

---

## Notes

- [NOTES]
