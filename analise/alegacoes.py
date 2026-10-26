"""As alegações de fraude ou de improbabilidade, na versão mais forte, cada uma com o teste que o dado deste projeto
permite fazer, sempre com 2002 a 2022 como controle e com o espelho do outro candidato.

O mapa das alegações (quem disse, onde, a versão mais forte e o que precisaria ser verdade no dado) está em
dados/agentes/alegacoes_fraude_2026.md, levantado por uma pesquisa de apoio; cada link é a fonte da alegação, não do
número. Números de terceiros citados aqui (votos depois das 17h nos logs) são marcados como de terceiros.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .comum import COPIAS, DERIV


def curva_da_apuracao() -> dict:
    """A frente do candidato contra o PT ao longo da apuração, em 2022 e em 2026 (pontos, por % de seções)."""
    c22 = pd.read_csv(COPIAS / "apuracao-eleicoes-2026" / "p7_margem_2022_por_pct_de_secoes.csv")
    c22 = c22[c22.turno == 2]
    c26 = pd.read_csv(COPIAS / "investigacao-segundo-turno-2026" / "d5_curva_noite.csv")
    c26 = c26.assign(frente_anti=-c26.vantagem_lula)
    cruz22 = float(np.interp(0, -c22.margem.to_numpy(), c22.pct_secoes.to_numpy()))
    # a virada que ficou: a primeira versão depois da última em que o Flávio ainda estava na frente
    ultima_anti = c26[c26.frente_anti >= 0].index.max()
    vira = c26.loc[ultima_anti + 1:]
    out = {"2022": {"maior_frente_anti": float(c22.margem.max()), "pt_passa_com_pct": cruz22,
                    "pontos": c22[["pct_secoes", "margem"]].rename(columns={"margem": "frente_anti"}).to_dict("records")},
           "2026": {"maior_frente_anti": float(c26.frente_anti.max()),
                    "maior_frente_anti_pct": float(c26.loc[c26.frente_anti.idxmax(), "pct_secoes"]),
                    "pt_passa_com_pct": float(vira.pct_secoes.iloc[0]) if len(vira) else None,
                    "pt_passa_hora": str(vira.gerado.iloc[0]) if len(vira) else None,
                    "versoes": int(len(c26)),
                    "flavio_passa_com_pct": float(c26[(c26.pct_secoes > 1) & (c26.frente_anti > 0)].pct_secoes.iloc[0]),
                    "flavio_passa_hora": str(c26[(c26.pct_secoes > 1) & (c26.frente_anti > 0)].gerado.iloc[0])}}
    q = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
    out["2026"]["pontos"] = [{"pct_secoes": float(c26[c26.pct_secoes <= x].pct_secoes.iloc[-1]),
                              "frente_anti": float(c26[c26.pct_secoes <= x].frente_anti.iloc[-1])} for x in q]
    return out


def teto_prorrogacao() -> dict:
    """Pior caso das três cidades em que a falta de ônibus motivou o pedido: e se todo voto do Lula ali não valesse?"""
    m = pd.read_csv(DERIV / "presidente_municipio.csv", dtype={"cd_tse": str})
    x = m[(m.uf == "ba") & m.municipio.isin(["SALVADOR", "FEIRA DE SANTANA", "LAURO DE FREITAS"])]
    lula2, fl2 = float(m.lula_2t.sum()), float(m.flavio_2t.sum())
    return {"municipios": x.municipio.tolist(), "votantes_a_mais_no_2t": float((x.comparecimento_2t - x.comparecimento_1t).sum()),
            "lula_ganhou_ali": float((x.lula_2t - x.lula_1t).sum()), "lula_2t_ali": float(x.lula_2t.sum()),
            "frente_nacional": lula2 - fl2,
            "frente_sem_nenhum_voto_do_lula_ali": lula2 - float(x.lula_2t.sum()) - fl2,
            "frente_sem_o_ganho_do_lula_ali": lula2 - float((x.lula_2t - x.lula_1t).sum()) - fl2,
            "votos_depois_das_17h_logs_terceiros": {"g1_tv_globo": 35521, "eleicao_kakaroto_dev": 34330,
                                                    "fonte": "dados/agentes/alegacoes_fraude_2026.md, tipo (d); contagem de terceiros, não refeita aqui"}}


def teto_exterior() -> dict:
    ab = pd.read_csv(DERIV / "presidente_abrangencia.csv")
    z = ab[(ab.abr == "zz") & (ab.turno == 2)].iloc[0]
    b = ab[(ab.abr == "br") & (ab.turno == 2)].iloc[0]
    return {"aptos_exterior": float(z.eleitores), "lula_exterior": float(z.lula), "flavio_exterior": float(z.flavio),
            "saldo_exterior": float(z.lula - z.flavio), "frente_nacional": float(b.lula - b.flavio),
            "frente_sem_o_exterior": float((b.lula - z.lula) - (b.flavio - z.flavio))}


def soma_ingenua(probs: dict, correta: float) -> dict:
    """O erro de multiplicar as "coincidências": pesquisas erraram, o líder do 1º turno perdeu, a regra de Minas quebrou,
    o favorito do mercado perdeu. As quatro são o mesmo fato (o Lula venceu uma disputa apertada) visto de quatro lugares;
    dado que o Lula venceu, todas aconteceriam juntas. Multiplicar trata como independentes o que não é."""
    p = [probs["pesquisas"], probs["historico"], probs["minas"], probs["mercado"]]
    return {"produto_ingenuo": float(np.prod(p)), "um_em_ingenuo": float(1 / np.prod(p)),
            "probabilidade_correta": float(correta), "um_em_correta": float(1 / correta), "componentes": probs}


def transferencia_pelas_pesquisas(cruz: pd.DataFrame, votos_1t: dict) -> dict:
    """O que as pesquisas diziam sobre o eleitor de cada candidato eliminado: a última rodada de cada instituto com o
    cruzamento (conferido na fonte), a parte do Lula entre Lula e Flávio, média simples entre institutos; e quantos votos
    isso daria a cada um, se os eleitores desses candidatos fossem votar na mesma proporção."""
    c = cruz[(cruz.conferida) & (cruz.ano == 2026) & cruz.grupo_1t.isin(list(votos_1t))].copy()
    c["campo_fim"] = pd.to_datetime(c.campo_fim)
    c = c.sort_values("campo_fim").groupby(["instituto", "grupo_1t"]).tail(1)
    c["lula_dois"] = 100 * c.pct_lula / (c.pct_lula + c.pct_adversario)
    out = {"por_grupo": {}, "linhas": c[["instituto", "campo_fim", "grupo_1t", "pct_lula", "pct_adversario", "lula_dois"]].astype(str).to_dict("records")}
    lula = flavio = 0.0
    for g, x in c.groupby("grupo_1t"):
        m = float(x.lula_dois.mean())
        votam = float((x.pct_lula + x.pct_adversario).mean()) / 100  # parte que escolhia um dos dois
        out["por_grupo"][g] = {"institutos": int(len(x)), "lula_entre_os_dois": m, "escolhiam_um_dos_dois": votam,
                               "minimo": float(x.lula_dois.min()), "maximo": float(x.lula_dois.max())}
        lula += votos_1t[g] * votam * m / 100
        flavio += votos_1t[g] * votam * (100 - m) / 100
    out["lula_receberia"] = lula
    out["flavio_receberia"] = flavio
    return out
