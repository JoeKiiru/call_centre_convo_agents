from fastapi import FastAPI
from src.api.routes import router
from src.services import ml_service

# Small FastAPI app used for demonstration and portfolio purposes.
app = FastAPI(title="Conversation Agents")

app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    # Pre-load a default sentiment model so first requests are faster.
    print("Pre-loading ML models...")
    ml_service.load_model(
        "sentiment-analysis", "cardiffnlp/twitter-roberta-base-sentiment-latest"
    )


@app.get("/health")
def health_check():
    # Simple health endpoint used by CI or demo scripts.
    return {"status": "healthy", "service": "conversation-agents"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
