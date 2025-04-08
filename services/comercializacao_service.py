import requests
import os
from fastapi import HTTPException
from utils.comercializacao_parser import parse_comercializacao

def obter_html(ano: int):
    # URL DO SITE COMERCIALIZAÇÃO (OPCAO 04)
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_04"

    # CAMINHO DO ARQUIVO DE CACHE LOCAL
    cache_path = f"cache/dados_parse_comercializacao_{ano}.html"

    try:
        # TENTA FAZER REQUEST PARA O SITE
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        html = response.text

        # SALVA O HTML NO CACHE LOCAL
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(html)

        return html
    except Exception:
        # CASO ERRO, TENTA USAR O ARQUIVO DE CACHE
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise HTTPException(status_code=503, detail="Erro ao acessar site e cache de comercializacao.")

def obter_dados_comercializacao(ano: int):
    # OBTÉM HTML DO SITE OU CACHE
    html = obter_html(ano)

    # PARSEIA OS DADOS
    dados = parse_comercializacao(html)
    
    # VERIFICA SE EXISTEM DADOS
    if not dados:
        raise HTTPException(status_code=404, detail=f"Não há dados de comercialização para o ano {ano}.")
    
    return dados  # RETORNA OS DADOS FORMATADOS
