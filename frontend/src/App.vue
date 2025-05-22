<script setup lang="ts">
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import { StagewiseToolbar } from '@stagewise/toolbar-vue'
import { computed } from 'vue'

const isDevelopment = computed(() => process.env.NODE_ENV === 'development')

const stagewiseConfig = {
  plugins: []
}
</script>

<template>
  <div class="flex h-screen w-screen bg-gray-100">
    <Sidebar />
    <main class="flex-1 p-10 overflow-hidden bg-gray-100">
      <StagewiseToolbar v-if="isDevelopment" :config="stagewiseConfig" />
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Inter', 'Helvetica Neue', Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  background: #f7f8fa;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
