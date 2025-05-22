# ZeusInbox MVP Task Breakdown


## 1. 项目初始化 & 架构准备

* [ ] 初始化 Git 仓库，配置`.gitignore`和README
* [ ] 选定并初始化前端项目（Vue3 + Electron脚手架）
* [ ] 初始化后端项目（FastAPI 项目结构、依赖管理）
* [ ] 搭建SQLite数据库，创建初始数据表
* [ ] 确定前后端通信规范（RESTful API）

---

## 2. 基础功能开发

### 2.1 用户与账号管理

* [ ] 前端设置页：邮箱账号(IMAP)管理界面设计与实现
* [ ] 后端API：邮箱账号的增/删/查/改接口
* [ ] 实现邮箱账号信息本地加密存储（如使用Python的cryptography）

### 2.2 邮件拉取与存储

* [ ] 后端：IMAP收取邮件逻辑（支持Outlook/PrivateEmail，解析邮件元数据、正文、附件）
* [ ] 数据库存储邮件元信息、正文摘要、标签等
* [ ] 实现定时/手动拉取未读邮件功能
* [ ] 前端邮件列表展示组件设计与开发
* [ ] 邮件详情展示页设计与开发

### 2.3 基础邮件管理

* [ ] 邮件标记为已读/未读/重要的接口与UI
* [ ] 简单标签/文件夹管理（如“收件箱”、“广告”、“重要”）
* [ ] 搜索和筛选功能（按发件人、主题、标签等）

---

## 3. AI & MCP集成相关

### 3.1 MCP能力接入

* [ ] 配置MCP Provider（设置界面/后端配置支持自定义MCP Tool Server地址）
* [ ] 后端MCP接口适配（支持与Node.js MCP Tool Server的HTTP/JSON通信）
* [ ] MCP工具注册与管理（预置邮件翻译、分类2-3个工具）
* [ ] 后端实现与AI Provider的多轮MCP工具调用链路
* [ ] 日志记录每次MCP交互和工具调用历史

### 3.2 AI助手与前端集成

* [ ] AI助手区UI设计与实现（邮件详情页右侧chat对话框）
* [ ] 前端与后端AI/MCP统一API集成（所有AI操作都走后端MCP链路）
* [ ] 实现邮件摘要、分类、建议回复、翻译等chat交互功能
* [ ] 支持AI结果复制、编辑和反馈

---

## 4. 安全与隐私

* [ ] 邮箱账号/密码/API Key 本地加密存储
* [ ] 本地数据隐私清理功能（UI和后端接口支持）
* [ ] 配置文件/日志加密和安全访问控制

---

## 5. 本地数据管理

* [ ] SQLite数据表结构设计与建表（账号、邮件、标签、AI历史、工具调用日志等）
* [ ] ORM层封装（推荐使用SQLModel或SQLAlchemy）
* [ ] 数据迁移脚本和本地备份/恢复机制

---

## 6. 跨平台适配与打包

* [ ] Electron打包配置（Win/Linux/MacOS）
* [ ] 各平台兼容性测试（界面、功能、系统托盘等）
* [ ] 自动更新/版本管理功能（可后置）

---

## 7. 测试与文档

* [ ] 单元测试和集成测试（后端API、前端主要功能）
* [ ] MVP功能全流程自测脚本
* [ ] 编写详细README、部署运行说明和技术架构文档
* [ ] 用户手册/FAQ初稿

---

## 8. 项目管理与协作

* [ ] 制定项目开发规则/Code Style（见前文Project Rules）
* [ ] 周会/进度同步与问题记录（如需团队协作）
* [ ] 需求/设计/接口文档同步更新

---

# 示例任务分工（可直接导入项目管理工具）

```markdown
- Project Initialization
  - Set up git repo & README
  - Init Vue3+Electron frontend
  - Init FastAPI backend
  - Design SQLite schema

- Account Management
  - Frontend: IMAP account UI
  - Backend: Account CRUD API
  - Encrypt credentials storage

- Email Fetch & Storage
  - Backend: IMAP fetch logic
  - Store email metadata/content
  - Frontend: Email list & detail UI

- Basic Email Management
  - Mark read/unread/important
  - Folder/tag management
  - Search/filter UI

- MCP Integration
  - Backend: MCP HTTP adapter
  - Configure MCP provider
  - Register & test basic tools (translate/classify)
  - Log tool call history

- AI Assistant UI
  - Chat panel on email detail
  - Integrate AI/MCP API
  - Copy/edit/feedback features

- Security & Privacy
  - Local encryption
  - Data clear UI

- Cross-Platform Build
  - Electron build for Win/Mac/Linux
  - Compatibility testing

- Testing & Docs
  - Unit/integration tests
  - README & user guide
```