---
description: Generate a PRD draft from research notes
---

This workflow transforms discovery notes into a formal Product Requirements Document.

1. **Run Setup Script**
   Ask the user for the feature name.
   // turbo
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null)/.prd-kit/scripts" && python -m prd_scripts.setup_draft --feature "[feature-name]" --json
   ```
   *(Note: Replace `[feature-name]` with the actual feature name before running)*

2. **Load Context**
   - Read `.prd-kit/commands/draft.md` for instructions.
   - Read `.prd-kit/memory/product-constitution.md` for principles.
   - Read `research.md` in the feature directory (path output from step 1).

3. **Generate PRD**
   Use the content from `research.md` to fill `PRD.md` (which starts as a copy of `.prd-kit/templates/prd-template.md`).
   - Create User Stories with Gherkin acceptance criteria.
   - Ensure all claims trace back to research.
   - Apply Voice & Tone from constitution.

4. **Validate Draft**
   // turbo
   ```bash
   python .prd-kit/validators/check-completeness.py
   ```
