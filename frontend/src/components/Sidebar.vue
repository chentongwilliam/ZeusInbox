<template>
  <nav class="flex flex-col justify-between h-screen w-60 bg-gray-900 text-white py-6">
    <div>
      <div class="text-2xl font-bold px-8 pb-8 tracking-widest">ZEUS INBOX</div>
      <ul>
        <li v-for="item in menu" :key="item.path">
          <router-link :to="item.path" class="flex items-center px-8 py-3 text-base hover:bg-gray-800 transition-colors rounded-r-full mb-1" active-class="bg-gray-800 border-l-4 border-green-400">
            <span class="mr-3 text-lg">{{ item.icon }}</span>
            <span>{{ $t(`sidebar.${item.id}`) }}</span>
          </router-link>
        </li>
      </ul>
    </div>
    <ul>
      <li v-for="item in bottomMenu" :key="item.path">
        <router-link :to="item.path" class="flex items-center px-8 py-2 text-base hover:bg-gray-800 transition-colors rounded-r-full mb-1" active-class="bg-gray-800 border-l-4 border-green-400">
          <span class="mr-3 text-lg">{{ item.icon }}</span>
          <span>{{ $t(`sidebar.${item.id}`) }}</span>
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
const menu = [
  { id: 'aiAutomation', path: '/automation', icon: '🤖' },
  { id: 'mail', path: '/mail', icon: '📧' },
  { id: 'bulkUnsubscribe', path: '/unsubscribe', icon: '📤' },
  { id: 'analytics', path: '/analytics', icon: '📊' },
  { id: 'earlyAccess', path: '/early', icon: '🚀' },
]

const bottomMenu = [
  { id: 'userGuide', path: '/guide', icon: '📖' },
  { id: 'settings', path: '/settings', icon: '⚙️' },
]
</script>

<style scoped>
.sidebar {
  width: 240px;
  background: #181c20;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100vh;
  padding: 24px 0 12px 0;
}
.sidebar-title {
  font-size: 1.5rem;
  font-weight: bold;
  padding: 0 32px 24px 32px;
  letter-spacing: 2px;
}
.sidebar-menu, .sidebar-bottom {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar-link {
  display: flex;
  align-items: center;
  padding: 12px 32px;
  color: #fff;
  text-decoration: none;
  font-size: 1rem;
  border-left: 4px solid transparent;
  transition: background 0.2s, border-color 0.2s;
}
.sidebar-link.active, .sidebar-link:hover {
  background: #23272b;
  border-left: 4px solid #42b883;
}
.icon {
  margin-right: 12px;
  font-size: 1.2em;
}
</style> 