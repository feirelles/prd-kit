---
description: Initialize or update technical stack and coding rules
---

This workflow helps you establish the Technical Constitution for the project.

1. **Read Command Instructions**
   Read `.prd-kit/commands/tech-constitution.md`.

2. **Check Existing Constitution**
   Check if `.prd-kit/memory/tech-constitution.md` exists. read it if it does.

3. **Auto-Discovery**
   Analyze project files to infer tech stack:
   - `package.json`
   - `tsconfig.json`
   - `.eslintrc` / `.prettierrc`
   - Project structure

4. **Interview User**
   Ask about:
   - Tech Stack details (Frontend, Backend, Database)
   - Coding Standards (Naming, Logic placement)
   - Architecture Patterns (Directory structure, Data flow)
   - Quality Gates (Testing, Linting)

5. **Create/Update Constitution**
   Write to `.prd-kit/memory/tech-constitution.md` covering:
   - Technology Stack
   - Coding Standards
   - Architecture Patterns
   - Quality/Testing requirements
