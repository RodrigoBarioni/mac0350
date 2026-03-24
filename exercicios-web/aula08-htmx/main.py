from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory=["templates", "templates/partial"])

curtidas = int(0)

@app.get("/home",response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"pagina": "/home/pagina1"})

@app.get("/home/pagina1", response_class=HTMLResponse)
async def pag1(request: Request):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/pagina1"})
    return templates.TemplateResponse(request, "pagina1.html")

@app.get("/home/pagina2", response_class=HTMLResponse)
async def pag2(request: Request):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/pagina2"})
    return templates.TemplateResponse(request, "pagina2.html")

@app.get("/home/curtidas", response_class=HTMLResponse)
async def pagina_curtidas(request: Request):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/curtidas"})
    return templates.TemplateResponse(request, "curtidas.html", {"curtidas": curtidas})

@app.post("/home/curtir", response_class=HTMLResponse)
async def curtir(request: Request):
    global curtidas
    curtidas += 1
    return str(curtidas)

@app.delete("/home/curtir", response_class=HTMLResponse)
async def limpar_curtidas(request: Request):
    global curtidas
    curtidas = 0
    return str(curtidas)