from fastapi import FastAPI


app = FastAPI(title="Beruška API", version="0.1.0")


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

