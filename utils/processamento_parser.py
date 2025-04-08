# IMPORTA O BEAUTIFULSOUP PARA FAZER O PARSE DO HTML
from bs4 import BeautifulSoup

# IMPORTA A EXCEÇÃO HTTP PARA LANÇAR ERROS COM STATUS
from fastapi import HTTPException

def parse_processamento(html: str) -> list:
    # CONVERTE O HTML EM OBJETO DE PARSE
    soup = BeautifulSoup(html, "html.parser")

    # LOCALIZA A TABELA QUE CONTÉM OS DADOS
    tabela = soup.find("table", class_="tb_base tb_dados")

    if not tabela:
        raise HTTPException(status_code=404, detail="Tabela de dados não encontrada.")

    resultado = []
    categoria_atual = None
    subprodutos = []

    for row in tabela.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) != 2:
            continue
        # IDENTIFICA UM PRODUTO PRINCIPAL
        nome = cols[0].get_text(strip=True)
        quantidade = cols[1].get_text(strip=True)
        classes = cols[0].get("class", [])
        # SALVA PRODUTO ANTERIOR (SE HOUVER)
        if "tb_item" in classes:
            if categoria_atual:
                resultado.append({
                    "PRODUTO": categoria_atual,
                    "QTD (Kg)": categoria_qtd,
                    "SUBPRODUTO": subprodutos
                })
            # INICIA UM NOVO PRODUTO PRINCIPAL
            categoria_atual = nome
            categoria_qtd = quantidade
            subprodutos = []
        # IDENTIFICA UM SUBPRODUTO (DENTRO DE UM PRODUTO PRINCIPAL)
        elif "tb_subitem" in classes and categoria_atual:
            subprodutos.append({
                "PRODUTO": nome,
                "QTD (Kg)": quantidade
            })

    # ADICIONA O ÚLTIMO PRODUTO
    if categoria_atual:
        resultado.append({
            "PRODUTO": categoria_atual,
            "QTD (Kg)": categoria_qtd,
            "SUBPRODUTO": subprodutos
        })

    # VERIFICA SE TODOS OS DADOS ESTÃO VAZIOS (COM "-")
    todos_vazios = all(
        item["QTD (Kg)"] == "-" and
        all(sub["QTD (Kg)"] == "-" for sub in item["SUBPRODUTO"])
        for item in resultado
    )

    if todos_vazios:
        raise HTTPException(
            status_code=404,
            detail="Não há dados de processamento disponíveis para o ano informado."
        )

    # CAPTURA O VALOR TOTAL DO <TFOOT>
    tfoot = tabela.find("tfoot", class_="tb_total")
    if tfoot:
        total_row = tfoot.find("tr")
        total_cols = total_row.find_all("td")
        if len(total_cols) == 2:
            total_valor = total_cols[1].get_text(strip=True)
            resultado.append({
                "TOTAL": total_valor
            })

    return resultado
