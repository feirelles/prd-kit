<!--
PRD Kit - Deliverable Template

VALIDATION REQUIREMENTS:
The following sections/fields are REQUIRED and checked by the validator:
  ✅ **Source PRD**: Must be present
  ✅ **Deliverable ID**: Must be present
  ✅ ## Context: Must exist as a section
  ✅ ## User Stories: Must exist as a section
  ✅ ## Acceptance Criteria: Must exist as a section

All other sections are recommended but not enforced.
-->

# Deliverable: [DELIVERABLE_NAME]

**Source PRD**: prds/[FEATURE_NAME]/PRD.md
**Deliverable ID**: [XXX]
**Dependencies**: [LIST_OF_DEPENDENCY_IDS or "None"]
**Priority**: [High/Medium/Low]

## Context

[CONTEXT_EXTRACTED_FROM_PRD]
<!-- 
REQUIRED SECTION - Summarize the relevant context from the source PRD.
Include only information relevant to this specific component.
This helps the implementer understand WHY this deliverable exists.
-->

## User Stories

<!-- REQUIRED SECTION - Copy only the user stories assigned to this deliverable -->

### [US_ID] [USER_STORY_TITLE]
**Priority**: [P1/P2/P3]

**As a** [PERSONA]
**I want to** [ACTION]
**So that** [BENEFIT]

**Acceptance Criteria:**
```gherkin
Given [PRECONDITION]
When [ACTION]
Then [EXPECTED_RESULT]
```

## Technical Requirements

### Functional Requirements
- [FUNC_REQ_1]
- [FUNC_REQ_2]

### Non-Functional Requirements
- [NFR_1]: [DESCRIPTION]
  <!-- Example: Response time < 200ms for API calls -->
- [NFR_2]: [DESCRIPTION]

### Constraints
- [CONSTRAINT_1]
- [CONSTRAINT_2]

## Acceptance Criteria

<!-- REQUIRED SECTION - Testable criteria for this component -->

### Must Have (MVP)
- [ ] [CRITERIA_1]
- [ ] [CRITERIA_2]
- [ ] [CRITERIA_3]

### Should Have
- [ ] [CRITERIA_4]
- [ ] [CRITERIA_5]

### Nice to Have
- [ ] [CRITERIA_6]

## Integration Points

### Consumes
<!-- APIs or services this deliverable will consume -->
- [SERVICE_1]: [DESCRIPTION]
- [SERVICE_2]: [DESCRIPTION]

### Provides
<!-- APIs or services this deliverable will expose -->
- [API_1]: [DESCRIPTION]
- [API_2]: [DESCRIPTION]

## Notes for Implementation

[ADDITIONAL_NOTES]
<!-- 
Any additional context, warnings, or suggestions for the implementation team.
Reference specific sections of the PRD if needed.
-->
