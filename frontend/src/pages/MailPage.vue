<template>
  <div class="w-full h-full flex">
    <!-- 主内容区域 -->
    <div class="flex-1 flex flex-col">
      <!-- 顶部标签栏 -->
      <div class="flex items-center gap-2 mb-6">
        <button class="px-4 py-2 rounded-t-lg bg-white border-b-2 border-green-500 font-semibold text-gray-900 shadow-none">To Reply</button>
        <button class="px-4 py-2 rounded-t-lg bg-gray-100 text-gray-500 shadow-none">Waiting</button>
        <button class="px-4 py-2 rounded-t-lg bg-gray-100 text-gray-500 shadow-none">Done</button>
      </div>
      <!-- 邮件列表 -->
      <div class="bg-white rounded-xl shadow border overflow-x-auto flex-1 flex flex-col">
        <div v-if="loading" class="text-gray-400 text-lg py-12 text-center">Loading...</div>
        <div v-else-if="error" class="text-red-500 text-lg py-12 text-center">{{ error }}</div>
        <div v-else-if="!emails.length" class="text-gray-400 text-lg py-12 text-center">{{ $t('mail.noMail') }}</div>
        <div v-else>
          <div v-for="mail in emails" :key="mail.id" class="flex items-center border-b px-4 py-3 hover:bg-gray-50 transition-all">
            <div class="w-1/5 font-bold truncate">{{ mail.from }}</div>
            <div class="w-2/5 truncate">{{ mail.subject }}</div>
            <div class="w-1/6 text-right text-gray-500">{{ formatMailTime(mail.date) }}</div>
            <div class="flex-1 text-gray-400 text-sm truncate ml-4">{{ mail.snippet }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 可调整宽度的分隔条 -->
    <div 
      class="w-1 cursor-col-resize hover:bg-blue-500 transition-colors duration-200"
      @mousedown="startResize"
    ></div>

    <!-- 聊天侧边栏 -->
    <div 
      class="flex flex-col h-full bg-gray-50 border-l border-gray-200"
      :style="{ width: `${sidebarWidth}px` }"
    >
      <!-- 聊天历史记录 -->
      <div class="flex-1 overflow-y-auto p-4">
        <div class="space-y-4">
          <!-- 聊天消息示例 -->
          <div class="flex items-start gap-3">
            <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white">AI</div>
            <div class="flex-1">
              <div class="bg-white rounded-lg p-3 shadow-sm">
                <p class="text-sm text-gray-700">你好！我是你的AI助手，有什么我可以帮你的吗？</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 示例按钮区域 -->
      <div class="px-4 pb-2">
        <div class="flex flex-wrap gap-2">
          <button 
            class="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-md text-sm transition-colors"
            @click="useExample('translate')"
          >
            {{ $t('chat.examples.translate') }}
          </button>
          <button 
            class="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-md text-sm transition-colors"
            @click="useExample('summarize')"
          >
            {{ $t('chat.examples.summarize') }}
          </button>
        </div>
      </div>

      <!-- 输入框 -->
      <div class="p-4 border-t border-gray-200">
        <div class="relative">
          <textarea
            class="w-full h-24 p-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            :placeholder="$t('chat.input.placeholder')"
            v-model="messageText"
            @keydown.enter.prevent="sendMessage"
          ></textarea>
          <button 
            class="absolute bottom-3 right-3 p-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600"
            @click="sendMessage"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import dayjs from 'dayjs'

const { t } = useI18n()

const emails = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const sidebarWidth = ref(320)

const fetchEmails = async () => {
  loading.value = true
  error.value = ''
  try {
    // 获取邮箱设置
    const settingsRes = await fetch('/api/email/settings')
    const settings = await settingsRes.json()
    if (!settings || !settings.email) {
      loading.value = false
      return
    }
    // 获取邮件
    const res = await fetch('/api/email/emails/latest-list?limit=20')
    if (!res.ok) throw new Error()
    emails.value = await res.json()
  } catch (e) {
    error.value = t('mail.connectionFailed')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchEmails()
})

// 时间格式化
const formatMailTime = (dateStr: string) => {
  const date = dayjs(dateStr)
  if (date.isSame(dayjs(), 'day')) {
    return date.format('HH:mm')
  }
  return date.format('YYYY-MM-DD')
}

// 聊天消息类型定义
interface ChatMessage {
  id: number
  content: string
  isAI: boolean
  timestamp: Date
}

// 聊天消息列表
const messages = ref<ChatMessage[]>([])
const messageText = ref('')

// 侧边栏宽度相关
const minWidth = 200 // 最小宽度
const maxWidth = 600 // 最大宽度
let isResizing = false
let startX = 0
let startWidth = 0

// 开始调整宽度
const startResize = (e: MouseEvent) => {
  isResizing = true
  startX = e.clientX
  startWidth = sidebarWidth.value
  
  // 添加全局事件监听
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', stopResize)
  
  // 防止选中文本
  e.preventDefault()
}

// 处理鼠标移动
const handleMouseMove = (e: MouseEvent) => {
  if (!isResizing) return
  
  const deltaX = startX - e.clientX
  const newWidth = Math.min(Math.max(startWidth + deltaX, minWidth), maxWidth)
  sidebarWidth.value = newWidth
}

// 停止调整宽度
const stopResize = () => {
  isResizing = false
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', stopResize)
}

// 使用示例
const useExample = (type: 'translate' | 'summarize') => {
  if (type === 'translate') {
    messageText.value = '请将以下内容翻译成中文：\n\n'
  } else if (type === 'summarize') {
    messageText.value = '请总结这封邮件的主要内容：\n\n'
  }
}

// 发送消息
const sendMessage = () => {
  if (!messageText.value.trim()) return
  
  messages.value.push({
    id: Date.now(),
    content: messageText.value,
    isAI: false,
    timestamp: new Date()
  })
  
  // TODO: 调用AI接口获取回复
  messageText.value = ''
}

// 组件卸载时清理事件监听
onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', stopResize)
})
</script>

<style scoped>
/* 自定义滚动条样式 */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: #CBD5E0 #EDF2F7;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #EDF2F7;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #CBD5E0;
  border-radius: 3px;
}

/* 防止文本选中 */
.cursor-col-resize {
  user-select: none;
}
</style> 