import { createApp, reactive } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 全局设置对象
export const globalSettings = reactive({
  language: 'en',
  emailUpdateInterval: 5
})

async function loadGlobalSettings() {
  try {
    const res = await fetch('/api/settings/all');
    if (res.ok) {
      const data = await res.json();
      if (data.language && ['en', 'zh', 'de'].includes(data.language)) {
        globalSettings.language = data.language;
        i18n.global.locale.value = data.language;
        localStorage.setItem('language', data.language);
      }
      if (typeof data.email_update_interval !== 'undefined' && data.email_update_interval !== null) {
        globalSettings.emailUpdateInterval = Number(data.email_update_interval);
      }
    }
  } catch (e) {}
}

loadGlobalSettings().then(() => {
  const app = createApp(App)
  app.use(router)
  app.use(i18n)
  app.use(ElementPlus)
  app.mount('#app')
})

// Use contextBridge
window.ipcRenderer?.on?.('main-process-message', (_event, message) => {
  console.log(message)
})
