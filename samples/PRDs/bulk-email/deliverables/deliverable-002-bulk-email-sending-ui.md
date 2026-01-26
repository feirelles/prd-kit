# Deliverable: Interface Completa de Envio Bulk de Avisos de Coleta

**Source PRD**: prds/Envio de Emails em Bulk Manual/PRD.md  
**Deliverable ID**: 002  
**Dependencies**: 001 (Composable useBulkCollectionTasks)  
**Priority**: High  
**Effort**: Medium (5-7 days)

---

## Context

Com o composable `useBulkCollectionTasks` implementado (deliverable 001), este deliverable cria a interface completa para envio em massa de avisos de coleta. A interface permite filtrar por período, visualizar lista de coletas, selecionar quais enviar, fazer preview navegável dos emails, e executar envio bulk com feedback de progresso em tempo real.

**Fluxo do Usuário**:
1. Seleciona período (data início/fim)
2. Carrega lista de coletas (via API)
3. Revisa tabela, marca/desmarca items
4. Abre preview modal, navega entre selecionados
5. Confirma e dispara envio bulk
6. Acompanha progresso em tempo real
7. Vê relatório final (sucessos/erros)

**Business Impact**: Reduz tempo de envio mensal de 2-3h para < 5 minutos, com controle total e rastreabilidade.

---

## User Stories

### [US1] Filtrar Coletas por Período
**Priority**: P0 (MVP - Bloqueador)

**As a** Gerente Operacional ou equipe de Agendamento  
**I want to** filtrar tasks de aviso de coleta por período (range de datas)  
**So that** eu veja apenas as coletas do mês que estou fechando

**Acceptance Criteria:**
```gherkin
Given estou na página de envio bulk de avisos
When seleciono um período (data início e data fim)
Then o sistema busca todas as tasks com role='agendamento' 
  And exibe a quantidade de items encontrados
  And habilita o botão "Carregar Lista"

Given não há tasks no período selecionado
When clico em "Carregar Lista"
Then o sistema exibe mensagem "Nenhuma coleta encontrada no período"
  And desabilita botões de ação

Given selecionei um período válido com tasks
When clico em "Carregar Lista"
Then o sistema carrega a tabela de seleção (US2)
```

### [US2] Selecionar Items para Envio
**Priority**: P0 (MVP - Bloqueador)

**As a** Gerente Operacional ou equipe de Agendamento  
**I want to** ver lista detalhada das coletas filtradas e selecionar quais receberão aviso  
**So that** eu tenha controle granular sobre os envios e possa excluir casos especiais

**Acceptance Criteria:**
```gherkin
Given carreguei lista de coletas do período
When a tabela é exibida
Then cada linha mostra:
  - Checkbox de seleção (marcado por padrão)
  - Nome do cliente
  - Nome do serviço principal
  - Data da coleta (formatada)
  - Quantidade de amostras
  - Lista de serviços laboratoriais
  And items já enviados vêm com checkbox desmarcado
  And items já enviados têm badge "Enviado em DD/MM"
  And posso marcar/desmarcar qualquer item livremente
  And contador mostra "X de Y selecionados"

Given marquei/desmarquei items
When clico em "Preview dos Selecionados"
Then sistema valida se há pelo menos 1 item selecionado
  And abre modal de preview com primeiro item selecionado

Given nenhum item está selecionado
When clico em "Preview" ou "Enviar Selecionados"
Then sistema exibe mensagem de erro "Selecione pelo menos 1 item"
```

### [US3] Preview de Emails com Navegação
**Priority**: P0 (MVP - Bloqueador)

**As a** Gerente Operacional ou equipe de Agendamento  
**I want to** visualizar preview de cada email antes de enviar, navegando entre os selecionados  
**So that** eu valide se os dados estão corretos antes do disparo em massa

**Acceptance Criteria:**
```gherkin
Given abri o preview dos items selecionados
When modal é exibido
Then vejo:
  - Preview do email completo renderizado
  - Indicador de posição "Email 1 de N"
  - Botão "← Anterior" (desabilitado no primeiro)
  - Botão "Próximo →" (desabilitado no último)
  - Botão "Fechar"
  - Botão "Enviar Todos"
  And preview usa template 'aviso-coleta' com variáveis preenchidas

Given estou no preview do item X
When clico em "Próximo"
Then modal atualiza para mostrar preview do item X+1
  And contador atualiza para "Email X+1 de N"

Given estou no preview do item X
When clico em "Anterior"
Then modal atualiza para mostrar preview do item X-1

Given naveguei entre vários items
When clico em "Fechar"
Then modal fecha e retorno à tabela de seleção
  And seleções permanecem intactas
```

### [US4] Enviar Bulk com Progresso
**Priority**: P0 (MVP - Bloqueador)

**As a** Gerente Operacional ou equipe de Agendamento  
**I want to** disparar envio de todos os emails selecionados de uma vez, vendo o progresso  
**So that** eu complete o processo rapidamente e tenha visibilidade do status de cada envio

**Acceptance Criteria:**
```gherkin
Given revisei os previews e confirmo os envios
When clico em "Enviar Todos"
Then modal de preview fecha
  And sistema retorna à tabela de seleção
  And exibe barra de progresso "Enviando X de N..."
  And tabela atualiza status de cada item em tempo real:
    - "Enviando..." (loading)
    - "✓ Enviado" (sucesso)
    - "✗ Erro" (falha) com mensagem
  And posso continuar navegando na página durante envio

Given envio está em andamento
When todos os emails são processados
Then sistema exibe notificação com resumo:
  - Total enviado com sucesso
  - Total com erro (se houver)
  - Botão "Ver Relatório Detalhado"
  And items enviados ficam marcados com badge "Enviado"
  And checkbox desses items é desmarcado automaticamente

Given alguns envios falharam
When vejo o relatório
Then sistema lista apenas os items com erro
  And para cada erro mostra: cliente, motivo da falha
  And posso marcar novamente os items com erro para reenvio
```

### [US5] Reenviar Items Previamente Enviados
**Priority**: P0 (MVP)

**As a** Gerente Operacional  
**I want to** reenviar avisos que já foram enviados anteriormente sem confirmações adicionais  
**So that** eu possa corrigir rapidamente casos de emails não recebidos

**Acceptance Criteria:**
```gherkin
Given um item que já teve email enviado (badge "Enviado em DD/MM")
  And esse item está desmarcado por padrão na tabela
When marco o checkbox desse item
  And clico em "Enviar Selecionados"
Then sistema envia normalmente sem pedir confirmação de reenvio
  And cria novo registro em email_sends
  And atualiza badge para data/hora do novo envio

Given selecionei mix de items (alguns já enviados, outros não)
When envio o batch
Then sistema processa todos igualmente
  And não diferencia novos envios de reenvios
```

---

## Technical Requirements

### Page Structure

**Route**: `/emails/bulk-avisos-coleta`

**File**: `app/pages/emails/bulk-avisos-coleta.vue`

**Layout**: Usar layout padrão do sistema com header/navigation

**Permissions**: Role check - apenas `agendamento`, `gestor`, `admin`

### Components Architecture

```
bulk-avisos-coleta.vue (Page Coordinator)
├── FilterSection (inline ou component)
│   └── DateRangePicker (Nuxt UI)
├── CollectionTasksTable (TanStack Vue Table)
│   ├── Checkbox column
│   ├── Data columns (cliente, serviço, data, etc)
│   └── Status badge
├── PreviewModal (adapted from existing modal)
│   ├── Email preview render
│   ├── Navigation controls (← →)
│   └── Action buttons
└── ProgressOverlay (during bulk send)
    ├── Progress bar
    └── Status list
```

### State Management

**Page State** (usar composables, não store):
```typescript
const filters = ref({
  startDate: null,
  endDate: null
})

const tasks = ref<BulkCollectionTask[]>([])
const selectedTaskIds = ref<Set<string>>(new Set())
const loadingTasks = ref(false)

const previewModal = ref({
  isOpen: false,
  currentIndex: 0,
  items: [] // apenas tasks selecionadas
})

const bulkSendProgress = ref({
  inProgress: false,
  current: 0,
  total: 0,
  results: [] // {taskId, status: 'success'|'error', error?: string}
})
```

### Data Flow

1. **Load Tasks** (usa deliverable 001):
   ```typescript
   const { tasks, loading, error, loadTasks } = useBulkCollectionTasks()
   
   const handleLoadTasks = async () => {
     await loadTasks(filters.value.startDate, filters.value.endDate)
     
     // Auto-select all except already sent
     selectedTaskIds.value = new Set(
       tasks.value
         .filter(t => !t.emailStatus.sent)
         .map(t => t.taskId)
     )
   }
   ```

2. **Open Preview**:
   ```typescript
   const openPreview = () => {
     const selectedTasks = tasks.value.filter(t => 
       selectedTaskIds.value.has(t.taskId)
     )
     if (selectedTasks.length === 0) {
       toast.error('Selecione pelo menos 1 item')
       return
     }
     previewModal.value = {
       isOpen: true,
       currentIndex: 0,
       items: selectedTasks
     }
   }
   ```

3. **Bulk Send**:
   ```typescript
   const sendBulk = async () => {
     const selectedTasks = tasks.value.filter(t => 
       selectedTaskIds.value.has(t.taskId)
     )
     
     bulkSendProgress.value = {
       inProgress: true,
       current: 0,
       total: selectedTasks.length,
       results: []
     }
     
     previewModal.value.isOpen = false
     
     for (const task of selectedTasks) {
       try {
         const result = await useEmailService().send({
           templateName: 'aviso-coleta',
           to: /* get from contacts */,
           data: { /* task data */ },
           taskId: task.taskId
         })
         
         bulkSendProgress.value.results.push({
           taskId: task.taskId,
           status: 'success'
         })
         
         // Update task in table
         task.emailStatus = { sent: true, lastSentAt: new Date().toISOString() }
         
       } catch (error) {
         bulkSendProgress.value.results.push({
           taskId: task.taskId,
           status: 'error',
           error: error.message
         })
       }
       
       bulkSendProgress.value.current++
     }
     
     bulkSendProgress.value.inProgress = false
     showSummaryToast()
   }
   ```

### UI Components

**Table (TanStack Vue Table)**:
- Checkbox selection column
- Client name
- Service name
- Collection date (formatted with date-fns)
- Samples count
- Laboratory samples (comma-separated)
- Status badge (Enviado/Pendente)

**Preview Modal**:
- Fullscreen or large modal
- Email preview (usar composable de renderização existente)
- Navigation: `← Anterior` | `Email X de N` | `Próximo →`
- Actions: `Fechar` | `Enviar Todos`
- Keyboard support: Arrow keys, Esc

**Progress Overlay**:
- Semi-transparent backdrop
- Progress bar with percentage
- List of items showing status icons
- "Enviando...", "✓ Enviado", "✗ Erro"

### Integration with Existing Code

**Reuse**:
- `useBulkCollectionTasks` composable (deliverable 001) ✓
- `useEmailService` composable (já existe)
- Template rendering logic (se houver composable)
- Date formatting utilities
- Toast notifications (Nuxt UI)

**New**:
- Page route configuration
- Page state management (filters, selection)
- Table component setup (TanStack Vue Table)
- Preview modal adaptation (adicionar navegação)
- Bulk send orchestration with progress

---

## Acceptance Criteria

```gherkin
Given acesso a página /emails/bulk-avisos-coleta como gestor
When página carrega
Then vejo filtro de período (date range picker)
  And vejo botão "Carregar Lista" desabilitado até selecionar datas

Given selecionei período e cliquei "Carregar Lista"
When API retorna 50 tasks
Then vejo tabela com 50 linhas
  And cada linha mostra todos os dados (cliente, serviço, data, qtd, amostras, status)
  And tasks não enviadas vêm com checkbox marcado
  And tasks já enviadas vêm com checkbox desmarcado e badge "Enviado"
  And contador mostra "45 de 50 selecionados" (se 5 já foram enviadas)

Given marquei 10 items e cliquei "Preview"
When modal abre
Then vejo preview do primeiro email renderizado
  And vejo "Email 1 de 10"
  And botão Anterior está desabilitado
  And botão Próximo está habilitado

Given estou no preview do email 5 de 10
When clico "Próximo"
Then vejo preview do email 6
  And contador atualiza para "Email 6 de 10"
  And ambos botões (Anterior e Próximo) estão habilitados

Given estou no preview e clico "Enviar Todos"
When envio bulk inicia
Then modal fecha
  And vejo overlay de progresso
  And tabela começa a atualizar status linha por linha
  And barra de progresso avança de 0% a 100%

Given envio bulk completou 10 emails (9 sucesso, 1 erro)
When processo termina
Then vejo toast de resumo: "9 enviados, 1 erro"
  And 9 linhas têm badge "Enviado" e checkbox desmarcado
  And 1 linha tem ícone de erro com mensagem
  And posso marcar a linha com erro e reenviar

Given tentei enviar sem selecionar nenhum item
When clico "Preview" ou "Enviar Selecionados"
Then vejo toast de erro "Selecione pelo menos 1 item"
  And modal não abre

Given usuário sem permissão (role: coletor)
When tenta acessar /emails/bulk-avisos-coleta
Then é redirecionado ou vê mensagem "Acesso negado"
```

---

## Integration Points
Composable**: `useBulkCollectionTasks()` (Deliverable 001) - carrega e agrega dados
### Consumes
- **API Endpoint**: `GET /api/tasks/bulk-collection-notices` (Deliverable 001)
- **Email Service**: `useEmailService().send()` (já existente)
- **Contacts API**: Para buscar destinatários dos emails (assumindo existente)
- **Auth/Permissions**: Role check middleware/composable

### Provides
- **User Interface**: Página completa acessível via menu/navegação
- **Bulk Email Flow**: End-to-end desde filtro até relatório

### Side Effects
- Cria registros em `email_sends` (via useEmailService)
- Pode gerar notificações/logs de auditoria

---

## Notes for Implementation

### Modal Adaptation Strategy

Se já existe modal de preview:
1. Identificar componente: buscar por "preview" em `app/components/`
2. Opções:
   - **A**: Adaptar componente existente adicionando props `items[]` e `currentIndex`
   - **B**: Criar versão inline na página (copiar/adaptar lógica)
3. Preferir **B** se modal existente for muito acoplado a envio individual

### Performance Considerations

- **Lazy load table rows**: Se > 100 items, considerar virtualização
- **Debounce**: Filtro de data com debounce antes de chamar API
- **Abort controller**: Cancelar request anterior se usuário mudar filtros rapidamente
- **Progress batching**: Atualizar UI a cada 5 items (não a cada 1) se volume grande

### Testing Checklist

- [ ] Carregar lista com dados reais
- [ ] Testar seleção/deseleção de checkboxes
- [ ] Testar navegação no preview (← →)
- [ ] Testar navegação por teclado (arrow keys)
- [ ] Testar envio bulk com 3-5 items
- [ ] Testar tratamento de erro (forçar falha em 1 item)
- [ ] Testar reenvio de item já enviado
- [ ] Testar permissões (roles diferentes)
- [ ] Validar responsividade (desktop/tablet)
- [ ] Validar loading states (skeleton, spinners)

### Edge Cases

- Período sem tasks → mostrar estado vazio
- Todos os items já enviados → todos checkboxes desmarcados
- Erro na API ao carregar → mostrar mensagem, permitir retry
- Perda de conexão durante bulk → registrar enviados, permitir reenvio dos pendentes
- Usuário fecha página durante envio → avisar com `beforeunload`

---

**Implementation Checklist**:
- [ ] Criar página `app/pages/emails/bulk-avisos-coleta.vue`
- [ ] Importar e usar `useBulkCollectionTasks()` (deliverable 001)
- [ ] Implementar filtro de período com DateRangePicker
- [ ] Implementar tabela com TanStack Vue Table + checkboxes
- [ ] Implementar lógica de seleção (select all, unselect)
- [ ] Implementar contador de selecionados
- [ ] Adaptar/criar modal de preview com navegação
- [ ] Implementar lógica de navegação (← → keyboard)
- [ ] Implementar bulk send orchestration
- [ ] Implementar overlay de progresso
- [ ] Implementar atualização de status em tempo real na tabela
- [ ] Implementar toast de resumo final
- [ ] Adicionar validação de permissões (role check)
- [ ] Adicionar tratamento de erros completo
- [ ] Testar fluxo end-to-end com dados reais
- [ ] Validar performance com 100+ items
- [ ] Adicionar loading states e feedback visual
