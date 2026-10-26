# Rodadas

O relatório é feito junto com o autor, rodada por rodada. Cada rodada diz o que foi feito e o que mudou.

## Rodada 1 · 26/10/2026

Primeira versão de tudo o que o pedido lista: pesquisas contra a urna, o erro histórico, as regras, estados e municípios, abstenção, branco e nulo, transferência de votos (estimativa), governador contra presidente, a probabilidade antes da votação e as duas lentes. Validação independente dos números centrais.

## Rodada 2 · 26/10/2026

O que mudou, pelo retorno dele (*"faltou mais criticidade no sentido de analisar o histórico, de analisar a probabilidade"*; a lente da fraude *"não testou suposições suficientes"*):
- **A chance virou uma conta explicada em três pilares**, com os pesos que ele escolheu no vídeo 14 (pesquisas 60%, histórico 25%, crescimento 15%), cada pilar pela contagem de casos passados, mais variantes de sensibilidade e o erro de multiplicar coincidências.
- **O erro das pesquisas comparado com a história:** os 2º turnos de presidente no Brasil de 2002 a 2022 e 35 de outros países (187 pesquisas conferidas número a número na fonte), mais os 39 de governador no Brasil.
- **Os mesmos testes em todas as eleições de 2002 a 2022**, município a município, como régua para a lente da fraude: votos sem origem, eleitor novo, comparecimento, subida fora do padrão, exterior, transferência por ano, crescimento pelos padrões passados, curva da apuração contra 2022 e o teto da prorrogação.
- **As alegações de fraude mapeadas na versão mais forte** (`dados/agentes/alegacoes_fraude_2026.md`) e testadas uma a uma.
- **O que as pesquisas diziam dos eleitores de Cury, Renan e Caiado** (44 números conferidos na fonte), contra o que o resultado exige.

O texto abaixo foi o registro da interrupção pelo limite de uso, mantido como histórico.

## Rodada 3 · 26/10/2026 (de onde vieram os 10,38 milhões)

Pedido dele: *"de onde veio os 10 milhões de votos que o Lula teve a mais [...] Você tá ficando muito em cima do muro"*. Entrou no topo do relatório a conta das três origens (eleitores dos outros candidatos, quem não tinha votado em ninguém, eleitores do Flávio que mudaram), por três ajustes que concordam, com o teste do método em 2006 (quando a troca de voto existiu e ele a encontra), a parte dos votos livres que o PT levou em cada eleição e onde o ganho aconteceu.

## Rodada 4 · 26/10/2026 (o que justifica a virada)

Pedido dele: o que justifica a virada (as medidas do governo, o eleitor de direita dos candidatos derrotados, onde ela aconteceu, os votos depois das 17h), e se o resultado é suspeito demais. Com a ressalva dele: *"o vídeo [...] tem um escopo mais reduzido se comparado ao vídeo 16"*, e o pedido de fazer pelo caminho mais simples (*"poderia ser bem mais simples e mais rápido"*): no lugar das bases de Bolsa Família e MEI por município, a renda per capita do Censo 2022.

Entrou no relatório a seção "O que justifica a virada": os fatos com link (apoios, medidas, transporte), o eleitor de direita em 5 grupos de município, a virada por renda, por região e por município, a tendência das pesquisas de 2014 a 2026, e o número dos votos depois das 17h publicado pelo vídeo 16 (34.810).

## Rodada 5 · 26/10/2026 (isso é normal? e a chance refeita)

Pedido dele: *"é normal, tendo em vista que os candidatos eram de direita, que a maior parte dos votos vá para o Lula? Nas outras eleições, isso aconteceu de verdade?"*, se é normal o comparecimento subir e a virada se espalhar por 5 mil municípios, e *"nesses 39% [...] tudo isso foi calculado com peso de forma correta, provavelmente essa probabilidade era bem mais baixa"*.

O que entrou (`analise/normalidade.py`, seção "Rodada 5" do relatório, gráficos g23 a g25):
- **A posição de cada candidato eliminado no 2º turno, de 2002 a 2026, com link** (`dados/agentes/apoios_segundo_turno.csv`, 27 de 28 com fonte), posta ao lado da parte dos votos livres que o PT levou. Resultado: 2026 sai do padrão (com quem saiu apoiando o adversário, o PT nunca tinha passado de 43%), e o espelho é 2022 (quem saiu apoiou o Lula e o Bolsonaro levou 70% dos livres).
- **O comparecimento e o espalhamento da virada em todas as eleições.** O comparecimento sempre caiu no 2º turno até 2018; subiu em 2022 e subiu 5 vezes mais em 2026. A virada em quase todos os municípios é o que acontece quando a diferença anda muito no país (2006 também).
- **A chance refeita, com três correções:** o histórico passa a olhar o quanto o líder estava perto de 50% (47% para 38%); o crescimento passa a usar só os anos em que quem saiu era de centro ou de direita (33% para 20%); e os pilares passam a ser somados como indícios (Bayes), no lugar da média com pesos. Central: **27%** (era 39%), ponta de baixo 8%, mercado 24%. O pilar das pesquisas não cai.
- 🔧 **Correção da rodada 3:** os "cerca de 6 milhões" vindos dos eleitores dos outros candidatos são de um dos dois modelos do projeto; o outro dá 4,4 milhões. A divisão entre quem saiu e quem voltou a votar fica como faixa (4,4 a 6,6 milhões); o total é exato.
- Validação: mais 3 contas refeitas por outro caminho (22 de 22).

## Rodada 6 · 26/10/2026 (os vídeos que circularam)

Pedido dele: *"transcrever cada um e avaliar se eles fazem sentido dado tudo que nós fizemos, se são congruentes ou se são algum outro ponto de vista que faltou a gente analisar"*, sobre 6 vídeos (Tarcísio de Freitas, Nikolas Ferreira e 4 criadores no TikTok).

O que entrou: a análise afirmação por afirmação em `docs/VIDEOS_QUE_CIRCULARAM.md`; a conta dos 60% refeita; os municípios em que o comparecimento caiu (onde ninguém novo votou, no saldo) de 2002 a 2026; os municípios em 5 grupos pela mudança do comparecimento (gráfico g26); a divisão simples entre os votos dos outros e os novos em todos os anos; e o aviso de que duas contas simples do projeto discordam sobre quem voltou a votar. Validação: mais 2 contas refeitas (24 de 24).

## Rodada 7 · 26/10/2026 (o espalhamento contra a série, e o Bolsa Família nas pesquisas)

Pelo retorno dele ao roteiro: se é normal o Lula ganhar mais votos que o Flávio em tantos municípios e até no Sul, e se o Bolsa Família, tendo efeito grande, já não apareceria nas pesquisas. Entrou: em quantos municípios o PT ganhou mais votos que o adversário em cada eleição e a parte do PT no ganho por região (2026 só perde para 2006), e a mesma empresa de pesquisa antes e depois de 19/10 (o Lula subiu 0,25 ponto em média em 13 institutos).

### Registro da interrupção

Pedido dele: a rodada 1 ficou superficial; faltou contexto histórico (as pesquisas já erraram tanto?), a probabilidade explicada com pesos e o porquê, e mais suposições testadas na lente da fraude.

Feito, sem commit ainda: `analise/historia.py` (os mesmos testes em 2002 a 2026, município a município: votos sem origem visível, comparecimento, uniformidade da subida, eleitores novos, exterior, transferência por ano, crescimento pelos padrões passados), `analise/probabilidade.py` (três pilares com os pesos do vídeo 14: pesquisas 60%, histórico 25%, crescimento 15%), `ferramentas/conferir-agentes.py`, e o teto da prorrogação (Salvador, Feira de Santana e Lauro de Freitas: mesmo sem nenhum voto do Lula ali, ele venceria por cerca de 2,95 milhões).

Falta: conferir e incorporar as quatro pesquisas de apoio em `dados/agentes/` (2º turnos no mundo, erro das pesquisas em 2º turnos, alegações de fraude e cruzamento do voto do 1º turno), ligar tudo em `ferramentas/analise.py`, refazer relatório e gráficos, validar e publicar.

**O que dá para aprofundar numa próxima rodada, se ele quiser:**
- validar a transferência de votos com as pesquisas que perguntaram em quem a pessoa votou no 1º turno, e rodar o mesmo modelo em 2022 para medir o erro dele;
- trocar a coligação do governador pelo apoio declarado no 2º turno;
- pesquisas estaduais de presidente (onde o erro pode ter sido maior);
- testar a hipótese do filtro de eleitor provável com os microdados que os institutos publicam.
