from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import TasksBlocks, Tasks
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select, col

@asynccontextmanager
async def initFunction(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI()

arquivo_sqlite = "Tarefas.db"
url_sqlite = f"sqlite:///{arquivo_sqlite}"

engine = create_engine(url_sqlite)

app.mount("/src", StaticFiles(directory="src"), name="src")
templates = Jinja2Templates(directory=["templates", "templates/part"])

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()

# Obter todos os blocos de tarefas
def blocos_de_tarefas():
    with Session(engine) as session:
        query = select(TasksBlocks)
        blocos = session.exec(query).all()
        return blocos
    
# Obter um bloco de tarefas específico
def bloco_de_tarefa(block_id: int):
    with Session(engine) as session:
        query = select(TasksBlocks).where(TasksBlocks.id == block_id)
        bloco = session.exec(query).first()
        return bloco

# Obter tarefas de um bloco específico
def tarefas_do_bloco(block_id: int):
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.block_id == block_id)
        tarefas = session.exec(query).all()
    return tarefas

# Obter tarefa específica de um bloco específico
def tarefa_do_bloco(block_id: int, task_id: int):
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.block_id == block_id, Tasks.id == task_id)
        tarefa = session.exec(query).first()
    return tarefa

# Criar um novo bloco de tarefas
@app.post("/blocos", response_class=HTMLResponse)
async def criar_bloco(request: Request):
    with Session(engine) as session:
        bloco = TasksBlocks(title=None, cover=None, icon=None)
        session.add(bloco)
        session.commit()
        session.refresh(bloco)
    return templates.TemplateResponse(request, "blocks.html", {"blocos": blocos_de_tarefas()})

# Modal para editar um bloco de tarefas
@app.get("/blocos/{block_id}/editar", response_class=HTMLResponse)
def modal_editar_bloco(request: Request, block_id: int):
    with Session(engine) as session:
        query = select(TasksBlocks).where(TasksBlocks.id == block_id)
        bloco = session.exec(query).first()
    return templates.TemplateResponse(request, "edit_block.html", {"bloco": bloco})

# Salvar as alterações de um bloco de tarefas
@app.put("/blocos/{block_id}", response_class=HTMLResponse)
def salvar_bloco(request: Request, block_id: int, title: str = Form(...), icon: str = Form(None), cover: str = Form(None)):
    with Session(engine) as session:
        query = select(TasksBlocks).where(TasksBlocks.id == block_id)
        bloco = session.exec(query).first()
        if bloco:
            bloco.title = title
            bloco.icon = icon
            bloco.cover = cover
            session.commit()
            session.refresh(bloco)
    return templates.TemplateResponse(request, "blocks.html", {"blocos": blocos_de_tarefas()})

# Obter todos os blocos de tarefas
@app.get("/blocos", response_class=HTMLResponse)
def lista_de_blocos(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(request, "index.html", {"bloco": None, "tarefas": []})
    return templates.TemplateResponse(request, "blocks.html", {"blocos": blocos_de_tarefas()})

# Deletar um bloco de tarefas
@app.delete("/blocos/{block_id}", response_class=HTMLResponse)
def deletar_bloco(request: Request, block_id: int):
    with Session(engine) as session:
        bloco = bloco_de_tarefa(block_id)
        if bloco:
            tarefas = tarefas_do_bloco(block_id)
            for tarefa in tarefas:
                session.delete(tarefa)
            session.delete(bloco)
            session.commit()
    return templates.TemplateResponse(request, "blocks.html", {"blocos": blocos_de_tarefas()})

# Obter tarefas de um bloco específico
@app.get("/blocos/{block_id}", response_class=HTMLResponse)
def obter_tarefas_do_bloco(request: Request, block_id: int):
    bloco = bloco_de_tarefa(block_id)
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(request, "index.html", { "titulo": bloco.title if bloco else "Meus blocos de tarefas", "bloco": bloco, "tarefas": tarefas_do_bloco(block_id) if bloco else []}, )   
    return templates.TemplateResponse( request, "tasks.html", { "titulo": bloco.title if bloco else "Meus blocos de tarefas", "tarefas": tarefas_do_bloco(block_id), "bloco": bloco_de_tarefa(block_id) })
    
# Criar uma nova tarefa em um bloco específico
@app.post("/blocos/{block_id}/tarefa", response_class=HTMLResponse)
def criar_tarefa(request: Request, block_id: int):
    with Session(engine) as session:
        tarefa = Tasks(title=None, block_id=block_id)
        session.add(tarefa)
        session.commit()
        session.refresh(tarefa)
    return templates.TemplateResponse(request, "card.html", {"tarefas": tarefas_do_bloco(block_id), "bloco": bloco_de_tarefa(block_id)})

# Modal para editar uma tarefa de um bloco específico
@app.get("/blocos/{block_id}/tarefas/{task_id}/editar", response_class=HTMLResponse)
def modal_editar_tarefa(request: Request, block_id: int, task_id: int):
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.id == task_id)
        tarefa = session.exec(query).first()
    return templates.TemplateResponse(request, "edit_task.html", {"tarefa": tarefa})

# Salvar as alterações de uma tarefa de um bloco específico
@app.put("/blocos/{block_id}/tarefas/{task_id}", response_class=HTMLResponse)
def salvar_tarefa(request: Request, block_id: int, task_id: int, title: str = Form(...), description: str = Form(None)):
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.id == task_id)
        tarefa = session.exec(query).first()
        if tarefa:
            tarefa.title = title
            tarefa.description = description
            session.commit()
            session.refresh(tarefa)
    return templates.TemplateResponse(request, "card.html", {"tarefas": tarefas_do_bloco(block_id), "bloco": bloco_de_tarefa(block_id)})


# Deletar uma tarefa de um bloco específico
@app.delete("/blocos/{block_id}/tarefas/{task_id}", response_class=HTMLResponse)
def deletar_tarefa(request: Request, block_id: int, task_id: int):
    with Session(engine) as session:
        tarefa = tarefa_do_bloco(block_id, task_id)
        if tarefa:
            session.delete(tarefa)
            session.commit()
    return templates.TemplateResponse(request, "card.html", {"tarefas": tarefas_do_bloco(block_id), "bloco": bloco_de_tarefa(block_id)})

# Marcar/desmarcar tarefa como finalizada
@app.put("/blocos/{block_id}/tarefas/{task_id}/alternar", response_class=HTMLResponse)
def alternar_tarefa(request: Request, block_id: int, task_id: int):
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.block_id == block_id, Tasks.id == task_id)
        tarefa = session.exec(query).first()
        if tarefa:
            tarefa.completed = not tarefa.completed
            session.add(tarefa)
            session.commit()
    return templates.TemplateResponse(request, "card.html", {"tarefas": tarefas_do_bloco(block_id), "bloco": bloco_de_tarefa(block_id)})

# Pesquisar blocos por título
def pesquisar_blocos(pesquisa):
    with Session(engine) as session:
        query = select(TasksBlocks).where(col(TasksBlocks.title).contains(pesquisa)).order_by(TasksBlocks.title)
        return session.exec(query).all()

@app.get("/pesquisar", response_class=HTMLResponse)
def pesquisar_bloco(request: Request, pesquisa: str | None=''):
    blocos = pesquisar_blocos(pesquisa)
    return templates.TemplateResponse(request, "blocks.html", {"blocos": blocos})

# Retorna a quantidade de blocos, tarefas e tarefas concluídas
@app.get("/info", response_class=HTMLResponse)
def info(request: Request):
    with Session(engine) as session:
        total_blocos = len(session.exec(select(TasksBlocks)).all())
        total_tarefas = len(session.exec(select(Tasks)).all())
        tarefas_concluidas = len(session.exec(select(Tasks).where(Tasks.completed == True)).all())
    return templates.TemplateResponse(request, "info.html", {"total_blocos": total_blocos, "total_tarefas": total_tarefas, "tarefas_concluidas": tarefas_concluidas})

# Página inicial
@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse(request, "index.html", {"tarefas": [], "bloco": None})