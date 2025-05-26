import { createI18n } from 'vue-i18n'

// English translations
const en = {
  settings: {
    title: 'Settings',
    email: {
      title: 'Email Settings',
      email: 'Email Account',
      imapServer: 'IMAP Server',
      imapPort: 'IMAP Port',
      username: 'Username',
      password: 'Password',
      isActive: 'Active',
      save: 'Save Settings',
      validating: "Validating email...",
      imapServerTooltip: 'For example: mail.privateemail.com',
      imapPortTooltip: 'SSL port is usually 993, non-SSL port is usually 143',
      requiredFields: 'Please fill in all required fields',
      invalidPort: 'Please enter a valid port number (1-65535)',
      connectionSuccess: 'Email connection successful!',
      saveSuccess: 'Settings saved successfully!',
      connectionFailed: 'Email connection failed',
      saveError: 'Error saving email settings',
      updateInterval: 'Auto Update Interval',
      updateIntervalTooltip: 'Set how often to check for new emails (1-60 minutes)',
      minutes: 'minutes',
      updateSuccess: 'Settings updated successfully!'
    },
    ai: {
      title: 'AI Settings',
      apiProvider: 'API Provider',
      apiKey: 'OpenRouter API Key',
      sortRouting: 'Sort underlying provider routing',
      model: 'Model',
      customInstructions: 'Custom Instructions',
      temperature: 'Temperature'
    },
    mcp: {
      title: 'MCP Server Settings',
      server: 'Server Address',
      port: 'Port',
      addServer: 'Add Server',
      address: 'Address',
      status: 'Status',
      active: 'Active',
      start: 'Start',
      stop: 'Stop',
      delete: 'Delete',
      error: 'Error Message',
      running: 'Running',
      stopped: 'Stopped',
      unknown: 'Unknown',
      add: 'Add',
      cancel: 'Cancel',
      confirmDelete: 'Are you sure to delete this server?',
      confirm: 'Confirm',
      refresh: 'Refresh',
      actions: 'Actions'
    },
    language: {
      title: 'Language Settings',
      current: 'Interface Language'
    },
    theme: {
      title: 'Theme Settings',
      mode: 'Theme Mode',
      light: 'Light',
      dark: 'Dark',
      system: 'Follow System'
    },
    notification: {
      title: 'Notification Settings',
      email: 'Email Notifications',
      desktop: 'Desktop Notifications'
    },
    backup: {
      title: 'Data Backup',
      auto: 'Auto Backup',
      frequency: 'Backup Frequency',
      daily: 'Daily',
      weekly: 'Weekly',
      monthly: 'Monthly',
      backupNow: 'Backup Now'
    },
    privacy: {
      title: 'Privacy Settings',
      dataCollection: 'Data Collection',
      usageStats: 'Usage Statistics'
    },
    about: {
      title: 'About',
      version: 'Version',
      copyright: '© 2025 ZeusInbox. All rights reserved.'
    }
  },
  sidebar: {
    aiAssistant: 'AI Personal Assistant',
    prompt: 'Prompt',
    mail: 'Mail',
    bulkUnsubscribe: 'Bulk Unsubscribe',
    analytics: 'Analytics',
    earlyAccess: 'Early Access',
    userGuide: 'User Guide',
    settings: 'Settings'
  },
  mail: {
    noMail: 'No emails yet',
    connectionFailed: 'Email connection failed, please check your settings',
    reply: 'Reply',
    replyAll: 'Reply all',
    forward: 'Forward',
    delete: 'Delete'
  },
  chat: {
    examples: {
      translate: 'Translate to Chinese',
      summarize: 'Summarize this email'
    },
    input: {
      placeholder: 'Type your message...'
    }
  }
}

// German translations
const de = {
  settings: {
    title: 'Einstellungen',
    email: {
      title: 'E-Mail-Einstellungen',
      email: 'E-Mail-Konto',
      imapServer: 'IMAP-Server',
      imapPort: 'IMAP-Port',
      username: 'Benutzername',
      password: 'Passwort',
      isActive: 'Aktiv',
      save: 'Einstellungen speichern',
      validating: "E-Mail wird überprüft...",
      imapServerTooltip: 'Beispiel: mail.privateemail.com',
      imapPortTooltip: 'SSL-Port ist normalerweise 993, nicht-SSL-Port ist normalerweise 143',
      requiredFields: 'Bitte füllen Sie alle erforderlichen Felder aus',
      invalidPort: 'Bitte geben Sie eine gültige Portnummer ein (1-65535)',
      connectionSuccess: 'E-Mail-Verbindung erfolgreich!',
      saveSuccess: 'Einstellungen erfolgreich gespeichert!',
      connectionFailed: 'E-Mail-Verbindung fehlgeschlagen',
      saveError: 'Fehler beim Speichern der E-Mail-Einstellungen',
      updateInterval: 'Automatisches Update-Intervall',
      updateIntervalTooltip: 'Legen Sie fest, wie oft nach neuen E-Mails gesucht werden soll (1-60 Minuten)',
      minutes: 'Minuten',
      updateSuccess: 'Einstellungen erfolgreich aktualisiert!'
    },
    ai: {
      title: 'KI-Einstellungen',
      apiProvider: 'API-Anbieter',
      apiKey: 'OpenRouter API-Schlüssel',
      sortRouting: 'Sortiere zugrundeliegendes Routing',
      model: 'Modell',
      customInstructions: 'Benutzerdefinierte Anweisungen',
      temperature: 'Temperatur'
    },
    mcp: {
      title: 'MCP-Server-Einstellungen',
      server: 'Server-Adresse',
      port: 'Port',
      addServer: 'Server hinzufügen',
      address: 'Adresse',
      status: 'Status',
      active: 'Aktiv',
      start: 'Start',
      stop: 'Stop',
      delete: 'Löschen',
      error: 'Fehlermeldung',
      running: 'Läuft',
      stopped: 'Nicht läuft',
      unknown: 'Unbekannt',
      add: 'Hinzufügen',
      cancel: 'Abbrechen',
      confirmDelete: 'Sind Sie sicher, dass Sie diesen Server löschen möchten?',
      confirm: 'Bestätigen',
      refresh: 'Aktualisieren',
      actions: 'Aktionen'
    },
    language: {
      title: 'Spracheinstellungen',
      current: 'Oberflächensprache'
    },
    theme: {
      title: 'Design-Einstellungen',
      mode: 'Design-Modus',
      light: 'Hell',
      dark: 'Dunkel',
      system: 'System'
    },
    notification: {
      title: 'Benachrichtigungseinstellungen',
      email: 'E-Mail-Benachrichtigungen',
      desktop: 'Desktop-Benachrichtigungen'
    },
    backup: {
      title: 'Datensicherung',
      auto: 'Automatische Sicherung',
      frequency: 'Sicherungshäufigkeit',
      daily: 'Täglich',
      weekly: 'Wöchentlich',
      monthly: 'Monatlich',
      backupNow: 'Jetzt sichern'
    },
    privacy: {
      title: 'Datenschutzeinstellungen',
      dataCollection: 'Datenerfassung',
      usageStats: 'Nutzungsstatistiken'
    },
    about: {
      title: 'Über',
      version: 'Version',
      copyright: '© 2025 ZeusInbox. Alle Rechte vorbehalten.'
    }
  },
  sidebar: {
    aiAssistant: 'AI Personal Assistant',
    prompt: 'Prompt',
    mail: 'E-Mail',
    bulkUnsubscribe: 'Massen-Abmeldung',
    analytics: 'Analytik',
    earlyAccess: 'Früher Zugang',
    userGuide: 'Benutzerhandbuch',
    settings: 'Einstellungen'
  },
  mail: {
    noMail: 'Noch keine E-Mails',
    connectionFailed: 'E-Mail-Verbindung fehlgeschlagen, bitte Einstellungen prüfen',
    reply: 'Antworten',
    replyAll: 'Allen antworten',
    forward: 'Weiterleiten',
    delete: 'Löschen'
  },
  chat: {
    examples: {
      translate: 'Ins Chinesische übersetzen',
      summarize: 'E-Mail zusammenfassen'
    },
    input: {
      placeholder: 'Geben Sie Ihre Nachricht ein...'
    }
  }
}

// Chinese translations
const zh = {
  settings: {
    title: '设置',
    email: {
      title: '邮箱设置',
      email: '邮箱账号',
      imapServer: 'IMAP服务器',
      imapPort: 'IMAP端口',
      username: '用户名',
      password: '密码',
      isActive: '是否激活',
      save: '保存设置',
      validating: "正在验证邮箱...",
      imapServerTooltip: '例如：mail.privateemail.com',
      imapPortTooltip: 'SSL端口通常是993，非SSL端口通常是143',
      requiredFields: '请填写所有必填字段',
      invalidPort: '请输入有效的端口号（1-65535）',
      connectionSuccess: '邮箱连接成功！',
      saveSuccess: '设置保存成功！',
      connectionFailed: '邮箱连接失败',
      saveError: '保存邮箱设置时出错',
      updateInterval: '自动更新间隔',
      updateIntervalTooltip: '设置检查新邮件的频率（1-60分钟）',
      minutes: '分钟',
      updateSuccess: '设置更新成功！'
    },
    ai: {
      title: 'AI设置',
      apiProvider: 'API提供商',
      apiKey: 'OpenRouter API密钥',
      sortRouting: '排序底层路由',
      model: '模型',
      customInstructions: '自定义指令',
      temperature: '温度'
    },
    mcp: {
      title: 'MCP服务器设置',
      server: '服务器地址',
      port: '端口',
      addServer: '添加服务器',
      address: '地址',
      status: '状态',
      active: '激活',
      start: '启动',
      stop: '停止',
      delete: '删除',
      error: '错误信息',
      running: '运行中',
      stopped: '未运行',
      unknown: '未知',
      add: '新增',
      cancel: '取消',
      confirmDelete: '确定要删除该服务器吗？',
      confirm: '确定',
      refresh: '刷新',
      actions: '操作'
    },
    language: {
      title: '语言设置',
      current: '界面语言'
    },
    theme: {
      title: '主题设置',
      mode: '主题模式',
      light: '浅色',
      dark: '深色',
      system: '跟随系统'
    },
    notification: {
      title: '通知设置',
      email: '邮件通知',
      desktop: '桌面通知'
    },
    backup: {
      title: '数据备份',
      auto: '自动备份',
      frequency: '备份频率',
      daily: '每天',
      weekly: '每周',
      monthly: '每月',
      backupNow: '立即备份'
    },
    privacy: {
      title: '隐私设置',
      dataCollection: '数据收集',
      usageStats: '使用统计'
    },
    about: {
      title: '关于',
      version: '版本',
      copyright: '© 2025 ZeusInbox. 保留所有权利。'
    }
  },
  sidebar: {
    aiAssistant: 'AI个人助理',
    prompt: '提示词',
    mail: '邮件',
    bulkUnsubscribe: '批量退订',
    analytics: '数据分析',
    earlyAccess: '抢先体验',
    userGuide: '用户指南',
    settings: '设置'
  },
  mail: {
    noMail: '暂无邮件',
    connectionFailed: '邮箱连接失败，请检查设置',
    reply: '回复',
    replyAll: '全部回复',
    forward: '转发',
    delete: '删除'
  },
  chat: {
    examples: {
      translate: '翻译成中文',
      summarize: '总结这封邮件'
    },
    input: {
      placeholder: '输入消息...'
    }
  }
}

const i18n = createI18n({
  legacy: false, // 使用Composition API
  locale: 'en', // 默认语言为英语
  fallbackLocale: 'en', // 回退语言为英语
  messages: {
    en,
    de,
    zh
  }
})

export default i18n 