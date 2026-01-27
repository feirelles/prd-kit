---
description: Generate deliverable files from the decomposition map for use with Spec Kit
handoffs:
  - label: Start Spec Kit
    agent: speckit.specify
    prompt: Initialize a new spec from the deliverable
    send: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Generate individual `deliverable-XXX.md` files for each component in the deliverables map. Each file will serve as input for initializing a Spec Kit specification.

## ⚠️ CRITICAL: Prerequisites

**Before running this command:**
- `deliverables-map.json` MUST already exist (created by `@prd-decompose`)
- If it doesn't exist, direct user to run `@prd-decompose` first

## Operating Constraints

**DOCUMENTATION ROLE**: Act as a Technical Writer creating implementation briefs.

**USE THE TEMPLATE**: Always load and follow `.prd-kit/templates/deliverable-template.md`.

**SELF-CONTAINED**: Each deliverable file must contain all context needed for Spec Kit.

**VALIDATION REQUIRED**: Every file must pass validation before completing.

**NO SPEC GENERATION**: Do NOT generate spec.md files. Deliverables are input for Spec Kit.

**TRACEABILITY**: Every requirement must trace back to the source PRD.

## Execution Steps

1. **Setup**: Run setup script:
   ```bash
   (cd .prd-kit/scripts 2>/dev/null || cd "$(git rev-parse --show-toplevel)/.prd-kit/scripts") && python -m prd_scripts.setup_deliverables --feature "feature-name" --json
   ```

2. **Load Inputs**:
   - Read `prds/[feature]/PRD.md` - source of requirements
   - Read `prds/[feature]/deliverables/deliverables-map.json` - decomposition (MUST exist)
   - **Read `.prd-kit/templates/deliverable-template.md`** - REQUIRED template for output format

3. **Validate Prerequisites**:
   - ❌ If `deliverables-map.json` doesn't exist → Stop and direct user to `@prd-decompose`
   - Dependency validation must pass
   - PRD must be approved

4. **For Each Deliverable in Map**:

   a. **Extract Relevant Context**:
      - Problem context related to this component
      - Only user stories assigned to this deliverable
      - NFRs that apply to this component type
      - Relevant risks and mitigations

   b. **Identify Integration Points**:
      - What other components does this consume?
      - What does this component expose to others?
      - Reference dependency IDs from map

   c. **Generate Acceptance Criteria**:
      - Copy Gherkin criteria from assigned user stories
      - Add integration criteria based on dependencies
      - Ensure criteria are independently testable

   d. **Define Out of Scope**:
      - Review the deliverables-map.json to identify which features belong to other deliverables
      - List features from the PRD that are planned but will be implemented in OTHER deliverables
      - Explain which deliverable will implement each out-of-scope feature
      - This prevents premature implementation when dependencies from other deliverables are not ready yet
      - Do NOT list features outside the PRD - only features planned for different deliverables

   e. **Write Deliverable File** (following template exactly):
      Create `prds/[feature]/deliverables/deliverable-XXX-[name].md`

      **REQUIRED Structure** (all sections mandatory):
      ```markdown
      # Deliverable: [Title]
      
      **Source PRD**: prds/[feature]/PRD.md
      **Deliverable ID**: [XXX]
      **Dependencies**: [List of IDs or "None"]
      **Priority**: [High/Medium/Low]
      
      ## Context
      [Extracted from PRD - problem + solution relevant to this component]
      
      ## User Stories
      [Only stories assigned to this deliverable]
      
      ## Technical Requirements
      [NFRs applicable to this component]
      
      ## Acceptance Criteria
      [Testable criteria for this component]
      
      ## Integration Points
      [What this consumes and provides]
      
      ## Out of Scope
      [Features from PRD that belong to other deliverables - prevents premature implementation]
      
      ## Notes for Implementation
      [Any additional context]
      ```

5. **Validate All Deliverables** (REQUIRED - must pass before completing):
   ```bash
   python .prd-kit/validators/check-deliverables.py prds/[feature]/deliverables/
   ```

   **Required Checks** (validation must pass):
   - ✅ All deliverables from map have files generated
   - ✅ Each file has `Source PRD` reference
   - ✅ Each file has `Deliverable ID`
   - ✅ Each file has `## Context` section
   - ✅ Each file has `## User Stories` section
   - ✅ Each file has `## Acceptance Criteria` section

   **If validation fails**: Fix the issues before proceeding.

6. **Generate Summary Report**:

   Create `prds/[feature]/deliverables/README.md`:
   ```markdown
   # Deliverables: [Feature Name]
   
   Generated from: prds/[feature]/PRD.md
   Generated at: [DATE]
   
   ## Implementation Order
   
   ### Phase 1 (Sequential)
   1. [deliverable-001-name.md](deliverable-001-name.md) - [Title]
   
   ### Phase 2 (Parallel)
   - [deliverable-002-name.md](deliverable-002-name.md) - [Title]
   - [deliverable-003-name.md](deliverable-003-name.md) - [Title]
   
   ## Handoff to Spec Kit
   
   For each deliverable, run:
   ```bash
   specify init specs/[feature]-[deliverable-name]
   ```
   When asked "What should I build?", provide the deliverable file content.
   ```

## Output Format

```
📦 Deliverables Generated

**Feature**: [feature-name]
**Directory**: prds/[feature]/deliverables/

**Generated Files**:
- deliverable-001-[name].md (Priority: High)
- deliverable-002-[name].md (Priority: High)
- deliverable-003-[name].md (Priority: Medium)
- deliverables-map.json
- README.md

**Implementation Order**:
Phase 1: 001 → Phase 2: 002, 003 (parallel)

**Handoff Instructions**:
For each deliverable, initialize Spec Kit:
```bash
specify init specs/[feature]-[name]
# Provide deliverable file content when prompted
```

✅ PRD Kit workflow complete!
```

## Quality Checklist

Before marking complete:
- [ ] All deliverables from map have files generated
- [ ] Each file follows template structure exactly
- [ ] User stories match those in PRD (no additions/removals)
- [ ] Dependencies are correctly documented
- [ ] Acceptance criteria are testable
- [ ] Integration points are specific
- [ ] README.md summarizes implementation order

## Context

{ARGS}
