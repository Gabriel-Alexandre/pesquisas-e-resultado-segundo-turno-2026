"""Rodada 4: o porquê da virada. Onde ela aconteceu e quanto cada lugar pesou, o eleitor dos candidatos de direita, a
tendência das pesquisas ao longo do 2º turno (2014 a 2026) e, com as bases externas, as medidas do governo.

Toda conta é feita do mesmo jeito para os dois candidatos e, quando há dado, para 2022 como régua.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .comum import COPIAS, DERIV, REGIAO

DIA = {2014: "2014-10-26", 2018: "2018-10-28", 2022: "2022-10-30", 2026: "2026-10-25"}
URNA_PT = {2014: 51.64, 2018: 44.87, 2022: 50.90}
ADV = {2014: 45, 2018: 17, 2022: 22}


def _mun() -> pd.DataFrame:
    m = pd.read_csv(DERIV / "presidente_municipio.csv", dtype={"cd_tse": str, "cd_ibge": str})
    m = m[m.uf != "zz"].copy()
    m["margem_1t"] = m.lula_1t - m.flavio_1t
    m["margem_2t"] = m.lula_2t - m.flavio_2t
    m["virada_margem"] = m.margem_2t - m.margem_1t          # quanto a diferença Lula menos Flávio andou para o Lula
    m["regiao"] = m.uf.map(REGIAO)
    m["direita_1t"] = m.renan_1t + m.caiado_1t + m.zema_1t
    return m


def onde_a_virada(m: pd.DataFrame | None = None) -> dict:
    """A diferença nacional andou de Flávio +2,22 mi para Lula +4,43 mi. Quanto dessa mudança veio de cada região, estado,
    tamanho de cidade, e dos municípios que trocaram de vencedor."""
    m = _mun() if m is None else m
    total = float(m.virada_margem.sum())
    porte = pd.cut(m.eleitores_1t, [0, 20_000, 100_000, 500_000, 1e9], labels=["até 20 mil eleitores", "20 a 100 mil", "100 a 500 mil", "mais de 500 mil"])
    viraram = (np.sign(m.margem_1t) < 0) & (np.sign(m.margem_2t) > 0)
    out = {"virada_total": total, "margem_1t": float(m.margem_1t.sum()), "margem_2t": float(m.margem_2t.sum())}

    def bloco(g):
        s = m.groupby(g, observed=True).agg(virada=("virada_margem", "sum"), eleitores=("eleitores_1t", "sum"))
        s["parte_da_virada_pct"] = 100 * s.virada / total
        s["parte_do_eleitorado_pct"] = 100 * s.eleitores / m.eleitores_1t.sum()
        return s.reset_index().to_dict("records")

    out["por_regiao"] = bloco("regiao")
    out["por_uf"] = sorted(bloco("uf"), key=lambda x: -x["virada"])
    out["por_porte"] = bloco(porte)
    out["capitais"] = {"virada": float(m[m.capital].virada_margem.sum()), "parte_pct": float(100 * m[m.capital].virada_margem.sum() / total)}
    out["municipios_que_viraram"] = {"quantos": int(viraram.sum()), "virada": float(m[viraram].virada_margem.sum()),
                                     "parte_pct": float(100 * m[viraram].virada_margem.sum() / total)}
    out["municipios_em_que_a_margem_andou_para_o_lula"] = int((m.virada_margem > 0).sum())
    out["municipios_em_que_andou_para_o_flavio"] = int((m.virada_margem < 0).sum())
    # quanto a virada se concentra: que parte vem dos 10% de municípios que mais viraram
    s = m.sort_values("virada_margem", ascending=False)
    out["parte_dos_100_que_mais_viraram_pct"] = float(100 * s.head(100).virada_margem.sum() / total)
    out["parte_dos_10pct_que_mais_viraram_pct"] = float(100 * s.head(len(s) // 10).virada_margem.sum() / total)
    out["eleitorado_dos_10pct_pct"] = float(100 * s.head(len(s) // 10).eleitores_1t.sum() / m.eleitores_1t.sum())
    out["maiores_contribuicoes"] = s.head(15)[["uf", "municipio", "virada_margem", "eleitores_1t"]].to_dict("records")
    return out


def eleitor_da_direita(m: pd.DataFrame | None = None) -> dict:
    """Se o eleitor de Renan, Caiado e Zema era de direita e foi para o Flávio, onde eles eram mais fortes o Lula deveria
    ter levado uma parte menor dos votos livres. Municípios em 5 grupos pela força desses três no 1º turno, e o mesmo para
    o Cury, cujo eleitor as pesquisas davam como mais dividido."""
    m = _mun() if m is None else m
    m = m.assign(livres=(m.cury_1t + m.direita_1t + m.outros_1t) + (m.abstencao_1t - m.abstencao_2t) + (m.brancos_1t + m.nulos_1t - m.brancos_2t - m.nulos_2t))
    out = {}
    for nome, col in (("direita (Renan, Caiado e Zema)", "direita_1t"), ("Cury", "cury_1t")):
        m["forca"] = 100 * m[col] / m.validos_1t
        q = pd.qcut(m.forca, 5, labels=["1 (mais fraco)", "2", "3", "4", "5 (mais forte)"])
        g = m.groupby(q, observed=True).agg(forca_media=("forca", "mean"), lula=("lula_2t", "sum"), lula1=("lula_1t", "sum"),
                                             fl=("flavio_2t", "sum"), fl1=("flavio_1t", "sum"), livres=("livres", "sum"))
        g["lula_levou_dos_livres_pct"] = 100 * (g.lula - g.lula1) / g.livres
        g["flavio_levou_dos_livres_pct"] = 100 * (g.fl - g.fl1) / g.livres
        out[nome] = g.reset_index().rename(columns={"forca": "grupo"}).to_dict("records")
    # Goiás, a base do Caiado
    go = m[m.uf == "go"]
    out["goias"] = {"caiado_1t_pct": float(100 * go.caiado_1t.sum() / go.validos_1t.sum()),
                    "lula_ganhou": float((go.lula_2t - go.lula_1t).sum()), "flavio_ganhou": float((go.flavio_2t - go.flavio_1t).sum()),
                    "livres": float(go.livres.sum()),
                    "lula_levou_pct": float(100 * (go.lula_2t - go.lula_1t).sum() / go.livres.sum())}
    return out


def tendencia_pesquisas(p26: pd.DataFrame) -> pd.DataFrame:
    """Para cada 2º turno de 2014 a 2026: a média das pesquisas do 2º turno, a inclinação ao longo do tempo (pontos por
    semana, com o efeito de cada instituto descontado) e o valor da reta no dia da eleição, contra a urna."""
    linhas = []
    for nome, ano in (("pindograma-late-polls-2012-2018.csv", 2014), ("pindograma-late-polls-2012-2018.csv", 2018),
                      ("pindograma-late-polls-2022.csv", 2022)):
        d = pd.read_csv(COPIAS / "investigacao-segundo-turno-2026" / nome, low_memory=False)
        d = d[(d.year == ano) & (d.turno == 2) & (d.SG_UE == "BR") & (d.CD_CARGO == 1)]
        d = d[d.NUMERO_CANDIDATO.isin([13, ADV[ano]])]
        w = d.pivot_table(index=["scenario_id", "pretty_name", "DT_FIM_PESQUISA"], columns="NUMERO_CANDIDATO", values="result", aggfunc="first").dropna()
        w = w.reset_index()
        w["pt"] = 100 * w[13] / (w[13] + w[ADV[ano]])
        w["data"] = pd.to_datetime(w.DT_FIM_PESQUISA)
        linhas.append((ano, w.rename(columns={"pretty_name": "instituto"})[["instituto", "data", "pt"]], URNA_PT[ano]))
    q = p26[p26.entra].assign(data=pd.to_datetime(p26.campo_fim), pt=p26.lula_valido)[["instituto", "data", "pt"]]
    linhas.append((2026, q, None))
    out = []
    for ano, w, urna in linhas:
        dia = pd.Timestamp(DIA[ano])
        w = w[(w.data <= dia) & (w.data >= dia - pd.Timedelta(days=24))].copy()
        w["dias"] = (w.data - dia).dt.days
        inst = pd.get_dummies(w.instituto, drop_first=True).astype(float)
        X = np.column_stack([np.ones(len(w)), w.dias.to_numpy(float), inst.to_numpy()])
        b, *_ = np.linalg.lstsq(X, w.pt.to_numpy(float), rcond=None)
        # valor no dia da eleição para o instituto médio: intercepto + média dos efeitos de instituto
        efeitos = np.concatenate([[0.0], b[2:]])
        no_dia = float(b[0] + efeitos.mean())
        ultima_semana = w[w.dias >= -7].pt.mean()
        out.append({"ano": ano, "pesquisas": int(len(w)), "inclinacao_por_semana": float(7 * b[1]),
                    "media_ultima_semana": float(ultima_semana), "reta_no_dia": no_dia, "urna": urna})
    return pd.DataFrame(out)


def por_renda(m: pd.DataFrame | None = None) -> dict:
    """Municípios em 5 grupos de mesmo tamanho pela renda per capita do Censo 2022: quanto cada candidato ganhou a cada 100
    eleitores, quanto a abstenção caiu, e quanto da virada da diferença veio de cada grupo. Se as medidas voltadas aos mais
    pobres (Bolsa Família) tivessem virado votos, o Lula deveria ter crescido mais nos municípios mais pobres."""
    m = _mun() if m is None else m
    r = pd.read_csv(DERIV / "renda_municipio_censo2022.csv", dtype={"cd_ibge": str})
    m = m.merge(r[["cd_ibge", "renda_pc"]], on="cd_ibge", how="left")
    q = pd.qcut(m.renda_pc, 5, labels=["1 (mais pobres)", "2", "3", "4", "5 (mais ricos)"])
    g = m.groupby(q, observed=True).agg(renda_media=("renda_pc", "median"), municipios=("cd_tse", "count"), eleitores=("eleitores_1t", "sum"),
                                         l1=("lula_1t", "sum"), l2=("lula_2t", "sum"), f1=("flavio_1t", "sum"), f2=("flavio_2t", "sum"),
                                         a1=("abstencao_1t", "sum"), a2=("abstencao_2t", "sum"), virada=("virada_margem", "sum"))
    g["lula_1t_pct"] = 100 * g.l1 / (g.l1 + g.f1)
    g["lula_ganhou_por_100"] = 100 * (g.l2 - g.l1) / g.eleitores
    g["flavio_ganhou_por_100"] = 100 * (g.f2 - g.f1) / g.eleitores
    g["abstencao_caiu_pontos"] = 100 * (g.a1 - g.a2) / g.eleitores
    g["parte_da_virada_pct"] = 100 * g.virada / m.virada_margem.sum()
    g["parte_do_eleitorado_pct"] = 100 * g.eleitores / m.eleitores_1t.sum()
    w = m.dropna(subset=["renda_pc"])
    x = np.log(w.renda_pc)
    y = (100 * (w.lula_2t - w.lula_1t) / w.eleitores_1t)
    ww = w.eleitores_1t
    xc, yc = x - np.average(x, weights=ww), y - np.average(y, weights=ww)
    corr = float(np.average(xc * yc, weights=ww) / np.sqrt(np.average(xc ** 2, weights=ww) * np.average(yc ** 2, weights=ww)))
    return {"grupos": g.reset_index().rename(columns={"renda_pc": "grupo"}).to_dict("records"), "correlacao_renda_e_ganho_do_lula": corr,
            "sem_renda": int(m.renda_pc.isna().sum())}
