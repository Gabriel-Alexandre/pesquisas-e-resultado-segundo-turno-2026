# CLAUDE.md

Projeto de dados do vídeo longo 19 (pesquisas, regras e resultado do 2º turno de 2026). Comece pelo `ESTADO.md` e pelo `docs/RODADAS.md`.

- **Iterativo, sem pré-registro** (decisão do autor, 26/10/2026): cada rodada entra no `docs/RODADAS.md` com o que mudou e por quê.
- Todo número sai de script e do `resultados/RESUMO.json`; o relatório é escrito por `ferramentas/gerar-relatorio.py`. ⛔ número à mão.
- Antes de publicar: `validacao-independente.py` 100%, `conferir-linguagem.py` ok, `pytest` passando, gráficos abertos e olhados.
- Os dois lados sempre: toda leitura passa pela lente L (legítimo) e pela lente F (fraude), com espelho para os dois candidatos. "Fraude" só como nome de hipótese.
- ⛔ recomendação de voto, julgamento de intenção, "mentiu". Texto público sem travessão.
- Não escrever em repositório de outro projeto: ler com cópia e hash (`ferramentas/copiar-referencias.py`).
- Commit e push: o autor autorizou para esta execução; nos próximos pedidos, seguir o que ele disser.
