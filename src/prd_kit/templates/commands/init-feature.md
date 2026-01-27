---
description: Initialize technical phase - create feature branch and directory structure
handoffs:
  - label: Analyze Project Context
    agent: prd-context
    prompt: Analyze the project and generate context for this feature
    send: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Initialize the technical phase for a deliverable: create a feature branch and spec directory. This is the **transition point** from client-facing documents to AI-ready technical documents.

## Operating Constraints

**SETUP ONLY**: Only create git branch and directory structure via setup script.

**NO MANUAL FILE CREATION**: The setup script handles all file creation.

**NO IMPLEMENTATION**: No code, no technical decisions, no additional files.

**CLIENT APPROVAL ASSUMED**: Only use this command AFTER deliverables are approved by client.

## Pre-Flight Check: Deliverable(s) Required

1. Parse $ARGUMENTS to extract deliverable IDs/names (comma or space separated)
2. For each deliverable:
   - Verify the deliverable file exists in `prds/[feature]/deliverables/`
   - If not found, collect error
3. If any not found:
   ```
   ⚠️ Deliverable(s) Not Found
   
   Could not find: [list invalid inputs]
   
   Available deliverables:
   - [list from deliverables-map.json]
   
   → Provide valid deliverable IDs or paths.
   ```

## Execution Steps

1. **Parse Input**: Extract all deliverable IDs from $ARGUMENTS (space separated)

2. **Run Setup Script** with all deliverables:
   
   Single deliverable:
   ```bash
   python -m prd_scripts.setup_init_feature --deliverable [ID] --json
   ```
   
   Multiple deliverables (creates ONE branch/directory for all):
   ```bash
   python -m prd_scripts.setup_init_feature --deliverable [ID1] [ID2] [ID3] --json
   ```
   
   The script will:
   - Load all deliverable files
   - Determine the next feature number
   - Generate combined name (if multiple)
   - Create ONE git branch
   - Create ONE spec directory
   - Copy all deliverable files into the directory

3. **Report Results**: Show the created branch, directory, and list of deliverables

**IMPORTANT**: Do NOT create any files manually. Do NOT implement any code. Do NOT make technical decisions. Only run the setup script and report results.

## Output Format

For single deliverable:
```
✅ Feature Initialized

📁 Directory: [directory path]
🌿 Branch: [branch name]

📄 Deliverable: [deliverable filename]

➡️  Next Step: Run @prd-context to analyze the project and generate technical context.
```

For multiple deliverables (combined in one branch):
```
✅ Feature Initialized ([N] deliverables combined)

📁 Directory: [directory path]
🌿 Branch: [branch name]

📄 Deliverables:
   - [deliverable 1 filename]
   - [deliverable 2 filename]
   - [deliverable N filename]

➡️  Next Step: Run @prd-context to analyze the project and generate technical context.
```

## Context

{ARGS}
