from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.model_service import fetch_models_from_openrouter

app = FastAPI(
    title="ZeusInbox API",
    description="Backend API for ZeusInbox email assistant",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to ZeusInbox API"}

# Import and include routers
# from app.api import email, auth, mcp
# app.include_router(email.router, prefix="/api/email", tags=["email"])
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# app.include_router(mcp.router, prefix="/api/mcp", tags=["mcp"])
from app.api import model
app.include_router(model.router, prefix="/api", tags=["model"])

fetch_models_from_openrouter()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 