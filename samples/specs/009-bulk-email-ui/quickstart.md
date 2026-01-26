# Quickstart: Interface de Envio Bulk de Avisos de Coleta

**Feature**: 009-bulk-email-ui  
**Purpose**: Development guide for implementing the bulk email sending interface  
**Last Updated**: 2026-01-25

## Overview

This feature creates a complete UI for bulk email sending of collection notices. It reuses existing composables and APIs from Specs 004, 005, and 007 - no backend changes required.

## Prerequisites

### Required Dependencies (Already Installed)
- ✅ Nuxt 4.x with SPA mode
- ✅ @nuxt/ui v4
- ✅ @tanstack/vue-table v8+
- ✅ date-fns v3+
- ✅ Pinia v3

### Required Features (Must Be Implemented First)
- ✅ **Spec 007**: `useBulkCollectionTasks` composable MUST exist
- ✅ **Spec 004**: Email APIs (`/api/tasks/:taskId/email-send`) MUST be functional
- ✅ **Spec 005**: Email modal pattern exists (will be adapted)

### Verify Dependencies

```bash
# Check if Spec 007 composable exists
ls -la frontend/app/composables/useBulkCollectionTasks.ts

# Check if email APIs exist
ls -la frontend/server/api/tasks/\[taskId\]/email-send.post.ts
ls -la frontend/server/api/tasks/\[taskId\]/email-preview.get.ts

# Run PocketBase (backend)
cd backend && ./pocketbase serve --dev

# Run Nuxt dev server (frontend)
cd frontend && npm run dev
```

## Development Workflow

### Phase 1: Page Structure & Routing

**Goal**: Create basic page with routing and layout

**File**: `frontend/app/pages/emails/bulk-avisos-coleta.vue`

```vue
<script setup lang="ts">
import { DateRangePicker } from '~/lib/components'

// Page Coordinator Pattern - manage UI state here
const filters = reactive({
  dateRange: null as [Date, Date] | null,
})

const selectedTaskIds = ref<Set<string>>(new Set())

definePageMeta({
  layout: 'default',
  middleware: ['auth'],
})
</script>

<template>
  <div class="h-full flex flex-col max-w-7xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-6">Envio Bulk de Avisos de Coleta</h1>
    
    <!-- Filter Section -->
    <div class="mb-4">
      <p>Date range filter goes here</p>
    </div>
    
    <!-- Table Section -->
    <div class="flex-1">
      <p>Table goes here</p>
    </div>
    
    <!-- Actions Footer -->
    <div class="mt-4 flex justify-between items-center">
      <p>Counter: X de Y selecionados</p>
      <div class="flex gap-2">
        <UButton>Preview</UButton>
        <UButton>Enviar Selecionados</UButton>
      </div>
    </div>
  </div>
</template>
```

**Test**: Navigate to `/emails/bulk-avisos-coleta` - page should render

---

### Phase 2: Date Filter Integration

**Goal**: Add date range picker using project's custom DateRangePicker component

**Update**: `bulk-avisos-coleta.vue` (add to template)

```vue
<script setup lang="ts">
import { DateRangePicker } from '~/lib/components'

const filters = reactive({
  dateRange: null as [Date, Date] | null,
})

const handleLoadTasks = async () => {
  // Next phase: integrate composable
  console.log('Loading tasks...', filters.dateRange)
}
</script>

<template>
  <div class="mb-4 flex gap-4 items-end">
    <!-- Use project's custom DateRangePicker component -->
    <DateRangePicker
      v-model="filters.dateRange"
      placeholder="Selecione o período"
      class="w-80"
    />
    
    <UButton 
      :disabled="!filters.dateRange"
      @click="handleLoadTasks"
    >
      Carregar Lista
    </UButton>
  </div>
</template>
```

**Test**: Select date range, button enables/disables correctly

---

### Phase 3: Integrate useBulkCollectionTasks Composable

**Goal**: Load tasks data from Spec 007 composable

**Update**: `bulk-avisos-coleta.vue`

```vue
<script setup lang="ts">
import { useBulkCollectionTasks } from '#imports'
import { DateRangePicker } from '~/lib/components'
import { format } from 'date-fns'

const filters = reactive({
  dateRange: null as [Date, Date] | null,
})

// Import composable from Spec 007
const { tasks, loading, error, loadTasks } = useBulkCollectionTasks()

const handleLoadTasks = async () => {
  if (!filters.dateRange) return
  
  // Format dates to YYYY-MM-DD
  const [startDate, endDate] = filters.dateRange
  const startStr = format(startDate, 'yyyy-MM-dd')
  const endStr = format(endDate, 'yyyy-MM-dd')
  
  await loadTasks(startStr, endStr)
  
  // Auto-select non-sent tasks
  selectedTaskIds.value = new Set(
    tasks.value
      .filter(t => !t.emailStatus.sent)
      .map(t => t.id)
  )
}
</script>

<template>
  <div class="flex-1">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else-if="tasks.length === 0">Nenhuma coleta encontrada</div>
    <div v-else>
      <p>{{ tasks.length }} tasks loaded</p>
      <!-- Table in next phase -->
    </div>
  </div>
</template>
```

**Test**: Load tasks, verify console shows correct data structure

---

### Phase 4: TanStack Vue Table with Selection

**Goal**: Create table component with checkbox selection

**File**: `frontend/app/components/emails/BulkEmailTable.vue`

```vue
<script setup lang="ts">
import {
  useVueTable,
  getCoreRowModel,
  FlexRender,
} from '@tanstack/vue-table'
import type { ColumnDef } from '@tanstack/vue-table'
import type { BulkCollectionTask } from '#types/bulk-collection-task'

interface Props {
  tasks: BulkCollectionTask[]
  selectedIds: Set<string>
}

interface Emits {
  (e: 'update:selectedIds', ids: Set<string>): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const columns: ColumnDef<BulkCollectionTask>[] = [
  {
    id: 'select',
    header: ({ table }) => (
      // Select all checkbox
      h('input', {
        type: 'checkbox',
        checked: table.getIsAllRowsSelected(),
        onChange: table.getToggleAllRowsSelectedHandler(),
      })
    ),
    cell: ({ row }) => (
      h('input', {
        type: 'checkbox',
        checked: row.getIsSelected(),
        onChange: row.getToggleSelectedHandler(),
      })
    ),
  },
  {
    accessorKey: 'clientName',
    header: 'Cliente',
  },
  {
    accessorKey: 'serviceName',
    header: 'Serviço',
  },
  {
    accessorKey: 'collectionDate',
    header: 'Data',
    cell: ({ getValue }) => format(new Date(getValue()), 'dd/MM/yyyy'),
  },
  {
    accessorKey: 'samplesCount',
    header: 'Amostras',
  },
  {
    accessorKey: 'laboratorySamples',
    header: 'Serviços Laboratoriais',
    cell: ({ getValue }) => (getValue() as string[]).join(', '),
  },
  {
    id: 'emailStatus',
    header: 'Status',
    cell: ({ row }) => {
      const status = row.original.emailStatus
      if (status.sent) {
        return h('span', { class: 'badge-sent' }, 
          `Enviado em ${format(new Date(status.lastSentAt!), 'dd/MM HH:mm')}`
        )
      }
      return h('span', 'Pendente')
    },
  },
]

const table = useVueTable({
  get data() { return props.tasks },
  columns,
  getCoreRowModel: getCoreRowModel(),
  enableRowSelection: true,
  onRowSelectionChange: (updater) => {
    // Sync selection with parent
    const newSelection = typeof updater === 'function' 
      ? updater(rowSelection.value) 
      : updater
    
    const newIds = new Set<string>()
    Object.entries(newSelection).forEach(([index, selected]) => {
      if (selected) {
        newIds.add(props.tasks[parseInt(index)].id)
      }
    })
    emit('update:selectedIds', newIds)
  },
})

// Initialize row selection from props
const rowSelection = computed(() => {
  const selection: Record<number, boolean> = {}
  props.tasks.forEach((task, index) => {
    if (props.selectedIds.has(task.id)) {
      selection[index] = true
    }
  })
  return selection
})
</script>

<template>
  <div class="overflow-auto">
    <table class="w-full">
      <thead>
        <tr v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
          <th v-for="header in headerGroup.headers" :key="header.id">
            <FlexRender
              :render="header.column.columnDef.header"
              :props="header.getContext()"
            />
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in table.getRowModel().rows" :key="row.id">
          <td v-for="cell in row.getVisibleCells()" :key="cell.id">
            <FlexRender
              :render="cell.column.columnDef.cell"
              :props="cell.getContext()"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
```

**Use in page**:
```vue
<BulkEmailTable 
  :tasks="tasks"
  :selected-ids="selectedTaskIds"
  @update:selected-ids="selectedTaskIds = $event"
/>
```

**Test**: Select/unselect rows, verify selectedTaskIds updates

---

### Phase 5: Preview Modal with Navigation

**Goal**: Adapt Spec 005 modal for bulk navigation

**File**: `frontend/app/components/emails/EmailPreviewModal.vue`

```vue
<script setup lang="ts">
import type { BulkCollectionTask } from '#types/bulk-collection-task'

interface Props {
  isOpen: boolean
  tasks: BulkCollectionTask[]
  currentIndex: number
}

interface Emits {
  (e: 'close'): void
  (e: 'next'): void
  (e: 'previous'): void
  (e: 'sendAll'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Fetch preview for current task
const currentTask = computed(() => props.tasks[props.currentIndex])

const { data: preview, pending } = useFetch(
  () => `/api/tasks/${currentTask.value?.id}/email-preview`,
  { 
    immediate: false,
    watch: [currentTask],
  }
)

// Keyboard navigation
onKeyStroke('ArrowLeft', () => {
  if (props.currentIndex > 0) emit('previous')
})

onKeyStroke('ArrowRight', () => {
  if (props.currentIndex < props.tasks.length - 1) emit('next')
})

onKeyStroke('Escape', () => emit('close'))
</script>

<template>
  <UModal :model-value="isOpen" @close="emit('close')" size="xl" fullscreen>
    <div class="p-6">
      <!-- Header with navigation -->
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold">
          Email {{ currentIndex + 1 }} de {{ tasks.length }}
        </h2>
        <div class="flex gap-2">
          <UButton 
            icon="i-heroicons-arrow-left"
            :disabled="currentIndex === 0"
            @click="emit('previous')"
          >
            Anterior
          </UButton>
          <UButton 
            icon="i-heroicons-arrow-right"
            :disabled="currentIndex === tasks.length - 1"
            @click="emit('next')"
          >
            Próximo
          </UButton>
        </div>
      </div>
      
      <!-- Email Preview -->
      <div v-if="pending" class="text-center py-8">
        Carregando preview...
      </div>
      <div v-else-if="preview" class="border rounded p-4">
        <!-- Render preview HTML -->
        <div v-html="preview.html" />
      </div>
      
      <!-- Actions -->
      <div class="flex justify-end gap-2 mt-6">
        <UButton variant="outline" @click="emit('close')">
          Fechar
        </UButton>
        <UButton color="primary" @click="emit('sendAll')">
          Enviar Todos
        </UButton>
      </div>
    </div>
  </UModal>
</template>
```

**Test**: Open modal, navigate with buttons and arrow keys

---

### Phase 6: Bulk Send with Progress

**Goal**: Sequential sending with real-time progress tracking

**Update**: `bulk-avisos-coleta.vue`

```vue
<script setup lang="ts">
const bulkProgress = reactive({
  inProgress: false,
  current: 0,
  total: 0,
  results: [] as Array<{taskId: string, status: 'success'|'error', error?: string}>
})

const handleBulkSend = async () => {
  const selected = tasks.value.filter(t => selectedTaskIds.value.has(t.id))
  
  bulkProgress.inProgress = true
  bulkProgress.current = 0
  bulkProgress.total = selected.length
  bulkProgress.results = []
  
  // Close modal
  previewModal.isOpen = false
  
  // Send sequentially
  for (const task of selected) {
    try {
      await $fetch(`/api/tasks/${task.id}/email-send`, { method: 'POST' })
      
      bulkProgress.results.push({
        taskId: task.id,
        status: 'success',
      })
      
      // Update task status in UI
      const taskIndex = tasks.value.findIndex(t => t.id === task.id)
      if (taskIndex !== -1) {
        tasks.value[taskIndex].emailStatus.sent = true
        tasks.value[taskIndex].emailStatus.lastSentAt = new Date().toISOString()
      }
      
      // Unselect sent task
      selectedTaskIds.value.delete(task.id)
      
    } catch (error: any) {
      bulkProgress.results.push({
        taskId: task.id,
        status: 'error',
        error: error.message || 'Erro desconhecido',
      })
    }
    
    bulkProgress.current++
  }
  
  bulkProgress.inProgress = false
  
  // Show summary toast
  const successCount = bulkProgress.results.filter(r => r.status === 'success').length
  const errorCount = bulkProgress.results.filter(r => r.status === 'error').length
  
  if (errorCount === 0) {
    toast.add({ title: `${successCount} enviados com sucesso`, color: 'green' })
  } else {
    toast.add({ 
      title: `${successCount} enviados, ${errorCount} erros`,
      color: 'orange',
    })
  }
}
</script>

<template>
  <!-- Progress Overlay -->
  <div v-if="bulkProgress.inProgress" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
    <UCard>
      <div class="p-6 min-w-[400px]">
        <h3 class="text-lg font-semibold mb-4">
          Enviando {{ bulkProgress.current }} de {{ bulkProgress.total }}...
        </h3>
        
        <!-- Progress Bar -->
        <div class="w-full bg-gray-200 rounded-full h-2 mb-4">
          <div 
            class="bg-primary h-2 rounded-full transition-all"
            :style="{ width: `${(bulkProgress.current / bulkProgress.total) * 100}%` }"
          />
        </div>
        
        <p class="text-sm text-gray-600">
          {{ Math.round((bulkProgress.current / bulkProgress.total) * 100) }}% completo
        </p>
      </div>
    </UCard>
  </div>
</template>
```

**Test**: Send bulk, verify progress bar updates and status badges update

---

## Testing Guide

### Unit Tests

```typescript
// tests/components/BulkEmailTable.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BulkEmailTable from '~/components/emails/BulkEmailTable.vue'

describe('BulkEmailTable', () => {
  it('renders tasks correctly', () => {
    const tasks = [
      { id: '1', clientName: 'Cliente A', serviceName: 'Serviço X', /* ... */ }
    ]
    const wrapper = mount(BulkEmailTable, { props: { tasks, selectedIds: new Set() } })
    expect(wrapper.text()).toContain('Cliente A')
  })
  
  it('emits selection changes', async () => {
    // Test checkbox selection logic
  })
})
```

### Integration Tests

```typescript
// tests/pages/bulk-avisos-coleta.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BulkAvisosColeta from '~/pages/emails/bulk-avisos-coleta.vue'

describe('Bulk Avisos Coleta Page', () => {
  it('loads tasks on date selection', async () => {
    // Test filter → load workflow
  })
  
  it('opens preview modal with selected tasks', async () => {
    // Test selection → preview workflow
  })
})
```

### E2E Tests

```typescript
// tests/e2e/bulk-email-flow.spec.ts
import { test, expect } from '@playwright/test'

test('complete bulk email flow', async ({ page }) => {
  await page.goto('/emails/bulk-avisos-coleta')
  
  // Select date range
  await page.fill('[name="startDate"]', '2026-02-01')
  await page.fill('[name="endDate"]', '2026-02-28')
  await page.click('text=Carregar Lista')
  
  // Wait for tasks to load
  await expect(page.locator('table tbody tr')).toHaveCount(10)
  
  // Select first 5 tasks
  for (let i = 0; i < 5; i++) {
    await page.check(`table tbody tr:nth-child(${i + 1}) input[type="checkbox"]`)
  }
  
  // Open preview
  await page.click('text=Preview')
  await expect(page.locator('text=Email 1 de 5')).toBeVisible()
  
  // Navigate
  await page.click('text=Próximo')
  await expect(page.locator('text=Email 2 de 5')).toBeVisible()
  
  // Send all
  await page.click('text=Enviar Todos')
  await expect(page.locator('text=5 enviados com sucesso')).toBeVisible()
})
```

## Common Issues & Solutions

### Issue: Composable not found
**Solution**: Verify Spec 007 is implemented, check import path

### Issue: Table selection not updating
**Solution**: Verify row selection sync logic in table component

### Issue: Preview modal not loading
**Solution**: Check API endpoint returns correct data, verify task ID is valid

### Issue: Bulk send stuck
**Solution**: Check network tab, verify API responses, add error handling

## Performance Optimization

### Lazy Loading (if > 200 tasks)
```typescript
import { useVirtualizer } from '@tanstack/vue-virtual'

// Add to table component for virtualization
```

### Debounce Date Filters
```typescript
const debouncedLoadTasks = useDebounceFn(handleLoadTasks, 500)
```

### Batch Progress Updates
```typescript
// Update UI every 5 items instead of every 1
if (bulkProgress.current % 5 === 0) {
  // Force re-render
}
```

## Next Steps

After completing this feature:

1. ✅ Test with real data (50+ tasks)
2. ✅ Validate permissions (role checks)
3. ✅ Performance test with 200 tasks
4. ✅ Deploy to staging
5. ✅ User acceptance testing
6. ✅ Production deployment

## Resources

- [Spec 007 - useBulkCollectionTasks](../007-bulk-collection-tasks-composable/spec.md)
- [Spec 005 - Task Email UI](../005-task-email-ui/spec.md)
- [Spec 004 - Email APIs](../004-task-email-integration/spec.md)
- [TanStack Table Docs](https://tanstack.com/table/v8/docs/framework/vue/guide/introduction)
- [Nuxt UI Components](https://ui.nuxt.com/)
