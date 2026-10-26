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
    # rodada 4: o ganho do Lula a cada 100 eleitores nos 20% de municípios mais pobres, refeito sem o código da análise
    import pandas as pd
    rr = pd.read_csv(RAIZ / "dados" / "derivados" / "renda_municipio_censo2022.csv", dtype={"cd_ibge": str})
    mm = pd.read_csv(RAIZ / "dados" / "derivados" / "presidente_municipio.csv", dtype={"cd_ibge": str})
    mm = mm[mm.uf != "zz"].merge(rr, on="cd_ibge")
    pobres = mm[mm.renda_pc <= mm.renda_pc.quantile(0.2)]
    conf("Lula ganhou a cada 100 eleitores, 20% mais pobres", 100 * (pobres.lula_2t.sum() - pobres.lula_1t.sum()) / pobres.eleitores_1t.sum(),
         R["porque"]["renda"]["grupos"][0]["lula_ganhou_por_100"], 0.01)
    v = pd.read_parquet(RAIZ / "dados" / "copias" / "previsao-segundo-turno-2026" / "mun_votos.parquet")
    a6 = v[(v.ano == 2006) & ~v.uf.isin(["ZZ", "VT"])]
    alck = a6[a6.partido == 45].groupby("turno").votos.sum()
    checks.append(("Alckmin teve menos votos no 2º turno de 2006 que no 1º", f"{int(alck[1])} e {int(alck[2])}", "precedente de troca direta", bool(alck[2] < alck[1])))
    # rodada 5: a parte dos votos livres que o PT levou em 2022, pelo total nacional dos dois turnos (sem o painel de municípios)
    a22 = v[(v.ano == 2022) & ~v.uf.isin(["ZZ", "VT"])].groupby(["turno", "partido"]).votos.sum()
    g_pt, g_ad = a22[2][13] - a22[1][13], a22[2][22] - a22[1][22]
    camp = {c["ano"]: c for c in R["normalidade"]["campo"]}
    conf("parte do PT nos votos livres, 2022 (pontos)", 100 * g_pt / (g_pt + g_ad), camp[2022]["parte_do_pt_nos_livres_pct"], 0.5)
    # rodada 5: a variação do comparecimento em 2026, pela soma dos municípios
    m26 = pd.read_csv(RAIZ / "dados" / "derivados" / "presidente_municipio.csv")
    m26 = m26[m26.uf != "zz"]
    comp = {c["ano"]: c for c in R["normalidade"]["comparecimento"]}
    conf("comparecimento subiu do 1º para o 2º turno, 2026 (pontos)",
         100 * (m26.abstencao_1t.sum() / m26.eleitores_1t.sum() - m26.abstencao_2t.sum() / m26.eleitores_2t.sum()),
         comp[2026]["comparecimento_variou_pontos"], 0.01)
    # rodada 5: as viradas entre os 2º turnos com o líder perto de 50% (frente até 4 pontos e líder com 45% ou mais)
    vc = pd.read_csv(RAIZ / "resultados" / "viradas_casos.csv").dropna(subset=["frente_1t", "virada"])
    perto = vc[(vc.frente_1t <= 4) & (vc.lider_1t_pct >= 45)]
    ch = R["normalidade"]["chance"]["historico"]
    checks.append(("viradas com o líder perto de 50%", f"{int(perto.virada.sum())} de {len(perto)}",
                   f"{ch['perto_de_50_viradas']} de {ch['perto_de_50_casos']}",
                   int(perto.virada.sum()) == ch["perto_de_50_viradas"] and len(perto) == ch["perto_de_50_casos"]))
    # rodada 6: a conta dos 60% refeita pelo total nacional, e os municípios em que o comparecimento caiu, pelo CSV
    V = R["resultado"]["variacao"]
    falta = V["lula"] + 0.6 * V["outros_candidatos"]
    conf("conta dos 60%: parte dos votos novos (%)", 100 * falta / -(V["abstencao"] + V["branco_nulo"]),
         R["videos"]["conta_dos_60"]["parte_dos_novos_pct"], 0.01)
    cai = m26[m26.abstencao_2t >= m26.abstencao_1t]
    sn26 = [x for x in R["videos"]["sem_novos"] if x["ano"] == 2026][0]
    conf("onde o comparecimento caiu: o Lula ganhou (votos)", float((cai.lula_2t - cai.lula_1t).sum()), sn26["pt_ganhou"], 1)
    # rodada 7: municípios em que o Lula ganhou mais votos que o Flávio, pelo CSV
    q26 = [x for x in R["rodada7"]["quem_ganhou_mais"] if x["ano"] == 2026][0]
    conf("municípios em que o Lula ganhou mais votos que o Flávio", float(((m26.lula_2t - m26.lula_1t) > (m26.flavio_2t - m26.flavio_1t)).sum()),
         q26["pt_ganhou_mais_votos_em"], 0)
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
