# ESTADO: onde o trabalho parou

**Atualizado em:** 26/10/2026.

## Em uma frase

Rodada 5 publicada: o relatório responde se o que aconteceu é normal contra 2002 a 2022 (o eleitor livre indo para o Lula com quem saiu apoiando o Flávio sai do padrão, o comparecimento subindo também, a virada espalhada não) e refaz a chance antes da votação com três correções (27%, era 39%). Escopo menor que o do vídeo 16, por decisão do autor.

## O que está pronto

| Peça | Arquivo |
|---|---|
| Resultado oficial dos dois turnos (país, UFs, 5.571 municípios), governador | `dados/derivados/` (brutos fora do git, hash no manifesto) |
| 54 pesquisas de 2º turno, 53 conferidas no registro do TSE e numa segunda fonte | `dados/derivados/pesquisas_2t_conferidas.csv` |
| Contas | `resultados/RESUMO.json` e as tabelas em `resultados/` |
| Validação independente | 22 de 22 (`resultados/validacao_independente.csv`) |
| Relatório, resumo, leitura das duas lentes | `RELATORIO.md`, `RESUMO_SIMPLES.md`, `docs/LEITURA_DA_IA.md` |
| 25 gráficos 1920x1080 | `resultados/figuras/` |
| Pesquisas de apoio (alegações, erro das pesquisas no mundo, cruzamento do voto do 1º turno) | `dados/agentes/`, conferidas em `dados/derivados/*_conferido*.csv` por `ferramentas/conferir-agentes.py` |

## Próxima rodada

É o autor quem escolhe. O que dá para aprofundar está no fim de `docs/RODADAS.md`. O roteiro do vídeo 19 mora no repositório de documentação, em `referencias-conteudo/roteiros/videos-longos/VIDEO_019_PESQUISAS_E_RESULTADO_SEGUNDO_TURNO_2026/`.
