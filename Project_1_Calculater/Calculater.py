from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import math
from pathlib import Path

app = FastAPI(title="Modern Calculator API")

# Mount static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class CalcRequest(BaseModel):
    expression: str


class CalcResponses(BaseModel):
    expression: str
    result: float
    error: str = None


def safe_eval(expression: str) -> float:
    """Safely evaluate mathematical expressions."""
    # Replace common symbols
    expression = expression.replace("÷", "/").replace("×", "*")
    
    # Allowed names for eval
    allowed_names = {
        "abs": abs,
        "pow": pow,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "pi": math.pi,
        "e": math.e,
    }
    
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")


@app.get("/")
async def root():
    """Serve the calculator UI."""
    return FileResponse(str(static_dir / "index.html"), media_type="text/html")


@app.post("/api/calc")
async def calculate(request: CalcRequest) -> CalcResponses:
    """Calculate the result of a mathematical expression."""
    try:
        result = safe_eval(request.expression)
        return CalcResponses(expression=request.expression, result=result)
    except ValueError as e:
        return CalcResponses(expression=request.expression, result=None, error=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)