<template>
  <div class="w-full h-full flex flex-col bg-white rounded-xl shadow border p-8 relative">
    <!-- 顶部操作栏 -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-2">
        <button class="p-2 rounded hover:bg-gray-100" @click="$emit('close')">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
      </div>
      <div class="flex items-center gap-6">
        <button class="text-blue-700 hover:underline bg-transparent" @click="onReply">{{ $t('mail.reply') }}</button>
        <button class="text-blue-700 hover:underline bg-transparent" @click="onReplyAll">{{ $t('mail.replyAll') }}</button>
        <button class="text-blue-700 hover:underline bg-transparent" @click="onForward">{{ $t('mail.forward') }}</button>
        <button class="text-blue-700 hover:underline bg-transparent" @click="onDelete">{{ $t('mail.delete') }}</button>
        <button class="p-1 rounded hover:bg-gray-100">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16" />
          </svg>
        </button>
      </div>
    </div>
    <!-- 邮件内容 -->
    <div class="mb-6">
      <div class="text-2xl font-bold mb-2">{{ mail.subject }}</div>
      <div class="flex items-center gap-4 text-gray-600 text-sm mb-1">
        <span>{{ mail.from }}</span>
        <span>{{ formatMailTime(mail.date) }}</span>
      </div>
    </div>
    <div class="flex-1 overflow-y-auto bg-gray-50 rounded p-6 text-gray-800">
      <div v-html="mail.body || mail.snippet"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import dayjs from 'dayjs'
const props = defineProps<{ mail: any }>()
const { t } = useI18n()

const formatMailTime = (dateStr: string) => {
  const date = dayjs(dateStr)
  if (date.isSame(dayjs(), 'day')) {
    return date.format('HH:mm')
  }
  return date.format('YYYY-MM-DD HH:mm')
}

const onReply = () => {}
const onReplyAll = () => {}
const onForward = () => {}
const onDelete = () => {}
</script>

<style scoped>
.w-full {
  min-width: 500px;
}
</style> 