# Tasks: Interface de Envio Bulk de Avisos de Coleta

**Input**: Design documents from `/specs/009-bulk-email-ui/`
**Prerequisites**: plan.md (✅), spec.md (✅), quickstart.md (✅)

**Note**: Tests are OPTIONAL - not explicitly requested in spec. Tasks focus on implementation.

**Organization**: Tasks organized by user story (US1-US5) to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- File paths are relative to repository root

---

## Phase 0: Feature Scaffolding (7 tasks)

**Purpose**: Create complete file structure with minimal boilerplate before implementation

- [x] T000 [Scaffold] Create page-specific type definitions in frontend/shared/types/bulkEmail.ts
  - Create: BulkSendProgress, PreviewModalState, BulkSendResult types
  - Content: Interface stubs with TODO comments for state management types

- [x] T001 [Scaffold] Create page file in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Create: Main page component shell
  - Content: Minimal template with definePageMeta, script setup, and placeholder sections

- [x] T002 [P] [Scaffold] Create Table component in frontend/app/components/BulkEmail/Table.vue
  - Create: Table component shell for TanStack Vue Table with selection
  - Content: Empty component with Props/Emits interface stubs
  - Note: Follow pattern from frontend/app/components/Tasks/Table.vue

- [x] T003 [P] [Scaffold] Create PreviewModal component in frontend/app/components/BulkEmail/PreviewModal.vue
  - Create: Modal component shell for preview with navigation
  - Content: Empty component with Props/Emits interface stubs
  - Note: Adapt pattern from frontend/app/components/Email/PreviewModal.vue

- [x] T004 [P] [Scaffold] Create SendProgress component in frontend/app/components/BulkEmail/SendProgress.vue
  - Create: Progress overlay component shell
  - Content: Empty component with Props interface stubs

- [x] T005 [Scaffold] Verify Nuxt auto-imports work for BulkEmail components
  - Test: Components are auto-imported as <BulkEmailTable>, <BulkEmailPreviewModal>, <BulkEmailSendProgress>
  - Note: Nuxt auto-imports from components/ directory using folder/file naming pattern
  - No index.ts needed - Nuxt handles this automatically

- [x] T006 [Scaffold] Verify TypeScript compilation passes
  - Run: `cd frontend && npm run typecheck`
  - Verify: No errors with stub implementations

**Checkpoint**: Complete file structure created - ready for implementation

---

## Phase 1: Setup & Foundation (3 tasks)

**Purpose**: Establish page routing and basic infrastructure

### Context Required (1 task)

- [ ] T007 [Context] Review nuxt skill for page patterns
  - Read: `.github/skills/nuxt/SKILL.md`
  - Focus: File-based routing, definePageMeta, layout patterns

### Implementation (2 tasks)

- [ ] T008 Setup page routing and layout structure in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: definePageMeta with layout, auth middleware
  - Add: Page title and base container with h-full flex flex-col pattern
  - Add: Import DateRangePicker from ~/lib/components

- [ ] T009 Verify page renders at /emails/bulk-avisos-coleta
  - Test: Navigate to URL in browser
  - Verify: Page loads with title and basic structure

**Checkpoint**: Page is accessible and routing works

---

## Phase 2: User Story 1 - Filtrar Tasks por Período (Priority: P0 - MVP) 🎯 MVP (5 tasks)

**Goal**: Allow user to filter tasks by date range and load collection notices list

**Independent Test**: Open page, select date range (01/02/2026 to 28/02/2026), click "Carregar Lista". Verify tasks load, counter shows quantity, and button enables/disables correctly.

### Context Required (2 tasks)

- [ ] T010 [Context] [US1] Review useBulkCollectionTasks composable implementation
  - Read: `frontend/app/composables/useBulkCollectionTasks.ts`
  - Understand: loadTasks API, return types, loading/error states

- [ ] T011 [Context] [US1] Review DateRangePicker component usage
  - Read: `frontend/app/lib/components/src/components/DateRangePicker.vue`
  - Understand: v-model pattern, date format expected

### Implementation (3 tasks)

- [ ] T012 [US1] Implement date range filter section in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: DateRangePicker component with v-model for dateRange reactive
  - Add: "Carregar Lista" UButton that disables when no date selected
  - Add: Loading state binding to button

- [ ] T013 [US1] Integrate useBulkCollectionTasks composable in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: Import and use composable (tasks, loading, error, loadTasks)
  - Add: handleLoadTasks function that formats dates and calls loadTasks
  - Add: Counter display showing "X coletas encontradas"

- [ ] T014 [US1] Implement empty state and error handling in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: Empty state message "Nenhuma coleta encontrada no período" (only when !loading && tasks.length === 0)
  - Add: Error alert with UAlert color="error" and "Tentar Novamente" button
  - Add: Loading state managed in composable (loading.value from useBulkCollectionTasks)
  - Note: Table uses overlay pattern for loading - see ui.tables.instructions.md

**Checkpoint**: Date filter works, tasks load correctly, empty/error states display

---

## Phase 3: User Story 2 - Selecionar Tasks para Envio (Priority: P0 - MVP) (6 tasks)

**Goal**: Display table with task details and checkbox selection for bulk email

**Independent Test**: After loading 20 tasks, verify each row has checkbox, non-sent tasks are auto-selected, sent tasks show "Enviado" badge, counter shows "X de Y selecionados".

### Context Required (2 tasks)

- [ ] T015 [Context] [US2] Review TanStack Table skill for Vue integration
  - Read: `.github/skills/tanstack-table/SKILL.md`
  - Focus: useVueTable, row selection, checkbox columns, FlexRender

- [ ] T016 [Context] [US2] Review existing table patterns in project
  - Read: `frontend/app/components/Tasks/Table.vue` (lines 1-100)
  - Understand: Column definitions, styling patterns, badge rendering

### Implementation (4 tasks)

- [ ] T017 [US2] Implement BulkEmailTable component with TanStack Vue Table in frontend/app/components/BulkEmail/Table.vue
  - Add: Column definitions for: checkbox, clientName, serviceName, dueDate, samplesCount, laboratorySamples, emailStatus
  - Add: useVueTable with getCoreRowModel and row selection enabled
  - Add: Emit selectedIds updates to parent via onRowSelectionChange
  - Add: Loading overlay pattern (never use v-if to hide table - see ui.tables.instructions.md)

- [ ] T018 [US2] Implement status badge rendering in frontend/app/components/BulkEmail/Table.vue
  - Add: "Enviado em DD/MM HH:mm" badge with color="success" for sent tasks
  - Add: "Pendente" badge with color="neutral" for non-sent tasks
  - Add: Format date using date-fns (format function)
  - Note: Use ONLY semantic color classes (text-primary, bg-muted) - NEVER specific colors like text-green-500

- [ ] T019 [US2] Integrate BulkEmailTable in page with selection state in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: selectedTaskIds as ref<Set<string>>(new Set()) in page state
  - Add: BulkEmailTable component receiving tasks as props, emitting selection changes
  - Add: Auto-select non-sent tasks when tasks are loaded (watcher on tasks)
  - Note: Page is coordinator - components emit events, page updates state (see pages.list-coordinator.instructions.md)

- [ ] T020 [US2] Implement selection counter and action buttons in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: Counter showing "X de Y selecionados" in real-time
  - Add: "Preview dos Selecionados" button (disabled when 0 selected)
  - Add: "Enviar Selecionados" button (disabled when 0 selected)
  - Add: Toast error when clicking buttons with 0 items selected

**Checkpoint**: Table renders with all columns, selection works, counter updates in real-time

---

## Phase 4: User Story 3 - Preview Navegável de Emails (Priority: P0 - MVP) (5 tasks)

**Goal**: Preview modal with navigation between selected emails using buttons and keyboard

**Independent Test**: Select 10 tasks, open preview. Verify modal shows first email, indicator "Email 1 de 10", navigation buttons work, keyboard arrows navigate, Esc closes modal.

### Context Required (2 tasks)

- [ ] T021 [Context] [US3] Review existing Email PreviewModal component
  - Read: `frontend/app/components/Email/PreviewModal.vue` (lines 1-200)
  - Understand: Modal structure, preview rendering, iframe pattern

- [ ] T022 [Context] [US3] Review VueUse onKeyStroke for keyboard navigation
  - Read: VueUse documentation for onKeyStroke
  - Understand: Key binding pattern for ArrowLeft, ArrowRight, Escape

### Implementation (3 tasks)

- [ ] T023 [US3] Implement BulkEmailPreviewModal with navigation in frontend/app/components/BulkEmail/PreviewModal.vue
  - Add: UModal with v-model:open prop, position indicator "Email X de N"
  - Add: Previous/Next buttons with disabled states at boundaries
  - Add: useFetch to load preview from /api/tasks/:taskId/email-preview
  - Add: Loading and error states for preview fetch
  - Note: Reuse iframe pattern from Email/PreviewModal.vue

- [ ] T024 [US3] Implement keyboard navigation in frontend/app/components/BulkEmail/PreviewModal.vue
  - Add: onKeyStroke('ArrowLeft') for previous navigation
  - Add: onKeyStroke('ArrowRight') for next navigation
  - Add: onKeyStroke('Escape') to close modal
  - Add: Guard conditions to respect boundary states

- [ ] T025 [US3] Integrate BulkEmailPreviewModal in page in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: previewModal reactive state (isOpen, currentIndex, selectedTasks array)
  - Add: Open modal on "Preview" button click with selected tasks
  - Add: Handle navigation events (next, previous, close)
  - Add: Preserve selection when modal closes without sending

**Checkpoint**: Preview modal shows emails with navigation, keyboard shortcuts work

---

## Phase 5: User Story 4 - Envio Bulk com Progresso (Priority: P0 - MVP) (6 tasks)

**Goal**: Execute bulk send with real-time progress tracking and table status updates

**Independent Test**: Select 5 tasks, preview, click "Enviar Todos". Verify modal closes, progress overlay shows 0-100%, table rows update status, toast shows summary at end.

### Context Required (1 task)

- [ ] T026 [Context] [US4] Review email-send API endpoint
  - Read: `frontend/server/api/tasks/[taskId]/email-send.post.ts`
  - Understand: Request format, response structure, error handling

### Implementation (5 tasks)

- [ ] T027 [US4] Implement BulkSendProgress overlay component in frontend/app/components/BulkEmail/SendProgress.vue
  - Add: Fixed overlay with semi-transparent backdrop (bg-background/80 backdrop-blur-sm)
  - Add: Progress bar with percentage (0% to 100%) using UProgress or custom
  - Add: Counter text "Enviando X de Y..."
  - Add: Results list showing success/error status per task

- [ ] T028 [US4] Implement bulk send orchestration function in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: bulkProgress reactive state (inProgress, current, total, results)
  - Add: executeBulkSend async function with sequential API calls
  - Add: Progress update after each send (current++, update results)
  - Add: Error handling with continue-on-error pattern

- [ ] T029 [US4] Integrate progress overlay and send button in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: BulkSendProgress component with bulkProgress binding
  - Add: "Enviar Todos" button in modal footer that triggers executeBulkSend
  - Add: Close modal when send starts, show progress overlay

- [ ] T030 [US4] Implement real-time table status updates during send in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: Update task.emailStatus in tasks array as each send completes
  - Add: Reactive binding so table re-renders with new status
  - Add: Auto-deselect successfully sent tasks after completion

- [ ] T031 [US4] Implement completion toast and cleanup in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: Toast notification on completion ("X enviados com sucesso" or "X enviados, Y erros")
  - Add: Hide progress overlay when done
  - Add: Keep errored items selected for retry

**Checkpoint**: Full bulk send flow works with real-time progress and status updates

---

## Phase 6: User Story 5 - Reenviar Items (Priority: P1) (3 tasks)

**Goal**: Allow resending previously sent emails without extra confirmation

**Independent Test**: Load tasks with already-sent items (badge "Enviado"), manually select one, click "Enviar Selecionados". Verify sends normally, creates new email_sends record with originalEmailId, badge updates to new date.

### Context Required (1 task)

- [ ] T032 [Context] [US5] Review originalEmailId field usage in email_sends
  - Read: PocketBase schema for email_sends collection
  - Understand: How originalEmailId tracks resends

### Implementation (2 tasks)

- [ ] T033 [US5] Update bulk send to support resends in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: Pass originalEmailId to email-send API when task has emailStatus.emailSendId
  - Verify: API creates new record with relation to original
  - Test: Resent items show updated timestamp

- [ ] T034 [US5] Verify resend flow works end-to-end
  - Test: Select mix of never-sent and already-sent tasks
  - Verify: Both process identically without confirmation dialogs
  - Verify: Badge shows latest send date after resend

**Checkpoint**: Resend feature works, no distinction in UI between new sends and resends

---

## Phase 7: Polish & Edge Cases (5 tasks)

**Purpose**: Handle edge cases, improve UX, and ensure robustness

- [ ] T035 [P] Implement beforeunload warning during active send in frontend/app/pages/emails/bulk-avisos-coleta.vue
  - Add: Window beforeunload event listener when bulkProgress.inProgress
  - Add: Warning message "Envio em andamento, tem certeza?"
  - Add: Remove listener when send completes

- [ ] T036 [P] Add error tooltips to table rows in frontend/app/components/BulkEmail/Table.vue
  - Add: Error icon with UTooltip for failed sends
  - Add: Display errorMessage from BulkSendResult in tooltip
  - Add: Red badge styling for error state (color="error")

- [ ] T037 [P] Implement table row styling for send-in-progress state in frontend/app/components/BulkEmail/Table.vue
  - Add: Spinner icon and "Enviando..." text while processing
  - Add: Disable checkbox while row is being processed
  - Add: Visual feedback for currently sending row

- [ ] T038 Verify performance with 100+ tasks
  - Test: Load 100-200 tasks, measure render time
  - Verify: Table renders < 1s, no UI jank
  - Note: Add virtualization if needed (out of scope for MVP)

- [ ] T039 Run quickstart.md validation checklist
  - Verify: All phases from quickstart work as documented
  - Test: Full flow from filter → preview → send
  - Document: Any deviations or additional notes

**Checkpoint**: Edge cases handled, UX polished, feature is production-ready

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 0 (Scaffolding)**: No dependencies - create file structure first
- **Phase 1 (Setup)**: Depends on Phase 0 - establishes routing
- **Phase 2 (US1 - Filter)**: Depends on Phase 1 - adds date filter
- **Phase 3 (US2 - Table)**: Depends on Phase 2 - displays filtered tasks
- **Phase 4 (US3 - Preview)**: Depends on Phase 3 - previews selected tasks
- **Phase 5 (US4 - Bulk Send)**: Depends on Phase 4 - sends selected tasks
- **Phase 6 (US5 - Resend)**: Depends on Phase 5 - enhances send for resends
- **Phase 7 (Polish)**: Depends on Phases 2-5 - improves all features

### User Story Dependencies (after foundational phases)

- **US1 (Filter)**: Independent foundation for all other stories
- **US2 (Table)**: Depends on US1 for data
- **US3 (Preview)**: Depends on US2 for selection
- **US4 (Bulk Send)**: Depends on US3 for workflow
- **US5 (Resend)**: Enhancement to US4, not blocking

### Parallel Opportunities

**Within Phase 0**:
```
T002 [Scaffold] BulkEmail/Table.vue
T003 [Scaffold] BulkEmail/PreviewModal.vue  } Can run in parallel
T004 [Scaffold] BulkEmail/SendProgress.vue
```

**Within Phase 7**:
```
T035 [P] beforeunload warning
T036 [P] Error tooltips        } Can run in parallel
T037 [P] Row styling
```

**Between User Stories** (if team has capacity):
- After Phase 3 (US2) completes, US3 can start while US2 polish continues
- Phases 2-5 are sequential per MVP requirement

---

## Implementation Strategy

### MVP First (US1-US4)

1. **Phase 0**: Create all file stubs (~30 min)
2. **Phase 1**: Setup routing (~30 min)
3. **Phase 2 (US1)**: Date filter + load tasks (~2-3 hours)
4. **Phase 3 (US2)**: Table with selection (~3-4 hours)
5. **Phase 4 (US3)**: Preview modal (~2-3 hours)
6. **Phase 5 (US4)**: Bulk send orchestration (~3-4 hours)

**MVP Estimated Time**: 1.5-2 days

### Incremental Delivery

After MVP:
- **Phase 6 (US5)**: Resend feature (~1-2 hours)
- **Phase 7**: Polish and edge cases (~2-3 hours)

**Total Estimated Time**: 2-3 days

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 39 |
| **Phase 0 (Scaffolding)** | 7 tasks |
| **Phase 1 (Setup)** | 3 tasks |
| **Phase 2 (US1 - Filter)** | 5 tasks |
| **Phase 3 (US2 - Table)** | 6 tasks |
| **Phase 4 (US3 - Preview)** | 5 tasks |
| **Phase 5 (US4 - Bulk Send)** | 6 tasks |
| **Phase 6 (US5 - Resend)** | 3 tasks |
| **Phase 7 (Polish)** | 5 tasks |
| **Parallel Opportunities** | 8 tasks marked [P] |
| **Context Tasks** | 8 tasks marked [Context] |

### Independent Test Criteria Per Story

| User Story | Independent Test |
|------------|------------------|
| US1 | Filter by date → Tasks load with count |
| US2 | Load tasks → Table shows with selection working |
| US3 | Select tasks → Preview with navigation works |
| US4 | Preview → Bulk send with progress tracking |
| US5 | Select sent item → Resend creates new record |

### Suggested MVP Scope

**Minimum Viable**: US1 + US2 + US3 + US4 (Phases 0-5)
- User can filter, select, preview, and bulk send emails
- Real-time progress and status updates
- ~1.5-2 days of work

**Full Feature**: Add US5 + Polish (Phases 6-7)
- Resend functionality for previously sent items
- Edge case handling and UX improvements
- ~2-3 days total

---

## Notes

- All dependencies verified: useBulkCollectionTasks composable ✅, email APIs ✅, DateRangePicker ✅
- No backend changes required - reuses existing APIs from Specs 004 & 007
- Page Coordinator Pattern: UI state managed in page component, not in store
- Sequential sending for individual progress tracking (not parallel)
- Desktop-first layout (no mobile optimization required)

### Critical Patterns from Instructions

| Pattern | Instruction File | Key Rule |
|---------|------------------|----------|
| **Loading Overlay** | ui.tables.instructions.md | Never use v-if to hide table during load - use overlay |
| **Semantic Colors** | nuxt.components.instructions.md | ONLY use text-primary, bg-muted, etc. NEVER text-green-500 |
| **Page Coordinator** | pages.list-coordinator.instructions.md | Page manages state, components emit events |
| **TanStack Table** | ui.tanstack-table.instructions.md | Use `get data()` getter, emit sorting changes |
| **Error Handling** | error-handling.instructions.md | Always wrap async in try-catch-finally |

### Component Directory Structure

```
frontend/app/components/
├── BulkEmail/                    # 🆕 New directory for this feature
│   ├── Table.vue                 # TanStack table with selection
│   ├── PreviewModal.vue          # Navigation preview modal  
│   └── SendProgress.vue          # Progress overlay
├── Email/                        # Existing - reuse patterns from here
│   └── PreviewModal.vue          # Reference for iframe pattern
└── Tasks/                        # Existing - reuse patterns from here
    └── Table.vue                 # Reference for TanStack setup
```
