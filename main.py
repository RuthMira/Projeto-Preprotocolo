from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.params import Form
from fastapi import FastAPI, Request
import uuid
import uvicorn
import json
import os

sessoes = {}

# gera uma nova sessão e retorna o id
def gerar_sessao():
    nova_sessao = {}
    nova_sessao["id"] = str(uuid.uuid4())
    nova_sessao["modelo"] = gerar_modelo_inicial()
    nova_sessao ["pesquisa_satisfacao"] = criar_nova_pesquisa_satisfacao()
    sessoes[nova_sessao["id"]] = nova_sessao
    return nova_sessao["id"]

def gerar_modelo_inicial():
    modelo = {}
    modelo["apresentante_nome"] = ""
    modelo["recibo_nome"] = ""
    modelo["recibo_nf_cpf_cnpj"] = ""
    modelo["boleto_nome"] = ""
    modelo["boleto_cpf_cnpj"] = ""
    modelo["boleto_chave_pix"] = ""
    modelo["boleto_tipo_chave"] = ""
    modelo["contato_nome"] = ""
    modelo["contato_telefone"] = ""
    modelo["contato_celular"] = ""
    modelo["contato_email"] = ""
    modelo["endereco_logradouro"] = ""
    modelo["endereco_numero"] = ""
    modelo["endereco_cep"] = ""
    modelo["endereco_complemento"] = ""
    modelo["endereco_via"] = ""
    modelo["endereco_bairro"] = ""
    modelo["endereco_cidade"] = ""
    modelo["endereco_estado"] = ""
    modelo["documento_tipo_natureza"] = ""
    modelo["documento_data_titulo"] = ""
    modelo["documento_emissor_titulo"] = ""
    modelo["documento_processo"] = ""
    modelo["documento_certidao"] = ""
    modelo["documento_livro"] = ""
    modelo["documento_folha"] = ""
    modelo["coaf_nome"] = ""
    modelo["coaf_servidor"] = ""
    modelo["coaf_obrigada"] = ""
    modelo["coaf_politica"] = ""
    modelo["coaf_beneficiario_nome_1"] = ""
    modelo["coaf_beneficiario_cpf_1"] = ""
    modelo["coaf_beneficiario_nome_2"] = ""
    modelo["coaf_beneficiario_cpf_2"] = ""
    modelo["coaf_nao_aplica"] = ""
    modelo["coaf_recusar"] = ""
    modelo["veracidade"] = ""
    return modelo

def criar_nova_pesquisa_satisfacao():
    nova_pesquisa_satisfacao = {}
    nova_pesquisa_satisfacao["facilidade"] = ""
    nova_pesquisa_satisfacao["clareza"] = ""
    nova_pesquisa_satisfacao["tempo"] = ""
    nova_pesquisa_satisfacao["comentario"] = ""
    nova_pesquisa_satisfacao["coaf"] = ""
    nova_pesquisa_satisfacao["form_utilizar_novamente"] = ""
    return nova_pesquisa_satisfacao

def apagar_sessao(id):
    if id in sessoes.keys():
        sessoes.pop(id)

def obter_modelo(id):
    return sessoes[id]["modelo"]

def obter_pesquisa_satisfacao(id):
    return sessoes[id]["pesquisa_satisfacao"]

app = FastAPI()

# Monta o diretório "Static" para servir arquivos estáticos
app.mount("/Static", StaticFiles(directory="Static"), name="Static")

# Configura o diretório de templates Jinja2
templates = Jinja2Templates(directory="Templates") 

# Rota para a Index, template principal via método GET
@app.get("/", response_class=HTMLResponse)
async def getIndexPage(request: Request):
    response = templates.TemplateResponse(request=request, name="index.html", context={"request":request,"metodo":"get","rota":"/tela_inicial"})
    response.delete_cookie("session_id")
    return response

# Rota para a Index, template principal via método GET
#### verificar se está em uso!
@app.post("/", response_class=HTMLResponse)
async def postIndexPage(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request":request})

# Rota para o modal da Tela Inicial via método GET
@app.get("/tela_inicial", response_class=HTMLResponse)
async def getModal(request: Request):
    return templates.TemplateResponse(request=request, name="/Components/tela_inicial.html", context={"request": request})

# Rota para o modal da Política de Privacidade via método GET
@app.get("/politica_privacidade", response_class=HTMLResponse)
async def getModal(request: Request):
    response = templates.TemplateResponse(request=request, name="/Components/politica_privacidade.html", context={"request": request})
    return response

# Rota para a Index_header, template do PreProtocolo via método POST
@app.post("/index_header", response_class=HTMLResponse)
async def postIndexHeadar(request: Request):
    paginacao = []
    paginacao.append({"nome":"Apresentante","rota":"/dados_apresentante"})
    paginacao.append({"nome":"Recibo","rota":"/dados_recibo"})
    paginacao.append({"nome":"Boleto","rota":"/dados_boleto"})
    paginacao.append({"nome":"Endereço","rota":"/dados_endereco"})
    paginacao.append({"nome":"Contato","rota":"/dados_contato"})
    paginacao.append({"nome":"Documento","rota":"/dados_documento"})
    paginacao.append({"nome":"Questionário COAF","rota":"/dados_questionario"})
    paginacao.append({"nome":"Pesquisa de Satisfação","rota":"/pesquisa_satisfacao"})
    
    resposta = templates.TemplateResponse(request=request, name="/index.html", context={"request":request,"metodo":"post","rota":"/dados_apresentante","paginacao":paginacao})
    session_id = gerar_sessao()
    resposta.set_cookie("session_id", session_id)
    return resposta

# Rota para a página "dados_apresentante" via método POST 
@app.post("/dados_apresentante", response_class=HTMLResponse)
async def postApresentante(request: Request):
    session_id = request.cookies.get("session_id") # já foi definido na rota /index_header
    if session_id: # se o cookie existir, ele carrega o div
        response = templates.TemplateResponse(request=request, name="/Components/dados_apresentante.html", context={"request":request})
        response.set_cookie(key="session_id", value=session_id)
        return response

# Rota para a página "dados_recibo" via método POST 
@app.post("/dados_recibo", response_class=HTMLResponse)
async def postRecibo(request: Request, apresentante_nome:str = Form(None)):
    session_id = request.cookies.get("session_id")
    if session_id:
        modelo = obter_modelo(session_id)
        print(apresentante_nome) # para testar o preenchimento
        modelo["apresentante_nome"] = apresentante_nome 
        response = templates.TemplateResponse(request=request, name="/Components/dados_recibo.html", context={"request":request})
        response.set_cookie(key="session_id", value=session_id)
        return response

# Rota para a página "/dados_boleto" via método POST 
@app.post("/dados_boleto", response_class=HTMLResponse)
async def getBoleto(request: Request, recibo_nome:str = Form(None), recibo_nf_cpf_cnpj:str = Form(None)):
    session_id = request.cookies.get("session_id")
    if session_id:
        modelo = obter_modelo(session_id)
        modelo["recibo_nome"] = recibo_nome
        modelo["recibo_nf_cpf_cnpj"] = recibo_nf_cpf_cnpj
        response = templates.TemplateResponse(request=request, name="/Components/dados_boleto.html", context={"request":request})
        response.set_cookie(key="session_id", value=session_id)
        return response

# Rota para a página "/dados_endereco" via método GET 
@app.post("/dados_endereco", response_class=HTMLResponse)
async def getEndereco(request: Request,boleto_nome: str = Form(None), boleto_cpf_cnpj : str = Form(None), boleto_chave_pix: str = Form(None), boleto_tipo_chave: str = Form(None)):
    session_id = request.cookies.get("session_id")
    if session_id:
        modelo = obter_modelo(session_id) 
        modelo["boleto_nome"] = boleto_nome 
        modelo["boleto_cpf_cnpj"] = boleto_cpf_cnpj
        modelo["boleto_chave_pix"] = boleto_chave_pix
        modelo["boleto_tipo_chave"] = boleto_tipo_chave
        response = templates.TemplateResponse(request=request, name="/Components/dados_endereco.html", context={"request":request})
        response.set_cookie(key="session_id", value=session_id)
        return response

# Rota para a página "/dados_contato" via método POST 
@app.post("/dados_contato", response_class=HTMLResponse)
async def getContato(request: Request, endereco_logradouro: str = Form(None), endereco_numero: str = Form(None), endereco_cep: str = Form(None), endereco_complemento: str = Form(None), endereco_estado: str = Form(None), endereco_via: str = Form(None), endereco_bairro: str = Form(None), endereco_cidade: str = Form(None)):
    session_id = request.cookies.get("session_id")
    if session_id:
        modelo = obter_modelo(session_id)
        modelo["endereco_logradouro"] = endereco_logradouro
        modelo["endereco_numero"] = endereco_numero
        modelo["endereco_cep"] = endereco_cep
        modelo["endereco_complemento"] = endereco_complemento
        modelo["endereco_via"] = endereco_via
        modelo["endereco_bairro"] = endereco_bairro
        modelo["endereco_cidade"] = endereco_cidade
        modelo["endereco_estado"] = endereco_estado
        response = templates.TemplateResponse(request=request, name="/Components/dados_contato.html", context={"request":request})
        response.set_cookie(key="session_id", value=session_id)
        return response

# Rota para a página "/dados_documento" via método POST 
@app.post("/dados_documento", response_class=HTMLResponse)
async def postDocumento(request: Request, contato_nome : str = Form(None), contato_telefone : str = Form(None), contato_celular : str = Form(None), contato_email : str = Form(None)):
    session_id = request.cookies.get("session_id")
    if session_id:
        modelo = obter_modelo(session_id)
        modelo["contato_nome"] = contato_nome
        modelo["contato_telefone"] = contato_telefone
        modelo["contato_celular"] = contato_celular
        modelo["contato_email"] = contato_email 
        response = templates.TemplateResponse(request=request, name="/Components/dados_documento.html", context={"request":request})
        response.set_cookie(key="session_id", value=session_id)
        return response

# Rota para a página "/dados_questionário" via método POST 
@app.post("/dados_questionario", response_class=HTMLResponse)
async def getQuestiobario(request: Request, documento_tipo_natureza : str = Form(None), documento_data_titulo : str = Form(None), documento_emissor_titulo : str = Form(None), documento_processo : str = Form(None), documento_certidao : str = Form(None), documento_livro : str = Form(None), documento_folha : str = Form(None) ):
    session_id = request.cookies.get("session_id")
    if session_id:
        modelo = obter_modelo(session_id)
        modelo["documento_tipo_natureza"] = documento_tipo_natureza
        modelo["documento_data_titulo"] = documento_data_titulo
        modelo["documento_emissor_titulo"] = documento_emissor_titulo
        modelo["documento_processo"] = documento_processo
        modelo["documento_certidao"] = documento_certidao
        modelo["documento_livro"] = documento_livro
        modelo["documento_folha"] = documento_folha
        response = templates.TemplateResponse(request=request, name="/Components/dados_questionario.html", context={"request":request})
        response.set_cookie(key="session_id", value=session_id)
        return response

# Rota para a página "/pesquisa_satisfação" via método POST 
@app.post("/pesquisa_satisfacao", response_class=HTMLResponse)
async def getPesquisa(request: Request, coaf_nome : str = Form(None), coaf_servidor : str = Form(None), coaf_obrigada : str = Form(None), coaf_politica : str = Form(None), coaf_beneficiario_nome_1 : str = Form(None), coaf_beneficiario_cpf_1 : str = Form(None), coaf_nao_aplica : str = Form(None), coaf_veracidade : str = Form(None), coaf_recusar : str = Form(None) ):
    session_id = request.cookies.get("session_id")
    if session_id:
        modelo = obter_modelo(session_id)
        modelo["coaf_nome"] = coaf_nome
        modelo["coaf_servidor"] = coaf_servidor
        modelo["coaf_obrigada"] = coaf_obrigada
        modelo["coaf_politica"] = coaf_politica
        modelo["coaf_beneficiario_nome_1"] = coaf_beneficiario_nome_1
        modelo["coaf_beneficiario_cpf_1"] = coaf_beneficiario_cpf_1
        modelo["coaf_nao_aplica"] = coaf_nao_aplica
        modelo["coaf_recusar2"] = coaf_recusar
        response = templates.TemplateResponse(request=request, name="/Components/pesquisa_satisfacao.html", context={"request": request})
        response.set_cookie(key="session_id", value=session_id)
        return response  

@app.post("/preprotocolo/cadastrar", response_class=HTMLResponse)
async def cadastrar(request: Request, facilidade : str = Form(None), clareza : str = Form(None), \
    tempo : str = Form(None), comentario : str = Form(None)):
    session_id = request.cookies.get("session_id")
    if session_id in sessoes.keys():
        pesquisa_satisfacao = obter_pesquisa_satisfacao(session_id)
        pesquisa_satisfacao["facilidade"] = facilidade
        pesquisa_satisfacao["clareza"] = clareza
        pesquisa_satisfacao["tempo"] = tempo
        pesquisa_satisfacao["comentario"] = comentario
        pesquisa_satisfacao["coaf"] = ""
        pesquisa_satisfacao["form_utilizar_novamente"] = ""
        salvar_pesquisa_satisfacao(pesquisa_satisfacao)
        #
        modelo = obter_modelo(session_id)
        salvar_modelo(modelo)
        # 
        response = templates.TemplateResponse(request=request, name="index.html", context={"request":request,"metodo":"get","rota":"/tela_inicial"})
        response.delete_cookie("session_id")
        return response 

@app.post("/form_finalizar_cadastro")
async def botaoSalvarFormulario(request: Request, veracidade: str = Form(None)):
    atributo_html_botao = ""
    atributo_html_checkbox = "checked"
    if not veracidade:
        atributo_html_botao = "disabled"
        atributo_html_checkbox = ""
    return templates.TemplateResponse(request=request, name="/Components/form_finalizar_cadastro.html", context={"request":request,"atributo_html_botao":atributo_html_botao, "atributo_html_checkbox":atributo_html_checkbox})

@app.post("/cadastrar", response_class=HTMLResponse)
async def postcadastrar(request: Request, veracidade: str = Form(None)):
    print("\n----------------------------\n")
    print("> Finalizando o cadastro...")
    session_id = request.cookies.get("session_id")
    modelo = obter_modelo(session_id)
    modelo["veracidade"] = veracidade
    print("> Modelo preenchido:")
    print(modelo)
    
    diretorio = os.path.dirname(__file__)
    arquivo = open( diretorio + "/Resultado/cadastro_preenchido.json","w",encoding='utf-8')
    json.dump(modelo, arquivo, indent=4)    

    salvar_modelo(modelo)
    apagar_sessao(session_id)
    response = templates.TemplateResponse(request=request, name="/Components/form_enviar_cadastro.html", context={"request":request})
    response.delete_cookie("session_id")
    return response

@app.post("/form_confirmar_cadastro", response_class=HTMLResponse)
async def postconfirmar1(request: Request):
    response = templates.TemplateResponse(request=request, name="/Components/form_confirmar_cadastro.html", context={"request":request})
    return response

@app.post("/form_confirmar_cadastro_v2", response_class=HTMLResponse)
async def postConfirmar2(request: Request):
    response = templates.TemplateResponse(request=request, name="/Components/toast_mensagem.html", context={"request":request,"titulo":"Olá mundo!","subtitulo":"foo","mensagem":"bar"})
    return response

# response = templates.TemplateResponse(request=request, name="index.html", context={"request":request,"metodo":"get","rota":"/tela_inicial"})
# response.delete_cookie("session_id")

def salvar_modelo(modelo):
    print("> Enviando dados para o servidor de cadastro...")
    # aqui entra a rotina de envio para o servidor de cadastro
    print("> Dados de cadastro enviados com sucesso.")
    print("\n----------------------------\n")

def salvar_pesquisa_satisfacao(modelo):
    print("> Enviando dados para o servidor de pesquisa...")
    # aqui entra a rotina de envio para o servidor de pesquisa
    print("> Dados de cadastro enviados com sucesso.")
    print("\n----------------------------\n")

uvicorn.run(app,host="0.0.0.0")
