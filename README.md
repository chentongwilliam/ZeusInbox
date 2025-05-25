# ZeusInbox - AI-Powered Email Assistant

ZeusInbox is a desktop email assistant that combines the power of AI with email management. It helps you manage your emails more efficiently through AI-powered features like automatic summarization, classification, and smart reply suggestions.

---

**Current Compatibility Notice**

⚠️ **At present, this project is fully adapted and tested only for privateemail.com mailboxes. Other email providers (such as Outlook, Gmail, QQ, 163, etc.) may not work out of the box due to differences in IMAP protocol implementation and authentication methods. Developers need to test and adapt the code as needed for other providers.**

- The dedicated adaptation code for privateemail is implemented in `backend/app/services/email_service.py`, specifically in the `get_privateemail_emails` method and the automatic dispatch logic within the `get_emails` method.
- If you need to support other email providers (such as Outlook, Gmail, etc.), please add provider-specific parsing and authentication logic in the `get_emails` method based on the IMAP server address.
- Important: Outlook/Office365 has now completely disabled IMAP login with username and password. OAuth2.0 authentication is required. See the official Microsoft notice: [Deprecation of Basic authentication in Exchange Online](https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/deprecation-of-basic-authentication-exchange-online). If you need to adapt for Outlook, please refer to the official documentation and implement the OAuth2.0 flow.
- If you encounter compatibility issues with fetch, search, or email content parsing for other providers, please extend `email_service.py` with provider-specific methods similar to the privateemail example.

---

## Features

- 📧 Support for multiple email accounts (IMAP)
- 🤖 AI-powered email management
  - Automatic email summarization
  - Smart classification
  - Reply suggestions
  - Translation
- 🔧 MCP (Model Context Protocol) integration
- 🔒 Local-first approach with data privacy
- 🖥️ Cross-platform support (Windows, Linux, macOS)

## Tech Stack

- Frontend: Vue 3 + Electron
- Backend: FastAPI (Python)
- Database: SQLite
- AI: OpenRouter API (via MCP)
- Email Protocol: IMAP

## Project Structure

```
zeusinbox/
├── frontend/           # Vue 3 + Electron frontend
├── backend/           # FastAPI backend
├── database/          # SQLite database files
└── docs/             # Documentation
```

## Development Setup

### Prerequisites

- Node.js 18+
- Python 3.9+
- Git

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Configuration

1. Email Account Setup
   - Add your email account through the settings page
   - Configure IMAP settings (server, port, credentials)

2. AI Integration
   - Set up your OpenRouter API key
   - Configure MCP Tool Server settings

## Security & Privacy

- All sensitive data is encrypted and stored locally
- No data is sent to external servers except for AI processing
- You can clear all local data at any time

## License

MIT License

## Contributing

Please read our contributing guidelines before submitting pull requests.

## Extending Global Settings

If you want to add new global settings (such as additional preferences, feature toggles, etc.) that should be loaded and managed across the entire application, follow these steps:

### 1. Backend: Add to .env and API
- Add your new setting to the `.env` file (e.g., `NEW_SETTING=value`).
- In `backend/app/api/settings.py`, update the `/api/settings/all` endpoint to include your new setting in the returned dictionary. For example:
  ```python
  return {
      "language": env_vars.get("LANGUAGE", "en"),
      "email_update_interval": env_vars.get("EMAIL_UPDATE_INTERVAL", 5),
      "new_setting": env_vars.get("NEW_SETTING", "default_value")
  }
  ```
- If you need to allow updating this setting from the frontend, add a corresponding API endpoint to save it to `.env`.

### 2. Frontend: Add to Global Settings
- In `frontend/src/main.ts`, add your new setting to the `globalSettings` reactive object:
  ```js
  export const globalSettings = reactive({
    language: 'en',
    emailUpdateInterval: 5,
    newSetting: 'default_value'
  })
  ```
- Update the `loadGlobalSettings` function to read the new setting from the backend response and assign it to `globalSettings`:
  ```js
  if (data.new_setting) {
    globalSettings.newSetting = data.new_setting;
  }
  ```
- Use `globalSettings.newSetting` anywhere in your Vue components to access or display the value.

### 3. Usage in Components
- Import and use `globalSettings` in any component:
  ```js
  import { globalSettings } from '../main'
  // ...
  console.log(globalSettings.newSetting)
  ```
- To update the setting and persist it, call the appropriate backend API and update `globalSettings` accordingly.

### 4. Summary
- All global settings should be loaded once at app startup and managed via the `globalSettings` object.
- This approach ensures consistency and makes it easy to add, update, or use new global settings throughout the app. 