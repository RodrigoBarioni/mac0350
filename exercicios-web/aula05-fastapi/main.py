from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi import Depends, HTTPException, status, Cookie, Response
from typing import Annotated

app = FastAPI()

class Usuario(BaseModel):
    nome: str
    senha: str
    bio: str

class LoginData(BaseModel):
    nome: str
    senha: str

usuarios_db = []

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
  <script>
    async function enviarUsuario() {
      const dados = {
          nome: document.getElementById('nome').value,
          senha: document.getElementById('senha').value,
          bio: document.getElementById('bio').value
      };

      const resposta = await fetch('/users', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(dados)
      });

      if (resposta.ok) {
          const resultado = await resposta.json();
          alert("Usuário " + resultado.usuario + " criado!");
      } else {
          alert("Erro ao criar usuário!");
      }
    }
  </script>
    <form>
    <input type="text" id="nome" placeholder="Nome">
    <input type="text" id="senha" placeholder="Senha">
    <input type="text" id="bio" placeholder="Bio">
    <button type="button" onclick="enviarUsuario()">Salvar via JS</button>
</form>
    """

@app.post("/users")
def criar_usuario(user: Usuario):
    usuarios_db.append(user.dict())
    return {"usuario": user.nome}

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <script>
      async function logar() {
          const dados = {
              nome: document.getElementById('nome').value,
              senha: document.getElementById('senha').value
          };

          const resposta = await fetch('/login', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(dados)
          });

          if (resposta.ok) {
              const resultado = await resposta.json();
              alert("Usuário " + resultado.usuario + " logou com sucesso!");
              window.location = "/home";
          } else {
              alert("Usuário ou senha inválidos!");
          }
      }
    </script>
    <form>
      <input type="text" id="nome" placeholder="Nome do Usuário">
      <input type="text" id="senha" placeholder="Senha">
      <button type="button" onclick="logar()">Logar</button>
    </form>
    """

@app.post("/login")
def login(dados: LoginData, response: Response):
    usuario_encontrado = None
    for u in usuarios_db:
        if u["nome"] == dados.nome and u["senha"] == dados.senha:
            usuario_encontrado = u
            break
    
    if not usuario_encontrado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    response.set_cookie(key="session_user", value=dados.nome)
    
    return {"message": "Logado com sucesso", "usuario": dados.nome}

def get_active_user(session_user: Annotated[str | None, Cookie()] = None):
    if not session_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acesso negado: você não está logado."
        )
    
    user = next((u for u in usuarios_db if u["nome"] == session_user), None)
    if not user:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    return user

@app.get("/home")
def show_profile(request: Request, user: dict = Depends(get_active_user)):
    return templates.TemplateResponse(
        request=request, 
        name="perfil.html", 
        context={"user": user["nome"], "bio": user["bio"]}
    )