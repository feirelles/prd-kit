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

⚠️ NO CODE ALLOWED:
- NO code snippets (no TypeScript, JavaScript, Python, etc.)
- NO file paths or directory structures
- NO specific library/framework implementations
- NO interface/type definitions

✅ USE INSTEAD:
- Plain English descriptions
- Business logic in prose
- Conceptual flows (if needed, use simple pseudocode)
- Technical constraints as bullet points

WHY: We haven't analyzed the project yet (@prd-context hasn't run).
Code at this stage is often wrong because we don't know the project patterns yet.
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

## Technical Constraints

<!-- High-level technical requirements and constraints ONLY -->
<!-- Describe WHAT needs to happen, not HOW to implement -->

**Performance**:
- [Constraint, e.g., "Must handle 1000 concurrent users"]

**Security**:
- [Constraint, e.g., "Must authenticate all requests"]

**Integration**:
- [Constraint, e.g., "Must be compatible with existing API"]

**Data**:
- [Constraint, e.g., "Must preserve data consistency"]

<!-- 
⚠️ NO CODE EXAMPLES HERE
Use plain English or simple pseudocode ONLY if absolutely necessary to explain a complex concept.

Example of GOOD constraint:
✅ "Authentication must verify user permissions before allowing access"

Example of BAD (too technical for this phase):
❌ "Use JWT tokens with RS256 signing and validate against auth0"
-->

---

## ⚠️ Document Scope

This deliverable is **CLIENT-FACING** (Phase 1). It describes WHAT to build, not HOW.

**What belongs here**:
- User-facing features and behavior
- Business rules and workflows
- Acceptance criteria (user perspective)
- High-level technical constraints

**What does NOT belong here**:
- Code snippets or implementations
- Specific file paths or structures
- Library/framework choices
- Type definitions or interfaces

Those technical details come in **Phase 2** after running:
- `@prd-init-feature` → creates branch and spec directory  
- `@prd-context` → analyzes project patterns
- `@prd-plan` → makes technical decisions
- `@prd-tasks` → generates implementation tasks

---

**Next Step**: After client approval, run `@prd-init-feature [DELIVERABLE_ID]` to start technical phase.
