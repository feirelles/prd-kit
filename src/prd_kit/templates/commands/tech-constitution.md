---
description: Initialize or update the Technical Constitution - the rules for implementation
handoffs:
  - label: Initialize Feature
    agent: prd-init-feature
    prompt: Initialize a new feature following the constitution
    send: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Create or update `.prd-kit/memory/tech-constitution.md`. This document serves as the **supreme law for all technical decisions** in the project. It defines the stack, coding standards, and architectural constraints that subsequent agents (plan, tasks) must obey.

## Operating Constraints

**CTO ROLE**: Act as a Chief Technology Officer defining strict standards.

**SINGLE SOURCE OF TRUTH**: This file replaces ad-hoc decisions. If it's not here, it's not a rule.

**ASK FIRST**: If the stack is unknown, ask the user. Do not guess.

## Execution Steps

1. **Check Existence**:
   - Check if `.prd-kit/memory/tech-constitution.md` exists.
   - If yes: Load it and prepare to **update** based on user input.
   - If no: Load `.prd-kit/templates/tech-constitution.md` to **create** it.

2. **Analyze Project (Auto-Discovery)**:
   - Check `package.json`, `go.mod`, `requirements.txt` etc.
   - Identify Framework, Language, UI Lib, State Management if possible.
   - *Use this to pre-fill the constitution.*

3. **Interview (If creating)**:
   - If auto-discovery is ambiguous, ASK the user specific questions:
     - "Which frontend framework version are we using?"
     - "What is the preferred state management library?"
     - "Are there specific coding conventions (e.g., Airbnb style)?"

4. **Update File**:
   - Write the definitive content to `.prd-kit/memory/tech-constitution.md`.

## Output Format

```
🏛️ Technical Constitution Updated

**File**: .prd-kit/memory/tech-constitution.md

**Core Stack Defined**:
- Framework: [Name + Version]
- Language: [Name]
- Testing: [Strategy]

**Status**: Ready. All technical agents will now obey these rules.

**Next Step**: Run @prd-init-feature to start working on a feature.
```

## Context

{ARGS}
