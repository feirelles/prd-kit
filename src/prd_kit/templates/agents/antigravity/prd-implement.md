---
description: Execute implementation tasks from tasks.md following the technical plan
---

This workflow executes the implementation tasks layer by layer.

1. **Load Context**
   Ask user for spec identifier.
   Read the following files:
   - `specs/[spec-id]/tasks.md` (The todo list)
   - `specs/[spec-id]/plan.md` (The blueprint)
   - `specs/[spec-id]/context.md` (The reference manual)
   - `.prd-kit/memory/tech-constitution.md` (The law)

2. **Execute Layer Loop**
   For each Layer (0 to 5):
   
   a. **Scan for [Context] Tasks**
      - Find all tasks marked `[Context]` in the current layer.
      - **CRITICAL**: Read EVERY file or skill referenced in these tasks using `readFile`.
      - LEARN the patterns before writing code.
      - Mark `[Context]` tasks as complete (`[x]`).

   b. **Implement Tasks**
      - Find `[Scaffold]` and `[Implement]` tasks.
      - Create/Edit files following:
        - Decisions from `plan.md`.
        - Patterns learned from `[Context]` tasks.
        - Rules from `tech-constitution.md`.
      - Mark tasks as complete (`[x]`).

   c. **Test & Verify**
      - Run `[Test]` tasks.
      - Run relevant commands (e.g., `npm run typecheck` for Layer 0).
      - Verify the layer's checkpoint criteria.

   d. **Checkpoint**
      - Ask user for confirmation to proceed to the next layer (unless in turbo mode).

3. **Update Status**
   After each layer, update `specs/[spec-id]/README.md`:
   `**Status**: Layer [N] Complete - [Layer Name]`

4. **Completion**
   When all layers are done:
   Update `specs/[spec-id]/README.md`:
   `**Status**: ✅ Implementation Complete`
