# Deliverable: [DELIVERABLE_NAME]

**Source PRD**: prds/[FEATURE_NAME]/PRD.md
**Deliverable ID**: [XXX]
**Dependencies**: [LIST_OF_DEPENDENCY_IDS]
**Priority**: [HIGH/MEDIUM/LOW]

## Context

[CONTEXT_EXTRACTED_FROM_PRD]
<!-- 
Summarize the relevant context from the source PRD that this deliverable addresses.
Include only information relevant to this specific component.
-->

## User Stories

<!-- Copy only the user stories that this deliverable implements -->

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

---

**Instructions for Spec Kit:**
Use this deliverable file as input when initializing a new spec:
```bash
specify init specs/[FEATURE_NAME]-[DELIVERABLE_NAME]
# Provide this file content when asked "What should I build?"
```
