# ZeusInbox Packaging & Run Guide / ZeusInbox 打包与运行说明

---

## 中文说明

### 1. 目标
本项目采用 Electron + Vue 前端，FastAPI 后端。打包后希望用户只需运行一个程序，前后端自动启动，无需手动操作。

### 2. 推荐打包方案

#### 2.1 Electron 主进程自动启动后端
- 在 Electron 的主进程（main.js/main.ts）中，使用 Node.js 的 child_process 自动拉起 FastAPI 后端服务。
- 用户只需双击应用，前后端自动启动。

##### 示例代码片段：
```js
const { app, BrowserWindow, ipcMain } = require('electron')
const { spawn } = require('child_process')
let backendProcess
const backendPort = 8001 // 可根据需要动态分配

app.on('ready', () => {
  // 启动 FastAPI 后端
  backendProcess = spawn('uvicorn', ['app.main:app', '--host', '127.0.0.1', '--port', backendPort], {
    cwd: 'backend',
    shell: true,
    stdio: 'inherit'
  })

  // 启动前端窗口
  const win = new BrowserWindow({ width: 1200, height: 800 })
  win.loadURL('http://localhost:5173') // 或者打包后的本地文件

  // 向渲染进程传递后端端口
  ipcMain.handle('get-backend-port', () => backendPort)
})

app.on('will-quit', () => {
  if (backendProcess) backendProcess.kill()
})
```

##### 前端获取端口示例：
```js
// preload.js
const { contextBridge, ipcRenderer } = require('electron')
contextBridge.exposeInMainWorld('electronAPI', {
  getBackendPort: () => ipcRenderer.invoke('get-backend-port')
})

// 前端页面中
const port = await window.electronAPI.getBackendPort()
fetch(`http://localhost:${port}/api/models`)
```

#### 2.2 注意事项
- 后端需打包为可执行文件或确保用户环境有 Python/uvicorn。
- 前端可用 electron-builder、electron-forge 等工具打包。
- 端口号、路径等可根据实际情况调整。
- 生产环境建议关闭 --reload。

#### 2.3 只打包前端，后端独立部署（可选）
- 适合后端部署在服务器，前端只访问API。
- 用户电脑只运行Electron前端。

### 3. 开发环境建议
- 前后端分开运行，分别用 `uvicorn app.main:app --reload` 和 `npm run dev`。
- 可用 start.sh 或 concurrently 一键启动。

---

## English Guide

### 1. Goal
This project uses Electron + Vue for frontend and FastAPI for backend. After packaging, users only need to run one program, and both frontend and backend will start automatically.

### 2. Recommended Packaging Solution

#### 2.1 Electron Main Process Auto-Starts Backend
- In Electron's main process (main.js/main.ts), use Node.js child_process to start FastAPI backend.
- Users only need to double-click the app, both frontend and backend will start automatically.

##### Example code:
```js
const { app, BrowserWindow, ipcMain } = require('electron')
const { spawn } = require('child_process')
let backendProcess
const backendPort = 8001 // You can set this dynamically

app.on('ready', () => {
  backendProcess = spawn('uvicorn', ['app.main:app', '--host', '127.0.0.1', '--port', backendPort], {
    cwd: 'backend',
    shell: true,
    stdio: 'inherit'
  })

  const win = new BrowserWindow({ width: 1200, height: 800 })
  win.loadURL('http://localhost:5173') // Or the packaged local file

  ipcMain.handle('get-backend-port', () => backendPort)
})

app.on('will-quit', () => {
  if (backendProcess) backendProcess.kill()
})
```

##### Frontend get port example:
```js
// preload.js
const { contextBridge, ipcRenderer } = require('electron')
contextBridge.exposeInMainWorld('electronAPI', {
  getBackendPort: () => ipcRenderer.invoke('get-backend-port')
})

// In frontend page
const port = await window.electronAPI.getBackendPort()
fetch(`http://localhost:${port}/api/models`)
```

#### 2.2 Notes
- Backend should be packaged as executable or ensure Python/uvicorn is available.
- Frontend can be packaged with electron-builder, electron-forge, etc.
- Adjust port, path, etc. as needed.
- In production, do not use --reload.

#### 2.3 Only package frontend, backend deployed separately (optional)
- Suitable for backend deployed on server, frontend only accesses API.
- User's computer only runs Electron frontend.

### 3. Development Suggestion
- Run frontend and backend separately: `uvicorn app.main:app --reload` and `npm run dev`.
- You can use start.sh or concurrently for one-click start.

---
If you need detailed packaging scripts or automation, feel free to ask! 