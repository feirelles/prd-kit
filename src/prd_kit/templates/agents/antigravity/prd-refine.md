---
description: Refine and validate the PRD draft against quality criteria
---

This workflow helps you validate the PRD for quality, completeness, and constitution compliance.

1. **Run Setup Script**
   Ask the user for the feature name.
   // turbo
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null)/.prd-kit/scripts" && python -m prd_scripts.setup_refine --feature "[feature-name]" --json
   ```
    *(Note: Replace `[feature-name]` with the actual feature name before running)*

2. **Load Context**
   - Read `.prd-kit/commands/refine.md` for instructions.
   - Read `.prd-kit/memory/product-constitution.md`.
   - Read `PRD.md` in the feature directory.

3. **Check Quality and Compliance**
   - Check if User Stories use constitution personas.
   - Check if Acceptance Criteria are in Gherkin format.
   - Check for risks and mitigations.
   - **Constitution Check**: For EACH principle in `.prd-kit/memory/product-constitution.md`, verify the PRD aligns.

4. **Refine PRD**
   - Edit `PRD.md` to fix issues.
   - Flag critical violations.

5. **Validate**
   // turbo
   ```bash
   python .prd-kit/validators/check-completeness.py
   ```
