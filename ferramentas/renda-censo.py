"""Baixa do IBGE (SIDRA, tabela 10295 do Censo 2022) o rendimento médio domiciliar per capita de cada município e grava
uma tabela leve em dados/derivados/renda_municipio_censo2022.csv. O arquivo bruto fica fora do git, com o hash no manifesto.
Uso: python ferramentas/renda-censo.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analise.comum import BRUTOS, DERIV, registrar_arquivo  # noqa: E402

URL = "https://apisidra.ibge.gov.br/values/t/10295/n6/all/v/13431/p/2022/c2/6794/c86/95251/c58/95253"


def main() -> None:
    bruto = BRUTOS / "externos" / "ibge" / "renda_pc_censo2022_t10295.json"
    bruto.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(URL, headers={"User-Agent": "pesquisas-e-resultado-segundo-turno-2026"}, timeout=120)
    r.raise_for_status()
    bruto.write_bytes(r.content)
    registrar_arquivo(bruto, URL, "IBGE, Censo 2022, tabela 10295, rendimento nominal médio mensal domiciliar per capita (variável 13431)")
    d = json.loads(r.content)[1:]
    t = pd.DataFrame({"cd_ibge": [x["D1C"] for x in d], "municipio_uf": [x["D1N"] for x in d],
                      "renda_pc": pd.to_numeric([x["V"] for x in d], errors="coerce")})
    out = DERIV / "renda_municipio_censo2022.csv"
    t.to_csv(out, index=False)
    registrar_arquivo(out, "ferramentas/renda-censo.py", "derivado do arquivo do IBGE acima")
    print(len(t), "municípios;", int(t.renda_pc.isna().sum()), "sem valor")


if __name__ == "__main__":
    main()
