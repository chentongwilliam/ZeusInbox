import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import AutomationPage from './pages/AutomationPage.vue'
import MailPage from './pages/MailPage.vue'
import SettingsPage from './pages/SettingsPage.vue'

const routes: RouteRecordRaw[] = [
  { path: '/automation', component: AutomationPage },
  { path: '/mail', component: MailPage },
  { path: '/unsubscribe', component: { template: '<h1>Bulk Unsubscribe</h1>' } },
  { path: '/analytics', component: { template: '<h1>Analytics</h1>' } },
  { path: '/early', component: { template: '<h1>Early Access</h1>' } },
  { path: '/guide', component: { template: '<h1>User Guide</h1>' } },
  { path: '/settings', component: SettingsPage },
  { path: '/', redirect: '/automation' },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router 