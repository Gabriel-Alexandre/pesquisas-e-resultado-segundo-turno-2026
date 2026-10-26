"""Refaz os números centrais por outro caminho, sem importar analise/modelo.py, direto dos arquivos brutos do TSE e das
capturas, e compara com resultados/RESUMO.json. Publicar só com 100% passando.
Uso: python ferramentas/validacao-independente.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TSE = RAIZ / "dados" / "brutos" / "tse"


def ler(p: Path) -> dict:
    b = p.read_bytes()
    try:
        return json.loads(b.decode("utf-8"))
    except UnicodeDecodeError:
        return json.loads(b.decode("latin-1"))


def votos(d: dict) -> dict:
    out = {}
    for a in d["carg"][0]["agr"]:
        for p in a["par"]:
            for c in p["cand"]:
                out[c["n"]] = int(c["vap"])
    return out


def main() -> None:
    R = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
    checks = []

    def conf(nome, a, b, tol=1e-6):
        ok = abs(a - b) <= tol
        checks.append((nome, a, b, ok))

    b1, b2 = ler(TSE / "6257" / "br.json"), ler(TSE / "6258" / "br.json")
    v1, v2 = votos(b1), votos(b2)
    conf("Lula ganhou do 1º para o 2º turno", v2["13"] - v1["13"], R["resultado"]["variacao"]["lula"])
    conf("Flávio ganhou do 1º para o 2º turno", v2["22"] - v1["22"], R["resultado"]["variacao"]["flavio"])
    vv2 = int(b2["v"]["vv"])
    conf("Lula nos válidos, 2º turno", 100 * v2["13"] / vv2, R["resultado"]["t2"]["lula_pct"])
    conf("abstenção caiu", int(b1["e"]["a"]) - int(b2["e"]["a"]), -R["resultado"]["variacao"]["abstencao"])
    # estados que viraram, lendo os arquivos de cada UF
    viradas = []
    for f in sorted((TSE / "6258").glob("*.json")):
        if f.stem in ("br", "zz"):
            continue
        a, b = votos(ler(TSE / "6257" / f.name)), votos(ler(f))
        if (a["13"] > a["22"]) != (b["13"] > b["22"]):
            viradas.append(f.stem)
    conf("estados que viraram (quantos)", len(viradas), len(R["estados"]["viraram"]), 0)
    checks.append(("estados que viraram (quais)", ",".join(viradas), ",".join(x["uf"] for x in R["estados"]["viraram"]),
                   viradas == [x["uf"] for x in R["estados"]["viraram"]]))
    # municípios que viraram, lendo os arquivos de cada município
    n_f_l = n_l_f = 0
    for f in (TSE / "6258" / "mun").glob("*/*.json"):
        if f.parent.name == "zz":
            continue
        a, b = votos(ler(TSE / "6257" / "mun" / f.parent.name / f.name)), votos(ler(f))
        n_f_l += a["22"] > a["13"] and b["13"] > b["22"]
        n_l_f += a["13"] > a["22"] and b["22"] > b["13"]
    conf("municípios de Flávio para Lula", n_f_l, R["municipios"]["viradas"].get("Flávio para Lula", 0), 0)
    conf("municípios de Lula para Flávio", n_l_f, R["municipios"]["viradas"].get("Lula para Flávio", 0), 0)
    # pesquisas: média da última de cada instituto, lida do CSV conferido
    linhas = list(csv.DictReader(open(RAIZ / "dados" / "derivados" / "pesquisas_2t_conferidas.csv", encoding="utf-8")))
    ult = {}
    for r in linhas:
        if r["casou"] != "True" or r["conferida"] != "True":
            continue
        inst = {"Veritá": "Verita", "Datatrends": "DataTrends"}.get(r["instituto"], r["instituto"])
        if inst not in ult or r["campo_fim"] > ult[inst]["campo_fim"]:
            ult[inst] = r
    vals = []
    for r in ult.values():
        if r["flavio_valido_publicado"]:
            vals.append(100 - float(r["flavio_valido_publicado"]))
        else:
            vals.append(100 * float(r["lula_total"]) / (float(r["lula_total"]) + float(r["flavio_total"])))
    conf("institutos com última pesquisa", len(vals), R["pesquisas"]["ultima_de_cada_instituto"]["n"], 0)
    conf("média da última de cada instituto (Lula)", sum(vals) / len(vals), R["pesquisas"]["ultima_de_cada_instituto"]["media_lula"])
    conf("nenhuma pesquisa no número da urna", float(all(
        (100 - float(r["flavio_valido_publicado"]) if r["flavio_valido_publicado"] else 100 * float(r["lula_total"]) / (float(r["lula_total"]) + float(r["flavio_total"])))
        < 100 * v2["13"] / vv2 for r in linhas if r["casou"] == "True" and r["conferida"] == "True")), float(R["pesquisas"]["nenhuma_chegou_na_urna"]), 0)
    conf("Laplace: 1 em 9", 1 / 9, R["probabilidade"]["historico_laplace"])
    # rodada 2: refeitos sem o código da análise
    erros = list(csv.DictReader(open(RAIZ / "resultados" / "erro_media_pesquisas_todos.csv", encoding="utf-8")))
    frente = R["probabilidade_v2"]["frente_flavio_pesquisas"]
    conf("segundos turnos com erro a favor do líder maior que a frente do Flávio", sum(float(e["superestimou_lider"]) > frente for e in erros),
         R["probabilidade_v2"]["pesquisas"]["casos_com_erro_maior"], 0)
    cres = list(csv.DictReader(open(RAIZ / "resultados" / "crescimento_pelos_padroes_passados.csv", encoding="utf-8")))
    conf("padrões passados em que o Lula venceria", sum(float(c["lula_pct"]) > 50 for c in cres), R["probabilidade_v2"]["crescimento"]["lula_venceria_em"], 0)
    W, pil = R["probabilidade_v2"]["pesos"], R["probabilidade_v2"]["pilares"]
    conf("chance combinada (soma dos pilares pelos pesos)", sum(W[k] * pil[k] for k in W), R["probabilidade_v2"]["combinada"])
    casos = list(csv.DictReader(open(RAIZ / "resultados" / "viradas_casos.csv", encoding="utf-8")))
    f1 = R["probabilidade_v2"]["frente_flavio_1t"]
    faixa = [c for c in casos if abs(float(c["frente_1t"]) - f1) <= 1.5 and float(c["frente_1t"]) >= 0]
    conf("viradas com frente parecida (faixa de 1,5 ponto)", sum(int(float(c["virada"])) for c in faixa), R["probabilidade_v2"]["historico"]["faixa_viradas"], 0)
    d26 = [x for x in R["de_onde"]["por_ano"] if x["ano"] == 2026][0]
    # o eleitorado de cada município muda um pouco entre os turnos (voto em trânsito); a conta fecha somando essa diferença
    mus = list(csv.DictReader(open(RAIZ / "dados" / "derivados" / "presidente_municipio.csv", encoding="utf-8")))
    d_aptos = sum(float(m["eleitores_2t"]) - float(m["eleitores_1t"]) for m in mus if m["uf"] != "zz")
    conf("ganho dos dois = votos livres + variação do eleitorado (municípios)", d26["ganho_pt"] + d26["ganho_adversario"], d26["livres_no_saldo"] + d_aptos, 1)
    import pandas as pd
    v = pd.read_parquet(RAIZ / "dados" / "copias" / "previsao-segundo-turno-2026" / "mun_votos.parquet")
    a6 = v[(v.ano == 2006) & ~v.uf.isin(["ZZ", "VT"])]
    alck = a6[a6.partido == 45].groupby("turno").votos.sum()
    checks.append(("Alckmin teve menos votos no 2º turno de 2006 que no 1º", f"{int(alck[1])} e {int(alck[2])}", "precedente de troca direta", bool(alck[2] < alck[1])))
    out = RAIZ / "resultados" / "validacao_independente.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["conta", "refeita", "resumo", "passou"])
        w.writerows(checks)
    for c in checks:
        print(("OK  " if c[3] else "FALHOU ") + c[0], c[1], c[2])
    print(f"{sum(c[3] for c in checks)} de {len(checks)} passaram")
    if not all(c[3] for c in checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
