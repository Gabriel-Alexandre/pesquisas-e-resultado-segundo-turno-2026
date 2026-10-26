# Plano do projeto (vídeo longo 19)

**26/10/2026.** O pedido, nas palavras do autor: *"analisar como as pesquisas vinham indicando uma coisa [...] e comparar isso com o resultado"*, as regras que *"normalmente sempre aconteciam"* (o líder do 1º turno vence, quem ganha Minas ganha, nunca houve virada), *"em quantos estados o Lula virou voto"*, a abstenção, os votos nulos, *"dos votos dos outros candidatos [...] quanto desses votos foram para cada candidato"*, governador contra presidente no mesmo estado, e *"a probabilidade disso acontecer [...] considere que a eleição ainda não aconteceu"*, feita em dois sentidos: *"considerando que o resultado da eleição foi fraude, e outra, considerando que o resultado da eleição foi justo"*.

🔴 **Sem pré-registro, por decisão dele:** *"não quero definir regras antes, não. Eu vou ir fazendo esse relatório junto com você, a gente vai inteirando, vai melhorando"*. O projeto anda por rodadas; cada rodada e o que mudou nela ficam em [`RODADAS.md`](RODADAS.md). Todo número continua saindo de script, com fonte e hash.

## Perguntas e de onde sai cada resposta

| Pergunta | Dado | Script |
|---|---|---|
| O que as pesquisas davam e quanto erraram | pesquisas de 2º turno registradas no TSE, conferidas no registro e numa segunda fonte | `capturar-pesquisas.py`, `conferir-pesquisas.py` |
| O erro já tinha acontecido? | erro das últimas pesquisas por instituto, 2014 a 2026 (projetos anteriores do canal) | `copiar-referencias.py` |
| As regras do histórico | resultado do TSE de 1989 a 2022 (presidente e governador) | `copiar-referencias.py`, `analise/modelo.py` |
| Quem venceu em cada estado e município, e quem virou | resultado oficial final do TSE por UF e por município, nos dois turnos | `coletar.py`, `derivar.py` |
| Abstenção, branco e nulo | o mesmo, e a série de 2002 a 2022 | idem |
| Para onde foram os votos dos outros candidatos | inferência ecológica com os 5.571 municípios | `analise/modelo.py` (`transferencia`) |
| Governador contra presidente | resultado de governador (1º e 2º turno) e coligação do eleito | `derivar.py`, `analise/modelo.py` |
| A probabilidade antes da votação | pesquisas e o erro histórico, o histórico do 1º turno, a Polymarket | `analise/modelo.py` (`probabilidades`) |
| As duas lentes (legítimo e fraude) | testes com espelho para os dois candidatos | `analise/modelo.py` (`testes_das_lentes`), `docs/LEITURA_DA_IA.md` |

## O que fica fora (e onde mora)

A apuração seção a seção, a hora de chegada dos boletins, a pausa da votação e os registros das urnas são o projeto do vídeo longo 16, [`investigacao-segundo-turno-2026`](https://github.com/Gabriel-Alexandre/investigacao-segundo-turno-2026).
