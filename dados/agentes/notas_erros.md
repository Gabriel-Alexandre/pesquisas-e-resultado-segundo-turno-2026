# Notas: erro das pesquisas em 2º turnos presidenciais

Levantamento de 26/10/2026, feito para a pergunta: o erro de 2026 no Brasil foi raro? Em 2026, a média das últimas pesquisas de 19 institutos dava Lula 49,19% dos válidos, e a urna deu 51,79%. O erro foi de 2,6 pontos no candidato e a média apontou o vencedor errado.

## Como foi feito

- **Fonte:** as tabelas de pesquisa da Wikipédia (em inglês, e em espanhol onde a inglesa não tem a tabela do 2º turno). Brasil 1989, 2002 e 2006 vêm dos PDFs do próprio Datafolha (links no CSV). Os números estão como na fonte. A vírgula decimal foi trocada por ponto, e o valor não mudou.
- **Quais pesquisas entram:** a última pesquisa de cada instituto que terminou o campo nos 7 dias anteriores à última pesquisa da tabela. Uso a última pesquisa, e não a véspera da eleição, porque vários países proíbem divulgar pesquisa na reta final (Chile 15 dias, Argentina 8, Peru, Colômbia e Equador uma semana). Ficam fora a boca de urna, a contagem rápida e a pesquisa *late poll* feita no dia da eleição.
- **Uma linha por pesquisa.** Quando a fonte traz a mesma pesquisa em votos válidos e em votos totais, uso a de válidos. A coluna `base` diz `validos` quando A + B soma 100 (±0,5) e `totais` quando não soma.
- **Urna (`candidato_x_urna`):**
  - No Brasil, é o % de válidos oficial publicado na fonte.
  - Nos outros países, eu calculei o % dos votos dados aos dois candidatos a partir dos votos que a Wikipédia publica. Não entram branco e nulo.
  - Na Colômbia o voto em branco conta como válido, então o número oficial é menor. Em 2022, por exemplo, o oficial é 50,42 × 47,35.
- **Líder da média (conta minha, fora do CSV):** em cada pesquisa calculei A ÷ (A + B), que é a parte de A entre os dois candidatos. Depois tirei a média simples dessas partes.

## Resultado por eleição

"Erro" é a média das pesquisas menos a urna, para o candidato A, em pontos. A urna é a parte de A nos votos dos dois candidatos.

| Eleição | Pesquisas | Média A (2 cand.) | Urna A | Líder da média | Venceu? | Erro em A |
|---|---|---|---|---|---|---|
| Brasil 1989 (Collor × Lula) | 1 | 51.65 | 53.03 | Collor | sim | -1.38 |
| Brasil 2002 (Lula × Serra) | 1 | 64.00 | 61.27 | Lula | sim | +2.73 |
| Brasil 2006 (Lula × Alckmin) | 1 | 61.00 | 60.83 | Lula | sim | +0.17 |
| Brasil 2010 (Dilma × Serra) | 4 | 56.46 | 56.05 | Dilma | sim | +0.41 |
| Brasil 2014 (Dilma × Aécio) | 4 | 52.17 | 51.64 | Dilma | sim | +0.53 |
| Brasil 2018 (Haddad × Bolsonaro) | 7 | 42.96 | 44.87 | Bolsonaro | sim | -1.91 |
| Brasil 2022 (Bolsonaro × Lula) | 10 | 48.41 | 49.10 | Lula | sim | -0.69 |
| Argentina 2015 (Scioli × Macri) | 6 | 47.06 | 48.66 | Macri | sim | -1.60 |
| Argentina 2023 (Massa × Milei) | 6 | 49.42 | 44.35 | Milei | sim | +5.07 |
| Chile 2013 (Bachelet × Matthei) | 1 | 65.13 | 62.17 | Bachelet | sim | +2.96 |
| Chile 2017 (Guillier × Piñera) | 1 | 45.75 | 45.43 | Piñera | sim | +0.32 |
| Chile 2021 (Boric × Kast) | 1 | 55.00 | 55.87 | Boric | sim | -0.87 |
| Chile 2025 (Jara × Kast) | 3 | 41.84 | 41.83 | Kast | sim | +0.01 |
| Colômbia 2014 (Santos × Zuluaga) | 4 | 50.19 | 53.13 | Santos | sim | -2.94 |
| Colômbia 2018 (Petro × Duque) | 8 | 42.94 | 43.61 | Duque | sim | -0.67 |
| Colômbia 2022 (Petro × Hernández) | 6 | 50.42 | 51.57 | Petro | sim | -1.15 |
| Colômbia 2026 (Cepeda × De la Espriella) | 3 | 46.63 | 49.51 | De la Espriella | sim | -2.88 |
| **Peru 2016 (Kuczynski × Fujimori)** | 4 | 49.45 | 50.12 | Fujimori | **não** | -0.67 |
| **Peru 2021 (Castillo × Fujimori)** | 3 | 49.14 | 50.13 | Fujimori | **não** | -0.99 |
| Peru 2026 (Fujimori × Sánchez) | 3 | 50.73 | 50.13 | Fujimori | sim | +0.60 |
| Equador 2017 (Moreno × Lasso) | 6 | 53.54 | 51.16 | Moreno | sim | +2.38 |
| **Equador 2021 (Arauz × Lasso)** | 8 | 50.48 | 47.64 | Arauz | **não** | +2.84 |
| Equador 2023 (Noboa × González) | 5 | 50.54 | 51.83 | Noboa | sim | -1.29 |
| **Equador 2025 (Noboa × González)** | 7 | 49.14 | 55.63 | González | **não** | -6.49 |
| Uruguai 2014 (Vázquez × Lacalle Pou) | 5 | 56.78 | 56.50 | Vázquez | sim | +0.28 |
| Uruguai 2019 (Martínez × Lacalle Pou) | 5 | 45.91 | 49.21 | Lacalle Pou | sim | -3.30 |
| Uruguai 2024 (Orsi × Delgado) | 6 | 51.04 | 52.00 | Orsi | sim | -0.96 |
| Guatemala 2019 (Giammattei × Torres) | 2 | 57.99 | 57.95 | Giammattei | sim | +0.04 |
| Guatemala 2023 (Arévalo × Torres) | 2 | 62.95 | 60.91 | Arévalo | sim | +2.04 |
| França 2017 (Macron × Le Pen) | 8 | 61.62 | 66.10 | Macron | sim | -4.47 |
| França 2022 (Macron × Le Pen) | 11 | 55.23 | 58.55 | Macron | sim | -3.32 |
| Polônia 2015 (Komorowski × Duda) | 3 | 48.82 | 48.45 | Duda | sim | +0.37 |
| Polônia 2020 (Duda × Trzaskowski) | 9 | 50.20 | 51.03 | Duda | sim | -0.83 |
| **Polônia 2025 (Nawrocki × Trzaskowski)** | 9 | 49.83 | 50.89 | Trzaskowski | **não** | -1.06 |
| **Romênia 2014 (Ponta × Iohannis)** | 2 | 54.50 | 45.57 | Ponta | **não** | +8.93 |
| Romênia 2019 (Iohannis × Dăncilă) | 1 | 66.00 | 66.09 | Iohannis | sim | -0.09 |
| **Romênia 2025 (Dan × Simion)** | 5 | 49.83 | 53.60 | Simion | **não** | -3.77 |
| Portugal 2026 (Seguro × Ventura) | 3 | 67.71 | 66.84 | Seguro | sim | +0.87 |
| Eslováquia 2019 (Šefčovič × Čaputová) | 1 | 44.80 | 41.59 | Čaputová | sim | +3.21 |
| **Eslováquia 2024 (Pellegrini × Korčok)** | 5 | 49.02 | 53.12 | Korčok | **não** | -4.10 |
| **Bolívia 2025 (Quiroga × Paz)** | 3 | 54.27 | 45.04 | Quiroga | **não** | +9.23 |
| Costa Rica 2022 (Chaves × Figueres) | 4 | 54.33 | 52.82 | Chaves | sim | +1.51 |

**Total: 42 eleições e 187 pesquisas. Em 9 das 42 eleições, o líder da média perdeu** (21%): Peru 2016, Peru 2021, Equador 2021, Equador 2025, Polônia 2025, Romênia 2014, Romênia 2025, Eslováquia 2024 e Bolívia 2025. No Brasil, de 1989 a 2022, o líder da média venceu as 7, e o maior erro foi o de 2002 (2,73).

Erro de pelo menos 2,6 pontos no candidato, na média: 15 das 42 eleições (Brasil 2002, Argentina 2023, Chile 2013, Colômbia 2014, Colômbia 2026, Equador 2021, Equador 2025, Uruguai 2019, França 2017, França 2022, Romênia 2014, Romênia 2025, Eslováquia 2019, Eslováquia 2024 e Bolívia 2025). A mediana do erro absoluto nas 42 é de 1,3 ponto (1,335).

## Dúvidas e limites

- **Brasil 2002 e 2006:** só entrou o Datafolha. A tabela do 2º turno não existe na Wikipédia, e a busca não achou a última Ibope nem a última Vox Populi com número e data. Brasil 1989 também tem só o Datafolha. O PDF tem a pesquisa de 16/12/1989 (47 × 44, totais).
- **Peru 2021 depende da regra:**
  - Pela regra dos 7 dias, entram Ipsos (5/6), IEP (2 a 4/6) e IDICE (28 e 29/5). As três estão em intenção de voto total, e a média dá Fujimori na frente.
  - Os simulacros em válidos de 25 a 28/5 davam Castillo na frente em três de quatro (Ipsos, CPI e Datum), mas ficam fora da janela.
  - A pesquisa Ipsos de 5/6 e a IEP de 2 a 4/6 foram feitas durante a proibição de divulgar no Peru.
- **Peru 2016:** a Ipsos e a GfK de 4/6, feitas na proibição, já davam Kuczynski na frente. As últimas divulgadas antes dela (Datum e CPI, até 1/6) davam Fujimori, e a média das quatro fica com Fujimori.
- **Chile 2017 e 2021:** sobra só a Cadem feita na proibição (13 a 15/12/2017 e 15 e 16/12/2021). Nas pesquisas anteriores à proibição, o líder é o mesmo (Piñera e Boric).
- **Ficaram de fora:**
  - Eslováquia 2019: só a Focus de 28 e 29/3.
  - Romênia 2019: só a pesquisa do PSD de 11/11 (é do partido).
  - Chile 2013: só a Ipsos-Usach.
  - Equador 2023: uma linha de 12/10 sem nome de instituto.
  - Uruguai 2014: Interconsult e Factum, que publicaram faixas (53% a 55%).
  - Uruguai 2024: Data 360, que não tem data de campo.
- **Eleições pedidas que não entraram:**
  - Guatemala 2015 e Costa Rica 2018: as páginas não têm tabela de pesquisas do 2º turno.
  - Colômbia 2010: a tabela só traz pesquisas anteriores ao 1º turno.
  - Peru 2011: não há tabela.
- **CMS no Equador 2017:** a fonte escreve 36,76% e 35,86% com vírgula. No CSV estão com ponto.
- **Nenhum número de pesquisa foi recalculado.** As contas que eu fiz são só a parte de cada candidato nos votos da urna (fora do Brasil) e as médias desta nota.
