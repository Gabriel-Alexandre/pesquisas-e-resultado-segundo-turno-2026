"""Caminhos, listas e utilidades usados em todo o projeto."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
BRUTOS = DADOS / "brutos"
DERIV = DADOS / "derivados"
COPIAS = DADOS / "copias"
CAPTURAS = BRUTOS / "capturas"
RES = RAIZ / "resultados"
FIG = RES / "figuras"
MANIFESTO = DADOS / "MANIFESTO.json"

BASE_TSE = "https://resultados.tse.jus.br/oficial/ele2026"
PRES_1T, PRES_2T = "6257", "6258"
GOV_1T, GOV_2T = "6259", "6260"
UFS_GOV_2T = ["ac", "am", "df", "es", "rn", "to"]
LULA, FLAVIO = "13", "22"
REPO = "github.com/Gabriel-Alexandre/pesquisas-e-resultado-segundo-turno-2026"

REGIAO = {
    "ac": "Norte", "am": "Norte", "ap": "Norte", "pa": "Norte", "ro": "Norte", "rr": "Norte", "to": "Norte",
    "al": "Nordeste", "ba": "Nordeste", "ce": "Nordeste", "ma": "Nordeste", "pb": "Nordeste", "pe": "Nordeste",
    "pi": "Nordeste", "rn": "Nordeste", "se": "Nordeste",
    "df": "Centro-Oeste", "go": "Centro-Oeste", "ms": "Centro-Oeste", "mt": "Centro-Oeste",
    "es": "Sudeste", "mg": "Sudeste", "rj": "Sudeste", "sp": "Sudeste",
    "pr": "Sul", "rs": "Sul", "sc": "Sul",
    "zz": "Exterior",
}
UFS = [u for u in REGIAO if u != "zz"]

# cores iguais em todos os projetos do canal
COR = {"lula": "#C8553D", "flavio": "#2D6A8A", "base": "#6B6B6B", "outros": "#B8A16B"}


def sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def _ler_manifesto() -> dict:
    if MANIFESTO.exists():
        return json.loads(MANIFESTO.read_text(encoding="utf-8"))
    return {"arquivos": {}}


def registrar_arquivo(caminho: Path, origem: str, nota: str = "") -> None:
    """Grava no manifesto: origem, hora, tamanho e sha256 de um arquivo (o caminho relativo à raiz é a chave)."""
    m = _ler_manifesto()
    rel = caminho.resolve().relative_to(RAIZ).as_posix()
    m["arquivos"][rel] = {"origem": origem, "hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                          "bytes": caminho.stat().st_size, "sha256": sha256(caminho), "nota": nota}
    MANIFESTO.write_text(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")


def registrar_lote(itens: list[tuple[Path, str, str]]) -> None:
    """Como registrar_arquivo, para muitos arquivos de uma vez (lê e escreve o manifesto uma vez só)."""
    m = _ler_manifesto()
    agora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for caminho, origem, nota in itens:
        rel = caminho.resolve().relative_to(RAIZ).as_posix()
        m["arquivos"][rel] = {"origem": origem, "hora": agora, "bytes": caminho.stat().st_size,
                              "sha256": sha256(caminho), "nota": nota}
    MANIFESTO.write_text(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")


def num(x) -> float:
    return float(str(x).replace(",", ".")) if x not in (None, "") else 0.0


def ler_json(caminho: Path) -> dict:
    b = caminho.read_bytes()
    try:
        return json.loads(b.decode("utf-8"))
    except UnicodeDecodeError:
        return json.loads(b.decode("latin-1"))


def salvar_json(obj, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
