---
description: Generate implementation tasks organized by technical layer
---

This workflow breaks down the technical plan into actionable, layered tasks.

1. **Read Command Instructions**
   Read `.prd-kit/commands/tasks.md`.

2. **Run Setup Script**
   Ask user for spec identifier.
   // turbo
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null)/.prd-kit/scripts" && python -m prd_scripts.setup_tasks --spec "[spec-id]" --json
   ```
   *(Note: Replace `[spec-id]` with the actual spec identifier)*

3. **Verify Status**
   Check output. Verify `HAS_PLAN` is true.

4. **Load Inputs**
   - Read `specs/[spec-id]/plan.md`.
   - Read `specs/[spec-id]/context.md`.
   - Read `specs/[spec-id]/deliverable.md`.
   - Read `.prd-kit/memory/tech-constitution.md`.

5. **Generate Tasks**
   Create `specs/[spec-id]/tasks.md`.
   Organize tasks by **Technical Layer**:
   - Layer 0: Types & Interfaces
   - Layer 1: Backend / API
   - Layer 2: Data Layer
   - Layer 3: UI Components
   - Layer 4: Page Integration
   - Layer 5: Polish & Validation

   **Task Types**:
   - Use `[Context]` tasks for reading skills/files (CRITICAL: Context first in each layer).
   - Use `[Scaffold]` for file creation.
   - Use `[Implement]` for logic.
   - Use `[Test]` for verification.

6. **Update Status**
   Update `specs/[spec-id]/README.md`:
   1. Change `[ ] tasks.md` to `[x] tasks.md`.
   2. Change `**Status**: ...` to `**Status**: Ready for Implementation`.
