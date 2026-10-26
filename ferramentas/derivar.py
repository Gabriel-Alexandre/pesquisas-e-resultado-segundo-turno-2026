"""Transforma os arquivos oficiais do TSE em tabelas leves (no git), e confere os totais.

Saídas em dados/derivados/:
- presidente_abrangencia.csv: país, UFs e exterior, 1º e 2º turno
- presidente_municipio.csv: cada município (e cada cidade do exterior), 1º e 2º turno lado a lado
- governador.csv: cada candidato a governador, 1º turno (27 UFs) e 2º turno (6 UFs), com a coligação
Conferência: a soma das UFs e do exterior = país, e a soma dos municípios = UF, em cada coluna e turno.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analise.comum import (BRUTOS, DERIV, GOV_1T, GOV_2T, PRES_1T, PRES_2T, REGIAO, UFS, UFS_GOV_2T,  # noqa: E402
                           ler_json, num, registrar_arquivo)

TSE = BRUTOS / "tse"
CAND_1T = {"13": "lula", "22": "flavio", "70": "cury", "14": "renan", "55": "caiado", "30": "zema"}


def linha(d: dict) -> dict:
    out = {"eleitores": num(d["e"]["te"]), "comparecimento": num(d["e"]["c"]), "abstencao": num(d["e"]["a"]),
           "brancos": num(d["v"]["vb"]), "nulos": num(d["v"]["tvn"]), "validos": num(d["v"]["vv"]),
           "final": d.get("tf") == "s", "secoes_pct": num(d["s"].get("pstn", d["s"].get("pst")))}
    outros = 0.0
    for c in (c for a in d["carg"][0]["agr"] for p in a["par"] for c in p["cand"]):
        nome = CAND_1T.get(c["n"])
        if nome:
            out[nome] = num(c["vap"])
        else:
            outros += num(c["vap"])
    out["outros"] = outros
    return out


def presidente() -> tuple[pd.DataFrame, pd.DataFrame]:
    ab, mu = [], []
    for turno, ele in ((1, PRES_1T), (2, PRES_2T)):
        for abr in ["br"] + list(REGIAO):
            ab.append({"turno": turno, "abr": abr, "regiao": REGIAO.get(abr, "Brasil"), **linha(ler_json(TSE / ele / f"{abr}.json"))})
        cfg = ler_json(TSE / ele / "config" / f"mun-e{int(ele):06d}-cm.json")
        for a in cfg["abr"]:
            uf = a["cd"].lower()
            for m in a["mu"]:
                mu.append({"turno": turno, "uf": uf, "cd_tse": m["cd"], "cd_ibge": m.get("cdi", ""), "municipio": m["nm"],
                           "capital": m.get("c") == "s", **linha(ler_json(TSE / ele / "mun" / uf / f"{m['cd']}.json"))})
    ab = pd.DataFrame(ab).fillna(0)
    mu = pd.DataFrame(mu).fillna(0)
    cols = ["eleitores", "comparecimento", "abstencao", "brancos", "nulos", "validos", "lula", "flavio", "cury", "renan", "caiado", "zema", "outros"]
    for t in (1, 2):
        a = ab[ab.turno == t].set_index("abr")
        soma = a.drop("br")[cols].sum()
        dif = (soma - a.loc["br", cols]).abs().max()
        m = mu[mu.turno == t].groupby("uf")[cols].sum()
        dif_mun = (m - a.loc[m.index, cols]).abs().max().max()
        print(f"turno {t}: UFs+exterior contra país, maior diferença {dif:.0f}; municípios contra UF, maior diferença {dif_mun:.0f}")
        assert dif == 0 and dif_mun == 0, "totais não fecham"
    m1 = mu[mu.turno == 1].drop(columns=["turno", "final", "secoes_pct"]).set_index(["uf", "cd_tse"])
    m2 = mu[mu.turno == 2].drop(columns=["turno", "final", "secoes_pct", "cury", "renan", "caiado", "zema", "outros", "municipio", "cd_ibge", "capital"], errors="ignore").set_index(["uf", "cd_tse"])
    lado = m1.join(m2, lsuffix="_1t", rsuffix="_2t", how="outer").reset_index()
    lado = lado.rename(columns={"cury": "cury_1t", "renan": "renan_1t", "caiado": "caiado_1t", "zema": "zema_1t", "outros": "outros_1t"})
    lado["regiao"] = lado.uf.map(REGIAO)
    return ab, lado


def governador() -> pd.DataFrame:
    out = []
    for turno, ele, ufs in ((1, GOV_1T, UFS), (2, GOV_2T, UFS_GOV_2T)):
        for uf in ufs:
            d = ler_json(TSE / ele / f"{uf}.json")
            vv = num(d["v"]["vv"])
            for a in d["carg"][0]["agr"]:
                for p in a["par"]:
                    for c in p["cand"]:
                        out.append({"uf": uf, "turno": turno, "numero": c["n"], "candidato": c["nmu"], "partido": p["sg"],
                                    "coligacao": a.get("com", ""), "votos": num(c["vap"]), "pct": 100 * num(c["vap"]) / vv if vv else 0,
                                    "situacao": c.get("st", ""), "final": d.get("tf") == "s"})
    return pd.DataFrame(out)


def main() -> None:
    DERIV.mkdir(parents=True, exist_ok=True)
    ab, mu = presidente()
    g = governador()
    for df, nome in ((ab, "presidente_abrangencia.csv"), (mu, "presidente_municipio.csv"), (g, "governador.csv")):
        p = DERIV / nome
        df.to_csv(p, index=False)
        registrar_arquivo(p, "ferramentas/derivar.py", "derivado dos arquivos do TSE em dados/brutos/tse (hash no manifesto)")
        print(nome, len(df))
    print("todos finais:", bool(ab.final.all()), "| municípios:", mu.uf.ne("zz").sum(), "| exterior:", mu.uf.eq("zz").sum())


if __name__ == "__main__":
    main()
