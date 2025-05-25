<template>
  <div class="w-full h-full flex flex-col">
    <!-- 顶部Tab导航栏 -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex gap-2">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          :class="[
            'px-4 py-2 rounded-t-lg font-semibold shadow-none',
            currentTab === tab.key
              ? 'bg-white border-b-2 border-green-500 text-gray-900'
              : 'bg-gray-100 text-gray-500'
          ]"
          @click="currentTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>
      <div class="flex gap-2" v-if="currentTab === 'rules'">
        <button class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md border border-gray-200 font-medium">Bulk Run on Inbox</button>
        <button class="px-4 py-2 bg-gray-900 text-white rounded-md font-semibold shadow">Create Rule</button>
      </div>
    </div>
    <!-- Tab内容区 -->
    <component :is="tabComponent" class="flex-1 min-h-0" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import PromptTab from './PromptTab.vue'
import RulesTab from './RulesTab.vue'
const tabs = [
  { key: 'prompt', label: 'Prompt', component: PromptTab },
  { key: 'rules', label: 'Rules', component: RulesTab },
  { key: 'pending', label: 'Pending', component: null },
  { key: 'history', label: 'History', component: null },
  { key: 'test', label: 'Test', component: null },
  { key: 'groups', label: 'Groups', component: null },
]
const currentTab = ref('prompt')
const tabComponent = computed(() => {
  const found = tabs.find(t => t.key === currentTab.value)
  return found?.component || {
    template: `<div class='flex-1 flex items-center justify-center text-gray-400 text-xl'>${found?.label || ''} coming soon...</div>`
  }
})
</script>

<style scoped>
/* 保持整体风格与其他页面一致 */
</style> 