"""Confere cada pesquisa do 2º turno em duas frentes: o registro no TSE e uma segunda fonte (a página citada).

1. Registro: registro nacional de presidente (SG_UE = BR) com fim e início de campo a até 1 dia, amostra a até 2% e o nome
   da empresa contendo a chave do instituto (arquivo pesquisa_eleitoral_2026.zip do TSE).
2. Segunda fonte: baixa a página citada, guarda o texto extraído (o HTML bruto fica fora do git) e procura os números:
   os dois totais, ou os dois válidos com uma casa, ou os dois válidos inteiros.
Saída: dados/derivados/pesquisas_2t_conferidas.csv (a lista inteira, com as colunas das duas conferências).
"""
from __future__ import annotations

import hashlib
import html
import io
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analise.comum import BRUTOS, CAPTURAS, DERIV, RAIZ, registrar_arquivo, sha256  # noqa: E402

HTML_BRUTO = CAPTURAS / "html"  # fora do git
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
CHAVES = {"Ideia": ["IDEIA"], "Alfa": ["ALFA"], "Real Time": ["REAL TIME"], "PoderData": ["PODER", "AYA"], "Nexus": ["NEXUS", "FSB"],
          "AtlasIntel": ["ATLAS"], "DataTrends": ["DATATRENDS", "DATA TRENDS"], "Vox Brasil": ["VOX"], "Gerp": ["GERP"],
          "Verita": ["VERITA"], "Futura": ["FUTURA", "100% CIDADES"], "Ipespe": ["IPESPE"], "MDA": ["MDA"], "Datafolha": ["DATAFOLHA", "FOLHA"],
          "Indexa": ["INDEXA"], "Palver": ["PALVER"], "Quaest": ["QUAEST"], "Colectta": ["COLECTTA"], "Instituto França": ["FRANCA"]}
NOMES = {"Veritá": "Verita", "Datatrends": "DataTrends"}


def sem_acento(s: str) -> str:
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()


def registro_tse() -> pd.DataFrame:
    z = zipfile.ZipFile(BRUTOS / "pesquisa_eleitoral_2026.zip")
    nome = next(n for n in z.namelist() if n.endswith("_BR.csv") or n.endswith("_BRASIL.csv"))
    reg = pd.read_csv(z.open(nome), sep=";", encoding="latin-1", dtype=str)
    reg = reg[(reg.SG_UE == "BR") & reg.DS_CARGO.str.contains("Presidente", na=False)].copy()
    reg["ini"] = pd.to_datetime(reg.DT_INICIO_PESQUISA, format="mixed", errors="coerce").dt.normalize()
    reg["fim"] = pd.to_datetime(reg.DT_FIM_PESQUISA, format="mixed", errors="coerce").dt.normalize()
    reg["n"] = pd.to_numeric(reg.QT_ENTREVISTADO, errors="coerce")
    reg["empresa"] = (reg.NM_EMPRESA.fillna("") + " | " + reg.NM_EMPRESA_FANTASIA.fillna("")).map(sem_acento)
    return reg


def _texto_html(conteudo: bytes) -> str:
    t = conteudo.decode("utf-8", errors="ignore")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return re.sub(r"[ \t]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))


def texto_de(url: str) -> tuple[str, Path | None]:
    nome = hashlib.sha1(url.encode()).hexdigest()[:16]
    txt = CAPTURAS / "pesquisas" / f"{nome}.txt"
    pdf = CAPTURAS / "pesquisas" / f"{nome}.pdf"
    if pdf.exists():
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(pdf.read_bytes())) as doc:
                return " ".join((pg.extract_text() or "") for pg in doc.pages), pdf
        except Exception:
            return "", pdf
    if txt.exists():
        return txt.read_text(encoding="utf-8"), txt
    try:
        r = requests.get(url, headers=UA, timeout=40)
    except requests.RequestException:
        return "", None
    if r.status_code != 200 or len(r.content) < 2000:
        return "", None
    txt.parent.mkdir(parents=True, exist_ok=True)
    if url.lower().endswith(".pdf") or r.headers.get("content-type", "").startswith("application/pdf"):
        pdf.write_bytes(r.content)
        registrar_arquivo(pdf, url, "segunda fonte de pesquisa")
        return texto_de(url)
    HTML_BRUTO.mkdir(parents=True, exist_ok=True)
    bruto = HTML_BRUTO / f"{nome}.html"
    bruto.write_bytes(r.content)
    txt.write_text(_texto_html(r.content), encoding="utf-8")
    registrar_arquivo(txt, url, f"texto extraído; HTML bruto (fora do git) sha256 {sha256(bruto)}")
    return txt.read_text(encoding="utf-8"), txt


def formas(x: float, casas: int = 1) -> list[str]:
    s = f"{x:.{casas}f}".replace(".", ",")
    out = [s, s.replace(",", ".")]
    if s.endswith(",0"):
        out.append(s[:-2])
    return out


def achou(texto: str, x: float, casas: int = 1) -> bool:
    return any(re.search(rf"(?<![\d,.]){re.escape(f)}(?![\d])", texto) for f in formas(x, casas))


def main() -> None:
    w = pd.read_csv(DERIV / "pesquisas_2t_wikipedia.csv")
    w = w[w.campo_fim.notna()].copy()
    w["instituto"] = w.instituto.replace(NOMES)
    reg = registro_tse()
    alt_p = DERIV / "pesquisas_2t_fonte_alternativa.csv"
    alt = pd.read_csv(alt_p) if alt_p.exists() else pd.DataFrame(columns=["instituto", "campo_fim", "url"])
    linhas = []
    for r in w.itertuples():
        ini, fim = pd.Timestamp(r.campo_ini), pd.Timestamp(r.campo_fim)
        c = reg[((reg.fim - fim).abs() <= pd.Timedelta(days=1)) & ((reg.ini - ini).abs() <= pd.Timedelta(days=1))
                & ((reg.n - r.amostra).abs() <= 0.02 * r.amostra)]
        chaves = CHAVES.get(r.instituto, [sem_acento(r.instituto)])
        c = c.loc[[any(k in e for k in chaves) for e in c.empresa]] if len(c) else c
        ressalva = ""
        if c.empty:
            # segunda passada: mesma empresa, mesmo fim de campo (1 dia), amostra a até 2%; o início de campo pode divergir
            c2 = reg[((reg.fim - fim).abs() <= pd.Timedelta(days=1)) & ((reg.n - r.amostra).abs() <= 0.02 * r.amostra)]
            c2 = c2.loc[[any(k in e for k in chaves) for e in c2.empresa]] if len(c2) else c2
            if len(c2):
                c, ressalva = c2, "início de campo diferente do registro"
        res = r._asdict()
        res.pop("Index")
        res.update(registro_tse=";".join(c.NR_PROTOCOLO_REGISTRO), empresa_tse=";".join(c.NM_EMPRESA), casou=len(c) > 0, ressalva_registro=ressalva, flavio_valido_publicado=None,
                   conferida=False, como="", url_conferida="", captura="")
        urls = [r.url_wikipedia] + alt[(alt.instituto == r.instituto) & (alt.campo_fim == r.campo_fim)].url.tolist()
        fv = 100 * r.flavio_total / (r.flavio_total + r.lula_total)
        for u in urls:
            if not isinstance(u, str) or not u:
                continue
            t, cap = texto_de(u)
            if not t:
                continue
            if achou(t, r.flavio_total) and achou(t, r.lula_total):
                res.update(conferida=True, como="totais no texto")
            else:
                for d in (0.0, 0.1, -0.1):
                    if achou(t, round(fv + d, 1)) and achou(t, round(100 - fv - d, 1)):
                        res.update(conferida=True, como=f"válidos no texto (arredondamento {d:+.1f})")
                        break
                else:
                    # válidos publicados pelo instituto que não saem dos totais da tabela (Instituto França: totais 45,1 e 43,1,
                    # válidos publicados 51,4 e 48,6); aceito até 0,3 ponto, e o válido publicado passa a ser o usado
                    for d in (0.2, 0.3, -0.2, -0.3):
                        if achou(t, round(fv + d, 1)) and achou(t, round(100 - fv - d, 1)):
                            res.update(conferida=True, como=f"válidos publicados no texto ({d:+.1f} dos totais)", flavio_valido_publicado=round(fv + d, 1))
                            break
                    if res["conferida"]:
                        pass
                    elif achou(t, round(fv), 0) and achou(t, round(100 - fv), 0) and f"{round(fv)}%" in t.replace(" %", "%"):
                        res.update(conferida=True, como="válidos inteiros no texto")
            if res["conferida"]:
                res.update(url_conferida=u, captura=cap.relative_to(RAIZ).as_posix() if cap else "")
                break
        linhas.append(res)
        print(f"{r.instituto:18} {r.campo_fim} registro={len(c)} conferida={res['conferida']} {res['como']}")
    out = DERIV / "pesquisas_2t_conferidas.csv"
    pd.DataFrame(linhas).to_csv(out, index=False)
    registrar_arquivo(out, "ferramentas/conferir-pesquisas.py")


if __name__ == "__main__":
    main()
