# Relatório: as pesquisas, as regras e o resultado do 2º turno de 2026

Gerado por `ferramentas/gerar-relatorio.py` a partir de `resultados/RESUMO.json`. Rodada 1 (26/10/2026). Todo número tem a fonte em [`docs/FONTES_DE_DADOS.md`](docs/FONTES_DE_DADOS.md) e o hash do arquivo de origem em `dados/MANIFESTO.json`.

## O que este relatório não consegue dizer

- **O voto é secreto.** "Para onde foram os votos do Cury, do Renan e do Caiado" é uma **estimativa** feita com o resultado de 5.571 municípios (inferência ecológica). Ela mostra o que é compatível com os números de cada lugar, não o caminho de cada eleitor, e tem faixa de incerteza larga (§6).
- **Probabilidade de algo que já aconteceu** é a chance que os números davam **antes** da votação. Uma chance de 1 em 3 ou de 1 em 9 não diz se o resultado é legítimo ou não: diz o tamanho da surpresa.
- **A apuração seção a seção, a pausa da noite e os registros das urnas** não são analisados aqui. Isso é o projeto do vídeo longo 16 (`investigacao-segundo-turno-2026`). Este projeto usa o resultado oficial final por país, estado e município.
- **Governador e presidente** foram comparados pela **coligação** do governador eleito (tem o PT, tem o PL, ou nenhum dos dois), que é uma regra mecânica. Apoio declarado no 2º turno não foi levantado nesta rodada.

## 1. O resultado, em números

| | 1º turno (04/10) | 2º turno (25/10) | Diferença |
|---|---|---|---|
| Lula | 53.879.538 (45,16%) | 64.256.232 (**51,79%**) | **+10.376.694** |
| Flávio | 56.104.503 (47,03%) | 59.826.041 (48,21%) | **+3.721.538** |
| Outros candidatos | 9.316.747 | 0 | -9.316.747 |
| Abstenção | 33.469.244 (21,08%) | 30.509.005 (19,22%) | -2.960.239 |
| Brancos e nulos | 5.975.047 | 4.153.801 | -1.821.246 |

**A conta fecha no voto.** O que os dois ganharam juntos (14.098.232) é exatamente o que saiu dos outros candidatos (9.316.747), da abstenção (2.960.239) e do branco e nulo (1.821.246). O Lula ficou com 73,6% desse saldo. A frente do Flávio no 1º turno era de 2.224.965 votos; a do Lula no 2º ficou em 4.430.191. A virada foi de 6,66 milhões de votos de diferença.

Se todo voto novo (quem voltou a votar e quem deixou o branco e o nulo) tivesse ido para o Lula, ele ainda precisaria de **60,1%** dos votos dos outros candidatos. Ou seja: sem troca direta de voto do Flávio para o Lula, a maioria dos eleitores de Cury, Renan e Caiado votou Lula.

## 2. As pesquisas contra a urna

Foram usadas as **53 pesquisas nacionais de 2º turno** de 05/10 a 24/10 que casaram com o registro no TSE **e** foram conferidas numa segunda fonte (lista em `resultados/pesquisas_2t.csv`, com o número do registro). Ficou fora da conta: Alfa de 22/10 (a amostra publicada não bate com a do registro).

| Conjunto | Pesquisas | Lula na média | Erro médio no Lula | Davam Flávio | Davam Lula | A urna ficou dentro da margem |
|---|---|---|---|---|---|---|
| Todas | 53 | 48,91% | -2,9 | 48 | 4 (+1 empate) | 13 |
| Última semana | 31 | 49,08% | -2,7 | 29 | 2 | 7 |
| Véspera (campo até 23 e 24/10) | 12 | 49,33% | -2,5 | 11 | 1 | 3 |
| **Última de cada instituto** | **19** | **49,19%** | **-2,6** | **17** | **2** | **6** |

- **Nenhuma das 53 pesquisas deu ao Lula o que a urna deu** (51,79%). A mais perto foi a Vox Brasil (50,99%).
- Na última de cada instituto, só **Vox Brasil** e **Colectta** davam o Lula à frente, e **as duas também ficaram abaixo da urna**.
- O erro médio foi de **2,6 pontos** no Lula (o dobro, 5,2 pontos, na diferença entre os dois). Todos os institutos erraram para o mesmo lado.
- A projeção do vídeo longo 14 dava Flávio 50,8%; a urna deu 48,21%: erro de 2,6 pontos, contra o erro médio de 1,8 que o próprio método teria tido no passado.

### A última pesquisa de cada instituto

| Instituto | Fim do campo | Lula | Flávio | Erro no Lula | Registro no TSE |
|---|---|---|---|---|---|
| Vox Brasil | 22/10 | 50,6% | 49,4% | -1,2 | BR032592026 |
| Colectta | 23/10 | 50,3% | 49,7% | -1,5 | BR056012026 |
| Futura | 24/10 | 49,8% | 50,2% | -1,9 | BR097262026 |
| Palver | 24/10 | 49,5% | 50,5% | -2,3 | BR017942026 |
| PoderData | 24/10 | 49,5% | 50,5% | -2,3 | BR028282026 |
| Datafolha | 24/10 | 49,5% | 50,5% | -2,3 | BR095402026 |
| Ipespe | 22/10 | 49,5% | 50,5% | -2,3 | BR043502026 |
| Nexus | 24/10 | 49,5% | 50,5% | -2,3 | BR082342026 |
| Quaest | 24/10 | 49,5% | 50,5% | -2,3 | BR091582026 |
| Indexa | 21/10 | 49,4% | 50,6% | -2,4 | BR023482026 |
| MDA | 23/10 | 49,3% | 50,7% | -2,5 | BR021362026 |
| AtlasIntel | 23/10 | 49,2% | 50,8% | -2,5 | BR063802026 |
| Verita | 23/10 | 49,0% | 51,0% | -2,8 | BR060702026;BR031812026 |
| Ideia | 19/10 | 48,9% | 51,1% | -2,9 | BR082512026 |
| Instituto França | 23/10 | 48,6% | 51,4% | -3,2 | BR048632026 |
| Alfa | 19/10 | 48,5% | 51,5% | -3,3 | BR008202026 |
| Gerp | 24/10 | 48,4% | 51,6% | -3,4 | BR093272026 |
| DataTrends | 21/10 | 47,9% | 52,1% | -3,9 | BR033652026 |
| Real Time | 22/10 | 47,9% | 52,1% | -3,9 | BR096702026 |

### O erro trocou de lado entre os turnos, e isso já tinha acontecido

Erro médio das últimas pesquisas de cada instituto, no candidato contra o PT, em pontos (positivo: a pesquisa deu mais a ele do que a urna):

| Eleição | 1º turno | 2º turno |
|---|---|---|
| 2014 | -5,6 | +1,9 |
| 2018 | -1,3 | +0,8 |
| 2022 | -1,0 | 0,0 |
| **2026** | -1,9 | **+2,6** |

No 1º turno, as pesquisas deram **menos** ao candidato contra o PT nas quatro eleições. No 2º turno de 2014 e de 2018 deram **mais**; em 2022, quase nada. Em 2026 o padrão se repetiu, com o maior erro de 2º turno da série.

## 3. As regras que "sempre valiam"

| Regra | Histórico | 2026 |
|---|---|---|
| O líder do 1º turno de presidente venceu o 2º | 7 de 7 (1989 a 2022) | **quebrou**: o Flávio liderou o 1º turno e perdeu |
| A menor frente de um líder do 1º turno | 5,23 pontos (2022) | 1,87 pontos, a menor da série |
| Quem venceu Minas no 1º turno venceu a eleição | 8 de 8 (1994 a 2022) | **quebrou**: Minas deu Flávio no 1º turno |
| Quem venceu Minas no 2º turno venceu a eleição | 6 de 6 (2002 a 2022) | valeu: Minas deu Lula no 2º turno |
| Estados que sempre acertaram o vencedor no 1º turno | AM, AP, MG, TO | acertaram de novo: AM, AP |
| Estados que sempre acertaram o vencedor no 2º turno | AM, MG | acertaram de novo: AM, MG |
| Governador: o líder do 1º turno venceu o 2º | 67 de 92 (1994 a 2022) | 2 viradas em 6 disputas: RN, TO |
| Governador com frente de até 3 pontos e líder abaixo de 50% | 10 viradas em 18 | sem caso no 2º turno de 2026 |

Regra com 7 ou 8 casos quebra: pela regra de Laplace, uma regra que acertou 7 de 7 vezes ainda deixa 1 em 9,0 de chance de quebrar na próxima. E em governador, onde há 92 casos, o líder do 1º turno perdeu 25 vezes; com frente de até 3 pontos, perdeu 10 em 18. A frente do Flávio, 1,87 pontos, era a menor já vista num 1º turno de presidente.

## 4. Quem venceu em cada lugar

- **Estados:** o Lula venceu em 12 no 1º turno e em 13 no 2º. **Só Minas Gerais virou** (Flávio para Lula); nenhum estado foi do Lula para o Flávio.
- **O Lula subiu em todos os 27 estados**, de 4,5 a 9,3 pontos. A subida foi parecida no país inteiro.
- **Municípios:** 211 viraram do Flávio para o Lula e 1 do Lula para o Flávio (mais 2 que estavam empatados e foram para o Lula). O Lula ganhou votos em 5.491 dos 5.571 municípios; o Flávio, em 4.624, e **perdeu votos em 938**.
- A maior cidade que virou foi o **Rio de Janeiro** (43,9% para 51,5% do Lula). As outras grandes: Osasco (SP), Ananindeua (PA), Macapá (AP), São Vicente (SP), Ribeirão Das Neves (MG).
- O ganho do Lula veio de cidades de todo tamanho: até 20 mil eleitores: +1,78 milhões; 20 a 100 mil: +2,75 milhões; 100 a 500 mil: +2,68 milhões; mais de 500 mil: +3,13 milhões. Nas capitais, +2,75 milhões para o Lula e +1,03 milhões para o Flávio.
- **Governador e presidente:** em **18 de 27** estados o governador eleito é de uma coligação do lado que venceu para presidente ali. Em 6, a coligação do governador não tinha nem o PT nem o PL. Os que ficaram de lados diferentes: Alagoas (Jhc, coligação do lado do Flávio; presidente: Lula); Amapá (Dr. Furlan, coligação do lado do Flávio; presidente: Lula); Pará (Dr. Daniel, coligação do lado do Flávio; presidente: Lula). Tabela: `resultados/governador_e_presidente.csv`.
- **2º turno de governador no mesmo dia:** 2 viradas em 6 disputas (Rio Grande do Norte: Cadu De Lula passou Allyson; Tocantins: Vicentinho Júnior passou Professora Dorinha).

## 5. Abstenção, branco e nulo

| Eleição | Abstenção no 1º turno | No 2º turno | Variação (pontos) |
|---|---|---|---|
| 2002 | 17,74% | 20,47% | +2,73 |
| 2006 | 16,75% | 18,99% | +2,24 |
| 2010 | 18,12% | 21,50% | +3,38 |
| 2014 | 19,39% | 21,10% | +1,71 |
| 2018 | 20,33% | 21,30% | +0,97 |
| 2022 | 20,95% | 20,58% | -0,36 |
| **2026** | 21,08% | 19,22% | **-1,86** |

Em cinco das seis eleições anteriores, **mais gente faltou** no 2º turno. Em 2026 a abstenção **caiu 1,86 pontos**: 2,96 milhões de pessoas a mais votando, a maior queda da série. Brancos e nulos caíram de 4,77% para 3,24% de quem votou. A abstenção **subiu** em 9 estados (AC, AM, AP, MA, PA, PI, RO, RR, TO), quase todos no Norte. Em 6 deles o Flávio teve menos votos no 2º turno do que no 1º (AC, AM, AP, MA, RR, TO).

A queda da abstenção **não** se concentrou onde o Lula era mais forte: ela foi de 1,83 pontos no terço onde o Lula foi mais fraco; 1,99 pontos no terço do meio; 1,55 pontos no terço onde o Lula foi mais forte. Mas, dentro de cada município, onde a abstenção mais caiu o Lula mais subiu (correlação de 0,26).

## 6. De onde vieram os votos (estimativa)

Modelo de transição com restrição (cada eleitor do 1º turno vai para algum lugar no 2º, e as proporções somam 100%), ajustado por região com os 5.571 municípios e somado no país; faixa de 90% por reamostragem de municípios. Arquivo: `resultados/transferencia_de_votos.csv`.

| Eleitor do 1º turno | Lula | Flávio | Branco ou nulo | Faltou |
|---|---|---|---|---|
| Augusto Cury | 48% (39 a 62) | 33% (24 a 39) | 19% (12 a 23) | 0% (0 a 5) |
| Renan Santos | 47% (36 a 55) | 41% (34 a 49) | 11% (7 a 17) | 1% (0 a 3) |
| Ronaldo Caiado | 44% (37 a 50) | 42% (35 a 49) | 12% (9 a 17) | 2% (1 a 4) |
| Zema e outros | 52% (32 a 67) | 43% (28 a 62) | 5% (1 a 9) | 0% (0 a 1) |
| Branco ou nulo | 70% (66 a 73) | 0% (0 a 2) | 30% (27 a 33) | 0% (0 a 1) |
| Faltou | 7% (6 a 8) | 1% (0 a 2) | 2% (2 a 3) | 90% (89 a 90) |
| Lula | 99% (99 a 99) | 0% (0 a 0) | 0% (0 a 0) | 0% (0 a 1) |
| Flávio | 0% (0 a 0) | 100% (99 a 100) | 0% (0 a 0) | 0% (0 a 1) |

Lendo a tabela: os eleitores de Cury, Renan e Caiado se dividiram, com um pouco mais para o Lula em cada um, mas as faixas se cruzam (não dá para cravar que o Lula levou mais que o Flávio em nenhum dos três sozinho). Somados, a estimativa dá ao Lula cerca de 4,34 milhões vindos dos outros candidatos, 4,19 milhões de quem tinha votado branco ou nulo e 2,23 milhões de quem tinha faltado.

**Limites que pesam:** o modelo enxerga mal a troca direta de um candidato para o outro (ele tende a dar zero), e o número de "branco e nulo para o Lula" é o mais frágil, porque o branco e o nulo são pequenos em cada município. O modelo reproduz o 2º turno observado com diferença de 13.522 votos no Lula. Uma matriz única para o país inteiro dá números diferentes (`resultados/transferencia_matriz_unica_pais_pct.csv`), o que mostra quanto a estimativa depende do recorte. A pesquisa que perguntou "em quem votou no 1º turno" seria a segunda fonte, e ainda não foi coletada.

## 7. A probabilidade, antes da votação

A média da última pesquisa de cada instituto dava ao Flávio uma frente de **1,61 pontos**. A pergunta é: com o que se sabia no sábado, qual era a chance de o Lula vencer?

| Régua | Chance do Lula | Em outras palavras |
|---|---|---|
| o líder do 1º turno sempre venceu (Laplace) | 11% | 1 em 9,0 |
| Polymarket na véspera | 19% | 1 em 5,3 |
| pesquisas e erro histórico (só presidente) | 33% | 1 em 3,0 |
| pesquisas e erro histórico (contagem) | 33% | 1 em 3,0 |
| pesquisas e erro histórico (todas as disputas) | 39% | 1 em 2,6 |
| governador com frente de até 3 pontos | 56% | mais de 1 em 2 |

- **Pesquisas e erro histórico:** em 42 segundos turnos de 2014 a 2022 (presidente e governador), a média das pesquisas errou a frente do líder com desvio de 7,3 pontos. Com esse erro, uma frente de 1,61 pontos vira em cerca de 1 de cada 3 eleições.
- **Vitória do Lula por 3,57 pontos ou mais** (o que aconteceu): 22% pela mesma conta, ou 14% contando os casos do histórico.
- **O histórico do 1º turno** (líder sempre venceu, 7 de 7) dá 1 em 9,0.
- **A Polymarket** dava 19% ao Lula na véspera. Nos mercados de eleição em que o favorito tinha de 70% a 90%, o favorito perdeu 3 de 18 vezes. A mesma Polymarket deu o Lula como favorito no 1º turno (72%) e errou.
- **Média das três réguas principais** (pesquisas com erro histórico, histórico do 1º turno e Polymarket): **23%**, ou 1 em 4,4.

## 8. As duas lentes

A leitura completa, com a versão mais forte de cada lado, está em [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md). O que os testes mostram:

| Teste | Lula | Flávio |
|---|---|---|
| Municípios em que o ganho passou de tudo o que estava livre (votos dos outros + queda da abstenção + queda de branco e nulo) | 291 municípios, 15.636 votos | 2 municípios, 228 votos |
| Municípios com comparecimento acima de 95% e 90% ou mais para um candidato, 1º turno | 0 | 0 |
| O mesmo, 2º turno | 0 | 0 |

Os 15.636 votos "sem origem visível" do Lula são **0,35%** da frente final. Eles cabem em troca direta de voto (gente que votou Flávio no 1º e Lula no 2º), que este teste não enxerga.

## 9. Validação

12 de 12 números centrais refeitos por outro caminho, direto dos arquivos do TSE e das capturas, sem usar o código da análise (`ferramentas/validacao-independente.py`, `resultados/validacao_independente.csv`). Os totais por UF somam o país e os municípios somam cada UF, nos dois turnos, com diferença zero (`ferramentas/derivar.py`).

## 10. Gráficos

`resultados/figuras/`, 1920x1080: de onde vieram os votos (g01), as pesquisas contra a urna (g02 e g03), o erro que troca de lado (g04), as regras (g05), os estados (g06), a abstenção (g07), a transferência estimada (g08), governador e presidente (g09), a probabilidade (g10) e os votos sem origem visível (g11).
