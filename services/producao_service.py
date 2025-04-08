import requests
import os
from fastapi import HTTPException
from utils.producao_parser import parse_producao

def obter_html(ano: int):
    # URL DO SITE DE PRODUÇÃO (OPCAO 02)
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02"

    # CAMINHO DO ARQUIVO DE CACHE
    cache_path = f"cache/dados_producao_{ano}.html"

    try:
        # TENTA OBTER OS DADOS DA INTERNET
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        html = response.text

        # SALVA O HTML NO CACHE LOCAL
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(html)

        return html
    except Exception:
        # CASO OCORRA ERRO, USA O ARQUIVO DE CACHE SE EXISTIR
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise HTTPException(status_code=503, detail="Erro ao acessar site e cache de produção.")

def obter_dados_producao(ano: int):
    # OBTÉM O HTML DE PRODUÇÃO
    html = obter_html(ano)

    # FAZ O PARSE DOS DADOS HTML
    dados = parse_producao(html)
    
    # VERIFICA SE EXISTEM DADOS
    if not dados:
        raise HTTPException(status_code=404, detail=f"Não há dados de produção para o ano {ano}.")
    
    return dados  # RETORNA OS DADOS FORMATADOS
