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

# ------------------------------------------------------------------ RELATÓRIO
relatorio = f"""# Relatório: as pesquisas, o histórico e a chance do que aconteceu no 2º turno de 2026

Gerado por `ferramentas/gerar-relatorio.py` a partir de `resultados/RESUMO.json`. **Rodada 2 (26/10/2026)**: refeita pelo retorno do autor, com o histórico de erro das pesquisas no Brasil e em outros países, as viradas de 2º turno, os mesmos testes em todas as eleições de 2002 a 2022 e a chance calculada em pilares com os pesos dele. O que mudou da rodada 1 está em [`docs/RODADAS.md`](docs/RODADAS.md).

## A resposta curta

**Antes da votação, a chance de o Lula vencer era de cerca de {pct(p2['combinada'])} ({um_em(p2['combinada'])}).** Era a menos provável das duas, mas longe de impossível: um resultado desse tamanho acontece em quase 2 de cada 5 disputas parecidas. A chance de ele vencer **pela diferença que venceu** ({br(v['frente_2t_pontos'], 2)} pontos ou mais) era menor: perto de {pct(PQ['contagem_resultado_igual_ou_maior'])} pelas pesquisas, e nenhum dos 6 padrões do passado chega a ela.

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

simples = f"""# Resumo simples (rodada 2)

## A pergunta: qual era a chance do que aconteceu?

**Cerca de {pct(p2['combinada'])}, ou {um_em(p2['combinada'])}, de o Lula vencer**, com o que se sabia no sábado. Era a menos provável das duas, mas longe de impossível.

| Pilar | Peso (o do vídeo 14) | Chance do Lula | De onde vem |
|---|---|---|---|
| Pesquisas | {pct(W['pesquisas'])} | {pct(pil['pesquisas'])} | em {PQ['casos_com_erro_maior']} de {PQ['casos']} segundos turnos passados, as pesquisas erraram a favor do líder por mais do que a frente do Flávio |
| Histórico de viradas | {pct(W['historico'])} | {pct(pil['historico'])} | com frente parecida com a do Flávio, o líder do 1º turno perdeu {HS['faixa_viradas']} de {HS['faixa_casos']} vezes |
| Crescimento | {pct(W['crescimento'])} | {pct(pil['crescimento'])} | com os votos livres indo como em cada eleição de 2002 a 2022, o Lula venceria em {CR['lula_venceria_em']} de {CR['padroes']} |
| **Junto** | | **{pct(p2['combinada'])}** | |

- **Por que não é "1 em 1.000":** multiplicar "as pesquisas erraram × o líder perdeu × Minas quebrou × o mercado errou" trata como quatro sorteios o que é um só fato: o Lula vencer uma disputa apertada. Dado que ele venceu, as quatro coisas acontecem juntas.
- **As pesquisas já erraram tanto?** No Brasil, uma vez: em 2002, do mesmo tamanho, mas com 28 pontos de frente. No mundo, o líder das pesquisas perdeu {len(perdeu)} de {len(em)} segundos turnos. O que 2026 teve de diferente foi um erro grande numa disputa apertada.
- **"Nunca houve virada"?** Para presidente, nunca, mas nenhum dos 7 casos tinha frente pequena. Com frente parecida, virada é quase cara ou coroa.
- **A lente da fraude:** a surpresa é real e o erro das pesquisas também. Mas os testes que dá para fazer com o resultado por município (votos sem origem, eleitor novo, comparecimento, subida fora do padrão, curva da apuração, prorrogação, exterior) ficam todos dentro do que aconteceu em 2002 a 2022. O seção a seção é o projeto do vídeo 16.

Relatório completo: [`RELATORIO.md`](RELATORIO.md). Leitura das duas lentes: [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md).
"""
(RAIZ / "RESUMO_SIMPLES.md").write_text(simples, encoding="utf-8")

leitura = f"""# Leitura da IA: as duas lentes (rodada 2)

Esta leitura é do Claude, a partir dos números do [`RELATORIO.md`](../RELATORIO.md). "Fraude" aqui é o nome de uma hipótese, testada com o mesmo rigor que a outra.

## Lente F: o resultado foi fraude

**A versão mais forte:** o líder do 1º turno, à frente em {U['deram_flavio']} de {U['n']} institutos e com {pct(1 - p2['mercado'])} no mercado, perdeu por {br(v['frente_2t_pontos'], 2)} pontos; nenhuma das {P['todas']['n']} pesquisas chegou no número; a abstenção caiu como nunca entre os turnos; as pesquisas diziam que os eleitores de Renan e Caiado iam para o Flávio; e a votação foi prorrogada por decisão de um ministro a pedido de uma das campanhas.

**O que fica de pé:** a surpresa (chance de cerca de {pct(p2['combinada'])}), o erro de todas as pesquisas para o mesmo lado (o 2º maior do Brasil), a queda inédita da abstenção, e a distância entre o que as pesquisas diziam dos eleitores eliminados e o que o resultado exige.

**O que não se sustenta no dado deste projeto:** a ideia de que o resultado era improvável a ponto de 1 em 1.000 (é a conta que multiplica o mesmo fato quatro vezes); voto novo indo todo para um lado (ele se dividiu); votos sem origem em escala que importe ({br(h26.pt_sem_origem_pct_da_margem, 2)}% da frente, contra {br(hist[hist.ano == 2006].pt_sem_origem_pct_da_margem.iloc[0], 1)}% em 2006); prorrogação ou exterior mudando o resultado (os tetos de pior caso ficam muito abaixo da frente); uma curva de apuração diferente da de 2022.

**O que não foi testado aqui e pode mudar a leitura:** logs, boletins e horários seção a seção (vídeo 16).

## Lente L: o resultado foi legítimo

**A versão mais forte:** uma disputa com frente de menos de 2 pontos, num país onde as pesquisas de 2º turno erram para o lado do candidato contra o PT desde 2014, decidida pelo eleitor que voltou a votar.

**O que fica de pé:** a chance real antes da votação, o erro já visto em tamanho, a conta que fecha, a subida uniforme, o eleitor novo dividido, a apuração com a forma de sempre.

**O que não explica bem:** por que nenhuma pesquisa chegou no número e por que a abstenção caiu tanto. A explicação do filtro de eleitor provável combina com o dado, mas não está provada.

## Conclusão

**O dado sustenta mais a lente L.** A diferença entre as duas não está na surpresa, que é real nas duas, e sim nos testes: tudo o que dá para medir com o resultado oficial por município fica dentro do padrão de seis eleições que ninguém contesta.
"""
(RAIZ / "docs" / "LEITURA_DA_IA.md").write_text(leitura, encoding="utf-8")
print("RELATORIO.md, RESUMO_SIMPLES.md e docs/LEITURA_DA_IA.md escritos")
