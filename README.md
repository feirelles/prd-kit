# PRD Kit

Product Requirements Document generation with AI agents.

## Overview

PRD Kit is a system for generating structured Product Requirements Documents (PRDs) using AI agents. It serves as the precursor to [GitHub Spec Kit](https://github.com/github/spec-kit), transforming product ideas into technical deliverables that can be used to initialize specs.

**Repository**: [github.com/feirelles/prd-kit](https://github.com/feirelles/prd-kit)

## Installation

Choose your preferred installation method:

### Option 1: Persistent Installation (Recommended)

Install once and use everywhere:

```bash
uv tool install prd-kit --from git+https://github.com/feirelles/prd-kit.git
```

Then use the `prd` command anywhere:

```bash
prd init my-project --ai copilot
prd version
```

To update to the latest version:

```bash
uv tool install --force prd-kit --from git+https://github.com/feirelles/prd-kit.git
```

### Option 2: One-Time Use (uvx)

Run directly without installation:

```bash
uvx --from git+https://github.com/feirelles/prd-kit.git prd init my-project --ai copilot
```

### Option 3: Local Development

```bash
# Clone and install locally
git clone https://github.com/feirelles/prd-kit.git
cd prd-kit
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

### Initialize a Project

```bash
prd init my-project --ai copilot
```

Options:
- `--ai copilot|claude` - AI agent to configure (default: copilot)
- `--here` - Initialize in current directory
- `--force` - Force init in non-empty directory
- `--no-git` - Skip git initialization

### Update an Existing Project

To update templates, agents, and scripts in an existing project to the latest version:

```bash
cd my-project
prd update
```

This preserves your PRDs and product-constitution.md while updating:
- Templates (prd-template.md, deliverable-template.md, etc.)
- Command definitions
- Agent files
- Setup scripts
- Validators

Options:
- `--ai copilot|claude` - Override AI agent type (auto-detected by default)

### Workflow

After initialization, interact with the AI agents:

#### Phase 1: Client-Facing Documents

1. **@prd-constitution** - Set up your product principles (required first time)
2. **@prd-tech-constitution** - Set up your technical stack and rules (required for Phase 2)
3. **@prd-discover** - Start discovery, describe your product idea
4. **@prd-draft** - Generate PRD from research notes
5. **@prd-refine** (optional) - Validate and improve the PRD
6. **@prd-decompose** - Break PRD into technical deliverables
7. **@prd-deliverables** - Generate deliverable files

> **Note**: Documents up to this point are suitable for client review and approval.

#### Phase 2: Technical Documents (AI-Ready)

After client approves deliverables:

7. **@prd-init-feature** - Create feature branch and spec directory
8. **@prd-context** - Analyze project codebase for patterns and context
9. **@prd-plan** - Generate technical plan with architecture decisions
10. **@prd-tasks** - Generate implementation tasks organized by layer

> **Note**: Technical documents contain code, paths, and AI-ready implementation details.

### Directory Structure

```
.prd-kit/
├── memory/
│   ├── product-constitution.md   # Your product principles
│   └── tech-constitution.md      # Your technical rules (stack, patterns)
├── templates/                     # Document templates
├── commands/                      # Agent command definitions
└── validators/                    # Validation scripts

prds/
└── [feature-name]/
    ├── research.md               # Discovery notes
    ├── PRD.md                    # Product Requirements Document
    └── deliverables/
        ├── deliverables-map.json
        └── deliverable-XXX.md    # Technical deliverables

specs/                             # NEW: Technical specs
└── [XXX-feature-name]/
    ├── README.md                 # Status tracker
    ├── deliverable.md            # Copy of approved deliverable
    ├── context.md                # Project analysis
    ├── plan.md                   # Technical decisions
    └── tasks.md                  # Implementation tasks by layer
```

## Task Organization

Tasks in `tasks.md` are organized by **technical layer** (not user story):

| Layer | Purpose | Checkpoint |
|-------|---------|------------|
| 0 | Types & Interfaces | TypeScript compiles |
| 1 | Backend / API | Endpoints respond |
| 2 | Data Layer | Data loads correctly |
| 3 | UI Components | Components render |
| 4 | Page Integration | Full flow works |
| 5 | Polish & Validation | Production-ready |

This prevents context-switching between frontend/backend during implementation.

## License

MIT

