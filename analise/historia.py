"""O 2º turno de 2026 comparado com os 2º turnos de 2002 a 2022, município a município.

Cada eleição passada serve de controle: um teste da lente da fraude só diz alguma coisa se 2026 sair do padrão das
eleições em que ninguém contesta o resultado. Em todas, "PT" é o candidato do PT e "adversário" é quem foi ao 2º turno
contra ele (2002 a 2014 PSDB; 2018 PSL; 2022 e 2026 PL).

Fontes: previsao-segundo-turno-2026 (votos e comparecimento por município, TSE, 2002 a 2026 no 1º turno e 2002 a 2022 no
2º turno; cópia com hash em dados/copias/) e o resultado oficial do 2º turno de 2026 deste projeto.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from .comum import COPIAS, DERIV
from .modelo import _ajustar

ANOS = [2002, 2006, 2010, 2014, 2018, 2022, 2026]
ADVERSARIO = {2002: 45, 2006: 45, 2010: 45, 2014: 45, 2018: 17, 2022: 22, 2026: 22}


def painel() -> pd.DataFrame:
    """Uma linha por município e eleição, com o 1º e o 2º turno lado a lado (contagens absolutas)."""
    v = pd.read_parquet(COPIAS / "previsao-segundo-turno-2026" / "mun_votos.parquet")
    d = pd.read_parquet(COPIAS / "previsao-segundo-turno-2026" / "mun_detalhe.parquet")
    v = v[~v.uf.isin(["ZZ", "VT"])]
    d = d[~d.uf.isin(["ZZ", "VT"])]
    linhas = []
    for ano in ANOS[:-1]:
        adv = ADVERSARIO[ano]
        for t in (1, 2):
            vv = v[(v.ano == ano) & (v.turno == t)]
            pt = vv[vv.partido == 13].groupby(["uf", "mun"]).votos.sum()
            an = vv[vv.partido == adv].groupby(["uf", "mun"]).votos.sum()
            tot = vv.groupby(["uf", "mun"]).votos.sum()
            dd = d[(d.ano == ano) & (d.turno == t)].set_index(["uf", "mun"])
            x = pd.DataFrame({f"pt{t}": pt, f"anti{t}": an, f"validos{t}": tot}).join(
                dd[["aptos", "abstencoes", "brancos", "nulos"]].rename(columns={"aptos": f"aptos{t}", "abstencoes": f"abs{t}"}))
            x[f"bn{t}"] = x.pop("brancos") + x.pop("nulos")
            x[f"out{t}"] = x[f"validos{t}"] - x[f"pt{t}"] - x[f"anti{t}"]
            linhas.append((ano, t, x))
    anos = []
    for ano in ANOS[:-1]:
        a = [x for (y, t, x) in linhas if y == ano]
        m = a[0].join(a[1], how="inner").fillna(0).reset_index()
        m["ano"] = ano
        anos.append(m)
    # 2026: os dois turnos deste projeto (municípios do Brasil)
    mu = pd.read_csv(DERIV / "presidente_municipio.csv", dtype={"cd_tse": str})
    mu = mu[mu.uf != "zz"]
    m26 = pd.DataFrame({"uf": mu.uf.str.upper(), "mun": mu.cd_tse.astype(int), "pt1": mu.lula_1t, "anti1": mu.flavio_1t,
                        "validos1": mu.validos_1t, "aptos1": mu.eleitores_1t, "abs1": mu.abstencao_1t,
                        "bn1": mu.brancos_1t + mu.nulos_1t, "pt2": mu.lula_2t, "anti2": mu.flavio_2t, "validos2": mu.validos_2t,
                        "aptos2": mu.eleitores_2t, "abs2": mu.abstencao_2t, "bn2": mu.brancos_2t + mu.nulos_2t, "ano": 2026})
    m26["out1"] = m26.validos1 - m26.pt1 - m26.anti1
    m26["out2"] = 0.0
    p = pd.concat(anos + [m26], ignore_index=True)
    p = p[(p.aptos1 > 0) & (p.validos2 > 0)].copy()
    return p


def _corr(a, b, w):
    a = a - np.average(a, weights=w)
    b = b - np.average(b, weights=w)
    return float(np.average(a * b, weights=w) / math.sqrt(np.average(a * a, weights=w) * np.average(b * b, weights=w)))


def testes_por_ano(p: pd.DataFrame) -> pd.DataFrame:
    """Os mesmos testes em cada eleição, para os dois lados."""
    out = []
    for ano, m in p.groupby("ano"):
        w = m.aptos1.to_numpy(float)
        margem = abs(m.pt2.sum() - m.anti2.sum())
        livre = m.out1 + (m.abs1 - m.abs2).clip(lower=0) + (m.bn1 - m.bn2).clip(lower=0)
        exc_pt = (m.pt2 - m.pt1 - livre).clip(lower=0)
        exc_an = (m.anti2 - m.anti1 - livre).clip(lower=0)
        comp1 = 100 * (1 - m.abs1 / m.aptos1)
        comp2 = 100 * (1 - m.abs2 / m.aptos2)
        pt1 = 100 * m.pt1 / m.validos1
        pt2 = 100 * m.pt2 / m.validos2
        sw = pt2 - pt1
        # o quanto a variação do PT (pontos) é explicada pela composição do 1º turno (regressão ponderada)
        X = np.column_stack([np.ones(len(m)), m.out1 / m.validos1, m.bn1 / (m.aptos1 - m.abs1), comp2 - comp1, pt1])
        beta, *_ = np.linalg.lstsq(X * np.sqrt(w)[:, None], sw.to_numpy() * np.sqrt(w), rcond=None)
        res = sw.to_numpy() - X @ beta
        r2 = 1 - np.average(res ** 2, weights=w) / np.average((sw - np.average(sw, weights=w)) ** 2, weights=w)
        sd_res = math.sqrt(np.average(res ** 2, weights=w))
        out.append({
            "ano": int(ano), "municipios": int(len(m)), "margem_final": float(margem),
            "pt_votos_sem_origem": float(exc_pt.sum()), "pt_municipios_sem_origem": int((exc_pt > 0).sum()),
            "anti_votos_sem_origem": float(exc_an.sum()), "anti_municipios_sem_origem": int((exc_an > 0).sum()),
            "pt_sem_origem_pct_da_margem": float(100 * exc_pt.sum() / margem),
            "abstencao_1t_pct": float(100 * m.abs1.sum() / m.aptos1.sum()), "abstencao_2t_pct": float(100 * m.abs2.sum() / m.aptos2.sum()),
            "comparecimento_acima_95_1t": int((comp1 > 95).sum()), "comparecimento_acima_95_2t": int((comp2 > 95).sum()),
            "variacao_pt_media": float(np.average(sw, weights=w)), "variacao_pt_desvio": float(math.sqrt(np.average((sw - np.average(sw, weights=w)) ** 2, weights=w))),
            "variacao_pt_min": float(sw.min()), "variacao_pt_max": float(sw.max()),
            "municipios_pt_caiu": int((sw < 0).sum()),
            "r2_variacao_explicada": float(r2), "desvio_residuo": float(sd_res),
            "municipios_residuo_acima_4dp": int((np.abs(res) > 4 * sd_res).sum()),
            "corr_forca_pt_1t_e_queda_abstencao": _corr(pt1, comp2 - comp1, w),
            "corr_queda_abstencao_e_ganho_pt": _corr(comp2 - comp1, sw, w),
        })
    return pd.DataFrame(out)


def transferencia_por_ano(p: pd.DataFrame) -> pd.DataFrame:
    """O mesmo modelo de transição (por região, com restrição) em cada eleição: para onde foram os votos dos outros
    candidatos, de branco e nulo e da abstenção do 1º turno."""
    reg = {"AC": "N", "AM": "N", "AP": "N", "PA": "N", "RO": "N", "RR": "N", "TO": "N", "AL": "NE", "BA": "NE", "CE": "NE", "MA": "NE",
           "PB": "NE", "PE": "NE", "PI": "NE", "RN": "NE", "SE": "NE", "DF": "CO", "GO": "CO", "MS": "CO", "MT": "CO",
           "ES": "SE", "MG": "SE", "RJ": "SE", "SP": "SE", "PR": "S", "RS": "S", "SC": "S"}
    out = []
    for ano, m in p.groupby("ano"):
        m = m.assign(r=m.uf.map(reg))
        tot = np.zeros((5, 4))
        for _, g in m.groupby("r"):
            e = g.aptos1.to_numpy(float)
            x = np.column_stack([g.pt1, g.anti1, g.out1, g.bn1, g.abs1]) / e[:, None]
            y = np.column_stack([g.pt2, g.anti2, g.bn2 + g.out2, e - g.pt2 - g.anti2 - g.bn2 - g.out2]) / e[:, None]
            t = _ajustar(x, y, e)
            tot += (x * e[:, None]).sum(axis=0)[:, None] * t
        orig = tot.sum(axis=1)
        for i, o in enumerate(["pt", "adversario", "outros", "branco_nulo", "abstencao"]):
            out.append({"ano": int(ano), "origem_1t": o, "votos_origem": float(orig[i]),
                        "para_pt_pct": 100 * tot[i, 0] / orig[i], "para_adversario_pct": 100 * tot[i, 1] / orig[i],
                        "para_branco_nulo_pct": 100 * tot[i, 2] / orig[i], "para_abstencao_pct": 100 * tot[i, 3] / orig[i]})
    return pd.DataFrame(out)


def crescimento_por_padrao_passado(p: pd.DataFrame, tr: pd.DataFrame) -> pd.DataFrame:
    """O 1º turno de 2026 com quem votou em Lula e em Flávio repetindo o voto, e os votos livres (dos outros candidatos,
    de branco e nulo e da abstenção) indo como foram em cada 2º turno passado (as proporções nacionais do modelo de
    transição daquele ano). Quem venceria?"""
    m = p[p.ano == 2026]
    livres = {"outros": m.out1.sum(), "branco_nulo": m.bn1.sum(), "abstencao": m.abs1.sum()}
    out = []
    for ano in ANOS[:-1]:
        t = tr[tr.ano == ano].set_index("origem_1t")
        pt = m.pt1.sum() + sum(livres[o] * t.loc[o, "para_pt_pct"] / 100 for o in livres)
        an = m.anti1.sum() + sum(livres[o] * t.loc[o, "para_adversario_pct"] / 100 for o in livres)
        out.append({"padrao_de": ano, "lula_pct": 100 * pt / (pt + an), "outros_para_pt_pct": float(t.loc["outros", "para_pt_pct"]),
                    "outros_para_adversario_pct": float(t.loc["outros", "para_adversario_pct"]),
                    "branco_nulo_para_pt_pct": float(t.loc["branco_nulo", "para_pt_pct"]),
                    "abstencao_para_pt_pct": float(t.loc["abstencao", "para_pt_pct"]),
                    "abstencao_para_adversario_pct": float(t.loc["abstencao", "para_adversario_pct"])})
    return pd.DataFrame(out)


def eleitores_novos(p: pd.DataFrame) -> pd.DataFrame:
    """Para cada eleição: de cada eleitor a mais que votou no 2º turno (comparecimento que subiu no município), quanto
    foi para o PT e quanto para o adversário. Regressão ponderada por município, em fração dos aptos, controlando a
    composição do 1º turno (votos dos outros candidatos e de branco e nulo). Coeficiente perto de 1 num só lado e zero no
    outro seria a marca de voto acrescentado a um candidato; a mesma conta em todas as eleições dá a régua."""
    out = []
    for ano, m in p.groupby("ano"):
        e = m.aptos1.to_numpy(float)
        dcomp = ((m.aptos2 - m.abs2) - (m.aptos1 - m.abs1)) / e
        X = np.column_stack([dcomp, m.out1 / e, m.bn1 / e, m.pt1 / e, m.anti1 / e, np.ones(len(m))])
        lin = {}
        for lado, col in (("pt", "pt"), ("adversario", "anti")):
            y = (m[f"{col}2"] - m[f"{col}1"]) / e
            beta, *_ = np.linalg.lstsq(X * np.sqrt(e)[:, None], y.to_numpy() * np.sqrt(e), rcond=None)
            lin[lado] = beta
        out.append({"ano": int(ano), "comparecimento_variou_pct": float(100 * dcomp.mul(e).sum() / e.sum()),
                    "novo_eleitor_para_pt": float(lin["pt"][0]), "novo_eleitor_para_adversario": float(lin["adversario"][0]),
                    "outros_para_pt": float(lin["pt"][1]), "outros_para_adversario": float(lin["adversario"][1]),
                    "branco_nulo_para_pt": float(lin["pt"][2]), "branco_nulo_para_adversario": float(lin["adversario"][2])})
    return pd.DataFrame(out)


def exterior(p_dir) -> pd.DataFrame:
    """Variação do PT nos válidos do 1º para o 2º turno, no Brasil e no exterior (urnas fora do país), por eleição."""
    v = pd.read_parquet(COPIAS / "previsao-segundo-turno-2026" / "mun_votos.parquet")
    out = []
    for ano in ANOS[:-1]:
        adv = ADVERSARIO[ano]
        linha = {"ano": ano}
        for nome, filtro in (("brasil", ~v.uf.isin(["ZZ", "VT"])), ("exterior", v.uf == "ZZ")):
            for t in (1, 2):
                x = v[filtro & (v.ano == ano) & (v.turno == t)]
                linha[f"{nome}_pt_{t}t"] = 100 * x[x.partido == 13].votos.sum() / x.votos.sum()
            linha[f"{nome}_variacao"] = linha[f"{nome}_pt_2t"] - linha[f"{nome}_pt_1t"]
        out.append(linha)
    ab = pd.read_csv(DERIV / "presidente_abrangencia.csv")
    linha = {"ano": 2026}
    for nome, abr in (("brasil", None), ("exterior", "zz")):
        for t in (1, 2):
            x = ab[(ab.turno == t) & ((ab.abr == abr) if abr else (~ab.abr.isin(["br", "zz"])))]
            linha[f"{nome}_pt_{t}t"] = 100 * x.lula.sum() / x.validos.sum()
        linha[f"{nome}_variacao"] = linha[f"{nome}_pt_2t"] - linha[f"{nome}_pt_1t"]
    out.append(linha)
    return pd.DataFrame(out)
