"""A chance do que aconteceu, calculada como se fosse sábado, 24/10/2026, com tudo o que se sabia.

Três pilares, com os pesos que o autor escolheu para a projeção do vídeo longo 14 (pesquisas 60%, histórico 25%,
crescimento 15%), cada um virando uma probabilidade com o seu próprio histórico de erro:

1. Pesquisas: a frente do Flávio na média da última pesquisa de cada instituto, contra a distribuição do erro da média
   das pesquisas em segundos turnos passados (Brasil, presidente e governador, e outros países). Probabilidade = parte
   dos casos passados em que a média errou a favor do líder por mais do que essa frente.
2. Histórico: com que frequência o líder do 1º turno perdeu o 2º, em função do tamanho da frente (regressão logística
   com presidente e governador no Brasil e presidente em outros países).
3. Crescimento: o 1º turno de 2026 com os votos dos outros, de branco e nulo e da abstenção indo como foram em cada
   2º turno passado no Brasil (2002 a 2022). Probabilidade = parte desses padrões em que o Lula venceria.

O mercado (Polymarket) entra como conferência, fora da média, com a sua calibração.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm

PESOS = {"pesquisas": 0.60, "historico": 0.25, "crescimento": 0.15}


def prob_pesquisas(frente_lider: float, erros: np.ndarray, alvo_extra: float = 0.0) -> dict:
    """erros = quanto a média das pesquisas superestimou a frente do líder das pesquisas (pontos); positivo = o líder
    foi pior na urna. A virada acontece quando o erro passa da frente."""
    erros = np.asarray(erros, float)
    emp = float(np.mean(erros > frente_lider))
    emp_mag = float(np.mean(erros > frente_lider + alvo_extra))
    mu, sd = float(np.mean(erros)), float(np.std(erros, ddof=1))
    return {"casos": int(len(erros)), "erro_medio": mu, "desvio": sd, "erro_absoluto_medio": float(np.mean(np.abs(erros))),
            "contagem": emp, "normal": float(1 - norm.cdf(frente_lider, mu, sd)),
            "normal_sem_vies": float(1 - norm.cdf(frente_lider, 0, sd)),
            "contagem_resultado_igual_ou_maior": emp_mag, "normal_resultado_igual_ou_maior": float(1 - norm.cdf(frente_lider + alvo_extra, mu, sd)),
            "casos_com_erro_maior": int(np.sum(erros > frente_lider))}


def logistica(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """P(virada) = 1 / (1 + exp(-(a + b·x))), por máxima verossimilhança."""
    def nll(p):
        z = p[0] + p[1] * x
        return float(np.sum(np.logaddexp(0, z) - y * z))
    r = minimize(nll, np.array([0.0, -0.1]), method="BFGS")
    return float(r.x[0]), float(r.x[1])


def prob_historico(casos: pd.DataFrame, frente: float, lider_pct: float) -> dict:
    """casos: colunas frente_1t (pontos), lider_1t_pct, virada (0/1), grupo."""
    c = casos.dropna(subset=["frente_1t", "virada"]).copy()
    a, b = logistica(c.frente_1t.to_numpy(float), c.virada.to_numpy(float))
    p_log = float(1 / (1 + np.exp(-(a + b * frente))))
    perto = c[(c.frente_1t <= 3) & (c.lider_1t_pct < 50)]
    faixa = c[(c.frente_1t <= frente + 1.5) & (c.frente_1t >= max(0, frente - 1.5))]
    por_grupo = {g: {"casos": int(len(x)), "viradas": int(x.virada.sum()),
                     "perto_casos": int(((x.frente_1t <= 3) & (x.lider_1t_pct < 50)).sum()),
                     "perto_viradas": int(x[(x.frente_1t <= 3) & (x.lider_1t_pct < 50)].virada.sum())}
                 for g, x in c.groupby("grupo")}
    return {"casos": int(len(c)), "viradas": int(c.virada.sum()), "logistica_a": a, "logistica_b": b, "logistica": p_log,
            "perto_casos": int(len(perto)), "perto_viradas": int(perto.virada.sum()),
            "perto": float(perto.virada.mean()) if len(perto) else None,
            "faixa_casos": int(len(faixa)), "faixa_viradas": int(faixa.virada.sum()),
            "faixa_lista": faixa.sort_values("frente_1t").to_dict("records"),
            "por_grupo": por_grupo}


def prob_crescimento(cenarios: pd.DataFrame, resultado_lula: float) -> dict:
    v = (cenarios.lula_pct > 50).astype(int)
    m = (cenarios.lula_pct >= resultado_lula).astype(int)
    return {"padroes": int(len(cenarios)), "lula_venceria_em": int(v.sum()), "contagem": float(v.mean()),
            "laplace": float((v.sum() + 1) / (len(v) + 2)), "resultado_igual_ou_maior": int(m.sum()),
            "por_padrao": cenarios.round(2).to_dict("records")}


def combinar(p: dict, pesos: dict = PESOS) -> float:
    return float(sum(pesos[k] * p[k] for k in pesos))


def erros_de_media_por_eleicao(pesq: pd.DataFrame) -> pd.DataFrame:
    """De uma lista de pesquisas (uma linha por pesquisa, conferida), a média da última pesquisa de cada instituto em cada
    eleição, em disputa a dois, contra a urna. Erro = quanto a média superestimou a frente de quem liderava a média."""
    p = pesq[pesq.conferida].copy()
    p["campo_fim"] = pd.to_datetime(p.campo_fim, errors="coerce")
    out = []
    for (pais, ano), g in p.groupby(["pais", "ano"]):
        g = g.sort_values("campo_fim").groupby("instituto").tail(1)
        a = (100 * g.candidato_a_pesquisa / (g.candidato_a_pesquisa + g.candidato_b_pesquisa)).mean()
        ua, ub = float(g.candidato_a_urna.iloc[0]), float(g.candidato_b_urna.iloc[0])
        urna_a = 100 * ua / (ua + ub)
        frente_pesq = 2 * a - 100
        frente_urna = 2 * urna_a - 100
        lider_a = frente_pesq >= 0
        out.append({"pais": pais, "ano": int(ano), "institutos": int(len(g)), "frente_lider_pesquisas": abs(frente_pesq),
                    "frente_lider_urna": frente_urna if lider_a else -frente_urna,
                    "superestimou_lider": abs(frente_pesq) - (frente_urna if lider_a else -frente_urna),
                    "lider_das_pesquisas_venceu": (frente_urna > 0) == lider_a})
    return pd.DataFrame(out)
