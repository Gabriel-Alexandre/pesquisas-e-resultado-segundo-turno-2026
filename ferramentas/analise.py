"""Roda todas as contas e grava resultados/RESUMO.json e as tabelas em resultados/.

Uso: python ferramentas/analise.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analise import modelo as M  # noqa: E402
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
    salvar_json(resumo, RES / "RESUMO.json")
    print("ok: resultados/RESUMO.json")


if __name__ == "__main__":
    main()
