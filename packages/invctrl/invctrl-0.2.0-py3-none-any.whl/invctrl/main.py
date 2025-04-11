from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from tinydb import TinyDB
from pathlib import Path
from importlib.resources import files
from invctrl.routes import request_order

app = FastAPI()

TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

DB_FILE = Path(__file__).parent / "db" / "request_order.json"
request_db = TinyDB(str(DB_FILE))

@app.get("/dashboard")
def dashboard(request: Request):
    data = request_db.all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "data": data})

@app.post("/request-order")
def handle_form(
    nama_barang: str = Form(...),
    jumlah: int = Form(...),
    nama_toko: str = Form(...)
):
    request_db.insert({
        "nama_barang": nama_barang,
        "jumlah": jumlah,
        "nama_toko": nama_toko
    })
    return RedirectResponse(url="/dashboard", status_code=303)

app.include_router(request_order.router)

def run():
    import uvicorn
    uvicorn.run("invctrl.main:app", host="0.0.0.0", port=8000)
