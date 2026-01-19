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

## Operating Constraints

**DOCUMENTATION ROLE**: Act as a Technical Writer creating implementation briefs.

**SELF-CONTAINED**: Each deliverable file must contain all context needed for Spec Kit.

**NO SPEC GENERATION**: Do NOT generate spec.md files. Deliverables are input for Spec Kit.

**TRACEABILITY**: Every requirement must trace back to the source PRD.

## Execution Steps

1. **Setup**: Run setup script (from `.prd-kit/scripts` directory):
   ```bash
   python -m prd_scripts.setup_deliverables --feature "feature-name" --json
   ```

2. **Load Inputs**:
   - Read `prds/[feature]/PRD.md` - source of requirements
   - Read `prds/[feature]/deliverables/deliverables-map.json` - decomposition
   - Read `.prd-kit/templates/deliverable-template.md` - output format

3. **Validate Prerequisites**:
   - deliverables-map.json must exist
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

   d. **Write Deliverable File**:
      Create `prds/[feature]/deliverables/deliverable-XXX-[name].md`

      Structure:
      ```markdown
      # Deliverable: [Title]
      
      **Source PRD**: prds/[feature]/PRD.md
      **Deliverable ID**: [XXX]
      **Dependencies**: [List of IDs]
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
      
      ## Notes for Implementation
      [Any additional context]
      ```

5. **Validate All Deliverables**:
   ```bash
   python .prd-kit/validators/check-deliverables.py prds/[feature]/deliverables/
   ```

   Checks:
   - All deliverables from map are generated
   - Required sections present
   - User stories match PRD
   - Dependencies reference valid IDs

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
