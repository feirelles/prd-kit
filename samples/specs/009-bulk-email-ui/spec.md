# Feature Specification: Interface de Envio Bulk de Avisos de Coleta

**Feature Branch**: `009-bulk-email-ui`  
**Created**: 2026-01-25  
**Status**: Draft  
**Input**: Deliverable 002 - Interface Completa de Envio Bulk de Avisos de Coleta

## Related Specs

- **007-bulk-collection-tasks-composable**: Composable que fornece dados agregados de tasks de coleta (dependência direta)
- **005-task-email-ui**: Padrões de UI para preview e envio de emails individuais (reutilização de componentes)
- **004-task-email-integration**: Backend APIs de email-preview e email-send (dependência indireta via composables)
- **002-email-core-service**: Serviço de envio de email via Gmail SMTP (dependência indireta)

## Context from Previous Features

### Integration Points Identified

1. **useBulkCollectionTasks composable (007)**: Fornece dados agregados de tasks de coleta com:
   - Filtro por período (startDate, endDate)
   - Dados completos: clientName, serviceName, samplesCount, laboratorySamples
   - Status de email: sent, lastSentAt, emailSendId
   - Loading e error states
   - Este será o composable principal para carregar dados da tabela

2. **Email Preview/Send APIs (004)**: APIs já implementadas:
   - `GET /api/tasks/:taskId/email-preview` - Preview antes do envio
   - `POST /api/tasks/:taskId/email-send` - Envio com tracking
   - Padrão: usar mesmas APIs para envio individual dentro do bulk

3. **Email Modal Pattern (005)**: Modal de preview já existe:
   - Template: `aviso-coleta.vue`
   - Preview HTML renderizado
   - Botões de ação (Enviar/Cancelar)
   - Adaptar para navegação (anterior/próximo) entre múltiplos items

4. **PocketBase Collections**:
   - `email_sends`: Registra cada envio com status, destinatários, template
   - `tasks`: Collection com role='agendamento' para tasks de aviso
   - Cada envio bulk cria múltiplos registros em email_sends

### Patterns from Existing Specs

- **Page Coordinator Pattern**: Páginas de lista gerenciam estado de UI (filtros, seleção, modal, progresso)
- **TanStack Vue Table**: Tabelas com seleção via checkboxes, ordenação, paginação
- **Composables para dados**: Separar lógica de dados (composable) de apresentação (component)
- **Toast notifications**: Feedback visual para sucessos e erros (Nuxt UI)
- **Progress overlay**: Mostrar progresso de operações longas com backdrop semi-transparente

### Database Entities (from PocketBase)

**tasks collection**:
- `id` (text) - ID da task
- `title` (text) - Título
- `dueDate` (date) - Data de vencimento (usado para filtro por período)
- `status` (select) - pending, completed, canceled
- `role` (select) - agendamento (filtro para tasks de aviso de coleta)
- `type` (select) - execution (filtro para tasks de execução)
- `serviceExecutionItemId` (relation) - Vincula task ao item de execução

**email_sends collection**:
- `id` (text) - ID do envio
- `to`, `cc`, `bcc` (json) - Destinatários
- `subject` (text) - Assunto do email
- `templateName` (text) - Nome do template usado (ex: 'aviso-coleta')
- `templateData` (json) - Dados para renderizar template
- `status` (select) - pending, sent, delivered, opened, bounced, failed
- `taskId` (relation) - Vincula envio à task (permite verificar se já enviado)
- `originalEmailId` (relation) - Para reenvios, referencia email original
- `errorMessage` (text) - Mensagem de erro se falhou

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Filtrar Tasks por Período (Priority: P0 - MVP Bloqueador)

Gerente operacional ou equipe de agendamento precisa filtrar tasks de aviso de coleta por um período específico (ex: mês de fechamento) para visualizar todas as coletas que precisam receber avisos.

**Why this priority**: É a base de todo o fluxo. Sem filtrar por período, não há como carregar a lista de coletas para envio em massa. É o primeiro passo obrigatório.

**Independent Test**: Abrir página `/emails/bulk-avisos-coleta`, selecionar período (01/02/2026 a 28/02/2026), clicar "Carregar Lista". Verificar que: (1) apenas tasks com role='agendamento' e dueDate no período são carregadas, (2) contador mostra quantidade encontrada, (3) botão é habilitado após seleção de datas.

**Acceptance Scenarios**:

1. **Given** estou na página de envio bulk, **When** seleciono período (01/02/2026 a 28/02/2026) com 50 tasks disponíveis, **Then** vejo contador "50 coletas encontradas" e botão "Carregar Lista" fica habilitado

2. **Given** selecionei período sem tasks (ex: período futuro sem coletas agendadas), **When** clico "Carregar Lista", **Then** sistema exibe mensagem "Nenhuma coleta encontrada no período" e desabilita botões de ação (Preview/Enviar)

3. **Given** selecionei período válido com 30 tasks, **When** clico "Carregar Lista", **Then** tabela é exibida com 30 linhas mostrando dados de cada coleta (ver US2)

---

### User Story 2 - Selecionar Tasks para Envio (Priority: P0 - MVP Bloqueador)

Usuário visualiza lista detalhada das coletas filtradas e seleciona quais receberão aviso por email. Cada linha mostra informações essenciais (cliente, serviço, data, amostras) e permite seleção individual via checkbox.

**Why this priority**: Controle granular é essencial. Usuário precisa poder excluir casos especiais (ex: cliente já notificado por outro canal, coleta cancelada) antes do envio em massa.

**Independent Test**: Após carregar lista de 20 tasks, verificar que: (1) cada linha tem checkbox, (2) tasks não enviadas vêm marcadas por padrão, (3) tasks já enviadas vêm desmarcadas com badge "Enviado", (4) posso marcar/desmarcar livremente, (5) contador mostra "X de Y selecionados".

**Acceptance Scenarios**:

1. **Given** carreguei lista de 50 tasks (45 não enviadas, 5 já enviadas), **When** tabela é exibida, **Then** vejo 50 linhas, cada uma mostrando: checkbox (45 marcados, 5 desmarcados), cliente, serviço, data formatada, quantidade de amostras, lista de serviços laboratoriais, e badge "Enviado em DD/MM" para as 5 já enviadas

2. **Given** tabela carregada com 45 tasks selecionadas por padrão, **When** desmarco 10 checkboxes, **Then** contador atualiza para "35 de 50 selecionados" em tempo real

3. **Given** marquei 20 tasks e cliquei "Preview dos Selecionados", **When** nenhum item está selecionado, **Then** vejo toast de erro "Selecione pelo menos 1 item" e modal não abre

4. **Given** marquei 15 tasks (incluindo 2 já enviadas anteriormente), **When** clico "Preview dos Selecionados", **Then** modal abre com preview do primeiro dos 15 selecionados (ver US3)

---

### User Story 3 - Preview Navegável de Emails (Priority: P0 - MVP Bloqueador)

Usuário visualiza preview de cada email antes do envio, navegando entre os items selecionados usando botões ou teclado. Preview mostra email renderizado completo com template 'aviso-coleta'.

**Why this priority**: Validação é crítica antes de envio em massa. Usuário precisa confirmar que dados extraídos (data, local, contatos, amostras) estão corretos para evitar retrabalho e reclamações de clientes.

**Independent Test**: Selecionar 10 tasks, abrir preview. Verificar que: (1) modal mostra preview do primeiro email, (2) indicador "Email 1 de 10", (3) botões Anterior/Próximo funcionam, (4) navegação por teclado (setas) funciona, (5) botão "Enviar Todos" está presente.

**Acceptance Scenarios**:

1. **Given** selecionei 10 tasks e cliquei "Preview", **When** modal abre, **Then** vejo preview HTML do primeiro email renderizado, indicador "Email 1 de 10", botão "← Anterior" desabilitado, botão "Próximo →" habilitado, botões "Fechar" e "Enviar Todos"

2. **Given** estou no preview do email 5 de 10, **When** clico "Próximo →", **Then** modal atualiza para mostrar preview do email 6, contador muda para "Email 6 de 10", ambos botões (Anterior e Próximo) ficam habilitados

3. **Given** estou no preview do email 10 de 10 (último), **When** vejo o modal, **Then** botão "Próximo →" está desabilitado, botão "← Anterior" está habilitado

4. **Given** estou no preview do email 3, **When** pressiono tecla seta direita (→), **Then** modal navega para email 4 (mesmo comportamento do botão Próximo)

5. **Given** estou no preview de qualquer email, **When** pressiono tecla Esc, **Then** modal fecha e retorno à tabela de seleção com seleções intactas

---

### User Story 4 - Envio Bulk com Progresso em Tempo Real (Priority: P0 - MVP Bloqueador)

Usuário dispara envio de todos os emails selecionados de uma vez e acompanha progresso em tempo real. Tabela mostra status de cada item (enviando, sucesso, erro) e barra de progresso indica percentual completo.

**Why this priority**: Core da feature - sem envio bulk automatizado, usuário teria que enviar um por um. Feedback em tempo real é essencial para transparência e confiança, especialmente ao processar dezenas de envios.

**Independent Test**: Selecionar 5 tasks, abrir preview, clicar "Enviar Todos". Verificar que: (1) modal fecha, (2) overlay de progresso aparece, (3) barra avança de 0% a 100%, (4) cada linha da tabela atualiza status (enviando → sucesso/erro), (5) ao final, toast mostra resumo (X enviados, Y erros).

**Acceptance Scenarios**:

1. **Given** estou no preview e clico "Enviar Todos" com 10 items selecionados, **When** envio inicia, **Then** modal fecha, overlay de progresso aparece com barra em 0%, tabela mostra status "Enviando..." para cada item, posso continuar navegando na página

2. **Given** envio bulk está em andamento (5 de 10 processados), **When** observo a interface, **Then** barra de progresso mostra 50%, 5 linhas da tabela têm badge verde "✓ Enviado", 5 linhas têm spinner "Enviando...", contador mostra "Enviando 6 de 10..."

3. **Given** envio bulk completou todos os 10 emails com sucesso, **When** processo termina, **Then** vejo toast "10 enviados com sucesso", todas as linhas têm badge "Enviado em DD/MM/YYYY HH:MM", checkboxes desses items são desmarcados automaticamente, overlay desaparece

4. **Given** envio bulk completou com 9 sucessos e 1 erro, **When** processo termina, **Then** vejo toast "9 enviados, 1 erro - Ver Relatório", 9 linhas têm badge verde "Enviado", 1 linha tem ícone vermelho "✗ Erro" com tooltip mostrando mensagem de erro, item com erro permanece marcado para reenvio

5. **Given** linha da tabela com erro de envio, **When** passo mouse sobre ícone de erro, **Then** vejo tooltip com mensagem detalhada do erro (ex: "Email inválido: contato sem email cadastrado", "Falha no servidor SMTP")

---

### User Story 5 - Reenviar Items Previamente Enviados (Priority: P1 - Alta)

Usuário pode reenviar avisos que já foram enviados anteriormente, sem confirmações adicionais. Útil para casos de emails não recebidos, erros de dados corrigidos, ou cliente solicitou reenvio.

**Why this priority**: Alta importância para correção de erros e casos excepcionais. Não é MVP bloqueador (sistema funciona sem), mas é feature muito solicitada para operação diária.

**Independent Test**: Carregar lista com tasks já enviadas (badge "Enviado"), marcar checkbox de uma já enviada, clicar "Enviar Selecionados". Verificar que: (1) envia normalmente sem confirmação adicional, (2) cria novo registro em email_sends, (3) badge atualiza para nova data/hora.

**Acceptance Scenarios**:

1. **Given** task na tabela com badge "Enviado em 15/01/2026 10:30" e checkbox desmarcado por padrão, **When** marco o checkbox e clico "Enviar Selecionados", **Then** sistema envia normalmente sem pedir confirmação, cria novo registro em email_sends com originalEmailId apontando para envio anterior, badge atualiza para "Enviado em 25/01/2026 14:20"

2. **Given** selecionei mix de 5 items (3 nunca enviados, 2 já enviados), **When** disparo envio bulk, **Then** sistema processa todos igualmente, não diferencia novos envios de reenvios, ao final 5 linhas têm badge "Enviado" com timestamp atualizado

3. **Given** task reenviada múltiplas vezes, **When** visualizo linha na tabela, **Then** badge mostra apenas data do envio mais recente (não mostra histórico de reenvios na tabela, apenas data atual)

---

### Edge Cases

**Empty States**:
- Período sem tasks → Mostrar estado vazio com ilustração e mensagem "Nenhuma coleta encontrada no período selecionado"
- Todos os items já enviados → Todos checkboxes desmarcados por padrão, contador "0 de N selecionados", botões de ação desabilitados até selecionar pelo menos 1

**Error Handling**:
- Erro na API ao carregar tasks → Mostrar mensagem de erro com botão "Tentar Novamente", não deixar página quebrada
- Perda de conexão durante bulk send → Registrar enviados com sucesso, marcar pendentes como erro, permitir reenvio dos que falharam
- Email sem destinatário (contato sem email) → Marcar como erro com mensagem clara "Cliente sem email cadastrado", permitir correção e reenvio

**Performance**:
- Carregar 200+ tasks → Implementar lazy loading ou virtualização na tabela, manter performance < 3s para renderização
- Envio de 100+ emails → Processar em batches (ex: 10 por vez), não travar UI, permitir cancelamento

**User Behavior**:
- Usuário fecha página durante envio → Mostrar `beforeunload` alert "Envio em andamento, tem certeza?", se confirmou, envios já processados são registrados
- Usuário tenta enviar sem selecionar nenhum item → Toast de erro "Selecione pelo menos 1 item para enviar", botões ficam desabilitados

**Navigation**:
- Preview no último item, tentar navegar para próximo → Botão "Próximo" desabilitado, tecla seta direita não faz nada
- Preview no primeiro item, tentar navegar para anterior → Botão "Anterior" desabilitado, tecla seta esquerda não faz nada

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Sistema MUST filtrar tasks com role='agendamento' e type='execution' dentro do período selecionado (datas início e fim)
- **FR-002**: Sistema MUST exibir lista de tasks em tabela com colunas: checkbox de seleção, nome do cliente, nome do serviço, data da coleta, quantidade de amostras, lista de serviços laboratoriais, status de envio
- **FR-003**: Sistema MUST marcar automaticamente checkboxes de tasks não enviadas e desmarcar tasks já enviadas ao carregar lista
- **FR-004**: Sistema MUST exibir badge "Enviado em DD/MM/YYYY HH:MM" em tasks que já tiveram email enviado
- **FR-005**: Sistema MUST atualizar contador "X de Y selecionados" em tempo real conforme usuário marca/desmarca checkboxes
- **FR-006**: Sistema MUST validar que pelo menos 1 item está selecionado antes de abrir preview ou iniciar envio
- **FR-007**: Sistema MUST exibir modal de preview mostrando email renderizado com template 'aviso-coleta' e dados da task
- **FR-008**: Sistema MUST permitir navegação entre previews de emails selecionados usando botões "← Anterior" e "Próximo →"
- **FR-009**: Sistema MUST permitir navegação entre previews usando teclas de seta esquerda/direita e fechar modal com tecla Esc
- **FR-010**: Sistema MUST exibir indicador de posição "Email X de N" no modal de preview
- **FR-011**: Sistema MUST desabilitar botão "Anterior" no primeiro email e botão "Próximo" no último email do preview
- **FR-012**: Sistema MUST processar envio bulk em série (um após o outro) para permitir tracking individual de progresso
- **FR-013**: Sistema MUST exibir overlay de progresso com barra percentual (0% a 100%) durante envio bulk
- **FR-014**: Sistema MUST atualizar status de cada linha da tabela em tempo real durante envio: "Enviando...", "✓ Enviado", "✗ Erro"
- **FR-015**: Sistema MUST criar registro em collection email_sends para cada envio bem-sucedido, vinculado à task (taskId)
- **FR-016**: Sistema MUST exibir toast notification ao final do envio bulk com resumo: "X enviados com sucesso" ou "X enviados, Y erros - Ver Relatório"
- **FR-017**: Sistema MUST exibir mensagem de erro específica em tooltip ao passar mouse sobre ícone de erro em linha com falha
- **FR-018**: Sistema MUST desmarcar automaticamente checkboxes de tasks após envio bem-sucedido
- **FR-019**: Sistema MUST manter seleção de checkboxes intacta ao fechar modal de preview sem enviar
- **FR-020**: Sistema MUST permitir reenvio de tasks já enviadas sem confirmação adicional, criando novo registro em email_sends com originalEmailId apontando para envio anterior
- **FR-021**: Sistema MUST restringir acesso à página apenas para usuários com roles: agendamento, gestor, admin
- **FR-022**: Sistema MUST exibir estado vazio com mensagem "Nenhuma coleta encontrada" quando período selecionado não tem tasks
- **FR-023**: Sistema MUST permitir que usuário continue navegando na página durante envio bulk (operação não bloqueia UI)

### Key Entities

- **BulkCollectionTask**: Representa uma task de coleta agregada com dados para envio bulk
  - Attributes: id, clientName, serviceName, collectionDate, samplesCount, laboratorySamples (array), emailStatus (sent, lastSentAt, emailSendId)
  - Relationships: Vinculada a task (tasks collection), service execution, cliente, email_sends

- **EmailSendRecord**: Representa um registro de envio de email
  - Attributes: id, to, cc, bcc, subject, templateName, templateData, status, taskId, originalEmailId, errorMessage
  - Relationships: Vinculado a task (taskId), pode referenciar email original (originalEmailId) para reenvios

- **PreviewState**: Estado do modal de preview durante navegação
  - Attributes: isOpen, currentIndex, selectedTasks (array de tasks selecionadas)
  - Relationships: Referencia subset de BulkCollectionTasks selecionados para preview

- **BulkSendProgress**: Estado de progresso do envio em massa
  - Attributes: inProgress, current, total, results (array com {taskId, status: 'success'|'error', error?: string})
  - Relationships: Rastreia progresso de múltiplos EmailSendRecords

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Usuários completam envio bulk de 50 avisos de coleta em menos de 5 minutos (vs. 2-3 horas manual)
- **SC-002**: Sistema processa e exibe resultados de 100 envios bulk em menos de 3 minutos, com feedback de progresso a cada 5 segundos
- **SC-003**: 100% das tasks processadas têm status atualizado na tabela (sucesso ou erro específico), sem items em estado indefinido
- **SC-004**: Usuários conseguem identificar e reenviar emails com erro em menos de 1 minuto após ver relatório de erros
- **SC-005**: Taxa de erros em envio bulk é inferior a 5% em condições normais (desconsiderando erros de dados como email inválido)
- **SC-006**: Interface mantém performance (tempo de resposta < 2s) ao carregar e renderizar lista de 200+ tasks
- **SC-007**: 95% dos usuários conseguem completar fluxo de filtro → seleção → preview → envio na primeira tentativa, sem necessidade de suporte
- **SC-008**: Tempo de operação mensal de fechamento reduz em 90% (de 2-3h para < 15 minutos) para equipe de agendamento

## Assumptions *(if applicable)*

1. **Composable useBulkCollectionTasks (007) está implementado e testado**: Feature depende diretamente deste composable para carregar dados agregados de tasks
2. **APIs de email (004) estão funcionais**: `/api/tasks/:taskId/email-preview` e `/api/tasks/:taskId/email-send` já implementadas e em produção
3. **Template 'aviso-coleta.vue' existe e está completo**: Template Vue Email com todas as variáveis necessárias (cliente, data, local, serviços, amostras)
4. **Clientes têm email cadastrado**: Tasks processadas têm clientes com pelo menos 1 contato email válido (casos sem email geram erro específico)
5. **Volume típico é 50-100 envios por período**: Performance otimizada para este range (suporta até 200, mas acima disso pode precisar paginação)
6. **Envios são em série, não paralelo**: Para permitir tracking individual de progresso e evitar sobrecarga no servidor SMTP
7. **Usuários têm permissões configuradas**: Roles (agendamento, gestor, admin) já atribuídos corretamente aos usuários no sistema
8. **Browser moderno com JavaScript habilitado**: Interface requer Vue 3, TanStack Table, e recursos modernos (ES6+, async/await)

## Out of Scope *(if applicable)*

- **Agendamento de envio bulk**: Envios são on-demand (usuário dispara manualmente), não há funcionalidade de agendar para data/hora futura
- **Histórico de reenvios por task**: Interface mostra apenas último envio (badge com data mais recente), não lista completa de todos os envios históricos
- **Edição de template antes do envio**: Preview é read-only, não permite editar assunto ou corpo do email antes de enviar
- **Envio de anexos customizados**: Sistema usa anexos padrão configurados no template, não permite adicionar anexos adicionais na interface
- **Filtragem avançada na tabela**: Apenas filtro por período (datas), não há filtros por cliente, serviço, ou status de envio dentro da tabela
- **Exportação de relatório de envios**: Resumo é exibido em toast e tabela atualizada, não há botão para exportar CSV/Excel com resultados
- **Cancelamento de envio em andamento**: Uma vez iniciado, envio bulk processa todos os items selecionados (não há botão "Cancelar Envio")
- **Preview em massa (múltiplos emails simultâneos)**: Modal mostra 1 preview por vez com navegação sequencial, não grid com múltiplos previews
- **Notificação por email ao usuário**: Sistema não envia email ao usuário operador informando conclusão do envio bulk
- **Logs de auditoria detalhados na UI**: Interface não mostra logs técnicos (quem enviou, IP, timestamp exato), apenas status simplificado

## Dependencies *(if applicable)*

### Technical Dependencies

- **007-bulk-collection-tasks-composable**: Composable `useBulkCollectionTasks()` DEVE estar implementado e exportado
- **004-task-email-integration**: APIs `/api/tasks/:taskId/email-preview` e `/api/tasks/:taskId/email-send` DEVEM estar funcionais
- **TanStack Vue Table v8+**: Biblioteca para tabela com seleção de checkboxes, sorting, e estado reativo
- **Nuxt UI v4**: Biblioteca de componentes (Button, Modal, Toast, Badge, DateRangePicker)
- **date-fns v3+**: Para formatação de datas (formato DD/MM/YYYY HH:MM)
- **PocketBase collections**: email_sends e tasks devem existir com schema correto (campos taskId, originalEmailId)

### Feature Dependencies

- **Spec 007**: DEVE estar implementado antes de começar esta feature (bloqueador)
- **Spec 005**: Composable useTaskEmail pode ser referenciado para padrões de envio individual
- **Spec 004**: Backend APIs são pré-requisito obrigatório

### Business Dependencies

- **Permissões de usuário configuradas**: Roles (agendamento, gestor, admin) devem estar atribuídos antes de release
- **Template aviso-coleta testado**: Template Vue Email deve ter sido validado com dados reais de clientes
- **Servidor SMTP configurado**: Credenciais Gmail e limites de envio (ex: 500 emails/dia) configurados e testados

## Integration with Existing Features

### Reuses from Spec 007 (Bulk Collection Tasks Composable)

**Composable Pattern**:
```typescript
// Esta feature USA o composable já implementado em 007
import { useBulkCollectionTasks } from '#imports'

const { tasks, loading, error, loadTasks } = useBulkCollectionTasks()

// Carregar tasks por período
await loadTasks('2026-02-01', '2026-02-28')

// tasks.value agora contém array de BulkCollectionTask com:
// - clientName, serviceName, collectionDate
// - samplesCount, laboratorySamples[]
// - emailStatus.sent, emailStatus.lastSentAt
```

### Reuses from Spec 005 (Task Email UI)

**Modal Preview Pattern**: Adaptar modal existente adicionando:
- Props `items: BulkCollectionTask[]` e `currentIndex: number`
- Navegação: botões Anterior/Próximo + keyboard listeners
- Manter estrutura de preview HTML renderizado do template

**Toast Notifications**: Usar mesmo padrão de feedback:
- Sucesso: toast verde "X enviados com sucesso"
- Erro: toast vermelho "X enviados, Y erros - Ver Relatório"

### Extends Spec 004 (Task Email Integration)

**API Usage Pattern**: Chamar APIs individuais dentro do loop de envio bulk:
```typescript
// Para cada task selecionada:
for (const task of selectedTasks) {
  try {
    const response = await $fetch(`/api/tasks/${task.id}/email-send`)
    // Atualizar status linha: sucesso
  } catch (error) {
    // Atualizar status linha: erro com mensagem
  }
}
```

### Database Integration

**email_sends collection**: Cada envio cria 1 registro:
- `taskId`: vincula ao task.id
- `templateName`: 'aviso-coleta'
- `status`: 'sent' ou 'failed'
- `originalEmailId`: preencher se for reenvio (vincula ao envio anterior)

**Query pattern**: Verificar se task já foi enviada:
```javascript
// No composable 007, query verifica:
emailSends = await pb.collection('email_sends')
  .getList(1, 50, {
    filter: `taskId = '${task.id}'`,
    sort: '-created',
  })

// Se emailSends.items.length > 0: task.emailStatus.sent = true
```

## Notes

### Implementation Priority

1. **Phase 1 - MVP (P0)**: US1, US2, US3, US4 - Fluxo completo de filtro → seleção → preview → envio com progresso
2. **Phase 2 - Enhancement (P1)**: US5 - Reenvio de items já enviados
3. **Phase 3 - Polish**: Edge cases, performance optimization, responsiveness

### UI/UX Considerations

**Layout**: Página full-width com:
- Header: Título "Envio Bulk de Avisos de Coleta" + filtro de período
- Body: Tabela TanStack Vue Table com sticky header
- Footer: Contador de selecionados + botões de ação (Preview, Enviar)

**Colors/Status**:
- Badge "Enviado": verde (#22c55e)
- Status "Enviando...": azul com spinner
- Status "✓ Enviado": verde com ícone check
- Status "✗ Erro": vermelho com tooltip de erro

**Responsive**: Desktop-first (tablet+ apenas), não otimizar para mobile (operação administrativa em escritório)

### Performance Targets

- Load 100 tasks: < 2s
- Render table with 200 rows: < 1s
- Process 50 bulk sends: < 3 min (average 3-4s per send)
- Progress update frequency: every 1 send (real-time)

### Testing Strategy

**Unit Tests**:
- Composable state management (filters, selection, progress)
- Table selection logic (select all, unselect, counter)
- Navigation logic (previous/next, keyboard)

**Integration Tests**:
- Load tasks → verify table renders correctly
- Select items → open preview → verify navigation
- Send bulk → verify API calls and status updates

**E2E Tests**:
- Complete flow: filter → load → select → preview → send → verify results
- Error handling: simulate API failures, verify error messages
- Reenvio: send, then resend same task, verify new record created

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]  
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
