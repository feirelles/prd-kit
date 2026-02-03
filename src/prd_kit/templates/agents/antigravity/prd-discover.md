---
description: Start PRD discovery - interview to understand your product idea and create research notes
---

This workflow helps you transform vague ideas into structured research notes.

1. **Pre-Flight Check**
   // turbo
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null)/.prd-kit/scripts" && python -m prd_scripts.setup_constitution --json
   ```
   Check the output. If the status is NOT "complete", stop and ask the user to run the `prd-constitution` workflow first.

2. **Run Setup Script**
   Ask the user for the feature name if not provided.
   // turbo
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null)/.prd-kit/scripts" && python -m prd_scripts.setup_discover --feature "[feature-name]" --json
   ```
   *(Note: Replace `[feature-name]` with the actual feature name before running)*

3. **Read Instructions and Constitution**
   - Read `.prd-kit/commands/discover.md`
   - Read `.prd-kit/memory/product-constitution.md`

4. **Identify Research File**
   The setup script output should locate the `research.md` file. Read it.

5. **Conduct Discovery Interview**
   Ask targeted questions to fill `[NEEDS_DETAIL]` tags in `research.md`.
   - Validate every idea against the constitution.
   - Ask ONE question at a time.

6. **Validate Research**
   // turbo
   ```bash
   python .prd-kit/validators/check-completeness.py
   ```
