"""Procura no que o público lê: travessão, e palavras que o assunto não permite como conclusão.
Uso: python ferramentas/conferir-linguagem.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVOS = ["RELATORIO.md", "RESUMO_SIMPLES.md", "README.md", "docs/LEITURA_DA_IA.md", "docs/PLANO.md", "docs/RODADAS.md"]
PROIBIDO = [("—", "travessão"), (r"\bmentiu\b", "mentiu"), (r"\bfraudulent", "fraudulento"), (r"\bvote em\b", "recomendação de voto"),
            (r"\bhouve fraude\b", "fraude como conclusão"), (r"\bfoi fraudad", "fraude como conclusão")]


def main() -> None:
    erros = 0
    for nome in ARQUIVOS:
        p = RAIZ / nome
        if not p.exists():
            continue
        for i, linha in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for rx, rot in PROIBIDO:
                if re.search(rx, linha, re.I):
                    print(f"{nome}:{i}: {rot}: {linha[:120]}")
                    erros += 1
    print("ok" if not erros else f"{erros} ocorrências")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
