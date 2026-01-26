---
description: Initialize technical phase - create feature branch and directory structure
handoffs:
  - label: Analyze Project Context
    agent: prd-context
    prompt: Analyze the project and generate context for this feature
    send: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Initialize the technical phase for a deliverable: create a feature branch, set up the spec directory structure, and prepare for implementation. This is the **transition point** from client-facing documents to AI-ready technical documents.

## Operating Constraints

**TECH LEAD ROLE**: Act as a Tech Lead initializing a new feature development.

**CLIENT APPROVAL ASSUMED**: Only use this command AFTER deliverables are approved by client.

**NO IMPLEMENTATION YET**: Only create structure, no actual code or detailed technical decisions.

## Pre-Flight Check: Deliverable Required

1. Identify the deliverable from $ARGUMENTS (ID, name, or path)
2. Verify the deliverable file exists in `prds/[feature]/deliverables/`
3. If not found:
   ```
   ⚠️ Deliverable Not Found
   
   Could not find deliverable matching: [input]
   
   Available deliverables:
   - [list from deliverables-map.json]
   
   → Provide a valid deliverable ID or path.
   ```

## Execution Steps

1. **Parse Input**: Extract deliverable ID from $ARGUMENTS

2. **Load Deliverable**: Read the deliverable file to get:
   - Deliverable name (`name`)
   - Deliverable ID (`id`)
   - Dependencies (`dependencies`)

3. **Determine Feature Number**: 
   - Check existing specs in `specs/` directory
   - Check any remote branches with `feat/` prefix
   - Use the **highest number found + 1**

4. **Generate Branch Name**:
   - Format: `feat/[XXX]-[short-name]`
   - Example: `feat/010-bulk-email-ui`

5. **Create Branch**:
   ```bash
   git checkout -b feat/[XXX]-[short-name]
   ```

6. **Create Directory Structure**:
   ```bash
   mkdir -p specs/[XXX]-[short-name]
   ```

7. **Create README Placeholder**:
   Create `specs/[XXX]-[short-name]/README.md`:
   ```markdown
   # [Feature Name]
   
   **Deliverable**: [link to deliverable file]
   **Branch**: feat/[XXX]-[short-name]
   **Status**: Initializing
   
   ## Documents
   - [ ] context.md - Project analysis (run @prd-context)
   - [ ] plan.md - Technical decisions (run @prd-plan)
   - [ ] tasks.md - Implementation tasks (run @prd-tasks)
   ```

8. **Copy Deliverable Reference**:
   - Copy or symlink the deliverable to `specs/[XXX]/deliverable.md`
   - This keeps the original user stories and acceptance criteria accessible

## Output Format

```
🚀 Feature Initialized

**Feature**: [XXX]-[feature-name]
**Branch**: feat/[XXX]-[feature-name]
**Directory**: specs/[XXX]-[feature-name]/

**Files Created**:
- README.md (status tracker)
- deliverable.md (copy from PRD deliverables)

**Deliverable Summary**:
- [X] user stories
- Priority: [HIGH/MEDIUM/LOW]
- Dependencies: [list or "None"]

**Next Step**: Run @prd-context to analyze the project and generate technical context.
```

## Context

{ARGS}
