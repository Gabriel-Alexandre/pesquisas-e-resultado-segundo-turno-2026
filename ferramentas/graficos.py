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
    ax = fig.add_axes([0.08, 0.19, 0.86, 0.61])
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
    p2 = R["probabilidade_v2"]
    pil, W = p2["pilares"], p2["pesos"]
    fig = figura(f"Antes da votação, a chance do Lula era de {br(100 * p2['combinada'], 0)}%",
                 "Três pilares, com os pesos da projeção do vídeo 14 (pesquisas 60%, histórico 25%, crescimento 15%)")
    ax = fig.add_axes([0.34, 0.16, 0.6, 0.64])
    itens = [("Pesquisas e o erro de\n80 segundos turnos (60%)", pil["pesquisas"]),
             ("Viradas com frente\nparecida (25%)", pil["historico"]),
             ("Votos livres como em\n2002 a 2022 (15%)", pil["crescimento"]),
             ("Junto", p2["combinada"]), ("Polymarket na véspera\n(conferência)", p2["mercado"])]
    y = np.arange(len(itens))[::-1]
    cores = [COR["base"], COR["base"], COR["base"], COR["lula"], "#B0B0B0"]
    ax.barh(y, [100 * v for _, v in itens], color=cores, height=0.6)
    for yi, (k, v) in zip(y, itens):
        ax.text(100 * v + 1, yi, f"{br(100 * v, 0)}%  (1 em {br(1 / v, 1)})", va="center", fontsize=22, color=TINTA)
    ax.set_yticks(y, [k for k, _ in itens], fontsize=19)
    ax.axvline(50, color=TINTA2, lw=1.5)
    ax.set_xlim(0, 75)
    ax.set_xlabel("chance do Lula (%)")
    rodape(fig, "pesquisas registradas e o erro histórico (Brasil e outros países); TSE, 1994 a 2022; Polymarket")
    salvar(fig, "g10_probabilidade_antes_da_eleicao.png")


def g16_erro_pesquisas_historico(R):
    e = pd.read_csv(RES / "erro_media_pesquisas_runoffs.csv")
    U, v = R["pesquisas"]["ultima_de_cada_instituto"], R["resultado"]["variacao"]
    erro26 = 2 * (50 - U["media_lula"]) + v["frente_2t_pontos"]
    fig = figura("As pesquisas já erraram tanto assim?",
                 "Quanto a média das pesquisas superestimou o líder em cada 2º turno presidencial (pontos na frente)")
    ax = fig.add_axes([0.08, 0.16, 0.86, 0.64])
    e = e.sort_values("superestimou_lider").reset_index(drop=True)
    cores = [COR["flavio"] if not ok else ("#8A8A8A" if p != "Brasil" else COR["base"]) for p, ok in zip(e.pais, e.lider_das_pesquisas_venceu)]
    ax.bar(range(len(e)), e.superestimou_lider, color=cores, width=0.75)
    pos = int((e.superestimou_lider < erro26).sum())
    ax.bar(pos - 0.5, erro26, color=COR["lula"], width=0.9)
    ax.text(pos - 2.5, erro26 + 3.2, "Brasil\n2026", ha="center", fontsize=18, weight="bold", color=COR["lula"])
    for i, r in e.iterrows():
        if r.pais == "Brasil" or abs(r.superestimou_lider) > 9:
            ax.text(i, r.superestimou_lider + (0.4 if r.superestimou_lider >= 0 else -0.9), f"{r.pais[:3]} {str(r.ano)[2:]}", ha="center", fontsize=12, rotation=90, color=TINTA2)
    ax.axhline(0, color=TINTA2, lw=1.2)
    ax.set_xticks([])
    ax.set_ylabel("pontos")
    ax.text(0, 16, "■ o líder das pesquisas perdeu", color=COR["flavio"], fontsize=20, weight="bold")
    ax.text(0, 13.5, "■ Brasil, o líder venceu", color=COR["base"], fontsize=20, weight="bold")
    ax.text(0, 11, "■ outros países, o líder venceu", color="#8A8A8A", fontsize=20, weight="bold")
    rodape(fig, "pesquisas de cada eleição na Wikipédia e nos PDFs do Datafolha, conferidas número a número (resultados/erro_media_pesquisas_runoffs.csv)")
    salvar(fig, "g16_erro_das_pesquisas_no_mundo.png")


def g17_soma_ingenua(R):
    si = R["probabilidade_v2"]["soma_ingenua"]
    c = si["componentes"]
    fig = figura("O erro de multiplicar as coincidências",
                 "Quatro fatos que parecem improváveis, mas são um só: o Lula vencer uma disputa apertada")
    itens = [("As pesquisas erram", c["pesquisas"]), ("O líder do 1º turno perde", c["historico"]),
             ("A regra de Minas quebra", c["minas"]), ("O favorito do mercado perde", c["mercado"])]
    y0 = 0.72
    for k, p in itens:
        fig.text(0.07, y0, k, fontsize=26, color=TINTA)
        fig.text(0.5, y0, f"{br(100 * p, 0)}%", fontsize=26, color=TINTA, weight="bold")
        y0 -= 0.09
    fig.text(0.07, 0.30, f"Multiplicando: 1 em {br(si['um_em_ingenuo'], 0)}", fontsize=34, color=TINTA2)
    fig.text(0.07, 0.30 - 0.004, "_" * 34, fontsize=34, color=TINTA2)
    fig.text(0.07, 0.18, f"O certo: 1 em {br(si['um_em_correta'], 1)} (a chance do próprio fato)", fontsize=34, color=COR["lula"], weight="bold")
    fig.text(0.6, 0.62, "Se o Lula vence,\nas quatro acontecem\njuntas, sempre.", fontsize=30, color=TINTA, weight="bold")
    rodape(fig, "este projeto (resultados/RESUMO.json, probabilidade_v2.soma_ingenua)")
    salvar(fig, "g17_o_erro_de_multiplicar.png")


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


def g12_curva_da_apuracao(R):
    c = R["alegacoes"]["curva"]
    fig = figura("A virada na contagem também aconteceu em 2022",
                 "Frente do candidato contra o PT ao longo da apuração do 2º turno, pela porcentagem de seções apuradas")
    ax = fig.add_axes([0.08, 0.14, 0.86, 0.68])
    a = pd.DataFrame(c["2022"]["pontos"])
    b = pd.DataFrame(c["2026"]["pontos"])
    ax.plot(a.pct_secoes, a.frente_anti, color=COR["base"], lw=4, marker="o", ms=9)
    ax.plot(b.pct_secoes, b.frente_anti, color=COR["flavio"], lw=4, marker="o", ms=9)
    ax.axhline(0, color=TINTA2, lw=1.5)
    ax.text(12, 4.3, "2022: Bolsonaro na frente até 67% das seções", color=COR["base"], fontsize=22, weight="bold")
    ax.text(30, 1.4, f"2026: Flávio na frente até {br(c['2026']['pt_passa_com_pct'], 0)}% das seções", color=COR["flavio"], fontsize=22, weight="bold")
    ax.set_xlabel("seções apuradas (%)")
    ax.set_ylabel("frente do candidato contra o PT (pontos)")
    ax.set_xlim(0, 101)
    ax.grid(axis="y", color=GRADE)
    rodape(fig, "TSE, versões do resultado divulgadas na noite (2026, 346 versões gravadas; 2022, pela hora de recebimento dos boletins)")
    salvar(fig, "g12_curva_da_apuracao_2022_e_2026.png")


def g13_votos_sem_origem_por_ano(R):
    t = pd.DataFrame(R["historia"]["testes"])
    fig = figura("Votos sem origem visível no município, em cada 2º turno",
                 "Ganho de um candidato acima de tudo o que estava livre no município (outros + abstenção + branco e nulo)")
    ax = fig.add_axes([0.08, 0.14, 0.86, 0.66])
    x = np.arange(len(t))
    ax.bar(x - 0.2, t.pt_votos_sem_origem, width=0.38, color=COR["lula"])
    ax.bar(x + 0.2, t.anti_votos_sem_origem, width=0.38, color=COR["flavio"])
    for i, r in enumerate(t.itertuples()):
        ax.text(i - 0.2, max(r.pt_votos_sem_origem, 1) * 1.3, n0(r.pt_votos_sem_origem), ha="center", fontsize=16, color=TINTA)
        ax.text(i + 0.2, max(r.anti_votos_sem_origem, 1) * 1.3, n0(r.anti_votos_sem_origem), ha="center", fontsize=16, color=TINTA)
    ax.set_yscale("symlog", linthresh=100)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xticks(x, [str(a) for a in t.ano], fontsize=24)
    ax.text(0, 4e6, "■ PT", color=COR["lula"], fontsize=22, weight="bold")
    ax.text(0.8, 4e6, "■ adversário", color=COR["flavio"], fontsize=22, weight="bold")
    ax.set_ylim(0, 1e7)
    rodape(fig, "TSE, resultado por município, 2002 a 2026 (escala logarítmica)")
    salvar(fig, "g13_votos_sem_origem_por_ano.png")


def g14_crescimento(R):
    c = pd.DataFrame(R["probabilidade_v2"]["crescimento"]["por_padrao"])
    urna = R["resultado"]["t2"]["lula_pct"]
    fig = figura("Se os votos livres fossem como num 2º turno passado",
                 "O 1º turno de 2026, com os votos dos outros, de branco e nulo e da abstenção indo como foram em cada ano")
    ax = fig.add_axes([0.08, 0.14, 0.86, 0.66])
    x = np.arange(len(c))
    ax.bar(x, c.lula_pct, color=[COR["lula"] if v > 50 else COR["base"] for v in c.lula_pct], width=0.6)
    for i, v in enumerate(c.lula_pct):
        ax.text(i, v + 0.15, f"{br(v)}%", ha="center", fontsize=24, weight="bold", color=TINTA)
    ax.axhline(50, color=TINTA2, lw=1.5)
    ax.axhline(urna, color=COR["lula"], lw=3, ls="--")
    ax.text(-0.4, urna + 0.15, f"urna: {br(urna, 2)}%", color=COR["lula"], fontsize=22, weight="bold")
    ax.set_xticks(x, [f"padrão de {a}" for a in c.padrao_de], fontsize=20)
    ax.set_ylim(45, 53)
    ax.set_ylabel("Lula nos válidos (%)")
    rodape(fig, "TSE, resultado por município 2002 a 2026; modelo de transição por região (resultados/transferencia_por_ano.csv)")
    salvar(fig, "g14_crescimento_pelos_padroes_passados.png")


def g15_transferencia_por_ano(R):
    t = pd.DataFrame(R["historia"]["transferencia"])
    t = t[t.origem_1t == "outros"]
    fig = figura("Para onde foram os votos dos outros candidatos, em cada 2º turno",
                 "Estimativa por município (o voto é secreto); parte dos eleitores dos outros que foi para cada lado")
    ax = fig.add_axes([0.08, 0.14, 0.86, 0.66])
    x = np.arange(len(t))
    ax.bar(x - 0.2, t.para_pt_pct, width=0.38, color=COR["lula"])
    ax.bar(x + 0.2, t.para_adversario_pct, width=0.38, color=COR["flavio"])
    for i, r in enumerate(t.itertuples()):
        ax.text(i - 0.2, r.para_pt_pct + 1, f"{br(r.para_pt_pct, 0)}%", ha="center", fontsize=18, color=TINTA)
        ax.text(i + 0.2, r.para_adversario_pct + 1, f"{br(r.para_adversario_pct, 0)}%", ha="center", fontsize=18, color=TINTA)
    ax.set_xticks(x, [str(a) for a in t.ano], fontsize=24)
    ax.set_ylim(0, 70)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.text(-0.4, 65, "■ para o PT", color=COR["lula"], fontsize=22, weight="bold")
    ax.text(1.2, 65, "■ para o adversário", color=COR["flavio"], fontsize=22, weight="bold")
    rodape(fig, "TSE, resultado por município, 2002 a 2026; modelo de transição por região")
    salvar(fig, "g15_outros_candidatos_por_ano.png")


def g18_de_onde_vieram_os_10_milhoes(R):
    d = R["de_onde"]
    a = d["ajustes_2026"]["por região"]
    gl, gf = d["ganho_lula_municipios"], d["ganho_flavio_municipios"]
    O, N = d["outros_livres"], d["novos_livres"]
    lula = [a["dos_outros"], a["dos_novos"], a["da_troca"]]
    flavio = [O - a["dos_outros"], N - a["dos_novos"], -a["da_troca"]]
    fig = figura("De onde vieram os votos a mais do Lula",
                 "Ganho do 1º para o 2º turno, separado pela origem (municípios do Brasil; ajuste por região)")
    ax = fig.add_axes([0.2, 0.16, 0.74, 0.62])
    cores = [OUTROS, "#8A8A8A", COR["flavio"]]
    nomes = ["eleitores dos outros candidatos", "quem não tinha votado em ninguém", "eleitores do Flávio que mudaram"]
    for yi, (vals, quem) in enumerate([(flavio, "Flávio"), (lula, "Lula")]):
        esq = 0
        for v, c, nome in zip(vals, cores, nomes):
            if v <= 0:
                continue
            ax.barh(yi, v / 1e6, left=esq, color=c, height=0.55, edgecolor=FUNDO, linewidth=3)
            if v > 4e5:
                ax.text(esq + v / 2e6, yi, br(v / 1e6, 1), ha="center", va="center", fontsize=24, color="white", weight="bold")
            esq += v / 1e6
        total = gl if quem == "Lula" else gf
        ax.text(esq + 0.15, yi, f"+{br(total / 1e6, 2)} mi", va="center", fontsize=26, weight="bold", color=TINTA)
    ax.set_yticks([0, 1], ["Flávio", "Lula"], fontsize=28)
    ax.set_xlim(0, 12)
    ax.set_xlabel("milhões de votos")
    for i, (c, nome) in enumerate(zip(cores, nomes)):
        fig.text(0.2 + i * 0.26, 0.83, "■", color=c, fontsize=24)
        fig.text(0.215 + i * 0.26, 0.83, nome, color=TINTA, fontsize=18)
    rodape(fig, "TSE, resultado por município nos dois turnos; ajuste com restrição por região (resultados/de_onde_vieram_por_ano.csv)")
    salvar(fig, "g18_de_onde_vieram_os_votos_do_lula.png")


def g19_parte_dos_livres_por_ano(R):
    d = pd.DataFrame(R["de_onde"]["por_ano"])
    fig = figura("Quanto dos votos livres o PT levou em cada 2º turno",
                 "Ganho do PT do 1º para o 2º turno, como parte dos votos livres (outros, abstenção, branco e nulo)")
    ax = fig.add_axes([0.08, 0.14, 0.86, 0.66])
    x = np.arange(len(d))
    ax.bar(x, d.parte_do_pt_nos_livres_pct, color=[COR["lula"] if a == 2026 else COR["base"] for a in d.ano], width=0.6)
    for i, r in enumerate(d.itertuples()):
        ax.text(i, r.parte_do_pt_nos_livres_pct + 2, f"{br(r.parte_do_pt_nos_livres_pct, 0)}%", ha="center", fontsize=24, weight="bold", color=TINTA)
    ax.axhline(50, color=TINTA2, lw=1.5)
    ax.set_xticks(x, [str(a) for a in d.ano], fontsize=24)
    ax.set_ylim(0, 140)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.text(1.45, 118, "2006: mais de 100%, porque\no Alckmin perdeu votos", ha="left", fontsize=18, color=TINTA2)
    rodape(fig, "TSE, resultado por município, 2002 a 2026")
    salvar(fig, "g19_parte_do_pt_nos_votos_livres.png")


def g20_por_renda(R):
    g = pd.DataFrame(R["porque"]["renda"]["grupos"])
    fig = figura("Onde cada um ganhou votos, pela renda do município",
                 "Votos ganhos do 1º para o 2º turno, a cada 100 eleitores (municípios em 5 grupos de mesmo número)")
    ax = fig.add_axes([0.08, 0.34, 0.86, 0.46])
    x = np.arange(len(g))
    ax.bar(x - 0.2, g.lula_ganhou_por_100, width=0.38, color=COR["lula"])
    ax.bar(x + 0.2, g.flavio_ganhou_por_100, width=0.38, color=COR["flavio"])
    for i, r in g.iterrows():
        ax.text(i - 0.2, r.lula_ganhou_por_100 + 0.15, br(r.lula_ganhou_por_100), ha="center", fontsize=20, weight="bold", color=TINTA)
        ax.text(i + 0.2, max(r.flavio_ganhou_por_100, 0) + 0.15, br(r.flavio_ganhou_por_100), ha="center", fontsize=20, weight="bold", color=TINTA)
        ax.text(i, -1.0, f"abstenção {('caiu ' + br(r.abstencao_caiu_pontos) + ' pt') if r.abstencao_caiu_pontos > 0.05 else 'parada'}\nvirada: {br(r.parte_da_virada_pct, 0)}% (eleitorado {br(r.parte_do_eleitorado_pct, 0)}%)",
                ha="center", va="top", fontsize=14, color=TINTA2)
    ax.axhline(0, color=TINTA2, lw=1.2)
    ax.set_xticks(x, [f"{r.grupo}\nrenda de R$ {br(r.renda_media, 0)}" for r in g.itertuples()], fontsize=16)
    ax.tick_params(axis="x", pad=70)
    ax.set_ylim(-0.5, 8.5)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.text(-0.4, 8.0, "■ Lula", color=COR["lula"], fontsize=22, weight="bold")
    ax.text(0.4, 8.0, "■ Flávio", color=COR["flavio"], fontsize=22, weight="bold")
    rodape(fig, "TSE, resultado por município nos dois turnos; IBGE, Censo 2022, rendimento domiciliar per capita (tabela 10295)")
    salvar(fig, "g20_ganho_por_renda_do_municipio.png")


def g21_eleitor_da_direita(R):
    d = pd.DataFrame(R["porque"]["direita"]["direita (Renan, Caiado e Zema)"])
    fig = figura("Onde a direita era mais forte, o Flávio levou mais",
                 "Parte dos votos livres que cada um levou, pela força de Renan, Caiado e Zema no 1º turno")
    ax = fig.add_axes([0.08, 0.16, 0.86, 0.62])
    x = np.arange(len(d))
    ax.bar(x, d.lula_levou_dos_livres_pct, color=COR["lula"], width=0.6)
    ax.bar(x, d.flavio_levou_dos_livres_pct, bottom=d.lula_levou_dos_livres_pct, color=COR["flavio"], width=0.6)
    for i, r in d.iterrows():
        ax.text(i, r.lula_levou_dos_livres_pct / 2, f"{br(r.lula_levou_dos_livres_pct, 0)}%", ha="center", va="center", fontsize=22, color="white", weight="bold")
        if r.flavio_levou_dos_livres_pct > 5:
            ax.text(i, r.lula_levou_dos_livres_pct + r.flavio_levou_dos_livres_pct / 2, f"{br(r.flavio_levou_dos_livres_pct, 0)}%", ha="center", va="center", fontsize=22, color="white", weight="bold")
    ax.set_xticks(x, [f"{r.grupo}\n(os três: {br(r.forca_media)}%)" for r in d.itertuples()], fontsize=17)
    ax.set_ylim(0, 108)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    rodape(fig, "TSE, resultado por município nos dois turnos (municípios em 5 grupos pela soma de Renan, Caiado e Zema nos válidos do 1º turno)")
    salvar(fig, "g21_eleitor_da_direita.png")


def g22_tendencia_das_pesquisas(R):
    t = pd.DataFrame(R["porque"]["tendencia"])
    urna26 = R["resultado"]["t2"]["lula_pct"]
    fig = figura("As pesquisas andavam para o PT, devagar em 2026",
                 "Inclinação das pesquisas do 2º turno ao longo das últimas 3 semanas, em pontos por semana para o PT")
    ax = fig.add_axes([0.08, 0.30, 0.86, 0.50])
    x = np.arange(len(t))
    ax.bar(x, t.inclinacao_por_semana, color=[COR["lula"] if a == 2026 else COR["base"] for a in t.ano], width=0.6)
    for i, r in t.iterrows():
        urna = r.urna if pd.notna(r.urna) else urna26
        ax.text(i, r.inclinacao_por_semana + 0.08, f"+{br(r.inclinacao_por_semana)}", ha="center", fontsize=26, weight="bold", color=TINTA)
        ax.text(i, -0.15, f"a reta dava {br(r.reta_no_dia)}%\na urna deu {br(urna)}%", ha="center", va="top", fontsize=17, color=TINTA2)
    ax.set_xticks(x, [str(a) for a in t.ano], fontsize=26)
    ax.tick_params(axis="x", pad=60)
    ax.set_ylim(0, 3.5)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    rodape(fig, "pesquisas registradas no TSE (Pindograma, 2014 a 2022; este projeto, 2026), com o efeito de cada instituto descontado")
    salvar(fig, "g22_tendencia_das_pesquisas.png")


def g23_votos_livres_e_quem_saiu(R):
    c = pd.DataFrame(R["normalidade"]["campo"])
    fig = figura("Para quem foram os votos livres, conforme quem saiu",
                 "Parte dos votos livres que o PT levou no 2º turno, e o que os candidatos eliminados fizeram")
    ax = fig.add_axes([0.08, 0.34, 0.86, 0.46])
    x = np.arange(len(c))
    ax.bar(x, c.parte_do_pt_nos_livres_pct.clip(upper=100), color=[COR["lula"] if a == 2026 else COR["base"] for a in c.ano], width=0.6)
    for i, r in c.iterrows():
        v = r.parte_do_pt_nos_livres_pct
        ax.text(i, min(v, 100) + 3, f"{br(v, 0)}%" + (" *" if v > 100 else ""), ha="center", fontsize=26, weight="bold", color=TINTA)
        ax.text(i, -6, f"apoio ao PT: {br(r.apoiou_pt_pct, 0)}%\napoio ao rival: {br(r.apoiou_adversario_pct, 0)}%",
                ha="center", va="top", fontsize=16, color=TINTA2)
    ax.axhline(50, color=TINTA2, lw=1.2, ls=(0, (4, 4)))
    ax.set_xticks(x, [str(a) for a in c.ano], fontsize=26)
    ax.tick_params(axis="x", pad=80)
    ax.set_ylim(0, 112)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    fig.text(0.08, 0.115, "Embaixo: dos votos dos candidatos que saíram, a parte cujo candidato declarou apoio a cada lado no 2º turno", fontsize=16, color=TINTA2)
    fig.text(0.08, 0.81, "* 2006: o PT levou mais do que estava livre, porque o Alckmin perdeu votos do 1º para o 2º turno", fontsize=16, color=TINTA2)
    rodape(fig, "TSE, resultado por município, 2002 a 2026; posição de cada candidato no 2º turno com link em dados/agentes/apoios_segundo_turno.csv")
    salvar(fig, "g23_votos_livres_e_quem_saiu.png")


def g24_comparecimento_por_ano(R):
    c = pd.DataFrame(R["normalidade"]["comparecimento"])
    fig = figura("O comparecimento do 1º para o 2º turno",
                 "Quanto o comparecimento mudou no país, em pontos, e em quantos municípios ele subiu")
    ax = fig.add_axes([0.08, 0.30, 0.86, 0.50])
    x = np.arange(len(c))
    ax.bar(x, c.comparecimento_variou_pontos, color=[COR["lula"] if a == 2026 else COR["base"] for a in c.ano], width=0.6)
    for i, r in c.iterrows():
        v = r.comparecimento_variou_pontos
        ax.text(i, v + (0.12 if v >= 0 else -0.12), ("+" if v > 0 else "") + br(v), ha="center", va="bottom" if v >= 0 else "top",
                fontsize=26, weight="bold", color=TINTA)
        ax.text(i, -4.3, f"subiu em\n{br(r.municipios_comparecimento_subiu_pct, 0)}% dos\nmunicípios", ha="center", va="top", fontsize=16, color=TINTA2)
    ax.axhline(0, color=TINTA2, lw=1.2)
    ax.set_xticks(x, [str(a) for a in c.ano], fontsize=26)
    ax.tick_params(axis="x", pad=100)
    ax.set_ylim(-4.2, 2.8)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    rodape(fig, "TSE, comparecimento por município nos dois turnos, 2002 a 2026")
    salvar(fig, "g24_comparecimento_por_ano.png")


def g25_a_chance_refeita(R):
    ch = R["normalidade"]["chance"]
    v = ch["variantes"]
    nomes = {"rodada 2 (média com pesos, sem as correções)": "a conta anterior",
             "média com pesos, com as correções 1 e 2": "a mesma média, corrigida",
             "Bayes: o histórico como ponto de partida e as pesquisas como indício (central)": "histórico + pesquisas (central)",
             "os três pilares como indícios independentes (ponta de baixo)": "os 3 independentes (ponta de baixo)",
             "mercado (Polymarket, véspera)": "o mercado na véspera"}
    itens = [(nomes[k], v[k]) for k in nomes]
    fig = figura("A chance do Lula antes da votação, refeita",
                 "Chance de o Lula vencer, calculada como se fosse a véspera, por cada jeito de juntar o que se sabia")
    ax = fig.add_axes([0.36, 0.14, 0.58, 0.66])
    y = np.arange(len(itens))[::-1]
    cores = [COR["base"], COR["base"], COR["lula"], COR["base"], OUTROS]
    for yi, (nome, p), c in zip(y, itens, cores):
        ax.barh(yi, 100 * p, color=c, height=0.6)
        ax.text(100 * p + 1, yi, f"{br(100 * p, 0)}%  (1 em {br(1 / p, 0 if 1 / p >= 10 else 1)})", va="center", fontsize=24, weight="bold", color=TINTA)
    ax.set_yticks(y, [i[0] for i in itens], fontsize=22)
    ax.set_xlim(0, 60)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.axvline(50, color=TINTA2, lw=1.2, ls=(0, (4, 4)))
    ax.text(50, len(itens) - 0.35, "50%", ha="center", fontsize=18, color=TINTA2)
    rodape(fig, "pesquisas registradas no TSE; 2º turnos no Brasil e em outros países; Polymarket (série do projeto do vídeo 16)")
    salvar(fig, "g25_a_chance_refeita.png")


def n0(x: float) -> str:
    return br(x, 0)


def main() -> None:
    R = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))
    for f in (g01_de_onde_vieram, g02_pesquisas, g03_ultima_de_cada, g04_erro_troca_de_lado, g05_regras, g06_estados,
              g07_abstencao, g08_transferencia, g09_governador, g10_probabilidade, g11_teste_votos_sem_origem,
              g12_curva_da_apuracao, g13_votos_sem_origem_por_ano, g14_crescimento, g15_transferencia_por_ano):
        f(R)
    for f in EXTRAS:
        f(R)


EXTRAS: list = [g16_erro_pesquisas_historico, g17_soma_ingenua, g18_de_onde_vieram_os_10_milhoes, g19_parte_dos_livres_por_ano, g20_por_renda, g21_eleitor_da_direita, g22_tendencia_das_pesquisas,
                g23_votos_livres_e_quem_saiu, g24_comparecimento_por_ano, g25_a_chance_refeita]


if __name__ == "__main__":
    main()
