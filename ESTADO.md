# ESTADO: onde o trabalho parou

**Atualizado em:** 26/10/2026.

## Em uma frase

Rodada 4 publicada: o relatório abre com de onde vieram os 10,38 milhões do Lula e o que justifica a virada (o eleitor de direita, a renda do município, onde ela aconteceu, a tendência das pesquisas), seguido da chance em três pilares e das duas lentes. Escopo menor que o do vídeo 16, por decisão do autor.

## O que está pronto

| Peça | Arquivo |
|---|---|
| Resultado oficial dos dois turnos (país, UFs, 5.571 municípios), governador | `dados/derivados/` (brutos fora do git, hash no manifesto) |
| 54 pesquisas de 2º turno, 53 conferidas no registro do TSE e numa segunda fonte | `dados/derivados/pesquisas_2t_conferidas.csv` |
| Contas | `resultados/RESUMO.json` e as tabelas em `resultados/` |
| Validação independente | 19 de 19 (`resultados/validacao_independente.csv`) |
| Relatório, resumo, leitura das duas lentes | `RELATORIO.md`, `RESUMO_SIMPLES.md`, `docs/LEITURA_DA_IA.md` |
| 22 gráficos 1920x1080 | `resultados/figuras/` |
| Pesquisas de apoio (alegações, erro das pesquisas no mundo, cruzamento do voto do 1º turno) | `dados/agentes/`, conferidas em `dados/derivados/*_conferido*.csv` por `ferramentas/conferir-agentes.py` |

## Próxima rodada

É o autor quem escolhe. O que dá para aprofundar está no fim de `docs/RODADAS.md`. O roteiro do vídeo 19 é pedido à parte, no repositório de documentação.
