---
description: Generate a PRD draft from research notes
handoffs:
  - label: Refine PRD
    agent: prd-refine
    prompt: Refine and validate the PRD draft
    send: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Synthesize the research notes (`research.md`) into a structured PRD draft (`PRD.md`) following the standard template. The draft may contain `[NEEDS_DETAIL]` tags for information that requires clarification.

## Operating Constraints

**SYNTHESIS ROLE**: Act as a Product Writer who transforms discovery notes into formal requirements.

**TEMPLATE ADHERENCE**: Follow `.prd-kit/templates/prd-template.md` structure exactly.

**TRACEABILITY**: Every statement in the PRD should trace back to research.md.

**NO INVENTION**: If research.md lacks information, mark with `[NEEDS_DETAIL]`. Never fabricate data.

## Execution Steps

1. **Setup**: Run setup script to get file paths:
   ```bash
   scripts/bash/setup-draft.sh --feature "feature-name" --json
   ```

2. **Load Inputs**:
   - Read `prds/[feature]/research.md` - the discovery notes
   - Read `.prd-kit/memory/product-constitution.md` - for alignment
   - Read `.prd-kit/templates/prd-template.md` - the target structure

3. **Validate Prerequisites**:
   - Verify research.md exists and has no `[NEEDS_DETAIL]` tags
   - If tags remain, inform user to complete discovery first:
     ```
     ⚠ Discovery Incomplete
     
     research.md still has unresolved fields:
     - [NEEDS_DETAIL: field1]
     - [NEEDS_DETAIL: field2]
     
     Run @prd-discover to complete the discovery phase first.
     ```

4. **Extract and Map Content**:
   Map research findings to PRD sections:

   | Research Section | PRD Section |
   |-----------------|-------------|
   | Problem Space answers | Problem Statement |
   | Solution overview | Solution Overview |
   | User goals + personas | User Stories |
   | Constraints | Non-Functional Requirements |
   | Success metrics | Success Metrics |
   | Potential risks | Risks & Mitigations |

5. **Generate User Stories**:
   For each key user need identified:
   - Write in standard format: As a [persona], I want [action], So that [benefit]
   - Assign priority (P1 for MVP, P2/P3 for later)
   - Write Gherkin acceptance criteria
   - Ensure testability

6. **Apply Constitution Standards**:
   - Use correct Voice & Tone
   - Ensure success metrics align with North Star
   - Verify no Anti-Pattern violations in requirements

7. **Create PRD Draft**:
   Write to `prds/[feature]/PRD.md`:
   - Fill all sections from template
   - Mark any gaps with `[NEEDS_DETAIL: specific_field]`
   - Include status as "Draft"

8. **Run Validation**:
   ```bash
   python .prd-kit/validators/check-completeness.py prds/[feature]/PRD.md
   ```

9. **Report Status**:
   - If validation passes: Ready for refinement
   - If validation fails: List specific gaps

## User Story Guidelines

**Format**:
```markdown
### [US1] [Descriptive Title]
**Priority**: P1 (MVP)

**As a** [specific persona from constitution]
**I want to** [concrete action]
**So that** [measurable benefit]

**Acceptance Criteria:**
```gherkin
Given [specific precondition]
When [specific action]
Then [observable, testable result]
And [additional outcomes if needed]
```
```

**Quality Checks**:
- [ ] Persona matches constitution definition
- [ ] Action is specific and implementable
- [ ] Benefit is user-focused, not feature-focused
- [ ] Acceptance criteria are testable
- [ ] No implementation details in story

## Output Format

```
📝 PRD Draft Generated

**Feature**: [feature-name]
**PRD File**: prds/[feature]/PRD.md

**Summary**:
- User Stories: [count] (P1: [n], P2: [n], P3: [n])
- NFRs: [count]
- Risks: [count]

**Validation**: ✓ Complete / ⚠ [n] fields need detail

**Next Step**: Run @prd-refine to validate and finalize
```

## Context

{ARGS}
