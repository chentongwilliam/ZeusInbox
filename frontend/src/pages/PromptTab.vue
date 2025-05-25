<template>
  <div class="flex flex-1 gap-6 min-h-0">
    <!-- Prompt内容，左侧输入区 -->
    <div class="flex-1 bg-white rounded-xl shadow border p-6 flex flex-col min-h-0">
      <div class="text-gray-900 text-xl font-bold mb-2">How your AI personal assistant should handle incoming emails</div>
      <div class="text-gray-500 mb-4">Write a prompt for your assistant to follow.</div>
      <div class="flex-1 flex flex-col min-h-0">
        <textarea
          class="flex-1 min-h-[180px] max-h-[400px] p-4 border rounded-lg resize-none text-gray-800 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-400 mb-4 overflow-auto"
          style="resize: none;"
          :placeholder="samplePlaceholder"
          v-model="promptText"
          @input="autoResize($event)"
          ref="promptTextarea"
        ></textarea>
        <div class="flex gap-2 mt-2 shrink-0">
          <button class="px-4 py-2 bg-gray-900 text-white rounded-md font-semibold shadow">Save</button>
          <button class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md border border-gray-200 font-medium">Give me ideas</button>
          <button class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md border border-gray-200 font-medium">Choose persona</button>
        </div>
      </div>
    </div>
    <!-- 右侧Examples区 -->
    <div class="w-96 bg-white rounded-xl shadow border p-6 flex flex-col min-h-0">
      <div class="text-gray-900 font-semibold mb-4">Examples</div>
      <div class="flex flex-col gap-2 overflow-y-auto" style="min-height:0;max-height:calc(100vh-220px);">
        <button
          v-for="(example, idx) in examples"
          :key="idx"
          class="text-left px-3 py-2 bg-gray-50 rounded border text-gray-700 hover:bg-gray-100"
          @click="addExampleToPrompt(example)"
        >
          {{ example }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
const samplePlaceholder = `Here's an example of what your prompt might look like:\n\n* Label emails that require a reply as 'Reply Required'.\n* Label urgent emails as 'Urgent'.\n* Label newsletters as 'Newsletter' and archive them.\n* Label marketing emails as 'Marketing' and archive them.\n* Label emails from @mycompany.com addresses as 'Team'.\n* Label receipts as 'Receipt' and archive them.\n\nIf someone asks about pricing, reply with:\n---\nHi NAME!\n\nI'm currently offering a 10% discount for the first 10 customers.\n\nLet me know if you're interested!\n---`
const promptText = ref('')
const promptTextarea = ref(null)
const examples = [
  "Label emails that require a reply as 'Reply Required'",
  "Label urgent emails as 'Urgent'",
  "Label newsletters as 'Newsletter' and archive them",
  "Label marketing emails as 'Marketing' and archive them",
  "Label emails from @mycompany.com addresses as 'Team'",
  "Label receipts as 'Receipt' and archive them",
  'Label pitch decks as "Pitch Deck" and forward them to john@investing.com',
  'Label receipts as "Receipt" and forward them to jane@accounting.com',
  'Reply to cold emails by telling them to check out Inbox Zero. Then mark them as spam',
  'Label high priority emails as "High Priority"',
  'If a founder asks to set up a call, send them my calendar link: https://cal.com/example',
]
function autoResize(e: any) {
  const ta = e?.target || promptTextarea.value
  if (ta) {
    ta.style.height = 'auto'
    ta.style.height = ta.scrollHeight + 'px'
  }
}
function addExampleToPrompt(example: string) {
  if (promptText.value) {
    promptText.value += '\n' + example
  } else {
    promptText.value = example
  }
  nextTick(() => {
    if (promptTextarea.value) autoResize({ target: promptTextarea.value })
  })
}
onMounted(() => {
  nextTick(() => {
    if (promptTextarea.value) autoResize({ target: promptTextarea.value })
  })
})
</script>

<style scoped>
/* 保持整体风格与其他页面一致 */
</style> 