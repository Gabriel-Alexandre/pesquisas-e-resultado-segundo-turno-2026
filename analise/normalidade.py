"""Rodada 5: "isso é normal?". Cada coisa que 2026 mostrou, posta ao lado das eleições de 2002 a 2022, e a chance
refeita com as nuances que a rodada 2 deixou de fora.

1. Para quem foram os votos livres, conforme o campo dos candidatos eliminados (com o apoio que cada um declarou).
2. O comparecimento e o espalhamento da virada pelos municípios, em todas as eleições.
3. A chance antes da votação, pilar por pilar, com três correções e três jeitos de juntar os pilares.

Fontes: TSE (resultado por município, 2002 a 2026, cópias com hash em dados/copias/), `dados/agentes/apoios_segundo_turno.csv`
(posição de cada candidato eliminado no 2º turno, com link) e os resultados das rodadas anteriores.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from .comum import COPIAS, RAIZ
from .historia import ADVERSARIO

APOIOS = RAIZ / "dados" / "agentes" / "apoios_segundo_turno.csv"


# ------------------------------------------------------------------ 1. o campo dos eliminados
def votos_do_primeiro_turno() -> pd.DataFrame:
    """Votos nacionais de cada partido no 1º turno (2002 a 2022 pela cópia do TSE; 2026 pelo resultado deste projeto)."""
    v = pd.read_parquet(COPIAS / "previsao-segundo-turno-2026" / "mun_votos.parquet")
    v = v[(v.turno == 1) & (v.ano < 2026)]
    return v.groupby(["ano", "partido"], as_index=False).votos.sum()


def campo_dos_eliminados(por_ano: pd.DataFrame, trano: pd.DataFrame, t1_2026: dict) -> pd.DataFrame:
    """Por eleição: parte dos votos dos eliminados cujo candidato apoiou o PT, apoiou o adversário ou ficou neutro; a
    parte dos votos livres que o PT levou no saldo (conta exata); e a parte dos votos dos próprios eliminados que foi
    para o PT pelos dois modelos de transição do projeto (estimativa: o voto é secreto e os dois modelos discordam).
    `por_ano` vem de historia.de_onde_vieram; `trano` de historia.transferencia_por_ano."""
    a = pd.read_csv(APOIOS)
    vt = votos_do_primeiro_turno()
    linhas = []
    for ano, g in a.groupby("ano"):
        if ano < 2026:
            x = vt[vt.ano == ano].set_index("partido").votos
            elim = x.drop([13, ADVERSARIO[ano]], errors="ignore")
            total_elim = float(elim.sum())
            votos = g.assign(votos=g.numero.map(x).fillna(0.0))
        else:
            nome = {"Augusto Cury": "cury", "Renan Santos": "renan", "Ronaldo Caiado": "caiado", "Romeu Zema": "zema"}
            votos = g.assign(votos=g.candidato.map(nome).map(t1_2026).fillna(0.0))
            total_elim = float(t1_2026["cury"] + t1_2026["renan"] + t1_2026["caiado"] + t1_2026["zema"] + t1_2026["outros"])
        soma = lambda col, val: float(votos.loc[votos[col] == val, "votos"].sum())  # noqa: E731
        d = por_ano[por_ano.ano == ano].iloc[0]
        tr = trano[(trano.ano == ano) & (trano.origem_1t == "outros")].iloc[0]
        linhas.append({
            "ano": int(ano), "votos_eliminados": total_elim,
            "apoiou_pt_pct": 100 * soma("posicao_2t", "apoiou o PT") / total_elim,
            "apoiou_adversario_pct": 100 * soma("posicao_2t", "apoiou o adversário") / total_elim,
            "neutro_pct": 100 - 100 * (soma("posicao_2t", "apoiou o PT") + soma("posicao_2t", "apoiou o adversário")) / total_elim,
            "campo_pt_pct": 100 * soma("campo", "PT") / total_elim,
            "campo_adversario_pct": 100 * soma("campo", "adversário") / total_elim,
            "campo_centro_pct": 100 * soma("campo", "centro") / total_elim,
            "principais": "; ".join(f"{r.candidato} ({r.posicao_2t})" for r in votos.sort_values("votos", ascending=False).head(3).itertuples()),
            "ganho_pt": float(d.ganho_pt), "ganho_adversario": float(d.ganho_adversario),
            "parte_do_pt_nos_livres_pct": float(d.parte_do_pt_nos_livres_pct),
            "eliminados_para_pt_modelo_nacional_pct": float(tr.para_pt_pct),
            "eliminados_para_adversario_modelo_nacional_pct": float(tr.para_adversario_pct),
            "eliminados_para_pt_modelo_regional_pct": float(100 * d.pt_dos_outros / d.outros_livres)})
    return pd.DataFrame(linhas)


def ganho_dos_dois_como_seria(t1: dict, cruz: dict, novos_livres: float, novo_pt: float, novo_adv: float) -> dict:
    """O que o 2º turno daria se os eleitores dos eliminados votassem como disseram nas pesquisas e quem voltou a votar
    se dividisse como na regressão do próprio ano (coeficientes `novo_pt` e `novo_adv`)."""
    lula = cruz["lula_receberia"] + novos_livres * novo_pt / (novo_pt + novo_adv)
    flavio = cruz["flavio_receberia"] + novos_livres * novo_adv / (novo_pt + novo_adv)
    margem = (t1["lula"] + lula) - (t1["flavio"] + flavio)
    return {"lula_ganharia": lula, "flavio_ganharia": flavio, "margem_lula": margem}


# ------------------------------------------------------------------ 2. comparecimento e espalhamento
def comparecimento_e_espalhamento(p: pd.DataFrame) -> pd.DataFrame:
    """Por eleição, município a município: quanto o comparecimento mudou do 1º para o 2º turno e em quantos municípios
    subiu; quanto a diferença entre os dois andou no país e em quantos municípios andou para o mesmo lado."""
    out = []
    for ano, m in p.groupby("ano"):
        w = m.aptos1.to_numpy(float)
        marg1 = (m.pt1 - m.anti1) / m.validos1
        marg2 = (m.pt2 - m.anti2) / m.validos2
        nac = (m.pt2.sum() - m.anti2.sum()) / m.validos2.sum() - (m.pt1.sum() - m.anti1.sum()) / m.validos1.sum()
        d = 100 * (marg2 - marg1)
        dc = 100 * ((1 - m.abs2 / m.aptos2) - (1 - m.abs1 / m.aptos1))
        media_d = np.average(d, weights=w)
        out.append({
            "ano": int(ano), "municipios": int(len(m)),
            "abstencao_1t_pct": float(100 * m.abs1.sum() / m.aptos1.sum()),
            "abstencao_2t_pct": float(100 * m.abs2.sum() / m.aptos2.sum()),
            "comparecimento_variou_pontos": float(100 * (m.abs1.sum() / m.aptos1.sum() - m.abs2.sum() / m.aptos2.sum())),
            "municipios_comparecimento_subiu": int((dc > 0).sum()),
            "municipios_comparecimento_subiu_pct": float(100 * np.mean(dc > 0)),
            "desvio_da_mudanca_de_comparecimento": float(np.sqrt(np.average((dc - np.average(dc, weights=w)) ** 2, weights=w))),
            "diferenca_andou_no_pais_pontos": float(100 * nac),
            "municipios_mesmo_lado_do_pais": int((np.sign(d) == np.sign(nac)).sum()),
            "municipios_mesmo_lado_do_pais_pct": float(100 * np.mean(np.sign(d) == np.sign(nac))),
            "desvio_da_virada_entre_municipios": float(np.sqrt(np.average((d - media_d) ** 2, weights=w))),
            "pt_cresceu_em": int((m.pt2 > m.pt1).sum()), "adversario_cresceu_em": int((m.anti2 > m.anti1).sum())})
    return pd.DataFrame(out)


# ------------------------------------------------------------------ 3. a chance refeita
def _logistica(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    X = np.column_stack([np.ones(len(X)), X])

    def nll(b):
        z = X @ b
        return float(np.sum(np.logaddexp(0, z) - y * z))
    return minimize(nll, np.zeros(X.shape[1]), method="BFGS").x


def _chances(p: float) -> float:
    return p / (1 - p)


def _de_chances(o: float) -> float:
    return o / (1 + o)


def chance_refeita(casos: pd.DataFrame, erros: pd.DataFrame, erros_runoffs: pd.DataFrame, cres: pd.DataFrame,
                   campo: pd.DataFrame, frente_pesq: float, frente_1t: float, flavio_1t_pct: float, extra: float,
                   mercado: float, v2: dict) -> dict:
    """As três correções e os três jeitos de juntar os pilares.

    Correção 1 (histórico): a rodada 2 contou as viradas entre 2º turnos com frente parecida no 1º turno, sem olhar o
    quanto o líder estava perto de 50%; um líder com 47% precisa de bem menos votos novos que um com 32%. A regressão
    passa a usar as duas coisas.
    Correção 2 (crescimento): a rodada 2 aplicou os padrões de transferência dos 6 segundos turnos sem olhar quem eram os
    eliminados; em 2026 eram todos de fora do campo do PT. Passam a valer só os anos parecidos.
    Correção 3 (o jeito de juntar): média com pesos trata os pilares como opiniões que se substituem; quando são indícios
    que se somam, a conta é por chances (Bayes). Ficam as duas pontas e a do meio.
    """
    c = casos.dropna(subset=["frente_1t", "virada"]).copy()
    c["falta_lider"] = 50 - c.lider_1t_pct
    b = _logistica(c[["frente_1t", "falta_lider"]].to_numpy(float), c.virada.to_numpy(float))
    hist = float(1 / (1 + np.exp(-(b[0] + b[1] * frente_1t + b[2] * (50 - flavio_1t_pct)))))
    perto = c[(c.frente_1t <= 4) & (c.lider_1t_pct >= 45)]

    # pesquisas: a contagem da rodada 2 e a mesma contagem só com 2º turnos de presidente com 4 ou mais institutos
    e = erros.superestimou_lider.to_numpy(float)
    pesq = float(np.mean(e > frente_pesq))
    pesq_mag = float(np.mean(e > frente_pesq + extra))
    r4 = erros_runoffs[erros_runoffs.institutos >= 4].superestimou_lider.to_numpy(float)
    pesq_4 = float(np.mean(r4 > frente_pesq))

    # crescimento: só os padrões dos anos em que a maior parte dos eliminados estava fora do campo do PT
    anos_parecidos = campo[(campo.ano < 2026) & (campo.campo_pt_pct < 50)].ano.tolist()
    cp = cres[cres.padrao_de.isin(anos_parecidos)]
    venceria = int((cp.lula_pct > 50).sum())
    cres_lap = (venceria + 1) / (len(cp) + 2)

    pil = {"pesquisas": pesq, "historico": hist, "crescimento": cres_lap}
    w = {"pesquisas": 0.60, "historico": 0.25, "crescimento": 0.15}
    linear = sum(w[k] * pil[k] for k in w)
    bayes = _de_chances(_chances(hist) * _chances(pesq))
    independente = _de_chances(_chances(hist) * _chances(pesq) * _chances(cres_lap))
    bayes_mag = _de_chances(_chances(hist) * _chances(pesq_mag))
    variantes = {
        "rodada 2 (média com pesos, sem as correções)": v2["combinada"],
        "média com pesos, com as correções 1 e 2": linear,
        "Bayes: o histórico como ponto de partida e as pesquisas como indício (central)": bayes,
        "Bayes com as pesquisas só de presidente com 4 ou mais institutos": _de_chances(_chances(hist) * _chances(pesq_4)),
        "os três pilares como indícios independentes (ponta de baixo)": independente,
        "mercado (Polymarket, véspera)": mercado}
    return {"historico": {"logistica": {"a": float(b[0]), "frente": float(b[1]), "falta_lider_para_50": float(b[2])},
                          "chance": hist, "rodada_2": v2["pilares"]["historico"], "casos": int(len(c)),
                          "perto_de_50_casos": int(len(perto)), "perto_de_50_viradas": int(perto.virada.sum()),
                          "perto_de_50_lista": perto.sort_values("frente_1t").to_dict("records")},
            "pesquisas": {"chance": pesq, "chance_resultado_igual_ou_maior": pesq_mag, "so_presidente_4_institutos": pesq_4,
                          "casos_4_institutos": int(len(r4)), "casos": int(len(e))},
            "crescimento": {"anos_parecidos": anos_parecidos, "lula_venceria_em": venceria, "padroes": int(len(cp)),
                            "laplace": cres_lap, "rodada_2": v2["pilares"]["crescimento"],
                            "lula_pct_por_padrao": cp[["padrao_de", "lula_pct"]].round(2).to_dict("records")},
            "pilares": pil, "linear": linear, "bayes": bayes, "independente": independente,
            "bayes_resultado_igual_ou_maior": bayes_mag, "mercado": mercado, "variantes": variantes}


# ------------------------------------------------------------------ 4. rodada 6: as contas dos vídeos que circularam
def conta_dos_60_por_cento(variacao: dict, parte_dos_outros: float = 0.60) -> dict:
    """A conta de um vídeo que circulou: se os eleitores de Lula e Flávio repetiram o voto e 60% dos votos dos outros
    candidatos foram para o Lula, quanto dos votos novos (abstenção e branco e nulo que caíram) o Lula precisou levar."""
    outros = -variacao["outros_candidatos"]
    novos = -variacao["abstencao"] - variacao["branco_nulo"]
    falta = variacao["lula"] - parte_dos_outros * outros
    return {"outros": outros, "novos": novos, "lula_dos_outros": parte_dos_outros * outros, "falta": falta,
            "parte_dos_novos_pct": 100 * falta / novos,
            "flavio_dos_outros_se_40": (1 - parte_dos_outros) * outros, "flavio_ganhou": variacao["flavio"]}


def votos_novos_por_faixa(p: pd.DataFrame, anos=(2022, 2026)) -> pd.DataFrame:
    """Municípios em 5 grupos do mesmo tamanho pela mudança do comparecimento. Se quem voltou a votar tivesse ido quase
    todo para um lado, a parte desse lado no que os dois ganharam subiria de um grupo para o outro."""
    out = []
    for ano in anos:
        v = p[p.ano == ano].copy()
        v["dc"] = 100 * (v.abs1 - v.abs2) / v.aptos1
        v["grupo"] = pd.qcut(v.dc.rank(method="first"), 5, labels=["1 (caiu mais)", "2", "3", "4", "5 (subiu mais)"])
        for g, x in v.groupby("grupo", observed=True):
            gl, gf, e = (x.pt2 - x.pt1).sum(), (x.anti2 - x.anti1).sum(), x.aptos1.sum()
            out.append({"ano": int(ano), "grupo": str(g), "municipios": int(len(x)),
                        "comparecimento_variou_pontos": float(np.average(x.dc, weights=x.aptos1)),
                        "votos_novos_por_100": float(100 * ((x.abs1 - x.abs2) + (x.bn1 - x.bn2)).sum() / e),
                        "pt_ganhou_por_100": float(100 * gl / e), "adversario_ganhou_por_100": float(100 * gf / e),
                        "parte_do_pt_no_ganho_pct": float(100 * gl / (gl + gf))})
    return pd.DataFrame(out)


def divisao_simples_por_ano(p: pd.DataFrame) -> pd.DataFrame:
    """A conta mais simples que separa as duas origens: em cada município, o ganho de cada lado como uma parte dos votos
    dos outros candidatos mais uma parte dos votos novos (sem constante, ponderado pelo eleitorado)."""
    out = []
    for ano, v in p.groupby("ano"):
        e = v.aptos1.to_numpy(float)
        X = np.column_stack([v.out1 / e, ((v.abs1 - v.abs2) + (v.bn1 - v.bn2)) / e])
        lin = {}
        for lado, col in (("pt", "pt"), ("adversario", "anti")):
            y = ((v[f"{col}2"] - v[f"{col}1"]) / e).to_numpy(float)
            b, *_ = np.linalg.lstsq(X * np.sqrt(e)[:, None], y * np.sqrt(e), rcond=None)
            lin[lado] = b
        out.append({"ano": int(ano), "outros_para_pt": float(lin["pt"][0]), "outros_para_adversario": float(lin["adversario"][0]),
                    "novos_para_pt": float(lin["pt"][1]), "novos_para_adversario": float(lin["adversario"][1])})
    return pd.DataFrame(out)


def onde_ninguem_novo_votou(p: pd.DataFrame) -> pd.DataFrame:
    """Municípios em que o comparecimento caiu do 1º para o 2º turno (não houve voto novo no saldo): quanto cada lado
    ganhou ali, em cada eleição."""
    out = []
    for ano, v in p.groupby("ano"):
        x = v[v.abs2 >= v.abs1]
        gl, gf = (x.pt2 - x.pt1).sum(), (x.anti2 - x.anti1).sum()
        out.append({"ano": int(ano), "municipios": int(len(x)), "eleitores": float(x.aptos1.sum()), "pt_ganhou": float(gl),
                    "adversario_ganhou": float(gf), "votos_dos_outros": float(x.out1.sum()),
                    "pt_ganhou_sobre_os_outros_pct": float(100 * gl / x.out1.sum())})
    return pd.DataFrame(out)


def simulacao_com_as_taxas_de_um_ano(p: pd.DataFrame, ano_base: int, desvio: float = 0.2, n: int = 10_000,
                                     semente: int = 2026) -> dict:
    """A simulação mostrada num dos vídeos (Tarcísio de Freitas): em cada UF, a taxa de conversão dos votos dos outros
    candidatos do ano-base ((votos 2º turno − votos 1º turno) ÷ votos dos outros no 1º turno, para cada lado), aplicada
    ao 1º turno de 2026, com um fator aleatório normal em volta de 1, n vezes. Feita para cada ano-base, para mostrar
    que a resposta depende do ano escolhido."""
    u = p.groupby(["ano", "uf"])[["pt1", "anti1", "out1", "pt2", "anti2"]].sum()
    base, alvo = u.loc[ano_base], u.loc[2026]
    tl = (base.pt2 - base.pt1) / base.out1
    tf = (base.anti2 - base.anti1) / base.out1
    x = alvo.join(pd.DataFrame({"tl": tl, "tf": tf}), how="inner")
    lula = (x.pt1 + x.out1 * x.tl).sum()
    flavio = (x.anti1 + x.out1 * x.tf).sum()
    rng = np.random.default_rng(semente)
    ganha = 0
    for _ in range(n):
        ls = (x.pt1 + x.out1 * x.tl * rng.normal(1, desvio, len(x))).sum()
        fs = (x.anti1 + x.out1 * x.tf * rng.normal(1, desvio, len(x))).sum()
        ganha += ls > fs
    return {"ano_base": int(ano_base), "lula_pct": float(100 * lula / (lula + flavio)), "lula_venceu_em": int(ganha),
            "simulacoes": int(n), "desvio_do_fator": desvio}


# ------------------------------------------------------------------ 5. rodada 7: o espalhamento contra a série, e as pesquisas antes e depois do pagamento
def quem_ganhou_mais_por_ano(p: pd.DataFrame) -> pd.DataFrame:
    """Por eleição: em quantos municípios o PT ganhou mais votos que o adversário do 1º para o 2º turno, e, por região,
    a parte do PT no que os dois ganharam."""
    from .comum import REGIAO
    out = []
    for ano, v in p.groupby("ano"):
        gl, gf = v.pt2 - v.pt1, v.anti2 - v.anti1
        r = {"ano": int(ano), "pt_ganhou_mais_votos_em_pct": float(100 * np.mean(gl > gf)),
             "pt_ganhou_mais_votos_em": int((gl > gf).sum()), "municipios": int(len(v))}
        reg = v.uf.str.lower().map(REGIAO)
        for nome, x in v.groupby(reg):
            a, b = (x.pt2 - x.pt1).sum(), (x.anti2 - x.anti1).sum()
            r[f"parte_do_pt_{nome}"] = float(100 * a / (a + b))
        out.append(r)
    return pd.DataFrame(out)


def pesquisas_antes_e_depois(pesq: pd.DataFrame, dia: str = "2026-10-19") -> dict:
    """Se o pagamento do Bolsa Família (19, 20 e 21/10) tivesse virado votos em escala, as pesquisas de campo depois
    dele mostrariam: a mesma empresa, antes e depois."""
    c = pesq[pesq.conferida == True].copy()  # noqa: E712
    c["ini"] = pd.to_datetime(c.campo_ini, format="mixed")
    c["fim"] = pd.to_datetime(c.campo_fim, format="mixed")
    c["lula"] = 100 * c.lula_total / (c.lula_total + c.flavio_total)
    pares = []
    for inst, g in c.groupby("instituto"):
        a = g[g.fim < dia].sort_values("fim").tail(1)
        d = g[g.ini >= dia].sort_values("fim").tail(1)
        if len(a) and len(d):
            pares.append({"instituto": inst, "antes": float(a.lula.iloc[0]), "depois": float(d.lula.iloc[0])})
    pr = pd.DataFrame(pares)
    return {"institutos": int(len(pr)), "variacao_media": float((pr.depois - pr.antes).mean()),
            "media_antes": float(c[c.fim < dia].lula.mean()), "media_depois": float(c[c.ini >= dia].lula.mean()),
            "pares": pr.round(2).to_dict("records")}
