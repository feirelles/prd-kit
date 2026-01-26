# Feature 009: Interface de Envio Bulk de Avisos de Coleta

**Status**: ✅ Planejamento Completo | **Branch**: `009-bulk-email-ui` | **Criado**: 2026-01-25

## 📋 Visão Geral

Interface completa para envio em massa de avisos de coleta que permite filtrar por período, selecionar tasks, visualizar preview navegável dos emails, e executar envio bulk com feedback de progresso em tempo real.

**Impacto de Negócio**: Reduz tempo de operação mensal de 2-3h para < 5 minutos (redução de 90%)

## 📁 Documentação

| Arquivo | Descrição | Status | Linhas |
|---------|-----------|--------|--------|
| [spec.md](./spec.md) | Especificação funcional completa | ✅ Completo | 523 |
| [plan.md](./plan.md) | Plano de implementação técnica | ✅ Completo | 370 |
| [quickstart.md](./quickstart.md) | Guia passo-a-passo para desenvolvimento | ✅ Completo | 685 |
| [checklists/requirements.md](./checklists/requirements.md) | Validação de qualidade | ✅ Aprovado | - |

**Total**: 1.578 linhas de documentação

## 🎯 User Stories (5 total)

### MVP (P0 - Bloqueador)
1. ✅ **US1** - Filtrar Tasks por Período
2. ✅ **US2** - Selecionar Tasks para Envio
3. ✅ **US3** - Preview Navegável de Emails
4. ✅ **US4** - Envio Bulk com Progresso em Tempo Real

### Enhancement (P1 - Alta)
5. ✅ **US5** - Reenviar Items Previamente Enviados

## 🔗 Dependências

### Specs Relacionadas (Todas Implementadas)
- ✅ **007-bulk-collection-tasks-composable** - Composable de dados (dependência direta)
- ✅ **005-task-email-ui** - Padrões de modal de preview (adaptação)
- ✅ **004-task-email-integration** - APIs de email (uso via composable)
- ✅ **002-email-core-service** - Serviço SMTP (dependência indireta)

### Tecnologias
- Nuxt 4.x (SPA mode)
- Vue 3.5+ / TypeScript 5.8+
- @nuxt/ui v4
- @tanstack/vue-table v8+
- date-fns v3+
- PocketBase 0.31.x

## 📊 Arquitetura Técnica

### Componentes Novos
```
app/pages/emails/bulk-avisos-coleta.vue        # Page Coordinator (~250-300 LOC)
app/components/emails/BulkEmailTable.vue       # TanStack Table (~150-200 LOC)
app/components/emails/EmailPreviewModal.vue    # Modal adaptado (~100-150 LOC)
app/components/emails/BulkSendProgress.vue     # Progress overlay (~50-80 LOC)
```

**Total Estimado**: 550-730 LOC (dividido em 4 componentes)

### Padrão de Estado
- ✅ **Page Coordinator Pattern** - UI state no componente da página
- ✅ **Sem Store** - Todo estado gerenciado via `ref()` e `reactive()`
- ✅ **Reuso de Composables** - `useBulkCollectionTasks` (Spec 007)

### APIs Utilizadas (Sem Mudanças)
- `GET /api/tasks/bulk-collection-notices` - Carregar tasks (Spec 007)
- `GET /api/tasks/:taskId/email-preview` - Preview individual (Spec 004)
- `POST /api/tasks/:taskId/email-send` - Envio individual (Spec 004)

## ✅ Validação Constitution

| Princípio | Status | Notas |
|-----------|--------|-------|
| Layer Separation | ✅ PASS | Page Coordinator Pattern aplicado |
| Type Safety | ✅ PASS | Reusa tipos do Spec 007 |
| Layout Consistency | ✅ PASS | Nuxt UI + padrões estabelecidos |
| File Organization | ✅ PASS | 4 componentes < 500 LOC cada |
| Reuse Before Reinvention | ✅ PASS | Zero duplicação, reusa 100% |
| Technology Stack | ✅ PASS | Stack aprovado, sem novidades |

**GATE STATUS**: ✅ **PASS** - Sem violações

## 📈 Métricas de Sucesso

| Métrica | Meta | Status |
|---------|------|--------|
| SC-001: Tempo de envio (50 tasks) | < 5 min | ✅ ~3 min estimado |
| SC-002: Processar 100 envios | < 3 min | ✅ Design suporta |
| SC-003: Status atualizado | 100% | ✅ Real-time |
| SC-004: Identificar erros | < 1 min | ✅ Inline na tabela |
| SC-006: Carregar 200 tasks | < 2s | ✅ Pode precisar virtualização |
| SC-007: Sucesso 1ª tentativa | 95% | ✅ UI clara + quickstart |
| SC-008: Redução de tempo | 90% | ✅ 98% (3 min vs 2-3h) |

## 🚀 Próximos Passos

### Para Começar Desenvolvimento
1. ✅ Especificação completa
2. ✅ Plano de implementação pronto
3. ✅ Quickstart guide disponível
4. ⏭️ **Próximo**: Execute `/speckit.tasks` para gerar task breakdown

### Checklist Pré-Implementação
- [ ] Verificar Spec 007 composable existe e está testado
- [ ] Confirmar APIs do Spec 004 estão funcionais
- [ ] Validar collections PocketBase (tasks, email_sends)
- [ ] Revisar quickstart.md para workflow de desenvolvimento
- [ ] Executar `/speckit.tasks` para breakdown detalhado

## ⏱️ Estimativa de Esforço

**Total**: Médio (5-7 dias)

**Breakdown**:
- **Dia 1-2**: Page + filtro + integração composable
- **Dia 2-3**: TanStack table + seleção
- **Dia 3-4**: Preview modal + navegação
- **Dia 4-5**: Bulk send + progresso
- **Dia 5-6**: Reenvio (Phase 2)
- **Dia 6-7**: Testes + edge cases + polish

## 📝 Notas de Implementação

### Fases
1. **Phase 1 - MVP (P0)**: US1, US2, US3, US4 - Fluxo completo de bulk send
2. **Phase 2 - Enhancement (P1)**: US5 - Funcionalidade de reenvio
3. **Phase 3 - Polish**: Edge cases, performance, responsividade

### Riscos & Mitigações
- **Risco**: TanStack Table learning curve → **Mitigação**: Quickstart com exemplos
- **Risco**: Performance 100+ tasks → **Mitigação**: Progress feedback + UI não-bloqueante
- **Risco**: Edge cases navegação → **Mitigação**: Testes de teclado

### Otimizações Opcionais
- Virtualização de tabela (se > 200 tasks)
- Debounce em filtros de data
- Batch updates de progresso (a cada 5 items)

## 📚 Recursos

- [Spec Completa](./spec.md) - Requisitos funcionais detalhados
- [Plano de Implementação](./plan.md) - Design técnico e arquitetura
- [Guia Quickstart](./quickstart.md) - Tutorial passo-a-passo
- [Checklist de Qualidade](./checklists/requirements.md) - Validação completa

## 🎓 Contexto para AI Agents

Esta feature está **100% documentada e validada**:
- Todos requisitos funcionais definidos com cenários Given-When-Then
- Arquitetura técnica detalhada com padrões estabelecidos
- Guia de desenvolvimento passo-a-passo disponível
- Validação de qualidade completa (sem NEEDS CLARIFICATION)
- Constitution check aprovado (sem violações)

**Status**: ✅ **READY FOR IMPLEMENTATION** - Execute `/speckit.tasks` para começar.
