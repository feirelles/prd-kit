# Deliverable: Composable de Busca de Tasks de Coleta com Dados Agregados

**Source PRD**: prds/Envio de Emails em Bulk Manual/PRD.md  
**Deliverable ID**: 001  
**Dependencies**: None  
**Priority**: High  
**Effort**: Small (2-3 days)

---

## Context

Quando a equipe fecha a agenda mensal de coletas, precisa enviar avisos em massa para todos os clientes. Atualmente não há forma de obter uma lista consolidada de tasks de coleta com todas as informações necessárias para exibição e envio (cliente, serviço, amostras, status de email).

Este deliverable provê um **composable Vue** que encapsula a lógica de busca e agregação de dados, consumindo diretamente o PocketBase via SDK. O composable retorna tasks filtradas por período com dados agregados de múltiplas collections em formato otimizado para a UI.

**Business Impact**: Habilita filtro por período e exibição de lista consolidada, reduzindo tempo de 2-3h para < 5 minutos no processo mensal.

**Architectural Decision**: Usa composable + PocketBase SDK (não endpoint intermediário) seguindo padrão do projeto.

---

## User Stories

### [US1] Filtrar Coletas por Período
**Priority**: P0 (MVP - Bloqueador)

**As a** Gerente Operacional ou equipe de Agendamento  
**I want to** filtrar tasks de aviso de coleta por período (range de datas)  
**So that** eu veja apenas as coletas do mês que estou fechando

**Context**: Tasks de aviso de coleta têm `role === 'agendamento'` e `type === 'execution'`. O filtro usa `dueDate` da task.

**Acceptance Criteria:**
```gherkin
Given estou na página de envio bulk de avisos
When seleciono um período (data início e data fim)
Then o sistema busca todas as tasks com role='agendamento' 
  And filtra por dueDate dentro do período selecionado
  And exibe a quantidade de items encontrados
  And habilita o botão "Carregar Lista"
```

### [US2] Selecionar Items para Envio
**Priority**: P0 (MVP - Bloqueador)

**As a** Gerente Operacional ou equipe de Agendamento  
**I want to** ver lista detalhada das coletas filtradas e selecionar quais receberão aviso  
**So that** eu tenha controle granular sobre os envios e possa excluir casos especiais

**Context**: Tabela mostra dados do service_execution_item relacionado à task. Serviços laboratoriais identificados via `service.segment === 'laboratorial'` no mesmo `serviceExecutionId`.

**Relevant Criteria (Backend):**
```gherkin
Given carreguei lista de coletas do período
When a tabela é exibida
Then cada linha mostra:
  - Nome do cliente (via service_execution → contract → client)
  - Nome do serviço principal
  - Data da coleta (dueDate da task formatada)
  - Quantidade de amostras (soma de expectedQuantity dos items laboratoriais)
  - Lista de serviços laboratoriais (nomes separados por vírgula)
  And items já enviados (existem em email_sends) vêm marcados como enviados
```

---

## Technical Requirements

### Composable Specification

**File**: `app/composables/useBulkCollectionTasks.ts` ou `composables/useBulkCollectionTasks.ts`

**Exported Function**: `useBulkCollectionTasks()`

**Return Interface**:
```typescript
interface UseBulkCollectionTasksReturn {
  // State
  tasks: Ref<BulkCollectionTask[]>
  loading: Ref<boolean>
  error: Ref<string | null>
  
  // Actions
  loadTasks: (startDate: string, endDate: string) => Promise<void>
  refreshTask: (taskId: string) => Promise<void>
  
  // Computed
  totalCount: ComputedRef<number>
  sentCount: ComputedRef<number>
  pendingCount: ComputedRef<number>
}
```

**Data Type**:
```typescript
interface BulkCollectionTask {
  taskId: string
  dueDate: string // ISO datetime
  clientId: string
  clientName: string
  serviceName: string
  samplesCount: number
  laboratorySamples: string[] // Array de nomes dos serviços laboratoriais
  emailStatus: { (PocketBase SDK)

1. **Base Query**: Tasks com `role='agendamento'` e `type='execution'` no período
   ```typescript
   const tasks = await pb.collection('tasks').getFullList({
     filter: `role='agendamento' && type='execution' && dueDate >= '${startDate}' && dueDate <= '${endDate}'`,
     expand: 'serviceExecutionItemId.contractServiceId.contractId.clientId,serviceExecutionItemId.contractServiceId.serviceId',
     sort: 'dueDate'
   })
   ```

2. **Laboratory Services Lookup** (para cada task):
   ```typescript
   const serviceExecutionId = task.expand.serviceExecutionItemId.serviceExecutionId
   
   const labItems = await pb.collection('service_execution_items').getFullList({
     filter: `serviceExecutionId='${serviceExecutionId}'`,
     expand: 'contractServiceId.serviceId'
   })
   
   const labServices = labItems.filter(item => 
     item.expand?.contractServiceId?.expand?.serviceId?.segment === 'laboratorial'
   )
   
   const samplesCount = labServices.reduce((sum, item) => 
     sum + (item.expectedQuantity || 0), 0
   )
   
   const laboratorySamples = labServices.map(item => 
     item.expand?.contractServiceId?.expand?.serviceId?.name
  Composable deve carregar dados em < 3 segundos para 200 tasks
- Usar expand strategy eficiente do PocketBase
- **Otimização crítica**: Batch fetch de lab services (evitar N+1 queries)
  - Buscar todos `service_execution_items` de uma vez com `IN` filter
  - Agrupar por `serviceExecutionId` no client
- Considerar índices no PocketBase:
  - `tasks.role` + `tasks.type` + `tasks.dueDate`
  - `email_sends.taskId`
  - `service_execution_items.serviceExecutionId`

### Error Handling

- Try/catch em cada query do PocketBase
- Retornar array vazio se período sem tasks (não erro)
- Tratamento de falhas parciais (ex: email status indisponível)
- Atualizar `error.value` com mensagem user-friendly
- Log de erros com contexto (taskId, query step) via `console.error`
     lastSentAt: emailSends[0]?.created,
     emailSendId: emailSends[0]?.id
   }
   ```

4. **Transform & Aggregate**:
   - Mapear dados expandidos para estrutura limpa
   - Agregar laboratory services
   - Combinar email status
   - Retornar array de `BulkCollectionTask`

1. **Base Query**: Tasks com `role='agendamento'` e `type='execution'` no período
2. **Expand Layers**:
   - `serviceExecutionItemId` → `contractServiceId.serviceId`
   - `contractServiceId.contractId` → `clientId`
3. **Laboratory Services Lookup**:
   - Para cada task, buscar `service_execution_items` do mesmo `serviceExecutionId`
   - Filtrar onde `contractServiceId.serviceId.segment === 'laboratorial'`
   - Agregar `expectedQuantity` (soma) e `serviceId.name` (array)
4. **Email Status Check**:
   - Query em `email_sends` com `taskId = task.id`
   - Ordenar por `created DESC`
   - Pegar o mais recente para status

### Performance Requirements

- Query deve completar em < 3 segundos para 200 tasks
- Usar expand strategy eficiente (batch fetching se disponível)
- Considerar índices em:
  - `tasks.role` + `tasks.type` + `tasks.dueDate`
  - `email_sends.taskId`
  - `service_execution_items.serviceExecutionId`

### Error Handling

- Validar formato de datas
- Retornar array vazio se período sem tasks (não erro)
- Tratamento de falhas em queries relacionadas (lab services, email status)
- Log de erros com contexto (taskId, query step)

---
composable useBulkCollectionTasks
When chamo loadTasks('2026-02-01', '2026-02-28')
Then tasks.value é populado com array de tasks
  And cada task contém: taskId, dueDate, clientName, serviceName, samplesCount, laboratorySamples[], emailStatus
  And tasks estão filtradas por role='agendamento' e type='execution'
  And dueDate está dentro do período solicitado
  And laboratorySamples contém apenas serviços com segment='laboratorial'
  And samplesCount é a soma de expectedQuantity dos items laboratoriais
  And emailStatus.sent é true se existe registro em email_sends para a task
  And loading.value volta para false após conclusão

Given período sem tasks de coleta
When chamo loadTasks com período vazio
Then tasks.value é array vazio
  And error.value é null (não é erro)
  And totalCount.value é 0

Given período com 100 tasks
When chamo loadTasks
Then operação completa em < 3 segundos
  And todos os 100 items em tasks.value têm dados completos agregados
  And não há N+1 queries (lab services buscados em batch)

Given task tem múltiplos serviços laboratoriais
When chamo loadTasks que inclui essa task
Then laboratorySamples contém array com todos os nomes
  And samplesCount é a soma de todos expectedQuantity

Given erro no PocketBase (network, auth, etc)
When chamo loadTasks
Then error.value contém mensagem amigável
  And loading.vSDK**: `usePocketBase()` composable
- **Collections**:
  - `tasks`: Base query, filtros, dueDate
  - `service_execution_items`: Dados de execução, link para contract/service
  - `contract_services`: Ligação com services
  - `services`: Nome e segment (laboratorial)
  - `contracts`: Link para client
  - `clients`: Nome do cliente
  - `email_sends`: Status de envio, timestamp

### Provides
- **Composable**: `useBulkCollectionTasks()`
- **Return Type**: `UseBulkCollectionTasksReturn` (reactive state + actions)
- **Consumed By**: Deliverable 002 (Frontend UI - página bulk)

### No Server-Side Logic Required
- Tudo roda no cliente via PocketBase SDK
- Sem necessidade de endpoints Nuxt intermediários
- Autenticação gerenciada pelo PocketBase client automaticamenteial)
  - `contracts`: Link para client
  - `clients`: Nome do cliente
  - `email_sends`: Status de envio, timestamp

### Provides
- **Endpoint REST**: `/api/tasks/bulk-collection-notices`
- **Response Type**: `BulkCollectionTasksResponse`
- **Consumed By**: Deliverable 002 (Frontend UI)
Composable Structure (seguir padrão do projeto)
```typescript
// app/composables/useBulkCollectionTasks.ts
export const useBulkCollectionTasks = () => {
  const { pb } = usePocketBase()
  
  // State
  const tasks = ref<BulkCollectionTask[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  // Computed
  const totalCount = computed(() => tasks.value.length)
  const sentCount = computed(() => 
    tasks.value.filter(t => t.emailStatus.sent).length
  )
  const pendingCount = computed(() => totalCount.value - sentCount.value)
  
  // Actions
  const loadTasks = async (startDate: string, endDate: string) => {
    loading.value = true
    error.value = null
    
    try {
      // 1. Buscar tasks base
      const tasksData = await pb.collection('tasks').getFullList({
        filter: `role='agendamento' && type='execution' && dueDate >= '${startDate}' && dueDate <= '${endDate}'`,
        expand: 'serviceExecutionItemId.contractServiceId.contractId.clientId,serviceExecutionItemId.contractServiceId.serviceId',
        sort: 'dueDate'
      })
      
      if (tasksData.length === 0) {
        tasks.value = []

**Critical**: Evitar N+1 queries usando batch fetching:
- ✅ Buscar todas lab services de uma vez com `serviceExecutionId IN (id1, id2, ...)`
- ✅ Buscar todos email sends de uma vez com `taskId IN (id1, id2, ...)`
- ✅ Agrupar results no client usando `Map` para O(1) lookup
- ❌ NÃO fazer loop com await para cada task (N+1 anti-pattern)

**Expand Strategy**:
- Usar expand multi-nível na query inicial de tasks
- Reduz round-trips ao PocketBase
- PocketBase resolve expands eficientemente server-side

**Caching** (opcional, se performance ainda for problema):
- Cache results no composable com timestamp
- Invalidar composable `app/composables/useBulkCollectionTasks.ts` ou `composables/useBulkCollectionTasks.ts`
- [ ] Implementar `loadTasks()` com query base de tasks + filtros de data
- [ ] Implementar batch fetch de laboratory services (evitar N+1)
- [ ] Implementar batch fetch de email status (evitar N+1)
- [ ] Implementar `transformTask()` helper para agregação
- [ ] Implementar `refreshTask()` para atualizar task individual
- [ ] Adicionar tratamento de erros e logging
- [ ] Criar interface TypeScript `BulkCollectionTask` em tipos adequados
- [ ] Testar com dados reais no PocketBase dev (5-10 tasks)
- [ ] Validar performance com 100+ tasks (< 3 segundos)
- [ ] Verificar que não há N+1 queries (usar logs do PocketBase)
- [ ] Testar edge cases (dados faltando, expands incompletos)
- [ ] Documentar uso do composable com exemplo no README ou comentários
**Integration Tests**:
- Criar tasks de teste no PocketBase dev
- Testar com 5-10 tasks reais
- Validar estrutura de dados retornada
- Verificar que não há N+1 queries (usar PocketBase logs)

**Performance Test**:
- Criar 100+ tasks via script
- Medir tempo de loadTasks()
- Deve ser < 3 segundos
- Usar `console.time('loadTasks')` para debug

**Edge Cases**:
- Task sem `serviceExecutionItemId` → logar warning, pular
- Service execution sem lab items → samplesCount = 0, laboratorySamples = []
- Cliente sem nome → usar "Cliente desconhecido"
- Expand incompleto → tratar gracefully com optional chaining
        .map(id => `serviceExecutionId='${id}'`)
        .join(' || ')
      
      const allLabItems = await pb.collection('service_execution_items').getFullList({
        filter: labItemsFilter,
        expand: 'contractServiceId.serviceId'
      })
      
      // Agrupar por serviceExecutionId
      const labItemsByExecution = new Map()
      allLabItems.forEach(item => {
        const execId = item.serviceExecutionId
        if (!labItemsByExecution.has(execId)) {
          labItemsByExecution.set(execId, [])
        }
        labItemsByExecution.get(execId).push(item)
      })
      
      // 3. Batch fetch de email status
      const taskIds = tasksData.map(t => t.id)
      const emailSendsFilter = taskIds
        .map(id => `taskId='${id}'`)
        .join(' || ')
      
      const emailSends = await pb.collection('email_sends').getFullList({
        filter: emailSendsFilter,
        sort: '-created'
      })
      
      // Agrupar por taskId (pegar o mais recente)
      const emailsByTask = new Map()
      emailSends.forEach(email => {
        if (!emailsByTask.has(email.taskId)) {
          emailsByTask.set(email.taskId, email)
        }
      })
      
      // 4. Transform & aggregate
      tasks.value = tasksData.map(task => transformTask(
        task,
        labItemsByExecution,
        emailsByTask
      ))
      
    } catch (err: any) {
      console.error('useBulkCollectionTasks: loadTasks failed', err)
      error.value = err.message || 'Erro ao carregar tasks'
      tasks.value = []
    } finally {
      loading.value = false
    }
  }
  
  const refreshTask = async (taskId: string) => {
    // Atualizar apenas uma task específica (após envio de email)
    // Implementação similar mas focada em 1 task
  }
  
  return {
    tasks: readonly(tasks),
    loading: readonly(loading),
    error: readonly(error),
    totalCount,
    sentCount,
    pendingCount,
    loadTasks,
    refreshTask
  }
}

// Helper function
function transformTask(
  task: any,
  labItemsByExecution: Map<string, any[]>,
  emailsByTask: Map<string, any>
): BulkCollectionTask {
  const sei = task.expand?.serviceExecutionItemId
  const client = sei?.expand?.contractServiceId?.expand?.contractId?.expand?.clientId
  const service = sei?.expand?.contractServiceId?.expand?.serviceId
  
  const serviceExecutionId = sei?.serviceExecutionId
  const labItems = labItemsByExecution.get(serviceExecutionId) || []
  
  const labServices = labItems.filter(item => 
    item.expand?.contractServiceId?.expand?.serviceId?.segment === 'laboratorial'
  )
  
  const samplesCount = labServices.reduce((sum, item) => 
    sum + (item.expectedQuantity || 0), 0
  )
  
  const laboratorySamples = labServices
    .map(item => item.expand?.contractServiceId?.expand?.serviceId?.name)
    .filter(Boolean)
  
  const emailSend = emailsByTask.get(task.id)
  
  return {
    taskId: task.id,
    dueDate: task.dueDate,
    clientId: client?.id || '',
    clientName: client?.name || client?.companyName || 'Cliente desconhecido',
    serviceName: service?.name || 'Serviço não especificado',
    samplesCount,
    laboratorySamples,
    emailStatus: {
      sent: !!emailSend,
      lastSentAt: emailSend?.created,
      emailSendId: emailSend?.id
    },
    serviceExecutionItemId: sei?.id || '',
    contractId: sei?.expand?.contractServiceId?.contractId || '',
    _rawTask: task
  }
}nst labItems = await pb.collection('service_execution_items').getFullList({
  filter: `serviceExecutionId='${task.expand.serviceExecutionItemId.serviceExecutionId}' && contractServiceId.serviceId.segment='laboratorial'`,
  expand: 'contractServiceId.serviceId'
})

// Verificar email status:
const emailSends = await pb.collection('email_sends').getFullList({
  filter: `taskId='${task.id}'`,
  sort: '-created',
  limit: 1
})
```

### Optimization Strategies
- Batch fetch de lab services (reduzir N+1 queries)
- Cache de expand results se PocketBase suportar
- Considerar worker/queue se volume > 200 tasks

### Testing Considerations
- Mock PocketBase responses para unit tests
- Integration test com dados reais (3-5 tasks)
- Performance test com 100+ tasks
- Edge case: task sem service_execution_item (deve logar warning)

---

**Implementation Checklist**:
- [ ] Criar endpoint `/api/tasks/bulk-collection-notices` em `server/api/tasks/bulk-collection-notices.get.ts`
- [ ] Implementar query base de tasks com filtros de data
- [ ] Implementar agregação de laboratory services
- [ ] Implementar verificação de email status
- [ ] Adicionar validação de roles (agendamento, gestor, admin)
- [ ] Adicionar tratamento de erros e logging
- [ ] Criar tipos TypeScript em `shared/types/` ou `server/utils/`
- [ ] Testar com dados reais (desenvolvimento)
- [ ] Validar performance com 100+ records
- [ ] Documentar query patterns para manutenção futura
