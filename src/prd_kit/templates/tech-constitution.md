# Technical Constitution

This document defines the **invariant technical rules** for the project. All architectural decisions, code implementation, and pattern selection MUST align with these rules.

---

## 1. Technology Stack (Strict)

| Layer | Technology | Version Constraints |
|-------|------------|---------------------|
| **Frontend Framework** | [e.g., Nuxt 4, React] | [e.g., Latest stable] |
| **Language** | [e.g., TypeScript] | [e.g., Strict mode] |
| **Styling** | [e.g., TailwindCSS, @nuxt/ui] | [e.g., No raw CSS] |
| **State Management** | [e.g., Pinia] | [e.g., Setup stores only] |
| **Backend/Database** | [e.g., PocketBase, Supabase] | [e.g., Typed client] |
| **Testing** | [e.g., Vitest] | [e.g., Unit + E2E] |

---

## 2. Coding Standards

### General Principles
- **DRY (Don't Repeat Yourself)**: Extract reusable logic into composables/hooks.
- **Type Safety**: No `any`. All props, emits, and API responses must be typed.
- **Files**: PascalCase for components (`UserCard.vue`), camelCase for logic (`useUser.ts`).

### Component Guidelines
- **Logic Extraction**: Components should focus on UI. Business logic goes to composables.
- **Props Definition**: Use TypeScript interfaces for props.
- **Style Co-location**: Styles must be scoped or utility-first.

### State Management Rules
- **Local vs Global**: Use component state for UI (modals, forms), global store for shared data (user, session).
- **Persistance**: Explicitly define what needs to survive page reloads.

---

## 3. Architecture Patterns

### Directory Structure (Strict)
```
[ROOT]/
├── components/     # UI Components only
├── composables/    # Business logic & Reusable state
├── pages/          # Route definitions (minimal logic)
├── server/         # Backend endpoints
├── types/          # Shared TypeScript interfaces
└── utils/          # Pure helper functions
```

### Data Flow
1. **API Layer**: Typed client fetches data.
2. **Service Layer**: Composables transform/cache data.
3. **UI Layer**: Components consume composables.

---

## 4. Testing Strategy

- **Unit Tests**: Required for all utility functions and complex composables.
- **Component Tests**: Required for core UI components.
- **E2E Tests**: Required for critical user flows (auth, checkout).

---

## 5. Security & Performance

- **Auth**: Never store tokens in localStorage (use httpOnly cookies).
- **Validation**: All user input must be validated (zod/valibot) before processing.
- **Loading**: Every async action must have a loading state.
- **Error Handling**: All errors must be caught and displayed to user gracefully.
