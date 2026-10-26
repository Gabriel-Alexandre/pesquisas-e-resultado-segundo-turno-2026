# As pesquisas, as regras e o resultado do 2º turno de 2026

Projeto aberto por trás do vídeo longo 19 do canal: o que as pesquisas davam e o que a urna deu, as regras que "sempre valiam", quem venceu em cada estado e município, a abstenção, o branco e o nulo, para onde foram os votos dos outros candidatos, governador contra presidente, e a chance que o resultado tinha **antes** da votação, lida por duas lentes (resultado legítimo e fraude).

Análise feita pelo Claude, com o resultado oficial do TSE e as pesquisas registradas no TSE.

## Por onde começar

1. [`RESUMO_SIMPLES.md`](RESUMO_SIMPLES.md): as respostas em uma tabela.
2. [`RELATORIO.md`](RELATORIO.md): tudo, com os números e de onde saíram.
3. [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md): as duas lentes e o que o dado sustenta mais.
4. [`resultados/figuras/`](resultados/figuras/): os gráficos.

## Como o projeto trabalha

Por rodadas, junto com o autor ([`docs/RODADAS.md`](docs/RODADAS.md)), sem pré-registro. Todo número sai de script, com fonte e hash do arquivo de origem em `dados/MANIFESTO.json`; os números centrais são refeitos por outro caminho em `ferramentas/validacao-independente.py`. Como refazer: [`docs/REPLICAR.md`](docs/REPLICAR.md). Fontes: [`docs/FONTES_DE_DADOS.md`](docs/FONTES_DE_DADOS.md).

A apuração seção a seção e a noite da votação são outro projeto: [`investigacao-segundo-turno-2026`](https://github.com/Gabriel-Alexandre/investigacao-segundo-turno-2026).
