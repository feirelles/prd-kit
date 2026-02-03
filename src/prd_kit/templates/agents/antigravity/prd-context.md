---
description: Analyze project codebase to discover patterns, stack, and reusable components
---

This workflow analyzes the existing project to inform new feature development.

1. **Read Command Instructions**
   Read `.prd-kit/commands/context.md`.

2. **Run Setup Script**
   Ask the user for the spec identifier (e.g., `001-feature-name`).
   // turbo
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null)/.prd-kit/scripts" && python -m prd_scripts.setup_context --spec "[spec-id]" --json
   ```
   *(Note: Replace `[spec-id]` with the actual spec identifier)*

3. **Verify Status**
   Check the output. Verify `HAS_DELIVERABLE` is true.

4. **Load Inputs**
   - Read `.prd-kit/memory/tech-constitution.md`.
   - Read `specs/[spec-id]/deliverable.md`.

5. **Analyze Project**
   - Check directory structure.
   - Search for **Database Schema**:
     - Check `pb_migrations/`, `prisma/schema.prisma`, `migrations/`, etc.
   - Search for similar components or patterns required by the deliverable.
   - Check `.github/skills/` for relevant skills.

6. **Generate Context**
   Create/Edit `specs/[spec-id]/context.md`.
   Include:
   - Project Stack
   - Reusable Patterns (with paths)
   - Database Schema (collections/tables found)
   - Available Skills
   - Open Questions

7. **Update Status**
   Update `specs/[spec-id]/README.md`:
   Change `[ ] context.md` to `[x] context.md`.
