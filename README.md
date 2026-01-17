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
- `--script sh|ps` - Script type (auto-detected if not specified)
- `--here` - Initialize in current directory
- `--force` - Force init in non-empty directory
- `--no-git` - Skip git initialization

### Workflow

After initialization, interact with the AI agents:

1. **@prd-discover** - Start discovery, describe your product idea
2. **@prd-draft** - Generate PRD from research notes
3. **@prd-refine** - Validate and improve the PRD
4. **@prd-decompose** - Break PRD into technical deliverables
5. **@prd-deliverables** - Generate deliverable files for Spec Kit

### Directory Structure

```
.prd-kit/
├── memory/
│   └── product-constitution.md   # Your product principles
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
```

## Handoff to Spec Kit

Each generated deliverable can be used to initialize a Spec Kit specification:

```bash
specify init specs/[feature]-[component]
# When asked "What should I build?", provide the deliverable file content
```

## License

MIT
