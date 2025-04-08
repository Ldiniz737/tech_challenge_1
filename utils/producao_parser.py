# IMPORTA O BEAUTIFULSOUP PARA FAZER O PARSE DO HTML
from bs4 import BeautifulSoup

# IMPORTA A EXCEÇÃO HTTP PARA LANÇAR ERROS COM STATUS
from fastapi import HTTPException


def parse_producao(html: str):
    # CONVERTE O HTML EM OBJETO DE PARSE
    soup = BeautifulSoup(html, "html.parser")

    # LOCALIZA A TABELA QUE CONTÉM OS DADOS
    tabela = soup.find("table", class_="tb_base tb_dados")
    linhas = tabela.find_all("tr")

    dados = []
    produto_atual = None

    # PERCORRE TODAS AS LINHAS DA TABELA
    for linha in linhas:
        colunas = linha.find_all("td")
        if len(colunas) != 2:
            continue

        nome = colunas[0].get_text(strip=True)
        qtd = colunas[1].get_text(strip=True)

        # IDENTIFICA PRODUTOS PRINCIPAIS
        if 'tb_item' in colunas[0].get('class', []):
            produto_atual = {
                "PRODUTO": nome,
                "QTD (L)": qtd,
                "SUBPRODUTO": []
            }
            dados.append(produto_atual)

        # IDENTIFICA SUBPRODUTOS RELACIONADOS AO ÚLTIMO PRODUTO PRINCIPAL
        elif 'tb_subitem' in colunas[0].get('class', []) and produto_atual:
            produto_atual["SUBPRODUTO"].append({
                "PRODUTO": nome,
                "QTD (L)": qtd
            })

    # VERIFICA SE TODOS OS DADOS ESTÃO VAZIOS (COM "-")
    todos_vazios = all(
        item["QTD (L)"] == "-" and
        all(sub["QTD (L)"] == "-" for sub in item["SUBPRODUTO"])
        for item in dados
    )

    # SE TODOS OS VALORES ESTÃO VAZIOS, RETORNA ERRO 404
    if todos_vazios:
        raise HTTPException(
            status_code=404,
            detail="Não há dados de produção disponíveis para o ano informado."
        )

    # BUSCA O VALOR TOTAL NO RODAPÉ (TFOOT) DA TABELA
    tfoot = tabela.find("tfoot")
    if tfoot:
        total_row = tfoot.find("tr")
        total_cols = total_row.find_all("td")
        if len(total_cols) == 2:
            total_valor = total_cols[1].get_text(strip=True)
            # ADICIONA O TOTAL NO FINAL DA LISTA
            dados.append({
                "TOTAL": total_valor
            })

    return dados

