# Relatório: as pesquisas, o histórico e a chance do que aconteceu no 2º turno de 2026

Gerado por `ferramentas/gerar-relatorio.py` a partir de `resultados/RESUMO.json`. **Rodada 2 (26/10/2026)**: refeita pelo retorno do autor, com o histórico de erro das pesquisas no Brasil e em outros países, as viradas de 2º turno, os mesmos testes em todas as eleições de 2002 a 2022 e a chance calculada em pilares com os pesos dele. O que mudou da rodada 1 está em [`docs/RODADAS.md`](docs/RODADAS.md).

## A resposta curta

**Antes da votação, a chance de o Lula vencer era de cerca de 27% (1 em 3,7), refeita na rodada 5** (a rodada 2 dava 39%; as três correções estão abaixo). A ponta de baixo, tratando os três pilares como indícios independentes, dá 8% (1 em 12,0), e o mercado dava 24% na véspera. Vencer **pela diferença que venceu** (3,57 pontos ou mais) tinha perto de 13% (1 em 7,6).

**Duas coisas de 2026 saem do padrão das eleições de 2002 a 2022, e uma não sai.** Saem: o candidato do PT levar 74% dos votos livres quando quem saiu era de direita ou de centro e apoiou o adversário, e o comparecimento subir 1,85 ponto do 1º para o 2º turno. Não sai: a virada se espalhar por quase todos os municípios, que é o que acontece sempre que a diferença anda muito no país.

## Rodada 5: isso é normal?

Pedido do autor: *"é normal, tendo em vista que os candidatos eram de direita, que a maior parte dos votos vá para o Lula? Nas outras eleições, isso aconteceu de verdade?"*, se é normal o comparecimento subir e a virada se espalhar, e se a chance de 39% considerou as pesquisas, o 1º turno e o crescimento *"com peso de forma correta"*. Cada resposta abaixo põe 2026 ao lado das 6 eleições anteriores, com a mesma conta.

### 1. O eleitor de quem saiu ir para o PT quando quem saiu apoiou o adversário

| Eleição | Quem saiu (os 3 maiores) e o que fez no 2º turno | Votos de quem saiu com apoio ao PT | Com apoio ao adversário | PT nos votos livres (saldo, conta exata) | Eleitores de quem saiu: PT e adversário (modelo nacional) | Para o PT (modelo regional) |
|---|---|---|---|---|---|---|
| 2002 | Anthony Garotinho (apoiou o PT); Ciro Gomes (apoiou o PT); Zé Maria (neutro ou nulo) | 98% | 0% | **49%** | 58% e 30% | 59% |
| 2006 | Heloísa Helena (neutro ou nulo); Cristovam Buarque (neutro ou nulo) | 0% | 0% | **126%** | 48% e 23% | 77% |
| 2010 | Marina Silva (neutro ou nulo); Plínio de Arruda Sampaio (neutro ou nulo) | 0% | 0% | **43%** | 37% e 42% | 49% |
| 2014 | Marina Silva (apoiou o adversário); Luciana Genro (neutro ou nulo); Pastor Everaldo (apoiou o adversário) | 0% | 93% | **41%** | 34% e 56% | 44% |
| 2018 | Ciro Gomes (neutro ou nulo); Geraldo Alckmin (neutro ou nulo); João Amoêdo (neutro ou nulo) | 6% | 0% | **65%** | 58% e 28% | 67% |
| 2022 | Simone Tebet (apoiou o PT); Ciro Gomes (apoiou o PT); Soraya Thronicke (neutro ou nulo) | 86% | 0% | **30%** | 37% e 41% | 37% |
| 2026 | Augusto Cury (apoiou o adversário); Renan Santos (neutro ou nulo); Ronaldo Caiado (apoiou o adversário) | 0% | 68% | **74%** | 47% e 40% | 71% |

A posição de cada candidato, com o link da fonte, está em `dados/agentes/apoios_segundo_turno.csv` (27 de 28 com fonte; Zé Maria, 2002, sem fonte). A coluna do saldo é conta exata; as duas últimas são estimativas, porque o voto é secreto, e os dois modelos do projeto discordam entre si.

**O que a tabela mostra:**
- **Em 2026, 68% dos votos de quem saiu eram de candidatos que declararam apoio ao Flávio, nenhum declarou apoio ao Lula, e o Lula levou 74% de tudo o que estava livre.** Nas 6 eleições anteriores, o PT só passou de 60% dos votos livres em 2006 e 2018, quando os maiores eliminados eram da esquerda ou ficaram neutros.
- **Nos anos em que quem saiu era de centro ou de direita (2010, 2014, 2022), o PT ficou com 30% a 43% dos votos livres.** Pelos dois modelos, o eleitor dos eliminados foi mais para o PT em 2026 do que em qualquer um desses anos: 47% contra 34% a 37% no modelo nacional, e 71% contra 37% a 49% no regional.
- **O espelho é 2022.** 86% dos votos de quem saiu eram de Tebet e Ciro, que apoiaram o Lula, e o Bolsonaro levou 70% dos votos livres. O apoio declarado já não decidia para onde ia o eleitor livre em 2022; em 2026 ele também não decidiu, no sentido contrário.
- **O que as pesquisas diziam desse eleitor:** entre Lula e Flávio, o de Cury dava 53% ao Lula, o de Renan 40% e o de Caiado 38% (média de 5 institutos cada). Se eles tivessem votado assim e quem voltou a votar tivesse se dividido como no próprio ano, o Flávio teria vencido por 2,66 milhões. O Lula venceu por 4,43 milhões: uma distância de 7,09 milhões, do mesmo tamanho do erro das pesquisas na diferença (5,2 pontos dos válidos, cerca de 6,43 milhões). **É o mesmo erro, visto de outro lugar: as pesquisas erraram justamente no eleitor que estava livre.**
- 🔧 **Correção do que foi dito na rodada 3:** o "cerca de 6 milhões vieram dos eleitores dos outros candidatos" é o modelo regional. O modelo nacional, usado desde a rodada 1, dá 4,40 milhões. A parte que vem de quem saiu e a que vem de quem voltou a votar mudam conforme o modelo: **de 4,40 milhões a 6,56 milhões vieram dos eleitores dos outros candidatos**, e o resto, de quem voltou a votar ou tinha votado branco ou nulo. O total é exato; a divisão, não.

**Veredito: não é normal.** É o resultado mais fora do padrão da série nesse quesito, junto com 2022 no sentido contrário. Pela lente do resultado legítimo, o espelho de 2022 mostra que o apoio declarado do candidato derrotado não leva o eleitor junto, e o erro das pesquisas do mesmo tamanho já aconteceu em segundos turnos de outros países (15 de 41 erraram a diferença por mais de 5,2 pontos). Pela lente da fraude, é exatamente nesse eleitor livre que um voto acrescentado apareceria. O que pesa contra ela, no dado por município: na regressão de cada ano, quem voltou a votar se dividiu quase igual entre os dois (51% e 45%, como em 2022), e o ganho do Lula aparece no país inteiro, sem bolsões. Seção a seção, é o projeto do vídeo 16.

### 2. O comparecimento subir e a virada se espalhar

| Eleição | Comparecimento do 1º para o 2º turno (pontos) | Municípios em que subiu | Diferença andou no país (pontos, a favor do PT) | Municípios que andaram no mesmo sentido | Desvio da virada entre municípios |
|---|---|---|---|---|---|
| 2002 | -2,72 | 282 (5%) | -0,7 | 69% | 13,37 |
| 2006 | -2,24 | 112 (2%) | +14,7 | 100% | 5,26 |
| 2010 | -3,38 | 131 (2%) | -2,2 | 72% | 5,61 |
| 2014 | -1,71 | 415 (7%) | -4,7 | 75% | 7,00 |
| 2018 | -0,97 | 748 (13%) | +6,5 | 69% | 8,09 |
| 2022 | +0,36 | 3.604 (65%) | -3,4 | 83% | 2,16 |
| 2026 | +1,85 | 4.440 (80%) | +5,4 | 97% | 1,87 |

- **O comparecimento:** de 2002 a 2018 ele sempre caiu do 1º para o 2º turno (-1,0 a -3,4 ponto), e subiu em no máximo 13% dos municípios. Em 2022 subiu pela primeira vez (+0,36, em 65% dos municípios). Em 2026 subiu +1,85, em 80% dos municípios: **o maior da série, 5 vezes o de 2022.** Em 2026, o transporte de graça no dia da votação era regra no país inteiro (Resolução TSE nº 23.751/2026, em `dados/agentes/fatos_entre_os_turnos.md`).
- **Onde ele subiu:** mais nas cidades de renda maior (a abstenção caiu 2,5 ponto nos 20% de municípios mais ricos e ficou parada nos 20% mais pobres) e não onde o PT era mais forte (a correlação entre a força do PT no 1º turno e a queda da abstenção foi -0,06 em 2026, contra -0,33 a 0,28 nas outras).
- **A virada espalhada:** em 2026 a diferença andou para o Lula em 97% dos municípios. Em 2006, o outro ano em que ela andou muito a favor do PT, foram 100%. Quando a diferença anda muito no país, ela anda em quase todo lugar. O desvio entre municípios (1,87 ponto) é o menor da série, perto do de 2022 (2,16): nos dois anos, poucos votos estavam livres (os eliminados somaram 7,8% dos válidos em 2026), e movimento pequeno sai mais igual.

**Veredito:** o comparecimento **não é normal** pela série de 2002 a 2018 e é a continuação, em tamanho maior, do que começou em 2022; ele subiu mais onde a renda é maior e não onde o PT era mais forte. A virada espalhada **é normal** para o tamanho do movimento.

### 3. A chance, refeita com as nuances que faltavam

A conta da rodada 2 tinha três defeitos. Dois puxavam a chance para cima, e um escondia o quanto ela podia cair.

1. **O histórico não olhava o quanto o líder estava perto de 50%.** A rodada 2 contou as viradas entre segundos turnos com frente parecida (23 em 49), misturando líderes com 20% e com 50%. Um líder com 47% precisa de bem menos votos novos. Com as duas coisas na conta (241 segundos turnos, regressão), a chance de virada cai de 47% para **38%**. Os 13 casos com o líder entre 45% e 50% e frente de até 4 pontos tiveram 6 viradas: Brasil SE 1994 (líder com 47,6%, 0,22 de frente, **virou**); Colômbia 1994 (líder com 45,3%, 0,32 de frente); Brasil PB 2010 (líder com 49,7%, 0,44 de frente); Chile 1999 (líder com 48,0%, 0,45 de frente); Brasil RR 2002 (líder com 49,2%, 0,60 de frente, **virou**); Montenegro 1997 (líder com 48,2%, 0,74 de frente, **virou**); Brasil PB 2006 (líder com 49,7%, 0,93 de frente); Brasil RN 2006 (líder com 49,6%, 0,97 de frente); Brasil PA 2014 (líder com 49,0%, 1,38 de frente, **virou**); Brasil PB 2014 (líder com 47,4%, 1,40 de frente, **virou**); Brasil CE 2014 (líder com 47,8%, 1,40 de frente); Brasil RR 2010 (líder com 47,6%, 2,58 de frente, **virou**); Brasil PB 1994 (líder com 46,6%, 3,22 de frente). Para presidente no Brasil, o líder do 1º turno venceu as 7 vezes, mas a menor frente foi de 5,2 pontos, então essa regra não fala de uma frente de 1,87.
2. **O crescimento usava os 6 padrões de transferência sem olhar quem tinha saído.** Em 2026 quem saiu era de centro ou de direita. Só com os anos parecidos (2010, 2014, 2022), o Lula venceria em 0 de 3 (ficaria com 48,8%, 48,7%, 47,6%). Pela regra de Laplace, **20%**, contra 33% antes.
3. **A média com pesos é o jeito errado de juntar indícios que apontam para o mesmo lado.** Ela trata os pilares como opiniões que se substituem. Quando cada um é um indício diferente, a conta é por chances (Bayes): o histórico dá o ponto de partida e as pesquisas atualizam. Como as pesquisas já carregam boa parte do que o crescimento mede (o eleitor dos eliminados é entrevistado nelas), o central usa os dois primeiros; contar os três como independentes é a ponta de baixo.

**O que não cai:** o pilar das pesquisas. Só com 2º turnos de presidente com 4 ou mais institutos (24 casos), a chance sobe para 42%; e no Brasil a média das pesquisas superestimou o líder nos 6 segundos turnos de 2002 a 2022, o que também puxaria para o Lula.

| Jeito de calcular | Chance do Lula | Em outras palavras |
|---|---|---|
| rodada 2 (média com pesos, sem as correções) | 39% | 1 em 2,5 |
| média com pesos, com as correções 1 e 2 | 35% | 1 em 2,9 |
| Bayes: o histórico como ponto de partida e as pesquisas como indício (central) | 27% | 1 em 3,7 |
| Bayes com as pesquisas só de presidente com 4 ou mais institutos | 30% | 1 em 3,3 |
| os três pilares como indícios independentes (ponta de baixo) | 8% | 1 em 12,0 |
| mercado (Polymarket, véspera) | 24% | 1 em 4,3 |

**Veredito:** a chance era **menor do que a rodada 2 disse: cerca de 27%, perto de 1 em 4**, com ponta de baixo de 8% e o mercado em 24%. Abaixo de 1 em 12,0 ela não vai por nenhum dos caminhos calculados aqui: com a frente de 1,6 ponto nas pesquisas, basta um erro de 2º turno do tamanho que já aconteceu muitas vezes. Ganhar por 3,6 pontos ou mais era mais raro: 13% (1 em 7,6).

## De onde vieram os 10,38 milhões de votos a mais do Lula

**A conta fecha, voto por voto.** Entre o 1º e o 2º turno ficaram livres 14,10 milhões de votos: os 9,32 milhões dos candidatos que saíram, 2,96 milhões de pessoas que não tinham votado e votaram, e 1,82 milhões que tinham votado branco ou nulo e escolheram alguém. O Lula ficou com 10,38 milhões e o Flávio com 3,72 milhões. Soma: 14,10 milhões, exatamente o que estava livre. **O Lula levou 3 de cada 4 votos que estavam em jogo.**

**De onde veio cada parte** (resultado de 5.571 municípios; o voto é secreto, então é uma estimativa, feita de três jeitos que dão quase o mesmo número):

| Ajuste | Eleitores dos outros candidatos | Quem não tinha votado em ninguém | Eleitores do Flávio que mudaram para o Lula |
|---|---|---|---|
| por região | 6,56 milhões | 3,55 milhões | 0,14 milhões |
| país inteiro | 6,01 milhões | 3,79 milhões | 0,21 milhões |
| estado por estado | 5,79 milhões | 3,83 milhões | 0,56 milhões |

**Resposta direta:**
1. **Cerca de 6 milhões (de 5,79 milhões a 6,56 milhões) vieram de quem votou em outro candidato no 1º turno** (Cury, Renan, Caiado, Zema e os demais). Dos 9,29 milhões desses eleitores, cerca de 2 em cada 3 votaram no Lula.
2. **Cerca de 3,6 milhões (de 3,55 milhões a 3,83 milhões) vieram de quem não tinha votado em ninguém no 1º turno**: quem faltou e voltou a votar, e quem tinha votado branco ou nulo. Dos 4,74 milhões que entraram, cerca de 3 em cada 4 votaram no Lula.
3. **Quase nada veio de eleitor do Flávio que mudou de lado: de 0,14 milhões a 0,56 milhões.** O método enxerga essa troca quando ela existe: em 2006, ele encontra 3,85 milhões de eleitores do Alckmin que foram para o Lula, e foi o ano em que o Alckmin teve menos votos no 2º turno do que no 1º.

**Onde:** SP, MG, RJ, BA somam 53% do ganho do Lula.

| UF | Lula ganhou | Parte do ganho do Lula | Flávio ganhou | Votos dos outros no 1º turno | Abstenção caiu |
|---|---|---|---|---|---|
| SP | +2,61 milhões | 25% | +1,22 milhões | 2,46 milhões | 0,93 milhões |
| MG | +1,16 milhões | 11% | +0,46 milhões | 1,01 milhões | 0,41 milhões |
| RJ | +0,87 milhões | 8% | +0,20 milhões | 0,71 milhões | 0,22 milhões |
| BA | +0,82 milhões | 8% | +0,17 milhões | 0,45 milhões | 0,37 milhões |
| PE | +0,56 milhões | 5% | +0,09 milhões | 0,31 milhões | 0,22 milhões |
| RS | +0,53 milhões | 5% | +0,30 milhões | 0,55 milhões | 0,19 milhões |

**Isso já aconteceu?** O candidato do PT ficar com a maior parte dos votos livres, sim, mas só quando quem saiu era da esquerda ou ficou neutro; com quem saiu apoiando o adversário, nunca (seção "Rodada 5" acima):

| Eleição | Votos livres no saldo | Parte que o PT levou | Eleitores do adversário que mudaram para o PT (estimativa) |
|---|---|---|---|
| 2002 | 27,00 milhões | 49% | 0,00 milhões |
| 2006 | 9,20 milhões | 126% | 3,85 milhões |
| 2010 | 18,65 milhões | 43% | 0,00 milhões |
| 2014 | 27,33 milhões | 41% | 0,00 milhões |
| 2018 | 24,17 milhões | 65% | 0,05 milhões |
| 2022 | 10,18 milhões | 30% | 0,00 milhões |
| 2026 | 14,03 milhões | 74% | 0,14 milhões |

Em 2006 o PT levou **mais do que tudo o que estava livre** (126%), porque, além dos livres, ganhou eleitores do Alckmin. Em 2022 foi o contrário: o Bolsonaro levou 70% dos livres e mesmo assim perdeu. **Os 74% de 2026 são o segundo maior da série, abaixo de 2006.**

**Por que isso surpreendeu:** as pesquisas diziam que os eleitores de Renan e de Caiado iam mais para o Flávio, e somando os três maiores o Flávio levaria uns 0,73 milhões a mais. O resultado mostra o contrário: 2 em cada 3 votaram no Lula. Esses cruzamentos das pesquisas usam grupos de 40 a 100 entrevistados, com margem de erro de 10 pontos ou mais, e em 2022 também não acertaram: davam de 42% a 60% do eleitor de Ciro e de Tebet para o Lula, e o Bolsonaro levou 70% dos votos livres. E o filtro de eleitor provável trabalha contra quem tende a faltar: na Nexus da véspera, tirar os 21% menos propensos a votar baixava o Lula de 49,5% para 47,6%, e foi justamente esse eleitor que voltou a votar.

**O que o dado não separa:** quanto dos 6 milhões veio de cada candidato. Os eleitores de Cury, Renan e Caiado estão misturados nos mesmos municípios, e o ajuste candidato por candidato fica instável (`resultados/de_onde_vieram_por_candidato_2026.csv`). O total dos três juntos é estável.

## O que justifica a virada (rodada 4)

**Escopo deste projeto:** pesquisas, histórico e resultado por país, estado e município. O que é seção por seção (logs das urnas, boletins, horário de cada voto) é do projeto do vídeo 16 (`investigacao-segundo-turno-2026`); daqui só se cita o número que ele publicou dos votos depois das 17h: **34.810 votos no país**, que seriam 0,79% da diferença mesmo se fossem todos do Lula.

**Os fatos de que se parte** (levantados com link em `dados/agentes/fatos_entre_os_turnos.md`):
- **Os apoios:** Zema declarou voto no Flávio em 05/10, Caiado em 06/10 e Cury em 08/10 (com um termo de compromisso); Renan Santos ficou neutro e criticou o Flávio.
- **As medidas do governo:** o Bolsa Família subiu 15,04% (decreto de 17/09, piso de R$ 600 para R$ 691) e a parcela de outubro foi paga em 19, 20 e 21/10, antes do 2º turno; o Prospera MEI (perdão de dívidas de MEIs a partir de 2027) foi anunciado em 13/10 e sancionado em 21/10; os impostos federais da gasolina foram zerados por 30 dias em 09/10.
- **O transporte:** ônibus de graça no dia da votação era obrigatório no país; São Paulo rodou com frota maior no 2º turno.

### 1. O eleitor de direita foi mais para o Flávio, mas não em bloco

Renan, Caiado e Zema tinham **5,61 milhões** de votos no 1º turno. O Flávio inteiro ganhou **3,72 milhões** no 2º. Mesmo que todo o ganho do Flávio tivesse vindo desses três, faltariam 1,89 milhões: o apoio declarado não levou os eleitores junto.

| Municípios pela força de Renan, Caiado e Zema | Os três no 1º turno | Lula levou dos votos livres | Flávio levou |
|---|---|---|---|
| 1 (mais fraco) | 1,7% | 99% | 1% |
| 2 | 2,4% | 90% | 10% |
| 3 | 3,1% | 81% | 19% |
| 4 | 4,1% | 76% | 24% |
| 5 (mais forte) | 7,4% | 67% | 33% |

Onde os três eram mais fortes, o Flávio levou mais, como se esperaria; mesmo assim o Lula levou a maior parte. Em Goiás, a base do Caiado (12,3% no 1º turno), o Lula levou 57% dos votos livres.

### 2. As medidas para os mais pobres não explicam a virada

Se o reajuste e a antecipação do Bolsa Família tivessem virado votos, o Lula teria crescido mais nos municípios mais pobres, onde estão os beneficiários. Municípios em 5 grupos pela renda per capita do Censo 2022:

| Grupo | Renda (mediana) | Lula no 1º turno | Lula ganhou a cada 100 eleitores | Flávio ganhou | Abstenção caiu (pontos) | Parte da virada da diferença | Parte do eleitorado |
|---|---|---|---|---|---|---|---|
| 1 (mais pobres) | R$ 659 | 72% | 4,6 | -0,1 | -0,1 | 11% | 10% |
| 2 | R$ 824 | 65% | 6,1 | 0,7 | 1,4 | 16% | 12% |
| 3 | R$ 1.183 | 49% | 6,6 | 1,8 | 1,6 | 18% | 16% |
| 4 | R$ 1.452 | 41% | 6,5 | 2,6 | 1,8 | 14% | 15% |
| 5 (mais ricos) | R$ 1.842 | 42% | 7,1 | 3,4 | 2,5 | 42% | 47% |

- O Lula **ganhou menos votos por eleitor nos municípios mais pobres** (4,6 a cada 100) **do que nos mais ricos** (7,1), e foi nos mais ricos que a abstenção mais caiu.
- Como o Flávio também ganhou mais nos mais ricos, **a virada da diferença foi parecida em todas as faixas de renda**: cada grupo deu à virada uma parte próxima do seu peso no eleitorado (um pouco acima nos três grupos mais pobres, um pouco abaixo nos dois mais ricos). Não há a concentração nos mais pobres que o Bolsa Família produziria.
- As medidas voltadas à classe média urbana (MEI, gasolina) combinam com o lugar onde o Lula mais ganhou votos, mas **não foram testadas** aqui.

### 3. Onde a virada aconteceu

A diferença entre os dois andou de Flávio 2,24 milhões à frente para Lula 4,40 milhões à frente: uma virada de 6,64 milhões. Ela andou para o Lula em **5.228 municípios** e para o Flávio em 339. Os 211 municípios que trocaram de vencedor deram só 8% da virada; o resto veio de lugares que já eram de um lado e ficaram mais Lula.

| Região | Parte da virada | Parte do eleitorado |
|---|---|---|
| Centro-Oeste | 4,5% | 7,6% |
| Nordeste | 38,5% | 27,6% |
| Norte | 6,9% | 8,3% |
| Sudeste | 43,0% | 42,0% |
| Sul | 7,0% | 14,5% |

O Nordeste deu mais do que o seu peso; o Sul e o Centro-Oeste, menos. A maior contribuição de uma cidade sozinha foi a de São Paulo (0,47 milhões).

### 4. O que apontava para o Lula antes da votação

| 2º turno | Inclinação das pesquisas (pontos por semana para o PT) | Média da última semana | Reta das pesquisas no dia da eleição | Urna |
|---|---|---|---|---|
| 2014 | +2,4 | 51,1% | 49,4% | 51,6% |
| 2018 | +2,9 | 42,1% | 45,7% | 44,9% |
| 2022 | +0,8 | 52,0% | 50,6% | 50,9% |
| 2026 | +0,6 | 49,1% | 49,5% | 51,8% |

Em 2026 as pesquisas andavam para o Lula, mas devagar: a reta chegava a 49,5% no dia da eleição, ainda abaixo de 50%. Em 2014 e 2018 o PT subia de 2 a 3 pontos por semana na reta final. Os outros sinais a favor eram poucos: duas pesquisas (Vox Brasil e Colectta) e o eleitor de baixa propensão a votar, que no Datafolha da véspera dava Lula 52 a 48.

### O que fica de pé, em uma frase por lado

- **A favor do resultado:** a virada se espalhou por quase todos os municípios, veio de eleitores dos candidatos derrotados que não seguiram o apoio declarado (cerca de 6 milhões) e de gente que voltou a votar (cerca de 3,6 milhões), com mais força nas cidades maiores, e os votos depois das 17h não mudam nada.
- **O que segue sem explicação completa:** por que tanta gente dos candidatos de direita não foi para o Flávio, e por que as pesquisas não captaram quem voltou a votar. O dado por município mostra onde e quanto; o motivo de cada eleitor, ele não mostra.

## 1. Como a chance foi calculada

Três pilares, cada um medindo a chance de um jeito diferente, com **os pesos que o autor escolheu para a projeção do vídeo longo 14** (pesquisas pesam mais porque são a medida mais direta e mais recente; o histórico pesa menos porque tem poucos casos de presidente; o crescimento pesa menos ainda porque depende de um modelo de transferência de votos, que é a parte mais frágil):

| Pilar | Peso | O que mede | O que o histórico mostra | Chance do Lula |
|---|---|---|---|---|
| **Pesquisas** | 60% | a frente do Flávio na média da última pesquisa de cada instituto (1,61 pontos) contra o erro da média das pesquisas em 80 segundos turnos passados | em 30 dos 80, a média das pesquisas superestimou o líder por mais do que essa frente | **38%** |
| **Histórico de viradas** | 25% | com que frequência o líder do 1º turno perdeu o 2º, quando a frente era parecida com a do Flávio (1,87 pontos; faixa de 1,5 ponto para cada lado) | 23 viradas em 49 disputas | **47%** |
| **Crescimento** | 15% | o 1º turno de 2026 com os votos livres (outros candidatos, branco e nulo, abstenção) indo como foram em cada 2º turno de 2002 a 2022 | o Lula venceria em 2 dos 6 padrões | **33%** |

**Conta:** 0,60 × 38% + 0,25 × 47% + 0,15 × 33% = **39,2%**.

**Conferência pelo mercado:** a Polymarket dava 23,5% ao Lula no preço diário da véspera (série do projeto do vídeo 16; a imprensa registrou 79,6% para o Flávio na manhã da eleição). Nos 45 mercados de eleição em que o favorito tinha de 70% a 90%, o favorito perdeu 6. A mesma Polymarket deu o Lula como favorito no 1º turno (72%) e errou.

**Quanto o número depende das escolhas:**

| Variante | Chance do Lula | Em outras palavras |
|---|---|---|
| pesos do vídeo 14 (60, 25, 15) | 39% | 1 em 2,5 |
| pesos iguais | 39% | 1 em 2,5 |
| só pesquisas | 38% | 1 em 2,7 |
| 60, 25, 15 com o mercado no lugar do crescimento | 38% | 1 em 2,6 |
| pesquisas só do presidente no Brasil | 36% | 1 em 2,7 |
| histórico só do presidente no Brasil (Laplace) | 30% | 1 em 3,3 |
| pesquisas corrigidas pelo viés do Brasil (presidente, 2002 a 2022) | 53% | 1 em 1,9 |

A variante mais desfavorável ao resultado usa só os 7 segundos turnos de presidente no Brasil para o histórico (0 viradas, pela regra de Laplace 1 em 9,0). Mesmo nela a chance fica perto de 1 em 3.

### O erro de multiplicar as "coincidências"

Uma conta que circula: as pesquisas erraram, o líder do 1º turno perdeu pela primeira vez, a regra de Minas quebrou e o favorito do mercado perdeu; multiplicando as chances de cada coisa (38% × 11% × 10% × 24%), dá **1 em 1.021**. A conta está errada porque as quatro coisas **são o mesmo fato** visto de quatro lugares: se o Lula vencesse, as pesquisas que davam Flávio errariam, o líder do 1º turno perderia, a regra de Minas quebraria e o favorito do mercado perderia, tudo junto, automaticamente. Multiplicar só vale para fatos independentes. A chance de todas acontecerem juntas é a chance de o Lula vencer: cerca de **1 em 2,5**.

## 2. As pesquisas já erraram tanto assim?

**O erro de 2026:** a média da última pesquisa de cada instituto (19 institutos) dava o Flávio 1,61 pontos à frente; a urna deu o Lula 3,57 à frente. A média superestimou a frente do Flávio em **5,2 pontos** (2,6 no voto de cada um). Nenhuma das 53 pesquisas chegou no número da urna; na última de cada instituto, 17 de 19 davam Flávio.

### No Brasil, 2º turno de presidente

| Eleição | Institutos | Frente do líder nas pesquisas | Frente dele na urna | Quanto a média superestimou o líder | O líder das pesquisas venceu? |
|---|---|---|---|---|---|
| 2002 | 1 | 28,0 | 22,5 | +5,5 | sim |
| 2006 | 1 | 22,0 | 21,7 | +0,3 | sim |
| 2010 | 4 | 12,9 | 12,1 | +0,8 | sim |
| 2014 | 4 | 4,3 | 3,3 | +1,1 | sim |
| 2018 | 7 | 14,1 | 10,3 | +3,8 | sim |
| 2022 | 10 | 3,2 | 1,8 | +1,4 | sim |
| **2026** | 19 | 1,6 | -3,6 | **+5,2** | **não** |

O líder das pesquisas tinha vencido todos os segundos turnos de presidente desde 2002, e **em todos os 6 a média superestimou o líder** (em média 2,1 pontos na frente). Quem descontasse esse viés de sempre da frente de 1,61 pontos do Flávio já chegaria a uma disputa empatada, levemente inclinada para o Lula (a chance pelas pesquisas iria a 60%; com só 6 eleições, isso entra como variante, não como número principal). **O erro de 2026 é o segundo maior da série**; o maior foi o de 2002 (só o Datafolha tem a última pesquisa publicada com data), mas lá o Lula tinha 28 pontos de frente e o erro não mudou o vencedor. **Em 2026 o erro foi do mesmo tamanho, numa disputa em que a frente era de menos de 2 pontos.** É isso que fez a diferença: erros desse tamanho já aconteceram, mas nunca numa disputa tão apertada.

### O lado do erro: menos à direita no 1º turno, mais no 2º

Erro médio das últimas pesquisas no candidato contra o PT, em pontos (positivo: deram mais a ele do que a urna):

| Eleição | 1º turno | 2º turno |
|---|---|---|
| 2014 | -5,6 | +1,9 |
| 2018 | -1,3 | +0,8 |
| 2022 | -1,0 | 0,0 |
| **2026** | -1,9 | **+2,6** |

No 1º turno as pesquisas deram menos ao candidato contra o PT nas quatro eleições; no 2º deram mais em 2014, 2018 e 2026. **A inversão de lado entre os turnos, que é apontada como sinal de algo estranho, já tinha acontecido em 2014 e 2018.**

### Em outros países

Na base de 41 segundos turnos presidenciais com pesquisas (Brasil e outros 35 no mundo, de 2010 a 2026, cada número conferido na fonte; `resultados/erro_media_pesquisas_runoffs.csv`), **o líder das pesquisas perdeu em 9** (22%). Em 10 delas a média superestimou o líder por mais do que em 2026, e em 15 o erro foi maior que o de 2026 para algum dos lados. Os maiores erros: Bolívia 2025 (+18,5), Romênia 2014 (+17,9), Equador 2025 (+13,0), Eslováquia 2024 (+8,2), Romênia 2025 (+7,5), Uruguai 2019 (+6,6), Chile 2013 (+5,9), Colômbia 2026 (+5,8), Equador 2021 (+5,7), Brasil 2002 (+5,5).

| Onde o líder das pesquisas perdeu | Frente nas pesquisas | Frente dele na urna | Quanto a média superestimou o líder |
|---|---|---|---|
| Bolívia 2025 | 8,5 | -9,9 | +18,5 |
| Romênia 2014 | 9,0 | -8,9 | +17,9 |
| Equador 2025 | 1,7 | -11,3 | +13,0 |
| Eslováquia 2024 | 2,0 | -6,2 | +8,2 |
| Romênia 2025 | 0,3 | -7,2 | +7,5 |
| Equador 2021 | 1,0 | -4,7 | +5,7 |
| Polônia 2025 | 0,3 | -1,8 | +2,1 |
| Peru 2021 | 1,7 | -0,3 | +2,0 |
| Peru 2016 | 1,1 | -0,2 | +1,3 |

**Leitura:** no Brasil, o erro de 2026 é grande; no mundo, é comum. O que pesa é a combinação de um erro de tamanho já visto com uma frente pequena. Em 2º turno de governador no Brasil (39 disputas de 2014 a 2022), o erro médio absoluto da média das pesquisas na frente do líder foi de 5,2 pontos.

## 3. "Nunca houve virada": o que o histórico diz

| Grupo | Segundos turnos | Viradas | Com frente de até 3 pontos e líder abaixo de 50% |
|---|---|---|---|
| Brasil governador | 92 | 25 | 10 em 18 |
| Brasil presidente | 7 | 0 | 0 em 0 |
| presidente, outros países | 142 | 49 | 14 em 32 |

Para presidente no Brasil, a regra "o líder do 1º turno vence" valia 7 de 7, **mas nenhuma dessas 7 eleições teve uma frente pequena**: a menor era de 5,23 pontos (2022), contra 1,87 em 2026. A regra nunca tinha sido testada numa disputa apertada. Quando a frente é parecida com a do Flávio (até 1,5 ponto para mais ou para menos), o líder perdeu **23 de 49** vezes: 8 de 17 em governador no Brasil e 15 de 32 em presidente pelo mundo. Em outros países, 49 viradas em 142 segundos turnos presidenciais. Os de presidente: Lituânia 2019 (0,37 ponto, **virou**); República Tcheca 2023 (0,41 ponto); Colômbia 1998 (0,41 ponto, **virou**); Chile 1999 (0,45 ponto); Chipre 1998 (0,55 ponto, **virou**); Macedônia do Norte 2019 (0,59 ponto); Ucrânia 2004 (0,66 ponto); Montenegro 1997 (0,74 ponto, **virou**); República Tcheca 2013 (0,81 ponto); Equador 1996 (0,89 ponto, **virou**); Costa Rica 2014 (0,93 ponto); Polônia 2015 (0,99 ponto); Croácia 2014 (1,27 ponto, **virou**); Romênia 2009 (1,30 ponto); Finlândia 2024 (1,41 ponto); Bulgária 2001 (1,44 ponto); França 2012 (1,45 ponto); Guatemala 1990 (1,58 ponto, **virou**); Polônia 2025 (1,82 ponto, **virou**); Polônia 1995 (2,00 pontos); Chile 2021 (2,09 pontos, **virou**); Chipre 2023 (2,45 pontos); França 1995 (2,46 pontos, **virou**); França 2017 (2,71 pontos); Colômbia 2026 (2,85 pontos); Chile 2025 (2,92 pontos, **virou**); Argentina 2015 (2,93 pontos, **virou**); Croácia 2019 (2,93 pontos); França 2002 (3,02 pontos); Polônia 2005 (3,23 pontos, **virou**); Sérvia 2004 (3,27 pontos, **virou**); Costa Rica 2018 (3,36 pontos, **virou**). Base: `resultados/viradas_casos.csv` (2º turnos de outros países conferidos na Wikipédia, 142 válidos).

**Minas:** quem venceu Minas no 1º turno venceu a eleição 8 de 8 vezes (quebrou em 2026: Minas deu Flávio no 1º turno); quem venceu Minas no 2º turno venceu a eleição 6 de 6 (valeu: Minas deu Lula). Minas acerta porque é parecida com o Brasil; numa eleição decidida por 1 a 2 pontos, um estado parecido com o país pode cair de qualquer lado.

## 4. O crescimento: os votos livres como em cada eleição passada

O 1º turno de 2026 com quem votou em Lula e em Flávio repetindo o voto, e os votos livres indo como foram em cada 2º turno de 2002 a 2022 (modelo de transição por município, por região; `resultados/crescimento_pelos_padroes_passados.csv`):

| Padrão de | Outros candidatos para PT e para o adversário | Branco e nulo para o PT | Abstenção para PT e para o adversário | Lula em 2026 |
|---|---|---|---|---|
| 2002 | 58% e 30% | 1% | 0,0% e 4,4% | **48,43%** |
| 2006 | 48% e 23% | 51% | 0,0% e 0,0% | **51,34%** |
| 2010 | 37% e 42% | 18% | 0,0% e 1,3% | **48,76%** |
| 2014 | 34% e 56% | 38% | 0,0% e 1,5% | **48,70%** |
| 2018 | 58% e 28% | 21% | 0,0% e 0,0% | **50,41%** |
| 2022 | 37% e 41% | 0% | 0,2% e 3,4% | **47,61%** |

O Lula venceria com o padrão de 2006 e com o de 2018, e perderia com os outros quatro. **Nenhum padrão do passado leva aos 51,79% que ele teve.** O que 2026 teve de diferente foi a abstenção: ela caiu 1,86 pontos entre os turnos, quando em 5 das 6 eleições anteriores tinha subido.

## 5. O resultado, em números

| | 1º turno (04/10) | 2º turno (25/10) | Diferença |
|---|---|---|---|
| Lula | 53.879.538 (45,16%) | 64.256.232 (**51,79%**) | **+10.376.694** |
| Flávio | 56.104.503 (47,03%) | 59.826.041 (48,21%) | **+3.721.538** |
| Outros candidatos | 9.316.747 | 0 | -9.316.747 |
| Abstenção | 33.469.244 (21,08%) | 30.509.005 (19,22%) | -2.960.239 |
| Brancos e nulos | 5.975.047 | 4.153.801 | -1.821.246 |

A conta fecha no voto: o que os dois ganharam (14.098.232) é exatamente o que saiu dos outros candidatos, da abstenção e do branco e nulo. Só Minas virou de estado (para o Lula); o Lula subiu em todos os 27 estados, de 4,5 a 9,3 pontos; 211 municípios viraram para o Lula e 1 para o Flávio. Em 18 de 27 estados o governador eleito é da coligação do lado que venceu para presidente ali; no 2º turno de governador do mesmo dia houve 2 viradas em 6 disputas.

**Abstenção, em cada eleição:**

| Eleição | Abstenção no 1º turno | No 2º | Variação | Subida média do PT nos municípios (pontos) | Desvio entre municípios | Municípios em que o PT caiu |
|---|---|---|---|---|---|---|
| 2002 | 17,73% | 20,45% | +2,72 | +14,8 | 10,50 | 57 |
| 2006 | 16,73% | 18,97% | +2,24 | +12,2 | 4,26 | 6 |
| 2010 | 18,07% | 21,44% | +3,38 | +8,9 | 6,30 | 704 |
| 2014 | 19,29% | 21,01% | +1,71 | +10,1 | 6,95 | 465 |
| 2018 | 20,19% | 21,17% | +0,97 | +15,3 | 6,96 | 3 |
| 2022 | 20,79% | 20,43% | -0,36 | +2,6 | 1,61 | 634 |
| 2026 | 20,84% | 18,99% | -1,85 | +6,6 | 1,71 | 4 |

O nível de 2026 no 2º turno (18,99% nos municípios do Brasil) é parecido com o de 2006; o incomum foi a **queda** entre os turnos. E a subida do Lula foi **a segunda mais uniforme da série** (desvio de 1,71 ponto entre municípios), depois da de 2022 (1,61).

## 6. Para onde foram os votos de Cury, Renan e Caiado

Três jeitos de medir, que não concordam inteiramente:

| Eleitor de | Institutos com o cruzamento | O que as pesquisas diziam (Lula entre Lula e Flávio) | O que o resultado por município indica (modelo de transição) |
|---|---|---|---|
| Augusto Cury | 5 | 53% (de 36 a 67) | 59% |
| Renan Santos | 5 | 40% (de 31 a 50) | 53% |
| Ronaldo Caiado | 5 | 38% (de 27 a 54) | 52% |

- **As pesquisas** (a última rodada de cada instituto com o cruzamento por voto no 1º turno, cada número conferido na fonte): os eleitores de Renan e de Caiado iam mais para o Flávio; os de Cury, um pouco mais para o Lula. Somando os três, o Flávio receberia cerca de 0,73 milhões a mais que o Lula. ⚠️ Cada grupo é cerca de 2% da amostra (uns 40 a 100 entrevistados), com margem de erro de 10 pontos ou mais.
- **O resultado por município, modelo com restrição:** dividiram-se com um pouco mais para o Lula em cada um (faixa larga).
- **O resultado por município, regressão das variações:** os outros candidatos meio a meio (45% e 46%).

**Leitura:** o dado agregado não separa com precisão o eleitor de cada candidato. O que ele diz com segurança é a conta do saldo: se todo voto novo fosse do Lula, ele ainda precisaria de 60,1% dos votos dos outros. Isso está dentro do que aconteceu em 2002 e 2018 (veja abaixo), mas acima do que as pesquisas de 2026 indicavam. A diferença entre "o que as pesquisas diziam desses eleitores" e "o que o resultado exige" é um dos pontos que a lente F levanta, e é real. Se os eleitores dos outros foram como as pesquisas diziam, o Lula precisou de troca direta de voto (gente que votou Flávio no 1º turno e Lula no 2º). Isso tem precedente: em 2006, o Alckmin teve **menos votos no 2º turno do que no 1º** (2,43 milhões a menos, nos municípios do Brasil; conferido em `ferramentas/validacao-independente.py`).

| Eleição | Votos dos outros no 1º turno | Para o PT | Para o adversário | Branco, nulo ou faltou | Pela regressão (PT e adversário) |
|---|---|---|---|---|---|
| 2002 | 25,78 milhões | 58% | 30% | 12% | 70% e 20% |
| 2006 | 9,36 milhões | 48% | 23% | 29% | 51% e 30% |
| 2010 | 20,77 milhões | 37% | 42% | 20% | 43% e 40% |
| 2014 | 25,82 milhões | 34% | 56% | 10% | 49% e 44% |
| 2018 | 26,37 milhões | 58% | 28% | 15% | 83% e 16% |
| 2022 | 9,86 milhões | 37% | 41% | 22% | 45% e 44% |
| 2026 | 9,29 milhões | 47% | 40% | 13% | 45% e 46% |

## 7. A lente da fraude: cada alegação, na versão mais forte, testada

O mapa das alegações (quem disse, onde, com o link) está em `dados/agentes/alegacoes_fraude_2026.md`. Cada teste usa as eleições de 2002 a 2022, que ninguém contesta, como régua, e o mesmo teste para o Flávio como espelho.

| Alegação (versão mais forte) | O que precisaria aparecer no dado | O que o dado mostra | Régua de 2002 a 2022 |
|---|---|---|---|
| **(a) As pesquisas e o mercado erraram demais** | erro fora da distribuição histórica | erro de 5,2 pontos na frente: o 2º maior do Brasil, mas superado em 10 de 41 segundos turnos | o lado do erro (mais à direita no 2º turno) é o mesmo de 2014 e 2018 |
| **(b) Nunca houve virada; Minas sempre acerta** | regra que vale também com frente pequena | as 7 eleições de presidente nunca tiveram frente pequena; com frente parecida, o líder perdeu 23 de 49 | Minas no 2º turno acertou de novo |
| **(c) A abstenção caiu demais, "surgiram" votos** | eleitor novo indo quase todo para um lado; queda concentrada onde o Lula é forte | onde o comparecimento subiu, o eleitor a mais se dividiu 51% para o Lula e 45% para o Flávio; a queda da abstenção quase não acompanha a força do Lula (correlação -0,06) | queda entre os turnos inédita; o nível do 2º turno é parecido com o de 2006 |
| **(c) Votos sem origem** | ganho que não cabe no que estava livre no município | 15.636 votos do Lula em 291 municípios (0,36% da frente); Flávio 228 | em 2006, numa eleição sem contestação, o PT teve 988.514 (4,8% da frente) |
| **(d) A prorrogação até 19h decidiu** | votos depois das 17h da ordem da frente | sem nenhum voto do Lula em Salvador, Feira de Santana e Lauro de Freitas, ele ainda venceria por 2,95 milhões. Os logs contados por terceiros dão 35.521 votos depois das 17h no país (g1/TV Globo) | a campanha do Flávio também pediu prorrogação (SP, PR e SC) |
| **(e) A pausa e a virada da noite** | curva que a ordem de chegada não explica | o Flávio liderou de 13,65% a 47,24% das seções (maior frente: 1,02 ponto); o Lula passou às 20:24 | em 2022 o Bolsonaro liderou até 68% das seções, com frente de até 4,0 pontos |
| **(g) Comparecimento estranho** | municípios com comparecimento perto de 100% e voto quase todo num lado | nenhum município acima de 95% de comparecimento | 2014 teve 6 no 2º turno |
| **Subida fora do padrão** | municípios em que a variação não segue a composição do 1º turno | 54 municípios fora de 4 desvios; a composição do 1º turno explica 80% da variação | 2022: 62 e 81% |
| **(h) Exterior** | saldo do exterior da ordem da frente | saldo de 28.657 votos; sem o exterior, frente de 4,40 milhões. A subida do Lula no exterior (+6,3) foi quase igual à do Brasil (+6,6) | urnas fora do país, apuradas à parte |
| **(f) Urna, código, logs, boletins** | divergência de assinatura, de RDV ou do teste de integridade | **não testado aqui** (é seção a seção: projeto do vídeo 16). O TSE publicou o teste de integridade sem divergência | |

**O que a lente F acerta, e fica de pé:** (1) a surpresa é real: nenhum dos três pilares dava o Lula como favorito; (2) todas as pesquisas erraram para o mesmo lado, e o erro do Brasil é o 2º maior desde 2002; (3) a queda da abstenção entre os turnos não tem precedente; (4) o que as pesquisas diziam dos eleitores de Renan e Caiado não combina bem com o que o resultado exige; (5) a parte seção a seção (logs, boletins, horário) não está neste projeto.

## 8. A lente do resultado legítimo

| Se foi legítimo, esperaria-se | O dado |
|---|---|
| uma chance real de virada antes da votação | 39% pelos três pilares |
| erro de pesquisa já visto | erro do mesmo tamanho em 2002; maior em 10 de 41 segundos turnos pelo mundo |
| votos fechando | fecham no voto |
| subida espalhada | o Lula subiu nos 27 estados e em 5.491 de 5.571 municípios, com a segunda menor variação entre municípios da série |
| eleitor novo dividido, sem lado único | 51% e 45% |
| apuração com a forma de sempre | a mesma virada na contagem de 2022, mais cedo e menor |

**O que a lente L não explica bem:** por que **nenhuma** das 53 pesquisas chegou no número; e por que a abstenção caiu tanto. A hipótese mais citada é o filtro de eleitor provável: no Datafolha da véspera, o eleitor de alta propensão a votar dava Flávio 52 a 48, e o de média e baixa, Lula 52 a 48; se mais gente de baixa propensão votou, o erro vai para o lado que aconteceu. Isso combina com a queda da abstenção, mas **não está provado**.

## 9. Juntando tudo

**O dado sustenta mais a lente do resultado legítimo**, com estes graus de confiança:
- **Alta confiança:** nenhum dos testes que este projeto consegue fazer com o resultado oficial por município mostra 2026 fora do padrão das eleições de 2002 a 2022, e os tetos de pior caso (prorrogação, exterior, votos sem origem) ficam muito abaixo da frente de 4,43 milhões.
- **Média confiança:** a chance antes da votação era de cerca de 39%. O número muda alguns pontos conforme as escolhas (de 30% a 53% nas variantes), mas em nenhuma fica abaixo de 1 em 4.
- **O que fica aberto:** o seção a seção (vídeo 16) e o porquê do erro das pesquisas.

## 10. Validação

22 de 22 números centrais refeitos por outro caminho (`ferramentas/validacao-independente.py`). Os números trazidos pelas pesquisas de apoio só entram depois de conferidos na página de origem por `ferramentas/conferir-agentes.py` (texto guardado em `dados/brutos/capturas/agentes/`). Totais por UF e por município fecham com diferença zero.
