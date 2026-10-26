"""Gráficos 1920x1080 para o vídeo, a partir de resultados/RESUMO.json e das tabelas em resultados/.

Cores iguais em todos os projetos do canal (Lula #C8553D, Flávio #2D6A8A, base #6B6B6B); toda barra leva o número
escrito ao lado, então a cor nunca é a única pista. Rodapé com a fonte e o endereço do repositório.
Uso: python ferramentas/graficos.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analise.comum import COR, FIG, REPO, RES  # noqa: E402

TINTA, TINTA2, GRADE, FUNDO = "#1F1F1F", "#5A5A5A", "#E4E2DD", "#FCFCFB"
OUTROS = "#9C7A2E"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 22, "axes.edgecolor": GRADE, "axes.labelcolor": TINTA2,
                     "xtick.color": TINTA2, "ytick.color": TINTA2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": FUNDO, "axes.facecolor": FUNDO})


def br(x: float, casas: int = 1) -> str:
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def mi(x: float) -> str:
    return f"{br(x / 1e6, 2)} mi"


def figura(titulo: str, subtitulo: str = ""):
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.text(0.05, 0.93, titulo, fontsize=40, weight="bold", color=TINTA)
    if subtitulo:
        fig.text(0.05, 0.885, subtitulo, fontsize=24, color=TINTA2)
    return fig


def rodape(fig, fonte: str) -> None:
    fig.text(0.05, 0.045, f"Fonte: {fonte}.", fontsize=16, color=TINTA2)
    fig.text(0.05, 0.018, f"Análise feita pelo Claude · {REPO}", fontsize=16, color=TINTA2)


def salvar(fig, nome: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / nome, dpi=100, facecolor=FUNDO)
    plt.close(fig)
    print(nome)


def g01_de_onde_vieram(R):
    v, t1 = R["resultado"]["variacao"], R["resultado"]["t1"]
    fig = figura("De onde vieram os votos do 2º turno, no saldo",
                 "O que os dois ganharam juntos é exatamente o que saiu dos outros, da abstenção e do branco e nulo")
    ax = fig.add_axes([0.08, 0.14, 0.86, 0.66])
    itens = [("Votos dos outros\ncandidatos", -v["outros_candidatos"], OUTROS), ("Voltaram a votar\n(abstenção caiu)", -v["abstencao"], "#8A8A8A"),
             ("Deixaram de votar\nbranco ou nulo", -v["branco_nulo"], "#B0B0B0"), ("Lula ganhou", v["lula"], COR["lula"]), ("Flávio ganhou", v["flavio"], COR["flavio"])]
    x = [0, 1, 2, 3.6, 4.6]
    for xi, (nome, val, cor) in zip(x, itens):
        ax.bar(xi, val / 1e6, width=0.7, color=cor)
        ax.text(xi, val / 1e6 + 0.2, mi(val), ha="center", fontsize=26, weight="bold", color=TINTA)
        ax.text(xi, -0.5, nome, ha="center", va="top", fontsize=20, color=TINTA2)
    ax.axvline(2.8, color=GRADE, lw=2)
    ax.text(1, 11.3, f"Livres para o 2º turno: {mi(-v['outros_candidatos'] - v['abstencao'] - v['branco_nulo'])}", ha="center", fontsize=22, color=TINTA)
    ax.text(4.1, 11.3, f"Ganho dos dois: {mi(v['ganho_dos_dois'])} ({br(v['parte_do_lula_no_ganho'])}% do Lula)", ha="center", fontsize=22, color=TINTA)
    ax.set_ylim(0, 12)
    ax.set_xlim(-0.6, 5.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    rodape(fig, "TSE, resultado oficial do 1º turno (04/10) e do 2º turno (25/10) de 2026")
    salvar(fig, "g01_de_onde_vieram_os_votos.png")


def g02_pesquisas(R):
    p = pd.read_csv(RES / "pesquisas_2t.csv", parse_dates=["campo_fim"])
    p = p[p.entra]
    urna = R["pesquisas"]["resultado_lula"]
    fig = figura("Nenhuma das 53 pesquisas chegou no número da urna",
                 "Lula nos votos válidos, em cada pesquisa registrada no TSE (data do fim do campo)")
    ax = fig.add_axes([0.08, 0.14, 0.86, 0.68])
    ax.scatter(p.campo_fim, p.lula_valido, s=160, color=COR["lula"], edgecolor=FUNDO, linewidth=2, zorder=3)
    ax.axhline(urna, color=COR["lula"], lw=3, ls="--")
    ax.text(p.campo_fim.min(), urna + 0.15, f"urna: Lula {br(urna, 2)}%", fontsize=24, color=COR["lula"], weight="bold")
    ax.axhline(50, color=TINTA2, lw=2)
    ax.text(p.campo_fim.min(), 50.1, "50%: acima disso, a pesquisa dava Lula", fontsize=20, color=TINTA2)
    ax.set_ylim(44.5, 53)
    ax.set_ylabel("Lula nos válidos (%)")
    ax.grid(axis="y", color=GRADE)
    s = R["pesquisas"]["todas"]
    ax.text(p.campo_fim.max(), 45.0, f"{s['deram_flavio']} davam Flávio · {s['deram_lula']} davam Lula · {s['empate']} empate",
            ha="right", fontsize=22, color=TINTA)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d/%m"))
    rodape(fig, "pesquisas registradas no TSE, conferidas no registro e numa segunda fonte; TSE (resultado)")
    salvar(fig, "g02_pesquisas_contra_a_urna.png")


def g03_ultima_de_cada(R):
    rk = pd.DataFrame(R["pesquisas"]["ranking_ultimas"]).sort_values("lula_valido")
    urna = R["pesquisas"]["resultado_lula"]
    fig = figura("A última pesquisa de cada instituto, contra a urna",
                 f"Lula nos válidos; a urna deu {br(urna, 2)}%. A distância é o erro de cada um")
    ax = fig.add_axes([0.2, 0.12, 0.74, 0.72])
    y = np.arange(len(rk))
    ax.barh(y, rk.lula_valido - 44, left=44, height=0.62, color=[COR["lula"] if v > 50 else COR["base"] for v in rk.lula_valido])
    for yi, r in zip(y, rk.itertuples()):
        ax.text(r.lula_valido + 0.08, yi, f"{br(r.lula_valido)}%  ({br(r.erro_lula)})", va="center", fontsize=17, color=TINTA)
    ax.set_yticks(y, [f"{r.instituto} ({r.campo_fim[8:10]}/{r.campo_fim[5:7]})" for r in rk.itertuples()], fontsize=17)
    ax.axvline(urna, color=COR["lula"], lw=3, ls="--")
    ax.text(urna, len(rk) - 0.2, " urna", color=COR["lula"], fontsize=20, weight="bold")
    ax.axvline(50, color=TINTA2, lw=1.5)
    ax.set_xlim(44, 53)
    ax.set_xlabel("Lula nos válidos (%)")
    rodape(fig, "pesquisas registradas no TSE (número do registro em resultados/pesquisas_2t.csv); TSE")
    salvar(fig, "g03_ultima_de_cada_instituto.png")


def g04_erro_troca_de_lado(R):
    h = pd.DataFrame(R["historico_erro_pesquisas"]["linhas"])
    s = R["pesquisas"]["ultima_de_cada_instituto"]
    h = pd.concat([h, pd.DataFrame([{"ano": 2026, "turno": 2, "erro_medio_anti_pt": -s["erro_medio"]}])])
    fig = figura("1º turno: pesquisas dão menos à direita. 2º: mais",
                 "Erro médio das últimas pesquisas no candidato contra o PT (positivo: deram mais a ele que a urna)")
    ax = fig.add_axes([0.08, 0.14, 0.86, 0.66])
    anos = [2014, 2018, 2022, 2026]
    for i, a in enumerate(anos):
        for t, desl, cor in ((1, -0.2, "#8A8A8A"), (2, 0.2, COR["flavio"])):
            v = h[(h.ano == a) & (h.turno == t)].erro_medio_anti_pt
            if len(v):
                val = float(v.iloc[0])
                ax.bar(i + desl, val, width=0.36, color=cor)
                rot = "0,0" if abs(val) < 0.05 else f"{'+' if val > 0 else ''}{br(val)}"
                ax.text(i + desl, val + (0.15 if val >= 0 else -0.15), rot, ha="center",
                        va="bottom" if val >= 0 else "top", fontsize=22, color=TINTA, weight="bold")
    ax.axhline(0, color=TINTA2, lw=1.5)
    ax.set_xticks(range(len(anos)), [str(a) for a in anos], fontsize=26)
    ax.set_ylim(-6.5, 3.5)
    ax.set_ylabel("pontos")
    ax.text(-0.45, 3.0, "■ 1º turno", color="#8A8A8A", fontsize=22, weight="bold")
    ax.text(0.35, 3.0, "■ 2º turno", color=COR["flavio"], fontsize=22, weight="bold")
    rodape(fig, "previsao-segundo-turno-2026 e presidente-primeiro-turno-2026 (2014 a 2026, 1º turno); este projeto (2026, 2º turno)")
    salvar(fig, "g04_erro_das_pesquisas_troca_de_lado.png")


def g05_regras(R):
    rg = R["regras"]
    mg = rg["minas"]
    fig = figura("As regras que sempre valiam, e 2026", "")
    linhas = [
        ("O líder do 1º turno de presidente venceu o 2º", f"{rg['presidente_lider_1t_venceu']['acertos']} de {rg['presidente_lider_1t_venceu']['vezes']} (1989 a 2022)", "quebrou: o líder perdeu"),
        ("A menor frente de um líder até 2022", f"{br(rg['presidente_lider_1t_venceu']['menor_frente_ate_2022'], 2)} pontos (2022)", f"{br(R['resultado']['variacao']['frente_1t_pontos'], 2)} pontos, a menor"),
        ("Quem venceu Minas no 1º turno venceu a eleição", f"{mg['sum_1t']} de {mg['count_1t']} (1994 a 2022)", "quebrou: deu Flávio"),
        ("Quem venceu Minas no 2º turno venceu a eleição", f"{mg['sum_2t']} de {mg['count_2t']} (2002 a 2022)", "valeu: deu Lula"),
        ("Governador: o líder do 1º turno venceu", f"{rg['governador_lider_1t_venceu']['vezes'] - rg['governador_lider_1t_venceu']['viradas']} de {rg['governador_lider_1t_venceu']['vezes']} (1994 a 2022)",
         f"{sum(1 for x in R['governador']['viradas_2t_2026'] if x['virada'])} viradas em {len(R['governador']['viradas_2t_2026'])} (RN e TO)"),
        ("Governador com frente de até 3 pontos", f"{rg['governador_frente_ate_3_pontos']['viradas']} viradas em {rg['governador_frente_ate_3_pontos']['vezes']}", "é comum virar"),
    ]
    y = 0.78
    fig.text(0.05, y + 0.06, "Regra", fontsize=22, color=TINTA2, weight="bold")
    fig.text(0.52, y + 0.06, "Histórico", fontsize=22, color=TINTA2, weight="bold")
    fig.text(0.77, y + 0.06, "2026", fontsize=22, color=TINTA2, weight="bold")
    for a, b, c in linhas:
        fig.text(0.05, y, a, fontsize=23, color=TINTA)
        fig.text(0.52, y, b, fontsize=23, color=TINTA, weight="bold")
        fig.text(0.77, y, c, fontsize=23, color=COR["lula"] if c.startswith("quebrou") else TINTA)
        y -= 0.115
    rodape(fig, "TSE, resultados de 1989 a 2026 (presidente e governador)")
    salvar(fig, "g05_regras_do_historico.png")


def g06_estados(R):
    e = pd.read_csv(RES / "estados.csv")
    e = e[e.uf != "zz"].sort_values("lula_pct_2t")
    fig = figura("O Lula subiu em todos os 27 estados; só Minas virou",
                 "Lula nos válidos no 1º turno (ponto vazio) e no 2º turno (ponto cheio)")
    ax = fig.add_axes([0.07, 0.12, 0.88, 0.7])
    y = np.arange(len(e))
    for yi, r in zip(y, e.itertuples()):
        ax.plot([r.lula_pct_1t, r.lula_pct_2t], [yi, yi], color=GRADE, lw=4, zorder=1)
        ax.scatter(r.lula_pct_1t, yi, s=120, facecolor=FUNDO, edgecolor=COR["lula"], linewidth=2.5, zorder=2)
        ax.scatter(r.lula_pct_2t, yi, s=140, color=COR["lula"], zorder=3)
        ax.text(r.lula_pct_2t + 0.8, yi, f"+{br(r.variacao_lula_pontos)}", va="center", fontsize=14, color=TINTA2)
    ax.set_yticks(y, [u.upper() for u in e.uf], fontsize=15)
    mg = list(e.uf).index("mg")
    ax.get_yticklabels()[mg].set_color(COR["lula"])
    ax.get_yticklabels()[mg].set_weight("bold")
    ax.axvline(50, color=TINTA2, lw=1.5)
    ax.set_xlabel("Lula nos válidos (%)")
    ax.grid(axis="x", color=GRADE)
    rodape(fig, "TSE, resultado oficial por UF")
    salvar(fig, "g06_estados_1t_2t.png")


def g07_abstencao(R):
    a = pd.read_csv(Path(__file__).resolve().parent.parent / "dados/copias/previsao-segundo-turno-2026/abstencao_historica.csv")
    a = a[a.ano < 2026]
    r1, r2 = R["resultado"]["t1"], R["resultado"]["t2"]
    anos = list(a.ano) + [2026]
    delta = list(a.delta_abst) + [r2["abstencao_pct"] - r1["abstencao_pct"]]
    fig = figura("A abstenção caiu do 1º para o 2º turno como nunca",
                 "Variação da abstenção entre os turnos, em pontos (positivo: mais gente faltou no 2º turno)")
    ax = fig.add_axes([0.08, 0.14, 0.86, 0.66])
    cores = [COR["base"]] * (len(anos) - 1) + [COR["lula"]]
    ax.bar(range(len(anos)), delta, color=cores, width=0.6)
    for i, d in enumerate(delta):
        ax.text(i, d + (0.1 if d >= 0 else -0.1), f"{'+' if d > 0 else ''}{br(d, 2)}", ha="center", va="bottom" if d >= 0 else "top",
                fontsize=24, weight="bold", color=TINTA)
    ax.axhline(0, color=TINTA2, lw=1.5)
    ax.set_xticks(range(len(anos)), [str(x) for x in anos], fontsize=24)
    ax.set_ylim(-2.6, 4)
    ax.set_ylabel("pontos")
    ax.text(len(anos) - 1.45, -1.6, f"{mi(-R['resultado']['variacao']['abstencao'])}\na mais votando", ha="right", fontsize=20, color=COR["lula"])
    rodape(fig, "TSE, 2002 a 2026 (presidente)")
    salvar(fig, "g07_abstencao_entre_os_turnos.png")


def g08_transferencia(R):
    t = pd.DataFrame(R["transferencia"]["tabela"])
    origens = [("cury", "Augusto Cury"), ("renan", "Renan Santos"), ("caiado", "Ronaldo Caiado"), ("branco_nulo", "Branco e nulo\nno 1º turno"), ("abstencao", "Faltou no\n1º turno")]
    destinos = [("lula", "Lula", COR["lula"]), ("flavio", "Flávio", COR["flavio"]), ("branco_nulo", "branco ou nulo", "#B0B0B0"), ("abstencao", "faltou", "#DADADA")]
    fig = figura("Para onde foram os eleitores de cada um",
                 "Estimativa por município (o voto é secreto: não é contagem). Entre parênteses, a faixa de 90%")
    ax = fig.add_axes([0.2, 0.16, 0.76, 0.64])
    for yi, (o, nome) in enumerate(origens[::-1]):
        esq = 0
        for d, dn, cor in destinos:
            r = t[(t.origem_1t == o) & (t.destino_2t == d)].iloc[0]
            ax.barh(yi, r.pct_da_origem, left=esq, color=cor, height=0.6, edgecolor=FUNDO, linewidth=2)
            if r.pct_da_origem >= 9:
                ax.text(esq + r.pct_da_origem / 2, yi, f"{br(r.pct_da_origem, 0)}%\n({br(r.pct_p5, 0)} a {br(r.pct_p95, 0)})", ha="center", va="center",
                        fontsize=15, color="white" if d in ("lula", "flavio") else TINTA)
            esq += r.pct_da_origem
    ax.set_yticks(range(len(origens)), [n for _, n in origens[::-1]], fontsize=20)
    ax.set_xlim(0, 100)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    x = 0
    for d, dn, cor in destinos:
        ax.text(x, len(origens) - 0.35, "■", color=cor, fontsize=24)
        ax.text(x + 2.2, len(origens) - 0.35, dn, color=TINTA, fontsize=20, weight="bold")
        x += 22
    rodape(fig, "TSE, resultado por município nos dois turnos; modelo de transição com restrição por região (resultados/transferencia_de_votos.csv)")
    salvar(fig, "g08_para_onde_foram_os_votos.png")


def g09_governador(R):
    g = pd.read_csv(RES / "governador_e_presidente.csv").sort_values("uf")
    fig = figura("Governador eleito e presidente no mesmo estado",
                 f"Em {R['governador']['mesmo_lado']} de 27 estados, o governador eleito é da coligação do lado que venceu para presidente ali")
    cores = {"Lula": COR["lula"], "Flávio": COR["flavio"], "nenhum": "#B0B0B0", "os dois": "#B0B0B0"}
    for i, r in enumerate(g.itertuples()):
        col, lin = i % 9, i // 9
        x0, y0 = 0.05 + col * 0.1, 0.62 - lin * 0.24
        fig.patches.append(plt.Rectangle((x0, y0), 0.045, 0.17, transform=fig.transFigure, color=cores[r.lado_da_coligacao]))
        fig.patches.append(plt.Rectangle((x0 + 0.047, y0), 0.045, 0.17, transform=fig.transFigure, color=cores[r.presidente_venceu_no_estado]))
        fig.text(x0 + 0.046, y0 + 0.19, r.uf.upper(), ha="center", fontsize=22, weight="bold", color=TINTA)
        fig.text(x0 + 0.0225, y0 + 0.085, "gov.", ha="center", va="center", fontsize=14, color="white")
        fig.text(x0 + 0.0695, y0 + 0.085, "pres.", ha="center", va="center", fontsize=14, color="white")
    fig.text(0.05, 0.1, "■ coligação com o PT / Lula venceu", color=COR["lula"], fontsize=20, weight="bold")
    fig.text(0.37, 0.1, "■ coligação com o PL / Flávio venceu", color=COR["flavio"], fontsize=20, weight="bold")
    fig.text(0.72, 0.1, "■ sem PT nem PL na coligação", color="#8A8A8A", fontsize=20, weight="bold")
    rodape(fig, "TSE, governador (1º e 2º turno) e presidente (2º turno) de 2026")
    salvar(fig, "g09_governador_e_presidente.png")


def g10_probabilidade(R):
    pr = R["probabilidade"]
    lei = sorted(pr["leituras"].items(), key=lambda kv: kv[1])
    fig = figura("Antes da votação, qual era a chance de o Lula vencer?",
                 "Cada régua dá um número. Só a dos governadores em disputa apertada passava de 50%")
    ax = fig.add_axes([0.36, 0.14, 0.58, 0.68])
    y = np.arange(len(lei))
    ax.barh(y, [100 * v for _, v in lei], color=COR["base"], height=0.6)
    for yi, (k, v) in zip(y, lei):
        ax.text(100 * v + 1, yi, f"{br(100 * v, 0)}%" + (f"  (1 em {br(1 / v, 1)})" if v < 0.5 else ""), va="center", fontsize=22, color=TINTA)
    ax.set_yticks(y, [k for k, _ in lei], fontsize=19)
    ax.axvline(50, color=TINTA2, lw=1.5)
    ax.set_xlim(0, 80)
    ax.set_xlabel("chance do Lula (%)")
    rodape(fig, "pesquisas registradas no TSE e o erro histórico de 2014 a 2022; TSE (1989 a 2022); Polymarket (preço da véspera)")
    salvar(fig, "g10_probabilidade_antes_da_eleicao.png")


def g11_teste_votos_sem_origem(R):
    te = R["testes_das_lentes"]
    v = R["resultado"]["variacao"]
    fig = figura("Votos sem origem visível no município",
                 "Ganho acima de (votos dos outros + queda da abstenção + queda de branco e nulo), somado no país")
    ax = fig.add_axes([0.08, 0.14, 0.86, 0.66])
    itens = [("Lula", te["t1_lula"]["votos_acima_do_livre"], te["t1_lula"]["municipios"], COR["lula"]),
             ("Flávio", te["t1_flavio"]["votos_acima_do_livre"], te["t1_flavio"]["municipios"], COR["flavio"]),
             ("Frente do Lula\nna eleição", v["frente_2t_lula"], None, COR["base"])]
    for i, (n, val, mun, cor) in enumerate(itens):
        ax.bar(i, val, color=cor, width=0.6)
        lab = f"{br(val, 0)} votos" + (f"\nem {mun} municípios" if mun is not None else "")
        ax.text(i, val * 1.4 + 3000, lab, ha="center", fontsize=24, weight="bold", color=TINTA)
    ax.set_yscale("symlog", linthresh=1000)
    ax.set_xticks(range(3), [n for n, *_ in itens], fontsize=24)
    ax.set_ylim(0, 3e7)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.text(1, 3e5, f"o excesso do Lula é {br(100 * itens[0][1] / v['frente_2t_lula'], 2)}% da frente", ha="center", fontsize=22, color=TINTA2)
    rodape(fig, "TSE, resultado por município nos dois turnos (escala logarítmica)")
    salvar(fig, "g11_votos_sem_origem.png")


def main() -> None:
    R = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))
    for f in (g01_de_onde_vieram, g02_pesquisas, g03_ultima_de_cada, g04_erro_troca_de_lado, g05_regras, g06_estados,
              g07_abstencao, g08_transferencia, g09_governador, g10_probabilidade, g11_teste_votos_sem_origem):
        f(R)


if __name__ == "__main__":
    main()
