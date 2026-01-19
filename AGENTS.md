# PRD Kit Agents

This project uses PRD Kit for Product Requirements Document generation.

## Available Agents

| Agent | Description |
|-------|-------------|
| `@prd-constitution` | Set up product principles, personas, and constraints (run first!) |
| `@prd-discover` | Start discovery phase - interview to understand the product idea |
| `@prd-draft` | Generate PRD draft from research notes |
| `@prd-refine` | Refine and validate PRD against constitution |
| `@prd-decompose` | Decompose PRD into technical deliverables |
| `@prd-deliverables` | Generate deliverable files for Spec Kit |

## Workflow

1. **Constitution**: `@prd-constitution` - Define product principles (one-time setup)
2. **Discovery**: `@prd-discover` - Describe your product idea
3. **Draft**: `@prd-draft` - Generate initial PRD
4. **Refine**: `@prd-refine` - Validate and improve PRD
5. **Decompose**: `@prd-decompose` - Break into deliverables
6. **Generate**: `@prd-deliverables` - Create deliverable files

## Configuration

- AI Agent: **copilot**
- Constitution: `.prd-kit/memory/product-constitution.md`
- Templates: `.prd-kit/templates/`
- Commands: `.prd-kit/commands/`

## Handoff to Spec Kit

After generating deliverables, use each `deliverable-XXX.md` file to initialize
a spec in Spec Kit:

```bash
specify init specs/[deliverable-name]
# When asked "What should I build?", provide the deliverable file content
```
