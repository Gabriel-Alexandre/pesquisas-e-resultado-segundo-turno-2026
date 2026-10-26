"""Baixa do TSE os arquivos oficiais de resultado que o projeto usa, com hash de cada um no manifesto.

- Presidente, 1º e 2º turno (eleições 6257 e 6258): país, cada UF e exterior.
- Presidente por município, 1º e 2º turno (lista de municípios do próprio TSE, arquivo mun-e00625X-cm.json).
- Governador, 1º turno (6259, as 27 UFs) e 2º turno (6260, as 6 UFs que tiveram).
- O registro de pesquisas eleitorais de 2026 (pesquisa_eleitoral_2026.zip).

Um coletor só, com limite de requisições e espera dobrada em 429 (o TSE devolve 429 acima de ~90 por segundo).
Uso: python ferramentas/coletar.py
"""
from __future__ import annotations

import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analise.comum import (BASE_TSE, BRUTOS, GOV_1T, GOV_2T, PRES_1T, PRES_2T, REGIAO, UFS, UFS_GOV_2T,  # noqa: E402
                           ler_json, registrar_lote)

CAB = {"User-Agent": "pesquisas-e-resultado-segundo-turno-2026 (projeto aberto; github.com/Gabriel-Alexandre)"}
TSE = BRUTOS / "tse"
POR_SEGUNDO = 40.0


class Limite:
    def __init__(self, por_segundo: float):
        self.intervalo = 1.0 / por_segundo
        self.trava = threading.Lock()
        self.proximo = time.monotonic()

    def esperar(self):
        with self.trava:
            agora = time.monotonic()
            if agora < self.proximo:
                time.sleep(self.proximo - agora)
            self.proximo = max(agora, self.proximo) + self.intervalo

    def frear(self):
        with self.trava:
            self.intervalo = min(self.intervalo * 1.5, 1.0)


LIM = Limite(POR_SEGUNDO)
_local = threading.local()


def sessao() -> requests.Session:
    if not hasattr(_local, "s"):
        _local.s = requests.Session()
    return _local.s


def baixar(url: str, destino: Path, refazer: bool = False) -> Path | None:
    if destino.exists() and destino.stat().st_size > 0 and not refazer:
        return destino
    espera = 2.0
    for _ in range(10):
        LIM.esperar()
        try:
            r = sessao().get(url, headers=CAB, timeout=60)
        except requests.RequestException:
            r = None
        if r is not None and r.status_code == 200:
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_bytes(r.content)
            return destino
        if r is not None and r.status_code == 404:
            return None
        if r is not None and r.status_code == 429:
            LIM.frear()
        time.sleep(espera)
        espera = min(espera * 2, 60)
    raise RuntimeError(f"sem resposta: {url}")


def url_abr(ele: str, abr: str, cargo: str = "0001") -> str:
    return f"{BASE_TSE}/{ele}/dados/{abr}/{abr}-c{cargo}-e{int(ele):06d}-u.json"


def url_mun(ele: str, uf: str, mun: str) -> str:
    return f"{BASE_TSE}/{ele}/dados/{uf}/{uf}{mun}-c0001-e{int(ele):06d}-u.json"


def lista_municipios(ele: str) -> list[tuple[str, str]]:
    cfg = TSE / ele / "config" / f"mun-e{int(ele):06d}-cm.json"
    baixar(f"{BASE_TSE}/{ele}/config/mun-e{int(ele):06d}-cm.json", cfg, refazer=True)
    d = ler_json(cfg)
    return [(a["cd"].lower(), m["cd"]) for a in d["abr"] for m in a["mu"]]


def main() -> None:
    tarefas: list[tuple[str, Path, str]] = []
    for ele in (PRES_1T, PRES_2T):
        for abr in ["br"] + list(REGIAO):
            tarefas.append((url_abr(ele, abr), TSE / ele / f"{abr}.json", f"presidente {ele} {abr}"))
    for uf in UFS:
        tarefas.append((url_abr(GOV_1T, uf, "0003"), TSE / GOV_1T / f"{uf}.json", f"governador 1t {uf}"))
    for uf in UFS_GOV_2T:
        tarefas.append((url_abr(GOV_2T, uf, "0003"), TSE / GOV_2T / f"{uf}.json", f"governador 2t {uf}"))
    for ele in (PRES_1T, PRES_2T):
        for uf, mun in lista_municipios(ele):
            tarefas.append((url_mun(ele, uf, mun), TSE / ele / "mun" / uf / f"{mun}.json", f"presidente {ele} mun {uf}{mun}"))
    print(f"{len(tarefas)} arquivos")
    feitos, faltou = [], []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=12) as ex:
        for (url, dest, nota), res in zip(tarefas, ex.map(lambda t: baixar(t[0], t[1]), tarefas)):
            (feitos if res else faltou).append((dest, url, nota) if res else url)
            if len(feitos) % 1000 == 0 and res:
                print(f"  {len(feitos)} em {time.time() - t0:.0f}s")
    zipdest = BRUTOS / "pesquisa_eleitoral_2026.zip"
    baixar("https://cdn.tse.jus.br/estatistica/sead/odsele/pesquisa_eleitoral/pesquisa_eleitoral_2026.zip", zipdest, refazer=True)
    feitos.append((zipdest, "https://cdn.tse.jus.br/estatistica/sead/odsele/pesquisa_eleitoral/pesquisa_eleitoral_2026.zip", "registro de pesquisas"))
    for ele in (PRES_1T, PRES_2T):
        cfg = TSE / ele / "config" / f"mun-e{int(ele):06d}-cm.json"
        feitos.append((cfg, f"{BASE_TSE}/{ele}/config/mun-e{int(ele):06d}-cm.json", "lista de municípios"))
    registrar_lote(feitos)
    print(f"baixados {len(feitos)}; sem arquivo (404) {len(faltou)}")
    for u in faltou[:20]:
        print("  404", u)


if __name__ == "__main__":
    main()
