# Plan: [FEATURE_NAME]

**Generated**: [TIMESTAMP]
**Deliverable**: [LINK]
**Context**: [LINK]

---

## Technical Summary

| Aspect | Decision |
|--------|----------|
| Route | `[ROUTE_PATH]` |
| Components | [N] new in `components/[FEATURE]/` |
| Composables | [REUSE_LIST] / [CREATE_LIST] |
| State | [PAGE_LEVEL/STORE] |
| API Changes | [NONE/DESCRIBE] |

---

## Architecture

### Component Tree

```
Page: pages/[PATH].vue (Coordinator)
├── [COMPONENT_1]
│   └── Pattern: [REFERENCE]
├── [COMPONENT_2]
│   └── Pattern: [REFERENCE]
└── [COMPONENT_3]
```

### Data Flow

```
[DESCRIPTION_OF_DATA_FLOW]
```

---

## Layer Breakdown

### Layer 0: Types & Interfaces

**Location**: `[TYPES_PATH]`

| Type | Purpose |
|------|---------|
| `[TYPE_1]` | [DESCRIPTION] |

### Layer 1: Backend (if applicable)

**Location**: `[API_PATH]`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `[ENDPOINT]` | [METHOD] | [DESCRIPTION] |

### Layer 2: Data Layer

**Location**: `[COMPOSABLES_PATH]`

| Composable | Reuse | Purpose |
|------------|-------|---------|
| `[NAME]` | [EXISTING/NEW] | [DESCRIPTION] |

### Layer 3: UI Components

**Location**: `[COMPONENTS_PATH]`

| Component | Pattern From | Key Props |
|-----------|--------------|-----------|
| `[NAME]` | [REFERENCE] | [PROPS] |

### Layer 4: Page Integration

**Location**: `[PAGES_PATH]`

| Responsibility | Implementation |
|----------------|----------------|
| State | [APPROACH] |
| Events | [APPROACH] |

### Layer 5: Polish

| Item | Approach |
|------|----------|
| Errors | [APPROACH] |
| Loading | [APPROACH] |
| Edge cases | [LIST] |

---

## Skills to Read

| Layer | Skill | Sections |
|-------|-------|----------|
| [N] | [SKILL] | [SECTIONS] |

---

## Acceptance Criteria Mapping

| AC | Layer | Implementation |
|----|-------|----------------|
| [AC_ID] | [LAYER] | [HOW] |

---

## Open Decisions

- [DECISION_NEEDED]
