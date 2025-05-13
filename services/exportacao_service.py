import requests
import os
from fastapi import HTTPException
from utils.exportacao_parser import parse_exportacao

CATEGORIAS_EXPORTACAO = {
    "vinhos_de_mesa": "subopt_01",
    "espumantes": "subopt_02",
    "uvas_frescas": "subopt_03",
    "suco_de_uva": "subopt_04"
}

CACHE_DIR = "cache"

def obter_html_exportacao(ano: int, categoria: str):
    if categoria not in CATEGORIAS_EXPORTACAO:
        raise HTTPException(status_code=400, detail="Categoria inválida. Escolha entre: vinhos_de_mesa, espumantes, uvas_frescas, suco_de_uva.")

    subopcao = CATEGORIAS_EXPORTACAO[categoria]
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&subopcao={subopcao}&opcao=opt_06"
    cache_path = os.path.join(CACHE_DIR, f"exportacao_{categoria}_{ano}.html")

    os.makedirs(CACHE_DIR, exist_ok=True)

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        html = response.text

        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(html)

        return html

    except Exception:
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise HTTPException(status_code=503, detail="Erro ao acessar site e cache de exportação.")

def obter_dados_exportacao(ano: int, categoria: str):
    html = obter_html_exportacao(ano, categoria)
    dados = parse_exportacao(html)

    if not dados:
        raise HTTPException(status_code=404, detail=f"Não há dados de exportação para {categoria} no ano {ano}.")

    return dados