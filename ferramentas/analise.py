"""Roda todas as contas e grava resultados/RESUMO.json e as tabelas em resultados/.

Uso: python ferramentas/analise.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pandas as pd  # noqa: E402

from analise import alegacoes as A  # noqa: E402
from analise import historia as HI  # noqa: E402
from analise import modelo as M  # noqa: E402
from analise import normalidade as NO  # noqa: E402
from analise import porque as QQ  # noqa: E402
from analise import probabilidade as PB  # noqa: E402
from analise.comum import COPIAS, DERIV  # noqa: E402
from analise.comum import RES, salvar_json  # noqa: E402


def main() -> None:
    RES.mkdir(parents=True, exist_ok=True)
    ab, mu = M.carregar_resultado()
    r = M.resultado_nacional(ab)
    lula = r["t2"]["lula_pct"]
    p = M.carregar_pesquisas(lula)
    sp = M.resumo_pesquisas(p, lula)
    hp = M.historico_erro_pesquisas()
    reg = M.regras_historicas(ab)
    est = M.estados(ab)
    m, rm = M.municipios(mu)
    tr = M.transferencia(mu, reamostras=200)
    gov = M.governadores(ab)
    gv = M.governador_viradas_2026()
    he = M.erro_historico_da_media()
    pr = M.probabilidades(sp["ultima_de_cada_instituto"]["media_lula"], r, he, reg)
    te = M.testes_das_lentes(m)

    p.to_csv(RES / "pesquisas_2t.csv", index=False)
    reg.pop("_tabela_ufs").to_csv(RES / "regra_uf_acerta_presidente.csv", index=False)
    est.to_csv(RES / "estados.csv", index=False)
    m[m.virou != ""][["uf", "municipio", "virou", "eleitores_1t", "lula_pct_1t", "lula_pct_2t", "lula_ganhou", "flavio_ganhou"]].sort_values(
        "eleitores_1t", ascending=False).to_csv(RES / "municipios_que_viraram.csv", index=False)
    m[["uf", "cd_tse", "cd_ibge", "municipio", "regiao", "eleitores_1t", "lula_pct_1t", "lula_pct_2t", "venc_1t", "venc_2t",
       "lula_ganhou", "flavio_ganhou", "outros_1t", "abstencao_caiu", "branco_nulo_caiu", "abstencao_pct_1t", "abstencao_pct_2t"]].to_csv(
        RES / "municipios.csv", index=False)
    tr["tabela"].to_csv(RES / "transferencia_de_votos.csv", index=False)
    tr["matriz_unica_pais_pct"].to_csv(RES / "transferencia_matriz_unica_pais_pct.csv")
    gov.to_csv(RES / "governador_e_presidente.csv", index=False)
    he.to_csv(RES / "erro_historico_media_pesquisas.csv", index=False)

    resumo = {
        "resultado": r, "pesquisas": sp, "historico_erro_pesquisas": hp, "regras": reg, "municipios": rm,
        "estados": {"viraram": est[est.virou != ""][["uf", "virou"]].to_dict("records"),
                    "lula_subiu_em": int((est.variacao_lula_pontos > 0).sum()),
                    "lula_subiu_min": float(est[est.uf != "zz"].variacao_lula_pontos.min()),
                    "lula_subiu_max": float(est[est.uf != "zz"].variacao_lula_pontos.max()),
                    "lula_venceu_1t": int((est[est.uf != "zz"].vencedor_1t == "Lula").sum()),
                    "lula_venceu_2t": int((est[est.uf != "zz"].vencedor_2t == "Lula").sum()),
                    "abstencao_subiu_em": est[(est.abstencao_variou > 0) & (est.uf != "zz")].uf.tolist(),
                    "flavio_perdeu_votos_em": est[(est.flavio_ganhou < 0) & (est.uf != "zz")].uf.tolist()},
        "transferencia": {"tabela": tr["tabela"].to_dict("records"), "observado_2t": tr["observado_2t"], "previsto_2t": tr["previsto_2t"],
                          "por_regiao_pct": tr["por_regiao_pct"], "matriz_unica_pais_pct": tr["matriz_unica_pais_pct"].round(2).to_dict()},
        "governador": {"mesmo_lado": int(gov.mesmo_lado.sum()), "ufs": int(len(gov)),
                       "lado": gov.lado_da_coligacao.value_counts().to_dict(),
                       "lado_diferente": gov[(~gov.mesmo_lado) & (gov.lado_da_coligacao.isin(["Lula", "Flávio"]))][
                           ["uf", "governador_eleito", "lado_da_coligacao", "presidente_venceu_no_estado"]].to_dict("records"),
                       "viradas_2t_2026": gv},
        "probabilidade": pr, "testes_das_lentes": te,
        "projecao_video_14": {"flavio_projetado": 50.848739823887946, "flavio_urna": r["t2"]["flavio_pct"],
                              "erro": 50.848739823887946 - r["t2"]["flavio_pct"], "erro_medio_teste_do_passado": 1.8},
    }
    # ------------------------------------------------------------ rodada 2: histórico, alegações e a probabilidade em pilares
    painel = HI.painel()
    testes = HI.testes_por_ano(painel)
    trano = HI.transferencia_por_ano(painel)
    novos = HI.eleitores_novos(painel)
    ext = HI.exterior(None)
    cres = HI.crescimento_por_padrao_passado(painel, trano)
    for df, nome in ((testes, "testes_por_ano"), (trano, "transferencia_por_ano"), (novos, "eleitores_novos_por_ano"),
                     (ext, "exterior_por_ano"), (cres, "crescimento_pelos_padroes_passados")):
        df.to_csv(RES / f"{nome}.csv", index=False)
    resumo["historia"] = {"testes": testes.to_dict("records"), "transferencia": trano.to_dict("records"),
                          "eleitores_novos": novos.to_dict("records"), "exterior": ext.to_dict("records")}
    resumo["alegacoes"] = {"curva": A.curva_da_apuracao(), "prorrogacao": A.teto_prorrogacao(), "exterior": A.teto_exterior()}

    frente_pesq = pr["frente_flavio_nas_pesquisas"]
    extra = r["variacao"]["frente_2t_pontos"]
    # erro histórico da média das pesquisas: Brasil (presidente e governador, 2014 a 2022) e, se conferidos, os outros casos
    # governador no Brasil pela base do Pindograma; presidente no Brasil (2002 a 2022) e outros países pela pesquisa de
    # apoio conferida número a número (a última pesquisa de cada instituto na semana final)
    gov = he[he.cargo == "governador"]
    erros = gov.assign(fonte="Brasil governador", pais="Brasil")[["fonte", "pais", "ano", "superestimou_lider"]]
    ep = DERIV / "erros_pesquisas_conferidos.csv"
    if ep.exists():
        e2 = PB.erros_de_media_por_eleicao(pd.read_csv(ep))
        e2.to_csv(RES / "erro_media_pesquisas_runoffs.csv", index=False)
        erros = pd.concat([erros, e2.assign(fonte=lambda d: d.pais.where(d.pais != "Brasil", "Brasil presidente").where(d.pais == "Brasil", "outros países"))[
            ["fonte", "pais", "ano", "superestimou_lider"]]])
    else:
        erros = pd.concat([erros, he[he.cargo == "presidente"].assign(fonte="Brasil presidente", pais="Brasil")[["fonte", "pais", "ano", "superestimou_lider"]]])
    erros.to_csv(RES / "erro_media_pesquisas_todos.csv", index=False)
    p_pesq = PB.prob_pesquisas(frente_pesq, erros.superestimou_lider.values, extra)
    p_pesq["por_fonte"] = {f: PB.prob_pesquisas(frente_pesq, g.superestimou_lider.values, extra)
                           for f, g in erros.groupby("fonte")}
    # viradas: Brasil (presidente e governador) e, se conferidos, 2º turnos presidenciais de outros países
    seg = pd.read_csv(COPIAS / "investigacao-segundo-turno-2026" / "p_segundos_turnos.csv")
    casos = pd.DataFrame({"frente_1t": seg.frente_1t_pontos, "lider_1t_pct": seg.lider_1t_pct, "virada": seg.virada,
                          "grupo": "Brasil " + seg.cargo, "pais": "Brasil", "ano": seg.ano, "uf": seg.uf})
    rp = DERIV / "runoffs_conferidos.csv"
    if rp.exists():
        ri = pd.read_csv(rp)
        # fora: 2º turnos anulados depois de acontecer (Sérvia, setembro de 1997 e setembro de 2002)
        anulados = ri.url_wikipedia.str.contains("1997_Serbian_general_election|September%E2%80%93October_2002", regex=True)
        ri = ri[ri.conferida & (ri.pais != "Brasil") & ~anulados]
        casos = pd.concat([casos, pd.DataFrame({"frente_1t": ri.lider_1t_pct - ri.segundo_1t_pct, "lider_1t_pct": ri.lider_1t_pct,
                                                "virada": ri.virada, "grupo": "presidente, outros países", "pais": ri.pais, "ano": ri.ano})])
    casos.to_csv(RES / "viradas_casos.csv", index=False)
    v1 = r["variacao"]["frente_1t_pontos"]
    p_hist = PB.prob_historico(casos, v1, r["t1"]["flavio_pct"])
    p_cres = PB.prob_crescimento(cres, r["t2"]["lula_pct"])
    # cada pilar pela conta mais simples de explicar: a contagem de casos passados (a curva normal e a logística ficam como conferência)
    pil = {"pesquisas": p_pesq["contagem"], "historico": p_hist["faixa_viradas"] / p_hist["faixa_casos"], "crescimento": p_cres["contagem"]}
    pil_mag = {"pesquisas": p_pesq["contagem_resultado_igual_ou_maior"], "historico": None, "crescimento": p_cres["resultado_igual_ou_maior"] / max(p_cres["padroes"], 1)}
    combinada = PB.combinar(pil)
    sens = {"pesos do vídeo 14 (60, 25, 15)": combinada,
            "pesos iguais": PB.combinar(pil, {"pesquisas": 1 / 3, "historico": 1 / 3, "crescimento": 1 / 3}),
            "só pesquisas": pil["pesquisas"],
            "60, 25, 15 com o mercado no lugar do crescimento": 0.6 * pil["pesquisas"] + 0.25 * pil["historico"] + 0.15 * pr["polymarket_lula_vespera"],
            "pesquisas só do presidente no Brasil": 0.6 * pr["pesquisas_normal_so_presidente"] + 0.25 * pil["historico"] + 0.15 * pil["crescimento"],
            "histórico só do presidente no Brasil (Laplace)": 0.6 * pil["pesquisas"] + 0.25 * pr["historico_laplace"] + 0.15 * pil["crescimento"],
            "pesquisas corrigidas pelo viés do Brasil (presidente, 2002 a 2022)": 0.6 * p_pesq["por_fonte"].get("Brasil presidente", {}).get("normal", pil["pesquisas"]) + 0.25 * pil["historico"] + 0.15 * pil["crescimento"]}
    resumo["probabilidade_v2"] = {"pesos": PB.PESOS, "frente_flavio_pesquisas": frente_pesq, "frente_flavio_1t": v1,
                                  "pesquisas": p_pesq, "historico": p_hist, "crescimento": p_cres, "pilares": pil,
                                  "pilares_resultado_igual_ou_maior": pil_mag, "combinada": combinada,
                                  "mercado": pr["polymarket_lula_vespera"], "sensibilidade": sens,
                                  "soma_ingenua": A.soma_ingenua({"pesquisas": pil["pesquisas"], "historico": pr["historico_laplace"],
                                                                  "minas": 1 / 10, "mercado": pr["polymarket_lula_vespera"]}, combinada)}
    # de onde vieram os votos: as três origens, por eleição, por UF e por candidato eliminado
    dov = HI.de_onde_vieram(painel)
    ond = HI.onde(painel)
    pc = HI.por_candidato_2026()
    dov.to_csv(RES / "de_onde_vieram_por_ano.csv", index=False)
    ond.to_csv(RES / "de_onde_vieram_por_uf_2026.csv", index=False)
    pc.to_csv(RES / "de_onde_vieram_por_candidato_2026.csv", index=False)
    d26 = dov[dov.ano == 2026].iloc[0]
    ajustes = {"por região": (d26.pt_dos_outros, d26.pt_dos_novos, d26.pt_da_troca - d26.pt_perdeu_na_troca),
               "país inteiro": (d26.pais_pt_dos_outros, d26.pais_pt_dos_novos, d26.pais_pt_da_troca),
               "estado por estado": tuple(float(ond[k].sum()) for k in ("pt_dos_outros", "pt_dos_novos", "pt_da_troca"))}
    resumo["de_onde"] = {"por_ano": dov.to_dict("records"), "por_uf": ond.to_dict("records"), "por_candidato": pc.to_dict("records"),
                         "ajustes_2026": {k: {"dos_outros": float(a_), "dos_novos": float(b_), "da_troca": float(c_)} for k, (a_, b_, c_) in ajustes.items()},
                         "outros_livres": float(d26.outros_livres), "novos_livres": float(d26.novos_livres),
                         "ganho_lula_municipios": float(d26.ganho_pt), "ganho_flavio_municipios": float(d26.ganho_adversario)}
    # rodada 4: o porquê (onde a virada aconteceu, o eleitor de direita, a renda, a tendência das pesquisas)
    tend = QQ.tendencia_pesquisas(p)
    tend.to_csv(RES / "tendencia_das_pesquisas.csv", index=False)
    resumo["porque"] = {"onde": QQ.onde_a_virada(), "direita": QQ.eleitor_da_direita(), "renda": QQ.por_renda(),
                        "tendencia": tend.to_dict("records")}
    cz = DERIV / "cruzamento_voto_1t_conferido.csv"
    if cz.exists():
        t1 = r["t1"]
        resumo["transferencia_pesquisas"] = A.transferencia_pelas_pesquisas(pd.read_csv(cz), {"cury": t1["cury"], "renan": t1["renan"], "caiado": t1["caiado"]})
    # rodada 5: isso é normal? (o campo dos eliminados, o comparecimento e o espalhamento, a chance refeita)
    campo = NO.campo_dos_eliminados(dov, trano, r["t1"])
    comp = NO.comparecimento_e_espalhamento(painel)
    campo.to_csv(RES / "campo_dos_eliminados_por_ano.csv", index=False)
    comp.to_csv(RES / "comparecimento_e_espalhamento_por_ano.csv", index=False)
    n26 = novos[novos.ano == 2026].iloc[0]
    tp = resumo.get("transferencia_pesquisas")
    seria = NO.ganho_dos_dois_como_seria(r["t1"], tp, float(d26.novos_livres), float(n26.novo_eleitor_para_pt),
                                         float(n26.novo_eleitor_para_adversario)) if tp else None
    ch = NO.chance_refeita(casos, erros, pd.read_csv(RES / "erro_media_pesquisas_runoffs.csv"), cres, campo, frente_pesq, v1,
                           r["t1"]["flavio_pct"], extra, pr["polymarket_lula_vespera"], resumo["probabilidade_v2"])
    resumo["normalidade"] = {"campo": campo.to_dict("records"), "comparecimento": comp.to_dict("records"),
                             "como_seria_pelas_pesquisas": seria, "chance": ch}
    # rodada 6: as contas dos vídeos que circularam depois do resultado
    faixas = NO.votos_novos_por_faixa(painel)
    divisao = NO.divisao_simples_por_ano(painel)
    sem_novos = NO.onde_ninguem_novo_votou(painel)
    for df, nome in ((faixas, "votos_novos_por_faixa"), (divisao, "divisao_simples_por_ano"), (sem_novos, "onde_ninguem_novo_votou")):
        df.to_csv(RES / f"{nome}.csv", index=False)
    resumo["videos"] = {"conta_dos_60": NO.conta_dos_60_por_cento(r["variacao"]), "faixas": faixas.to_dict("records"),
                        "divisao": divisao.to_dict("records"), "sem_novos": sem_novos.to_dict("records"),
                        "simulacao_por_ano": [NO.simulacao_com_as_taxas_de_um_ano(painel, a) for a in (2002, 2006, 2010, 2014, 2018, 2022)]}
    # rodada 7: o espalhamento contra a série e as pesquisas antes e depois do pagamento do Bolsa Família
    qg = NO.quem_ganhou_mais_por_ano(painel)
    qg.to_csv(RES / "quem_ganhou_mais_por_ano.csv", index=False)
    resumo["rodada7"] = {"quem_ganhou_mais": qg.to_dict("records"),
                         "pesquisas_antes_e_depois": NO.pesquisas_antes_e_depois(pd.read_csv(DERIV / "pesquisas_2t_conferidas.csv"))}
    salvar_json(resumo, RES / "RESUMO.json")
    print("ok: resultados/RESUMO.json")


if __name__ == "__main__":
    main()
