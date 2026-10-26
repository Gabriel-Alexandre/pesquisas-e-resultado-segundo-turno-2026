# ESTADO: onde o trabalho parou

**Atualizado em:** 26/10/2026.

## Em uma frase

Rodada 6 publicada: os 6 vídeos que circularam depois do resultado, conferidos afirmação por afirmação contra o projeto (`docs/VIDEOS_QUE_CIRCULARAM.md`); a conta dos 98% confere na aritmética e põe a estranheza no lugar errado (ela está no eleitor livre inteiro, não em quem voltou a votar). A rodada 5 segue valendo: 2 coisas fora do padrão de 2002 a 2022 e a chance antes da votação de 27%. Escopo menor que o do vídeo 16, por decisão do autor.

## O que está pronto

| Peça | Arquivo |
|---|---|
| Resultado oficial dos dois turnos (país, UFs, 5.571 municípios), governador | `dados/derivados/` (brutos fora do git, hash no manifesto) |
| 54 pesquisas de 2º turno, 53 conferidas no registro do TSE e numa segunda fonte | `dados/derivados/pesquisas_2t_conferidas.csv` |
| Contas | `resultados/RESUMO.json` e as tabelas em `resultados/` |
| Validação independente | 24 de 24 (`resultados/validacao_independente.csv`) |
| Relatório, resumo, leitura das duas lentes | `RELATORIO.md`, `RESUMO_SIMPLES.md`, `docs/LEITURA_DA_IA.md` |
| 26 gráficos 1920x1080 | `resultados/figuras/` |
| Pesquisas de apoio (alegações, erro das pesquisas no mundo, cruzamento do voto do 1º turno) | `dados/agentes/`, conferidas em `dados/derivados/*_conferido*.csv` por `ferramentas/conferir-agentes.py` |

## Próxima rodada

É o autor quem escolhe. O que dá para aprofundar está no fim de `docs/RODADAS.md`. O roteiro do vídeo 19 mora no repositório de documentação, em `referencias-conteudo/roteiros/videos-longos/VIDEO_019_PESQUISAS_E_RESULTADO_SEGUNDO_TURNO_2026/`.
