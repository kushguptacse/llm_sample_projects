from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from web_url_summary import summarize_url

app = FastAPI(title="AI Website Summarizer")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class SummaryRequest(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/summarize")
async def summarize(data: SummaryRequest):
    if not data.url:
        raise HTTPException(status_code=400, detail="URL is required")
        
    summary = summarize_url(data.url)
    
    if summary.startswith("Error:"):
        raise HTTPException(status_code=500, detail=summary)
        
    return {"summary": summary}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
