# PRD Kit Agents

This project uses PRD Kit for Product Requirements Document generation.

## Available Agents

### Phase 1: PRD Creation (Client-Facing)

| Agent | Description | Output |
|-------|-------------|--------|
| `@prd-constitution` | Set up product principles, personas, and constraints | `product-constitution.md` |
| `@prd-discover` | Interview to understand the product idea | `research.md` |
| `@prd-draft` | Generate PRD draft from research notes | `PRD.md` |
| `@prd-refine` | Validate PRD against quality criteria | `PRD.md` (approved) |
| `@prd-decompose` | Break PRD into technical components | `deliverables-map.json` |
| `@prd-deliverables` | Generate deliverable files | `deliverable-XXX.md` files |

### Phase 2: Technical Implementation (AI-Ready)

| Agent | Description | Output |
|-------|-------------|--------|
| `@prd-tech-constitution` | Define technical stack and coding rules | `tech-constitution.md` |
| `@prd-init-feature` | Create git branch and spec directory | Branch + `specs/XXX/` |
| `@prd-context` | Analyze codebase for patterns | `context.md` |
| `@prd-plan` | Make architectural decisions | `plan.md` |
| `@prd-tasks` | Generate implementation tasks | `tasks.md` |
| `@prd-implement` | Execute tasks following the plan | Code files |

## Workflow

### Phase 1: PRD Creation
1. `@prd-constitution` - Define product principles (one-time setup)
2. `@prd-discover` - Describe your product idea
3. `@prd-draft` - Generate initial PRD
4. `@prd-refine` - Validate and improve PRD
5. `@prd-decompose` - Create deliverables map (JSON only!)
6. `@prd-deliverables` - Generate deliverable files

### Phase 2: Technical Implementation
7. `@prd-tech-constitution` - Define technical rules (one-time setup)
8. `@prd-init-feature [deliverable(s)]` - Create branch and spec directory
9. `@prd-context [spec]` - Analyze project patterns
10. `@prd-plan [spec]` - Create technical plan
11. `@prd-tasks [spec]` - Generate implementation tasks
12. `@prd-implement [spec]` - Execute tasks (stops at checkpoints for verification)

## Agent Scope Limitations

Each agent is **strictly limited** to its specific function:

| Agent | DOES | DOES NOT |
|-------|------|----------|
| `@prd-init-feature` | Create git branch, create directory | Implement code, create additional files |
| `@prd-context` | Analyze codebase, write context.md | Make decisions, create code |
| `@prd-plan` | Make decisions, write plan.md | Implement, create components |
| `@prd-tasks` | Generate task list, write tasks.md | Execute tasks, write code |
| `@prd-implement` | Execute tasks, write code | Deviate from plan, skip checkpoints |

## Configuration

- AI Agent: **copilot**
- Constitution: `.prd-kit/memory/product-constitution.md`
- Tech Constitution: `.prd-kit/memory/tech-constitution.md`
- Templates: `.prd-kit/templates/`
- Commands: `.prd-kit/commands/`
- Scripts: `.prd-kit/scripts/prd_scripts/`

## Directory Structure

```
prds/
  [feature]/
    research.md          # Discovery notes
    PRD.md               # Product requirements
    deliverables/
      deliverables-map.json
      deliverable-001-*.md
      deliverable-002-*.md

specs/
  [XXX]-[feature]/       # Created by @prd-init-feature
    deliverable.md       # Copy from PRD
    context.md           # Project analysis
    plan.md              # Technical decisions
    tasks.md             # Implementation tasks
```

