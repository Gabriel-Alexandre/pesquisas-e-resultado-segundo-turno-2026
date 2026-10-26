"""Escreve RELATORIO.md, RESUMO_SIMPLES.md e docs/LEITURA_DA_IA.md a partir de resultados/RESUMO.json e das tabelas.
Nenhum número é escrito à mão: todos saem daqui. Rodada 2.
Uso: python ferramentas/gerar-relatorio.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "resultados"
R = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))
NOME_PAIS = {"Franca": "França", "Polonia": "Polônia", "Romenia": "Romênia", "Eslovaquia": "Eslováquia", "Colombia": "Colômbia",
             "Bolivia": "Bolívia", "Equador": "Equador", "Uruguai": "Uruguai", "Lithuania": "Lituânia", "Czech Republic": "República Tcheca",
             "Chile": "Chile", "Cyprus": "Chipre", "North Macedonia": "Macedônia do Norte", "Ukraine": "Ucrânia", "Montenegro": "Montenegro",
             "Ecuador": "Equador", "Costa Rica": "Costa Rica", "Poland": "Polônia", "Croatia": "Croácia", "Romania": "Romênia",
             "Finland": "Finlândia", "Bulgaria": "Bulgária", "France": "França", "Guatemala": "Guatemala", "Argentina": "Argentina",
             "Serbia": "Sérvia", "Slovakia": "Eslováquia", "Slovenia": "Eslovênia", "Peru": "Peru", "Austria": "Áustria",
             "Moldova": "Moldávia", "Uruguay": "Uruguai", "El Salvador": "El Salvador", "Haiti": "Haiti", "Portugal": "Portugal",
             "Dominican Republic": "República Dominicana", "Bolivia ": "Bolívia"}


def br(x: float, c: int = 1) -> str:
    return f"{x:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def n(x: float) -> str:
    return br(x, 0)


def mi(x: float) -> str:
    return f"{br(x / 1e6, 2)} milhões"


def pct(p: float, c: int = 0) -> str:
    return f"{br(100 * p, c)}%"


def um_em(p: float) -> str:
    return f"1 em {br(1 / p, 1)}"


def sinal(x: float, c: int = 1) -> str:
    return "0,0" if abs(x) < 0.05 else f"{'+' if x > 0 else ''}{br(x, c)}"


def pais(x: str) -> str:
    return NOME_PAIS.get(x, x)


r, v = R["resultado"], R["resultado"]["variacao"]
t1, t2 = r["t1"], r["t2"]
P, U = R["pesquisas"], R["pesquisas"]["ultima_de_cada_instituto"]
reg = R["regras"]
p1 = R["probabilidade"]
p2 = R["probabilidade_v2"]
PQ, HS, CR = p2["pesquisas"], p2["historico"], p2["crescimento"]
pil = p2["pilares"]
W = p2["pesos"]
te = R["testes_das_lentes"]
mun, est, gov = R["municipios"], R["estados"], R["governador"]
hist = pd.DataFrame(R["historia"]["testes"])
trano = pd.DataFrame(R["historia"]["transferencia"])
novos = pd.DataFrame(R["historia"]["eleitores_novos"])
ext = pd.DataFrame(R["historia"]["exterior"])
ale = R["alegacoes"]
tr = pd.DataFrame(R["transferencia"]["tabela"])
tp = R.get("transferencia_pesquisas")
val = list(csv.reader(open(RES / "validacao_independente.csv", encoding="utf-8")))[1:]
val_ok = sum(1 for x in val if x[3] == "True")
viradas_gov = [x for x in gov["viradas_2t_2026"] if x["virada"]]
frente = v["frente_2t_lula"]
erro_2026 = 2 * (50 - U["media_lula"]) + v["frente_2t_pontos"]  # quanto a média superestimou a frente do Flávio
em = pd.read_csv(RES / "erro_media_pesquisas_runoffs.csv") if (RES / "erro_media_pesquisas_runoffs.csv").exists() else pd.DataFrame()
gov_hist = pd.read_csv(RES / "erro_media_pesquisas_todos.csv")
gov_hist = gov_hist[gov_hist.fonte == "Brasil governador"]
h26 = hist[hist.ano == 2026].iloc[0]
casos = pd.read_csv(RES / "viradas_casos.csv")
tem_mundo = (casos.grupo == "presidente, outros países").any()

# ------------------------------------------------------------------ tabelas
tab_pilares = "\n".join([
    f"| **Pesquisas** | {pct(W['pesquisas'])} | a frente do Flávio na média da última pesquisa de cada instituto ({br(p2['frente_flavio_pesquisas'], 2)} pontos) contra o erro da média das pesquisas em {PQ['casos']} segundos turnos passados | em {PQ['casos_com_erro_maior']} dos {PQ['casos']}, a média das pesquisas superestimou o líder por mais do que essa frente | **{pct(pil['pesquisas'])}** |",
    f"| **Histórico de viradas** | {pct(W['historico'])} | com que frequência o líder do 1º turno perdeu o 2º, quando a frente era parecida com a do Flávio ({br(p2['frente_flavio_1t'], 2)} pontos; faixa de 1,5 ponto para cada lado) | {HS['faixa_viradas']} viradas em {HS['faixa_casos']} disputas | **{pct(pil['historico'])}** |",
    f"| **Crescimento** | {pct(W['crescimento'])} | o 1º turno de 2026 com os votos livres (outros candidatos, branco e nulo, abstenção) indo como foram em cada 2º turno de 2002 a 2022 | o Lula venceria em {CR['lula_venceria_em']} dos {CR['padroes']} padrões | **{pct(pil['crescimento'])}** |",
])
sens = "\n".join(f"| {k} | {pct(x)} | {um_em(x)} |" for k, x in p2["sensibilidade"].items())

if len(em):
    em = em.assign(nome=em.pais.map(pais))
    br_pres = em[em.pais == "Brasil"].sort_values("ano")
    fora = em[em.pais != "Brasil"]
    perdeu = fora[~fora.lider_das_pesquisas_venceu].sort_values("superestimou_lider", ascending=False)
    maiores = em.assign(ab=em.superestimou_lider).sort_values("ab", ascending=False)
    acima_2026 = int((em.superestimou_lider > erro_2026).sum())
    acima_2026_abs = int((em.superestimou_lider.abs() > erro_2026).sum())
    tab_br = "\n".join(f"| {int(x.ano)} | {int(x.institutos)} | {br(x.frente_lider_pesquisas)} | {br(x.frente_lider_urna)} | {sinal(x.superestimou_lider)} | {'sim' if x.lider_das_pesquisas_venceu else '**não**'} |"
                       for x in br_pres.itertuples())
    tab_br += f"\n| **2026** | {U['n']} | {br(p2['frente_flavio_pesquisas'])} | {br(-v['frente_2t_pontos'])} | **{sinal(erro_2026)}** | **não** |"
    tab_perdeu = "\n".join(f"| {x.nome} {int(x.ano)} | {br(x.frente_lider_pesquisas)} | {br(x.frente_lider_urna)} | {sinal(x.superestimou_lider)} |" for x in perdeu.itertuples())
    lista_maiores = ", ".join(f"{x.nome} {int(x.ano)} ({sinal(x.superestimou_lider)})" for x in maiores.head(10).itertuples())
else:
    tab_br = tab_perdeu = lista_maiores = ""
    acima_2026 = acima_2026_abs = 0
    fora = perdeu = pd.DataFrame()

tab_hist = "\n".join(
    f"| {int(x.ano)} | {br(x.abstencao_1t_pct, 2)}% | {br(x.abstencao_2t_pct, 2)}% | {sinal(x.abstencao_2t_pct - x.abstencao_1t_pct, 2)} | {sinal(x.variacao_pt_media)} | {br(x.variacao_pt_desvio, 2)} | {int(x.municipios_pt_caiu)} |"
    for x in hist.itertuples())
tab_sem_origem = "\n".join(
    f"| {int(x.ano)} | {n(x.pt_votos_sem_origem)} em {int(x.pt_municipios_sem_origem)} | {n(x.anti_votos_sem_origem)} em {int(x.anti_municipios_sem_origem)} | {br(x.pt_sem_origem_pct_da_margem, 2)}% | {int(x.comparecimento_acima_95_2t)} | {int(x.municipios_residuo_acima_4dp)} |"
    for x in hist.itertuples())
tab_novos = "\n".join(f"| {int(x.ano)} | {sinal(x.comparecimento_variou_pct, 2)} | {pct(x.novo_eleitor_para_pt)} | {pct(x.novo_eleitor_para_adversario)} |" for x in novos.itertuples())
outros = trano[trano.origem_1t == "outros"]
tab_outros = "\n".join(
    f"| {int(x.ano)} | {mi(x.votos_origem)} | {br(x.para_pt_pct, 0)}% | {br(x.para_adversario_pct, 0)}% | {br(x.para_branco_nulo_pct + x.para_abstencao_pct, 0)}% | {pct(novos[novos.ano == x.ano].outros_para_pt.iloc[0])} e {pct(novos[novos.ano == x.ano].outros_para_adversario.iloc[0])} |"
    for x in outros.itertuples())
tab_cres = "\n".join(f"| {x['padrao_de']} | {br(x['outros_para_pt_pct'], 0)}% e {br(x['outros_para_adversario_pct'], 0)}% | {br(x['branco_nulo_para_pt_pct'], 0)}% | {br(x['abstencao_para_pt_pct'], 1)}% e {br(x['abstencao_para_adversario_pct'], 1)}% | **{br(x['lula_pct'], 2)}%** |" for x in CR["por_padrao"])
tab_ext = "\n".join(f"| {int(x.ano)} | {sinal(x.brasil_variacao)} | {sinal(x.exterior_variacao)} |" for x in ext.itertuples())
tab_casos_faixa = "; ".join(f"{pais(str(c.get('pais')))} {int(c['ano'])} ({br(c['frente_1t'], 2)} ponto{'s' if c['frente_1t'] >= 2 else ''}{', **virou**' if c['virada'] else ''})" for c in HS["faixa_lista"] if "outros" in str(c.get("grupo")))
gov_faixa = [c for c in HS["faixa_lista"] if "governador" in str(c.get("grupo"))]
grupos_hist = "\n".join(f"| {g} | {x['casos']} | {x['viradas']} | {x['perto_viradas']} em {x['perto_casos']} |" for g, x in HS["por_grupo"].items())
if tp:
    tab_tp = "\n".join(f"| {nome} | {tp['por_grupo'][g]['institutos']} | {br(tp['por_grupo'][g]['lula_entre_os_dois'], 0)}% (de {br(tp['por_grupo'][g]['minimo'], 0)} a {br(tp['por_grupo'][g]['maximo'], 0)}) | {br(tr[(tr.origem_1t == g) & (tr.destino_2t == 'lula')].pct_da_origem.iloc[0] / (tr[(tr.origem_1t == g) & (tr.destino_2t.isin(['lula', 'flavio']))].pct_da_origem.sum()) * 100, 0)}% |"
                       for g, nome in (("cury", "Augusto Cury"), ("renan", "Renan Santos"), ("caiado", "Ronaldo Caiado")))
c22, c26 = ale["curva"]["2022"], ale["curva"]["2026"]
pr_, ex_ = ale["prorrogacao"], ale["exterior"]
si = p2["soma_ingenua"]
hp = pd.DataFrame(R["historico_erro_pesquisas"]["linhas"])
e1 = {int(x.ano): x.erro_medio_anti_pt for x in hp[hp.turno == 1].itertuples()}
e2_ = {int(x.ano): x.erro_medio_anti_pt for x in hp[hp.turno == 2].itertuples()}
tab_lado = "\n".join(f"| {a} | {sinal(e1[a])} | {sinal(e2_[a])} |" for a in (2014, 2018, 2022)) + f"\n| **2026** | {sinal(e1[2026])} | **{sinal(-U['erro_medio'])}** |"

mundo_txt = ""
if tem_mundo:
    mu_ = HS["por_grupo"].get("presidente, outros países", {})
    mundo_txt = f" Em outros países, {mu_.get('viradas', 0)} viradas em {mu_.get('casos', 0)} segundos turnos presidenciais."

# ------------------------------------------------------------------ de onde vieram os votos
DO = R["de_onde"]
AJ = DO["ajustes_2026"]
A0 = AJ["por região"]
OL, NL = DO["outros_livres"], DO["novos_livres"]
GL, GF = DO["ganho_lula_municipios"], DO["ganho_flavio_municipios"]
faixa = {k: (min(a[k] for a in AJ.values()), max(a[k] for a in AJ.values())) for k in ("dos_outros", "dos_novos", "da_troca")}
dov = pd.DataFrame(DO["por_ano"])
ond = pd.DataFrame(DO["por_uf"])
tab_ajustes = "\n".join(f"| {k} | {mi(a['dos_outros'])} | {mi(a['dos_novos'])} | {mi(a['da_troca'])} |" for k, a in AJ.items())
top = ond.head(6)
tab_uf = "\n".join(f"| {x.uf} | +{mi(x.lula_ganhou)} | {br(100 * x.lula_ganhou / GL, 0)}% | +{mi(x.flavio_ganhou)} | {mi(x.outros_livres)} | {mi(x.abstencao_caiu)} |" for x in top.itertuples())
parte4 = 100 * top.lula_ganhou.sum() / GL
tab_livres = "\n".join(f"| {int(x.ano)} | {mi(x.livres_no_saldo)} | {br(x.parte_do_pt_nos_livres_pct, 0)}% | {mi(x.pt_da_troca)} |" for x in dov.itertuples())
d06 = dov[dov.ano == 2006].iloc[0]
d22 = dov[dov.ano == 2022].iloc[0]
# ------------------------------------------------------------------ o porquê (rodada 4)
PQ4 = R["porque"]
ond4, dir4, ren4 = PQ4["onde"], PQ4["direita"], PQ4["renda"]
gr = pd.DataFrame(ren4["grupos"])
dr = pd.DataFrame(dir4["direita (Renan, Caiado e Zema)"])
tn = pd.DataFrame(PQ4["tendencia"])
direita_1t = t1["renan"] + t1["caiado"] + t1["zema"]
tab_renda = "\n".join(f"| {x.grupo} | R$ {n(x.renda_media)} | {br(x.lula_1t_pct, 0)}% | {br(x.lula_ganhou_por_100)} | {br(x.flavio_ganhou_por_100)} | {br(x.abstencao_caiu_pontos)} | {br(x.parte_da_virada_pct, 0)}% | {br(x.parte_do_eleitorado_pct, 0)}% |" for x in gr.itertuples())
tab_dir = "\n".join(f"| {x.grupo} | {br(x.forca_media)}% | {br(x.lula_levou_dos_livres_pct, 0)}% | {br(x.flavio_levou_dos_livres_pct, 0)}% |" for x in dr.itertuples())
tab_reg4 = "\n".join(f"| {x['regiao']} | {br(x['parte_da_virada_pct'], 1)}% | {br(x['parte_do_eleitorado_pct'], 1)}% |" for x in ond4["por_regiao"])
tab_tend = "\n".join(f"| {int(x.ano)} | {'+' if x.inclinacao_por_semana > 0 else ''}{br(x.inclinacao_por_semana)} | {br(x.media_ultima_semana)}% | {br(x.reta_no_dia)}% | {br(x.urna if pd.notna(x.urna) else t2['lula_pct'])}% |" for x in tn.itertuples())
# ------------------------------------------------------------------ isso é normal? (rodada 5)
NM = R["normalidade"]
cp5 = pd.DataFrame(NM["campo"])
cm5 = pd.DataFrame(NM["comparecimento"])
CH = NM["chance"]
SE = NM["como_seria_pelas_pesquisas"]
k26, c22c = cp5[cp5.ano == 2026].iloc[0], cp5[cp5.ano == 2022].iloc[0]
cen = cp5[cp5.ano.isin(CH["crescimento"]["anos_parecidos"])]
m26c, m22c = cm5[cm5.ano == 2026].iloc[0], cm5[cm5.ano == 2022].iloc[0]
ate18 = cm5[cm5.ano <= 2018]
erro_votos = erro_2026 / 100 * t2["validos"]
tab_campo = "\n".join(
    f"| {int(x.ano)} | {x.principais} | {br(x.apoiou_pt_pct, 0)}% | {br(x.apoiou_adversario_pct, 0)}% | **{br(x.parte_do_pt_nos_livres_pct, 0)}%** | {br(x.eliminados_para_pt_modelo_nacional_pct, 0)}% e {br(x.eliminados_para_adversario_modelo_nacional_pct, 0)}% | {br(x.eliminados_para_pt_modelo_regional_pct, 0)}% |"
    for x in cp5.itertuples())
tab_comp = "\n".join(
    f"| {int(x.ano)} | {sinal(x.comparecimento_variou_pontos, 2)} | {n(x.municipios_comparecimento_subiu)} ({br(x.municipios_comparecimento_subiu_pct, 0)}%) | {sinal(x.diferenca_andou_no_pais_pontos)} | {br(x.municipios_mesmo_lado_do_pais_pct, 0)}% | {br(x.desvio_da_virada_entre_municipios, 2)} |"
    for x in cm5.itertuples())
tab_ch = "\n".join(f"| {k} | {pct(x)} | {um_em(x)} |" for k, x in CH["variantes"].items())
perto5 = "; ".join(f"{pais(str(c.get('pais')))}{' ' + str(c['uf']) if isinstance(c.get('uf'), str) and c.get('uf') not in ('BR',) else ''} {int(c['ano'])} (líder com {br(c['lider_1t_pct'], 1)}%, {br(c['frente_1t'], 2)} de frente{', **virou**' if c['virada'] else ''})" for c in CH["historico"]["perto_de_50_lista"])
eleit_pt = (min(DO["ajustes_2026"]["por região"]["dos_outros"], k26.eliminados_para_pt_modelo_nacional_pct / 100 * OL),
            max(DO["ajustes_2026"]["por região"]["dos_outros"], k26.eliminados_para_pt_modelo_nacional_pct / 100 * OL))
brp = casos[casos.grupo == 'Brasil presidente']
lid_faixa = [c['lider_1t_pct'] for c in HS['faixa_lista']]
mais_que_5 = int((em.superestimou_lider.abs() > erro_2026).sum()) if len(em) else 0
# ------------------------------------------------------------------ os vídeos que circularam (rodada 6)
VD = R["videos"]
c60 = VD["conta_dos_60"]
fx = pd.DataFrame(VD["faixas"])
fx26 = fx[fx.ano == 2026]
subiu = fx26[fx26.comparecimento_variou_pontos > 0]
sn = pd.DataFrame(VD["sem_novos"])
sn26 = sn[sn.ano == 2026].iloc[0]
sn_hist = sn[(sn.ano < 2026) & (sn.ano != 2006)]
dv = pd.DataFrame(VD["divisao"])
dv26 = dv[dv.ano == 2026].iloc[0]
sims = {x['ano_base']: x for x in VD['simulacao_por_ano']}
sim22, sim06, sim18 = sims[2022], sims[2006], sims[2018]
# ------------------------------------------------------------------ rodada 7
R7 = R["rodada7"]
qg = pd.DataFrame(R7["quem_ganhou_mais"])
q26 = qg[qg.ano == 2026].iloc[0]
pad = R7["pesquisas_antes_e_depois"]
tab_qg = "\n".join(f"| {int(x.ano)} | {n(x.pt_ganhou_mais_votos_em)} ({br(x.pt_ganhou_mais_votos_em_pct, 0)}%) | {br(x['parte_do_pt_Sul'], 0)}% | {br(x['parte_do_pt_Sudeste'], 0)}% | {br(x['parte_do_pt_Centro-Oeste'], 0)}% | {br(x['parte_do_pt_Nordeste'], 0)}% | {br(x['parte_do_pt_Norte'], 0)}% |" for _, x in qg.iterrows())
# ------------------------------------------------------------------ RELATÓRIO
relatorio = f"""# Relatório: as pesquisas, o histórico e a chance do que aconteceu no 2º turno de 2026

Gerado por `ferramentas/gerar-relatorio.py` a partir de `resultados/RESUMO.json`. **Rodada 2 (26/10/2026)**: refeita pelo retorno do autor, com o histórico de erro das pesquisas no Brasil e em outros países, as viradas de 2º turno, os mesmos testes em todas as eleições de 2002 a 2022 e a chance calculada em pilares com os pesos dele. O que mudou da rodada 1 está em [`docs/RODADAS.md`](docs/RODADAS.md).

## A resposta curta

**Antes da votação, a chance de o Lula vencer era de cerca de {pct(CH['bayes'])} ({um_em(CH['bayes'])}), refeita na rodada 5** (a rodada 2 dava {pct(p2['combinada'])}; as três correções estão abaixo). A ponta de baixo, tratando os três pilares como indícios independentes, dá {pct(CH['independente'])} ({um_em(CH['independente'])}), e o mercado dava {pct(CH['mercado'])} na véspera. Vencer **pela diferença que venceu** ({br(v['frente_2t_pontos'], 2)} pontos ou mais) tinha perto de {pct(CH['bayes_resultado_igual_ou_maior'])} ({um_em(CH['bayes_resultado_igual_ou_maior'])}).

**Duas coisas de 2026 saem do padrão das eleições de 2002 a 2022, e uma não sai.** Saem: o candidato do PT levar {br(k26.parte_do_pt_nos_livres_pct, 0)}% dos votos livres quando quem saiu era de direita ou de centro e apoiou o adversário, e o comparecimento subir {br(m26c.comparecimento_variou_pontos, 2)} ponto do 1º para o 2º turno. Não sai: a virada se espalhar por quase todos os municípios, que é o que acontece sempre que a diferença anda muito no país.

## Rodada 5: isso é normal?

Pedido do autor: *"é normal, tendo em vista que os candidatos eram de direita, que a maior parte dos votos vá para o Lula? Nas outras eleições, isso aconteceu de verdade?"*, se é normal o comparecimento subir e a virada se espalhar, e se a chance de 39% considerou as pesquisas, o 1º turno e o crescimento *"com peso de forma correta"*. Cada resposta abaixo põe 2026 ao lado das 6 eleições anteriores, com a mesma conta.

### 1. O eleitor de quem saiu ir para o PT quando quem saiu apoiou o adversário

| Eleição | Quem saiu (os 3 maiores) e o que fez no 2º turno | Votos de quem saiu com apoio ao PT | Com apoio ao adversário | PT nos votos livres (saldo, conta exata) | Eleitores de quem saiu: PT e adversário (modelo nacional) | Para o PT (modelo regional) |
|---|---|---|---|---|---|---|
{tab_campo}

A posição de cada candidato, com o link da fonte, está em `dados/agentes/apoios_segundo_turno.csv` (27 de 28 com fonte; Zé Maria, 2002, sem fonte). A coluna do saldo é conta exata; as duas últimas são estimativas, porque o voto é secreto, e os dois modelos do projeto discordam entre si.

**O que a tabela mostra:**
- **Em 2026, {br(k26.apoiou_adversario_pct, 0)}% dos votos de quem saiu eram de candidatos que declararam apoio ao Flávio, nenhum declarou apoio ao Lula, e o Lula levou {br(k26.parte_do_pt_nos_livres_pct, 0)}% de tudo o que estava livre.** Nas 6 eleições anteriores, o PT só passou de 60% dos votos livres em 2006 e 2018, quando os maiores eliminados eram da esquerda ou ficaram neutros.
- **Nos anos em que quem saiu era de centro ou de direita ({', '.join(str(a) for a in cen.ano)}), o PT ficou com {br(cen.parte_do_pt_nos_livres_pct.min(), 0)}% a {br(cen.parte_do_pt_nos_livres_pct.max(), 0)}% dos votos livres.** Pelos dois modelos, o eleitor dos eliminados foi mais para o PT em 2026 do que em qualquer um desses anos: {br(k26.eliminados_para_pt_modelo_nacional_pct, 0)}% contra {br(cen.eliminados_para_pt_modelo_nacional_pct.min(), 0)}% a {br(cen.eliminados_para_pt_modelo_nacional_pct.max(), 0)}% no modelo nacional, e {br(k26.eliminados_para_pt_modelo_regional_pct, 0)}% contra {br(cen.eliminados_para_pt_modelo_regional_pct.min(), 0)}% a {br(cen.eliminados_para_pt_modelo_regional_pct.max(), 0)}% no regional.
- **O espelho é 2022.** {br(c22c.apoiou_pt_pct, 0)}% dos votos de quem saiu eram de Tebet e Ciro, que apoiaram o Lula, e o Bolsonaro levou {br(100 - c22c.parte_do_pt_nos_livres_pct, 0)}% dos votos livres. O apoio declarado já não decidia para onde ia o eleitor livre em 2022; em 2026 ele também não decidiu, no sentido contrário.
- **O que as pesquisas diziam desse eleitor:** entre Lula e Flávio, o de Cury dava {br(tp['por_grupo']['cury']['lula_entre_os_dois'], 0)}% ao Lula, o de Renan {br(tp['por_grupo']['renan']['lula_entre_os_dois'], 0)}% e o de Caiado {br(tp['por_grupo']['caiado']['lula_entre_os_dois'], 0)}% (média de 5 institutos cada). Se eles tivessem votado assim e quem voltou a votar tivesse se dividido como no próprio ano, o Flávio teria vencido por {mi(-SE['margem_lula'])}. O Lula venceu por {mi(frente)}: uma distância de {mi(frente - SE['margem_lula'])}, do mesmo tamanho do erro das pesquisas na diferença ({br(erro_2026, 1)} pontos dos válidos, cerca de {mi(erro_votos)}). **É o mesmo erro, visto de outro lugar: as pesquisas erraram justamente no eleitor que estava livre.**
- 🔧 **Correção do que foi dito na rodada 3:** o "cerca de 6 milhões vieram dos eleitores dos outros candidatos" é o modelo regional. O modelo nacional, usado desde a rodada 1, dá {mi(k26.eliminados_para_pt_modelo_nacional_pct / 100 * OL)}. A parte que vem de quem saiu e a que vem de quem voltou a votar mudam conforme o modelo: **de {mi(eleit_pt[0])} a {mi(eleit_pt[1])} vieram dos eleitores dos outros candidatos**, e o resto, de quem voltou a votar ou tinha votado branco ou nulo. O total é exato; a divisão, não.

**Veredito: não é normal.** É o resultado mais fora do padrão da série nesse quesito, junto com 2022 no sentido contrário. Pela lente do resultado legítimo, o espelho de 2022 mostra que o apoio declarado do candidato derrotado não leva o eleitor junto, e o erro das pesquisas do mesmo tamanho já aconteceu em segundos turnos de outros países ({mais_que_5} de {len(em)} erraram a diferença por mais de {br(erro_2026, 1)} pontos). Pela lente da fraude, é exatamente nesse eleitor livre que um voto acrescentado apareceria. O que pesa contra ela, no dado por município: na regressão de cada ano, quem voltou a votar se dividiu quase igual entre os dois ({pct(novos[novos.ano == 2026].novo_eleitor_para_pt.iloc[0])} e {pct(novos[novos.ano == 2026].novo_eleitor_para_adversario.iloc[0])}, como em 2022), e o ganho do Lula aparece no país inteiro, sem bolsões. Seção a seção, é o projeto do vídeo 16.

### 2. O comparecimento subir e a virada se espalhar

| Eleição | Comparecimento do 1º para o 2º turno (pontos) | Municípios em que subiu | Diferença andou no país (pontos, a favor do PT) | Municípios que andaram no mesmo sentido | Desvio da virada entre municípios |
|---|---|---|---|---|---|
{tab_comp}

- **O comparecimento:** de 2002 a 2018 ele sempre caiu do 1º para o 2º turno ({sinal(ate18.comparecimento_variou_pontos.max(), 1)} a {sinal(ate18.comparecimento_variou_pontos.min(), 1)} ponto), e subiu em no máximo {br(ate18.municipios_comparecimento_subiu_pct.max(), 0)}% dos municípios. Em 2022 subiu pela primeira vez ({sinal(m22c.comparecimento_variou_pontos, 2)}, em {br(m22c.municipios_comparecimento_subiu_pct, 0)}% dos municípios). Em 2026 subiu {sinal(m26c.comparecimento_variou_pontos, 2)}, em {br(m26c.municipios_comparecimento_subiu_pct, 0)}% dos municípios: **o maior da série, {br(m26c.comparecimento_variou_pontos / m22c.comparecimento_variou_pontos, 0)} vezes o de 2022.** Em 2026, o transporte de graça no dia da votação era regra no país inteiro (Resolução TSE nº 23.751/2026, em `dados/agentes/fatos_entre_os_turnos.md`), só que nos 2 turnos, então ele sozinho não explica a subida de um turno para o outro.
- **Onde ele subiu:** mais nas cidades de renda maior (a abstenção caiu {br(gr.iloc[-1].abstencao_caiu_pontos)} ponto nos 20% de municípios mais ricos e ficou parada nos 20% mais pobres) e não onde o PT era mais forte (a correlação entre a força do PT no 1º turno e a queda da abstenção foi {br(h26.corr_forca_pt_1t_e_queda_abstencao, 2)} em 2026, contra {br(hist[hist.ano < 2026].corr_forca_pt_1t_e_queda_abstencao.min(), 2)} a {br(hist[hist.ano < 2026].corr_forca_pt_1t_e_queda_abstencao.max(), 2)} nas outras).
- **A virada espalhada:** em 2026 a diferença andou para o Lula em {br(m26c.municipios_mesmo_lado_do_pais_pct, 0)}% dos municípios. Em 2006, o outro ano em que ela andou muito a favor do PT, foram {br(cm5[cm5.ano == 2006].municipios_mesmo_lado_do_pais_pct.iloc[0], 0)}%. Quando a diferença anda muito no país, ela anda em quase todo lugar. O desvio entre municípios ({br(m26c.desvio_da_virada_entre_municipios, 2)} ponto) é o menor da série, perto do de 2022 ({br(m22c.desvio_da_virada_entre_municipios, 2)}): nos dois anos, poucos votos estavam livres (os eliminados somaram {br(100 * OL / t1['validos'], 1)}% dos válidos em 2026), e movimento pequeno sai mais igual.

**Veredito:** o comparecimento **não é normal** pela série de 2002 a 2018 e é a continuação, em tamanho maior, do que começou em 2022; ele subiu mais onde a renda é maior e não onde o PT era mais forte. A virada espalhada **é normal** para o tamanho do movimento.

### 3. A chance, refeita com as nuances que faltavam

A conta da rodada 2 tinha três defeitos. Dois puxavam a chance para cima, e um escondia o quanto ela podia cair.

1. **O histórico não olhava o quanto o líder estava perto de 50%.** A rodada 2 contou as viradas entre segundos turnos com frente parecida ({HS['faixa_viradas']} em {HS['faixa_casos']}), misturando líderes com {br(min(lid_faixa), 0)}% e com {br(max(lid_faixa), 0)}%. Um líder com 47% precisa de bem menos votos novos. Com as duas coisas na conta ({CH['historico']['casos']} segundos turnos, regressão), a chance de virada cai de {pct(CH['historico']['rodada_2'])} para **{pct(CH['historico']['chance'])}**. Os {CH['historico']['perto_de_50_casos']} casos com o líder entre 45% e 50% e frente de até 4 pontos tiveram {CH['historico']['perto_de_50_viradas']} viradas: {perto5}. Para presidente no Brasil, o líder do 1º turno venceu as {len(brp)} vezes, mas a menor frente foi de {br(brp.frente_1t.min(), 1)} pontos, então essa regra não fala de uma frente de {br(p2['frente_flavio_1t'], 2)}.
2. **O crescimento usava os 6 padrões de transferência sem olhar quem tinha saído.** Em 2026 quem saiu era de centro ou de direita. Só com os anos parecidos ({', '.join(str(a) for a in CH['crescimento']['anos_parecidos'])}), o Lula venceria em {CH['crescimento']['lula_venceria_em']} de {CH['crescimento']['padroes']} (ficaria com {', '.join(br(x['lula_pct'], 1) + '%' for x in CH['crescimento']['lula_pct_por_padrao'])}). Pela regra de Laplace, **{pct(CH['crescimento']['laplace'])}**, contra {pct(CH['crescimento']['rodada_2'])} antes.
3. **A média com pesos é o jeito errado de juntar indícios que apontam para o mesmo lado.** Ela trata os pilares como opiniões que se substituem. Quando cada um é um indício diferente, a conta é por chances (Bayes): o histórico dá o ponto de partida e as pesquisas atualizam. Como as pesquisas já carregam boa parte do que o crescimento mede (o eleitor dos eliminados é entrevistado nelas), o central usa os dois primeiros; contar os três como independentes é a ponta de baixo.

**O que não cai:** o pilar das pesquisas. Só com 2º turnos de presidente com 4 ou mais institutos ({CH['pesquisas']['casos_4_institutos']} casos), a chance sobe para {pct(CH['pesquisas']['so_presidente_4_institutos'])}; e no Brasil a média das pesquisas superestimou o líder nos 6 segundos turnos de 2002 a 2022, o que também puxaria para o Lula.

| Jeito de calcular | Chance do Lula | Em outras palavras |
|---|---|---|
{tab_ch}

**Veredito:** a chance era **menor do que a rodada 2 disse: cerca de {pct(CH['bayes'])}, perto de 1 em 4**, com ponta de baixo de {pct(CH['independente'])} e o mercado em {pct(CH['mercado'])}. Abaixo de {um_em(CH['independente'])} ela não vai por nenhum dos caminhos calculados aqui: com a frente de {br(p2['frente_flavio_pesquisas'], 1)} ponto nas pesquisas, basta um erro de 2º turno do tamanho que já aconteceu muitas vezes. Ganhar por {br(v['frente_2t_pontos'], 1)} pontos ou mais era mais raro: {pct(CH['bayes_resultado_igual_ou_maior'])} ({um_em(CH['bayes_resultado_igual_ou_maior'])}).

## Rodada 7: o Lula ganhar mais votos que o Flávio em quase todo lugar, e o Bolsa Família nas pesquisas

**É normal o candidato do PT ganhar mais votos que o adversário em tantos municípios, e até no Sul?**

| Eleição | Municípios em que o PT ganhou mais votos que o adversário | Parte do PT no que os dois ganharam: Sul | Sudeste | Centro-Oeste | Nordeste | Norte |
|---|---|---|---|---|---|---|
{tab_qg}

Em 2026 o Lula ganhou mais votos que o Flávio em **{n(q26.pt_ganhou_mais_votos_em)} municípios ({br(q26.pt_ganhou_mais_votos_em_pct, 0)}%)**; só 2006 teve mais ({br(qg[qg.ano == 2006].pt_ganhou_mais_votos_em_pct.iloc[0], 0)}%), e em 2022 foram {br(qg[qg.ano == 2022].pt_ganhou_mais_votos_em_pct.iloc[0], 0)}%. **No Sul**, o Lula levou {br(q26['parte_do_pt_Sul'], 0)}% do que os dois ganharam; fora 2006, o PT nunca tinha passado de {br(qg[(qg.ano != 2006) & (qg.ano < 2026)]['parte_do_pt_Sul'].max(), 0)}% ali. **Veredito: fora do padrão, e é a mesma coisa da rodada 5 vista no mapa:** em 2006, o único ano parecido, quem saiu era da esquerda e o adversário perdeu votos; em 2026, quem saiu apoiou o Flávio.

**Se o Bolsa Família tivesse virado votos em escala, as pesquisas de depois do pagamento mostrariam?** O pagamento de outubro foi em 19, 20 e 21/10. Nos {pad['institutos']} institutos com pesquisa antes e depois de 19/10, o Lula subiu em média {sinal(pad['variacao_media'], 2)} ponto dos válidos (média de {br(pad['media_antes'], 1)}% antes e {br(pad['media_depois'], 1)}% depois). A urna deu {br(t2['lula_pct'], 1)}%. O que as pesquisas captaram depois do pagamento é uma fração pequena do que faltou; a virada que elas não viram não aparece nelas como efeito do pagamento. Limite: pesquisa de campo até 24/10 pode não pegar um efeito dos últimos dias.

## Rodada 6: os vídeos que circularam depois do resultado

O autor mandou 6 vídeos que circularam nas redes (Tarcísio de Freitas, Nikolas Ferreira e 4 criadores no TikTok) e pediu para ver se eles batem com este projeto ou trazem um ponto que faltava. A análise afirmação por afirmação está em [`docs/VIDEOS_QUE_CIRCULARAM.md`](docs/VIDEOS_QUE_CIRCULARAM.md). O principal:

- **A conta dos 98% (@carlosphyll).** Com 60% dos votos dos outros candidatos para o Lula, faltariam {mi(c60['falta'])}, {br(c60['parte_dos_novos_pct'], 1)}% dos votos novos ({mi(c60['novos'])}). A aritmética confere (e os 40% restantes dão ao Flávio {mi(c60['flavio_dos_outros_se_40'])}, o que ele ganhou). A conclusão, de que quase todo eleitor novo escolheu o Lula, não segue: os 60% são uma escolha. Nos {n(sn26.municipios)} municípios em que o comparecimento caiu, onde no saldo ninguém novo votou, o Flávio {'perdeu' if sn26.adversario_ganhou < 0 else 'ganhou'} {n(abs(sn26.adversario_ganhou) / 1e3)} mil votos e o Lula ganhou {n(sn26.pt_ganhou / 1e3)} mil, {br(sn26.pt_ganhou_sobre_os_outros_pct, 0)}% dos votos dos outros candidatos ali (nos mesmos municípios, de 2002 a 2022 sem 2006: de {br(sn_hist.pt_ganhou_sobre_os_outros_pct.min(), 0)}% a {br(sn_hist.pt_ganhou_sobre_os_outros_pct.max(), 0)}%). E onde o comparecimento subiu, a parte do Lula no que os dois ganharam ficou entre {br(subiu.parte_do_pt_no_ganho_pct.min(), 0)}% e {br(subiu.parte_do_pt_no_ganho_pct.max(), 0)}%, sem subir junto com o comparecimento (`g26`). **A estranheza está no eleitor livre inteiro, não em quem voltou a votar.**
- **O mesmo 73,6% (@pietragrisotto)** e o Lula subindo quase 8 pontos no Sudeste e 7,5 no Centro-Oeste: os números conferem; é a estranheza da rodada 5.
- **As "primeiras vezes" (Nikolas Ferreira):** a virada, a regra do 1º turno e a de Minas no 1º turno são verdade e são o mesmo fato; a prorrogação nacional é um fato separado e também é verdade (a 1ª da história), com efeito em voto medido pelo projeto do vídeo 16.
- **O mercado no dia seguinte (@igor.bevilaqua):** o circuit breaker de 26/10 confere; o resto é do projeto do vídeo 18.
- **A simulação do Tarcísio de Freitas (antes do resultado):** a taxa de conversão de 2022 por UF aplicada a 2026, com fator aleatório, dá o Flávio com {br(100 - sim22['lula_pct'], 1)}%, o número dele. O fator só varia em volta de 2022; com cada outro ano-base o mesmo método dá: {'; '.join(f"{a}: Lula {br(x['lula_pct'], 1)}%" for a, x in sims.items())}. A faixa de 90% dele (51,8% a 53,6% para o Flávio) não cobria a chance de 2026 não se comportar como 2022, que foi o que aconteceu.
- ⚠️ **Duas contas simples deste projeto discordam** sobre como quem voltou a votar se dividiu ({pct(novos[novos.ano == 2026].novo_eleitor_para_pt.iloc[0])} e {pct(novos[novos.ano == 2026].novo_eleitor_para_adversario.iloc[0])} controlando o 1º turno; {pct(dv26.novos_para_pt)} e {pct(dv26.novos_para_adversario)} sem controle). As duas são estimativas; a leitura sem modelo é a dos grupos de municípios acima.

## De onde vieram os 10,38 milhões de votos a mais do Lula

**A conta fecha, voto por voto.** Entre o 1º e o 2º turno ficaram livres {mi(-v['outros_candidatos'] - v['abstencao'] - v['branco_nulo'])} de votos: os {mi(-v['outros_candidatos'])} dos candidatos que saíram, {mi(-v['abstencao'])} de pessoas que não tinham votado e votaram, e {mi(-v['branco_nulo'])} que tinham votado branco ou nulo e escolheram alguém. O Lula ficou com {mi(v['lula'])} e o Flávio com {mi(v['flavio'])}. Soma: {mi(v['ganho_dos_dois'])}, exatamente o que estava livre. **O Lula levou 3 de cada 4 votos que estavam em jogo.**

**De onde veio cada parte** (resultado de 5.571 municípios; o voto é secreto, então é uma estimativa, feita de três jeitos que dão quase o mesmo número):

| Ajuste | Eleitores dos outros candidatos | Quem não tinha votado em ninguém | Eleitores do Flávio que mudaram para o Lula |
|---|---|---|---|
{tab_ajustes}

**Resposta direta:**
1. **Cerca de 6 milhões (de {mi(faixa['dos_outros'][0])} a {mi(faixa['dos_outros'][1])}) vieram de quem votou em outro candidato no 1º turno** (Cury, Renan, Caiado, Zema e os demais). Dos {mi(OL)} desses eleitores, cerca de 2 em cada 3 votaram no Lula.
2. **Cerca de 3,6 milhões (de {mi(faixa['dos_novos'][0])} a {mi(faixa['dos_novos'][1])}) vieram de quem não tinha votado em ninguém no 1º turno**: quem faltou e voltou a votar, e quem tinha votado branco ou nulo. Dos {mi(NL)} que entraram, cerca de 3 em cada 4 votaram no Lula.
3. **Quase nada veio de eleitor do Flávio que mudou de lado: de {mi(faixa['da_troca'][0])} a {mi(faixa['da_troca'][1])}.** O método enxerga essa troca quando ela existe: em 2006, ele encontra {mi(d06.pt_da_troca)} de eleitores do Alckmin que foram para o Lula, e foi o ano em que o Alckmin teve menos votos no 2º turno do que no 1º.

**Onde:** {', '.join(top.uf.head(4))} somam {br(100 * top.lula_ganhou.head(4).sum() / GL, 0)}% do ganho do Lula.

| UF | Lula ganhou | Parte do ganho do Lula | Flávio ganhou | Votos dos outros no 1º turno | Abstenção caiu |
|---|---|---|---|---|---|
{tab_uf}

**Isso já aconteceu?** O candidato do PT ficar com a maior parte dos votos livres, sim, mas só quando quem saiu era da esquerda ou ficou neutro; com quem saiu apoiando o adversário, nunca (seção "Rodada 5" acima):

| Eleição | Votos livres no saldo | Parte que o PT levou | Eleitores do adversário que mudaram para o PT (estimativa) |
|---|---|---|---|
{tab_livres}

Em 2006 o PT levou **mais do que tudo o que estava livre** ({br(d06.parte_do_pt_nos_livres_pct, 0)}%), porque, além dos livres, ganhou eleitores do Alckmin. Em 2022 foi o contrário: o Bolsonaro levou {br(100 - d22.parte_do_pt_nos_livres_pct, 0)}% dos livres e mesmo assim perdeu. **Os 74% de 2026 são o segundo maior da série, abaixo de 2006.**

**Por que isso surpreendeu:** as pesquisas diziam que os eleitores de Renan e de Caiado iam mais para o Flávio, e somando os três maiores o Flávio levaria uns {mi(tp['flavio_receberia'] - tp['lula_receberia']) if tp else ''} a mais. O resultado mostra o contrário: 2 em cada 3 votaram no Lula. Esses cruzamentos das pesquisas usam grupos de 40 a 100 entrevistados, com margem de erro de 10 pontos ou mais, e em 2022 também não acertaram: davam de 42% a 60% do eleitor de Ciro e de Tebet para o Lula, e o Bolsonaro levou {br(100 - d22.parte_do_pt_nos_livres_pct, 0)}% dos votos livres. E o filtro de eleitor provável trabalha contra quem tende a faltar: na Nexus da véspera, tirar os 21% menos propensos a votar baixava o Lula de 49,5% para 47,6%, e foi justamente esse eleitor que voltou a votar.

**O que o dado não separa:** quanto dos 6 milhões veio de cada candidato. Os eleitores de Cury, Renan e Caiado estão misturados nos mesmos municípios, e o ajuste candidato por candidato fica instável (`resultados/de_onde_vieram_por_candidato_2026.csv`). O total dos três juntos é estável.

## O que justifica a virada (rodada 4)

**Escopo deste projeto:** pesquisas, histórico e resultado por país, estado e município. O que é seção por seção (logs das urnas, boletins, horário de cada voto) é do projeto do vídeo 16 (`investigacao-segundo-turno-2026`); daqui só se cita o número que ele publicou dos votos depois das 17h: **34.810 votos no país**, que seriam 0,79% da diferença mesmo se fossem todos do Lula.

**Os fatos de que se parte** (levantados com link em `dados/agentes/fatos_entre_os_turnos.md`):
- **Os apoios:** Zema declarou voto no Flávio em 05/10, Caiado em 06/10 e Cury em 08/10 (com um termo de compromisso); Renan Santos ficou neutro e criticou o Flávio.
- **As medidas do governo:** o Bolsa Família subiu 15,04% (decreto de 17/09, piso de R$ 600 para R$ 691) e a parcela de outubro foi paga em 19, 20 e 21/10, antes do 2º turno; o Prospera MEI (perdão de dívidas de MEIs a partir de 2027) foi anunciado em 13/10 e sancionado em 21/10; os impostos federais da gasolina foram zerados por 30 dias em 09/10.
- **O transporte:** ônibus de graça no dia da votação era obrigatório no país; São Paulo rodou com frota maior no 2º turno.

### 1. O eleitor de direita foi mais para o Flávio, mas não em bloco

Renan, Caiado e Zema tinham **{mi(direita_1t)}** de votos no 1º turno. O Flávio inteiro ganhou **{mi(v['flavio'])}** no 2º. Mesmo que todo o ganho do Flávio tivesse vindo desses três, faltariam {mi(direita_1t - v['flavio'])}: o apoio declarado não levou os eleitores junto.

| Municípios pela força de Renan, Caiado e Zema | Os três no 1º turno | Lula levou dos votos livres | Flávio levou |
|---|---|---|---|
{tab_dir}

Onde os três eram mais fortes, o Flávio levou mais, como se esperaria; mesmo assim o Lula levou a maior parte. Em Goiás, a base do Caiado ({br(dir4['goias']['caiado_1t_pct'], 1)}% no 1º turno), o Lula levou {br(dir4['goias']['lula_levou_pct'], 0)}% dos votos livres.

### 2. As medidas para os mais pobres não explicam a virada

Se o reajuste e a antecipação do Bolsa Família tivessem virado votos, o Lula teria crescido mais nos municípios mais pobres, onde estão os beneficiários. Municípios em 5 grupos pela renda per capita do Censo 2022:

| Grupo | Renda (mediana) | Lula no 1º turno | Lula ganhou a cada 100 eleitores | Flávio ganhou | Abstenção caiu (pontos) | Parte da virada da diferença | Parte do eleitorado |
|---|---|---|---|---|---|---|---|
{tab_renda}

- O Lula **ganhou menos votos por eleitor nos municípios mais pobres** ({br(gr.iloc[0].lula_ganhou_por_100)} a cada 100) **do que nos mais ricos** ({br(gr.iloc[-1].lula_ganhou_por_100)}), e foi nos mais ricos que a abstenção mais caiu.
- Como o Flávio também ganhou mais nos mais ricos, **a virada da diferença foi parecida em todas as faixas de renda**: cada grupo deu à virada uma parte próxima do seu peso no eleitorado (um pouco acima nos três grupos mais pobres, um pouco abaixo nos dois mais ricos). Não há a concentração nos mais pobres que o Bolsa Família produziria.
- As medidas voltadas à classe média urbana (MEI, gasolina) combinam com o lugar onde o Lula mais ganhou votos, mas **não foram testadas** aqui.

### 3. Onde a virada aconteceu

A diferença entre os dois andou de Flávio {mi(-ond4['margem_1t'])} à frente para Lula {mi(ond4['margem_2t'])} à frente: uma virada de {mi(ond4['virada_total'])}. Ela andou para o Lula em **{n(ond4['municipios_em_que_a_margem_andou_para_o_lula'])} municípios** e para o Flávio em {n(ond4['municipios_em_que_andou_para_o_flavio'])}. Os {ond4['municipios_que_viraram']['quantos']} municípios que trocaram de vencedor deram só {br(ond4['municipios_que_viraram']['parte_pct'], 0)}% da virada; o resto veio de lugares que já eram de um lado e ficaram mais Lula.

| Região | Parte da virada | Parte do eleitorado |
|---|---|---|
{tab_reg4}

O Nordeste deu mais do que o seu peso; o Sul e o Centro-Oeste, menos. A maior contribuição de uma cidade sozinha foi a de São Paulo ({mi(ond4['maiores_contribuicoes'][0]['virada_margem'])}).

### 4. O que apontava para o Lula antes da votação

| 2º turno | Inclinação das pesquisas (pontos por semana para o PT) | Média da última semana | Reta das pesquisas no dia da eleição | Urna |
|---|---|---|---|---|
{tab_tend}

Em 2026 as pesquisas andavam para o Lula, mas devagar: a reta chegava a {br(tn[tn.ano == 2026].reta_no_dia.iloc[0])}% no dia da eleição, ainda abaixo de 50%. Em 2014 e 2018 o PT subia de 2 a 3 pontos por semana na reta final. Os outros sinais a favor eram poucos: duas pesquisas (Vox Brasil e Colectta) e o eleitor de baixa propensão a votar, que no Datafolha da véspera dava Lula 52 a 48.

### O que fica de pé, em uma frase por lado

- **A favor do resultado:** a virada se espalhou por quase todos os municípios, veio de eleitores dos candidatos derrotados que não seguiram o apoio declarado (cerca de 6 milhões) e de gente que voltou a votar (cerca de 3,6 milhões), com mais força nas cidades maiores, e os votos depois das 17h não mudam nada.
- **O que segue sem explicação completa:** por que tanta gente dos candidatos de direita não foi para o Flávio, e por que as pesquisas não captaram quem voltou a votar. O dado por município mostra onde e quanto; o motivo de cada eleitor, ele não mostra.

## 1. Como a chance foi calculada

Três pilares, cada um medindo a chance de um jeito diferente, com **os pesos que o autor escolheu para a projeção do vídeo longo 14** (pesquisas pesam mais porque são a medida mais direta e mais recente; o histórico pesa menos porque tem poucos casos de presidente; o crescimento pesa menos ainda porque depende de um modelo de transferência de votos, que é a parte mais frágil):

| Pilar | Peso | O que mede | O que o histórico mostra | Chance do Lula |
|---|---|---|---|---|
{tab_pilares}

**Conta:** {br(W['pesquisas'], 2)} × {pct(pil['pesquisas'])} + {br(W['historico'], 2)} × {pct(pil['historico'])} + {br(W['crescimento'], 2)} × {pct(pil['crescimento'])} = **{pct(p2['combinada'], 1)}**.

**Conferência pelo mercado:** a Polymarket dava {pct(p2['mercado'], 1)} ao Lula no preço diário da véspera (série do projeto do vídeo 16; a imprensa registrou 79,6% para o Flávio na manhã da eleição). Nos {p1['polymarket_favoritos_70_90']['mercados']} mercados de eleição em que o favorito tinha de 70% a 90%, o favorito perdeu {p1['polymarket_favoritos_70_90']['favorito_perdeu']}. A mesma Polymarket deu o Lula como favorito no 1º turno ({pct(p1['polymarket_1t']['preco'])}) e errou.

**Quanto o número depende das escolhas:**

| Variante | Chance do Lula | Em outras palavras |
|---|---|---|
{sens}

A variante mais desfavorável ao resultado usa só os 7 segundos turnos de presidente no Brasil para o histórico (0 viradas, pela regra de Laplace {um_em(p1['historico_laplace'])}). Mesmo nela a chance fica perto de 1 em 3.

### O erro de multiplicar as "coincidências"

Uma conta que circula: as pesquisas erraram, o líder do 1º turno perdeu pela primeira vez, a regra de Minas quebrou e o favorito do mercado perdeu; multiplicando as chances de cada coisa ({pct(si['componentes']['pesquisas'])} × {pct(si['componentes']['historico'])} × {pct(si['componentes']['minas'])} × {pct(si['componentes']['mercado'])}), dá **1 em {n(si['um_em_ingenuo'])}**. A conta está errada porque as quatro coisas **são o mesmo fato** visto de quatro lugares: se o Lula vencesse, as pesquisas que davam Flávio errariam, o líder do 1º turno perderia, a regra de Minas quebraria e o favorito do mercado perderia, tudo junto, automaticamente. Multiplicar só vale para fatos independentes. A chance de todas acontecerem juntas é a chance de o Lula vencer: cerca de **{um_em(si['probabilidade_correta'])}**.

## 2. As pesquisas já erraram tanto assim?

**O erro de 2026:** a média da última pesquisa de cada instituto ({U['n']} institutos) dava o Flávio {br(p2['frente_flavio_pesquisas'], 2)} pontos à frente; a urna deu o Lula {br(v['frente_2t_pontos'], 2)} à frente. A média superestimou a frente do Flávio em **{br(erro_2026)} pontos** ({br(erro_2026 / 2)} no voto de cada um). Nenhuma das {P['todas']['n']} pesquisas chegou no número da urna; na última de cada instituto, {U['deram_flavio']} de {U['n']} davam Flávio.

### No Brasil, 2º turno de presidente

| Eleição | Institutos | Frente do líder nas pesquisas | Frente dele na urna | Quanto a média superestimou o líder | O líder das pesquisas venceu? |
|---|---|---|---|---|---|
{tab_br}

O líder das pesquisas tinha vencido todos os segundos turnos de presidente desde 2002, e **em todos os 6 a média superestimou o líder** (em média {br(PQ['por_fonte']['Brasil presidente']['erro_medio'])} pontos na frente). Quem descontasse esse viés de sempre da frente de {br(p2['frente_flavio_pesquisas'], 2)} pontos do Flávio já chegaria a uma disputa empatada, levemente inclinada para o Lula (a chance pelas pesquisas iria a {pct(PQ['por_fonte']['Brasil presidente']['normal'])}; com só 6 eleições, isso entra como variante, não como número principal). **O erro de 2026 é o segundo maior da série**; o maior foi o de 2002 (só o Datafolha tem a última pesquisa publicada com data), mas lá o Lula tinha 28 pontos de frente e o erro não mudou o vencedor. **Em 2026 o erro foi do mesmo tamanho, numa disputa em que a frente era de menos de 2 pontos.** É isso que fez a diferença: erros desse tamanho já aconteceram, mas nunca numa disputa tão apertada.

### O lado do erro: menos à direita no 1º turno, mais no 2º

Erro médio das últimas pesquisas no candidato contra o PT, em pontos (positivo: deram mais a ele do que a urna):

| Eleição | 1º turno | 2º turno |
|---|---|---|
{tab_lado}

No 1º turno as pesquisas deram menos ao candidato contra o PT nas quatro eleições; no 2º deram mais em 2014, 2018 e 2026. **A inversão de lado entre os turnos, que é apontada como sinal de algo estranho, já tinha acontecido em 2014 e 2018.**

### Em outros países

Na base de {len(em)} segundos turnos presidenciais com pesquisas (Brasil e outros {len(fora)} no mundo, de 2010 a 2026, cada número conferido na fonte; `resultados/erro_media_pesquisas_runoffs.csv`), **o líder das pesquisas perdeu em {len(perdeu)}** ({pct(len(perdeu) / max(len(em), 1))}). Em {acima_2026} delas a média superestimou o líder por mais do que em 2026, e em {acima_2026_abs} o erro foi maior que o de 2026 para algum dos lados. Os maiores erros: {lista_maiores}.

| Onde o líder das pesquisas perdeu | Frente nas pesquisas | Frente dele na urna | Quanto a média superestimou o líder |
|---|---|---|---|
{tab_perdeu}

**Leitura:** no Brasil, o erro de 2026 é grande; no mundo, é comum. O que pesa é a combinação de um erro de tamanho já visto com uma frente pequena. Em 2º turno de governador no Brasil ({len(gov_hist)} disputas de 2014 a 2022), o erro médio absoluto da média das pesquisas na frente do líder foi de {br(gov_hist.superestimou_lider.abs().mean())} pontos.

## 3. "Nunca houve virada": o que o histórico diz

| Grupo | Segundos turnos | Viradas | Com frente de até 3 pontos e líder abaixo de 50% |
|---|---|---|---|
{grupos_hist}

Para presidente no Brasil, a regra "o líder do 1º turno vence" valia {reg['presidente_lider_1t_venceu']['acertos']} de {reg['presidente_lider_1t_venceu']['vezes']}, **mas nenhuma dessas 7 eleições teve uma frente pequena**: a menor era de {br(reg['presidente_lider_1t_venceu']['menor_frente_ate_2022'], 2)} pontos (2022), contra {br(v['frente_1t_pontos'], 2)} em 2026. A regra nunca tinha sido testada numa disputa apertada. Quando a frente é parecida com a do Flávio (até 1,5 ponto para mais ou para menos), o líder perdeu **{HS['faixa_viradas']} de {HS['faixa_casos']}** vezes: {sum(c['virada'] for c in gov_faixa)} de {len(gov_faixa)} em governador no Brasil e {HS['faixa_viradas'] - sum(c['virada'] for c in gov_faixa)} de {HS['faixa_casos'] - len(gov_faixa)} em presidente pelo mundo.{mundo_txt} Os de presidente: {tab_casos_faixa}. Base: `resultados/viradas_casos.csv` (2º turnos de outros países conferidos na Wikipédia, {int((casos.grupo == "presidente, outros países").sum())} válidos).

**Minas:** quem venceu Minas no 1º turno venceu a eleição {reg['minas']['sum_1t']} de {reg['minas']['count_1t']} vezes (quebrou em 2026: Minas deu Flávio no 1º turno); quem venceu Minas no 2º turno venceu a eleição {reg['minas']['sum_2t']} de {reg['minas']['count_2t']} (valeu: Minas deu Lula). Minas acerta porque é parecida com o Brasil; numa eleição decidida por 1 a 2 pontos, um estado parecido com o país pode cair de qualquer lado.

## 4. O crescimento: os votos livres como em cada eleição passada

O 1º turno de 2026 com quem votou em Lula e em Flávio repetindo o voto, e os votos livres indo como foram em cada 2º turno de 2002 a 2022 (modelo de transição por município, por região; `resultados/crescimento_pelos_padroes_passados.csv`):

| Padrão de | Outros candidatos para PT e para o adversário | Branco e nulo para o PT | Abstenção para PT e para o adversário | Lula em 2026 |
|---|---|---|---|---|
{tab_cres}

O Lula venceria com o padrão de 2006 e com o de 2018, e perderia com os outros quatro. **Nenhum padrão do passado leva aos {br(t2['lula_pct'], 2)}% que ele teve.** O que 2026 teve de diferente foi a abstenção: ela caiu {br(t1['abstencao_pct'] - t2['abstencao_pct'], 2)} pontos entre os turnos, quando em 5 das 6 eleições anteriores tinha subido.

## 5. O resultado, em números

| | 1º turno (04/10) | 2º turno (25/10) | Diferença |
|---|---|---|---|
| Lula | {n(t1['lula'])} ({br(t1['lula_pct'], 2)}%) | {n(t2['lula'])} (**{br(t2['lula_pct'], 2)}%**) | **+{n(v['lula'])}** |
| Flávio | {n(t1['flavio'])} ({br(t1['flavio_pct'], 2)}%) | {n(t2['flavio'])} ({br(t2['flavio_pct'], 2)}%) | **+{n(v['flavio'])}** |
| Outros candidatos | {n(-v['outros_candidatos'])} | 0 | {n(v['outros_candidatos'])} |
| Abstenção | {n(t1['abstencao'])} ({br(t1['abstencao_pct'], 2)}%) | {n(t2['abstencao'])} ({br(t2['abstencao_pct'], 2)}%) | {n(v['abstencao'])} |
| Brancos e nulos | {n(t1['brancos'] + t1['nulos'])} | {n(t2['brancos'] + t2['nulos'])} | {n(v['branco_nulo'])} |

A conta fecha no voto: o que os dois ganharam ({n(v['ganho_dos_dois'])}) é exatamente o que saiu dos outros candidatos, da abstenção e do branco e nulo. Só Minas virou de estado (para o Lula); o Lula subiu em todos os 27 estados, de {br(est['lula_subiu_min'])} a {br(est['lula_subiu_max'])} pontos; {mun['viradas'].get('Flávio para Lula', 0)} municípios viraram para o Lula e {mun['viradas'].get('Lula para Flávio', 0)} para o Flávio. Em {gov['mesmo_lado']} de {gov['ufs']} estados o governador eleito é da coligação do lado que venceu para presidente ali; no 2º turno de governador do mesmo dia houve {len(viradas_gov)} viradas em {len(gov['viradas_2t_2026'])} disputas.

**Abstenção, em cada eleição:**

| Eleição | Abstenção no 1º turno | No 2º | Variação | Subida média do PT nos municípios (pontos) | Desvio entre municípios | Municípios em que o PT caiu |
|---|---|---|---|---|---|---|
{tab_hist}

O nível de 2026 no 2º turno ({br(h26.abstencao_2t_pct, 2)}% nos municípios do Brasil) é parecido com o de 2006; o incomum foi a **queda** entre os turnos. E a subida do Lula foi **a segunda mais uniforme da série** (desvio de {br(h26.variacao_pt_desvio, 2)} ponto entre municípios), depois da de 2022 ({br(hist[hist.ano == 2022].variacao_pt_desvio.iloc[0], 2)}).

## 6. Para onde foram os votos de Cury, Renan e Caiado

Três jeitos de medir, que não concordam inteiramente:

| Eleitor de | Institutos com o cruzamento | O que as pesquisas diziam (Lula entre Lula e Flávio) | O que o resultado por município indica (modelo de transição) |
|---|---|---|---|
{tab_tp if tp else ''}

- **As pesquisas** (a última rodada de cada instituto com o cruzamento por voto no 1º turno, cada número conferido na fonte): os eleitores de Renan e de Caiado iam mais para o Flávio; os de Cury, um pouco mais para o Lula. Somando os três, o Flávio receberia cerca de {mi(tp['flavio_receberia'] - tp['lula_receberia']) if tp else ''} a mais que o Lula. ⚠️ Cada grupo é cerca de 2% da amostra (uns 40 a 100 entrevistados), com margem de erro de 10 pontos ou mais.
- **O resultado por município, modelo com restrição:** dividiram-se com um pouco mais para o Lula em cada um (faixa larga).
- **O resultado por município, regressão das variações:** os outros candidatos meio a meio ({pct(novos[novos.ano == 2026].outros_para_pt.iloc[0])} e {pct(novos[novos.ano == 2026].outros_para_adversario.iloc[0])}).

**Leitura:** o dado agregado não separa com precisão o eleitor de cada candidato. O que ele diz com segurança é a conta do saldo: se todo voto novo fosse do Lula, ele ainda precisaria de {br(v['lula_precisou_dos_outros_pct_se_todo_novo_fosse_dele'])}% dos votos dos outros. Isso está dentro do que aconteceu em 2002 e 2018 (veja abaixo), mas acima do que as pesquisas de 2026 indicavam. A diferença entre "o que as pesquisas diziam desses eleitores" e "o que o resultado exige" é um dos pontos que a lente F levanta, e é real. Se os eleitores dos outros foram como as pesquisas diziam, o Lula precisou de troca direta de voto (gente que votou Flávio no 1º turno e Lula no 2º). Isso tem precedente: em 2006, o Alckmin teve **menos votos no 2º turno do que no 1º** ({mi(39950856 - 37522266)} a menos, nos municípios do Brasil; conferido em `ferramentas/validacao-independente.py`).

| Eleição | Votos dos outros no 1º turno | Para o PT | Para o adversário | Branco, nulo ou faltou | Pela regressão (PT e adversário) |
|---|---|---|---|---|---|
{tab_outros}

## 7. A lente da fraude: cada alegação, na versão mais forte, testada

O mapa das alegações (quem disse, onde, com o link) está em `dados/agentes/alegacoes_fraude_2026.md`. Cada teste usa as eleições de 2002 a 2022, que ninguém contesta, como régua, e o mesmo teste para o Flávio como espelho.

| Alegação (versão mais forte) | O que precisaria aparecer no dado | O que o dado mostra | Régua de 2002 a 2022 |
|---|---|---|---|
| **(a) As pesquisas e o mercado erraram demais** | erro fora da distribuição histórica | erro de {br(erro_2026)} pontos na frente: o 2º maior do Brasil, mas superado em {acima_2026} de {len(em)} segundos turnos | o lado do erro (mais à direita no 2º turno) é o mesmo de 2014 e 2018 |
| **(b) Nunca houve virada; Minas sempre acerta** | regra que vale também com frente pequena | as 7 eleições de presidente nunca tiveram frente pequena; com frente parecida, o líder perdeu {HS['faixa_viradas']} de {HS['faixa_casos']} | Minas no 2º turno acertou de novo |
| **(c) A abstenção caiu demais, "surgiram" votos** | eleitor novo indo quase todo para um lado; queda concentrada onde o Lula é forte | onde o comparecimento subiu, o eleitor a mais se dividiu {pct(novos[novos.ano == 2026].novo_eleitor_para_pt.iloc[0])} para o Lula e {pct(novos[novos.ano == 2026].novo_eleitor_para_adversario.iloc[0])} para o Flávio; a queda da abstenção quase não acompanha a força do Lula (correlação {br(h26.corr_forca_pt_1t_e_queda_abstencao, 2)}) | queda entre os turnos inédita; o nível do 2º turno é parecido com o de 2006 |
| **(c) Votos sem origem** | ganho que não cabe no que estava livre no município | {n(h26.pt_votos_sem_origem)} votos do Lula em {int(h26.pt_municipios_sem_origem)} municípios ({br(h26.pt_sem_origem_pct_da_margem, 2)}% da frente); Flávio {n(h26.anti_votos_sem_origem)} | em 2006, numa eleição sem contestação, o PT teve {n(hist[hist.ano == 2006].pt_votos_sem_origem.iloc[0])} ({br(hist[hist.ano == 2006].pt_sem_origem_pct_da_margem.iloc[0], 1)}% da frente) |
| **(d) A prorrogação até 19h decidiu** | votos depois das 17h da ordem da frente | sem nenhum voto do Lula em Salvador, Feira de Santana e Lauro de Freitas, ele ainda venceria por {mi(pr_['frente_sem_nenhum_voto_do_lula_ali'])}. Os logs contados por terceiros dão {n(pr_['votos_depois_das_17h_logs_terceiros']['g1_tv_globo'])} votos depois das 17h no país (g1/TV Globo) | a campanha do Flávio também pediu prorrogação (SP, PR e SC) |
| **(e) A pausa e a virada da noite** | curva que a ordem de chegada não explica | o Flávio liderou de {br(c26['flavio_passa_com_pct'], 2)}% a {br(c26['pt_passa_com_pct'], 2)}% das seções (maior frente: {br(c26['maior_frente_anti'], 2)} ponto); o Lula passou às {c26['pt_passa_hora'][11:16]} | em 2022 o Bolsonaro liderou até {br(c22['pt_passa_com_pct'], 0)}% das seções, com frente de até {br(c22['maior_frente_anti'], 1)} pontos |
| **(g) Comparecimento estranho** | municípios com comparecimento perto de 100% e voto quase todo num lado | nenhum município acima de 95% de comparecimento | 2014 teve {int(hist[hist.ano == 2014].comparecimento_acima_95_2t.iloc[0])} no 2º turno |
| **Subida fora do padrão** | municípios em que a variação não segue a composição do 1º turno | {int(h26.municipios_residuo_acima_4dp)} municípios fora de 4 desvios; a composição do 1º turno explica {pct(h26.r2_variacao_explicada)} da variação | 2022: {int(hist[hist.ano == 2022].municipios_residuo_acima_4dp.iloc[0])} e {pct(hist[hist.ano == 2022].r2_variacao_explicada.iloc[0])} |
| **(h) Exterior** | saldo do exterior da ordem da frente | saldo de {n(ex_['saldo_exterior'])} votos; sem o exterior, frente de {mi(ex_['frente_sem_o_exterior'])}. A subida do Lula no exterior ({sinal(ext[ext.ano == 2026].exterior_variacao.iloc[0])}) foi quase igual à do Brasil ({sinal(ext[ext.ano == 2026].brasil_variacao.iloc[0])}) | urnas fora do país, apuradas à parte |
| **(f) Urna, código, logs, boletins** | divergência de assinatura, de RDV ou do teste de integridade | **não testado aqui** (é seção a seção: projeto do vídeo 16). O TSE publicou o teste de integridade sem divergência | |

**O que a lente F acerta, e fica de pé:** (1) a surpresa é real: nenhum dos três pilares dava o Lula como favorito; (2) todas as pesquisas erraram para o mesmo lado, e o erro do Brasil é o 2º maior desde 2002; (3) a queda da abstenção entre os turnos não tem precedente; (4) o que as pesquisas diziam dos eleitores de Renan e Caiado não combina bem com o que o resultado exige; (5) a parte seção a seção (logs, boletins, horário) não está neste projeto.

## 8. A lente do resultado legítimo

| Se foi legítimo, esperaria-se | O dado |
|---|---|
| uma chance real de virada antes da votação | {pct(p2['combinada'])} pelos três pilares |
| erro de pesquisa já visto | erro do mesmo tamanho em 2002; maior em {acima_2026} de {len(em)} segundos turnos pelo mundo |
| votos fechando | fecham no voto |
| subida espalhada | o Lula subiu nos 27 estados e em {n(mun['lula_ganhou_votos_em'])} de {n(mun['municipios'])} municípios, com a segunda menor variação entre municípios da série |
| eleitor novo dividido, sem lado único | {pct(novos[novos.ano == 2026].novo_eleitor_para_pt.iloc[0])} e {pct(novos[novos.ano == 2026].novo_eleitor_para_adversario.iloc[0])} |
| apuração com a forma de sempre | a mesma virada na contagem de 2022, mais cedo e menor |

**O que a lente L não explica bem:** por que **nenhuma** das {P['todas']['n']} pesquisas chegou no número; e por que a abstenção caiu tanto. A hipótese mais citada é o filtro de eleitor provável: no Datafolha da véspera, o eleitor de alta propensão a votar dava Flávio 52 a 48, e o de média e baixa, Lula 52 a 48; se mais gente de baixa propensão votou, o erro vai para o lado que aconteceu. Isso combina com a queda da abstenção, mas **não está provado**.

## 9. Juntando tudo

**O dado sustenta mais a lente do resultado legítimo**, com estes graus de confiança:
- **Alta confiança:** nenhum dos testes que este projeto consegue fazer com o resultado oficial por município mostra 2026 fora do padrão das eleições de 2002 a 2022, e os tetos de pior caso (prorrogação, exterior, votos sem origem) ficam muito abaixo da frente de {mi(frente)}.
- **Média confiança:** a chance antes da votação era de cerca de {pct(p2['combinada'])}. O número muda alguns pontos conforme as escolhas (de {pct(min(p2['sensibilidade'].values()))} a {pct(max(p2['sensibilidade'].values()))} nas variantes), mas em nenhuma fica abaixo de 1 em 4.
- **O que fica aberto:** o seção a seção (vídeo 16) e o porquê do erro das pesquisas.

## 10. Validação

{val_ok} de {len(val)} números centrais refeitos por outro caminho (`ferramentas/validacao-independente.py`). Os números trazidos pelas pesquisas de apoio só entram depois de conferidos na página de origem por `ferramentas/conferir-agentes.py` (texto guardado em `dados/brutos/capturas/agentes/`). Totais por UF e por município fecham com diferença zero.
"""
(RAIZ / "RELATORIO.md").write_text(relatorio, encoding="utf-8")

simples = f"""# Resumo simples (rodada 5)

## De onde vieram os 10,38 milhões de votos a mais do Lula

| Origem | Votos para o Lula | De quantos estavam livres |
|---|---|---|
| Eleitores dos outros candidatos (Cury, Renan, Caiado, Zema e outros) | de {mi(eleit_pt[0])} a {mi(eleit_pt[1])}, conforme o modelo | de {mi(OL)} |
| Quem não tinha votado em ninguém no 1º turno (faltou, branco ou nulo) | o resto, de {mi(GL - eleit_pt[1])} a {mi(GL - eleit_pt[0])} | de {mi(NL)} |
| Eleitores do Flávio que mudaram | menos de 0,6 milhão | quase nada |

A conta fecha: estavam livres {mi(v['ganho_dos_dois'])}, o Lula levou {mi(v['lula'])} e o Flávio {mi(v['flavio'])}. SP, MG, RJ e BA somam metade do ganho do Lula.

## Isso é normal? (rodada 5)

| Pergunta | Resposta | O número |
|---|---|---|
| O eleitor de quem saiu ir para o Lula, se quem saiu era de direita ou de centro? | **Não é normal.** Nos anos parecidos ({', '.join(str(a) for a in cen.ano)}) o PT levou de {br(cen.parte_do_pt_nos_livres_pct.min(), 0)}% a {br(cen.parte_do_pt_nos_livres_pct.max(), 0)}% dos votos livres | 2026: {br(k26.parte_do_pt_nos_livres_pct, 0)}%, com {br(k26.apoiou_adversario_pct, 0)}% dos votos de quem saiu vindo de quem apoiou o Flávio |
| Já aconteceu o apoio declarado não valer? | **Sim, em 2022, no sentido contrário** | Tebet e Ciro ({br(c22c.apoiou_pt_pct, 0)}% dos votos de quem saiu) apoiaram o Lula, e o Bolsonaro levou {br(100 - c22c.parte_do_pt_nos_livres_pct, 0)}% dos livres |
| As pesquisas viram isso? | **Não.** Pelo que diziam do eleitor de Cury, Renan e Caiado, o Flávio venceria por {mi(-SE['margem_lula'])} | a distância até o resultado ({mi(frente - SE['margem_lula'])}) tem o tamanho do erro das pesquisas ({mi(erro_votos)}) |
| O comparecimento subir no 2º turno? | **Não é normal até 2018** (sempre caiu); subiu pela 1ª vez em 2022 ({sinal(m22c.comparecimento_variou_pontos, 2)}) e em 2026 subiu {sinal(m26c.comparecimento_variou_pontos, 2)} | subiu mais nas cidades de renda maior, não onde o PT era mais forte |
| A virada em quase todos os municípios? | **É normal** para o tamanho do movimento | 2026: {br(m26c.municipios_mesmo_lado_do_pais_pct, 0)}% dos municípios; 2006: {br(cm5[cm5.ano == 2006].municipios_mesmo_lado_do_pais_pct.iloc[0], 0)}% |

## Os vídeos que circularam (rodada 6)

| Vídeo | O que diz | O dado |
|---|---|---|
| @carlosphyll | com 60% dos outros para o Lula, 98% de quem voltou a votar teria escolhido o Lula | a aritmética confere ({br(c60['parte_dos_novos_pct'], 0)}%); os 60% são uma escolha. Onde ninguém novo votou, o Lula ganhou {br(sn26.pt_ganhou_sobre_os_outros_pct, 0)}% dos votos dos outros e o Flávio perdeu votos; onde mais gente voltou, a parte do Lula não subiu |
| @ale_paschalis | o eleitor do Cury jamais votaria no Lula, então a conta não fecha | nas pesquisas, o eleitor do Cury dava 53% ao Lula entre os dois |
| @pietragrisotto | 73,6% dos votos adicionais para o Lula | confere; é a estranheza da rodada 5 |
| Nikolas Ferreira | muitas "primeiras vezes" | 3 delas são o mesmo fato; a prorrogação nacional é a única separada, e é verdade |
| @igor.bevilaqua | circuit breaker no dia seguinte | confere; o mercado é do vídeo 18 |
| Tarcísio de Freitas (antes do resultado) | com as taxas de 2022 por UF e Monte Carlo, Flávio com 52,6% | reproduzido: {br(100 - sim22['lula_pct'], 1)}%; com outro ano-base, outra eleição (2006: Lula {br(sim06['lula_pct'], 1)}%; 2018: {br(sim18['lula_pct'], 1)}%) |

Detalhe: [`docs/VIDEOS_QUE_CIRCULARAM.md`](docs/VIDEOS_QUE_CIRCULARAM.md).

## A pergunta: qual era a chance do que aconteceu?

**Cerca de {pct(CH['bayes'])}, ou {um_em(CH['bayes'])}, de o Lula vencer**, com o que se sabia no sábado (refeita na rodada 5; a rodada 2 dava {pct(p2['combinada'])}). Ponta de baixo: {pct(CH['independente'])}. Mercado: {pct(CH['mercado'])}.

**O que mudou na rodada 5:** o histórico passou a olhar o quanto o Flávio estava perto de 50% ({pct(CH['historico']['rodada_2'])} → {pct(CH['historico']['chance'])}); o crescimento passou a usar só os anos em que quem saiu era de centro ou de direita ({pct(CH['crescimento']['rodada_2'])} → {pct(CH['crescimento']['laplace'])}); e os pilares passaram a ser somados como indícios (o histórico como ponto de partida, as pesquisas atualizando), no lugar da média com pesos. A tabela abaixo é a da rodada 2, mantida para comparação.

| Pilar | Peso (o do vídeo 14) | Chance do Lula | De onde vem |
|---|---|---|---|
| Pesquisas | {pct(W['pesquisas'])} | {pct(pil['pesquisas'])} | em {PQ['casos_com_erro_maior']} de {PQ['casos']} segundos turnos passados, as pesquisas erraram a favor do líder por mais do que a frente do Flávio |
| Histórico de viradas | {pct(W['historico'])} | {pct(pil['historico'])} | com frente parecida com a do Flávio, o líder do 1º turno perdeu {HS['faixa_viradas']} de {HS['faixa_casos']} vezes |
| Crescimento | {pct(W['crescimento'])} | {pct(pil['crescimento'])} | com os votos livres indo como em cada eleição de 2002 a 2022, o Lula venceria em {CR['lula_venceria_em']} de {CR['padroes']} |
| **Junto** | | **{pct(p2['combinada'])}** | |

- **Por que não é "1 em 1.000":** multiplicar "as pesquisas erraram × o líder perdeu × Minas quebrou × o mercado errou" trata como quatro sorteios o que é um só fato: o Lula vencer uma disputa apertada. Dado que ele venceu, as quatro coisas acontecem juntas.
- **As pesquisas já erraram tanto?** No Brasil, uma vez: em 2002, do mesmo tamanho, mas com 28 pontos de frente. No mundo, o líder das pesquisas perdeu {len(perdeu)} de {len(em)} segundos turnos. O que 2026 teve de diferente foi um erro grande numa disputa apertada.
- **"Nunca houve virada"?** Para presidente, nunca, mas nenhum dos 7 casos tinha frente pequena. Com frente parecida e o líder perto de 50%, o líder perdeu perto de 4 em cada 10 vezes ({pct(CH['historico']['chance'])}, rodada 5).
- **A lente da fraude:** a surpresa é real, o erro das pesquisas também, e dois sinais saem do padrão de 2002 a 2022 (o eleitor livre indo para o Lula com quem saiu apoiando o Flávio, e o comparecimento subindo). Os testes de fraude que dá para fazer com o resultado por município (votos sem origem, eleitor novo indo todo para um lado, subida fora do padrão, curva da apuração, prorrogação, exterior) ficam dentro do que aconteceu em 2002 a 2022. O seção a seção é o projeto do vídeo 16.

Relatório completo: [`RELATORIO.md`](RELATORIO.md). Leitura das duas lentes: [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md).
"""
(RAIZ / "RESUMO_SIMPLES.md").write_text(simples, encoding="utf-8")

leitura = f"""# Leitura da IA: as duas lentes (rodada 5)

Esta leitura é do Claude, a partir dos números do [`RELATORIO.md`](../RELATORIO.md). "Fraude" aqui é o nome de uma hipótese, testada com o mesmo rigor que a outra.

## Lente F: o resultado foi fraude

**A versão mais forte:** o líder do 1º turno, à frente em {U['deram_flavio']} de {U['n']} institutos e com {pct(1 - p2['mercado'])} no mercado, perdeu por {br(v['frente_2t_pontos'], 2)} pontos; nenhuma das {P['todas']['n']} pesquisas chegou no número; a abstenção caiu como nunca entre os turnos; as pesquisas diziam que os eleitores de Renan e Caiado iam para o Flávio; e a votação foi prorrogada por decisão de um ministro a pedido de uma das campanhas.

**O que fica de pé:** a surpresa (chance de cerca de {pct(CH['bayes'])}, refeita na rodada 5), o eleitor de candidatos que apoiaram o Flávio indo mais para o Lula do que em qualquer eleição parecida desde 2002 ({br(k26.parte_do_pt_nos_livres_pct, 0)}% dos votos livres), o comparecimento subindo como nunca, o erro de todas as pesquisas para o mesmo lado (o 2º maior do Brasil), a queda inédita da abstenção, e a distância entre o que as pesquisas diziam dos eleitores eliminados e o que o resultado exige.

**O que não se sustenta no dado deste projeto:** a ideia de que o resultado era improvável a ponto de 1 em 1.000 (é a conta que multiplica o mesmo fato quatro vezes); voto novo indo todo para um lado (ele se dividiu); votos sem origem em escala que importe ({br(h26.pt_sem_origem_pct_da_margem, 2)}% da frente, contra {br(hist[hist.ano == 2006].pt_sem_origem_pct_da_margem.iloc[0], 1)}% em 2006); prorrogação ou exterior mudando o resultado (os tetos de pior caso ficam muito abaixo da frente); uma curva de apuração diferente da de 2022.

**O que não foi testado aqui e pode mudar a leitura:** logs, boletins e horários seção a seção (vídeo 16).

## Lente L: o resultado foi legítimo

**A versão mais forte:** uma disputa com frente de menos de 2 pontos, num país onde as pesquisas de 2º turno erram para o lado do candidato contra o PT desde 2014, decidida pelo eleitor que voltou a votar.

**O que fica de pé:** a chance real antes da votação, o erro já visto em tamanho, a conta que fecha, a subida uniforme, o eleitor novo dividido, a apuração com a forma de sempre.

**O que não explica bem:** por que nenhuma pesquisa chegou no número, por que a abstenção caiu tanto e por que o eleitor de quem apoiou o Flávio foi tanto para o Lula. O espelho é 2022, quando o eleitor de Tebet e Ciro, que apoiaram o Lula, foi mais para o Bolsonaro: o apoio declarado não decidiu nas duas eleições. A explicação do filtro de eleitor provável combina com o dado, mas não está provada.

## Conclusão

**O dado sustenta mais a lente L.** A diferença entre as duas não está na surpresa, que é real nas duas, e sim nos testes: tudo o que dá para medir com o resultado oficial por município fica dentro do padrão de seis eleições que ninguém contesta.
"""
(RAIZ / "docs" / "LEITURA_DA_IA.md").write_text(leitura, encoding="utf-8")
print("RELATORIO.md, RESUMO_SIMPLES.md e docs/LEITURA_DA_IA.md escritos")
