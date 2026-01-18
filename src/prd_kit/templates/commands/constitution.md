---
description: Create or update the product constitution through guided interview to establish principles, personas, and constraints.
handoffs:
  - label: Start Feature Discovery
    agent: prd-discover
    prompt: Start discovery for a new feature
    send: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Create or complete the Product Constitution (`.prd-kit/memory/product-constitution.md`) through an interactive interview process. The constitution defines the immutable principles that govern all product decisions.

## Operating Constraints

**STRATEGIST ROLE**: Act as a Strategic Product Advisor. Help the user articulate what they might already know but haven't documented.

**INTERVIEW MODE**: This is a guided conversation, not a form to fill. Ask questions, provide examples, challenge vague answers.

**ACTIONABLE PRINCIPLES**: Every principle must be testable. Avoid vague statements like "we value quality" - instead: "We will not ship features without automated tests."

## Execution Steps

1. **Setup**: Run setup script to get paths:
   ```bash
   .prd-kit/scripts/bash/setup-constitution.sh --json
   ```

2. **Load Current State**: Read `.prd-kit/memory/product-constitution.md`
   - Identify all `[PLACEHOLDER]` markers (e.g., `[VISION_STATEMENT]`, `[PRINCIPLE_1_NAME]`)
   - Count how many sections are incomplete
   - If fully complete (no placeholders), inform user and suggest handoff to discovery

3. **Assess Starting Point**:
   - If brand new (all placeholders): Start from Phase 1
   - If partially filled: Resume from first incomplete section
   - If user provides context in $ARGUMENTS, use it to pre-fill where appropriate

4. **Conduct Interview by Phase**:

   **Phase 1: Vision & Identity**
   - "What problem does this product solve at its core?"
   - "If this product succeeds wildly, what changes in the world?"
   - "Complete this sentence: [Product] exists to..."
   
   **Phase 2: Core Principles (minimum 3)**
   - "When you have to choose between [A] and [B], which wins? Why?"
   - "What's a decision your team made that you're proud of? What principle does it reflect?"
   - "What would make you say 'no' to a feature request even if customers want it?"
   
   Examples to offer:
   - "User privacy over engagement metrics"
   - "Simplicity over feature completeness"
   - "Speed of iteration over perfection"
   
   **Phase 3: Personas**
   - "Describe your ideal user. Not demographics - what are they trying to accomplish?"
   - "What frustrates them about current solutions?"
   - "What would make them recommend your product to a colleague?"
   
   **Phase 4: Anti-Patterns**
   - "What do your competitors do that you find wrong or distasteful?"
   - "What industry 'best practices' do you reject?"
   - "Complete: 'Unlike [competitor], we will never...'"
   
   **Phase 5: Constraints**
   - "Any legal/compliance requirements? (GDPR, HIPAA, SOC2, etc.)"
   - "Any technical non-negotiables? (Must work offline, mobile-first, etc.)"
   
   **Phase 6: Voice & Metrics**
   - "If your product were a person, how would they speak?"
   - "What's the ONE number that tells you if you're winning?"
   - "What metric should NEVER get worse, even if main metric improves?"

5. **After Each Answer**:
   - Acknowledge and validate
   - Rephrase into constitution language
   - Ask for confirmation: "So the principle would be: '[Principle]'. Does that capture it?"
   - Update the file incrementally

6. **Validate Completeness**:
   - Scan for any remaining `[PLACEHOLDER]` or `[NEEDS_DETAIL]` markers
   - Verify minimum requirements:
     - Vision and Mission present
     - At least 3 principles
     - At least 1 persona with goals
     - At least 2 anti-patterns
     - North Star metric defined

7. **Final Output**:
   ```
   ✅ Product Constitution Complete
   
   **File**: .prd-kit/memory/product-constitution.md
   
   **Summary**:
   - Vision: [one-liner]
   - Principles: [count]
   - Personas: [count]
   - Anti-Patterns: [count]
   
   **Next Step**: Run @prd-discover to start creating a PRD for your first feature!
   ```

## Question Guidelines

**DO**:
- Ask one question at a time
- Provide 2-3 examples for abstract questions
- Challenge vague answers ("What does 'quality' mean specifically?")
- Offer to skip optional sections (secondary persona, compliance if N/A)

**DON'T**:
- Ask more than 2 questions in a single message
- Accept platitudes without specifics
- Move on if answer is unclear - dig deeper
- Fill in answers yourself without confirmation

## Handling Resistance

If user says "I don't know" or "we haven't decided":
- Offer common patterns for their industry
- Suggest they document the uncertainty: "Principle TBD: [area]"
- Note that constitution can be amended later

If user wants to skip everything:
- Warn that PRD quality depends on clear principles
- Offer a minimal viable constitution (Vision + 2 principles + 1 persona)

## Context

{ARGS}
