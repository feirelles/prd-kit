# Deliverables: Envio de Emails em Bulk Manual

**Source PRD**: [../PRD.md](../PRD.md)  
**Generated**: 2026-01-25  
**Total Deliverables**: 2

---

## Overview

Este diretório contém os deliverables técnicos decompostos do PRD de Envio de Emails em Bulk Manual. Cada deliverable representa um componente implementável independentemente, com dependências claramente definidas.

---

## Deliverables

### [001] Composable de Busca de Tasks de Coleta com Dados Agregados
**File**: [deliverable-001-bulk-collection-tasks-api.md](deliverable-001-bulk-collection-tasks-api.md)  
**Type**: Frontend (Composable)  
**Priority**: High  
**Effort**: Small (2-3 days)  
**Dependencies**: None  
**User Stories**: US1, US2

**Description**: Composable Vue que encapsula a lógica de busca e agregação de dados, consumindo PocketBase diretamente via SDK. Retorna tasks filtradas por período com dados agregados (cliente, serviço, amostras laboratoriais, status de email).

**Key Technical Points**:
- Composable: `useBulkCollectionTasks()`
- Query otimizada com expand multi-nível no PocketBase
- Batch fetching de lab services e email status (evita N+1 queries)
- Reactive state: `tasks`, `loading`, `error`
- Performance target: < 3s para 200 tasks
- **Sem endpoint server intermediário** (acesso direto ao PocketBase)

---

### [002] Interface Completa de Envio Bulk de Avisos de Coleta
**File**: [deliverable-002-bulk-email-sending-ui.md](deliverable-002-bulk-email-sending-ui.md)  
**Type**: Frontend  
**Priority**: High  
**Effort**: Medium (5-7 days)  
**Dependencies**: 001  
**User Stories**: US1, US2, US3, US4, US5

**Description**: Interface completa incluindo filtro por período, tabela de seleção, modal de preview com navegação, envio bulk com progresso interativo e relatório final.

**Key Technical Points**:
- Página: `/emails/bulk-avisos-coleta`
- TanStack Vue Table com checkbox selection
- Modal de preview adaptado com navegação (← →)
- Envio sequencial com useEmailService
- Progresso em tempo real na tabela
- Permissões: agendamento, gestor, admin

---

## Implementation Order

```
Phase 1: Composable Foundation
  └─ [001] Composable (2-3 days)

Phase 2: Complete Frontend
  └─ [002] Full UI (5-7 days, depends on 001)

Total: 7-10 days sequential
```

### Dependency Graph

```
[001] Composable ────► [002] Complete Frontend UI
```

---

## Getting Started

### For Frontend Developers

**Start with Deliverable 001** (Composable):

1. Read [deliverable-001-bulk-collection-tasks-api.md](deliverable-001-bulk-collection-tasks-api.md)
2. Create composable: `app/composables/useBulkCollectionTasks.ts`
3. Implement:
   - `loadTasks(startDate, endDate)` with PocketBase queries
   - Batch fetching optimization (critical!)
   - Transform logic to aggregate data
4. Test with:
   ```typescript
   const { tasks, loading, error, loadTasks } = useBulkCollectionTasks()
   await loadTasks('2026-02-01', '2026-02-28')
   console.log(tasks.value)
   ```
5. Validate:
   - No N+1 queries (check PocketBase logs)
   - Performance < 3s for 100+ tasks
   - All data fields populated correctly

**Then Deliverable 002** (UI Page):

1. **Wait for composable** (deliverable 001) to be complete
2. Read [deliverable-002-bulk-email-sending-ui.md](deliverable-002-bulk-email-sending-ui.md)
3. Create page: `app/pages/emails/bulk-avisos-coleta.vue`
4. Use the composable created in 001
5. Implement UI components:
   - Date filter
   - Table with checkboxes
   - PComposable
cd /path/to/project
specify init 001-bulk-collection-tasks-composable
# Provide deliverable-001 content when prompted

# For Frontend UISpec Kit

Each deliverable can be used as input for Spec Kit to generate detailed implementation specs:

```bash
# For Backend
cd /path/to/project
specify init 001-bulk-collection-tasks-api
# Provide deliverable-001 content when prompted

# For Frontend
specify init 002-bulk-email-sending-ui
# Provide deliverable-002 content when prompted
```

---

## Validation

All deliverables have been validated:
- ✅ Structure follows template
- ✅ All required sections present
- ✅ User stories properly formatted
- ✅ Acceptance criteria in Gherkin
- ✅ Dependencies correctly mapped

Run validation manually:
```bash
cd .prd-kit
python3 validators/check-deliverables.py "../prds/Envio de Emails em Bulk Manual/deliverables/"
```

---

## Questions?

Refer back to:
- [PRD](../PRD.md) for full context
- [Research](../research.md) for discovery notes
- [deliverables-map.json](deliverables-map.json) for structured decomposition

Or consult with Product Team for clarifications.
