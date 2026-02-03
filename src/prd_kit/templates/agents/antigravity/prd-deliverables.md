---
description: Generate deliverable files from the decomposition map
---

This workflow generates the client-facing deliverable documents.

1. **Run Setup Script**
   Ask the user for the feature name.
   // turbo
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null)/.prd-kit/scripts" && python -m prd_scripts.setup_deliverables --feature "[feature-name]" --json
   ```
    *(Note: Replace `[feature-name]` with the actual feature name before running)*

2. **Read Instructions**
   Read `.prd-kit/commands/generate-deliverables.md`.

3. **Verify Prerequisites**
   Check if `deliverables-map.json` exists in the feature's `deliverables` folder.

4. **Generate Deliverable Files**
   For each deliverable in the map:
   - Read `.prd-kit/templates/deliverable-template.md`.
   - Create `deliverable-XXX-[name].md`.
   - Fill with content from PRD (Context, User Stories, Acceptance Criteria).
   - **CRITICAL**: Do NOT include code snippets, file paths, or specific library choices. These are requirements documents, not specs.
   - Include an "Out of Scope" section for features in the PRD but belonging to other deliverables.

5. **Generate README**
   Create `README.md` in the deliverables folder.
   - Include an overview table.
   - Show implementation order by phases.

6. **Validate Files**
   // turbo
   ```bash
   python .prd-kit/validators/check-deliverables.py prds/[feature-name]/deliverables/
   ```
   *(Replace `[feature-name]` with the actual feature name)*
