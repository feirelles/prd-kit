---
description: Decompose an approved PRD into technical deliverables
---

This workflow helps you break the approved PRD into implementable deliverables.

1. **Run Setup Script**
   Ask the user for the feature name.
   // turbo
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null)/.prd-kit/scripts" && python -m prd_scripts.setup_decompose --feature "[feature-name]" --json
   ```
    *(Note: Replace `[feature-name]` with the actual feature name before running)*

2. **Read Command Instructions**
   Read `.prd-kit/commands/decompose.md`.

3. **Analyze PRD**
   Read `PRD.md` to identify discrete components (Frontend, Backend, Integration).

4. **Create Deliverables Map**
   Create `deliverables-map.json` in the deliverables folder.
   
   **CRITICAL**: Create ONLY `deliverables-map.json`. Do NOT create `deliverable-XXX.md` files yet.

   Use the structure:
   ```json
   {
      "feature": "...",
      "deliverables": [ ... ],
      "dependency_graph": { ... },
      "implementation_order": [ ... ]
   }
   ```

5. **Validate Map**
   // turbo
   ```bash
   python .prd-kit/validators/check-deliverables.py
   ```
   (Note: Use the path to the deliverables directory if needed)
