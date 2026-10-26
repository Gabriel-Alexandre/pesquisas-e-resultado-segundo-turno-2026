# Os vídeos que circularam depois do resultado (rodada 6)

**26/10/2026.** O autor mandou 6 vídeos que circularam nas redes depois do 2º turno e pediu: *"transcrever cada um e avaliar se eles fazem sentido dado tudo que nós fizemos, se são congruentes ou se são algum outro ponto de vista que faltou a gente analisar"*. Cada vídeo foi transcrito (whisper, `ggml-large-v3-turbo`); a transcrição inteira e os arquivos ficam fora deste repositório (são de terceiros), com o hash anotado no repositório de documentação do canal. Aqui ficam só a paráfrase de cada afirmação, frases curtas entre aspas, e o que o dado deste projeto diz sobre ela. Os números novos saem de `analise/normalidade.py` (seção 4) e estão em `resultados/RESUMO.json` (`videos`).

**Legenda do veredito:** ✅ confere · ⚠️ confere o número, a conclusão não segue · ❌ não confere · ⬜ fora do escopo deste projeto · ➕ ponto de vista que faltava e entrou

---

## 1. @carlosphyll: *"os números não mentem"*, a conta dos 98%

**O que diz:** com os eleitores de Lula e Flávio repetindo o voto e 60% dos votos dos outros candidatos indo para o Lula, faltariam 4,7 milhões de votos para o crescimento dele; isso seria 98% dos votos "extras" (abstenção e branco e nulo que caíram), *"algo que nunca aconteceu na história"*.

| Afirmação | Veredito | O dado |
|---|---|---|
| Flávio 56,1 mi e Lula 53,8 mi no 1º turno; os outros 9,3 mi | ✅ | 56.104.503 · 53.879.538 · 9.316.747 |
| a abstenção caiu perto de 3 milhões, *"nunca antes"* | ✅ em parte | caiu 2,96 milhões; em 2022 já tinha caído (0,36 ponto), em 2026 caiu 1,85 ponto, a maior queda da série |
| branco e nulo caíram 1,8 milhão; "extras" 4,8 milhões | ✅ | 1,82 e 4,78 milhões |
| com 60% dos outros, faltam 4,7 milhões, 98% dos extras | ⚠️ | a conta exata dá **100%** (4.786.646 de 4.781.485); e a suposição dos 60% faz o Flávio receber os outros 40%, que são exatamente o que ele ganhou (3,73 milhões contra 3,72) |
| logo, 98% de quem voltou a votar escolheu um candidato | ⚠️ não segue | os 60% são uma escolha; o total de votos livres não diz como eles se dividem entre quem saiu e quem voltou. Duas medidas que não dependem dessa escolha: (1) nos **1.133 municípios em que o comparecimento caiu** (no saldo, ninguém novo votou), o Flávio **perdeu** 39 mil votos e o Lula ganhou 710 mil, **83%** dos votos dos outros candidatos ali; (2) nos municípios onde mais gente voltou a votar, a parte do Lula no que os dois ganharam **não sobe** (de 69% a 76% nos grupos em que o comparecimento subiu, `resultados/votos_novos_por_faixa.csv`, gráfico `g26`). Se quem voltou fosse quase todo de um lado, essa parte subiria |

**Leitura:** a aritmética é a mesma que este projeto fez (rodada 1: *"sem troca direta, o Lula precisou de pelo menos 60% dos votos dos outros"*; é o outro canto da mesma conta). A estranheza existe, mas está no eleitor livre inteiro (73,6% para o Lula, com quem saiu apoiando o Flávio; rodada 5), não especificamente em quem voltou a votar. Ponto de vista que faltava (➕): **o saldo esconde quem entrou e quem saiu.** Os 2,96 milhões são a diferença entre quem votou só no 2º turno e quem votou só no 1º; o arquivo por município não diz quantos fizeram cada coisa.

⚠️ **Duas contas simples deste projeto discordam** sobre como quem voltou a votar se dividiu: com a composição do 1º turno controlada (rodada 2), 51% Lula e 45% Flávio; só com os votos dos outros e os novos, sem constante (rodada 6), 80% e 20% (e 67% e 33% dos outros). As duas são estimativas; a leitura que não depende de modelo é a dos grupos de municípios acima.

## 2. @pietragrisotto: *"dos votos adicionais, 73,60% foram para o Lula"*

| Afirmação | Veredito | O dado |
|---|---|---|
| 73,60% dos votos adicionais para o Lula, 26,40% para o Flávio | ✅ | 73,6% (`resultado.variacao.parte_do_lula_no_ganho`) |
| isso não quer dizer que os eleitores dos outros foram 100% para um lado | ✅ | é a mesma ressalva do relatório |
| Sudeste: Lula subiu quase 8 pontos; Centro-Oeste, quase 7,5 | ✅ | +7,6 e +7,4 pontos nos válidos |
| por isso é improvável: teria de trazer muito do eleitor de Zema, Caiado, Cury e Renan | ⚠️ | é a mesma estranheza que a rodada 5 mediu contra 2002 a 2022 (fora do padrão); "improvável" não é "impossível": em 2022 o eleitor de quem apoiou o Lula foi 70% para o Bolsonaro. E o Lula subir mais em pontos no Sudeste e no Centro-Oeste é esperado: era onde havia mais votos livres (o Flávio também subiu 3,5 pontos no Centro-Oeste) |
| a prorrogação foi decisão de um ministro do STF (Zanin), sozinho, e não do TSE | ✅ | Poder360, Conjur e O Tempo, 25/10 |
| *"isso aconteceu em 2015 na Venezuela, com a diferença que eles não conseguiram virar votos"* | ✅ em parte | nas parlamentares de 6/12/2015, o CNE estendeu a votação em 1 hora, e a oposição (MUD) chamou de ilegal; a oposição venceu a eleição. A comparação diz que houve prorrogação nos dois; não mostra efeito de prorrogação em voto |

## 3. Nikolas Ferreira (via Metrópoles): as *"primeiras vezes"* e a prudência

| Afirmação | Veredito | O dado |
|---|---|---|
| 1ª vez uma virada; 1ª vez que quem ganha o 1º turno perde | ✅ | o líder do 1º turno de presidente tinha vencido 7 de 7 (1989 a 2022) |
| 1ª vez que quem perdeu Minas venceu | ✅ no 1º turno | quem venceu Minas no 1º turno venceu 8 de 8 até 2022, e o Flávio venceu Minas no 1º turno; no 2º turno o Lula venceu Minas, e a regra do 2º turno (6 de 6) valeu |
| 1ª vez que uma eleição é prorrogada, e pelo ex-advogado do candidato | ✅ | 1ª prorrogação nacional (O Tempo e Rádio Senado, 25 e 26/10); o ministro Cristiano Zanin foi advogado do Lula |
| *"São muitas primeiras vezes"* para ignorar | ⚠️ | as 3 primeiras são **o mesmo fato** (o Lula vencer uma disputa em que o Flávio liderou o 1º turno e Minas): se ele vence, as 3 acontecem juntas. Somá-las como coincidências é o erro da conta que multiplica (rodada 2). A prorrogação é o único fato separado, e é verdadeira; o efeito dela em voto é do projeto do vídeo 16 (os votos depois das 17h foram 34.810, 0,79% da diferença) |
| *"a chance de anular essa eleição é praticamente nula"*; não ir para a rua no calor da emoção | ⬜ | opinião e conselho, fora do que o dado mede |

## 4. @igor.bevilaqua: o mercado no dia seguinte

| Afirmação | Veredito | O dado |
|---|---|---|
| a bolsa caiu mais de 10% e acionou o circuit breaker | ✅ | B3 acionou o circuit breaker na manhã de 26/10 com queda de 10% (Tribuna do Norte, InfoMoney, Metrópoles) |
| 1º circuit breaker desde a pandemia | ⚠️ | o InfoMoney diz que foi o 1º desde março de 2020; o fechamento do dia e o resto (dólar, leilões do Tesouro, os R$ 300 bilhões) são do projeto do vídeo 18 (`economia-brasil-2027-2030`), que espera o fechamento |
| *"Pela primeira vez na história do país, uma apuração pausada"* | ⚠️ | o que houve foi a votação prorrogada e a divulgação segurada até as 19h06 (InfoMoney e Terra, 25/10); a pausa da apuração foi no 1º turno (projeto do vídeo 8) |

⬜ **Fora do escopo:** o mercado é o assunto do vídeo 18. Fica registrado aqui para não se perder.

## 5. @ale_paschalis: a lousa, *"a conta não fecha"*

**O que diz:** os votos a mais dos dois têm de vir dos votos válidos que aumentaram (4,78 milhões) e dos votos dos outros candidatos (9,32 milhões); mesmo dando ao Lula 100% do aumento, ele precisaria de 5,6 milhões dos outros; como Cury, Renan, Caiado e Zema *"são todos de direita"* e o eleitor do Cury *"jamais votaria no Lula"*, a conta não fecharia.

| Afirmação | Veredito | O dado |
|---|---|---|
| os números da lousa (válidos, Flávio, Lula, outros, e as diferenças) | ✅ | 119.300.788 e 124.082.273 válidos; +3,72 e +10,38 milhões |
| o que os dois ganharam é exatamente o aumento dos válidos mais os votos dos outros | ✅ | é a conta que abre este relatório (14,10 milhões dos dois lados) |
| com 100% do aumento para o Lula, ele ainda precisaria de 5,6 milhões dos outros | ✅ | 10.376.694 − 4.781.485 = 5.595.209, 60% dos votos dos outros; é o número da rodada 1 deste projeto |
| quem votou no Cury *"jamais votaria no Lula"* | ❌ | nas 5 pesquisas que cruzaram o voto do 1º turno, o eleitor do Cury dava, entre os dois, 53% ao Lula (de 36% a 67% conforme o instituto); o do Renan, 40%; o do Caiado, 38% |
| logo, a conta não fecha | ⚠️ | com o que as pesquisas diziam desse eleitor, o Lula não chegaria aos 60% (rodada 5: o Flávio venceria por 2,66 milhões); é o mesmo achado deste projeto, o eleitor livre foi mais para o Lula do que as pesquisas e os apoios indicavam, e fica fora do padrão de 2002 a 2022. "Não fecha" no sentido de "impossível" não segue: em 2022 o eleitor de quem apoiou o Lula foi 70% para o Bolsonaro, o mesmo tamanho de desvio no sentido contrário |

⛔ O fim do vídeo tem palavrão; não entra em nenhum trecho.

## 6. Tarcísio de Freitas: a simulação de Monte Carlo, antes do resultado

**O que diz** (vídeo gravado antes da apuração): com os dados do TSE por UF, a taxa de conversão de 2022 (*"os votos do segundo turno no candidato A, menos os votos do primeiro turno no candidato A, dividido pelos votos do primeiro turno dos outros candidatos"*), aplicada ao 1º turno de 2026 com um fator aleatório normal e milhares de repetições, dá o Flávio com 52,6% a 52,7% (*"90% das ocorrências"* entre 51,8% e 53,6%), cerca de 63 milhões de votos contra 57 milhões.

| Afirmação | Veredito | O dado |
|---|---|---|
| o método (taxa de conversão de 2022 por UF, aplicada a 2026) | ✅ reproduzido | `analise/normalidade.py` (`simulacao_com_as_taxas_de_um_ano`), com o fator aleatório normal de desvio 0,2 e 10 mil repetições: **Lula 47,4%, Flávio 52,6%**, Flávio 62,8 milhões e Lula 56,6 milhões; o Lula vence em 0 de 10 mil. É o número dele |
| 90% das vezes entre 51,8% e 53,6% para o Flávio | ⚠️ | a urna deu 48,2%, fora da faixa. O fator aleatório só varia o tamanho das taxas de 2022 em volta delas mesmas; não cobre a chance de 2026 se comportar diferente de 2022. **O mesmo método com outro ano-base dá outra eleição:** 2002 Lula 48,8%; **2006 Lula 55,6%** (vence em 10 mil de 10 mil); 2010 48,4%; 2014 48,2%; **2018 50,0%** (vence em metade); 2022 47,4% |
| ➕ o ponto de vista | ✅ congruente | é o pilar do crescimento deste projeto (rodadas 2 e 5) com um ano só: o padrão de 2022 dá Flávio, como os anos em que quem saiu era de centro ou de direita (0 de 3 na rodada 5). A incerteza que falta na faixa dele é justamente a de qual padrão vale, e em 2026 o eleitor livre se comportou como nos anos em que quem saiu era da esquerda |
