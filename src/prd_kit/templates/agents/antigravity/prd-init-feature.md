---
description: Initialize feature branch and spec directory from a deliverable
---

This workflow creates the infrastructure for implementing a new feature: git branch and spec directory.

1. **Read Command Instructions**
   Read `.prd-kit/commands/init-feature.md`.

2. **Identify Deliverables**
   Ask the user which deliverable(s) to initialize.
   Can be a single ID (e.g., `002`) or multiple IDs (e.g., `002 003`).

3. **Run Setup Script**
   // turbo
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null)/.prd-kit/scripts" && python -m prd_scripts.setup_init_feature --deliverable [deliverable-ids] --json
   ```
   *(Note: Replace `[deliverable-ids]` with the actual IDs provided by the user, space-separated)*

4. **Verify Output**
   The script output will show the created directory (`specs/...`) and branch (`feat/...`).
   Report this to the user.

5. **Stop**
   Do not create any additional files or code.
