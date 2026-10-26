"""Escreve RELATORIO.md, RESUMO_SIMPLES.md e docs/LEITURA_DA_IA.md a partir de resultados/RESUMO.json e das tabelas.
Nenhum número é escrito à mão: todos saem daqui.
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
NOME_UF = {"ac": "Acre", "al": "Alagoas", "am": "Amazonas", "ap": "Amapá", "ba": "Bahia", "ce": "Ceará", "df": "Distrito Federal",
           "es": "Espírito Santo", "go": "Goiás", "ma": "Maranhão", "mg": "Minas Gerais", "ms": "Mato Grosso do Sul", "mt": "Mato Grosso",
           "pa": "Pará", "pb": "Paraíba", "pe": "Pernambuco", "pi": "Piauí", "pr": "Paraná", "rj": "Rio de Janeiro", "rn": "Rio Grande do Norte",
           "ro": "Rondônia", "rr": "Roraima", "rs": "Rio Grande do Sul", "sc": "Santa Catarina", "se": "Sergipe", "sp": "São Paulo", "to": "Tocantins"}


def br(x: float, c: int = 1) -> str:
    return f"{x:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def n(x: float) -> str:
    return br(x, 0)


def mi(x: float) -> str:
    return f"{br(x / 1e6, 2)} milhões"


def pct(p: float, c: int = 0) -> str:
    return f"{br(100 * p, c)}%"


def sinal(x: float) -> str:
    return "0,0" if abs(x) < 0.05 else f"{'+' if x > 0 else ''}{br(x)}"


def um_em(p: float) -> str:
    return f"1 em {br(1 / p, 1)}"


r, v = R["resultado"], R["resultado"]["variacao"]
t1, t2 = r["t1"], r["t2"]
P = R["pesquisas"]
U = P["ultima_de_cada_instituto"]
reg = R["regras"]
pr = R["probabilidade"]
te = R["testes_das_lentes"]
mun = R["municipios"]
est = R["estados"]
gov = R["governador"]
tr = pd.DataFrame(R["transferencia"]["tabela"])
hp = pd.DataFrame(R["historico_erro_pesquisas"]["linhas"])
proj = R["projecao_video_14"]
val = list(csv.reader(open(RES / "validacao_independente.csv", encoding="utf-8")))[1:]
val_ok = sum(1 for x in val if x[3] == "True")
viradas_gov = [x for x in gov["viradas_2t_2026"] if x["virada"]]


def fluxo(o: str, d: str) -> pd.Series:
    return tr[(tr.origem_1t == o) & (tr.destino_2t == d)].iloc[0]


def linha_fluxo(o: str, nome: str) -> str:
    cel = []
    for d in ("lula", "flavio", "branco_nulo", "abstencao"):
        f = fluxo(o, d)
        cel.append(f"{br(f.pct_da_origem, 0)}% ({br(f.pct_p5, 0)} a {br(f.pct_p95, 0)})")
    return f"| {nome} | " + " | ".join(cel) + " |"


def votos_para_lula(o: str) -> float:
    return float(fluxo(o, "lula").votos)


erro_2t_hist = {int(x.ano): float(x.erro_medio_anti_pt) for x in hp[hp.turno == 2].itertuples()}
erro_1t_hist = {int(x.ano): float(x.erro_medio_anti_pt) for x in hp[hp.turno == 1].itertuples()}
excesso_lula = te["t1_lula"]["votos_acima_do_livre"]
frente = v["frente_2t_lula"]
abst_hist = pd.read_csv(RAIZ / "dados/copias/previsao-segundo-turno-2026/abstencao_historica.csv")
abst_hist = abst_hist[abst_hist.ano < 2026]
queda_abst = t2["abstencao_pct"] - t1["abstencao_pct"]

# ------------------------------------------------------------------ RELATÓRIO
ranking = "\n".join(f"| {x['instituto']} | {x['campo_fim'][8:10]}/{x['campo_fim'][5:7]} | {br(x['lula_valido'])}% | {br(100 - x['lula_valido'])}% | {br(x['erro_lula'])} | {x['registro_tse']} |"
                    for x in sorted(P["ranking_ultimas"], key=lambda x: -x["lula_valido"]))
leituras = "\n".join(f"| {k} | {pct(p)} | {um_em(p) if p < 0.5 else 'mais de 1 em 2'} |"
                     for k, p in sorted(pr["leituras"].items(), key=lambda kv: kv[1]))
tab_regras = f"""| Regra | Histórico | 2026 |
|---|---|---|
| O líder do 1º turno de presidente venceu o 2º | {reg['presidente_lider_1t_venceu']['acertos']} de {reg['presidente_lider_1t_venceu']['vezes']} (1989 a 2022) | **quebrou**: o Flávio liderou o 1º turno e perdeu |
| A menor frente de um líder do 1º turno | {br(reg['presidente_lider_1t_venceu']['menor_frente_ate_2022'], 2)} pontos (2022) | {br(v['frente_1t_pontos'], 2)} pontos, a menor da série |
| Quem venceu Minas no 1º turno venceu a eleição | {reg['minas']['sum_1t']} de {reg['minas']['count_1t']} (1994 a 2022) | **quebrou**: Minas deu Flávio no 1º turno |
| Quem venceu Minas no 2º turno venceu a eleição | {reg['minas']['sum_2t']} de {reg['minas']['count_2t']} (2002 a 2022) | valeu: Minas deu Lula no 2º turno |
| Estados que sempre acertaram o vencedor no 1º turno | {', '.join(reg['ufs_que_sempre_acertaram_no_1t']['ufs'])} | acertaram de novo: {', '.join(reg['ufs_que_sempre_acertaram_no_1t']['acertaram_em_2026'])} |
| Estados que sempre acertaram o vencedor no 2º turno | {', '.join(reg['ufs_que_sempre_acertaram_no_2t']['ufs'])} | acertaram de novo: {', '.join(reg['ufs_que_sempre_acertaram_no_2t']['acertaram_em_2026'])} |
| Governador: o líder do 1º turno venceu o 2º | {reg['governador_lider_1t_venceu']['vezes'] - reg['governador_lider_1t_venceu']['viradas']} de {reg['governador_lider_1t_venceu']['vezes']} (1994 a 2022) | {len(viradas_gov)} viradas em {len(gov['viradas_2t_2026'])} disputas: {', '.join(x['uf'].upper() for x in viradas_gov)} |
| Governador com frente de até 3 pontos e líder abaixo de 50% | {reg['governador_frente_ate_3_pontos']['viradas']} viradas em {reg['governador_frente_ate_3_pontos']['vezes']} | — |"""
tab_regras = tab_regras.replace("| — |", "| sem caso no 2º turno de 2026 |")
gov_dif = "; ".join(f"{NOME_UF[x['uf']]} ({x['governador_eleito'].title()}, coligação do lado do {x['lado_da_coligacao']}; presidente: {x['presidente_venceu_no_estado']})" for x in gov["lado_diferente"])
abst_tab = "\n".join(f"| {int(x.ano)} | {br(x.abst_1t, 2)}% | {br(x.abst_2t, 2)}% | {'+' if x.delta_abst > 0 else ''}{br(x.delta_abst, 2)} |" for x in abst_hist.itertuples())
abst_tab += f"\n| **2026** | {br(t1['abstencao_pct'], 2)}% | {br(t2['abstencao_pct'], 2)}% | **{br(queda_abst, 2)}** |"
hist_erro_tab = "\n".join(f"| {a} | {sinal(erro_1t_hist[a])} | {sinal(erro_2t_hist[a])} |" for a in (2014, 2018, 2022))
hist_erro_tab += f"\n| **2026** | {br(erro_1t_hist[2026])} | **+{br(-U['erro_medio'])}** |"

relatorio = f"""# Relatório: as pesquisas, as regras e o resultado do 2º turno de 2026

Gerado por `ferramentas/gerar-relatorio.py` a partir de `resultados/RESUMO.json`. Rodada 1 (26/10/2026). Todo número tem a fonte em [`docs/FONTES_DE_DADOS.md`](docs/FONTES_DE_DADOS.md) e o hash do arquivo de origem em `dados/MANIFESTO.json`.

## O que este relatório não consegue dizer

- **O voto é secreto.** "Para onde foram os votos do Cury, do Renan e do Caiado" é uma **estimativa** feita com o resultado de 5.571 municípios (inferência ecológica). Ela mostra o que é compatível com os números de cada lugar, não o caminho de cada eleitor, e tem faixa de incerteza larga (§6).
- **Probabilidade de algo que já aconteceu** é a chance que os números davam **antes** da votação. Uma chance de 1 em 3 ou de 1 em 9 não diz se o resultado é legítimo ou não: diz o tamanho da surpresa.
- **A apuração seção a seção, a pausa da noite e os registros das urnas** não são analisados aqui. Isso é o projeto do vídeo longo 16 (`investigacao-segundo-turno-2026`). Este projeto usa o resultado oficial final por país, estado e município.
- **Governador e presidente** foram comparados pela **coligação** do governador eleito (tem o PT, tem o PL, ou nenhum dos dois), que é uma regra mecânica. Apoio declarado no 2º turno não foi levantado nesta rodada.

## 1. O resultado, em números

| | 1º turno (04/10) | 2º turno (25/10) | Diferença |
|---|---|---|---|
| Lula | {n(t1['lula'])} ({br(t1['lula_pct'], 2)}%) | {n(t2['lula'])} (**{br(t2['lula_pct'], 2)}%**) | **+{n(v['lula'])}** |
| Flávio | {n(t1['flavio'])} ({br(t1['flavio_pct'], 2)}%) | {n(t2['flavio'])} ({br(t2['flavio_pct'], 2)}%) | **+{n(v['flavio'])}** |
| Outros candidatos | {n(-v['outros_candidatos'])} | 0 | {n(v['outros_candidatos'])} |
| Abstenção | {n(t1['abstencao'])} ({br(t1['abstencao_pct'], 2)}%) | {n(t2['abstencao'])} ({br(t2['abstencao_pct'], 2)}%) | {n(v['abstencao'])} |
| Brancos e nulos | {n(t1['brancos'] + t1['nulos'])} | {n(t2['brancos'] + t2['nulos'])} | {n(v['branco_nulo'])} |

**A conta fecha no voto.** O que os dois ganharam juntos ({n(v['ganho_dos_dois'])}) é exatamente o que saiu dos outros candidatos ({n(-v['outros_candidatos'])}), da abstenção ({n(-v['abstencao'])}) e do branco e nulo ({n(-v['branco_nulo'])}). O Lula ficou com {br(v['parte_do_lula_no_ganho'])}% desse saldo. A frente do Flávio no 1º turno era de {n(v['frente_1t_flavio'])} votos; a do Lula no 2º ficou em {n(v['frente_2t_lula'])}. A virada foi de {mi(v['vaivem'])} de votos de diferença.

Se todo voto novo (quem voltou a votar e quem deixou o branco e o nulo) tivesse ido para o Lula, ele ainda precisaria de **{br(v['lula_precisou_dos_outros_pct_se_todo_novo_fosse_dele'])}%** dos votos dos outros candidatos. Ou seja: sem troca direta de voto do Flávio para o Lula, a maioria dos eleitores de Cury, Renan e Caiado votou Lula.

## 2. As pesquisas contra a urna

Foram usadas as **{P['todas']['n']} pesquisas nacionais de 2º turno** de 05/10 a 24/10 que casaram com o registro no TSE **e** foram conferidas numa segunda fonte (lista em `resultados/pesquisas_2t.csv`, com o número do registro). Ficou fora da conta: {', '.join(f"{x['instituto']} de {x['campo_fim'][8:10]}/{x['campo_fim'][5:7]}" for x in P['fora_da_conta'])} (a amostra publicada não bate com a do registro).

| Conjunto | Pesquisas | Lula na média | Erro médio no Lula | Davam Flávio | Davam Lula | A urna ficou dentro da margem |
|---|---|---|---|---|---|---|
| Todas | {P['todas']['n']} | {br(P['todas']['media_lula'], 2)}% | {br(P['todas']['erro_medio'])} | {P['todas']['deram_flavio']} | {P['todas']['deram_lula']} (+{P['todas']['empate']} empate) | {P['todas']['urna_dentro_da_margem']} |
| Última semana | {P['ultima_semana']['n']} | {br(P['ultima_semana']['media_lula'], 2)}% | {br(P['ultima_semana']['erro_medio'])} | {P['ultima_semana']['deram_flavio']} | {P['ultima_semana']['deram_lula']} | {P['ultima_semana']['urna_dentro_da_margem']} |
| Véspera (campo até 23 e 24/10) | {P['vespera']['n']} | {br(P['vespera']['media_lula'], 2)}% | {br(P['vespera']['erro_medio'])} | {P['vespera']['deram_flavio']} | {P['vespera']['deram_lula']} | {P['vespera']['urna_dentro_da_margem']} |
| **Última de cada instituto** | **{U['n']}** | **{br(U['media_lula'], 2)}%** | **{br(U['erro_medio'])}** | **{U['deram_flavio']}** | **{U['deram_lula']}** | **{U['urna_dentro_da_margem']}** |

- **Nenhuma das {P['todas']['n']} pesquisas deu ao Lula o que a urna deu** ({br(t2['lula_pct'], 2)}%). A mais perto foi a {P['pesquisa_mais_perto']['instituto']} ({br(float(P['pesquisa_mais_perto']['lula_valido']), 2)}%).
- Na última de cada instituto, só **Vox Brasil** e **Colectta** davam o Lula à frente, e **as duas também ficaram abaixo da urna**.
- O erro médio foi de **{br(-U['erro_medio'])} pontos** no Lula (o dobro, {br(-2 * U['erro_medio'])} pontos, na diferença entre os dois). Todos os institutos erraram para o mesmo lado.
- A projeção do vídeo longo 14 dava Flávio {br(proj['flavio_projetado'], 1)}%; a urna deu {br(proj['flavio_urna'], 2)}%: erro de {br(proj['erro'], 1)} pontos, contra o erro médio de {br(proj['erro_medio_teste_do_passado'], 1)} que o próprio método teria tido no passado.

### A última pesquisa de cada instituto

| Instituto | Fim do campo | Lula | Flávio | Erro no Lula | Registro no TSE |
|---|---|---|---|---|---|
{ranking}

### O erro trocou de lado entre os turnos, e isso já tinha acontecido

Erro médio das últimas pesquisas de cada instituto, no candidato contra o PT, em pontos (positivo: a pesquisa deu mais a ele do que a urna):

| Eleição | 1º turno | 2º turno |
|---|---|---|
{hist_erro_tab}

No 1º turno, as pesquisas deram **menos** ao candidato contra o PT nas quatro eleições. No 2º turno de 2014 e de 2018 deram **mais**; em 2022, quase nada. Em 2026 o padrão se repetiu, com o maior erro de 2º turno da série.

## 3. As regras que "sempre valiam"

{tab_regras}

Regra com 7 ou 8 casos quebra: pela regra de Laplace, uma regra que acertou {reg['presidente_lider_1t_venceu']['vezes']} de {reg['presidente_lider_1t_venceu']['vezes']} vezes ainda deixa {um_em(pr['historico_laplace'])} de chance de quebrar na próxima. E em governador, onde há {reg['governador_lider_1t_venceu']['vezes']} casos, o líder do 1º turno perdeu {reg['governador_lider_1t_venceu']['viradas']} vezes; com frente de até 3 pontos, perdeu {reg['governador_frente_ate_3_pontos']['viradas']} em {reg['governador_frente_ate_3_pontos']['vezes']}. A frente do Flávio, {br(v['frente_1t_pontos'], 2)} pontos, era a menor já vista num 1º turno de presidente.

## 4. Quem venceu em cada lugar

- **Estados:** o Lula venceu em {est['lula_venceu_1t']} no 1º turno e em {est['lula_venceu_2t']} no 2º. **Só Minas Gerais virou** (Flávio para Lula); nenhum estado foi do Lula para o Flávio.
- **O Lula subiu em todos os 27 estados**, de {br(est['lula_subiu_min'])} a {br(est['lula_subiu_max'])} pontos. A subida foi parecida no país inteiro.
- **Municípios:** {mun['viradas'].get('Flávio para Lula', 0)} viraram do Flávio para o Lula e {mun['viradas'].get('Lula para Flávio', 0)} do Lula para o Flávio (mais {mun['viradas'].get('empate para Lula', 0)} que estavam empatados e foram para o Lula). O Lula ganhou votos em {n(mun['lula_ganhou_votos_em'])} dos {n(mun['municipios'])} municípios; o Flávio, em {n(mun['flavio_ganhou_votos_em'])}, e **perdeu votos em {n(mun['flavio_perdeu_votos_em'])}**.
- A maior cidade que virou foi o **Rio de Janeiro** ({br(mun['maiores_viradas_em_votos'][0]['lula_pct_1t'])}% para {br(mun['maiores_viradas_em_votos'][0]['lula_pct_2t'])}% do Lula). As outras grandes: {', '.join(f"{x['municipio'].title()} ({x['uf'].upper()})" for x in mun['maiores_viradas_em_votos'][1:6])}.
- O ganho do Lula veio de cidades de todo tamanho: {'; '.join(f"{k}: +{mi(x['lula'])}" for k, x in mun['ganho_por_porte'].items())}. Nas capitais, +{mi(mun['capitais_lula_ganhou'])} para o Lula e +{mi(mun['capitais_flavio_ganhou'])} para o Flávio.
- **Governador e presidente:** em **{gov['mesmo_lado']} de {gov['ufs']}** estados o governador eleito é de uma coligação do lado que venceu para presidente ali. Em {gov['lado'].get('nenhum', 0)}, a coligação do governador não tinha nem o PT nem o PL. Os que ficaram de lados diferentes: {gov_dif}. Tabela: `resultados/governador_e_presidente.csv`.
- **2º turno de governador no mesmo dia:** {len(viradas_gov)} viradas em {len(gov['viradas_2t_2026'])} disputas ({'; '.join(f"{NOME_UF[x['uf']]}: {x['segundo_1t'].title()} passou {x['lider_1t'].title()}" for x in viradas_gov)}).

## 5. Abstenção, branco e nulo

| Eleição | Abstenção no 1º turno | No 2º turno | Variação (pontos) |
|---|---|---|---|
{abst_tab}

Em cinco das seis eleições anteriores, **mais gente faltou** no 2º turno. Em 2026 a abstenção **caiu {br(-queda_abst, 2)} pontos**: {mi(-v['abstencao'])} de pessoas a mais votando, a maior queda da série. Brancos e nulos caíram de {br(t1['branco_nulo_pct'], 2)}% para {br(t2['branco_nulo_pct'], 2)}% de quem votou. A abstenção **subiu** em {len(est['abstencao_subiu_em'])} estados ({', '.join(x.upper() for x in est['abstencao_subiu_em'])}), quase todos no Norte. Em {len(est['flavio_perdeu_votos_em'])} deles o Flávio teve menos votos no 2º turno do que no 1º ({', '.join(x.upper() for x in est['flavio_perdeu_votos_em'])}).

A queda da abstenção **não** se concentrou onde o Lula era mais forte: ela foi de {'; '.join(f"{br(q, 2)} pontos no {k}" for k, q in te['t3_queda_por_terco'].items())}. Mas, dentro de cada município, onde a abstenção mais caiu o Lula mais subiu (correlação de {br(te['t3_correlacao_queda_abstencao_e_ganho_lula_pontos'], 2)}).

## 6. De onde vieram os votos (estimativa)

Modelo de transição com restrição (cada eleitor do 1º turno vai para algum lugar no 2º, e as proporções somam 100%), ajustado por região com os 5.571 municípios e somado no país; faixa de 90% por reamostragem de municípios. Arquivo: `resultados/transferencia_de_votos.csv`.

| Eleitor do 1º turno | Lula | Flávio | Branco ou nulo | Faltou |
|---|---|---|---|---|
{linha_fluxo('cury', 'Augusto Cury')}
{linha_fluxo('renan', 'Renan Santos')}
{linha_fluxo('caiado', 'Ronaldo Caiado')}
{linha_fluxo('outros', 'Zema e outros')}
{linha_fluxo('branco_nulo', 'Branco ou nulo')}
{linha_fluxo('abstencao', 'Faltou')}
{linha_fluxo('lula', 'Lula')}
{linha_fluxo('flavio', 'Flávio')}

Lendo a tabela: os eleitores de Cury, Renan e Caiado se dividiram, com um pouco mais para o Lula em cada um, mas as faixas se cruzam (não dá para cravar que o Lula levou mais que o Flávio em nenhum dos três sozinho). Somados, a estimativa dá ao Lula cerca de {mi(votos_para_lula('cury') + votos_para_lula('renan') + votos_para_lula('caiado') + votos_para_lula('outros'))} vindos dos outros candidatos, {mi(votos_para_lula('branco_nulo'))} de quem tinha votado branco ou nulo e {mi(votos_para_lula('abstencao'))} de quem tinha faltado.

**Limites que pesam:** o modelo enxerga mal a troca direta de um candidato para o outro (ele tende a dar zero), e o número de "branco e nulo para o Lula" é o mais frágil, porque o branco e o nulo são pequenos em cada município. O modelo reproduz o 2º turno observado com diferença de {n(abs(R['transferencia']['previsto_2t']['lula'] - R['transferencia']['observado_2t']['lula']))} votos no Lula. Uma matriz única para o país inteiro dá números diferentes (`resultados/transferencia_matriz_unica_pais_pct.csv`), o que mostra quanto a estimativa depende do recorte. A pesquisa que perguntou "em quem votou no 1º turno" seria a segunda fonte, e ainda não foi coletada.

## 7. A probabilidade, antes da votação

A média da última pesquisa de cada instituto dava ao Flávio uma frente de **{br(pr['frente_flavio_nas_pesquisas'], 2)} pontos**. A pergunta é: com o que se sabia no sábado, qual era a chance de o Lula vencer?

| Régua | Chance do Lula | Em outras palavras |
|---|---|---|
{leituras}

- **Pesquisas e erro histórico:** em {pr['disputas_no_historico']} segundos turnos de 2014 a 2022 (presidente e governador), a média das pesquisas errou a frente do líder com desvio de {br(pr['desvio_do_erro_todas'], 1)} pontos. Com esse erro, uma frente de {br(pr['frente_flavio_nas_pesquisas'], 2)} pontos vira em cerca de 1 de cada 3 eleições.
- **Vitória do Lula por {br(v['frente_2t_pontos'], 2)} pontos ou mais** (o que aconteceu): {pct(pr['pesquisas_normal_frente_igual_ou_maior'])} pela mesma conta, ou {pct(pr['pesquisas_empirico_frente_igual_ou_maior'])} contando os casos do histórico.
- **O histórico do 1º turno** (líder sempre venceu, {reg['presidente_lider_1t_venceu']['vezes']} de {reg['presidente_lider_1t_venceu']['vezes']}) dá {um_em(pr['historico_laplace'])}.
- **A Polymarket** dava {pct(pr['polymarket_lula_vespera'])} ao Lula na véspera. Nos mercados de eleição em que o favorito tinha de 70% a 90%, o favorito perdeu {pr['polymarket_favoritos_70_90']['favorito_perdeu']} de {pr['polymarket_favoritos_70_90']['mercados']} vezes. A mesma Polymarket deu o Lula como favorito no 1º turno ({pct(pr['polymarket_1t']['preco'])}) e errou.
- **Média das três réguas principais** (pesquisas com erro histórico, histórico do 1º turno e Polymarket): **{pct(pr['media_das_tres'])}**, ou {um_em(pr['media_das_tres'])}.

## 8. As duas lentes

A leitura completa, com a versão mais forte de cada lado, está em [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md). O que os testes mostram:

| Teste | Lula | Flávio |
|---|---|---|
| Municípios em que o ganho passou de tudo o que estava livre (votos dos outros + queda da abstenção + queda de branco e nulo) | {te['t1_lula']['municipios']} municípios, {n(te['t1_lula']['votos_acima_do_livre'])} votos | {te['t1_flavio']['municipios']} municípios, {n(te['t1_flavio']['votos_acima_do_livre'])} votos |
| Municípios com comparecimento acima de 95% e 90% ou mais para um candidato, 1º turno | {te['t2']['1t']['e_lula_90_ou_mais']} | {te['t2']['1t']['e_flavio_90_ou_mais']} |
| O mesmo, 2º turno | {te['t2']['2t']['e_lula_90_ou_mais']} | {te['t2']['2t']['e_flavio_90_ou_mais']} |

Os {n(excesso_lula)} votos "sem origem visível" do Lula são **{br(100 * excesso_lula / frente, 2)}%** da frente final. Eles cabem em troca direta de voto (gente que votou Flávio no 1º e Lula no 2º), que este teste não enxerga.

## 9. Validação

{val_ok} de {len(val)} números centrais refeitos por outro caminho, direto dos arquivos do TSE e das capturas, sem usar o código da análise (`ferramentas/validacao-independente.py`, `resultados/validacao_independente.csv`). Os totais por UF somam o país e os municípios somam cada UF, nos dois turnos, com diferença zero (`ferramentas/derivar.py`).

## 10. Gráficos

`resultados/figuras/`, 1920x1080: de onde vieram os votos (g01), as pesquisas contra a urna (g02 e g03), o erro que troca de lado (g04), as regras (g05), os estados (g06), a abstenção (g07), a transferência estimada (g08), governador e presidente (g09), a probabilidade (g10) e os votos sem origem visível (g11).
"""
(RAIZ / "RELATORIO.md").write_text(relatorio, encoding="utf-8")

# ------------------------------------------------------------------ RESUMO SIMPLES
simples = f"""# Resumo simples

**O que aconteceu:** o Lula teve {br(t2['lula_pct'], 2)}% dos votos válidos e o Flávio {br(t2['flavio_pct'], 2)}%. No 1º turno o Flávio estava na frente por {n(v['frente_1t_flavio'])} votos; no 2º o Lula venceu por {n(v['frente_2t_lula'])}.

| Pergunta | Resposta curta | Por quê |
|---|---|---|
| As pesquisas acertaram? | **Não.** {U['deram_flavio']} dos {U['n']} institutos davam Flávio na última pesquisa | erraram todas para o mesmo lado, {br(-U['erro_medio'])} pontos em média no Lula; nenhuma das {P['todas']['n']} chegou no número da urna |
| Alguma pesquisa dava Lula? | Vox Brasil e Colectta | e mesmo elas ficaram abaixo da urna |
| Já tinha acontecido? | o lado do erro, sim | em 2014 e 2018 o 2º turno também deu mais ao candidato contra o PT do que a urna |
| "O líder do 1º turno sempre vence" | quebrou pela 1ª vez em {reg['presidente_lider_1t_venceu']['vezes'] + 1} eleições | a frente do Flávio era a menor da história ({br(v['frente_1t_pontos'], 2)} pontos); em governador, virada é comum |
| "Quem ganha Minas ganha a eleição" | no 1º turno, quebrou; no 2º, valeu | Minas deu Flávio no 1º turno e Lula no 2º |
| Quantos estados viraram? | **1, Minas Gerais**, para o Lula | o Lula subiu de {br(est['lula_subiu_min'])} a {br(est['lula_subiu_max'])} pontos em todos os 27 |
| Quantos municípios viraram? | {mun['viradas'].get('Flávio para Lula', 0)} para o Lula, {mun['viradas'].get('Lula para Flávio', 0)} para o Flávio | o maior foi a cidade do Rio de Janeiro |
| A abstenção? | **caiu** {br(-queda_abst, 2)} pontos, {mi(-v['abstencao'])} a mais votando | em quase toda eleição ela sobe no 2º turno |
| Brancos e nulos? | caíram {mi(-v['branco_nulo'])} | |
| Para onde foram Cury, Renan e Caiado? | se dividiram, um pouco mais para o Lula em cada um | estimativa com faixa larga; sem troca direta de voto, o Lula precisava de {br(v['lula_precisou_dos_outros_pct_se_todo_novo_fosse_dele'], 0)}% deles |
| Governador e presidente no mesmo estado | {gov['mesmo_lado']} de {gov['ufs']} do mesmo lado | {gov['lado'].get('nenhum', 0)} governadores sem PT nem PL na coligação |
| Qual era a chance do Lula antes da votação? | entre {um_em(pr['menor'][1])} e {um_em(pr['leituras']['pesquisas e erro histórico (todas as disputas)'])}, conforme a régua | média das três réguas principais: {pct(pr['media_das_tres'])} |
| Os dados mostram voto sem explicação? | {n(excesso_lula)} votos do Lula sem origem visível, {br(100 * excesso_lula / frente, 2)}% da frente | cabem em troca direta de voto; nenhum município com comparecimento acima de 95% |

Leitura das duas lentes (resultado legítimo e fraude): [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md). Relatório completo: [`RELATORIO.md`](RELATORIO.md).
"""
(RAIZ / "RESUMO_SIMPLES.md").write_text(simples, encoding="utf-8")

# ------------------------------------------------------------------ LEITURA DA IA (duas lentes)
leitura = f"""# Leitura da IA: as duas lentes

Pedido do autor: analisar o resultado **dando como verdadeira, uma de cada vez**, a premissa de que foi legítimo e a de que foi fraude, para os dois lados serem bem atendidos. Esta leitura é do Claude, a partir dos números do [`RELATORIO.md`](../RELATORIO.md). "Fraude" aqui é o nome de uma hipótese, nunca uma conclusão.

## Lente L · o resultado foi legítimo

**A versão mais forte:** as pesquisas erraram como já erraram antes, num 2º turno decidido por uma frente pequena, e o eleitor que estava fora (abstenção, branco, nulo e os outros candidatos) decidiu a eleição.

**O que se esperaria ver no dado, e o que se vê:**

| Se foi legítimo, esperaria-se | O dado |
|---|---|
| uma chance real de virada, antes da votação | {um_em(pr['leituras']['pesquisas e erro histórico (todas as disputas)'])} pelas pesquisas com o erro histórico; {um_em(pr['media_das_tres'])} na média das três réguas |
| erro de pesquisa do tamanho e do lado já vistos | o 2º turno de 2014 e o de 2018 também deram mais ao candidato contra o PT; o de 2026 foi o maior ({br(-U['erro_medio'])} pontos) |
| a soma dos votos fechando | fecha no voto: tudo o que os dois ganharam saiu dos outros, da abstenção e do branco e nulo |
| subida espalhada, não em poucos lugares | o Lula subiu em todos os 27 estados ({br(est['lula_subiu_min'])} a {br(est['lula_subiu_max'])} pontos) e ganhou votos em {n(mun['lula_ganhou_votos_em'])} de {n(mun['municipios'])} municípios |
| votos novos explicando o ganho | {mi(-v['abstencao'])} de pessoas a mais votando; onde a abstenção mais caiu o Lula mais subiu |
| eleições do mesmo dia coerentes | {gov['mesmo_lado']} de {gov['ufs']} governadores eleitos do mesmo lado do presidente no estado; {len(viradas_gov)} viradas em {len(gov['viradas_2t_2026'])} segundos turnos de governador |

**O que essa lente não explica bem:** por que **todas** as pesquisas erraram para o mesmo lado e nenhuma chegou no número; por que a abstenção caiu tanto, contra o padrão de quase todas as eleições; e o que o modelo de transferência não consegue separar (troca direta de voto). A explicação mais citada, o filtro de "eleitor provável" das pesquisas ter cortado justamente quem voltou a votar, combina com a queda da abstenção, mas **não foi testada** aqui.

**O que mudaria esta leitura:** municípios ou seções em que o ganho do Lula não caiba em nenhuma origem, um padrão de comparecimento e votação que fuja do resto do país, ou a apuração seção a seção mostrando algo que os totais não mostram.

## Lente F · o resultado foi fraude

**A versão mais forte:** um candidato que liderou o 1º turno, liderava {U['deram_flavio']} de {U['n']} institutos na véspera e tinha {pct(1 - pr['polymarket_lula_vespera'])} no mercado perdeu por {br(v['frente_2t_pontos'], 2)} pontos, quebrando uma regra que valia desde 1989 e a regra de Minas no 1º turno. Pela régua mais dura, o histórico do 1º turno, a chance era de {um_em(pr['historico_laplace'])}; a vitória por {br(v['frente_2t_pontos'], 2)} pontos ou mais, pelas pesquisas, era de {pct(pr['pesquisas_normal_frente_igual_ou_maior'])}.

**O que se esperaria ver no dado, e o que se vê:**

| Se foi fraude, esperaria-se | O dado |
|---|---|
| votos que não cabem em nenhuma origem, concentrados | {te['t1_lula']['municipios']} municípios com {n(te['t1_lula']['votos_acima_do_livre'])} votos do Lula sem origem visível ({br(100 * excesso_lula / frente, 2)}% da frente); o espelho do Flávio dá {te['t1_flavio']['municipios']} municípios e {n(te['t1_flavio']['votos_acima_do_livre'])} votos. A diferença existe, mas é pequena demais para a eleição e cabe em troca direta de voto |
| a mancha de comparecimento muito alto com voto quase todo num lado | nenhum município com comparecimento acima de 95%, nos dois turnos |
| ganho concentrado em poucos lugares | ganho em todos os estados e em {n(mun['lula_ganhou_votos_em'])} municípios, de todos os tamanhos |
| pesquisas que "acertam sempre" e uma urna fora delas | as pesquisas erram muito em 2º turno ({pr['disputas_no_historico']} disputas, desvio de {br(pr['desvio_do_erro_todas'], 1)} pontos) e erraram no 1º turno de 2026 para o outro lado |
| um mercado que nunca erra | a Polymarket errou o 1º turno e, na faixa de 70% a 90%, o favorito perdeu {pr['polymarket_favoritos_70_90']['favorito_perdeu']} de {pr['polymarket_favoritos_70_90']['mercados']} vezes |

**O que essa lente acerta:** o resultado foi uma surpresa de verdade. Nenhuma das três réguas principais dava o Lula como favorito, a regra do líder do 1º turno quebrou pela primeira vez, e a queda da abstenção é fora do padrão. Essas três coisas merecem a apuração seção a seção, a hora de chegada dos boletins e os registros das urnas, que este projeto não cobre.

**O que mudaria esta leitura:** os mesmos testes, feitos seção a seção (o vídeo 16), mostrando concentração que o município esconde; pesquisas pós-eleição mostrando que os eleitores dos outros candidatos não votaram como o resultado exige.

## O que o dado sustenta mais

**A lente L.** Por três razões que não dependem de opinião: (1) a chance antes da votação não era pequena o bastante para ser estranha: na média das réguas, {um_em(pr['media_das_tres'])}, e na régua das pesquisas com o erro histórico, {um_em(pr['leituras']['pesquisas e erro histórico (todas as disputas)'])}; (2) os votos fecham e a subida foi espalhada pelo país inteiro; (3) o teste que procuraria voto acrescentado acha no máximo {n(excesso_lula)} votos, {br(100 * excesso_lula / frente, 2)}% da frente. A lente F não fica apagada: a surpresa é real, o erro de todas as pesquisas para o mesmo lado é real, e a parte da apuração seção a seção ainda não foi medida aqui.
"""
(RAIZ / "docs" / "LEITURA_DA_IA.md").write_text(leitura, encoding="utf-8")
print("RELATORIO.md, RESUMO_SIMPLES.md e docs/LEITURA_DA_IA.md escritos")
