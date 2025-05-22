# ZeusInbox - AI-Powered Email Assistant

ZeusInbox is a desktop email assistant that combines the power of AI with email management. It helps you manage your emails more efficiently through AI-powered features like automatic summarization, classification, and smart reply suggestions.

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