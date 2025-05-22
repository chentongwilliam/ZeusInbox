<template>
  <div class="w-full h-full flex flex-col">
    <!-- 顶部标签栏 -->
    <div class="flex items-center gap-2 mb-6">
      <button class="px-4 py-2 rounded-t-lg bg-white border-b-2 border-green-500 font-semibold text-gray-900 shadow-none">To Reply</button>
      <button class="px-4 py-2 rounded-t-lg bg-gray-100 text-gray-500 shadow-none">Waiting</button>
      <button class="px-4 py-2 rounded-t-lg bg-gray-100 text-gray-500 shadow-none">Done</button>
    </div>
    <!-- 邮件列表 -->
    <div class="bg-white rounded-xl shadow border overflow-x-auto flex-1 flex flex-col items-center justify-center">
      <div class="text-gray-400 text-lg py-12">{{$t('mail.noMail')}}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 目前无邮件数据，后续可扩展为动态加载（MailPage）
</script>

<style scoped>
/* 可根据需要自定义样式 */
</style> 