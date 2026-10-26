"""Captura da Wikipedia (en) as tabelas de pesquisas do 2º turno (outubro, depois do 1º turno) e do 1º turno (reta final).

A Wikipedia é a primeira fonte. Cada pesquisa do 2º turno é casada depois com o registro do TSE
(ferramentas/casar-registro-tse.py) e conferida numa segunda fonte (ferramentas/conferir-pesquisas.py).
Saída: dados/brutos/capturas/wikipedia-*.wikitext e dados/derivados/pesquisas_2t_wikipedia.csv, pesquisas_1t_wikipedia.csv
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analise.comum import CAPTURAS, DERIV, registrar_arquivo  # noqa: E402

PAGINA = "Opinion_polling_for_the_2026_Brazilian_presidential_election"
API = "https://en.wikipedia.org/w/api.php"
H = {"User-Agent": "pesquisas-e-resultado-segundo-turno-2026 (pesquisa aberta)"}
MESES = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10}


def secao(titulo_comeca: str, nivel_pai: str) -> tuple[str, int]:
    j = requests.get(API, params={"action": "parse", "page": PAGINA, "prop": "sections|revid", "format": "json"},
                     headers=H, timeout=60).json()["parse"]
    dentro = False
    for s in j["sections"]:
        if s["level"] == "2":
            dentro = s["line"] == nivel_pai
        if dentro and s["line"].startswith(titulo_comeca):
            idx = s["index"]
            break
    t = requests.get(API, params={"action": "parse", "page": PAGINA, "prop": "wikitext", "section": idx, "format": "json"},
                     headers=H, timeout=60).json()["parse"]["wikitext"]["*"]
    return t, j["revid"]


def limpar(c: str) -> str:
    c = re.sub(r"<ref[^>]*>.*?</ref>|<ref[^>]*/>", "", c, flags=re.S)
    c = re.sub(r"^\s*((style|rowspan|colspan|class|data-sort-value)=\"?[^|\"]*\"?\s*)+\|", "", c.strip())
    c = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", c)
    c = re.sub(r"\{\{[^}]*\}\}", "", c)
    return c.replace("'", "").strip()


def numero(c: str):
    c = limpar(c).replace(",", "")
    m = re.search(r"-?\d+(\.\d+)?", c)
    return float(m.group()) if m else None


def periodo(c: str):
    c = limpar(c)
    m = re.match(r"(\d+)\s*(\w{3})?\D+(\d+)\s*(\w{3})", c) or re.match(r"(\d+)()\s*()(\w{3})", c)
    if not m:
        return None, None
    mes_fim = MESES.get(m.group(4)[:3])
    mes_ini = MESES.get((m.group(2) or m.group(4))[:3]) or mes_fim
    ini = int(m.group(1))
    fim = int(m.group(3) or m.group(1))
    return f"2026-{mes_ini:02d}-{ini:02d}", f"2026-{mes_fim:02d}-{fim:02d}"


def blocos(texto: str):
    for bloco in texto.split("\n|-")[1:]:
        cel = [c for c in re.split(r"\n\||\|\|", bloco) if c.strip() and not c.strip().startswith("}")]
        yield bloco, cel


def main() -> None:
    CAPTURAS.mkdir(parents=True, exist_ok=True)
    texto, revid = secao("October (after", "Second round")
    cap = CAPTURAS / "wikipedia-2t-outubro.wikitext"
    cap.write_text(texto, encoding="utf-8")
    registrar_arquivo(cap, f"https://en.wikipedia.org/wiki/{PAGINA} (2º turno, outubro, revid {revid})", f"revid {revid}")
    linhas = []
    for bloco, cel in blocos(texto):
        if len(cel) < 9 or "colspan" in bloco.split("\n")[1]:
            continue
        url = re.search(r"https?://[^\s\]|}<]+", bloco)
        ini, fim = periodo(cel[1])
        linhas.append({"instituto": limpar(cel[0]), "campo_ini": ini, "campo_fim": fim, "lula_total": numero(cel[2]),
                       "flavio_total": numero(cel[3]), "bni": numero(cel[4]), "margem_erro": numero(cel[5]),
                       "amostra": numero(cel[6]), "url_wikipedia": url.group() if url else ""})
    df = pd.DataFrame(linhas)
    df["url_wikipedia"] = df.url_wikipedia.str.replace(r"\?utm_source=chatgpt\.com", "", regex=True)
    df["lula_valido_wiki"] = 100 * df.lula_total / (df.flavio_total + df.lula_total)
    out = DERIV / "pesquisas_2t_wikipedia.csv"
    DERIV.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    registrar_arquivo(out, "ferramentas/capturar-pesquisas.py", f"revid {revid}")
    print(df.to_string())


if __name__ == "__main__":
    main()
