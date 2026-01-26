---
description: Analyze project codebase and generate technical context for a feature
handoffs:
  - label: Generate Technical Plan
    agent: prd-plan
    prompt: Generate the technical plan based on the context
    send: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Analyze the existing codebase and generate a `context.md` file that provides the AI with all necessary information to make informed technical decisions. This is **just-in-time context discovery** - no stale memory files to maintain.

## Operating Constraints

**ARCHITECT ROLE**: Act as a Solutions Architect analyzing an existing codebase.

**DISCOVERY ONLY**: Analyze and document, don't make decisions yet.

**NO ASSUMPTIONS**: If something is unclear, note it in "Open Questions" section.

## Pre-Flight Check: Feature Directory Required

1. Identify the spec directory from $ARGUMENTS
2. Verify `specs/[XXX]-[name]/` exists
3. If not found:
   ```
   ⚠️ Feature Not Initialized
   
   Could not find spec directory for: [input]
   
   → Run @prd-init-feature first to create the feature structure.
   ```

## Analysis Scope

Analyze these areas of the project:

### 1. Project Stack Detection

Examine configuration files to detect:
- **Frontend**: package.json (Vue, React, Nuxt, Next, etc.)
- **Backend**: package.json, requirements.txt, go.mod, etc.
- **Database**: Check for PocketBase, Prisma, Drizzle, etc.
- **UI Library**: @nuxt/ui, shadcn, Vuetify, etc.

### 2. Directory Structure Analysis

Identify project conventions:
- Where are components stored?
- Where are pages/routes?
- Where are composables/hooks?
- Where are API routes/endpoints?
- Where are types/interfaces?

### 3. Existing Patterns Discovery

Search for patterns relevant to this feature:
- Similar components (tables, modals, forms)
- Composables that could be reused
- API endpoint patterns
- State management approach

### 4. Previous Specs Analysis

Read existing specs for context:
- Check `specs/*/plan.md` for prior technical decisions
- Check `specs/*/context.md` for lessons learned
- Identify dependencies from related features

### 5. Skills and Instructions Discovery

Check for available guidance:
- `.github/skills/*/SKILL.md` - Domain expertise
- `.github/instructions/*.md` - Coding guidelines

## Execution Steps

1. **Parse Input**: Extract spec directory from $ARGUMENTS

2. **Load Deliverable**: Read `specs/[XXX]/deliverable.md` for user stories

3. **Detect Project Stack**:
   ```bash
   # Check common config files
   cat package.json | head -50
   ls -la
   ```

4. **Load Technical Constitution**: 
   - Read `.prd-kit/memory/tech-constitution.md`
   - **CRITICAL**: Use this to filter discovered patterns. Only patterns aligned with the constitution should be recommended.

5. **Analyze Directory Structure**:
   ```bash
   # List key directories
   ls -la app/ src/ components/ pages/ server/
   ```

6. **Search for Relevant Patterns**: Based on deliverable requirements:
   - If needs table → search for existing table components
   - If needs modal → search for modal patterns
   - If needs API → check server/api structure

7. **Read Previous Specs**:
   ```bash
   ls specs/
   # For relevant ones, read plan.md
   ```

8. **Discover Skills/Instructions**:
   ```bash
   ls .github/skills/
   ls .github/instructions/
   ```

9. **Generate context.md**: Create `specs/[XXX]/context.md`

## Output Format: context.md

```markdown
# Context: [Feature Name]

**Generated**: [timestamp]
**Deliverable**: [link to deliverable]

---

## Project Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Framework | Nuxt 4 | 4.x |
| UI Library | @nuxt/ui | 3.x |
| State | Pinia | 2.x |
| Backend | PocketBase | 0.22.x |

---

## Directory Structure

```
[project-root]/
├── app/
│   ├── components/     # Vue components
│   ├── composables/    # Reusable logic
│   ├── pages/          # File-based routing
│   └── stores/         # Pinia stores
├── server/
│   └── api/            # Server routes
└── shared/
    └── types/          # TypeScript types
```

---

## Reusable Patterns

### Tables
- **Location**: `components/Tasks/Table.vue`
- **Library**: TanStack Vue Table
- **Features**: Selection, sorting, pagination

### Modals
- **Location**: `components/Email/PreviewModal.vue`
- **Pattern**: UModal with v-model:open

### Composables
| Name | Purpose | Reuse Potential |
|------|---------|-----------------|
| `useEmailService()` | Email sending | Direct reuse |
| `useBulkCollectionTasks()` | Data loading | Reference pattern |

---

## Related Previous Specs

| Spec | Relevance |
|------|-----------|
| 004-email-service | API endpoints to consume |
| 007-collection-tasks | Data model reference |

---

## Available Skills

| Skill | When to Use |
|-------|-------------|
| tanstack-table | Table implementation |
| nuxt-ui | UI component patterns |
| pinia-stores | State management |

---

## Available Instructions

| Instruction | Applies To |
|-------------|------------|
| pages.list-coordinator | Page state management |
| ui.tables | Table loading patterns |

---

## Open Questions

- [Any unclear aspects that need user input]
```

## Command Output

```
📊 Context Generated

**Feature**: [XXX]-[feature-name]
**File**: specs/[XXX]-[feature-name]/context.md

**Analysis Summary**:
- Stack: [Framework] + [UI Library]
- [N] reusable patterns identified
- [N] related specs referenced
- [N] skills available

**Next Step**: Run @prd-plan to generate the technical plan.
```

## Context

{ARGS}
