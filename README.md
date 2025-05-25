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