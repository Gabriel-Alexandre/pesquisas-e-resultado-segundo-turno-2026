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

### Registro da interrupção

Pedido dele: a rodada 1 ficou superficial; faltou contexto histórico (as pesquisas já erraram tanto?), a probabilidade explicada com pesos e o porquê, e mais suposições testadas na lente da fraude.

Feito, sem commit ainda: `analise/historia.py` (os mesmos testes em 2002 a 2026, município a município: votos sem origem visível, comparecimento, uniformidade da subida, eleitores novos, exterior, transferência por ano, crescimento pelos padrões passados), `analise/probabilidade.py` (três pilares com os pesos do vídeo 14: pesquisas 60%, histórico 25%, crescimento 15%), `ferramentas/conferir-agentes.py`, e o teto da prorrogação (Salvador, Feira de Santana e Lauro de Freitas: mesmo sem nenhum voto do Lula ali, ele venceria por cerca de 2,95 milhões).

Falta: conferir e incorporar as quatro pesquisas de apoio em `dados/agentes/` (2º turnos no mundo, erro das pesquisas em 2º turnos, alegações de fraude e cruzamento do voto do 1º turno), ligar tudo em `ferramentas/analise.py`, refazer relatório e gráficos, validar e publicar.

**O que dá para aprofundar numa próxima rodada, se ele quiser:**
- validar a transferência de votos com as pesquisas que perguntaram em quem a pessoa votou no 1º turno, e rodar o mesmo modelo em 2022 para medir o erro dele;
- trocar a coligação do governador pelo apoio declarado no 2º turno;
- pesquisas estaduais de presidente (onde o erro pode ter sido maior);
- testar a hipótese do filtro de eleitor provável com os microdados que os institutos publicam.
