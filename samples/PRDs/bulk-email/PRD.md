# PRD: Interface de Envio Bulk de Avisos de Coleta

**Created**: 2026-01-24 | **Author**: Product Team | **Status**: Draft  
**Priority**: P0 (Imediato) | **Source**: [research.md](research.md)

---

## Problem Statement

### The Problem

Quando a agenda mensal de coletas é fechada, a equipe precisa notificar todos os clientes sobre suas coletas programadas. Atualmente, esse processo requer envio manual repetitivo de avisos individuais, consumindo horas de trabalho e criando risco de esquecimento de clientes.

**Who has this problem**: Gerente Operacional e equipe de Agendamento que fecham a agenda mensal.

**How they cope today**: Processo manual de envio individual ou processo não sistematizado, levando a:
- Tempo excessivo gasto em tarefa repetitiva
- Risco de clientes não notificados
- Falta de rastreabilidade de quais avisos foram enviados
- Retrabalho quando precisa reenviar

### Impact

**Custo operacional**: Horas de trabalho manual todo mês (estimado: 2-3 horas/mês para ~100 avisos)

**Risco de qualidade**: Clientes não notificados podem gerar reclamações, perda de confiança, e problemas operacionais nas coletas

**Eficiência**: Processo crítico mensal que bloqueia outros trabalhos até ser concluído

### Evidence

- Sistema de envio individual já existe (specs/002-email-core-service)
- Volume validado: ~100 avisos de coleta por mês
- Frequência: 1x por mês no fechamento da agenda
- Templates e tracking já implementados
- Caso de uso recorrente e previsível

---

## Solution Overview

### Proposed Solution

Interface web para envio em massa de avisos de coleta, com fluxo controlado:

1. **Filtro por período**: Seleção de range de datas (baseado em `dueDate` das tasks)
2. **Tabela de seleção**: Lista com checkboxes mostrando todos os items filtrados
3. **Preview com navegação**: Modal reutilizável com anterior/próximo para revisar emails
4. **Envio bulk**: Disparo em lote com progresso interativo e relatório final

**Diferencial**: Integração total com sistema existente (templates, tracking, tasks), permitindo controle granular sobre quem recebe e quando, mantendo rastreabilidade completa.

### Key Benefits

- **Eficiência 10x**: De 2-3 horas para < 5 minutos no processo mensal completo
- **Controle total**: Seleção manual de quem recebe, preview antes de enviar, possibilidade de reenvio
- **Rastreabilidade**: 100% dos envios registrados em `email_sends` com status e eventos
- **Agilidade sem sacrificar qualidade**: Filtros ágeis + preview + validação antes do envio
- **Zero retrabalho**: Sistema marca items já enviados, evitando duplicações

### Out of Scope

- Envio automático/agendado (já existe via US3 do PRD original de emails)
- Customização de templates (usa template 'aviso-coleta' existente)
- Edição de conteúdo do email (template é fixo e parametrizado)
- Outros tipos de email além de aviso de coleta (foco exclusivo em coletas)
- Confirmação de reenvio (usuário pode remarcar e reenviar diretamente)
- Agendamento de envio para data futura

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

Given não há tasks no período selecionado
When clico em "Carregar Lista"
Then o sistema exibe mensagem "Nenhuma coleta encontrada no período"
  And desabilita botões de ação

Given selecionei um período válido com tasks
When clico em "Carregar Lista"
Then o sistema carrega a tabela de seleção (US2)
```

---

### [US2] Selecionar Items para Envio
**Priority**: P0 (MVP - Bloqueador)

**As a** Gerente Operacional ou equipe de Agendamento  
**I want to** ver lista detalhada das coletas filtradas e selecionar quais receberão aviso  
**So that** eu tenha controle granular sobre os envios e possa excluir casos especiais

**Context**: Tabela mostra dados do service_execution_item relacionado à task. Serviços laboratoriais identificados via `service.segment === 'laboratorial'` no mesmo `serviceExecutionId`.

**Acceptance Criteria:**
```gherkin
Given carreguei lista de coletas do período
When a tabela é exibida
Then cada linha mostra:
  - Checkbox de seleção (marcado por padrão)
  - Nome do cliente (via service_execution → contract → client)
  - Nome do serviço principal
  - Data da coleta (dueDate da task formatada)
  - Quantidade de amostras (soma de expectedQuantity dos items laboratoriais)
  - Lista de serviços laboratoriais (nomes separados por vírgula)
  And items já enviados (existem em email_sends) vêm com checkbox desmarcado
  And items já enviados têm indicador visual (badge "Enviado em DD/MM")
  And posso marcar/desmarcar qualquer item livremente
  And contador mostra "X de Y selecionados"

Given marquei/desmarquei items
When clico em "Preview dos Selecionados"
Then sistema valida se há pelo menos 1 item selecionado
  And abre modal de preview (US3) com primeiro item selecionado

Given nenhum item está selecionado
When clico em "Preview dos Selecionados" ou "Enviar Selecionados"
Then sistema exibe mensagem de erro "Selecione pelo menos 1 item"
```

**Data Requirements**:
- Buscar `service_execution_items` onde `serviceExecutionId` = task's service_execution_item_id
- Filtrar items com `contractServiceId.serviceId.segment === 'laboratorial'`
- Agregar `expectedQuantity` para total de amostras
- Coletar `serviceId.name` de todos items laboratoriais

---

### [US3] Preview de Emails com Navegação
**Priority**: P0 (MVP - Bloqueador)

**As a** Gerente Operacional ou equipe de Agendamento  
**I want to** visualizar preview de cada email antes de enviar, navegando entre os selecionados  
**So that** eu valide se os dados estão corretos antes do disparo em massa

**Context**: Reutiliza modal de preview existente (de envio individual), adicionando botões de navegação "Anterior" e "Próximo".

**Acceptance Criteria:**
```gherkin
Given abri o preview dos items selecionados
When modal é exibido
Then vejo:
  - Preview do email completo renderizado (destinatário, assunto, corpo HTML)
  - Indicador de posição "Email 1 de N"
  - Botão "← Anterior" (desabilitado no primeiro)
  - Botão "Próximo →" (desabilitado no último)
  - Botão "Fechar"
  - Botão "Enviar Todos" (principal)
  And preview usa template 'aviso-coleta' com variáveis preenchidas

Given estou no preview do item X
When clico em "Próximo"
Then modal atualiza para mostrar preview do item X+1
  And contador atualiza para "Email X+1 de N"

Given estou no preview do item X
When clico em "Anterior"
Then modal atualiza para mostrar preview do item X-1
  And contador atualiza para "Email X-1 de N"

Given naveguei entre vários items
When clico em "Fechar"
Then modal fecha e retorno à tabela de seleção
  And seleções permanecem intactas
```

**Technical Notes**:
- Preview renderiza template usando dados reais de cada task/service_execution_item
- Navegação percorre apenas items com checkbox marcado (não todos da tabela)
- Estado de navegação (posição atual) mantido no modal

---

### [US4] Enviar Bulk com Progresso
**Priority**: P0 (MVP - Bloqueador)

**As a** Gerente Operacional ou equipe de Agendamento  
**I want to** disparar envio de todos os emails selecionados de uma vez, vendo o progresso  
**So that** eu complete o processo rapidamente e tenha visibilidade do status de cada envio

**Context**: Usa composable `useEmailService` existente. Cada envio registrado em `email_sends` com `status`, vinculado à `taskId` correspondente.

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
    - "✗ Erro" (falha) com mensagem de erro
  And posso continuar navegando na página durante o envio

Given envio está em andamento
When todos os emails são processados
Then sistema exibe notificação de sucesso com resumo:
  - Total enviado com sucesso
  - Total com erro (se houver)
  - Botão "Ver Relatório Detalhado"
  And items enviados ficam marcados na tabela com badge "Enviado"
  And checkbox desses items é desmarcado automaticamente

Given alguns envios falharam
When vejo o relatório
Then sistema lista apenas os items com erro
  And para cada erro mostra: cliente, motivo da falha
  And posso marcar novamente os items com erro para reenvio
```

**Performance Requirements**:
- Envio de 100 emails: < 2 minutos (média 2s por email)
- Taxa de erro esperada: < 1%
- Feedback visual atualizado a cada email processado

**Error Handling**:
- Falhas individuais NÃO interrompem o batch
- Sistema continua enviando os demais após erro
- Erros registrados em log e mostrados no relatório final

---

### [US5] Reenviar Items Previamente Enviados
**Priority**: P0 (MVP)

**As a** Gerente Operacional  
**I want to** reenviar avisos que já foram enviados anteriormente sem confirmações adicionais  
**So that** eu possa corrigir rapidamente casos de emails não recebidos ou situações especiais

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
  And não diferencia novos envios de reenvios no processo
```

**Business Rule**: Reenvios são tratados como novos envios. Não há validação ou bloqueio. Responsabilidade do usuário.

---

## Non-Functional Requirements

### Performance

- **Carregamento de lista**: Filtro + query de tasks: < 3 segundos para 200 items
- **Renderização de tabela**: < 1 segundo para 200 linhas
- **Preview de email**: Renderização de template: < 500ms
- **Envio bulk**: 
  - 100 emails: < 2 minutos (média 1.2s por email incluindo tracking)
  - Sem bloqueio de UI durante envio
  - Feedback de progresso atualizado a cada email (não apenas no final)

### Usability

- **Fluxo linear**: Filtro → Seleção → Preview → Envio (máximo 4 passos)
- **Tempo total**: < 5 minutos do início ao envio completo de 100 avisos
- **Feedback claro**: Estados de loading, sucesso, erro visíveis em tempo real
- **Prevenção de erros**: 
  - Validação de período obrigatório
  - Alerta se nenhum item selecionado
  - Confirmação visual de items já enviados

### Security

- **Permissões**: Apenas roles `agendamento`, `gestor`, `admin` podem acessar
- **Audit trail**: Todos envios registrados em `email_sends` com `senderId` (usuário que disparou)
- **Rate limiting**: Não aplicável (volume baixo, 1x/mês)

### Reliability

- **Resiliência**: Falhas individuais não interrompem batch
- **Rastreabilidade**: 100% dos envios (sucesso e falha) registrados em `email_sends`
- **Idempotência**: Reenvios criam novos registros (não atualizam existentes)
- **Timeout**: Email individual timeout após 10s (retry automático 1x)

### Accessibility

- Tabela navegável por teclado (tab, space para checkboxes)
- Indicadores visuais complementados com texto (não apenas cores)
- Modal de preview navegável por teclado (← → para navegação)

---

## Success Metrics

### Primary Metrics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Tempo para enviar 100 avisos | 2-3 horas (manual) | < 5 minutos | Time tracking da sessão |
| Taxa de erro em envios | N/A | < 1% | `COUNT(status='failed') / COUNT(total)` em `email_sends` |
| Taxa de adoção | 0% | 100% | Uso mensal pela equipe |

### Supporting Metrics

- **Eficiência**: Tempo médio por envio individual: < 2 segundos
- **Qualidade**: Taxa de reenvios necessários: < 5%
- **Rastreabilidade**: 100% dos envios com registro em `email_sends`

### Guardrail Metrics

- **Tempo de carregamento**: Nenhum passo > 3 segundos
- **Disponibilidade**: 99% uptime (dependente de infraestrutura existente)
- **Satisfação**: Zero reclamações de clientes não notificados

---

## Risks & Mitigations

### High Risk

**R1: Volume maior que esperado (>200 envios) causa timeout ou travamento**

- **Probability**: Low (histórico valida ~100/mês)
- **Impact**: High (processo mensal crítico bloqueado)
- **Mitigation**: 
  - Implementar paginação se lista > 150 items
  - Processamento assíncrono com queue (considerar se volume crescer)
  - Permitir cancelamento de batch em andamento

**R2: Falha no SMTP bloqueia todos os envios**

- **Probability**: Medium (dependência externa)
- **Impact**: High (processo bloqueado)
- **Mitigation**:
  - Retry automático com backoff exponencial (já implementado no core service)
  - Mensagem clara de erro com ação corretiva
  - Permitir reenvio fácil dos items que falharam

### Medium Risk

**R3: Usuário fecha página durante envio, perde progresso**

- **Probability**: Medium
- **Impact**: Medium (retrabalho)
- **Mitigation**:
  - Warning antes de fechar página se envio em andamento
  - Envios processados em background (não bloqueiam navegação)
  - Items já enviados ficam marcados mesmo se usuário sair

**R4: Dados de amostras laboratoriais incorretos ou faltando**

- **Probability**: Low (dados vêm de tasks já validadas)
- **Impact**: Medium (email com informação errada)
- **Mitigation**:
  - Preview obrigatório antes de enviar
  - Validação de dados mínimos (cliente, serviço, data)
  - Indicador visual se dados incompletos

### Low Risk

**R5: Performance degrada com filtros muito amplos (6+ meses)**

- **Probability**: Low (uso normal: 1 mês por vez)
- **Impact**: Low (apenas lentidão)
- **Mitigation**:
  - Sugestão de período (último mês, próximo mês)
  - Warning se período > 3 meses
  - Limit máximo de 200 results

---

## Dependencies

### Internal Dependencies

- ✅ **Sistema de Email Core** (specs/002-email-core-service):
  - Composable `useEmailService` com método `send()`
  - Template 'aviso-coleta' já implementado
  - Collections `email_sends`, `email_events` no PocketBase
  - Tracking de abertura/clique funcionando

- ✅ **Tasks & Service Executions**:
  - Collection `tasks` com fields: `role`, `dueDate`, `serviceExecutionItemId`, `type`
  - Collection `service_execution_items` com expand para `contractServiceId.serviceId`
  - Field `service.segment` para identificar serviços laboratoriais

- ✅ **Modal de Preview**:
  - Componente existente de preview de email individual
  - Necessita adaptação: adicionar navegação (anterior/próximo)

### External Dependencies

- Gmail SMTP (já configurado no sistema de emails)
- PocketBase API (runtime)

### No Blockers

Todas as dependências já implementadas e em produção. Feature pode ser desenvolvida imediatamente.

---

## Timeline & Milestones

### Phase 1: MVP (Priority P0)
**Effort**: M (2-3 dias de desenvolvimento)
**Target**: Imediato (próximo fechamento mensal)

**Deliverables**:
- US1: Filtro por período ✓
- US2: Tabela de seleção com checkboxes ✓
- US3: Preview com navegação ✓
- US4: Envio bulk com progresso ✓
- US5: Reenvio sem confirmação ✓

**Success Criteria**:
- Envio de 100 avisos em < 5 minutos end-to-end
- Taxa de erro < 1%
- Feedback positivo do Gerente Operacional

### Future Enhancements (Out of Current Scope)

- Filtros adicionais: por cliente, por contrato, por tipo de serviço
- Exportar lista de envios (CSV, Excel)
- Agendamento de envio para data futura
- Bulk para outros tipos de email (entrega de laudo)
- Histórico de batches enviados

---

## Open Questions

**Q1**: Há limite de rate limiting do Gmail para envios bulk?
- **Impact**: Medium - pode afetar performance
- **Resolution Path**: Validar com configuração atual do SMTP, documentar limites
- **Owner**: Tech Lead

**Q2**: Desempenho da query de tasks com expand multi-nível é aceitável?
- **Impact**: Medium - afeta usabilidade
- **Resolution Path**: Testar query com volume real de dados, otimizar se necessário
- **Owner**: Backend Developer

---

## Appendix

### Technical Context

**Collections Structure**:
```
tasks
├── role: 'agendamento' (identifica tasks de aviso de coleta)
├── dueDate: ISO datetime (data da coleta)
├── serviceExecutionItemId: relation → service_execution_items
└── type: 'execution'

service_execution_items
├── serviceExecutionId: relation → service_executions
├── contractServiceId: relation → contract_services
├── expectedQuantity: number
└── expand: contractServiceId.serviceId
    └── segment: 'laboratorial' (identifica serviços de análise)

email_sends
├── taskId: relation → tasks (vincula email à task)
├── status: 'sent' | 'failed' | 'delivered'
├── to: email destinatário
├── senderId: user que disparou
└── created: timestamp do envio
```

### UI Wireframe (Textual)

```
┌─ Página: Envio Bulk de Avisos de Coleta ─────────────────┐
│                                                            │
│ [Filtro]                                                   │
│ Período: [__/__/____] até [__/__/____]  [Carregar Lista]  │
│                                                            │
│ ┌─ Tabela de Coletas ────────────────────────────────────┐│
│ │ [✓] | Cliente         | Serviço    | Data  | Qtd | Amostras│
│ │ [✓] | Empresa ABC     | Água       | 05/02 | 3   | Água, Solo │
│ │ [ ] | Empresa XYZ     | Ar         | 07/02 | 1   | Ar (Enviado)│
│ │ [✓] | Cliente Teste   | Completo   | 10/02 | 5   | Água, Solo, Ar│
│ └────────────────────────────────────────────────────────┘│
│                                                            │
│ 15 de 20 selecionados  [Preview] [Enviar Selecionados]    │
└────────────────────────────────────────────────────────────┘

┌─ Modal: Preview de Emails ────────────────────────────────┐
│ Email 1 de 15                                        [x]   │
│                                                            │
│ Para: contato@empresaabc.com                               │
│ Assunto: Aviso de Coleta - 05/02/2026                     │
│                                                            │
│ ┌─ Preview Renderizado ────────────────────────────────┐  │
│ │ [HTML renderizado do template aviso-coleta]           │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
│ [← Anterior]                [Próximo →]  [Enviar Todos]   │
└────────────────────────────────────────────────────────────┘
```

### Constitution Alignment

**Principles Validation**:
- ✅ **I. Automação > Customização Manual**: Elimina processo manual repetitivo
- ✅ **II. Agilidade sem Sacrificar Qualidade**: Filtros ágeis + preview + rastreabilidade total
- ✅ **III. Eficiência Interna Primeiro**: Ferramenta exclusiva para equipe, ROI claro
- ✅ **IV. Plataforma Alinhada ao Contexto**: Integrada ao fluxo de fechamento de agenda

**Personas Served**:
- Gerente Operacional (primário): Controle total + visibilidade
- Agendamento (primário): Execução rápida do processo mensal
- Admin (secundário): Suporte e envios de emergência

**Anti-Patterns Avoided**:
- ✅ Não é solução patch: Integra com sistema de emails robusto
- ✅ Não é flexibilidade prematura: Foco em caso de uso validado
- ✅ Não é gambiarra: Reutiliza 80% de código existente

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-24  
**Next Review**: After refinement with stakeholders
