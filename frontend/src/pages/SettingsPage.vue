<template>
  <div class="settings-container">
    <div class="settings-layout">
      <!-- 左侧导航栏 -->
      <div class="settings-nav">
        <div class="nav-section">
          <div class="nav-title">{{ $t('settings.title') }}</div>
          <div 
            v-for="section in sections" 
            :key="section.id"
            :class="['nav-item', { active: currentSection === section.id }]"
            @click="currentSection = section.id"
          >
            {{ $t(`settings.${section.id}.title`) }}
          </div>
        </div>
      </div>

      <!-- 右侧内容区 -->
      <div class="settings-content">
        <!-- 邮箱设置 -->
        <div v-if="currentSection === 'email'" class="settings-section">
          <h2>{{ $t('settings.email.title') }}</h2>
          <el-form :model="emailForm" label-width="120px">
            <el-form-item :label="$t('settings.email.email')">
              <el-input v-model="emailForm.email" :placeholder="$t('settings.email.email')" />
            </el-form-item>
            <el-form-item :label="$t('settings.email.imapServer')">
              <el-input v-model="emailForm.imap_server" placeholder="imap.example.com" />
            </el-form-item>
            <el-form-item :label="$t('settings.email.imapPort')">
              <el-input v-model="emailForm.imap_port" placeholder="993" />
            </el-form-item>
            <el-form-item :label="$t('settings.email.username')">
              <el-input v-model="emailForm.username" :placeholder="$t('settings.email.username')" />
            </el-form-item>
            <el-form-item :label="$t('settings.email.password')">
              <el-input type="password" v-model="emailForm.password" :placeholder="$t('settings.email.password')" />
            </el-form-item>
            <el-form-item :label="$t('settings.email.isActive')">
              <el-switch v-model="emailForm.is_active" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveEmailSettings">{{ $t('settings.email.save') }}</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- AI设置 -->
        <div v-if="currentSection === 'ai'" class="settings-section">
          <h2>{{ $t('settings.ai.title') }}</h2>
          <el-form label-width="160px">
            <el-form-item :label="$t('settings.ai.apiProvider')">
              <el-select v-model="aiSettings.apiProvider" filterable>
                <el-option label="OpenRouter" value="OpenRouter" />
                <el-option label="OpenAI" value="OpenAI" />
                <el-option label="DeepSeek" value="DeepSeek" />
              </el-select>
            </el-form-item>
            <el-form-item :label="$t('settings.ai.apiKey')">
              <el-input v-model="aiSettings.apiKey" type="password" show-password :placeholder="$t('settings.ai.apiKey')" />
            </el-form-item>
            <el-form-item :label="$t('settings.ai.model')">
              <el-select v-model="aiSettings.model" filterable :placeholder="$t('settings.ai.model')">
                <el-option
                  v-for="item in modelOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                  <div>
                    <div style="font-weight:bold">{{ item.label }}</div>
                    <div style="font-size:12px;color:#888">{{ item.desc }}</div>
                    <div v-if="item.limits" style="font-size:12px;color:#e74c3c">{{ item.limits }}</div>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item :label="$t('settings.ai.customInstructions')">
              <el-input
                v-model="aiSettings.customInstructions"
                type="textarea"
                :rows="3"
                :placeholder="$t('settings.ai.customInstructions')"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveAISettings">{{ $t('settings.email.save') }}</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- MCP Server设置 -->
        <div v-if="currentSection === 'mcp'" class="settings-section">
          <h2>{{ $t('settings.mcp.title') }}</h2>
          <el-button type="success" @click="showAddServerDialog = true" style="margin-bottom: 16px;">
            {{ $t('settings.mcp.addServer') }}
          </el-button>
          <el-row gutter="16">
            <el-col :span="12" v-for="server in mcpServers" :key="server.id" style="margin-bottom: 16px;">
              <el-card>
                <div style="margin-bottom: 8px;">
                  <span>{{ $t('settings.mcp.address') }}: </span>{{ server.address }}<br>
                  <span>{{ $t('settings.mcp.port') }}: </span>{{ server.port }}<br>
                  <span>{{ $t('settings.mcp.status') }}: </span>
                  <el-tag :type="server.status === 'running' ? 'success' : (server.status === 'stopped' ? 'info' : 'warning')">
                    {{ $t('settings.mcp.' + (server.status || 'unknown')) }}
                  </el-tag>
                  <el-switch v-model="server.active" @change="toggleActive(server)" style="margin-left: 16px;" />
                  <span style="margin-left: 4px;">{{ $t('settings.mcp.active') }}</span>
                </div>
                <div v-if="server.error" class="mcp-error" style="margin-bottom: 8px;">
                  <el-alert :title="server.error" type="error" show-icon />
                </div>
                <div>
                  <el-button size="small" type="primary" @click="startServer(server)" v-if="server.status !== 'running'">{{ $t('settings.mcp.start') }}</el-button>
                  <el-button size="small" type="warning" @click="stopServer(server)" v-if="server.status === 'running'">{{ $t('settings.mcp.stop') }}</el-button>
                  <el-button size="small" type="danger" @click="confirmDeleteServer(server)">{{ $t('settings.mcp.delete') }}</el-button>
                  <el-button size="small" @click="refreshServer(server)">{{ $t('settings.mcp.refresh') }}</el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
          <el-dialog v-model="showAddServerDialog" :title="$t('settings.mcp.addServer')">
            <el-form :model="addServerForm">
              <el-form-item :label="$t('settings.mcp.address')">
                <el-input v-model="addServerForm.address" />
              </el-form-item>
              <el-form-item :label="$t('settings.mcp.port')">
                <el-input v-model="addServerForm.port" />
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="showAddServerDialog = false">{{ $t('settings.mcp.cancel') }}</el-button>
              <el-button type="primary" @click="addServer">{{ $t('settings.mcp.add') }}</el-button>
            </template>
          </el-dialog>
          <el-dialog v-model="showDeleteDialog" :title="$t('settings.mcp.confirmDelete')">
            <span>{{ $t('settings.mcp.confirmDelete') }}</span>
            <template #footer>
              <el-button @click="showDeleteDialog = false">{{ $t('settings.mcp.cancel') }}</el-button>
              <el-button type="danger" @click="deleteServer">{{ $t('settings.mcp.confirm') }}</el-button>
            </template>
          </el-dialog>
        </div>

        <!-- 语言设置 -->
        <div v-if="currentSection === 'language'" class="settings-section">
          <h2>{{ $t('settings.language.title') }}</h2>
          <el-form label-width="120px">
            <el-form-item :label="$t('settings.language.current')">
              <el-select v-model="currentLocale" @change="changeLanguage">
                <el-option label="English" value="en" />
                <el-option label="Deutsch" value="de" />
                <el-option label="中文" value="zh" />
              </el-select>
            </el-form-item>
          </el-form>
        </div>

        <!-- 主题设置 -->
        <div v-if="currentSection === 'theme'" class="settings-section">
          <h2>{{ $t('settings.theme.title') }}</h2>
          <el-form label-width="120px">
            <el-form-item :label="$t('settings.theme.mode')">
              <el-radio-group v-model="themeSettings.mode">
                <el-radio label="light">{{ $t('settings.theme.light') }}</el-radio>
                <el-radio label="dark">{{ $t('settings.theme.dark') }}</el-radio>
                <el-radio label="system">{{ $t('settings.theme.system') }}</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
        </div>

        <!-- 通知设置 -->
        <div v-if="currentSection === 'notification'" class="settings-section">
          <h2>{{ $t('settings.notification.title') }}</h2>
          <el-form label-width="120px">
            <el-form-item :label="$t('settings.notification.email')">
              <el-switch v-model="notificationSettings.email" />
            </el-form-item>
            <el-form-item :label="$t('settings.notification.desktop')">
              <el-switch v-model="notificationSettings.desktop" />
            </el-form-item>
          </el-form>
        </div>

        <!-- 数据备份 -->
        <div v-if="currentSection === 'backup'" class="settings-section">
          <h2>{{ $t('settings.backup.title') }}</h2>
          <el-form label-width="120px">
            <el-form-item :label="$t('settings.backup.auto')">
              <el-switch v-model="backupSettings.auto" />
            </el-form-item>
            <el-form-item :label="$t('settings.backup.frequency')">
              <el-select v-model="backupSettings.frequency">
                <el-option :label="$t('settings.backup.daily')" value="daily" />
                <el-option :label="$t('settings.backup.weekly')" value="weekly" />
                <el-option :label="$t('settings.backup.monthly')" value="monthly" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="backupNow">{{ $t('settings.backup.backupNow') }}</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 关于信息 -->
        <div v-if="currentSection === 'about'" class="settings-section">
          <h2>{{ $t('settings.about.title') }}</h2>
          <div class="about-content">
            <p>{{ $t('settings.about.version') }}: 1.0.0</p>
            <p>{{ $t('settings.about.copyright') }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'

interface ModelOption {
  label: string;
  value: string;
  desc?: string;
  limits?: string;
}

interface MCPServer {
  id: string;
  address: string;
  port: string;
  active: boolean;
  status: string; // running, stopped, unknown
  error?: string;
}

const { t, locale } = useI18n()

// 导航配置
const sections = [
  { id: 'email', title: t('settings.email.title') },
  { id: 'ai', title: t('settings.ai.title') },
  { id: 'mcp', title: t('settings.mcp.title') },
  { id: 'language', title: t('settings.language.title') },
  { id: 'theme', title: t('settings.theme.title') },
  { id: 'notification', title: t('settings.notification.title') },
  { id: 'backup', title: t('settings.backup.title') },
  { id: 'about', title: t('settings.about.title') }
]

const currentSection = ref('email')
const currentLocale = computed({
  get: () => locale.value,
  set: (value) => locale.value = value
})

// 邮箱设置表单
const emailForm = reactive({
  email: '',
  imap_server: '',
  imap_port: '',
  username: '',
  password: '',
  is_active: true
})

// AI设置
const aiSettings = reactive({
  apiProvider: 'OpenRouter',
  apiKey: '',
  model: '',
  customInstructions: ''
})

const modelOptions = ref<ModelOption[]>([])

function loadModels() {
  fetch('/api/models')
    .then(res => res.json())
    .then(data => {
      const arr = data.models?.data || data.data || []
      modelOptions.value = arr.map((item: any) => ({
        label: item.name || item.id,
        value: item.id || item.name,
        desc: item.description || '',
        limits: item.limits || ''
      }))
    })
    .catch(() => { modelOptions.value = [] })
}

watch(() => aiSettings.apiProvider, (val) => {
  if (val === 'OpenRouter') {
    loadModels()
  } else {
    modelOptions.value = []
  }
}, { immediate: true })

onMounted(() => {
  if (aiSettings.apiProvider === 'OpenRouter') {
    loadModels()
  }
})

// MCP Server设置
const mcpServers = ref<MCPServer[]>([])
const showAddServerDialog = ref(false)
const addServerForm = reactive({ address: '', port: '' })
const showDeleteDialog = ref(false)
let serverToDelete: MCPServer | null = null
let refreshTimer: any = null

function fetchServers() {
  // TODO: Replace with real API call
  // Example mock data:
  mcpServers.value = [
    { id: '1', address: 'localhost', port: '8188', active: true, status: 'running', error: '' },
    { id: '2', address: '127.0.0.1', port: '9001', active: false, status: 'stopped', error: 'Connection refused' }
  ]
}

function refreshAllServers() {
  // TODO: Replace with real API call for all servers
  fetchServers()
}

function refreshServer(server: MCPServer) {
  // TODO: Replace with real API call for single server
  fetchServers()
}

function addServer() {
  // TODO: Replace with real API call
  mcpServers.value.push({
    id: Date.now().toString(),
    address: addServerForm.address,
    port: addServerForm.port,
    active: true,
    status: 'unknown',
    error: ''
  })
  showAddServerDialog.value = false
  addServerForm.address = ''
  addServerForm.port = ''
}

function confirmDeleteServer(server: MCPServer) {
  showDeleteDialog.value = true
  serverToDelete = server
}

function deleteServer() {
  if (serverToDelete) {
    mcpServers.value = mcpServers.value.filter(s => s.id !== serverToDelete!.id)
    showDeleteDialog.value = false
    serverToDelete = null
  }
}

function toggleActive(server: MCPServer) {
  // TODO: Replace with real API call
  server.active = !server.active
}

function startServer(server: MCPServer) {
  // TODO: Replace with real API call
  server.status = 'running'
  server.error = ''
}

function stopServer(server: MCPServer) {
  // TODO: Replace with real API call
  server.status = 'stopped'
}

onMounted(() => {
  fetchServers()
  refreshTimer = setInterval(refreshAllServers, 5000)
})
onUnmounted(() => {
  if (refreshTimer) clearInterval(refreshTimer)
})

// MCP Server设置
const mcpSettings = reactive({
  server: '',
  port: ''
})

// 主题设置
const themeSettings = reactive({
  mode: 'light'
})

// 通知设置
const notificationSettings = reactive({
  email: true,
  desktop: true
})

// 备份设置
const backupSettings = reactive({
  auto: true,
  frequency: 'daily'
})

// 保存邮箱设置
const saveEmailSettings = () => {
  // TODO: 实现保存逻辑
  console.log('保存邮箱设置:', emailForm)
}

// 保存AI设置
const saveAISettings = () => {
  // TODO: 实现保存逻辑
  console.log('保存AI设置:', aiSettings)
}

// 立即备份
const backupNow = () => {
  // TODO: 实现备份逻辑
  console.log('开始备份')
}

// 切换语言
const changeLanguage = (lang: string) => {
  locale.value = lang
  // 保存语言设置到本地存储
  localStorage.setItem('language', lang)
}
</script>

<style scoped>
.settings-container {
  height: 100vh;
  background: #f5f5f5;
}

.settings-layout {
  display: flex;
  height: 100%;
}

.settings-nav {
  width: 240px;
  background: #f3f3f3;
  border-right: 1px solid #e0e0e0;
  padding: 20px 0;
}

.nav-section {
  padding: 0 12px;
}

.nav-title {
  font-size: 12px;
  color: #666;
  padding: 8px 12px;
  margin-bottom: 8px;
}

.nav-item {
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
  margin-bottom: 2px;
  font-size: 13px;
}

.nav-item:hover {
  background: #e8e8e8;
}

.nav-item.active {
  background: #e0e0e0;
}

.settings-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.settings-section {
  max-width: 800px;
  margin: 0 auto;
}

.settings-section h2 {
  margin-bottom: 24px;
  font-size: 20px;
  font-weight: 500;
}

.about-content {
  line-height: 1.6;
  color: #666;
}
</style> 