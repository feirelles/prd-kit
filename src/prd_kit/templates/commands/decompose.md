---
description: Decompose an approved PRD into technical deliverables - creates deliverables-map.json ONLY
handoffs:
  - label: Generate Deliverable Files
    agent: prd-deliverables
    prompt: Generate the deliverable files from the decomposition map
    send: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Analyze the approved PRD and decompose it into discrete technical deliverables (components) with identified dependencies. Output **ONLY** a `deliverables-map.json` that defines what needs to be built.

## ⚠️ CRITICAL: Scope Limitation

**THIS COMMAND ONLY CREATES `deliverables-map.json`**

| ✅ DO | ❌ DO NOT |
|-------|----------|
| Create `deliverables-map.json` | Create `deliverable-XXX.md` files |
| Validate the map structure | Generate README.md in deliverables |
| Define dependencies | Write any implementation details |
| Set implementation order | Hand off to Spec Kit directly |

**The `@prd-deliverables` agent is responsible for generating the actual deliverable files.**

## Operating Constraints

**ARCHITECT ROLE**: Act as a Technical Architect analyzing requirements for implementation.

**MAP ONLY**: Your only output is `deliverables-map.json`. No other files.

**NO IMPLEMENTATION DETAILS**: Focus on WHAT components are needed, not HOW to build them.

**DEPENDENCY ACCURACY**: Dependencies must be real (component A needs B's API), not speculative.

**SPEC KIT ALIGNMENT**: Each deliverable entry should be suitable as input for `specify init`.

## Execution Steps

1. **Setup**: Run setup script (from `.prd-kit/scripts` directory):
   ```bash
   python -m prd_scripts.setup_decompose --feature "feature-name" --json
   ```

2. **Load Inputs**:
   - Read `prds/[feature]/PRD.md` - the approved PRD
   - Read `.prd-kit/memory/product-constitution.md` - for technical constraints
   - Optionally read `.specify/memory/constitution.md` if exists (technical constitution)

3. **Validate Prerequisites**:
   - PRD must have status "Approved"
   - No `[NEEDS_DETAIL]` tags allowed
   - If not ready, direct user to complete refinement

4. **Analyze PRD Structure**:

   Extract from User Stories:
   - User-facing interfaces (UI components)
   - Backend services (APIs, business logic)
   - Data storage needs
   - External integrations

   Extract from NFRs:
   - Infrastructure requirements
   - Security components
   - Monitoring/observability needs

5. **Identify Deliverable Candidates**:

   Common patterns:
   | Pattern | Deliverable Type |
   |---------|-----------------|
   | "User can see/interact" | Frontend Component |
   | "System stores/retrieves" | Backend API + Data |
   | "Integration with X" | Integration Service |
   | "Performance < Xms" | May need caching layer |
   | "Authentication/Authorization" | Auth Service |

6. **Apply Decomposition Rules**:

   **Separation Criteria**:
   - Different deployment units → separate deliverables
   - Different teams ownership → separate deliverables
   - Can be developed in parallel → separate deliverables
   - Tight coupling required → same deliverable

   **Size Guidelines**:
   - Each deliverable should be 1-4 weeks of work
   - If larger, consider breaking down further
   - If smaller, consider combining

7. **Map Dependencies**:

   For each deliverable pair (A, B):
   - Does A need B's API? → A depends on B
   - Does A need B's data? → A depends on B
   - Can A work without B? → No dependency

   **Dependency Rules**:
   - No circular dependencies allowed
   - Minimize dependency depth
   - Frontend typically depends on Backend
   - Services may be independent

8. **Generate deliverables-map.json**:

   ```json
   {
     "source_prd": "prds/[feature]/PRD.md",
     "generated_at": "[ISO_DATE]",
     "deliverables": [
       {
         "id": "001",
         "name": "[component-name]",
         "title": "[Human Readable Title]",
         "type": "frontend|backend|integration|infrastructure",
         "description": "[Brief description]",
         "user_stories": ["US1", "US2"],
         "dependencies": [],
         "priority": "high|medium|low",
         "estimated_effort": "small|medium|large",
         "file": "deliverable-001-[name].md"
       }
     ],
     "dependency_graph": {
       "001": [],
       "002": ["001"],
       "003": ["001", "002"]
     },
     "implementation_order": [
       {"phase": 1, "deliverables": ["001"], "parallel": false},
       {"phase": 2, "deliverables": ["002", "003"], "parallel": true}
     ]
   }
   ```

9. **Validate Dependency Graph**:
   ```bash
   python .prd-kit/validators/check-deliverables.py prds/[feature]/deliverables/deliverables-map.json
   ```

   Checks:
   - No circular dependencies
   - All referenced IDs exist
   - Implementation order is valid

10. **Generate Implementation Order**:
    ```bash
    python .prd-kit/validators/generate-implementation-order.py prds/[feature]/deliverables/deliverables-map.json
    ```

## Output Format

```
🔀 PRD Decomposed

**Feature**: [feature-name]
**Deliverables Map**: prds/[feature]/deliverables/deliverables-map.json

**Identified Deliverables**:
1. [001] [Title] (Priority: High)
   - Type: [type]
   - Stories: US1, US2
   - Dependencies: None

2. [002] [Title] (Priority: High)
   - Type: [type]
   - Stories: US3
   - Dependencies: 001

**Implementation Order**:
Phase 1: [001] (sequential)
Phase 2: [002], [003] (can be parallel)

**Dependency Graph**:
```
[001] ──┬──► [002]
        └──► [003]
```

✅ **Decomposition Complete**

⚠️ **STOP HERE** - Do NOT generate deliverable files yet!

**Next Step**: Run `@prd-deliverables` to generate the individual deliverable files from this map.
```

## ⚠️ IMPORTANT: What NOT To Do

After creating `deliverables-map.json`:
- ❌ DO NOT create `deliverable-XXX.md` files
- ❌ DO NOT create README.md in deliverables folder
- ❌ DO NOT run the deliverables validation on files (only on the map)
- ✅ DO hand off to `@prd-deliverables` for file generation

## Context

{ARGS}
