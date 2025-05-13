from bs4 import BeautifulSoup

def parse_exportacao(html: str):
    soup = BeautifulSoup(html, "html.parser")
    tabela = soup.find("table", class_="tb_base tb_dados")
    if not tabela:
        return []

    dados = []
    tbody = tabela.find("tbody")
    if not tbody:
        return []

    for row in tbody.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 3:
            pais = cols[0].text.strip()
            quantidade = cols[1].text.strip().replace(".", "").replace(",", ".")
            valor = cols[2].text.strip().replace(".", "").replace(",", ".")
            dados.append({
                "pais": pais,
                "quantidade_kg": float(quantidade) if quantidade != "-" else None,
                "valor_usd": float(valor) if valor != "-" else None,
            })

    if all(item["quantidade_kg"] is None and item["valor_usd"] is None for item in dados):
        return [] 

    return dados