import requests
import os
from fastapi import HTTPException
from utils.processamento_parser import parse_processamento

CATEGORIAS = {
    "viniferas": "subopt_01",
    "americanas_hibridas": "subopt_02",
    "uvas_de_mesa": "subopt_03",
    "sem_classificacao": "subopt_04"
}

def obter_html(ano: int, categoria: str):
    if categoria not in CATEGORIAS:
        raise HTTPException(status_code=400, detail="Categoria inválida. Escolha entre: viniferas, americanas_hibridas, uvas_de_mesa, sem_classificacao.")

    subopcao = CATEGORIAS[categoria]
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&subopcao={subopcao}&opcao=opt_03"
    cache_path = f"cache/processamento_{categoria}_{ano}.html"

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        html = response.text

        # Salvar no cache
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(html)

        return html

    except Exception:
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise HTTPException(status_code=503, detail="Erro ao acessar site e cache de processamento.")

def obter_dados_processamento(ano: int, categoria: str):
    html = obter_html(ano, categoria)
    dados = parse_processamento(html)

    if not dados:
        raise HTTPException(status_code=404, detail=f"Não há dados de processamento para {categoria} no ano {ano}.")

    return dados