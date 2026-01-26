# Research: Envio de Emails em Bulk Manual

**Created**: 2026-01-24 | **Status**: ✅ Complete → PRD Drafted

## Initial Idea

Criar uma tela para que usuários possam enviar emails manuais em bulk (lote). A tela deve permitir filtrar por service_execution_items e data antes de disparar os envios.

## Discovery Questions & Answers

### Problem Space

**Q: What problem are we trying to solve?**
A: Necessidade de enviar avisos de coleta em massa quando a agenda do mês é fechada, de forma controlada e rastreável.

**Q: Who experiences this problem?**
A: Gerente Operacional (persona primária) que fecha a agenda mensal e precisa notificar clientes sobre coletas programadas.

**Q: How do they solve it today?**
A: [NEEDS_DETAIL: É feito manualmente um por um? Não é feito? Usa outro sistema?]

**Q: What's the cost of not solving this?**
A: Tempo gasto em envios manuais repetitivos, possíveis esquecimentos de notificar clientes, falta de rastreabilidade de quais avisos foram enviados.

### User Understanding

**Q: Who is the primary persona?**
A: Gerente Operacional - responsável por fechar agenda mensal e coordenar avisos aos clientes

**Q: What are their main goals?**
A: Enviar avisos de coleta em massa de forma eficiente, com controle sobre quem recebe e quando, mantendo rastreabilidade

**Q: What are their pain points?**
A: Processo manual repetitivo, risco de esquecer clientes, falta de visibilidade de quais avisos foram enviados

### Solution Space

**Q: What's the proposed solution?**
A: Interface de envio bulk de avisos de coleta com:
- Filtros por período (dueDate das tasks)
- Seleção manual de quais items recebem email
- Preview em modal com navegação (anterior/próximo) para revisão
- Envio em lote após confirmação

**Q: What are the key features?**
A:
1. **Filtro por período**: Range de datas baseado em dueDate das tasks de aviso de coleta
2. **Tabela de seleção**: Após filtrar, mostra lista com checkboxes contendo:
   - Cliente
   - Serviço
   - Data da coleta
   - Quantidade de amostras
   - Quais amostras (items laboratoriais do mesmo service_execution)
3. **Estado inicial**: Todos marcados, exceto items que já tiveram email enviado (vem desmarcados mas podem ser remarcados)
4. **Reenvio sem confirmação**: Items já enviados podem ser reenviados sem diálogo de confirmação
5. **Modal de preview**: Reutiliza modal existente de preview de 1 envio, adicionando:
   - Navegação anterior/próximo
   - Navega apenas pelos items **selecionados** (checkboxes marcados)
6. **Envio bulk**: Botão para enviar todos os items selecionados
7. **Rastreamento**: Via email_sends/email_events existentes

**Q: What's explicitly out of scope?**
A:
- Envio automático/agendado (já existe no sistema via US3 do PRD original)
- Templates customizados (usa template 'aviso-coleta' existente)
- Edição de conteúdo do email (template é fixo)
- Confirmação de reenvio (usuário pode remarcar e reenviar diretamente)
- Outros tipos de email além de aviso de coleta (foco apenas em avisos)

### Success Criteria

**Q: How will we measure success?**
A:
- **Eficiência**: Tempo para enviar avisos do mês inteiro (deve ser < 5 minutos vs. horas manualmente)
- **Precisão**: Taxa de erros em envios bulk (meta: < 1%)
- **Uso**: Frequência de uso (esperado: 1x por mês, ~100 avisos)
- **Rastreabilidade**: 100% dos envios registrados em email_sends

**Q: What's the target for each metric?**
A:
- Envio de 100 emails: < 2 minutos (2 segundos por email em média)
- Taxa de erro: < 1% (máximo 1 falha em 100 envios)
- Tempo de preparação (filtro + seleção + preview): < 3 minutos
- Total do processo: < 5 minutos do início ao fim

### Constraints

**Q: Are there any compliance requirements?**
A: Não há compliance específico, mas deve seguir mesmos padrões de rastreabilidade do sistema de emails existente (email_sends, email_events)

**Q: Are there technical constraints?**
A:
- Usar infraestrutura existente: useEmailService composable, template 'aviso-coleta'
- Collections PocketBase: tasks, service_execution_items, service_executions, email_sends, email_events
- Reutilizar modal de preview existente (adicionar navegação)
- Identificar serviços laboratoriais via `service.segment === 'laboratorial'`
- Buscar amostras: filtrar service_execution_items pelo mesmo serviceExecutionId onde segment='laboratorial'
- Tasks de aviso de coleta tem `role === 'agendamento'` e são do tipo execution

**Q: Are there timeline constraints?**
A: 
- **Prioridade**: P0 (bloqueador/crítico)
- **Prazo**: Imediato - necessário para próximo fechamento mensal de agenda
- **Dependências**: Nenhuma - todas as dependências já implementadas (sistema de emails, templates, PocketBase collections)

## Constitution Alignment

### Checked Against Principles

- [x] **I. Automação > Customização Manual**: ✅ ALINHA PERFEITAMENTE
  - Substitui processo manual repetitivo de envio um por um
  - Mantém controle sem sacrificar agilidade
  - Foco em eficiência operacional

- [x] **II. Agilidade sem Sacrificar Qualidade**: ✅ ALINHA
  - Filtros ágeis (período + seleção)
  - Preview para validação antes de enviar (qualidade)
  - Rastreabilidade total via email_sends/email_events

- [x] **III. Eficiência Interna Primeiro**: ✅ ALINHA
  - Ferramenta exclusiva para equipe interna (Agendamento, Gerente, Admin)
  - Otimiza processo crítico mensal (fechamento de agenda)
  - ROI claro: horas economizadas todo mês

- [x] **IV. Plataforma Alinhada ao Contexto**: ✅ ALINHA
  - Integrada ao fluxo de fechamento de agenda mensal
  - Usa dados já cadastrados (tasks, service_executions, contacts)
  - Não requer cadastros extras ou paralelos

### Serves Personas

- **Gerente Operacional** (✅ Persona Primária): 
  - Ganha: Visibilidade e controle total sobre avisos enviados
  - Economiza: Horas de trabalho manual todo mês
  - Reduz: Risco de esquecer clientes

- **Agendamento** (✅ Persona Secundária):
  - Pode disparar avisos quando agenda é fechada
  - Interface simples e rápida

- **Admin** (✅ Suporte):
  - Pode fazer envios de emergência ou correções

### Does NOT Violate Anti-Patterns

- ✅ **Não é "solução patch"**: Integra com sistema de emails existente, reutiliza templates e composables
- ✅ **Não é "flexibilidade prematura"**: Filtros específicos para caso de uso validado (aviso de coleta mensal)
- ✅ **Não é "gambiarra por pressa"**: Reutiliza infraestrutura robusta já implementada
- ✅ **Não adiciona complexidade desnecessária**: UX simples, processo linear (filtrar > selecionar > preview > enviar)

### Potential Conflicts

Nenhum conflito identificado. Feature alinha perfeitamente com princípios do produto.

## Key Insights

1. **Reutilização Máxima**: Sistema de emails robusto já existe - apenas adicionar interface de bulk
2. **Caso de Uso Validado**: Processo mensal recorrente com volume previsível (~100 avisos/mês)
3. **Estrutura de Dados Clara**: 
   - Tasks de agendamento (`role='agendamento'`) são os triggers
   - Serviços laboratoriais identificados via `segment='laboratorial'`
   - Relacionamento via `serviceExecutionId` para buscar amostras
4. **UX Progressiva**: Filtro > Tabela com seleção > Preview > Envio com progresso
5. **Componentes Reutilizáveis**: Modal de preview já existe, apenas adicionar navegação
6. **Permissões Claras**: Agendamento, Gerente, Admin
7. **Sem Bloqueios Técnicos**: Todas as peças necessárias já implementadas

## Next Steps

- [x] Definir caso de uso principal: Aviso de coleta manual
- [x] Especificar comportamento dos filtros: Período (dueDate) + checkboxes
- [x] Definir UX: Tabela > Preview com navegação > Envio com progresso
- [x] Validar persona principal: Gerente + Agendamento + Admin
- [x] Resolver estrutura de dados: service_execution_items, segment='laboratorial'
- [x] Validar contra product-constitution.md: ✅ 100% alinhado
- [ ] Proceder para @prd-draft

---

**Validation Status**: ✅ Discovery completa - Pronto para @prd-draft

**Sumário Executivo**:
- **Feature**: Interface de envio bulk de avisos de coleta com filtros e preview
- **Prioridade**: P0 (imediato)
- **Esforço Estimado**: M (2-3 dias) - reutiliza 80% de código existente
- **Personas**: Agendamento, Gerente Operacional, Admin
- **Alinhamento**: 100% alinhado com todos os princípios da constituição
- **Bloqueadores**: Nenhum - todas dependências já implementadas
