# Tech Challenge Fase 1 - Welcome to Machine Learning Engineering 

## Visão geral
O presente projeto foi desenvolvido como atividade da Fase 1 do curso Pós Tech em Machine Learning Engineering.

O objetivo principal é criar uma API pública em Python que consulta e disponibiliza os [dados de vitivinicultura da Embrapa](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01).

## O projeto
A API realiza um web scraping das páginas, obtendo informações de:

* [Produção](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02);
* [Processamento](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03);
* [Comercialização](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04);
* [Importação](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05);
* [Exportação](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06).

Esses dados serão utilizados para alimentar um modelo de Machine Learning, conforme esquema a seguir:

<!-- *imagem_aqui* -->

## Instalação

Para a instalação, comece clonando o repositório em sua máquina:

```
git clone https://github.com/Ldiniz737/tech_challenge_1.git
```

Em seguida, no terminal, crie o ambiente virtual `venv`:

```
python -m venv venv
```

Ative o ambiente virtual:

```
venv/scripts/activate
```

Finalmente, instale os arquivos de `requirements.txt`:

```
pip install -r requirements.txt
```

## Alunos

Izabelly de Oliveira Menezes

Larissa Diniz da Silva 

Rafael Dos Santos Callegari 

Luis Fernando Torres 

Renato Massamitsu Zama Inomata 
