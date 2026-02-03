---
description: Generate technical plan with architecture decisions for a feature
---

This workflow creates a detailed technical blueprint for implementation.

1. **Read Command Instructions**
   Read `.prd-kit/commands/plan.md`.

2. **Run Setup Script**
   Ask the user for the spec identifier.
   // turbo
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null)/.prd-kit/scripts" && python -m prd_scripts.setup_plan --spec "[spec-id]" --json
   ```
   *(Note: Replace `[spec-id]` with the actual spec identifier)*

3. **Verify Status**
   Check output. Verify `HAS_CONTEXT` is true.

4. **Load Inputs**
   - Read `specs/[spec-id]/deliverable.md` (What to build).
   - Read `specs/[spec-id]/context.md` (How to build it - patterns).
   - Read `.prd-kit/memory/tech-constitution.md` (Rules to follow).

5. **Make Technical Decisions**
   For each User Story, decide:
   - **Route/Path**: URL structure.
   - **Components**: New vs Reused.
   - **Data**: Composables, Store, or Local State.
   - **API**: Endpoints needed.

   **CRITICAL**: All decisions MUST align with `tech-constitution.md` and reuse patterns from `context.md`.

6. **Generate Plan**
   Create `specs/[spec-id]/plan.md` with Sections:
   - Technical Summary
   - Architecture (Component Tree, Data Flow)
   - Layer Breakdown (0-5)
   - Skills to Read
   - Constitution Compliance Check

7. **Update Status**
   Update `specs/[spec-id]/README.md`:
   Change `[ ] plan.md` to `[x] plan.md`.
