"""FastAPI后端 - Prompt优化器"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

from core.optimizer import PromptOptimizer

app = FastAPI(title="Prompt优化器", description="自动化Prompt工程优化平台")
optimizer = PromptOptimizer()

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


class OptimizeRequest(BaseModel):
    task: str
    test_cases: List[dict]
    max_iterations: Optional[int] = 2


@app.get("/")
async def index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.post("/optimize")
async def optimize(req: OptimizeRequest):
    result = optimizer.optimize(req.task, req.test_cases, req.max_iterations)
    return {"status": "success", "data": result}

@app.get("/history")
async def history():
    return {"status": "success", "data": optimizer.get_history()}

@app.get("/strategies")
async def strategies():
    return {"status": "success", "data": optimizer.get_strategies()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
