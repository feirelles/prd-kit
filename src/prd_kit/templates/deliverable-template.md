# Deliverable: [DELIVERABLE_NAME]

**Source PRD**: prds/[FEATURE_NAME]/PRD.md
**Deliverable ID**: [XXX]
**Dependencies**: [LIST_OF_DEPENDENCY_IDS]
**Priority**: [HIGH/MEDIUM/LOW]
**Effort**: [SMALL/MEDIUM/LARGE]

---

## Context

[CONTEXT_EXTRACTED_FROM_PRD]
<!-- 
Summarize the relevant context from the source PRD that this deliverable addresses.
Include only information relevant to this specific component.
NO CODE OR TECHNICAL DETAILS HERE - those come after @prd-context
-->

---

## User Stories

<!-- Copy only the user stories that this deliverable implements -->

### [US_ID] [USER_STORY_TITLE]
**Priority**: [P0/P1/P2]

**As a** [PERSONA]
**I want to** [ACTION]
**So that** [BENEFIT]

**Acceptance Criteria:**
```gherkin
Given [PRECONDITION]
When [ACTION]
Then [EXPECTED_RESULT]
```

---

## Integration Points

<!-- Conceptual only - no code, no specific paths -->

### Consumes
- [SERVICE_1]: [DESCRIPTION]
- [SERVICE_2]: [DESCRIPTION]

### Provides
- [API_1]: [DESCRIPTION]
- [API_2]: [DESCRIPTION]

---

## Implementation Notes

<!-- High-level guidelines, constraints, warnings -->
<!-- NO CODE: paths, types, interfaces, snippets -->

[NOTES]

---

**Next Step**: After client approval, run `@prd-init-feature [DELIVERABLE_ID]` to start technical phase.
