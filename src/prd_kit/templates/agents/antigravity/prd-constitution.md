---
description: Create or update your product constitution - define principles, personas, and constraints
---

This workflow guides you through creating a comprehensive Product Constitution.

1. **Run Setup Script**
   // turbo
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null)/.prd-kit/scripts" && python -m prd_scripts.setup_constitution --json
   ```

2. **Read Command Instructions**
   Read the file at `.prd-kit/commands/constitution.md` to understand the detailed requirements for the constitution.

3. **Check Current State**
   Read the file at `.prd-kit/memory/product-constitution.md` to see what is already defined.

4. **Conduct Interview**
   Interview the user to fill in any `[PLACEHOLDER]` sections in `product-constitution.md`.
   Cover these phases:
   - Phase 1: Vision & Identity
   - Phase 2: Core Principles (3-5 items)
   - Phase 3: Personas
   - Phase 4: Anti-Patterns
   - Phase 5: Constraints & Compliance
   - Phase 6: Voice & Success
   
   Ask one question at a time and explain why it matters.

5. **Validate**
   Ensure all placeholders are filled.
   // turbo
   ```bash
   python .prd-kit/validators/check-completeness.py
   ```
