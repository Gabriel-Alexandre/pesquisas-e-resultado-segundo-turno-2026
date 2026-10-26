"""As contas do projeto, em funções (o script ferramentas/analise.py chama todas e grava os resultados).

Convenções:
- "válido" = porcentagem dos votos válidos; nas pesquisas, Lula ÷ (Lula + Flávio) dos totais, ou o válido que o próprio
  instituto publicou quando ele não sai dos totais da tabela (marcado em `flavio_valido_publicado`).
- erro de pesquisa = número da pesquisa menos o número da urna, em pontos do Lula nos válidos (positivo = deu mais ao Lula
  do que a urna deu). O erro na diferença entre os dois é o dobro.
- Nada aqui escolhe vencedor de nada que ainda vai acontecer: a eleição acabou e o resultado é o oficial do TSE.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm

from .comum import COPIAS, DERIV, REGIAO

DIA_ELEICAO = pd.Timestamp("2026-10-25")
ORIGENS_1T = ["lula", "flavio", "cury", "renan", "caiado", "outros", "branco_nulo", "abstencao"]
DESTINOS_2T = ["lula", "flavio", "branco_nulo", "abstencao"]
NOME = {"lula": "Lula", "flavio": "Flávio", "cury": "Augusto Cury", "renan": "Renan Santos", "caiado": "Ronaldo Caiado",
        "outros": "Zema e outros", "branco_nulo": "branco e nulo", "abstencao": "abstenção"}


# ---------------------------------------------------------------- resultado oficial

def carregar_resultado() -> tuple[pd.DataFrame, pd.DataFrame]:
    ab = pd.read_csv(DERIV / "presidente_abrangencia.csv")
    mu = pd.read_csv(DERIV / "presidente_municipio.csv", dtype={"cd_tse": str, "cd_ibge": str})
    return ab, mu


def resultado_nacional(ab: pd.DataFrame) -> dict:
    b = ab[ab.abr == "br"].set_index("turno")
    out = {}
    for t in (1, 2):
        r = b.loc[t]
        out[f"t{t}"] = {k: float(r[k]) for k in ["eleitores", "comparecimento", "abstencao", "brancos", "nulos", "validos",
                                                   "lula", "flavio", "cury", "renan", "caiado", "zema", "outros"]}
        out[f"t{t}"]["lula_pct"] = 100 * r.lula / r.validos
        out[f"t{t}"]["flavio_pct"] = 100 * r.flavio / r.validos
        out[f"t{t}"]["abstencao_pct"] = 100 * r.abstencao / r.eleitores
        out[f"t{t}"]["branco_nulo_pct"] = 100 * (r.brancos + r.nulos) / r.comparecimento
    t1, t2 = out["t1"], out["t2"]
    out["variacao"] = {
        "lula": t2["lula"] - t1["lula"], "flavio": t2["flavio"] - t1["flavio"],
        "outros_candidatos": -(t1["cury"] + t1["renan"] + t1["caiado"] + t1["zema"] + t1["outros"]),
        "abstencao": t2["abstencao"] - t1["abstencao"], "branco_nulo": (t2["brancos"] + t2["nulos"]) - (t1["brancos"] + t1["nulos"]),
        "frente_1t_flavio": t1["flavio"] - t1["lula"], "frente_2t_lula": t2["lula"] - t2["flavio"],
    }
    v = out["variacao"]
    v["vaivem"] = v["frente_1t_flavio"] + v["frente_2t_lula"]
    v["ganho_dos_dois"] = v["lula"] + v["flavio"]
    v["parte_do_lula_no_ganho"] = 100 * v["lula"] / v["ganho_dos_dois"]
    v["frente_1t_pontos"] = t1["flavio_pct"] - t1["lula_pct"]
    v["frente_2t_pontos"] = t2["lula_pct"] - t2["flavio_pct"]
    # o mínimo que o Lula precisou dos outros candidatos se todo voto novo (abstenção e branco e nulo) fosse dele
    novos = -v["abstencao"] - v["branco_nulo"]
    outros = -v["outros_candidatos"]
    v["lula_precisou_dos_outros_pct_se_todo_novo_fosse_dele"] = 100 * (v["lula"] - novos) / outros
    return out


# ---------------------------------------------------------------- pesquisas

def carregar_pesquisas(resultado_lula: float) -> pd.DataFrame:
    p = pd.read_csv(DERIV / "pesquisas_2t_conferidas.csv")
    p["lula_valido"] = 100 * p.lula_total / (p.lula_total + p.flavio_total)
    pub = p.flavio_valido_publicado.notna()
    p.loc[pub, "lula_valido"] = 100 - p.loc[pub, "flavio_valido_publicado"]
    p["flavio_valido"] = 100 - p.lula_valido
    p["campo_fim"] = pd.to_datetime(p.campo_fim)
    p["entra"] = p.casou & p.conferida
    p["erro_lula"] = p.lula_valido - resultado_lula
    p["deu_lula"] = p.lula_valido > 50
    p["empate_cravado"] = p.lula_valido == 50
    # margem de erro declarada é sobre o total; no válido ela cresce na razão válidos ÷ total
    p["margem_valido"] = p.margem_erro * 100 / (p.lula_total + p.flavio_total)
    p["urna_dentro_da_margem"] = p.erro_lula.abs() <= p.margem_valido
    return p.sort_values("campo_fim", ascending=False).reset_index(drop=True)


def resumo_pesquisas(p: pd.DataFrame, resultado_lula: float) -> dict:
    ok = p[p.entra]
    ultimas = ok.sort_values("campo_fim").groupby("instituto").tail(1).sort_values("erro_lula")
    semana = ok[ok.campo_fim >= DIA_ELEICAO - pd.Timedelta(days=7)]
    vespera = ok[ok.campo_fim >= DIA_ELEICAO - pd.Timedelta(days=2)]

    def bloco(df: pd.DataFrame) -> dict:
        return {"n": int(len(df)), "media_lula": float(df.lula_valido.mean()), "mediana_lula": float(df.lula_valido.median()),
                "erro_medio": float(df.erro_lula.mean()), "erro_absoluto_medio": float(df.erro_lula.abs().mean()),
                "deram_flavio": int((df.lula_valido < 50).sum()), "deram_lula": int((df.lula_valido > 50).sum()),
                "empate": int((df.lula_valido == 50).sum()), "maior_lula": float(df.lula_valido.max()),
                "urna_dentro_da_margem": int(df.urna_dentro_da_margem.sum())}

    out = {"resultado_lula": resultado_lula, "todas": bloco(ok), "ultima_semana": bloco(semana), "vespera": bloco(vespera),
           "ultima_de_cada_instituto": bloco(ultimas), "fora_da_conta": p[~p.entra][["instituto", "campo_fim"]].astype(str).to_dict("records"),
           "ranking_ultimas": [{"instituto": r.instituto, "campo_fim": str(r.campo_fim.date()), "lula_valido": round(r.lula_valido, 2),
                                "erro_lula": round(r.erro_lula, 2), "registro_tse": r.registro_tse} for r in ultimas.itertuples()]}
    # a menor distância de qualquer pesquisa até a urna
    out["nenhuma_chegou_na_urna"] = bool((ok.lula_valido < resultado_lula).all())
    out["pesquisa_mais_perto"] = ok.loc[ok.erro_lula.abs().idxmin(), ["instituto", "lula_valido"]].astype(str).to_dict()
    return out


def historico_erro_pesquisas() -> dict:
    """Erro médio das últimas pesquisas de cada instituto, por eleição e turno, no lado do candidato contra o PT
    (positivo = a pesquisa deu mais a ele do que a urna). Fonte: previsao-segundo-turno-2026 (2014 a 2022) e
    presidente-primeiro-turno-2026 (1º turno de 2026)."""
    e = pd.read_csv(COPIAS / "previsao-segundo-turno-2026" / "institutos_erros.csv")
    linhas = []
    for (ano, turno), g in e.groupby(["ano", "turno"]):
        linhas.append({"ano": int(ano), "turno": int(turno), "institutos": int(len(g)), "erro_medio_anti_pt": float(g.erro.mean()),
                       "erro_absoluto_medio": float(g.erro.abs().mean())})
    b6 = pd.read_csv(COPIAS / "presidente-primeiro-turno-2026" / "b6_erro_por_instituto_e_rodada.csv")
    b = b6[b6.rodada == "2026-1"]
    # erro em b6 é na diferença (Flávio menos Lula); a metade é o erro na parte de cada um numa disputa a dois
    if not ((e.ano == 2026) & (e.turno == 1)).any():
        linhas.append({"ano": 2026, "turno": 1, "institutos": int(len(b)), "erro_medio_anti_pt": float(b.erro.mean() / 2),
                       "erro_absoluto_medio": float((b.erro / 2).abs().mean())})
    return {"linhas": sorted(linhas, key=lambda x: (x["ano"], x["turno"]))}


# ---------------------------------------------------------------- regras do histórico

def regras_historicas(ab: pd.DataFrame) -> dict:
    hist = pd.read_csv(COPIAS / "investigacao-segundo-turno-2026" / "historico_turnos.csv")
    seg = pd.read_csv(COPIAS / "investigacao-segundo-turno-2026" / "p_segundos_turnos.csv")
    pres = seg[seg.cargo == "presidente"]
    gov = seg[seg.cargo == "governador"]
    out = {"presidente_lider_1t_venceu": {"vezes": int(len(pres)), "acertos": int((pres.virada == 0).sum()),
                                          "menor_frente_ate_2022": float(pres.frente_1t_pontos.min())},
           "governador_lider_1t_venceu": {"vezes": int(len(gov)), "viradas": int(gov.virada.sum())}}
    perto = gov[(gov.frente_1t_pontos <= 3) & (gov.lider_1t_pct < 50)]
    out["governador_frente_ate_3_pontos"] = {"vezes": int(len(perto)), "viradas": int(perto.virada.sum())}

    # quem venceu cada UF no 1º turno de presidente venceu a eleição? (1994 a 2022 pelo TSE; 1989 sem dado por UF aqui)
    p = hist[(hist.cargo == "presidente")]
    vencedor = {}
    for ano, g in p.groupby("ano"):
        t = g[g.turno == g.turno.max()].groupby("nr_candidato").votos_nominais.sum()
        vencedor[ano] = int(t.idxmax())
    regra = []
    for ano, g in p.groupby("ano"):
        for turno in sorted(g.turno.unique()):
            por_uf = g[g.turno == turno].groupby(["uf", "nr_candidato"]).votos_nominais.sum().reset_index()
            lider = por_uf.loc[por_uf.groupby("uf").votos_nominais.idxmax()]
            for r in lider.itertuples():
                regra.append({"ano": int(ano), "turno": int(turno), "uf": r.uf, "acertou": int(r.nr_candidato) == vencedor[ano]})
    regra = pd.DataFrame(regra)
    u = ab[ab.abr.isin([x for x in REGIAO if x != "zz"])]
    for t in (1, 2):
        g = u[u.turno == t]
        for r in g.itertuples():
            regra = pd.concat([regra, pd.DataFrame([{"ano": 2026, "turno": t, "uf": r.abr.upper(), "acertou": r.lula > r.flavio}])])
    tab = regra[regra.ano < 2026].groupby(["uf", "turno"]).acertou.agg(["sum", "count"]).unstack()
    tab.columns = [f"{a}_{b}t" for a, b in tab.columns]
    a26 = regra[regra.ano == 2026].pivot(index="uf", columns="turno", values="acertou")
    tab["acertou_2026_1t"] = a26[1]
    tab["acertou_2026_2t"] = a26[2]
    tab = tab.reset_index()
    tab = tab[tab.uf.isin([x.upper() for x in REGIAO if x != "zz"])].reset_index(drop=True)
    tab["acertou_2026_1t"] = tab.acertou_2026_1t.astype(bool)
    tab["acertou_2026_2t"] = tab.acertou_2026_2t.astype(bool)
    out["minas"] = {k: (bool(v) if isinstance(v, (bool, np.bool_)) else int(v)) for k, v in tab[tab.uf == "MG"].iloc[0].drop("uf").items()}
    perfeitos_1t = tab[tab["sum_1t"] == tab["count_1t"]]
    out["ufs_que_sempre_acertaram_no_1t"] = {"ufs": perfeitos_1t.uf.tolist(),
                                             "acertaram_em_2026": perfeitos_1t[perfeitos_1t.acertou_2026_1t].uf.tolist()}
    perfeitos_2t = tab[tab["sum_2t"] == tab["count_2t"]]
    out["ufs_que_sempre_acertaram_no_2t"] = {"ufs": perfeitos_2t.uf.tolist(),
                                             "acertaram_em_2026": perfeitos_2t[perfeitos_2t.acertou_2026_2t.astype(bool)].uf.tolist()}
    out["_tabela_ufs"] = tab
    return out


# ---------------------------------------------------------------- estados e municípios

def estados(ab: pd.DataFrame) -> pd.DataFrame:
    u = ab[ab.abr != "br"].copy()
    w = u.pivot(index="abr", columns="turno", values=["lula", "flavio", "validos", "abstencao", "eleitores", "brancos", "nulos",
                                                       "cury", "renan", "caiado", "zema", "outros"])
    t = pd.DataFrame(index=w.index)
    t["regiao"] = [REGIAO[x] for x in t.index]
    for k in (1, 2):
        t[f"lula_pct_{k}t"] = 100 * w["lula"][k] / w["validos"][k]
        t[f"vencedor_{k}t"] = np.where(w["lula"][k] > w["flavio"][k], "Lula", "Flávio")
        t[f"abstencao_pct_{k}t"] = 100 * w["abstencao"][k] / w["eleitores"][k]
    t["virou"] = np.where(t.vencedor_1t != t.vencedor_2t, "para " + t.vencedor_2t, "")
    t["lula_ganhou"] = w["lula"][2] - w["lula"][1]
    t["flavio_ganhou"] = w["flavio"][2] - w["flavio"][1]
    t["outros_1t"] = w["cury"][1] + w["renan"][1] + w["caiado"][1] + w["zema"][1] + w["outros"][1]
    t["abstencao_variou"] = w["abstencao"][2] - w["abstencao"][1]
    t["branco_nulo_variou"] = (w["brancos"][2] + w["nulos"][2]) - (w["brancos"][1] + w["nulos"][1])
    t["variacao_lula_pontos"] = t.lula_pct_2t - t.lula_pct_1t
    return t.reset_index().rename(columns={"abr": "uf"})


def municipios(mu: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    m = mu[mu.uf != "zz"].copy()
    m["lula_pct_1t"] = 100 * m.lula_1t / m.validos_1t
    m["lula_pct_2t"] = 100 * m.lula_2t / m.validos_2t
    m["venc_1t"] = np.where(m.lula_1t > m.flavio_1t, "Lula", np.where(m.lula_1t < m.flavio_1t, "Flávio", "empate"))
    m["venc_2t"] = np.where(m.lula_2t > m.flavio_2t, "Lula", np.where(m.lula_2t < m.flavio_2t, "Flávio", "empate"))
    m["virou"] = np.where(m.venc_1t != m.venc_2t, m.venc_1t + " para " + m.venc_2t, "")
    m["lula_ganhou"] = m.lula_2t - m.lula_1t
    m["flavio_ganhou"] = m.flavio_2t - m.flavio_1t
    m["outros_1t"] = m[["cury_1t", "renan_1t", "caiado_1t", "zema_1t", "outros_1t"]].sum(axis=1)
    m["abstencao_caiu"] = m.abstencao_1t - m.abstencao_2t
    m["branco_nulo_caiu"] = (m.brancos_1t + m.nulos_1t) - (m.brancos_2t + m.nulos_2t)
    m["abstencao_pct_1t"] = 100 * m.abstencao_1t / m.eleitores_1t
    m["abstencao_pct_2t"] = 100 * m.abstencao_2t / m.eleitores_2t
    viradas = m[m.virou != ""]
    porte = pd.cut(m.eleitores_1t, [0, 20_000, 100_000, 500_000, 1e9], labels=["até 20 mil eleitores", "20 a 100 mil", "100 a 500 mil", "mais de 500 mil"])
    ganho_porte = m.groupby(porte, observed=True)[["lula_ganhou", "flavio_ganhou"]].sum()
    res = {"municipios": int(len(m)), "lula_venceu_1t": int((m.venc_1t == "Lula").sum()), "lula_venceu_2t": int((m.venc_2t == "Lula").sum()),
           "flavio_venceu_1t": int((m.venc_1t == "Flávio").sum()), "flavio_venceu_2t": int((m.venc_2t == "Flávio").sum()),
           "viradas": viradas.virou.value_counts().to_dict(),
           "lula_ganhou_votos_em": int((m.lula_ganhou > 0).sum()), "flavio_ganhou_votos_em": int((m.flavio_ganhou > 0).sum()),
           "flavio_perdeu_votos_em": int((m.flavio_ganhou < 0).sum()),
           "capitais_lula_ganhou": float(m[m.capital].lula_ganhou.sum()), "capitais_flavio_ganhou": float(m[m.capital].flavio_ganhou.sum()),
           "ganho_por_porte": {str(k): {"lula": float(v.lula_ganhou), "flavio": float(v.flavio_ganhou)} for k, v in ganho_porte.iterrows()},
           "maiores_viradas_em_votos": viradas.assign(eleitores=viradas.eleitores_1t).nlargest(10, "eleitores_1t")[
               ["uf", "municipio", "virou", "eleitores_1t", "lula_pct_1t", "lula_pct_2t"]].to_dict("records")}
    return m, res


# ---------------------------------------------------------------- de onde vieram os votos (inferência ecológica)

def _matrizes(m: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    e = m.eleitores_1t.to_numpy(float)
    x = np.column_stack([m.lula_1t, m.flavio_1t, m.cury_1t, m.renan_1t, m.caiado_1t, m.zema_1t + m.outros_1t,
                         m.brancos_1t + m.nulos_1t, m.abstencao_1t]) / e[:, None]
    bn2 = m.brancos_2t + m.nulos_2t
    y = np.column_stack([m.lula_2t, m.flavio_2t, bn2, e - m.lula_2t - m.flavio_2t - bn2]) / e[:, None]
    return x, y, e


def _ajustar(x: np.ndarray, y: np.ndarray, w: np.ndarray, t0: np.ndarray | None = None) -> np.ndarray:
    """Matriz de transição T (origem × destino), linhas somando 1 e tudo entre 0 e 1, que minimiza
    sum_i w_i ||y_i - x_i T||^2 (regressão de Goodman com restrição)."""
    w = w / w.sum()  # escala: sem isso o otimizador para no ponto de partida
    a = (x * w[:, None]).T @ x
    b = (x * w[:, None]).T @ y
    k, j = x.shape[1], y.shape[1]

    def f(v):
        t = v.reshape(k, j)
        return float(np.sum(t * (a @ t)) - 2 * np.sum(t * b))

    def g(v):
        t = v.reshape(k, j)
        return (2 * (a @ t) - 2 * b).ravel()

    cons = [{"type": "eq", "fun": (lambda v, i=i: v.reshape(k, j)[i].sum() - 1), "jac": (lambda v, i=i: np.eye(k)[i].repeat(j) * 1.0)}
            for i in range(k)]
    v0 = (t0 if t0 is not None else np.full((k, j), 1 / j)).ravel()
    r = minimize(f, v0, jac=g, bounds=[(0, 1)] * (k * j), constraints=cons, method="SLSQP", options={"maxiter": 1000, "ftol": 1e-15})
    if not r.success:
        raise RuntimeError(f"ajuste não convergiu: {r.message}")
    return np.clip(r.x.reshape(k, j), 0, 1)


def transferencia(mu: pd.DataFrame, reamostras: int = 200, semente: int = 2026) -> dict:
    """Uma matriz por região (o eleitor do Nordeste não precisa se comportar como o do Sul), somada no país.
    Intervalo por reamostragem de municípios dentro de cada região."""
    m = mu[mu.uf != "zz"].copy()
    m["regiao"] = m.uf.map(REGIAO)
    rng = np.random.default_rng(semente)
    regioes = sorted(m.regiao.unique())
    dados = {r: _matrizes(m[m.regiao == r]) for r in regioes}
    base = {r: _ajustar(*dados[r]) for r in regioes}

    def fluxos(mats: dict) -> np.ndarray:
        tot = np.zeros((len(ORIGENS_1T), len(DESTINOS_2T)))
        for r in regioes:
            x, _, e = dados[r]
            tot += (x * e[:, None]).sum(axis=0)[:, None] * mats[r]  # votos de origem × proporção (média da região)
        return tot

    # o fluxo pela matriz média da região, aplicado aos totais de origem de cada região
    principal = fluxos(base)
    boot = []
    for _ in range(reamostras):
        mats = {}
        for r in regioes:
            x, y, e = dados[r]
            idx = rng.integers(0, len(e), len(e))
            mats[r] = _ajustar(x[idx], y[idx], e[idx], base[r])
        boot.append(fluxos(mats))
    boot = np.array(boot)
    lo, hi = np.percentile(boot, 5, axis=0), np.percentile(boot, 95, axis=0)
    origem_tot = principal.sum(axis=1)
    tabela = []
    for i, o in enumerate(ORIGENS_1T):
        for k, d in enumerate(DESTINOS_2T):
            tabela.append({"origem_1t": o, "destino_2t": d, "votos": principal[i, k], "votos_p5": lo[i, k], "votos_p95": hi[i, k],
                           "pct_da_origem": 100 * principal[i, k] / origem_tot[i],
                           "pct_p5": 100 * lo[i, k] / origem_tot[i], "pct_p95": 100 * hi[i, k] / origem_tot[i]})
    tabela = pd.DataFrame(tabela)
    # quanto a matriz reproduz o 2º turno observado
    obs = {d: float(sum(dados[r][1][:, k] @ dados[r][2] for r in regioes)) for k, d in enumerate(DESTINOS_2T)}
    prev = {d: float(principal[:, k].sum()) for k, d in enumerate(DESTINOS_2T)}
    # ajuste também com uma matriz só para o país (sensibilidade)
    xn, yn, en = _matrizes(m)
    tn = _ajustar(xn, yn, en)
    nac = pd.DataFrame(tn * 100, index=ORIGENS_1T, columns=DESTINOS_2T)
    regiao_tab = {r: pd.DataFrame(base[r] * 100, index=ORIGENS_1T, columns=DESTINOS_2T).round(1).to_dict() for r in regioes}
    return {"tabela": tabela, "observado_2t": obs, "previsto_2t": prev, "matriz_unica_pais_pct": nac, "por_regiao_pct": regiao_tab}


# ---------------------------------------------------------------- governador × presidente

def governadores(ab: pd.DataFrame) -> pd.DataFrame:
    g = pd.read_csv(DERIV / "governador.csv", dtype={"numero": str})
    eleitos = g[g.situacao.str.contains("Eleito", na=False) & ~g.situacao.str.startswith("Não")]
    linhas = []
    pres = ab[(ab.abr != "br") & (ab.abr != "zz")].pivot(index="abr", columns="turno", values=["lula", "flavio", "validos"])
    for uf, e in eleitos.groupby("uf"):
        e = e.sort_values("turno").iloc[-1]
        col = f" {e.coligacao} ".replace("/", " / ")
        tem_pt, tem_pl = " PT " in col, " PL " in col
        lado = "Lula" if tem_pt and not tem_pl else "Flávio" if tem_pl and not tem_pt else "os dois" if tem_pt and tem_pl else "nenhum"
        lula2 = 100 * pres.loc[uf, ("lula", 2)] / pres.loc[uf, ("validos", 2)]
        venc = "Lula" if lula2 > 50 else "Flávio"
        # o candidato a governador da coligação de cada lado (no 1º turno), para a comparação de votação
        g1 = g[(g.uf == uf) & (g.turno == 1)].copy()
        cols = " " + g1.coligacao.str.replace("/", " / ") + " "
        lado_pt = g1[cols.str.contains(" PT ")]
        lado_pl = g1[cols.str.contains(" PL ")]
        linhas.append({"uf": uf, "governador_eleito": e.candidato, "partido": e.partido, "turno_decidido": int(e.turno),
                       "pct_governador": e.pct, "coligacao": e.coligacao, "lado_da_coligacao": lado,
                       "presidente_venceu_no_estado": venc, "lula_pct_2t": lula2,
                       "mesmo_lado": lado == venc,
                       "gov_coligacao_pt_pct_1t": float(lado_pt.pct.max()) if len(lado_pt) else np.nan,
                       "gov_coligacao_pl_pct_1t": float(lado_pl.pct.max()) if len(lado_pl) else np.nan,
                       "lula_pct_1t": 100 * pres.loc[uf, ("lula", 1)] / pres.loc[uf, ("validos", 1)],
                       "flavio_pct_1t": 100 * pres.loc[uf, ("flavio", 1)] / pres.loc[uf, ("validos", 1)]})
    return pd.DataFrame(linhas)


# ---------------------------------------------------------------- probabilidade antes da eleição

def erro_historico_da_media() -> pd.DataFrame:
    """Para cada 2º turno de 2014 a 2022 (presidente e governador): quanto a média das pesquisas da última semana
    superestimou a frente de quem liderava as pesquisas (positivo = o líder das pesquisas foi pior na urna)."""
    p = pd.read_csv(COPIAS / "investigacao-segundo-turno-2026" / "p3_disputas.csv")
    p = p[p.empate_nas_pesquisas == 0].copy()
    venceu = p.lider_das_pesquisas_venceu == 1
    # frente do líder nas pesquisas e na urna
    p["frente_lider_pesquisas"] = np.where(venceu, p.frente_media_pesquisas_para_o_vencedor, -p.frente_media_pesquisas_para_o_vencedor)
    p["frente_lider_urna"] = np.where(venceu, p.frente_real_do_vencedor, -p.frente_real_do_vencedor)
    p["superestimou_lider"] = p.frente_lider_pesquisas - p.frente_lider_urna
    return p


def probabilidades(media_lula: float, resultado: dict, hist_erro: pd.DataFrame, regras: dict) -> dict:
    frente_flavio = 2 * (50 - media_lula)          # frente do Flávio na média das pesquisas, em pontos
    frente_real_lula = resultado["variacao"]["frente_2t_pontos"]
    e_all = hist_erro.superestimou_lider.to_numpy()
    e_pres = hist_erro[hist_erro.cargo == "presidente"].superestimou_lider.to_numpy()
    sd_all = float(np.std(e_all, ddof=1))
    vies_all = float(np.mean(e_all))
    out = {"frente_flavio_nas_pesquisas": frente_flavio, "frente_real_lula": frente_real_lula,
           "disputas_no_historico": int(len(e_all)), "desvio_do_erro_todas": sd_all, "vies_medio_todas": vies_all,
           "erros_presidente": [float(x) for x in e_pres]}
    # 1) pesquisas + erro histórico (todas as disputas de 2º turno 2014 a 2022)
    out["pesquisas_empirico"] = float(np.mean(e_all > frente_flavio))
    out["pesquisas_empirico_frente_igual_ou_maior"] = float(np.mean(e_all > frente_flavio + frente_real_lula))
    out["pesquisas_normal"] = float(1 - norm.cdf(frente_flavio, loc=vies_all, scale=sd_all))
    out["pesquisas_normal_sem_vies"] = float(1 - norm.cdf(frente_flavio, loc=0, scale=sd_all))
    out["pesquisas_normal_frente_igual_ou_maior"] = float(1 - norm.cdf(frente_flavio + frente_real_lula, loc=vies_all, scale=sd_all))
    # só presidente (3 eleições), desvio pelas 3
    sd_p = float(np.std(e_pres, ddof=1))
    out["desvio_do_erro_presidente"] = sd_p
    out["pesquisas_normal_so_presidente"] = float(1 - norm.cdf(frente_flavio, loc=0, scale=sd_p))
    # 2) histórico: o líder do 1º turno de presidente venceu sempre (regra de Laplace)
    n = regras["presidente_lider_1t_venceu"]["vezes"]
    out["historico_laplace"] = 1 / (n + 2)
    perto = regras["governador_frente_ate_3_pontos"]
    out["historico_governador_perto"] = perto["viradas"] / perto["vezes"]
    # 3) mercado
    f = pd.read_csv(COPIAS / "investigacao-segundo-turno-2026" / "polymarket_favoritos.csv")
    f_todos = f
    if "repetida" in f:
        f = f[f.repetida.fillna(0).astype(int) == 0]  # o mesmo pleito em mais de um mercado conta uma vez
    br = f[f.slug == "brazil-presidential-election"].iloc[0]
    out["polymarket_lula_vespera"] = float(br.preco_vencedor_vespera)
    faixa = f[(f.preco_favorito >= 0.70) & (f.preco_favorito <= 0.90) & (f.slug != "brazil-presidential-election")]
    out["polymarket_favoritos_70_90"] = {"mercados": int(len(faixa)), "favorito_perdeu": int((faixa.acertou == 0).sum())}
    out["polymarket_1t"] = {"favorito": "Lula", "preco": float(f_todos[f_todos.slug == "brazil-presidential-election-first-round-winner"].preco_favorito.iloc[0]),
                            "acertou": False}
    # combinação simples: média das três leituras (cada uma com o mesmo peso)
    tres = [out["pesquisas_normal"], out["historico_laplace"], out["polymarket_lula_vespera"]]
    out["media_das_tres"] = float(np.mean(tres))
    # a leitura mais desfavorável ao resultado (lente da fraude, versão mais forte) e a mais favorável
    leituras = {"pesquisas e erro histórico (todas as disputas)": out["pesquisas_normal"],
                "pesquisas e erro histórico (só presidente)": out["pesquisas_normal_so_presidente"],
                "pesquisas e erro histórico (contagem)": out["pesquisas_empirico"],
                "o líder do 1º turno sempre venceu (Laplace)": out["historico_laplace"],
                "governador com frente de até 3 pontos": out["historico_governador_perto"],
                "Polymarket na véspera": out["polymarket_lula_vespera"]}
    out["leituras"] = leituras
    out["menor"] = min(leituras.items(), key=lambda kv: kv[1])
    out["maior"] = max(leituras.items(), key=lambda kv: kv[1])
    out["em_1_em_n"] = {k: (round(1 / v) if v > 0 else math.inf) for k, v in leituras.items()}
    return out


# ---------------------------------------------------------------- testes das duas lentes

def testes_das_lentes(m: pd.DataFrame) -> dict:
    """Testes que separariam as duas premissas, feitos com espelho (o mesmo para os dois candidatos).

    T1 · votos sem origem: no município, o ganho de um candidato maior que tudo o que estava livre (votos dos outros
         candidatos + a queda da abstenção + a queda de branco e nulo) só fecha com troca direta de voto ou com voto
         acrescentado. Conta para os dois.
    T2 · comparecimento muito alto: municípios com comparecimento acima de 95% e com 90% ou mais para um candidato,
         nos dois turnos (a mancha que o enchimento de urna deixa na literatura de Klimek e outros, 2012).
    T3 · onde a abstenção caiu: a queda da abstenção acompanha a força do Lula no 1º turno? (a hipótese do filtro de
         eleitor provável das pesquisas)
    """
    livre = m.outros_1t + m.abstencao_caiu.clip(lower=0) + m.branco_nulo_caiu.clip(lower=0)
    out = {}
    for c in ("lula", "flavio"):
        ganho = m[f"{c}_ganhou"]
        excesso = (ganho - livre).clip(lower=0)
        out[f"t1_{c}"] = {"municipios": int((excesso > 0).sum()), "votos_acima_do_livre": float(excesso.sum()),
                          "eleitores_nesses_municipios": float(m.loc[excesso > 0, "eleitores_1t"].sum())}
    out["t1_lula"]["exemplos"] = m.assign(exc=(m.lula_ganhou - livre)).nlargest(5, "exc")[["uf", "municipio", "lula_ganhou", "exc"]].to_dict("records")
    comp1 = 100 * m.comparecimento_1t / m.eleitores_1t
    comp2 = 100 * m.comparecimento_2t / m.eleitores_2t
    out["t2"] = {}
    for t, comp in ((1, comp1), (2, comp2)):
        lp = 100 * m[f"lula_{t}t"] / m[f"validos_{t}t"]
        out["t2"][f"{t}t"] = {"comparecimento_acima_95": int((comp > 95).sum()),
                              "e_lula_90_ou_mais": int(((comp > 95) & (lp >= 90)).sum()),
                              "e_flavio_90_ou_mais": int(((comp > 95) & (lp <= 10)).sum()),
                              "comparecimento_medio": float(np.average(comp, weights=m.eleitores_1t))}
    # T3: correlação, ponderada por eleitores, entre a força do Lula no 1º turno e a queda da abstenção (em pontos)
    queda = m.abstencao_pct_1t - m.abstencao_pct_2t
    w = m.eleitores_1t
    def corr(a, b):
        a, b = a - np.average(a, weights=w), b - np.average(b, weights=w)
        return float(np.average(a * b, weights=w) / math.sqrt(np.average(a * a, weights=w) * np.average(b * b, weights=w)))
    out["t3_correlacao_forca_lula_1t_e_queda_abstencao"] = corr(m.lula_pct_1t, queda)
    terc = pd.qcut(m.lula_pct_1t, 3, labels=["terço onde o Lula foi mais fraco", "terço do meio", "terço onde o Lula foi mais forte"])
    out["t3_queda_por_terco"] = {str(k): float(np.average(queda[terc == k], weights=w[terc == k])) for k in terc.cat.categories}
    out["t3_votos_novos_por_terco"] = {str(k): float(m.loc[terc == k, "abstencao_caiu"].sum()) for k in terc.cat.categories}
    # o ganho do Lula em pontos acompanha a queda da abstenção?
    out["t3_correlacao_queda_abstencao_e_ganho_lula_pontos"] = corr(queda, m.lula_pct_2t - m.lula_pct_1t)
    return out


def governador_viradas_2026() -> list[dict]:
    """Nas 6 UFs com 2º turno de governador em 2026: o líder do 1º turno venceu o 2º?"""
    g = pd.read_csv(DERIV / "governador.csv", dtype={"numero": str})
    out = []
    for uf, x in g.groupby("uf"):
        if (x.turno == 2).sum() == 0:
            continue
        t1 = x[x.turno == 1].nlargest(2, "pct")
        t2 = x[x.turno == 2].sort_values("pct", ascending=False)
        out.append({"uf": uf, "lider_1t": t1.iloc[0].candidato, "lider_1t_pct": float(t1.iloc[0].pct),
                    "segundo_1t": t1.iloc[1].candidato, "segundo_1t_pct": float(t1.iloc[1].pct),
                    "vencedor_2t": t2.iloc[0].candidato, "vencedor_2t_pct": float(t2.iloc[0].pct),
                    "virada": t2.iloc[0].candidato != t1.iloc[0].candidato})
    return out
