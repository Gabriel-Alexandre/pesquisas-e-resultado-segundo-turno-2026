# Como refazer tudo

```bash
pip install -r requirements.txt
python ferramentas/coletar.py              # TSE: ~11.600 arquivos, uns 5 minutos
python ferramentas/capturar-pesquisas.py   # Wikipedia (a lista muda com o tempo: o revid usado está no manifesto)
python ferramentas/conferir-pesquisas.py   # registro do TSE e segunda fonte
python ferramentas/copiar-referencias.py   # precisa dos outros projetos do canal ao lado (as cópias já estão no git)
python ferramentas/derivar.py
python ferramentas/analise.py
python ferramentas/validacao-independente.py
python ferramentas/graficos.py
python ferramentas/gerar-relatorio.py
python ferramentas/conferir-linguagem.py
python -m pytest -q
```
