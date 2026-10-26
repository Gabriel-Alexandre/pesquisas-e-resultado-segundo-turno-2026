"""Confere, contra a página citada, os números que as pesquisas de apoio (agentes) levantaram.

Para cada linha: baixa a página (Wikipedia pela API, com o revid; outras páginas pelo texto), guarda o texto extraído
em dados/brutos/capturas/agentes/ e procura cada número com as formas comuns (47.03, 47,03, 47.0, 47). A linha entra
na conta só se TODOS os números dela aparecerem na página.
Saídas: dados/derivados/runoffs_conferidos.csv e dados/derivados/erros_pesquisas_conferidos.csv
"""
from __future__ import annotations

import hashlib
import html
import re
import sys
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analise.comum import CAPTURAS, DADOS, DERIV, registrar_arquivo  # noqa: E402

AG = DADOS / "agentes"
CAP = CAPTURAS / "agentes"
UA = {"User-Agent": "pesquisas-e-resultado-segundo-turno-2026 (pesquisa aberta; github.com/Gabriel-Alexandre)"}
_cache: dict[str, str] = {}


def texto(url: str) -> str:
    if url in _cache:
        return _cache[url]
    nome = hashlib.sha1(url.encode()).hexdigest()[:16]
    arq = CAP / f"{nome}.txt"
    if arq.exists():
        _cache[url] = arq.read_text(encoding="utf-8")
        return _cache[url]
    u = urlparse(url)
    t, rev = "", ""
    for tentativa in range(4):
        try:
            if "wikipedia.org" in u.netloc and u.path.startswith("/wiki/"):
                r = requests.get(f"https://{u.netloc}/w/index.php", params={"title": unquote(u.path[6:]), "action": "raw"},
                                 headers=UA, timeout=60)
                t = r.text if r.status_code == 200 else ""
                rev = r.headers.get("x-content-revision", "") or "raw"
            elif url.lower().endswith(".pdf"):
                import io
                import pdfplumber
                r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
                with pdfplumber.open(io.BytesIO(r.content)) as doc:
                    t = " ".join((pg.extract_text() or "") for pg in doc.pages)
            else:
                r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
                c = re.sub(r"<script.*?</script>|<style.*?</style>", " ", r.text, flags=re.S)
                t = html.unescape(re.sub(r"<[^>]+>", " ", c)) if r.status_code == 200 else ""
        except Exception:
            t = ""
        if t:
            break
        time.sleep(3 * (tentativa + 1))
    if t:
        CAP.mkdir(parents=True, exist_ok=True)
        arq.write_text(t, encoding="utf-8")
        registrar_arquivo(arq, url, f"texto da fonte citada por pesquisa de apoio; revid {rev}")
        time.sleep(0.3)
    if t:
        _cache[url] = t
    return t


def formas(x: float) -> list[str]:
    s = []
    for casas in (2, 1):
        v = f"{x:.{casas}f}"
        s += [v, v.replace(".", ",")]
        if v.endswith("0"):
            s += [v[:-1], v[:-1].replace(".", ",")]
    if abs(x - round(x)) < 1e-9:
        s.append(str(int(round(x))))
    return list(dict.fromkeys(s))


def achou(t: str, x) -> bool:
    if pd.isna(x):
        return True
    return any(re.search(rf"(?<![\d.,]){re.escape(f)}(?![\d])", t) for f in formas(float(x)))


def conferir(arq: str, cols: list[str], url_col: str, saida: str) -> None:
    p = AG / arq
    if not p.exists():
        print("sem arquivo:", arq)
        return
    d = pd.read_csv(p)
    ok, falta = [], []
    for r in d.itertuples(index=False):
        t = texto(getattr(r, url_col))
        miss = [c for c in cols if not achou(t, getattr(r, c))] if t else ["(página não abriu)"]
        ok.append(not miss)
        falta.append(";".join(miss))
    d["conferida"] = ok
    d["nao_achados"] = falta
    out = DERIV / saida
    d.to_csv(out, index=False)
    registrar_arquivo(out, f"ferramentas/conferir-agentes.py sobre dados/agentes/{arq}")
    print(f"{arq}: {sum(ok)} de {len(d)} linhas conferidas")


def main() -> None:
    conferir("runoffs_internacionais.csv", ["lider_1t_pct", "segundo_1t_pct", "vencedor_2t_pct"], "url_wikipedia", "runoffs_conferidos.csv")
    conferir("erros_pesquisas_runoffs.csv", ["candidato_a_pesquisa", "candidato_b_pesquisa"], "url_fonte", "erros_pesquisas_conferidos.csv")
    conferir("cruzamento_voto_1t.csv", ["pct_lula", "pct_adversario"], "url_fonte", "cruzamento_voto_1t_conferido.csv")


if __name__ == "__main__":
    main()
