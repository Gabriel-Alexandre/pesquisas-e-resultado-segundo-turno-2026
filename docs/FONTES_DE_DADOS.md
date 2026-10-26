# Fontes de dados

| Dado | Fonte | Onde fica | Como confere |
|---|---|---|---|
| Resultado de presidente, 1º e 2º turno, país, UFs, exterior e cada município | TSE, divulgação oficial (`resultados.tse.jus.br/oficial/ele2026`, eleições 6257 e 6258) | `dados/brutos/tse/` (fora do git; hash de cada arquivo em `dados/MANIFESTO.json`); tabelas em `dados/derivados/` | soma das UFs = país e soma dos municípios = UF, diferença zero |
| Governador, 1º turno (27 UFs) e 2º turno (6 UFs) | TSE, eleições 6259 e 6260, cargo 3 | idem | arquivo final |
| Registro das pesquisas | TSE, `pesquisa_eleitoral_2026.zip` (dados abertos) | `dados/brutos/` (fora do git, hash no manifesto) | casamento por empresa, datas e amostra |
| Lista de pesquisas de 2º turno | Wikipedia (en), *Opinion polling for the 2026 Brazilian presidential election*, seção de outubro (revid no manifesto) | `dados/brutos/capturas/wikipedia-2t-outubro.wikitext` | cada pesquisa conferida no registro do TSE e numa segunda fonte (texto extraído em `dados/brutos/capturas/pesquisas/`; o HTML bruto fica fora do git) |
| Histórico de presidente e governador, 1989 a 2022 | TSE (dados abertos), já baixado e derivado no projeto `investigacao-segundo-turno-2026` | `dados/copias/investigacao-segundo-turno-2026/` | cópia com hash e commit de origem no manifesto |
| Erro das pesquisas por instituto, 2014 a 2026 | projetos `previsao-segundo-turno-2026` e `presidente-primeiro-turno-2026` (pesquisas registradas no TSE) | `dados/copias/` | idem |
| Erro da média das pesquisas em 2º turnos, 2014 a 2022 | Pindograma (pesquisas registradas), derivado em `investigacao-segundo-turno-2026` | `dados/copias/investigacao-segundo-turno-2026/p3_disputas.csv` | idem |
| Polymarket (preço na véspera e mercados de eleição resolvidos) | API pública da Polymarket, coletada em `investigacao-segundo-turno-2026` | `dados/copias/investigacao-segundo-turno-2026/polymarket_*.csv` | idem |
| Abstenção, 2002 a 2022 | TSE, derivado em `previsao-segundo-turno-2026` | `dados/copias/previsao-segundo-turno-2026/abstencao_historica.csv` | idem |
