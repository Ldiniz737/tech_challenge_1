from fastapi import FastAPI, HTTPException
from typing import Literal

# IMPORTA AS FUNÇÕES QUE BUSCAM E PROCESSAM OS DADOS
from services.producao_service import obter_dados_producao
from services.comercializacao_service import obter_dados_comercializacao
from services.processamento_service import obter_dados_processamento

# INSTANCIA A APLICAÇÃO FASTAPI
app = FastAPI()

# ENDPOINT DE PRODUÇÃO - ACEITA PARAM ANO, PADRÃO 2023
@app.get("/producao")
def endpoint_producao(ano: int = 2023):
    return obter_dados_producao(ano)

# ENDPOINT DE COMERCIALIZAÇÃO - ACEITA PARAM ANO, PADRÃO 2023
@app.get("/comercializacao")
def endpoint_comercializacao(ano: int = 2023):
    return obter_dados_comercializacao(ano)

# ENDPOINT DE PROCESSAMENTO - ACEITA ANO E CATEGORIA COM VALIDAÇÃO FIXA
@app.get("/processamento")
def endpoint_processamento(
    ano: int = 2023,
    categoria: Literal["viniferas", "americanas_hibridas", "uvas_de_mesa", "sem_classificacao"] = "viniferas"
):
    return obter_dados_processamento(ano, categoria)



