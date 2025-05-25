<template>
  <div class="bg-white rounded-xl shadow border overflow-x-auto flex-1">
    <table class="min-w-full text-left">
      <thead class="bg-gray-50 text-gray-500 text-sm">
        <tr>
          <th class="px-6 py-3 font-medium">Name</th>
          <th class="px-6 py-3 font-medium">Conditions</th>
          <th class="px-6 py-3 font-medium">Type</th>
          <th class="px-6 py-3 font-medium">Actions</th>
          <th class="px-6 py-3 font-medium">Automated</th>
          <th class="px-6 py-3 font-medium">Threads</th>
          <th class="px-6 py-3 font-medium"></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td colspan="7" class="text-center text-gray-400 py-12">No rules yet.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
// 未来可扩展为动态加载规则数据
</script>

<style scoped>
/* 保持整体风格与其他页面一致 */
</style> 